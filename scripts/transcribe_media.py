#!/usr/bin/env python3
import argparse
from pathlib import Path
from replife_common import OUTPUTS, ensure_dirs

parser = argparse.ArgumentParser(description="Create transcript placeholders for approved media. Replace with faster-whisper when configured.")
parser.add_argument("file")
parser.add_argument("--model-size", default="small")
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
ensure_dirs()
source = Path(args.file)
out_txt = OUTPUTS / "transcripts" / f"{source.stem}.txt"
out_srt = OUTPUTS / "transcripts" / f"{source.stem}.srt"
if args.dry_run:
    print(f"DRY RUN: would transcribe {source} with model {args.model_size}")
else:
    out_txt.write_text(f"Transcript placeholder for {source.name}\nReplace this with reviewed transcript text.\n", encoding="utf-8")
    out_srt.write_text("1\n00:00:00,000 --> 00:00:05,000\nTranscript placeholder. Review before repurposing.\n", encoding="utf-8")
    print(f"Created transcript files: {out_txt}, {out_srt}")
