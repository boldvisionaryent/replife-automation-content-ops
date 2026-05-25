---
title: "RepLife Automation Complete Replacement Manual v4 - Step-by-Step Non-Technical Setup Guide"
subtitle: "Content Operations Only - No Commerce Automation"
author: "RepLife Automation Package"
date: "May 24, 2026"
---

# RepLife Automation Complete Replacement Manual v4 - Step-by-Step Setup Guide

**Setup file to use:** `replife-automation-content-ops-full-vps-v4-step-by-step.zip`  
**Server:** Ubuntu 24.04 VPS  
**Audience:** non-technical operator using MobaXterm or another SSH/SFTP tool  
**Main rule:** copy one command block at a time, read the expected result, and stop instead of guessing when the check does not match.

This guide improves the previous V4 manual by removing repeated reference material from the setup sections and turning the installation into a direct, numbered, step-by-step procedure. Reference material is still included later, but the setup section tells you exactly what to do next and how to check that it worked.

## What this system does

RepLife Automation supports RepLife content operations. It helps with planning, draft generation, validation, reports, social scheduling review, backups, and monitoring.

## What this system does not do

This system does not run store operations, payments, customer service, refund handling, order handling, checkout, shipping, taxes, coupons, Gelato fulfillment, WooCommerce automation, customer DMs, comment auto-replies, or unattended public posting. WordPress/WooCommerce/Gelato remain on IONOS and outside this VPS automation setup.

## Protected existing apps

These already-running apps must not be rebuilt or reconfigured by this setup:

| Existing app | Current rule |
|---|---|
| Task Scheduler App | Check only. Do not install, rebuild, or reconfigure. |
| Financial Command Center | Check only. Do not install, rebuild, or reconfigure. |
| LobeHub | Check only. Do not reinstall or reuse its ports. |
| Existing n8n | Reuse only for RepLife reminders and light coordination. Do not install another n8n. |
| Caddy | Preserve existing site blocks. Back up and validate before reload. |

## New RepLife services configured by this guide

| Service | Purpose | Local-only target | Public URL |
|---|---|---:|---|
| Matomo | Content analytics only | `127.0.0.1:8081` | `https://analytics.YOURDOMAIN.com` |
| Existing n8n | Reminders/light checks only | `127.0.0.1:5678` | `https://automations.YOURDOMAIN.com` |
| Uptime Kuma | Visual service monitoring | `127.0.0.1:3001` | `https://monitor.YOURDOMAIN.com` |
| Postiz | Approved social scheduling | `127.0.0.1:4007` | `https://social.YOURDOMAIN.com` |
| Postiz Temporal UI | Local Postiz internals only | `127.0.0.1:4080` | No public URL |
| Better Stack | External uptime and heartbeat checks | Website only | Better Stack dashboard |
| OneDrive/restic | Backups and archive | Website/remote only | OneDrive |
| Python scripts | Content operations and checks | Local commands only | No public URL |

# Before you start

## Values you must know before setup

Do not guess these. If you do not know one, stop at the relevant step and ask the owner or technical team.

| Needed value | What it is used for | Example |
|---|---|---|
| Domain root | Caddy, DNS, `.env` | `replife.example.com` or `yourdomain.com` |
| VPS username | File paths | The result of `whoami` |
| VPS public IP address | DNS records | From the VPS host panel or `curl -4 https://ifconfig.me` |
| Caddy basic-auth password | Uptime Kuma public monitor route | A strong password you choose |
| Microsoft Lists access | Operations control center | Microsoft 365 account |
| Better Stack access | Uptime and cron heartbeat monitoring | Better Stack account |
| OneDrive access | Backups/archive | Microsoft account |
| Postiz social channels | Social scheduling | Facebook, Instagram, YouTube, TikTok; optional LinkedIn/X/Reddit/Medium |
| GitHub Models token/model | Optional AI scripts | Token with models read access |

## Terminal rules for non-technical users

| When you see this | What to do |
|---|---|
| A command block | Copy the whole block into the VPS terminal and press Enter. |
| `YOURDOMAIN.com` | Replace it with your real domain root. |
| `YOUR_USER` | Replace it with the username shown by `whoami`. |
| `nano FILE` | A text editor opens inside the terminal. |
| `CTRL + O`, `ENTER`, `CTRL + X` | Save and exit nano. |
| A check says `STOP`, `failed`, `not found`, `permission denied`, or `cannot connect` | Stop. Do not continue to the next step until fixed. |

## Forbidden commands during this setup

Never run these during RepLife setup:

```bash
docker system prune -a
docker compose down -v
docker stop $(docker ps -q)
docker restart $(docker ps -q)
sudo rm -rf /var/lib/docker
sudo systemctl restart caddy
```

Use `sudo systemctl reload caddy` only after Caddy validates. Use Docker commands only inside the service folder you are actively configuring.

# Step 1 - Connect to the VPS and upload the zip

## 1.1 Connect with SSH

1. Open MobaXterm or your SSH tool.
2. Start an SSH session to the VPS.
3. Log in with your VPS username and password or SSH key.

## 1.2 Confirm you are on the VPS

Run:

```bash
whoami
pwd
hostname
```

Expected result:

- `whoami` shows your Linux username.
- `pwd` usually shows `/home/YOUR_USER`.
- `hostname` shows the VPS hostname.

Stop if you are not connected to the VPS.

## 1.3 Upload the zip

Use the SFTP file panel in MobaXterm and upload this file into your VPS home folder:

```text
replife-automation-content-ops-full-vps-v4-step-by-step.zip
```

The expected VPS path is:

```text
~/replife-automation-content-ops-full-vps-v4-step-by-step.zip
```

## 1.4 Check the zip is in the right place

Run:

```bash
cd ~
ls -lh ~/replife-automation-content-ops-full-vps-v4-step-by-step.zip
```

Expected result:

- You see one file listed.
- The file size is not `0`.

Stop if the file is missing. Upload it again before continuing.

# Step 2 - Install base packages and unpack the RepLife package

## 2.1 Install required Ubuntu packages

Run:

```bash
sudo apt update
sudo apt install -y unzip git curl jq openssl python3 python3-venv python3-pip
```

Expected result:

- The command finishes without errors.
- It is OK if Ubuntu says some packages are already installed.

Stop if the command fails.

## 2.2 Create the RepLife backend folder and unzip the package

Run:

```bash
cd ~
mkdir -p ~/replife-backend
unzip -o ~/replife-automation-content-ops-full-vps-v4-step-by-step.zip
cp -a ~/replife-automation-content-ops/. ~/replife-backend/
cd ~/replife-backend
chmod +x scripts/*.sh
```

