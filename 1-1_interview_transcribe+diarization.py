# %%
# # diarization + transcribe with whisperx
# https://github.com/m-bain/whisperX

import whisperx
import gc
import json
from whisperx.diarize import DiarizationPipeline
from pathlib import Path
import hf_transfer

from dotenv import load_dotenv
import os


# %%
load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")


# %% set parameters
device = "cuda"
path_folder_base = Path(__file__).resolve().parent / "data_raw" / "interviews"
li_folders = sorted([f for f in path_folder_base.iterdir() if f.is_dir()])
print(f"Found {len(li_folders)} interview folders under {path_folder_base}")

li_none_audio = [f for f in li_folders if not any(f.rglob("*.m4a")) and not any(f.rglob("*.WAV"))]
print(f"Found {len(li_none_audio)} folders with no .m4a or .WAV files: {[f.name for f in li_none_audio]}")

# %%
def format_interview_transcript(segments):
    """Format diarized WhisperX segments into a readable interview transcript."""
    speaker_aliases = {}
    turns = []
    for segment in segments:
        text = segment.get("text", "").strip()
        if not text:
            continue

        raw_speaker = segment.get("speaker") or segment.get("speaker_id") or "UNKNOWN"
        if raw_speaker not in speaker_aliases:
            alias_index = len(speaker_aliases)
            speaker_aliases[raw_speaker] = chr(ord("A") + alias_index) if alias_index < 26 else f"SPEAKER_{alias_index + 1}"

        speaker = speaker_aliases[raw_speaker]
        start = segment.get("start")
        end = segment.get("end")
        turns.append({
            "speaker": speaker,
            "start": start,
            "end": end,
            "text": text,
        })

    def time_stamp(value):
        if value is None:
            return "?"
        minutes, seconds = divmod(float(value), 60)
        return f"{int(minutes):02d}:{seconds:06.3f}"

    raw_lines = []
    clean_lines = []
    last_speaker = None
    for turn in turns:
        raw_lines.append(
            f"[{time_stamp(turn['start'])} - {time_stamp(turn['end'])}] {turn['speaker']}: {turn['text']}"
        )
        if clean_lines and last_speaker == turn["speaker"]:
            clean_lines[-1] = f"{turn['speaker']}: {clean_lines[-1][3:]} {turn['text']}"
        else:
            clean_lines.append(f"{turn['speaker']}: {turn['text']}")
        last_speaker = turn["speaker"]

    return "\n".join(raw_lines) + "\n", "\n".join(clean_lines) + "\n"

# %%
batch_size = 16 # reduce if low on GPU mem
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)

# load models outside the loop to avoid reloading for each interview
model = whisperx.load_model("base", device, compute_type=compute_type)
diarize_model = DiarizationPipeline(token=HF_API_TOKEN, device=device)

# %%
for pp in li_folders:
    # pp = "P01"
    path_folder_user = path_folder_base / pp
    path_folder_audio = path_folder_user / "audio"
    path_folder_transcripts = path_folder_user / "transcript"
    print(path_folder_transcripts)

    pp_id = path_folder_user.name

    audio_file = next(path_folder_user.rglob("*.m4a"), None)
    audio_file = audio_file or next(path_folder_user.rglob("*.WAV"), None)
    if audio_file is None:
        # raise FileNotFoundError(f"No .m4a file found under {path_folder_user}")
        print(f"No .m4a or .WAV file found under {path_folder_user}, skipping...")
        continue

    #
    # 1. Transcribe with original whisper (batched)
    # model = whisperx.load_model("base", device, compute_type=compute_type) ## move to outside loop -> load only once

    # save model to local path (optional)
    # model_dir = "/path/"
    # model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)

    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    # print(result["segments"]) # before alignment

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)

    # delete model if low on GPU resources
    # import gc; import torch; gc.collect(); torch.cuda.empty_cache(); del model

    #
    # 2. Align whisper output
    # model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)

    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    # print(result["segments"]) # after alignment

    # delete model if low on GPU resources
    # import gc; import torch; gc.collect(); torch.cuda.empty_cache(); del model_a

    #
    # 3. Assign speaker labels
    # diarize_model = DiarizationPipeline(token=HF_API_TOKEN, device=device)

    # add min/max number of speakers if known
    diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=2)

    result = whisperx.assign_word_speakers(diarize_segments, result)
    # print(diarize_segments)
    # print(result["segments"]) # segments are now assigned speaker IDs

    # 4. Save results
    path_folder_transcripts.mkdir(parents=True, exist_ok=True)
    print(path_folder_transcripts)
    path_file_transcript_json = path_folder_transcripts / f"{pp_id}_interview_transcript_raw.json"
    path_file_transcript_raw_txt = path_folder_transcripts / f"{pp_id}_interview_transcript_raw.txt"
    path_file_transcript_clean_txt = path_folder_transcripts / f"{pp_id}_interview_transcript_clean.txt"
    
    # print(path_file_transcript_json)

    raw_transcript_text, clean_transcript_text = format_interview_transcript(result["segments"])

    with path_file_transcript_json.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    path_file_transcript_raw_txt.write_text(raw_transcript_text, encoding="utf-8")
    path_file_transcript_clean_txt.write_text(clean_transcript_text, encoding="utf-8")
    print(f"Transcripts saved to {path_folder_transcripts}")
    # %%
