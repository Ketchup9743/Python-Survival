from pathlib import Path

import web_server


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "dist"


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(web_server.HTML_PAGE, encoding="utf-8")
    print(f"Built Cloudflare Pages site in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
