# Package Fixes V3

This corrected package fixes execution issues found in the newly uploaded zip.

## Fixed

- Converted text files from Windows CRLF to Ubuntu-safe LF line endings.
- Added `.gitattributes` so future edits keep Linux scripts safe.
- Added `.venv/` to `.gitignore`.
- Replaced the Day 17M sample `.txt` media file with a non-empty `.mp3` placeholder so the media validator can pass.
- Added `scripts/day17m_strict_dry_run.sh` so Day 17M is one safe command.
- Added `--input` and `--output` support to `social_package_builder.py`.
- Added `--output` support to `postiz_queue_builder.py`.
- Added `--input` support and stricter failures to `postiz_queue_linter.py`.
- Corrected Postiz after-install documentation so Docker Compose checks run from `services/postiz/postiz-docker-compose`.
- Improved placeholder checks so the master `.env` domain placeholders are caught while optional heartbeat variables do not block unrelated setup.

## Verified Locally

The following local checks passed after the fixes:

```bash
python3 -m compileall -q scripts
bash -n scripts/*.sh
bash scripts/validate_all_scripts_preview.sh
bash scripts/day17m_strict_dry_run.sh
```

Live VPS checks still require the real VPS, DNS, Docker, Caddy, Postiz, Better Stack, OneDrive, and account credentials.
