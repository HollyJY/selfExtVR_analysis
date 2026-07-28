# %% [markdown]
# # what to do in the script
# 1. put audio files into data_raw/interviews
# 2. transcribe the audio files into text files and put them into data_raw/interviews
# 
# ---
# 
# ├── data_raw/
# │   └── interviews/
# │       └── P01/
# │           ├── audio/
# │           │   └── P01_interview_raw.m4a
# │           ├── transcript/
# │           │   ├── P01_interview_transcript_raw.txt
# │           │   └── P01_interview_transcript_clean.txt
# │           ├── notes/
# │           │   └── P01_interview_notes.md
# │           └── consent_or_admin/

# %% call service to transcribe the audio files

from turtle import st

import requests
from pathlib import Path

url = "http://192.168.37.177:7001/api/v1/stt"

folder_path = Path("/Users/holly/Library/Mobile Documents/iCloud~md~obsidian/Documents/zjy/1-Project/intern2/6_analysis/data_raw/interviews")

# %% iterate through all participant folders in the interviews folder
for pp_folder in Path(folder_path).iterdir():
    if pp_folder.is_dir():
        audio_folder = pp_folder / "audio"
        if audio_folder.exists():
            audio_file = next(audio_folder.glob("*.m4a"), None)
            # print(audio_file)
            if audio_file:
                with open(audio_file, "rb") as f:
                    files = {
                        "audio": (audio_file.name, f, "audio/m4a")
                    }
                    data = {
                        "session_id": "test_asr_interview",
                        "trial_id": pp_folder.name[1:],
                        "lang": "en",   # or "auto"
                    }

                    r = requests.post(url, files=files, data=data, timeout=60)

                print("status:", r.status_code)
                print(r.text)
                r.raise_for_status()
                result = r.json()
                print("asr_text_path:", result.get("asr_text_path"))


# %%
