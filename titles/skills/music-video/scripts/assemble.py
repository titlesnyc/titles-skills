"""Beat/lyric-aligned assembler. Reads an edit.json, cuts each shot starting at
its detected motion-onset (so no clip opens on a static frame), snaps the cut grid
onto the downbeat (phase), stretches a shot only when it must outrun its clip,
concatenates, and muxes the track with a fade-out. Also writes edl.json (resolved
timeline) for the storyboard PDF.

edit.json schema:
{
  "audio": "path/to/track.mp3",
  "clips_dir": "path/to/clips",
  "out": "path/to/out.mp4",
  "fps": 24, "phase": 0.14, "fade_out": 0.6,
  "out_w": 1440, "out_h": 1440, "fit": "crop",   # e.g. 1080x1920 + "pad" for 9:16
  "clips":  {"beach": "01-beach.mp4", ...},      # clip lengths are auto-detected
  "labels": {"beach": "Beach", ...},
  "edl":    [["beach", 5.12], ["herowave", 3.20], ..., ["heroraise", null]]
      # duration in seconds; the single null shot fills to the track's end
}
Usage: python assemble.py edit.json
"""
import subprocess, os, sys, json, shutil, numpy as np

cfg = json.load(open(sys.argv[1]))
AUDIO=cfg["audio"]; CD=cfg["clips_dir"]; OUT=cfg["out"]
FPS=int(cfg.get("fps",24)); PHASE=cfg.get("phase",0.14); FADE=cfg.get("fade_out",0.6)
OUT_W=int(cfg.get("out_w",1440)); OUT_H=int(cfg.get("out_h",1440)); FIT=cfg.get("fit","crop")
FILES=cfg["clips"]; LABELS=cfg.get("labels",{}); EDL=cfg["edl"]

# fail loud on missing inputs rather than a cryptic ffmpeg error mid-run
if not os.path.exists(AUDIO): raise SystemExit(f"assemble: audio not found: {AUDIO}")
miss=[v for v in FILES.values() if not os.path.exists(os.path.join(CD,v))]
if miss: raise SystemExit(f"assemble: missing clips in {CD}: {miss}")

work=os.path.dirname(os.path.abspath(OUT)); os.makedirs(work,exist_ok=True)
tmp=os.path.join(work,".mvwork"); segdir=os.path.join(tmp,"seg"); os.makedirs(segdir,exist_ok=True)
# output frame: 'crop' fills the frame (may trim edges); 'pad' letterboxes (keeps the whole frame)
_geom=(f"scale={OUT_W}:{OUT_H}:force_original_aspect_ratio=decrease,pad={OUT_W}:{OUT_H}:(ow-iw)/2:(oh-ih)/2:color=black"
       if FIT=="pad" else
       f"scale={OUT_W}:{OUT_H}:force_original_aspect_ratio=increase,crop={OUT_W}:{OUT_H}")
VF=f"{_geom},fps={FPS},format=yuv420p"

def onset(f,W=64):
    raw=subprocess.run(["ffmpeg","-v","error","-i",f,"-vf",f"scale={W}:{W},format=gray",
                        "-f","rawvideo","-"],stdout=subprocess.PIPE,check=True).stdout
    v=np.frombuffer(raw,np.uint8).astype(np.float32).reshape(-1,W*W)
    dd=np.abs(np.diff(v,axis=0)).mean(axis=1)
    return (int(np.argmax(dd>0.35*dd.max()))+1+2)/FPS
def clipdur(f):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",f],stdout=subprocess.PIPE,check=True).stdout.decode() or 0)
ONSET={k:onset(os.path.join(CD,v)) for k,v in FILES.items()}
REAL={k:clipdur(os.path.join(CD,v)) for k,v in FILES.items()}   # actual clip length, not assumed

dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
    "-of","csv=p=0",AUDIO],stdout=subprocess.PIPE,check=True).stdout.decode())
# EDL entry: [key, duration] or [key, duration, in_override] (seconds into the clip)
NORM=[(e[0], e[1], (e[2] if len(e)>2 else None)) for e in EDL]
durs=[(d+(PHASE if i==0 else 0.0)) if d is not None else None for i,(_,d,_o) in enumerate(NORM)]
durs[-1]=round(dur-sum(x for x in durs if x is not None),3)

concat=open(os.path.join(tmp,"concat.txt"),"w"); timeline=[]; t=0.0
for i,((c,_,ovr),d) in enumerate(zip(NORM,durs)):
    f=os.path.join(CD,FILES[c])
    cl=REAL[c]
    inp=ONSET[c] if ovr is None else float(ovr)
    inp=max(0.0,min(inp,max(0.0,cl-0.1)))            # keep in-point inside the actual clip
    avail=max(0.1,cl-inp); seg=os.path.join(segdir,f"s{i:02d}.mp4")
    if d<=avail:
        vf=VF; args=["-ss",f"{inp:.3f}","-i",f,"-t",f"{d:.3f}"]
    else:
        vf=f"setpts={d/avail:.4f}*PTS,{VF}"; args=["-ss",f"{inp:.3f}","-i",f,"-t",f"{avail:.3f}"]
    subprocess.run(["ffmpeg","-y","-v","error",*args,"-vf",vf,"-t",f"{d:.3f}","-an",
        "-c:v","libx264","-crf","18","-preset","veryfast","-video_track_timescale",str(FPS*1000),seg],check=True)
    concat.write(f"file '{seg}'\n")
    timeline.append({"i":i,"key":c,"label":LABELS.get(c,c),"file":f,
                     "in":round(inp,3),"dur":round(d,3),"start":round(t,3),"end":round(t+d,3)})
    t+=d
concat.close()
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0",
    "-i",os.path.join(tmp,"concat.txt"),"-c","copy",os.path.join(tmp,"video.mp4")],check=True)
subprocess.run(["ffmpeg","-y","-v","error","-i",os.path.join(tmp,"video.mp4"),"-i",AUDIO,
    "-map","0:v:0","-map","1:a:0","-af",f"afade=t=out:st={dur-FADE:.2f}:d={FADE}",
    "-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{dur:.3f}","-movflags","+faststart",OUT],check=True)
json.dump({"audio":AUDIO,"clips_dir":CD,"duration":round(dur,3),"segments":timeline},
          open(os.path.join(work,"edl.json"),"w"),indent=1)
shutil.rmtree(tmp, ignore_errors=True)
print(f"OK  {OUT}  {dur:.2f}s  {len(EDL)} shots  -> edl.json written")
