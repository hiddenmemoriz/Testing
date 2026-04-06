import subprocess
import random
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import tempfile

QUOTES_FILE = Path("quotes.txt")
INPUT_VIDEO = Path("input/reel.mp4")
OUTPUT_VIDEO = Path("output/reel_with_text.mp4")

OUTPUT_FOLDER_ID = "1EVIHk24_3C7DsCLcYoQOdrM_T11UrkWH"
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Read quotes and pick a random one
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

print("Processing video...")
result = subprocess.run(cmd, shell=True)
if result.returncode != 0:
    raise RuntimeError("FFmpeg failed")
print("Video ready!")

# Upload to Google Drive
print("Uploading to Google Drive...")
sa_json = os.environ["GDRIVE_SERVICE_ACCOUNT_JSON"]
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    f.write(sa_json)
    tmp_path = f.name

creds = service_account.Credentials.from_service_account_file(tmp_path, scopes=SCOPES)
os.unlink(tmp_path)
service = build("drive", "v3", credentials=creds)

file_metadata = {
    "name": OUTPUT_VIDEO.name,
    "parents": [OUTPUT_FOLDER_ID]
}
media = MediaFileUpload(str(OUTPUT_VIDEO), mimetype="video/mp4", resumable=True)
uploaded = service.files().create(body=file_metadata, media_body=media, fields="id,name").execute()
print(f"Uploaded: {uploaded['name']} (id: {uploaded['id']})")
