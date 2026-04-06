import subprocess
import random
from pathlib import Path

QUOTES_FILE = Path("quotes.txt")
INPUT_VIDEO = Path("input/reel.mp4")
OUTPUT_VIDEO = Path("output/reel_with_text.mp4")

# Read quotes and pick a random one
lines = [l.strip() for l in QUOTES_FILE.read_text().splitlines() if l.strip()]
quote = random.choice(lines)
print(f"Quote selected: {quote}")

# Escape special characters for ffmpeg
escaped = (quote
    .replace("'", r"\'")
    .replace(":", r"\:")
    .replace(",", r"\,")
    .replace("[", r"\[")
    .replace("]", r"\]"))

# Create output folder
OUTPUT_VIDEO.parent.mkdir(exist_ok=True)

# Add text to video using ffmpeg
cmd = (
    f'ffmpeg -i "{INPUT_VIDEO}" '
    f'-vf "drawtext='
    f'fontsize=50:'
    f'fontcolor=white:'
    f'text=\'{escaped}\':"
    f'x=(w-text_w)/2:'
    f'y=(h*0.75):'
    f'box=1:boxcolor=black@0.5:boxborderw=15" '
    f'-codec:a copy '
    f'"{OUTPUT_VIDEO}" -y'
)

result = subprocess.run(cmd, shell=True)
if result.returncode == 0:
    print(f"✅ Done! Output: {OUTPUT_VIDEO}")
else:
    raise RuntimeError("FFmpeg failed")
