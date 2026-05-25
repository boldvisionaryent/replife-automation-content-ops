# Services Folder

Use this folder only for RepLife services installed by this package:

- `matomo`
- `uptime-kuma`
- `postiz`

Do not install n8n here on the current VPS. n8n already exists and must be reused.

Included service templates:

- `matomo/docker-compose.yml` and `matomo/.env.example`
- `uptime-kuma/docker-compose.yml` and `uptime-kuma/.env.example`
- `postiz/POSTIZ_PORT_EDIT_GUIDE.md`

Recommended beginner setup:

```bash
cd ~/replife-backend
bash scripts/setup_matomo_service.sh
bash scripts/setup_uptime_kuma_service.sh
bash scripts/setup_postiz_service.sh
```

For Matomo and Uptime Kuma, the helper scripts copy `.env.example` to `.env` and use the included compose files.

For Postiz, the helper script clones the official Postiz compose repo inside `services/postiz/`, then edits the official `docker-compose.yml` with the safe local-only port changes.

Before adding any service folder:

```bash
cd ~/replife-backend
bash scripts/check_protected_apps.sh
```

After starting a service:

```bash
docker compose ps
docker compose config
cd ~/replife-backend
bash scripts/check_protected_apps.sh
```