Expected result:

- No error messages.
- You are now inside `~/replife-backend`.

## 2.3 Confirm the package folders exist

Run:

```bash
cd ~/replife-backend
pwd
ls -la
ls -la scripts services templates docs inputs
```

Expected result:

- `pwd` shows `/home/YOUR_USER/replife-backend`.
- You see these folders: `docs`, `scripts`, `services`, `templates`, `inputs`, `outputs`, and `logs`.

Stop if any of those folders are missing.

# Step 3 - Run the protected-app preflight check

This check protects the Task Scheduler App, Financial Command Center, LobeHub, existing n8n, and Caddy before you add RepLife services.

Run:

```bash
cd ~/replife-backend
bash scripts/check_protected_apps.sh
```

Expected result:

```text
Protected-app preflight passed.
```

The script should also show Docker containers and planned RepLife ports.

Stop if it reports a `STOP` or required protected app problem. Do not install Matomo, Uptime Kuma, or Postiz until this is fixed.

Common reasons this may stop:

| Message | What it means | What to do |
|---|---|---|
| Caddy is not active | The public web proxy is not running | Ask technical team to repair Caddy first. |
| Task Scheduler listener not found | The protected Task Scheduler app may not be running on the expected port | Do not continue until confirmed. |
| Financial Command Center listener not found | The protected FCC app may not be running on the expected port | Do not continue until confirmed. |
| existing n8n listener not found | n8n may not be running at `127.0.0.1:5678` | Do not install a second n8n. Fix or confirm existing n8n. |
| planned RepLife port already in use | A new RepLife port conflicts with something | Stop and ask technical team to choose a safe alternate plan. |

# Step 4 - Create and fill the master `.env` file

The master `.env` file stores private setup values. Never upload it to GitHub, Microsoft Lists, Postiz, n8n, email, or public documentation.

## 4.1 Create the file

Run:

```bash
cd ~/replife-backend
cp .env.example .env
chmod 600 .env
```

Expected result:

- No output is OK.
- `.env` now exists.

Check it:

```bash
ls -lh .env
```

Expected result:

- You see `.env`.
- Permissions should begin with `-rw-------` or similar.

## 4.2 Get your Linux username

Run:

```bash
whoami
```

Write down the result. You will use it to replace `YOUR_USER`.

## 4.3 Edit `.env`

Run:

```bash
cd ~/replife-backend
nano .env
```

Make these required edits now:

| Find | Replace with |
|---|---|
| `DOMAIN=YOURDOMAIN.com` | `DOMAIN=your real domain root` |
| `MATOMO_BASE_URL=https://analytics.YOURDOMAIN.com` | `MATOMO_BASE_URL=https://analytics.your real domain root` |
| `POSTIZ_BASE_URL=https://social.YOURDOMAIN.com` | `POSTIZ_BASE_URL=https://social.your real domain root` |
| `/home/YOUR_USER/replife-backend/secrets/restic-onedrive-password` | `/home/the_username_from_whoami/replife-backend/secrets/restic-onedrive-password` |

Keep this line as-is unless you are in a supervised Postiz API session:

```text
POSTIZ_API_ENABLED=no
```

Leave optional values such as `replace_me_optional` alone until that feature is being configured.

Save and exit nano:

```text
CTRL + O
ENTER
CTRL + X
```

## 4.4 Confirm the important `.env` values

Run:

```bash
cd ~/replife-backend
grep -E '^(DOMAIN|TZ|MATOMO_BASE_URL|POSTIZ_BASE_URL|POSTIZ_API_ENABLED|RESTIC_PASSWORD_FILE)=' .env
```

Expected result:

- `DOMAIN` is your real domain root.
- `MATOMO_BASE_URL` uses `https://analytics.` plus your real domain.
- `POSTIZ_BASE_URL` uses `https://social.` plus your real domain.
- `POSTIZ_API_ENABLED=no`.
- `RESTIC_PASSWORD_FILE` has your real Linux username, not `YOUR_USER`.

## 4.5 Run the runtime placeholder check

Run:

```bash
cd ~/replife-backend
bash scripts/check_active_placeholders.sh runtime-basic
```

Expected result:

```text
Active placeholder check passed for mode: runtime-basic
```

Stop if it lists files and placeholder values. Reopen `.env`, fix the listed values, and run the check again.

# Step 5 - Create the Microsoft Lists control center

Microsoft Lists is the non-technical control center. It tracks setup status, account access, services, scripts, approvals, content calendars, Postiz schedules, cron approvals, and weekly reviews.

## 5.1 Open the templates folder on the VPS

Run:

```bash
cd ~/replife-backend
ls -la templates/microsoft-lists
```

Expected result: you see CSV files including:

```text
implementation_day_tracker.csv
account_access_confirmation.csv
service_inventory.csv
n8n_workflows.csv
cron_approval.csv
automation_scripts.csv
content_calendar.csv
postiz_schedules.csv
social_approval_ladder.csv
weekly_operations_reviews.csv
replife_show_episodes.csv
shakeum_content_ideas.csv
product_prompt_drafts.csv
website_drafts.csv
```

## 5.2 Download the CSV templates to your computer

Use MobaXterm SFTP:

1. Open the VPS folder: `/home/YOUR_USER/replife-backend/templates/microsoft-lists`.
2. Select all CSV files.
3. Download them to a local folder on your computer.

## 5.3 Create each Microsoft List from CSV

For each CSV file:

1. Open Microsoft Lists in your browser.
2. Choose **New list**.
3. Choose **From CSV**.
4. Upload one CSV file.
5. Name the list using the friendly name in the table below.
6. Confirm the columns.
7. Create the list.
8. Repeat for the next CSV.

| CSV file | Microsoft List name |
|---|---|
| `implementation_day_tracker.csv` | RepLife Implementation Day Tracker |
| `account_access_confirmation.csv` | RepLife Account Access Confirmation |
| `service_inventory.csv` | RepLife Service Inventory |
| `n8n_workflows.csv` | RepLife n8n Workflows |
| `cron_approval.csv` | RepLife Cron Approval |
| `automation_scripts.csv` | RepLife Automation Scripts |
| `content_calendar.csv` | RepLife Content Calendar |
| `postiz_schedules.csv` | RepLife Postiz Schedules |
| `social_approval_ladder.csv` | RepLife Social Approval Ladder |
| `weekly_operations_reviews.csv` | RepLife Weekly Operations Reviews |
| `replife_show_episodes.csv` | RepLife Show Episodes |
| `shakeum_content_ideas.csv` | SHAKEUM Content Ideas |
| `product_prompt_drafts.csv` | Product Prompt Drafts |
| `website_drafts.csv` | Website Drafts |

