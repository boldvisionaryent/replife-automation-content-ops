# Protected Existing Apps

These apps are already installed and functioning. They are not setup targets for this repository.

## Protected Apps

| App | Protection rule |
|---|---|
| Task Scheduler App | Check health only. Do not install, rebuild, or reconfigure. |
| Financial Command Center | Check health only. Do not install, rebuild, or reconfigure. |
| LobeHub | Check existing ports only. Do not reinstall or reuse its ports. |
| n8n | Reuse existing instance. Do not install a second n8n. |
| Caddy | Preserve existing site blocks. Validate before reload. |

## Protected Ports

| Purpose | Port |
|---|---:|
| Task Scheduler App | 127.0.0.1:8135 |
| Financial Command Center | 127.0.0.1:8095 |
| Existing n8n | 127.0.0.1:5678 |
| LobeHub reserved | 9000, 8080, 3210, 3000, 5050 |
| Caddy public HTTPS | 80, 443 |

## RepLife Ports

| RepLife service | Port |
|---|---:|
| Matomo | 127.0.0.1:8081 |
| Uptime Kuma | 127.0.0.1:3001 |
| Postiz | 127.0.0.1:4007 |
| Postiz Temporal UI, optional | 127.0.0.1:4080 |

## Never Run During RepLife Setup

```bash
docker system prune -a
docker compose down -v
docker stop $(docker ps -q)
docker restart $(docker ps -q)
sudo rm -rf /var/lib/docker
sudo systemctl restart caddy
```

Restart only the one RepLife service you are actively configuring, from that service folder.
