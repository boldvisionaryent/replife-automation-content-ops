# Package Fixes V4

This V4 package is the full RepLife automation content-operations zip package with the V3 execution fixes retained and the full-length V4 manual alignment applied.

## Retained V3 Execution Fixes

- Converted text/script files to LF line endings for Ubuntu Bash compatibility.
- Added `.gitattributes` to keep shell, Python, Markdown, YAML, CSV, and environment files Linux-safe.
- Added `.venv/` to `.gitignore`.
- Added `scripts/day17m_strict_dry_run.sh` so Day 17M can be run with one clear command.
- Added sample media under `inputs/end-to-end-dry-run/media/sample.mp3` so the media validator has a safe sample input.
- Updated `social_package_builder.py`, `postiz_queue_builder.py`, and `postiz_queue_linter.py` to support explicit input/output paths required by the Day 17M strict dry run.
- Improved active placeholder checks so the real `.env` is checked before activating runtime, AI, backup, Postiz API, or cron features.

## V4 Manual Alignment

- The full-length V4 PDF/DOCX manual preserves the original 66-page manual detail while updating setup commands to use this V4 package.
- The manual now uses `bash scripts/day17m_strict_dry_run.sh` as the preferred Day 17M command.
- The manual keeps the original content-operations boundary: no commerce, no customer-service automation, no DM/comment auto-reply automation, no unattended Postiz sending.

## Safe Validation Commands

From `~/replife-backend` on the VPS after unzip:

```bash
chmod +x scripts/*.sh
bash -n scripts/*.sh
python3 -m compileall -q scripts
bash scripts/validate_all_scripts_preview.sh
bash scripts/day17m_strict_dry_run.sh
```

These commands do not publish, schedule, upload, send, reply, touch commerce, or modify protected apps.