## 5.4 Record setup progress

Open **RepLife Implementation Day Tracker** and add/update a row for each setup step. At minimum, record:

- Step number.
- Date.
- Status: Not Started, In Progress, Passed, Blocked, or Fixed.
- Validation command used.
- Result.
- Next safe step.

Check: after this step, you should have a Microsoft Lists workspace that lets a non-technical operator see what is configured, what passed, what is blocked, and what needs review.

# Step 6 - Configure DNS records

RepLife uses four public subdomains. They point to the VPS public IP. Caddy then sends traffic to the correct local-only service.

## 6.1 Find the VPS public IP address

Run this from the VPS:

```bash
curl -4 https://ifconfig.me
printf '\n'
```

Write down the IP address. Do not use `127.0.0.1` for DNS.

If this command fails, get the VPS public IPv4 address from the VPS hosting panel.

## 6.2 Add DNS A records

In your DNS host, create these A records:

| Host/name | Type | Value |
|---|---|---|
| `analytics` | A | VPS public IPv4 address |
| `automations` | A | VPS public IPv4 address |
| `monitor` | A | VPS public IPv4 address |
| `social` | A | VPS public IPv4 address |

If your DNS is hosted at IONOS, use the IONOS domain DNS area. If your DNS is not hosted at IONOS and you do not know where it is hosted, stop and ask the owner or technical team before continuing.

## 6.3 Check DNS from the VPS

Replace `YOURDOMAIN.com` with your real domain and run:

```bash
DOMAIN="YOURDOMAIN.com"
for host in analytics automations monitor social; do
  echo "Checking $host.$DOMAIN"
  getent hosts "$host.$DOMAIN" || true
done
```

Expected result:

- Each name should eventually show the VPS public IP.
- DNS may take time to update.

Do not configure Caddy public routes until DNS is ready or intentionally waiting for DNS propagation.

# Step 7 - Back up and validate Caddy before changes

Caddy is already protecting existing apps. You must back it up before editing it.

Run:

```bash
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.backup-before-replife-$(date +%F-%H%M)
sudo caddy validate --config /etc/caddy/Caddyfile
```

Expected result:

- Caddy validation succeeds.

Stop if validation fails. Do not edit or reload Caddy until the existing Caddyfile is fixed.

# Step 8 - Install and configure Matomo

Matomo tracks public content analytics only. Do not use it for commerce, checkout, carts, payments, customers, refunds, store pages, shipping, taxes, coupons, or fulfillment.

## 8.1 Run the Matomo setup script

Run:

```bash
cd ~/replife-backend
bash scripts/setup_matomo_service.sh
```

Expected result:

- It says it created or kept `services/matomo/.env`.
- It validates Docker Compose.
- It pulls images.
- It starts containers.
- It says Matomo is running locally at `http://127.0.0.1:8081`.

Stop if the script reports port `8081` is already in use or if Docker fails.

## 8.2 Check Matomo containers

Run:

```bash
cd ~/replife-backend/services/matomo
docker compose ps
curl -I http://127.0.0.1:8081
```

Expected result:

- `docker compose ps` shows the Matomo containers running.
- `curl -I` returns an HTTP response such as `HTTP/1.1 200`, `302`, or similar.

## 8.3 Add the Matomo Caddy block

Open the Caddyfile:

```bash
sudo nano /etc/caddy/Caddyfile
```

At the bottom of the file, add this block. Replace `YOURDOMAIN.com` with your real domain root:

```caddy
analytics.YOURDOMAIN.com {
    encode gzip zstd
    reverse_proxy 127.0.0.1:8081
}
```

Save and exit nano.

## 8.4 Validate and reload Caddy

Run:

```bash
sudo caddy fmt --overwrite /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

Expected result:

- Caddy validation succeeds.
- Reload completes without errors.

Stop if Caddy validation fails. Do not reload if validation fails. Restore the backup or fix the last block you added.

## 8.5 Check Matomo public URL

Replace `YOURDOMAIN.com` with your real domain and run:

```bash
curl -I https://analytics.YOURDOMAIN.com
```

Expected result:

- You receive an HTTP response.
- A certificate error usually means DNS or Caddy/HTTPS is not ready yet.

## 8.6 Complete the Matomo browser setup

Open:

```text
https://analytics.YOURDOMAIN.com
```

When Matomo asks for database settings, use:

| Matomo wizard field | Value |
|---|---|
| Database server | `db` |
| Login | `matomo` |
| Password | Value of `MATOMO_DB_PASSWORD` from `services/matomo/.env` |
| Database name | `matomo` |
| Table prefix | `matomo_` |

To display the Matomo database password on the VPS, run:

```bash
cd ~/replife-backend
grep '^MATOMO_DB_PASSWORD=' services/matomo/.env | cut -d= -f2-
```

Create the Matomo admin account and write the login location in **RepLife Account Access Confirmation**.

## 8.7 Add the public-content site in Matomo

Inside Matomo:

1. Create a site entry for RepLife public content pages.
2. Do not enable ecommerce tracking.
3. Do not add tracking to checkout, cart, account, order, customer, refund, shipping, tax, coupon, fulfillment, store-admin, or payment pages.
4. Record the Matomo site ID in `.env` as `MATOMO_SITE_ID` if it is different from `1`.

## 8.8 Recheck protected apps

Run:

```bash
cd ~/replife-backend
bash scripts/check_protected_apps.sh
```

Expected result:

```text
Protected-app preflight passed.
```

# Step 9 - Confirm existing n8n and set RepLife reminder rules

Do not install a new n8n. RepLife uses the existing n8n only for reminders, HTTP checks, simple notifications, and coordination.

## 9.1 Confirm n8n is listening locally

Run:

```bash
sudo ss -tulpn | grep ':5678 ' || true
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep -i n8n || true
```

Expected result:

- You see n8n listening on `127.0.0.1:5678` or an existing n8n container.

Stop if n8n is missing. Do not install another n8n.

## 9.2 Confirm the public n8n route

If the route already exists, open:

```text
https://automations.YOURDOMAIN.com
```

If the route does not exist, add this Caddy block only once. Do not create duplicate site blocks:

```caddy
automations.YOURDOMAIN.com {
    encode gzip zstd
    reverse_proxy 127.0.0.1:5678
}
```

Then validate and reload Caddy:

```bash
sudo caddy fmt --overwrite /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

