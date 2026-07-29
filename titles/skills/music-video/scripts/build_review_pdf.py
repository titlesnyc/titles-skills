"""Storyboard review PDF: one row per shot with a thumbnail, its time in the final
cut, the scene label, and the lyric line(s) playing over that span. Lets you review
transcription + scene alignment at a glance.
Usage: python build_review_pdf.py edl.json lyrics.json out.pdf [title]
edl.json is written by assemble.py; lyrics.json by transcribe.py (pass "" to skip lyrics)."""
import sys, os, json, subprocess, textwrap, shutil, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

edl=json.load(open(sys.argv[1])); segs=edl["segments"]
lyr=json.load(open(sys.argv[2]))["lines"] if len(sys.argv)>2 and sys.argv[2] and os.path.exists(sys.argv[2]) else []
OUT=sys.argv[3] if len(sys.argv)>3 else "storyboard.pdf"
TITLE=sys.argv[4] if len(sys.argv)>4 else "Music-video storyboard"
work=os.path.dirname(os.path.abspath(OUT)); th=os.path.join(work,".mvthumbs"); os.makedirs(th,exist_ok=True)

rows=[]
for s in segs:
    grab=min(s["in"]+s["dur"]/2, 4.9)
    p=os.path.join(th,f"t{s['i']:02d}.png")
    subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{grab:.3f}","-i",s["file"],"-frames:v","1",
        "-vf","scale=360:360:force_original_aspect_ratio=increase,crop=360:360",p],check=True)
    over=[l["text"] for l in lyr if l["start"]<s["end"]-0.05 and l["end"]>s["start"]+0.05]
    rows.append((s,p," / ".join(over) if over else "(instrumental)"))

PER=4
with PdfPages(OUT) as pdf:
    fig=plt.figure(figsize=(8.5,11))
    fig.text(0.5,0.8,TITLE,ha="center",size=24,weight="bold")
    meta=[f"track duration: {edl['duration']}s","",f"shots: {len(segs)}",
          "every shot starts at its motion-onset; cuts snap to the beat grid",
          "each row: thumbnail · time in final cut · scene · lyric over that span"]
    fig.text(0.12,0.62,"\n".join(meta),va="top",size=11,family="monospace")
    pdf.savefig(fig); plt.close(fig)
    for p0 in range(0,len(rows),PER):
        chunk=rows[p0:p0+PER]
        fig,axes=plt.subplots(len(chunk),2,figsize=(8.5,11),
            gridspec_kw={"width_ratios":[1,1.6],"hspace":0.35,"wspace":0.05})
        if len(chunk)==1: axes=np.array([axes])
        for r,(s,img,txt) in enumerate(chunk):
            axes[r,0].imshow(mpimg.imread(img)); axes[r,0].axis("off"); axes[r,1].axis("off")
            body=(f"Shot {s['i']+1:>2}  [{s['start']:5.2f}-{s['end']:5.2f}] ({s['dur']:.2f}s)\n"
                  f"SCENE: {s['label']}\n\n"+"\n".join(textwrap.wrap('“'+txt+'”',42)))
            axes[r,1].text(0,0.5,body,va="center",size=10.5,family="monospace")
        pdf.savefig(fig); plt.close(fig)
shutil.rmtree(th, ignore_errors=True)
print("PDF:",OUT)
