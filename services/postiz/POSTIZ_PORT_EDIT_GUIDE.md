# Postiz Port Edit Guide

The recommended beginner method is:

```bash
cd ~/replife-backend
bash scripts/setup_postiz_service.sh
```

Use the manual guide below only if the helper script fails and you need to repair the file by hand.

Use this guide after cloning the official Postiz Docker Compose repo:

```bash
cd ~/replife-backend/services/postiz
git clone https://github.com/gitroomhq/postiz-docker-compose
cd postiz-docker-compose
nano docker-compose.yml
```

Find the `postiz:` service. In that service, replace this public port line:

```yaml
ports:
  - "4007:5000"
```

with this local-only port line:

```yaml
ports:
  - "127.0.0.1:4007:5000"
```

Find the `temporal-ui:` service. Replace this public/default port line:

```yaml
ports:
  - '8080:8080'
```

with this local-only alternate port line:

```yaml
ports:
  - '127.0.0.1:4080:8080'
```

Also set the Postiz URL values:

```yaml
MAIN_URL: 'https://social.YOURDOMAIN.com'
FRONTEND_URL: 'https://social.YOURDOMAIN.com'
NEXT_PUBLIC_BACKEND_URL: 'https://social.YOURDOMAIN.com/api'
```

Then validate:

```bash
docker compose config
docker compose pull
docker compose up -d
docker ps --format 'table {{.Names}}\t{{.Ports}}\t{{.Status}}' | grep -E 'postiz|temporal'
```

Correct patterns:

```text
127.0.0.1:4007->5000/tcp
127.0.0.1:4080->8080/tcp
```

Stop and fix the file if you see `0.0.0.0:4007`, `0.0.0.0:4080`, or host port `8080`.