## 9.3 Create RepLife n8n organization rules

Inside n8n:

1. Create a tag named `RepLife`.
2. Prefix every RepLife workflow with `RepLife - `.
3. Use only safe nodes for RepLife: Schedule Trigger, Manual Trigger, HTTP Request, IF, Set/Edit Fields, and notification nodes.
4. Do not use Code, Python Code, Execute Command, local file read/write, Local File Trigger, broad file-system access, heavy loops, queue mode changes, or task-runner changes.
5. Do not edit Financial Command Center workflows during RepLife setup.

Recommended reminder workflows:

| Workflow name | Purpose |
|---|---|
| `RepLife - Weekly Planning Reminder` | Remind owner to choose weekly theme and backlog. |
| `RepLife - Postiz Review Reminder` | Remind owner to review queue rows before scheduling. |
| `RepLife - Publishing Window Reminder` | Remind owner to check scheduled posts and engagement. |
| `RepLife - Backup Review Reminder` | Remind owner to confirm backup and restore tests. |

Record each workflow in **RepLife n8n Workflows**.

# Step 10 - Install and configure Uptime Kuma

Uptime Kuma is the internal visual status dashboard. It should monitor services. It should not restart them automatically.

## 10.1 Run the Uptime Kuma setup script

Run:

```bash
cd ~/replife-backend
bash scripts/setup_uptime_kuma_service.sh
```

Expected result:

- The script validates the compose file.
- It pulls and starts Uptime Kuma.
- It says Uptime Kuma is running locally at `http://127.0.0.1:3001`.

Stop if port `3001` is already in use or Docker fails.

## 10.2 Check Uptime Kuma locally

Run:

```bash
cd ~/replife-backend/services/uptime-kuma
docker compose ps
curl -I http://127.0.0.1:3001
```

Expected result:

- Uptime Kuma container is running.
- `curl -I` returns an HTTP response.

## 10.3 Create a Caddy basic-auth password hash

Choose a strong password for the monitor page. Run this command, replacing `CHANGE_THIS_PASSWORD` with the password you chose:

```bash
caddy hash-password --plaintext "CHANGE_THIS_PASSWORD"
```

Copy the hash output. You will paste it into the Caddy block.

## 10.4 Add the Uptime Kuma Caddy block

Open Caddy:

```bash
sudo nano /etc/caddy/Caddyfile
```

Add this block, replacing both `YOURDOMAIN.com` and `REPLACE_WITH_CADDY_HASH`:

```caddy
monitor.YOURDOMAIN.com {
    encode gzip zstd
    basic_auth {
        admin REPLACE_WITH_CADDY_HASH
    }
    reverse_proxy 127.0.0.1:3001
}
```

Save and exit.

## 10.5 Validate and reload Caddy

Run:

```bash
sudo caddy fmt --overwrite /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

Expected result: validation succeeds and reload completes.

## 10.6 Open Uptime Kuma and create owner account

Open:

```text
https://monitor.YOURDOMAIN.com
```

Browser behavior:

1. The browser should ask for a username and password.
2. Username is `admin`.
3. Password is the password you chose before hashing.
4. Uptime Kuma should open.
5. Create the Uptime Kuma owner account.

## 10.7 Add Uptime Kuma monitors

Inside Uptime Kuma, add these monitors:

| Monitor name | Type | URL |
|---|---|---|
| RepLife Matomo Local | HTTP(s) | `http://127.0.0.1:8081` |
| RepLife Existing n8n Local | HTTP(s) | `http://127.0.0.1:5678` |
| RepLife Uptime Kuma Public | HTTP(s) | `https://monitor.YOURDOMAIN.com` |
| RepLife Analytics Public | HTTP(s) | `https://analytics.YOURDOMAIN.com` |
| RepLife Existing n8n Public | HTTP(s) | `https://automations.YOURDOMAIN.com` |

After Postiz is installed, add:

| Monitor name | Type | URL |
|---|---|---|
| RepLife Postiz Local | HTTP(s) | `http://127.0.0.1:4007` |
| RepLife Social Public | HTTP(s) | `https://social.YOURDOMAIN.com` |

Record Uptime Kuma setup in **RepLife Service Inventory**.

# Step 11 - Install and configure Postiz

Postiz is for approved social scheduling only. It must not auto-approve posts, send DMs, auto-reply to comments, or handle commerce.

## 11.1 Run the Postiz setup script

Run:

```bash
cd ~/replife-backend
bash scripts/setup_postiz_service.sh
```

Expected result:

- The script checks ports `4007` and `4080`.
- It clones the official Postiz Docker Compose repository.
- It patches Postiz to local-only port `127.0.0.1:4007:5000`.
- It patches Temporal UI to local-only port `127.0.0.1:4080:8080`.
- It validates Docker Compose.
- It starts Postiz.
- It stops if unsafe public ports are exposed.

Stop if the script fails. Do not guess and do not expose Postiz directly to the public internet.

## 11.2 Check Postiz ports

Run:

```bash
docker ps --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}' | grep -E 'postiz|temporal' || true
```

Correct patterns include:

```text
127.0.0.1:4007->5000/tcp
127.0.0.1:4080->8080/tcp
```

Stop and fix before continuing if you see:

```text
0.0.0.0:4007
0.0.0.0:4080
0.0.0.0:8080
:::4007
:::4080
:::8080
```

## 11.3 Add the Postiz Caddy block

Open Caddy:

```bash
sudo nano /etc/caddy/Caddyfile
```

Add this block, replacing `YOURDOMAIN.com`:

```caddy
social.YOURDOMAIN.com {
    encode gzip zstd
    reverse_proxy 127.0.0.1:4007
}
```

Save and exit.

## 11.4 Validate and reload Caddy

Run:

```bash
sudo caddy fmt --overwrite /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

Expected result: validation succeeds and reload completes.

## 11.5 Open Postiz and create owner account

Open:

```text
https://social.YOURDOMAIN.com
```

Complete these actions:

1. Create the first owner/admin account.
2. Log in.
3. Disable public/open registration after owner setup if Postiz exposes that setting.
4. Record the admin login location in **RepLife Account Access Confirmation**.

## 11.6 Connect only approved social channels

Inside Postiz, connect only the social channels approved for RepLife content operations.

Required channels if used by the current content plan:

- Facebook.
- Instagram.
- YouTube.
- TikTok.

Optional channels only if used that month:

- LinkedIn.
- X (Twitter).
- Reddit.
- Medium.

Important: Some self-hosted Postiz social providers may require provider app environment variables before a channel can connect. If Postiz shows missing provider configuration or asks for app credentials you do not have, stop and ask the owner or technical team. Do not enter commerce, payment, WooCommerce, Gelato, Stripe, customer-service, DM, or store credentials.

## 11.7 Add Postiz monitors in Uptime Kuma

Add the monitors listed in Step 10.7:

- `RepLife Postiz Local` -> `http://127.0.0.1:4007`.
- `RepLife Social Public` -> `https://social.YOURDOMAIN.com`.

