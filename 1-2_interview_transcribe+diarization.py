# %%
# # diarization + transcribe with whisperx
# https://github.com/m-bain/whisperX

import whisperx
import gc
from whisperx.diarize import DiarizationPipeline
from pathlib import Path


# %% set parameters
device = "cuda"
path_folder_base = Path("data_raw/interviews")
path_folder_user = path_folder_base / "P01"

audio_file = next(path_folder_user.glob("*.m4a"), None)
batch_size = 16 # reduce if low on GPU mem
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)

# %%
# 1. Transcribe with original whisper (batched)
model = whisperx.load_model("base", device, compute_type=compute_type)

# save model to local path (optional)
# model_dir = "/path/"
# model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)

audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size)
print(result["segments"]) # before alignment

# delete model if low on GPU resources
# import gc; import torch; gc.collect(); torch.cuda.empty_cache(); del model

# %%
# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

print(result["segments"]) # after alignment

# delete model if low on GPU resources
# import gc; import torch; gc.collect(); torch.cuda.empty_cache(); del model_a

# %%
# 3. Assign speaker labels
diarize_model = DiarizationPipeline(token="", device=device)

# add min/max number of speakers if known
diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=2)

result = whisperx.assign_word_speakers(diarize_segments, result)
print(diarize_segments)
print(result["segments"]) # segments are now assigned speaker IDs

# %%