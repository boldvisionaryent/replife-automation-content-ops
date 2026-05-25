# RepLife Service and Port Plan

Use this plan to avoid breaking existing VPS applications.

## Public DNS Names Used By RepLife

| DNS name | Service |
|---|---|
| analytics.YOURDOMAIN.com | Matomo |
| automations.YOURDOMAIN.com | Existing n8n |
| monitor.YOURDOMAIN.com | Uptime Kuma |
| social.YOURDOMAIN.com | Postiz |
| ai.YOURDOMAIN.com | Optional existing LobeHub route only |

Do not create `webhook.YOURDOMAIN.com` for commerce.

## Local-Only Ports

| Service | Bind |
|---|---|
| Matomo | 127.0.0.1:8081 |
| Uptime Kuma | 127.0.0.1:3001 |
| Postiz | 127.0.0.1:4007 |
| Postiz Temporal UI | 127.0.0.1:4080, local only |

## Public Exposure Rule

Only Caddy listens publicly on ports 80 and 443.

Every RepLife app container must bind to `127.0.0.1`, not `0.0.0.0`.

The included Docker Compose templates already use local-only binds:

- Matomo: `127.0.0.1:8081:80`
- Uptime Kuma: `127.0.0.1:3001:3001`
- Postiz edited official compose: `127.0.0.1:4007:5000`
- Postiz Temporal UI edited official compose: `127.0.0.1:4080:8080`

## Caddy Reload Rule

After every Caddy edit:

```bash
sudo caddy fmt --overwrite /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

If validation fails, do not reload.