## 11.8 Keep Postiz API disabled by default

Check:

```bash
cd ~/replife-backend
grep '^POSTIZ_API_ENABLED=' .env
```

Expected result:

```text
POSTIZ_API_ENABLED=no
```

# Step 12 - Configure Better Stack monitoring

Better Stack monitors public URLs from outside the VPS and receives heartbeat pings from approved cron jobs.

## 12.1 Create public URL monitors

In Better Stack, create these URL monitors one at a time:

1. Monitor name: `RepLife Analytics Public`
   URL: `https://analytics.YOURDOMAIN.com`
2. Monitor name: `RepLife Automations Public`
   URL: `https://automations.YOURDOMAIN.com`
3. Monitor name: `RepLife Monitor Public`
   URL: `https://monitor.YOURDOMAIN.com`
4. Monitor name: `RepLife Social Public`
   URL: `https://social.YOURDOMAIN.com`

Expected result: Better Stack reports the URLs as up after DNS and Caddy are working.

## 12.2 Create heartbeats only after manual tests

Do not create cron heartbeats until the job runs manually and passes. Create these heartbeat names only when the related job is ready:

- `RepLife Default Cron` -> `.env` variable `BETTERSTACK_DEFAULT_HEARTBEAT_URL`
- `Matomo Archive` -> `.env` variable `BETTERSTACK_MATOMO_ARCHIVE_HEARTBEAT_URL`
- `Weekly Report` -> `.env` variable `BETTERSTACK_WEEKLY_REPORT_HEARTBEAT_URL`
- `Weekly Content Ops` -> `.env` variable `BETTERSTACK_WEEKLY_CONTENT_OPS_HEARTBEAT_URL`
- `OneDrive Media Archive` -> `.env` variable `BETTERSTACK_ONEDRIVE_MEDIA_ARCHIVE_HEARTBEAT_URL`
- `Restic Backup` -> `.env` variable `BETTERSTACK_ONEDRIVE_RESTIC_BACKUP_HEARTBEAT_URL`

Copy heartbeat URLs into `.env` only after the related command passes manually.

# Step 13 - Configure OneDrive, rclone, restic, backup, and restore test

Backups are not complete until a restore test works.

## 13.1 Install backup tools

Run:

```bash
sudo apt update
sudo apt install -y rclone restic
```

Expected result: packages install successfully.

## 13.2 Configure rclone OneDrive remote

Run:

```bash
rclone config
```

Use these choices:

1. Choose `n` for new remote.
2. Name it exactly:

```text
onedrive-replife
```

3. Choose the storage provider whose text says `Microsoft OneDrive`.
4. If asked for `client_id`, press Enter unless the owner gave you a custom Microsoft app ID.
5. If asked for `client_secret`, press Enter unless the owner gave you a custom Microsoft app secret.
6. If asked for advanced config, choose `n`.
7. If asked for auto config on a headless VPS, choose `n` and follow the URL instructions in your browser.
8. When authorization is complete, save the remote.

Because rclone menus can change, choose by the option text, not by a memorized number.

## 13.3 Test OneDrive remote

Run:

```bash
rclone lsd onedrive-replife:
rclone mkdir onedrive-replife:RepLife-VPS
rclone lsd onedrive-replife:
```

Expected result:

- The command can list OneDrive.
- The folder `RepLife-VPS` exists or is created.

Stop if OneDrive does not list.

## 13.4 Create the restic password file

Run:

```bash
cd ~/replife-backend
mkdir -p secrets
openssl rand -base64 32 > secrets/restic-onedrive-password
chmod 600 secrets/restic-onedrive-password
```

Show the password once so you can store it somewhere safe outside the VPS:

```bash
cat secrets/restic-onedrive-password
```

Important: save this password in a secure password manager. Without it, restic backups cannot be restored.

## 13.5 Initialize and test restic backup

Run:

```bash
cd ~/replife-backend
export RESTIC_REPOSITORY="rclone:onedrive-replife:RepLife-VPS/resticbackups"
export RESTIC_PASSWORD_FILE="$PWD/secrets/restic-onedrive-password"
restic init
restic backup docs scripts templates services .env.example requirements.txt
restic snapshots
mkdir -p /tmp/replife-restore-test
restic restore latest --target /tmp/replife-restore-test
ls -la /tmp/replife-restore-test
```

Expected result:

- `restic init` creates the repository. If it says it already exists, continue with backup/snapshots.
- `restic backup` completes.
- `restic snapshots` shows at least one snapshot.
- `restic restore` creates files in `/tmp/replife-restore-test`.

Record the backup and restore test in Microsoft Lists. Do not enable backup cron until backup and restore both pass.

Important backup boundary: this starter backup protects source/configuration package files. Live Docker volume/database backup and restore for Matomo/Postiz/Uptime Kuma must be verified on the real VPS after those services are running and before relying on disaster recovery.

# Step 14 - Set up the Python automation environment

Run:

```bash
cd ~/replife-backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
export PYTHONPATH="$PWD"
```

Expected result:

- The virtual environment activates.
- Requirements install without errors.

Run validation:

```bash
cd ~/replife-backend
source .venv/bin/activate
export PYTHONPATH="$PWD"
python3 -m compileall -q scripts
bash -n scripts/*.sh
bash scripts/validate_all_scripts_preview.sh
```

Expected result:

```text
Preview validation passed.
```

Stop if any command fails.

# Step 15 - Optional GitHub Models / AI setup

Use GitHub Models only if you intentionally want repeatable AI-backed scripts. LobeHub remains the existing manual AI workspace and should not be reinstalled.

## 15.1 Edit `.env` only when AI is ready

Run:

```bash
cd ~/replife-backend
nano .env
```

Fill:

```text
GITHUB_TOKEN=your_token_with_models_read_access
GITHUB_MODELS_MODEL=the_verified_model_id
AI_PAID_USAGE_ENABLED=no
```

Save and exit.

## 15.2 Check AI placeholders

Run:

```bash
cd ~/replife-backend
bash scripts/check_active_placeholders.sh ai
python scripts/github_models_model_check.py
python scripts/ai_usage_report.py --dry-run
```

