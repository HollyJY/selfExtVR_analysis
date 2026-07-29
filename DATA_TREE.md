# Proposed Data Tree

```text
6_analysis/
├── README.md
├── DATA_TREE.md
├── 0_combine.py
├── 1-1_trial_wise_agency.ipynb
├── analysis.md
│
├── data_raw/
│   ├── HMD/
│   │   └── P01_session/
│   │       ├── expInfo_P01_session.csv
│   │       ├── resScale_P01_session.csv
│   │       ├── resPostQues_P01_session.csv
│   │       ├── YYYYMMDD_P01_log.csv
│   │       ├── YYYYMMDD_P01_log_eye.csv
│   │       ├── YYYYMMDD_P01_log_eye_raw.csv
│   │       └── trial_001/
│   ├── server/
│   │   └── P01_session/
│   │       ├── resQues_P01_pre.csv
│   │       ├── resQues_P01_post.csv
│   │       ├── extself_P01_*.m4a
│   │       ├── meta/
│   │       └── trial_001/
│   │           ├── user_1B_asr.txt
│   │           ├── user_1B_mic.wav
│   │           ├── user_2B_llm.txt
│   │           ├── user_2B_tts.wav
│   │           ├── timeline.jsonl
│   │           └── call_log.jsonl
│   └── interviews/
│       └── all_audio/
│           ├── extself_P01_**.m4a
│       └── P01/
│           ├── audio/
│           │   └── P01_interview_raw.m4a
│           ├── transcript/
│           │   ├── P01_interview_transcript_raw.txt
│           │   └── P01_interview_transcript_clean.txt
│           ├── notes/
│           │   └── P01_interview_notes.md
│           └── consent_or_admin/
│
├── data_intermediate/
│   └── P01/
│       ├── expInfo_P01.csv
│       ├── ans_llm_P01.csv
│       ├── resScale_P01.csv
│       ├── resQues_P01_pre.csv
│       ├── resQues_P01_post.csv
│       ├── resPostQues_P01.csv
│       ├── YYYYMMDD_P01_log.csv
│       ├── YYYYMMDD_P01_log_eye.csv
│       └── YYYYMMDD_P01_log_eye_raw.csv
│
├── data_analysis/
│   ├── participants.csv
│   ├── all_expInfo.csv
│   ├── all_ans_llm.csv
│   ├── all_resScale_session.csv
│   ├── trial_wise_responses.csv
│   ├── trial_wise_SoP.csv
│   ├── interview_index.csv
│   ├── interview_segments.csv
│   └── codebook_interviews.csv
│
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── models/
│
└── docs/
    ├── data_dictionary.md
    ├── processing_log.md
    └── exclusion_log.md
```

## How This Maps To The Current Folders

Current folder | Proposed role
--- | ---
`data_extSelf_HMD/` | Raw HMD data. Equivalent to `data_raw/HMD/`.
`data_extSelf_server/` | Raw server/audio/text data. Equivalent to `data_raw/server/`.
`data_extSelf_preprocessed/` | Participant-level intermediate data. Equivalent to `data_intermediate/`.
`data_extSelf/` | Stacked analysis-ready CSVs. Equivalent to `data_analysis/`.

You do not need to rename everything immediately. The important part is to use these roles consistently.

## What To Stack

Stack data when every participant has the same schema and one row means the same thing.

Good stacked files:

- `participants.csv`: one row per participant.
- `all_expInfo.csv`: one row per trial with condition, scene, voice, and generation rule.
- `all_ans_llm.csv`: one row per trial with original ASR response and LLM output.
- `all_resScale_session.csv`: one row per scale response item.
- `trial_wise_responses.csv`: one row per participant-trial-question response.
- `trial_wise_SoP.csv`: one row per participant/trial/SoP measure, if this is how the file is defined.
- `interview_segments.csv`: one row per interview excerpt/segment.
- `codebook_interviews.csv`: one row per qualitative code.

Keep data separate by participant when files are raw, large, personal, or have irregular structure.

Do not stack these raw files:

- Raw `.wav` / `.m4a` audio.
- Raw eye-tracking logs, unless you create a separate derived feature table.
- Raw `call_log.jsonl` and `timeline.jsonl`.
- Raw interview audio.
- Raw interview transcripts, unless you also create a structured `interview_segments.csv`.

## Recommended Interview Tables

Keep full transcripts as individual text files:

```text
data_raw/interviews/P01/transcript/P01_interview_transcript_clean.txt
data_raw/interviews/P02/transcript/P02_interview_transcript_clean.txt
```

Then create a stacked interview index:

```text
data_analysis/interview_index.csv
```

Suggested columns:

```text
pp,interview_date,audio_file,raw_transcript_file,clean_transcript_file,notes_file,transcribed_by,checked_by,remarks
```

For qualitative analysis, create a stacked segment table:

```text
data_analysis/interview_segments.csv
```

Suggested columns:

```text
segment_id,pp,turn_id,speaker,start_time,end_time,quote,summary,code_primary,code_secondary,memo
```

For the codebook:

```text
data_analysis/codebook_interviews.csv
```

Suggested columns:

```text
code,definition,include_when,exclude_when,example_quote
```

## Rule Of Thumb

Keep two versions of the data:

1. Raw participant folders: preserved exactly, one folder per participant.
2. Analysis tables: stacked CSVs with `pp` and, when needed, `trial`, `question_index`, `segment_id`, or `turn_id`.

This gives you both preservation and easy analysis. If something goes wrong in a stacked file, you can always trace it back to the raw participant folder.

