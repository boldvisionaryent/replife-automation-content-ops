# Caddy RepLife Snippets

Back up Caddy before editing:

```bash
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.backup-before-replife-$(date +%F-%H%M)
sudo caddy validate --config /etc/caddy/Caddyfile
```

Use `basic_auth`, not `basicauth`.

## Matomo

```caddy
analytics.YOURDOMAIN.com {
    encode gzip zstd
    reverse_proxy 127.0.0.1:8081
}
```

## Existing n8n

Confirm the existing n8n block. Do not add a duplicate block if one already exists.

```caddy
automations.YOURDOMAIN.com {
    encode gzip zstd
    reverse_proxy 127.0.0.1:5678
}
```

## Uptime Kuma

Protect this route with Caddy basic authentication.

```caddy
monitor.YOURDOMAIN.com {
    encode gzip zstd
    basic_auth {
        admin REPLACE_WITH_CADDY_HASH
    }
    reverse_proxy 127.0.0.1:3001
}
```

Create the hash:

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

## Validate And Reload

```bash
sudo caddy fmt --overwrite /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```