Expected result:

- Placeholder check passes.
- GitHub Models configuration looks ready.
- AI usage report dry run completes.

If you are not using AI yet, skip this step and keep AI-dependent automation disabled.

# Step 16 - Run the Day 17M strict dry run

Day 17M is the final beginner safety bridge before locking the workflow. It uses sample inputs only and must not publish, schedule, send, reply, upload, or touch commerce.

Run:

```bash
cd ~/replife-backend
source .venv/bin/activate
export PYTHONPATH="$PWD"
bash scripts/day17m_strict_dry_run.sh
```

Expected result:

```text
Day 17M strict dry run passed.
No publish, schedule, send, reply, upload, or commerce action was performed.
```

Check the test output folder:

```bash
ls -la outputs/test-results/day17m
```

Record the result in **RepLife Implementation Day Tracker** and **RepLife Automation Scripts**.

Stop if Day 17M fails. Do not move to workflow lock or cron.

# Step 17 - Day 18 workflow lock

Do this only after Day 17M passes.

In Microsoft Lists, create a Day 18 workflow lock record with:

| Field | What to record |
|---|---|
| Workflow name | RepLife Content Operations v4 Step-by-Step |
| Approved input folders | `inputs/planning`, `inputs/media`, `inputs/social` |
| Approved output folders | `outputs/reports`, `outputs/social`, `outputs/social-queues`, `outputs/test-results` |
| Queue path | `outputs/social-queues/approved_postiz_queue.csv` |
| Approval ladder | Idea, Drafted, Media Validated, Packaged, Caption Reviewed, Queue Built, Approved for Postiz, Uploaded to Postiz, Scheduled in Postiz, Posted / Complete, Archived |
| Disable procedure | Disable cron line, set `POSTIZ_API_ENABLED=no`, use manual Postiz scheduling fallback |
| Last dry run | Date and result of Day 17M |

If the workflow order changes later, repeat Day 17M before trusting the new workflow.

# Step 18 - Day 19 cron gate

Cron is last. Do not put live Postiz sending, media uploads, DMs, comments, customer service, commerce, or public posting in cron.

## 18.1 Run pre-cron validation

Run:

```bash
cd ~/replife-backend
bash scripts/pre_cron_validation.sh
```

If using backup cron, also run:

```bash
bash scripts/pre_cron_validation.sh backup
```

If using AI cron, also run:

```bash
bash scripts/pre_cron_validation.sh ai
```

If using Postiz API checks, also run:

```bash
bash scripts/pre_cron_validation.sh postiz-api
```

Expected result:

```text
Pre-cron validation passed.
```

Stop if validation fails.

## 18.2 Allowed cron jobs

Only these job types are candidates after manual testing:

| Job type | Allowed? | Required before cron |
|---|---|---|
| Matomo archive | Yes | Two successful manual runs and heartbeat URL. |
| Weekly reports/dashboard | Yes | Manual run reviewed. |
| Weekly content ops runner | Yes, dry-run/previews only | Two manual runs; confirms it stops before public action. |
| OneDrive archive | Yes | rclone remote tested. |
| restic backup | Yes | backup, snapshots, and restore test passed. |
| Postiz send/media upload | No | Never unattended. |
| Commerce/customer service/DM/comment automation | No | Never part of this VPS. |

## 18.3 Edit cron only after approval

Run:

```bash
crontab -e
```

Add only approved wrapper commands. Example pattern:

```cron
# RepLife weekly dry-run content ops - safe preview only
0 9 * * 1 cd /home/YOUR_USER/replife-backend && bash scripts/run_with_heartbeat.sh BETTERSTACK_WEEKLY_CONTENT_OPS_HEARTBEAT_URL bash scripts/weekly_content_ops_runner.sh >> logs/weekly_content_ops_cron.log 2>&1
```

Replace `YOUR_USER` with the result of `whoami`.

To disable a bad job, run `crontab -e`, add `#` to the beginning of that line, save, and exit.

# Step 19 - First full weekly operating cycle

Use this order every week.

## 19.1 Confirm protected apps and accounts

Run:

```bash
cd ~/replife-backend
bash scripts/check_protected_apps.sh
bash scripts/check_active_placeholders.sh runtime-basic
```

Expected result: both pass.

Open Microsoft Lists and confirm required account access:

- Microsoft Lists.
- GitHub private repository if used.
- LobeHub.
- Existing n8n.
- Matomo.
- Postiz.
- Better Stack.
- Uptime Kuma.
- OneDrive.
- Facebook, Instagram, YouTube, TikTok if used that week.

## 19.2 Choose or confirm monthly theme

Edit:

```bash
cd ~/replife-backend
nano inputs/planning/monthly_theme.csv
```

Validate:

```bash
python scripts/monthly_theme_validator.py
```

Expected result: monthly theme validation passes.

## 19.3 Put approved media in the correct folder

Use this folder for production media:

```text
~/replife-backend/inputs/media
```

Create it if needed:

```bash
mkdir -p ~/replife-backend/inputs/media
```

Filename rules:

- Lowercase letters.
- Numbers.
- Hyphen `-`.
- Underscore `_`.
- Dot `.`.
- Approved extensions only: `mp4`, `mov`, `mkv`, `wav`, `mp3`, `flac`, `png`, `jpg`, `jpeg`, `webp`.

Validate files:

```bash
cd ~/replife-backend
python scripts/validate_content_files.py inputs/media
python scripts/media_spec_validator.py --input inputs/media
```

## 19.4 Run the weekly safe preview runner

Run:

```bash
cd ~/replife-backend
source .venv/bin/activate
export PYTHONPATH="$PWD"
bash scripts/weekly_content_ops_runner.sh "Faith Over Fear"
```

Replace `Faith Over Fear` with the current theme if needed.

Expected result:

```text
Weekly runner stopped before human review, media upload, Postiz loading, or public scheduling.
```

## 19.5 Review outputs before Postiz

Review generated outputs in:

```text
outputs/reports
outputs/social
outputs/social-queues
```

Open the queue file:

```bash
nano outputs/social-queues/approved_postiz_queue.csv
```

Every row starts as not approved. A human must review before changing rows to approved.

## 19.6 Schedule in Postiz manually by default

Open:

```text
https://social.YOURDOMAIN.com
```

Manually create or schedule approved posts. Confirm:

- Caption is correct.
- Platform is correct.
- Account/channel is correct.
- Media is correct.
- Date/time is correct.
- Nothing duplicated.

Record the schedule in **RepLife Postiz Schedules**.

