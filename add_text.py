import subprocess
import random
from pathlib import Path

QUOTES_FILE = Path("quotes.txt")
INPUT_VIDEO = Path("input/reel.mp4")
OUTPUT_VIDEO = Path("output/reel_with_text.mp4")

lines = [l.strip() for l in QUOTES_FILE.read_text().splitlines() if l.strip()]
quote = random.choice(lines)
print(f"Quote selected: {quote}")

escaped = (quote
    .replace("'", r"\'")
    .replace(":", r"\:")
    .replace(",", r"\,")
    .replace("[", r"\[")
    .replace("]", r"\]"))

OUTPUT_VIDEO.parent.mkdir(exist_ok=True)

cmd = (
    'ffmpeg -i "' + str(INPUT_VIDEO) + '" '
    '-vf "drawtext='
    'fontsize=50:'
    'fontcolor=white:'
    "text='" + escaped + "':"
    'x=(w-text_w)/2:'
    'y=(h*0.75):'
    'box=1:boxcolor=black@0.5:boxborderw=15" '
    '-codec:a copy '
    '"' + str(OUTPUT_VIDEO) + '" -y'
)

result = subprocess.run(cmd, shell=True)
if result.returncode == 0:
    print(f"Done! Output: {OUTPUT_VIDEO}")
else:
    raise RuntimeError("FFmpeg failed")
