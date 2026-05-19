# Deployment Guide

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (no local Python environment needed)
- Optional: a Discord webhook URL for alerting on detected hijacks

---

## Docker Run

```bash
docker build -t bgprogue .

docker run --rm \
  -e DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK \
  bgprogue \
  --prefix 185.70.40.0/24 \
  --authorized-as 62371 \
  --start "2020-09-29 16:00:00" \
  --stop  "2020-09-29 18:59:59"
```

Omit `-e DISCORD_WEBHOOK_URL` to run without alerting.

---

## Docker Compose

```yaml
services:
  bgp_rogue:
    build: .
    environment:
      - DISCORD_WEBHOOK_URL=${DISCORD_WEBHOOK_URL:-}
    command: >
      --prefix 185.70.40.0/24
      --authorized-as 62371
      --start "2020-09-29 16:00:00"
      --stop  "2020-09-29 18:59:59"
```

Run with:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK docker compose up
```

---

## Configuration Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_WEBHOOK_URL` | No | Discord channel webhook URL. When set, a message is posted for every detected hijack. |

### Creating a Discord webhook

1. Open your Discord server → channel settings → **Integrations** → **Webhooks**.
2. Click **New Webhook**, copy the URL.
3. Pass it as `DISCORD_WEBHOOK_URL` at runtime — do not bake it into the image or commit it to source control.
