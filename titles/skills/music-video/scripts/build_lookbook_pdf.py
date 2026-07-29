"""Lookbook PDF: a grid of the candidate stills with scene labels + the lyric/section
each will cover — so the look and character consistency get reviewed BEFORE the
expensive animation step. Stills are ~10x cheaper than clips, so gate on this first.

Usage: python build_lookbook_pdf.py lookbook.json out.pdf
lookbook.json:
{
  "title": "Project — character",
  "subtitle": "model / notes",          # optional
  "stills_dir": "stills",
  "items": [ {"file": "1-hero.png", "title": "1 - Hero", "caption": "hook anchor"}, ... ]
}
"""
import sys, os, json, textwrap
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

cfg = json.load(open(sys.argv[1]))
OUT = sys.argv[2] if len(sys.argv) > 2 else "lookbook.pdf"
D = cfg.get("stills_dir", ".")
items = cfg["items"]
COLS, ROWS = 2, 4
per = COLS * ROWS
with PdfPages(OUT) as pdf:
    for p in range(0, len(items), per):
        chunk = items[p:p+per]
        fig = plt.figure(figsize=(8.5, 11))
        if p == 0:
            fig.suptitle(cfg.get("title", "Lookbook"), y=0.975, fontsize=20, fontweight="bold")
            if cfg.get("subtitle"):
                fig.text(0.5, 0.945, cfg["subtitle"], ha="center", fontsize=9.5, color="#555")
        for i, it in enumerate(chunk):
            ax = fig.add_subplot(ROWS, COLS, i+1)
            path = os.path.join(D, it["file"])
            if os.path.exists(path):
                ax.imshow(mpimg.imread(path))
            else:
                ax.text(0.5, 0.5, "(missing)\n"+it["file"], ha="center", va="center", fontsize=8)
            ax.axis("off")
            ax.set_title(it.get("title", it["file"]), fontsize=11, fontweight="bold", pad=3)
            cap = it.get("caption", "")
            if cap:
                ax.text(0.5, -0.08, "\n".join(textwrap.wrap(cap, 34)), transform=ax.transAxes,
                        ha="center", va="top", fontsize=8, color="#444")
        fig.subplots_adjust(left=0.04, right=0.96, top=0.90, bottom=0.05, wspace=0.08, hspace=0.42)
        pdf.savefig(fig); plt.close(fig)
print("PDF:", OUT)
