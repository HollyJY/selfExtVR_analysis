# GPU-enabled environment for analysis, Whisper transcription, and diarization.
# Build: docker build -t selfextvr-analysis .
# Run:   docker run --rm --gpus all -it -e HF_TOKEN -v "$PWD":/workspace selfextvr-analysis
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/home/analyst/.cache/huggingface

# FFmpeg is required by Whisper and libsndfile provides reliable audio loading
# for pyannote/torchaudio.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        build-essential \
        ffmpeg \
        git \
        libsndfile1 \
        python3-pip \
        python3.10 \
        python3.10-venv \
    && rm -rf /var/lib/apt/lists/*

# CUDA 12.4 PyTorch wheels. Keep this separate from the remaining packages so
# Docker can reuse this large layer when analysis dependencies change.
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install \
        --index-url https://download.pytorch.org/whl/cu124 \
        torch==2.5.1 \
        torchaudio==2.5.1 \
        torchvision==0.20.1 \
    && python3 -m pip install \
        openai-whisper \
        pyannote.audio \
        huggingface_hub \
        ipykernel \
        jupyterlab \
        matplotlib \
        numpy \
        pandas \
        requests \
        scipy \
        seaborn \
        statsmodels

RUN useradd --create-home --shell /bin/bash analyst
WORKDIR /workspace
COPY --chown=analyst:analyst . /workspace
USER analyst

