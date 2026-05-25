# Cron Policy

Cron is enabled only after manual validation passes.

## Required Before Any Cron Job

1. The command runs manually.
2. The command logs to a known log file.
3. Dry-run mode passes, if available.
4. The command does not touch protected apps.
5. The command does not touch commerce.
6. The command does not require human judgment.
7. The rollback/disable step is documented.
8. `bash scripts/pre_cron_validation.sh` passes.
9. Feature-specific validation passes when needed:
   - backups: `bash scripts/pre_cron_validation.sh backup`
   - AI reports/scripts: `bash scripts/pre_cron_validation.sh ai`
   - Postiz API checks: `bash scripts/pre_cron_validation.sh postiz-api`

## Never Add To Cron

- optional Postiz loader with confirm-send behavior
- media upload sender
- public posting without approval
- commerce scripts
- customer-service scripts
- comment auto-reply scripts
- DM automation
- Docker prune commands
- global Docker restart commands

## Safe Pattern

Cron should run wrapper scripts only. Wrapper scripts should:

- `cd ~/replife-backend`
- activate `.venv` when Python is needed
- export `PYTHONPATH="$PWD"`
- write logs under `logs/`
- call Better Stack heartbeat only after the job succeeds
