#!/usr/bin/env python3
"""Generate link-card pages for queue entries. Each page carries og:image tags
so a tweet ending in this link renders a large image card. The page itself
shows the image and links out to the real paper."""
import html
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
QUEUE = Path("/home/antpc/x_pipeline/queue.jsonl")
SITE = "https://sahiliitm.github.io/xcards"

PAGE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<title>{title}</title>
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}/img/{eid}.jpg">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{margin:0;font-family:-apple-system,Georgia,serif;background:#0b0b0e;color:#e8e6e3}}
img{{width:100%;max-height:70vh;object-fit:cover;display:block}}
div{{max-width:640px;margin:0 auto;padding:28px 20px}}
h1{{font-size:24px;line-height:1.35;font-weight:600}}
a{{display:inline-block;margin-top:18px;padding:12px 22px;background:#1d9bf0;color:#fff;text-decoration:none;border-radius:999px;font-size:16px}}
p.small{{color:#8b8b93;font-size:14px;margin-top:24px}}
</style></head>
<body>
<img src="{site}/img/{eid}.jpg" alt="">
<div><h1>{title}</h1>
<a href="{paper}">read the paper &rarr;</a>
<p class="small">via @sahil_vi &middot; image: wikimedia commons</p>
</div></body></html>
"""


def main():
    entries = [json.loads(l) for l in QUEUE.read_text().splitlines() if l.strip()]
    paper_map = {}
    for e in entries:
        text = e["text"]
        if "paper: http" in text:
            paper_map[e["id"]] = text.split("paper: ", 1)[1].strip().split()[0]
    made = []
    for e in entries:
        eid = e["id"]
        img = BASE / "img" / f"{eid}.jpg"
        paper = paper_map.get(eid)
        if not img.exists() or not paper:
            continue
        first_line = e["text"].split("\n")[0].strip().rstrip(".")
        title = html.escape(first_line[:90])
        desc = html.escape(" ".join(e["text"].split())[:200])
        out = PAGE.format(title=title, desc=desc, site=SITE, eid=eid, paper=paper)
        (BASE / "p" / f"{eid}.html").write_text(out)
        made.append(eid)
    print("cards:", made)


if __name__ == "__main__":
    main()