# Step 20 - Supervised Postiz API/media actions only when needed

Manual Postiz scheduling is the fallback and preferred beginner method. Use Postiz API/media loading only in a supervised session.

## 20.1 Required gates before any live API/media action

All must be true:

1. Queue row has `approved=yes`.
2. Media row has `upload_ready=yes` if media is required.
3. Caption and queue linters pass.
4. Postiz API budget guard passes.
5. Postiz API smoke test passes.
6. Payload preview JSON is created.
7. Human reviews the preview.
8. `POSTIZ_API_ENABLED` is temporarily changed to `yes` only during the session.
9. `POSTIZ_API_ENABLED` is changed back to `no` immediately after.
10. Browser verification in Postiz confirms the result.

## 20.2 Prepare the session

Run:

```bash
cd ~/replife-backend
source .venv/bin/activate
export PYTHONPATH="$PWD"
bash scripts/check_protected_apps.sh
python scripts/postiz_queue_linter.py
python scripts/postiz_queue_linter.py --approved-only
python scripts/postiz_api_budget_guard.py
python scripts/postiz_api_smoke_test.py
python scripts/postiz_integration_export.py
```

Stop if any command fails.

## 20.3 Create a dry-run payload preview

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

Stop if anything is wrong.

## 20.4 Temporarily enable API mode only during the supervised session

Run:

```bash
nano .env
```

Change:

```text
POSTIZ_API_ENABLED=no
```

to:

```text
POSTIZ_API_ENABLED=yes
```

Run only the approved supervised command. Example small send limit:

```bash
python scripts/optional_postiz_loader.py \
  --confirm-send \
  --limit 3 \
  --payload-preview-output outputs/social-queues/previews/postiz-payload-preview.json
```

Immediately turn API mode off:

```bash
nano .env
```

Change it back to:

```text
POSTIZ_API_ENABLED=no
```

Verify:

```bash
grep '^POSTIZ_API_ENABLED=' .env
```

Expected result:

```text
POSTIZ_API_ENABLED=no
```

Open Postiz in the browser and confirm every scheduled item.

# Step 21 - Monthly operating rhythm

Perform these monthly:

1. Confirm account access in Microsoft Lists.
2. Confirm Postiz social channels are still connected.
3. Run protected-app check.
4. Run backup and restore test.
5. Review Matomo report.
6. Import manual social metrics.
7. Review top content.
8. Review capacity/backlog report.
9. Archive old outputs.
10. Update next month theme.

Useful commands:

```bash
cd ~/replife-backend
bash scripts/check_protected_apps.sh
python scripts/capacity_backlog_report.py
python scripts/matomo_content_report.py
python scripts/top_content_analyzer.py
python scripts/owner_dashboard.py
```

# Step 22 - Day 20, first 90 days, Day 91+, and year-one rules

| Period | Do this | Do not do this |
|---|---|---|
| Day 20 | Review protected apps, services, Caddy, Docker folders, Microsoft Lists, logs, backups, restore, Postiz process, Better Stack. | Do not expand before stabilizing failures. |
| Days 21-90 | Operate before expanding. Update one service at a time. Keep public actions manual-approved. | Do not add tools unless the current stack cannot solve the need. |
| Day 91+ | Monthly reset, channel check, GitHub Models check if AI is used, restore test, Matomo/social metrics review, dashboard review. | Do not let cron/API actions drift. |
| Year one | Prefer Microsoft Lists, Python scripts, Matomo reports, Postiz manual review, n8n reminders, Better Stack checks. | Do not turn the VPS into commerce, customer-service, or unattended publishing infrastructure. |

# Final acceptance checklist

RepLife setup is complete only when all items are true:

| Check | Pass? |
|---|---|
| Full v4 step-by-step zip is uploaded and unpacked. |  |
| Protected-app preflight passes. |  |
| `.env` runtime-basic placeholder check passes. |  |
| Microsoft Lists templates are created/imported. |  |
| DNS records exist for analytics, automations, monitor, and social. |  |
| Caddy validates before every reload. |  |
| Only Caddy listens publicly on ports 80 and 443. |  |
| Matomo runs on `127.0.0.1:8081` and tracks public content only. |  |
| Existing n8n is reused; no second n8n installed. |  |
| Uptime Kuma runs on `127.0.0.1:3001` and monitor route has basic auth. |  |
| Postiz runs on `127.0.0.1:4007`; Temporal UI is local-only on `127.0.0.1:4080`. |  |
| Postiz API remains `POSTIZ_API_ENABLED=no` by default. |  |
| Better Stack public monitors exist. |  |
| OneDrive/rclone/restic backup and restore test passes. |  |
| Python environment validates. |  |
| Day 17M strict dry run passes. |  |
| Day 18 workflow lock is recorded. |  |
| Day 19 pre-cron validation passes before cron is enabled. |  |
| Cron excludes Postiz sending/media upload/customer-service/DM/comment/commerce/public posting. |  |
| Monthly reset and restore-test rhythm is recorded. |  |

# Troubleshooting guide

| Problem | What to check first | Safe action |
|---|---|---|
| Website does not load | Uptime Kuma, then service folder, then Caddy validation | Do not restart everything. Check only the related service. |
| Caddy validation fails | Last edited Caddy block | Do not reload. Fix or restore backup. |
| Docker port shows `0.0.0.0` | Compose file port line | Stop that service and change to `127.0.0.1`. |
| Matomo wizard cannot connect to DB | Database host/user/password | Use host `db`, user `matomo`, password from `services/matomo/.env`. |
| Uptime Kuma public page asks for login | This is expected | Use Caddy basic-auth username `admin` and your chosen password. |
| Postiz cannot connect a social channel | Provider configuration or platform login | Stop and ask for provider credentials. Do not enter commerce credentials. |
| Better Stack heartbeat fails | Job failed or URL wrong | Fix job first. Heartbeat should only ping after success. |
| Backup fails | rclone remote, restic password, OneDrive access | Do not enable backup cron. Repeat restore test after fixing. |
| Cron causes trouble | `crontab -e` | Comment out the line with `#`, save, and review logs. |
| Private file is staged in Git | `scripts/git_commit_preflight.sh` | Unstage private files and rerun the preflight. |

# Appendix A - Quick command checklist

Use this only after you understand the full steps above.

