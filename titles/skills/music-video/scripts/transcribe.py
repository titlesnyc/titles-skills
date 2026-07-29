"""Word-level lyric transcription. Optionally isolates the vocal stem first
(Demucs) for much better accuracy on produced tracks.
Usage: python transcribe.py <audio> [--isolate] [--model small|medium|large-v3]
Writes lyrics.json {lang, lines[], words[]} + lyrics.srt next to the audio.
Signal-only: gives words + timings, NOT melody/genre. Verify low-confidence words."""
import subprocess, sys, json, os
from faster_whisper import WhisperModel

audio = sys.argv[1]
isolate = "--isolate" in sys.argv
model_size = "small"
if "--model" in sys.argv: model_size = sys.argv[sys.argv.index("--model")+1]
outdir = os.path.dirname(os.path.abspath(audio)) or "."

src = audio
if isolate:
    subprocess.run([sys.executable,"-m","demucs","--two-stems=vocals","-n","htdemucs",
                    "-o", os.path.join(outdir,"stems"), audio], check=True)
    stem = os.path.splitext(os.path.basename(audio))[0]
    src = os.path.join(outdir,"stems","htdemucs",stem,"vocals.wav")
    print("vocal stem:", src)

model = WhisperModel(model_size, device="cpu", compute_type="int8")
segments,_ = model.transcribe(src, word_timestamps=True, beam_size=5,
                              vad_filter=False, condition_on_previous_text=False)
lines, words = [], []
for s in segments:
    lines.append({"start":round(s.start,2),"end":round(s.end,2),"text":s.text.strip()})
    for w in (s.words or []):
        words.append({"w":w.word.strip(),"start":round(w.start,2),
                      "end":round(w.end,2),"p":round(w.probability,2)})
# instrumental guard: Whisper hallucinates words over non-vocal audio, so flag weak transcripts
srcdur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],
    stdout=subprocess.PIPE,check=True).stdout.decode() or 1)
mean_p=(sum(w["p"] for w in words)/len(words)) if words else 0.0
wpm=len(words)/(srcdur/60) if srcdur else 0
instrumental=bool((len(lines)==0) or (wpm<6) or (mean_p<0.4 and wpm<25))
json.dump({"lines":lines,"words":words,"mean_confidence":round(float(mean_p),2),
           "words_per_min":round(float(wpm),1),"instrumental_suspected":instrumental},
          open(os.path.join(outdir,"lyrics.json"),"w"), indent=1)

def ts(t):
    h,m,s=int(t//3600),int(t%3600//60),t%60; return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".",",")
with open(os.path.join(outdir,"lyrics.srt"),"w") as f:
    for i,l in enumerate(lines,1): f.write(f"{i}\n{ts(l['start'])} --> {ts(l['end'])}\n{l['text']}\n\n")

print(f"lines={len(lines)} words={len(words)}  -> lyrics.json / lyrics.srt")
for l in lines: print(f"  [{l['start']:6.2f}-{l['end']:6.2f}] {l['text']}")
lc=[w for w in words if w["p"]<0.5]
if lc: print("low-confidence:", ", ".join(f"{w['w']}@{w['start']}" for w in lc[:40]))
if instrumental:
    print(f"\n**  LIKELY INSTRUMENTAL (mean_conf {mean_p:.2f}, {wpm:.0f} words/min) — do NOT trust "
          f"these words; drive pacing from analyze_audio.py sections instead.  **")
