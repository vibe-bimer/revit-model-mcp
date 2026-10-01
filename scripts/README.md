# Server-side scripts

| Script | What it does |
| --- | --- |
| `update-site.sh` | Regenerates the feature pages from the tool registry, builds the site strictly and publishes it atomically |
| `serve-site.sh <port>` | Serves the published site on the LAN; refuses a port that belongs to another process and checks the page it serves |
| `site-cron.sh` | What cron runs: pull when the tree is clean, publish, and start a server when nothing answers with this site |
| `install-site-cron.sh [schedule]` | Installs (or replaces) the crontab entry, `*/15 * * * *` by default |

```bash
scripts/install-site-cron.sh          # every 15 minutes, port 8099
SITE_PORT=8099 scripts/serve-site.sh  # serve by hand
SITE_PORT=8099 scripts/update-site.sh # publish by hand
```