```bash
# Upload zip first, then:
sudo apt update
sudo apt install -y unzip git curl jq openssl python3 python3-venv python3-pip
cd ~
mkdir -p ~/replife-backend
unzip -o ~/replife-automation-content-ops-full-vps-v4-step-by-step.zip
cp -a ~/replife-automation-content-ops/. ~/replife-backend/
cd ~/replife-backend
chmod +x scripts/*.sh
bash scripts/check_protected_apps.sh
cp .env.example .env
chmod 600 .env
nano .env
bash scripts/check_active_placeholders.sh runtime-basic
bash scripts/setup_matomo_service.sh
bash scripts/setup_uptime_kuma_service.sh
bash scripts/setup_postiz_service.sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
export PYTHONPATH="$PWD"
bash scripts/validate_all_scripts_preview.sh
bash scripts/day17m_strict_dry_run.sh
```

Do not paste this entire checklist blindly. The full setup requires DNS, Caddy, browser dashboards, Microsoft Lists, Postiz owner setup, channel checks, Better Stack, OneDrive, and restore testing.

# Appendix B - Caddy blocks

Replace `YOURDOMAIN.com` with your real domain.

## Matomo

```caddy
analytics.YOURDOMAIN.com {
    encode gzip zstd
    reverse_proxy 127.0.0.1:8081
}
```

## Existing n8n

Do not add a duplicate block if one already exists.

```caddy
automations.YOURDOMAIN.com {
    encode gzip zstd
    reverse_proxy 127.0.0.1:5678
}
```

## Uptime Kuma

```caddy
monitor.YOURDOMAIN.com {
    encode gzip zstd
    basic_auth {
        admin REPLACE_WITH_CADDY_HASH
    }
    reverse_proxy 127.0.0.1:3001
}
```

Create hash:

```bash
caddy hash-password --plaintext "CHANGE_THIS_PASSWORD"
```

## Postiz

```caddy
social.YOURDOMAIN.com {
    encode gzip zstd
    reverse_proxy 127.0.0.1:4007
}
```

Do not expose Postiz Temporal UI publicly.

After every Caddy edit:

```bash
sudo caddy fmt --overwrite /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

If validation fails, do not reload.

# Appendix C - Script catalog

| Script | Purpose | When to use |
|---|---|---|
| `check_protected_apps.sh` | Protects existing apps and checks planned ports. | Before and after service changes. |
| `check_active_placeholders.sh` | Finds required placeholders by mode. | Before activating a feature. |
| `setup_matomo_service.sh` | Creates Matomo `.env`, validates compose, pulls and starts Matomo. | Matomo install step. |
| `setup_uptime_kuma_service.sh` | Creates Uptime Kuma `.env`, validates compose, pulls and starts Uptime Kuma. | Uptime Kuma install step. |
| `setup_postiz_service.sh` | Clones official Postiz compose and patches local-only ports. | Postiz install step. |
| `day17m_strict_dry_run.sh` | One-command end-to-end dry run using sample inputs only. | Required before Day 18 workflow lock. |
| `pre_cron_validation.sh` | Final safety gate before cron. | Required before Day 19 cron. |
| `run_with_heartbeat.sh` | Runs a command and pings Better Stack only after success. | Approved cron wrapper only. |
| `git_commit_preflight.sh` | Blocks private/generated files from Git commits. | Before Git commits. |
| `monthly_theme_validator.py` | Validates monthly theme CSV. | Start of planning. |
| `validate_content_files.py` | Validates filenames. | Before media processing. |
| `media_spec_validator.py` | Validates media extension and size. | Before package/queue build. |
| `social_package_builder.py` | Creates reviewable platform packages. | Draft content package stage. |
| `postiz_queue_builder.py` | Builds queue rows that start unapproved. | Before human review. |
| `postiz_queue_linter.py` | Checks queue readiness. | Before Postiz scheduling/API. |
| `optional_postiz_loader.py` | Supervised optional Postiz loader. | Manual only, never cron. |
| `postiz_media_uploader.py` | Supervised media upload gate. | Manual only, never cron. |
| `weekly_content_ops_runner.sh` | Runs safe weekly flow and stops before public actions. | Weekly review or safe cron after approval. |
| `restic_onedrive_backup.sh` | Runs encrypted restic backup. | Only after manual restore test passes. |
| `onedrive_restore_test.sh` | Restore-test helper. | Monthly restore check. |

# Appendix D - Business workflow

Monthly operating flow:

1. Choose RepLife Show monthly theme.
2. Choose SHAKEUM campaign or song tie-in.
3. Generate Product Prompting concepts only as creative draft support tied to the theme.
4. Import approved media.
5. Validate filenames and media specs.
6. Transcribe approved audio/video when needed.
7. Repurpose transcripts into clip ideas, captions, website drafts, and show notes.
8. Build social publishing packages.
9. Lint platform captions and queue settings.
10. Build the Postiz queue.
11. Human reviews and approves rows.
12. Schedule manually in Postiz or run supervised loader only after approval.
13. Confirm scheduled content inside Postiz.
14. Review Matomo and manual social metrics.
15. Archive old outputs and reset for the next batch.

Business boundaries:

- RepLife Show is the platform connector.
- SHAKEUM remains its own artist entity.
- Product Prompting remains creative draft support only.
- WordPress WooCommerce/Gelato on IONOS owns commerce.
- The VPS owns content operations only.

# Appendix E - Weekly operating limits

Use these limits for the first year unless a written upgrade plan changes them:

- 1 RepLife Show weekly content package.
- 1 SHAKEUM weekly content package.
- 1 Product Prompting concept batch.
- 1 website draft batch.
- 1 active `approved_postiz_queue.csv`.
- 6 maximum rows per optional Postiz loader run.
- 6 maximum `upload_ready=yes` media rows at one time.
- 0 unsent approved rows before creating a new weekly queue unless the previous queue is intentionally archived.

Stop new packaging if disk usage is high, backlog report warns, Postiz connections are missing, previous queue still has unsent approved rows, or Postiz API smoke test fails.

# Appendix F - Best-practice references used

This setup follows current conservative self-hosting practice:

- Docker service ports bind to `127.0.0.1` so Caddy is the public entry point.
- Caddy handles HTTPS reverse proxying and basic authentication.
- Postiz is configured through Docker Compose/environment variables.
- n8n risky nodes remain outside RepLife production workflows.
- rclone connects to OneDrive and restic performs encrypted backup/restore testing.
- GitHub Models optional AI setup uses the current models API version values already present in `.env.example`.

Final operating rule: if a future change would make the VPS handle commerce, customer service, store operations, DMs, comments, public posting without approval, or unattended Postiz API sending, do not add it to this system. Solve the need with a manual step, Microsoft Lists field, Python draft/report script, Matomo report, Postiz manual review, n8n reminder, or external platform workflow instead.
