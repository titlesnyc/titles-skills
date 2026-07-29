"""Tempo + beat grid + energy/section map for a track (numpy + ffmpeg only).
Usage: python analyze_audio.py <audio> [out.json]
Prints a summary and writes analysis.json {duration, bpm, beat_period, first_beat, sections}.
Note: BPM from onset autocorrelation often locks to a subdivision (e.g. 187.5 = 2x 93.75);
the 1.28s bar / 0.64s beat grid is clean either way."""
import subprocess, sys, json, numpy as np

path = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "analysis.json"
SR = 22050
raw = subprocess.run(["ffmpeg","-v","error","-i",path,"-ac","1","-ar",str(SR),"-f","f32le","-"],
                     stdout=subprocess.PIPE, check=True).stdout
x = np.frombuffer(raw, np.float32).astype(np.float64)
dur = len(x)/SR

hop=int(SR*0.02); win=int(SR*0.04); n=(len(x)-win)//hop
frames=np.array([x[i*hop:i*hop+win] for i in range(n)])
energy=np.sqrt((frames**2).mean(axis=1))+1e-9
onset=np.concatenate([[0],np.maximum(0,np.diff(np.log(energy)))]); fps=SR/hop
o=onset-onset.mean(); ac=np.correlate(o,o,mode="full")[len(o)-1:]
lag_lo,lag_hi=int(fps*60/180),int(fps*60/60)
best=lag_lo+int(np.argmax(ac[lag_lo:lag_hi])); bpm=60*fps/best
phase=int(np.argmax([onset[np.arange(p,len(onset),best)].sum() for p in range(best)]))
first_beat=phase/fps

secN=len(x)//SR
rms=np.array([np.sqrt((x[i*SR:(i+1)*SR]**2).mean()) for i in range(secN)])
norm=(rms-rms.min())/(np.ptp(rms)+1e-9)
sm=np.convolve(norm,np.ones(3)/3,mode="same"); d=np.abs(np.diff(sm))
bounds=[i for i in range(1,len(d)) if d[i]>d.mean()+1.2*d.std()]
merged=[]
for b in bounds:
    if not merged or b-merged[-1]>4: merged.append(b)
segs=[0]+merged+[len(norm)]
sections=[{"start":a,"end":b,"loudness":round(float(norm[a:b].mean()),2),
           "level":("LOW" if norm[a:b].mean()<.4 else "MID" if norm[a:b].mean()<.7 else "HIGH")}
          for a,b in zip(segs,segs[1:])]

res={"duration":round(dur,2),"bpm":round(bpm,1),"beat_period":round(60/bpm,3),
     "bar_4_4":round(60/bpm*4,3),"first_beat":round(first_beat,2),"sections":sections}
json.dump(res,open(out,"w"),indent=1)
blocks=" .:-=+*#%@"
spark="".join(blocks[min(9,int(v*9+.5))] for v in norm)
print(json.dumps({k:res[k] for k in ["duration","bpm","beat_period","bar_4_4","first_beat"]}))
print("energy/sec:",spark)
for s in sections: print(f"  {s['start']:3d}-{s['end']:3d}s {s['level']} ({s['loudness']})")
