# Postiz Service Folder

Postiz uses the official `gitroomhq/postiz-docker-compose` package as the base install.
This folder adds a RepLife port edit guide:

- public Postiz web app binds to `127.0.0.1:4007`
- Temporal UI binds to `127.0.0.1:4080`
- host port `8080` is not used, so LobeHub stays protected
- Caddy exposes only `https://social.YOURDOMAIN.com`

Edit the official compose file before starting:

```bash
cd ~/replife-backend/services/postiz
less POSTIZ_PORT_EDIT_GUIDE.md
```

Before production, pin image references according to the install-day verification steps in the setup manual.
