# Deploying Python Survival to Cloudflare Pages

Cloudflare Pages serves the browser UI, while the existing Python server runs
the game API. The Pages Function at `functions/api/[[path]].js` forwards the
game's `/api/state` and `/api/command` requests to that server.

You do not need to own a domain for the game website. Cloudflare Pages provides
the project with a `*.pages.dev` address.

## 1. Build the Pages site

In the Cloudflare Pages project settings, set:

- **Root directory:** `/`
- **Build command:** `python game-code/build_pages.py`
- **Build output directory:** `dist`

The build command exports the existing UI from `game-code/web_server.py` to
`dist/index.html`, so the browser page does not need to be maintained twice.

## 2. Run the Python backend

On your server, install Python 3 and copy or clone this repository. Start the
game API with:

```bash
python3 game-code/web_server.py --host 127.0.0.1 --port 8000
```

Put it behind an HTTPS endpoint reachable from Cloudflare Pages Functions. Do
not open port 8000 directly to the public internet.

For a quick test without a domain, run a Cloudflare Quick Tunnel on the server:

```bash
cloudflared tunnel --url http://localhost:8000
```

It prints a temporary `https://....trycloudflare.com` URL. Keep the tunnel
running and use that URL as `BACKEND_URL` below. The URL can change when the
tunnel restarts, so update the Pages setting if it does. For a stable hostname,
use a named Cloudflare Tunnel with a domain in your Cloudflare account, or an
HTTPS reverse proxy on a hostname you control.

## 3. Connect Pages to the backend

In the Pages project, add this **production environment variable**:

- `BACKEND_URL` = the HTTPS origin for the Python backend, e.g. the
  `https://....trycloudflare.com` URL from the Quick Tunnel (no `/api` suffix)

Set the same variable for **Preview** deployments if previews should work too.
Redeploy after changing environment variables.

## 4. Verify

Open the deployed Pages URL. The new-adventure screen should load, and starting
a character should make requests to `/api/state` and `/api/command` through the
Pages Function.

Game sessions are currently stored in the Python process's memory, so a server
restart clears active browser sessions. `/save` writes to
`game-code/savegame.json` on that server; back up that file if you want to keep
the saved character.
