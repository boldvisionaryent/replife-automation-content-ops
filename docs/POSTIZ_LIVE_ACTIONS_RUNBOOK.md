# Postiz Live Actions Runbook

Use this only after the normal RepLife setup is complete and Postiz is installed.

This runbook covers the three actions that require extra care:

1. Live Postiz sending.
2. Media upload.
3. External API activity.

Default rule:

```env
POSTIZ_API_ENABLED=no
```

Keep it set to `no` unless you are intentionally running a supervised session.

## Safety Rules

Never run live sending, media upload, or external API actions until all of these are true:

1. The content has been reviewed by a human.
2. The queue row is marked `approved=yes`.
3. Any media row is marked `upload_ready=yes`.
4. The caption and queue linters pass.
5. The Postiz API smoke test passes.
6. The Postiz API budget guard passes.
7. A dry-run payload preview has been created.
8. The preview JSON opens and looks correct.
9. The content appears correct inside Postiz after loading or scheduling.
10. `POSTIZ_API_ENABLED` is set back to `no` immediately after the session.

Never add these actions to cron or n8n:

- `optional_postiz_loader.py --confirm-send`
- `postiz_media_uploader.py --confirm-upload`
- any media upload sender
- any public posting sender
- any customer-service, DM, auto-reply, outreach-send, or commerce action

## Part A - Prepare The VPS Session

Run:

```bash
cd ~/replife-backend
source .venv/bin/activate
export PYTHONPATH="$PWD"
bash scripts/check_protected_apps.sh
```

Expected:

```text
Protected-app preflight passed.
```

If this fails, stop.

## Part B - Confirm Postiz In The Browser

Open:

```text
https://social.YOURDOMAIN.com
```

Check:

1. You can log in.
2. Registration is not publicly open.
3. The needed social channel is connected.
4. The calendar opens.
5. You can manually create or view a draft/scheduled post.

If the platform is disconnected, stop and reconnect it inside Postiz before using any loader.

## Part C - Confirm Queue Review

Run:

```bash
cd ~/replife-backend
python scripts/postiz_queue_linter.py
python scripts/postiz_queue_linter.py --approved-only
```

Open the queue file:

```bash
nano outputs/social-queues/approved_postiz_queue.csv
```

For each row that may be sent:

```text
approved=yes
upload_ready=yes, only if media upload is needed
caption is final
platform is correct
scheduled time is correct
integration/channel is correct if used
```

Save nano:

```text
CTRL + O
ENTER
CTRL + X
```

## Part D - External API Readiness

Run:

```bash
python scripts/postiz_api_budget_guard.py
python scripts/postiz_api_smoke_test.py
python scripts/postiz_integration_export.py
```

Expected:

- Budget guard passes.
- Smoke test configuration is ready.
- Integration export worksheet is created.

Then check:

```bash
nano outputs/social-queues/postiz_integrations_export.csv
```

Replace sample integration IDs with real connected Postiz integration/channel IDs only after confirming them in Postiz.

## Part E - Create A Payload Preview

Run:

```bash
mkdir -p outputs/social-queues/previews
python scripts/optional_postiz_loader.py \
  --dry-run \
  --payload-preview-output outputs/social-queues/previews/postiz-payload-preview.json
python -m json.tool outputs/social-queues/previews/postiz-payload-preview.json \
  > /tmp/postiz-payload-preview.checked.json
python scripts/postiz_wizard_payload_checker.py --approved-only
```

Open the preview:

```bash
nano outputs/social-queues/previews/postiz-payload-preview.json
```

Check:

1. The platform is correct.
2. The caption is correct.
3. The media information is correct if present.
4. The schedule/time is correct if present.
5. No commerce, customer-service, DM, auto-reply, or store information appears.

If anything looks wrong, stop and fix the queue before continuing.

## Part F - Supervised Media Upload

Use this only for rows where media upload is required.

First dry-run:

```bash
python scripts/postiz_media_uploader.py --dry-run
```

If the dry-run looks correct, temporarily enable the supervised API session:

```bash
nano .env
```

Change:

```env
POSTIZ_API_ENABLED=no
```

to:

```env
POSTIZ_API_ENABLED=yes
```

Save nano.

Run the upload safety gate:

```bash
python scripts/postiz_media_uploader.py --confirm-upload
```

Immediately turn API mode back off:

```bash
nano .env
```

Change:

```env
POSTIZ_API_ENABLED=yes
```

back to:

```env
POSTIZ_API_ENABLED=no
```

Then open Postiz in the browser and confirm the uploaded media appears as expected.

## Part G - Supervised Live Postiz Sending

Prefer manual scheduling in Postiz when possible. Use this only after all review and preview checks pass.

First dry-run:

```bash
python scripts/optional_postiz_loader.py \
  --dry-run \
  --payload-preview-output outputs/social-queues/previews/postiz-payload-preview.json
```

Review the preview again:

```bash
python -m json.tool outputs/social-queues/previews/postiz-payload-preview.json \
  > /tmp/postiz-payload-preview.checked.json
```

Temporarily enable API mode:

```bash
nano .env
```

Change:

```env
POSTIZ_API_ENABLED=no
```

to:

```env
POSTIZ_API_ENABLED=yes
```

Run only a small supervised send:

```bash
python scripts/optional_postiz_loader.py \
  --confirm-send \
  --limit 3 \
  --payload-preview-output outputs/social-queues/previews/postiz-payload-preview.json
```

Immediately turn API mode back off:

```bash
nano .env
```

Change:

```env
POSTIZ_API_ENABLED=yes
```

back to:

```env
POSTIZ_API_ENABLED=no
```

Then open Postiz:

```text
https://social.YOURDOMAIN.com
```

Confirm:

1. The post exists in Postiz.
2. The caption is correct.
3. The media is correct.
4. The platform/channel is correct.
5. The scheduled time is correct.
6. Nothing was duplicated.

If anything is wrong, do not send more rows.

## Part H - After The Session

Run:

```bash
grep POSTIZ_API_ENABLED .env
python scripts/postiz_queue_linter.py --approved-only
bash scripts/check_protected_apps.sh
```

Expected:

```text
POSTIZ_API_ENABLED=no
```

Record the session in Microsoft Lists:

- date
- platform
- rows reviewed
- rows uploaded
- rows sent or scheduled
- issues found
- next safe step

## Part I - Rollback Or Stop

If something goes wrong:

1. Stop sending.
2. Set `POSTIZ_API_ENABLED=no`.
3. Open Postiz in the browser.
4. Delete or correct draft/scheduled items manually inside Postiz.
5. Comment out any related cron line if one exists.
6. Record the issue in Microsoft Lists.
7. Fix the queue and run dry-run preview again before trying another supervised session.

Remember: optional Postiz loading is never unattended. Manual Postiz scheduling is always the fallback.
