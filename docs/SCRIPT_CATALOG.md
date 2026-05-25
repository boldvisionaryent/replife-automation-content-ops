# RepLife Script Catalog

This catalog explains what each script in the full zip does.

All scripts are safe source files. They do not contain real credentials. Public posting, media upload, and Postiz API sending remain manual/supervised actions.

For step-by-step live Postiz sending, media upload, and external API activity, read `docs/POSTIZ_LIVE_ACTIONS_RUNBOOK.md`.

## Setup And Safety

| Script | Purpose |
|---|---|
| `check_protected_apps.sh` | Confirms existing Scheduler, Financial Command Center, n8n, Caddy, and LobeHub protection before setup. |
| `check_active_placeholders.sh` | Checks active `.env` and service files for placeholders by mode. |
| `git_commit_preflight.sh` | Blocks private/generated files before Git commits. |
| `pre_cron_validation.sh` | Runs protected-app, placeholder, Git, Python, and shell checks before cron. |
| `validate_all_scripts_preview.sh` | Runs setup-time preview validation. |
| `day17m_strict_dry_run.sh` | Runs the required Day 17M sample-only dry run and writes local test outputs under `outputs/test-results/day17m`. |
| `validate_all_scripts_pre_cron.sh` | Runs stricter validation immediately before cron. |
| `run_with_heartbeat.sh` | Runs a command and pings Better Stack only after success. |
| `setup_matomo_service.sh` | Creates Matomo service `.env`, validates the included compose file, pulls images, and starts Matomo. |
| `setup_uptime_kuma_service.sh` | Creates Uptime Kuma service `.env`, validates the included compose file, pulls image, and starts Uptime Kuma. |
| `setup_postiz_service.sh` | Clones the official Postiz compose repo, applies RepLife local-only port edits, validates, pulls, and starts Postiz. |
| `patch_postiz_compose_ports.py` | Edits the official Postiz compose file so Postiz and Temporal UI bind only to 127.0.0.1. |

## Planning And Reports

| Script | Purpose |
|---|---|
| `monthly_theme_validator.py` | Validates the monthly theme planning CSV. |
| `business_ownership_validator.py` | Checks generated outputs for valid business workstream ownership. |
| `content_idea_generator.py` | Creates draft content ideas. |
| `weekly_operations_report.py` | Creates a weekly operations review report. |
| `matomo_content_report.py` | Creates a Matomo content report placeholder or API-backed report when configured. |
| `top_content_analyzer.py` | Summarizes top-content review inputs. |
| `manual_social_metrics_import.py` | Imports manually exported social metrics CSV. |
| `content_batch_planner.py` | Creates a content batch plan. |
| `capacity_backlog_report.py` | Reviews disk capacity and backlog risk. |
| `owner_dashboard.py` | Creates a simple owner dashboard. |
| `published_content_confirmation_import.py` | Imports manually confirmed published-content rows. |
| `ai_usage_report.py` | Reports AI usage log count. |
| `github_models_model_check.py` | Checks GitHub Models environment configuration. |

## Media, Transcripts, And Drafts

| Script | Purpose |
|---|---|
| `external_asset_intake.py` | Registers external creative assets for later processing. |
| `validate_content_files.py` | Validates filenames before processing. |
| `file_naming_validator.py` | Compatibility wrapper for filename validation. |
| `media_spec_validator.py` | Checks media extension and size readiness. |
| `transcribe_media.py` | Creates safe transcript placeholders until faster-whisper is configured. |
| `transcript_repurposer.py` | Creates draft clips/captions/notes from transcripts. |
| `quote_card_generator.py` | Creates a simple SVG quote-card draft. |
| `shakeum_hero_song_pack.py` | Creates a SHAKEUM campaign draft pack. |
| `product_prompt_generator.py` | Creates internal Product Prompting drafts. |
| `product_prompt_public_language_checker.py` | Blocks commerce-style terms in public Product Prompting drafts. |
| `website_draft_generator.py` | Creates Markdown website drafts for manual WordPress copy. |
| `playlist_creator_outreach_drafts.py` | Creates draft outreach messages for manual sending. |
| `comment_reply_drafter.py` | Creates comment reply drafts for manual review and posting. |

## Social Packaging And Postiz

| Script | Purpose |
|---|---|
| `content_asset_manifest.py` | Builds a content asset manifest from approved media. |
| `social_package_builder.py` | Creates reviewable platform-specific social packages. |
| `social_package_index_builder.py` | Indexes social package files. |
| `platform_caption_linter.py` | Checks package/caption readiness. |
| `postiz_schedule_manifest.py` | Creates a monthly schedule worksheet. |
| `postiz_queue_archive.py` | Archives the previous Postiz queue when confirmed. |
| `postiz_queue_builder.py` | Creates queue rows that start as `approved=no`. |
| `postiz_queue_linter.py` | Checks queue readiness before media upload or loading. |
| `postiz_api_budget_guard.py` | Checks safe Postiz API request limits. |
| `postiz_api_smoke_test.py` | Checks Postiz API environment settings before live testing. |
| `postiz_integration_export.py` | Creates a worksheet for real Postiz integration IDs. |
| `approved_caption_to_queue_helper.py` | Helps map reviewed captions into queue rows. |
| `postiz_media_uploader.py` | Manual/supervised media upload safety gate. |
| `postiz_wizard_payload_checker.py` | Checks optional loader preview JSON. |
| `optional_postiz_loader.py` | Manual/supervised optional Postiz loader preview and safety gate. |
| `weekly_content_ops_runner.sh` | Runs the safe weekly workflow and stops before human review/send steps. |

## Archive And Backup

| Script | Purpose |
|---|---|
| `matomo_archive.sh` | Runs Matomo archive after manual tests pass. |
| `onedrive_media_archive.sh` | Copies selected outputs to OneDrive through rclone. |
| `onedrive_media_cleanup_after_archive.sh` | Dry-run-first cleanup helper. |
| `restic_onedrive_backup.sh` | Runs encrypted restic backup to OneDrive remote. |
| `onedrive_zip_backup.sh` | Creates an optional source zip/tar backup. |
| `onedrive_restore_test.sh` | Creates a restore-test folder and records the manual restore step. |
