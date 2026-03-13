#!/usr/bin/env python3
"""Minimal static blog builder. Converts markdown posts to HTML with KaTeX."""

import re
import shutil
from pathlib import Path

POSTS_DIR = Path("posts")
OUTPUT_DIR = Path("docs")
ASSETS_SRC = POSTS_DIR  # assets referenced relative to posts
ASSETS_DST = OUTPUT_DIR / "assets"

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<style>
  body {{
    max-width: 38em;
    margin: 2em auto;
    padding: 0 1em;
    font-family: 'Latin Modern Roman', 'Computer Modern', Georgia, serif;
    font-size: 18px;
    line-height: 1.6;
    color: #222;
    background: #fdfdfd;
  }}
  h1 {{ font-size: 1.6em; margin-bottom: 0.2em; }}
  h2 {{ font-size: 1.25em; margin-top: 1.8em; }}
  .date {{ color: #888; font-size: 0.9em; margin-bottom: 2em; }}
  .katex-display {{ overflow-x: auto; overflow-y: hidden; }}
  img {{ max-width: 100%; border-radius: 4px; }}
  a {{ color: #245; }}
  .home {{ font-size: 0.9em; margin-bottom: 1.5em; }}
  .home a {{ text-decoration: none; color: #666; }}
</style>
</head>
<body>
<div class="home"><a href="index.html">&larr; all posts</a></div>
<h1>{title}</h1>
<div class="date">{date}</div>
{body}
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<script>
renderMathInElement(document.body, {{
  delimiters: [
    {{left: "$$", right: "$$", display: true}},
    {{left: "$", right: "$", display: false}}
  ]
}});
</script>
</body>
</html>
"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Complex Analysis</title>
<style>
  body {{
    max-width: 38em;
    margin: 2em auto;
    padding: 0 1em;
    font-family: 'Latin Modern Roman', 'Computer Modern', Georgia, serif;
    font-size: 18px;
    line-height: 1.6;
    color: #222;
    background: #fdfdfd;
  }}
  h1 {{ font-size: 1.6em; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ margin: 0.8em 0; }}
  a {{ color: #245; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .date {{ color: #888; font-size: 0.85em; margin-left: 0.5em; }}
</style>
</head>
<body>
<h1>Complex Analysis</h1>
<ul>
{entries}
</ul>
</body>
</html>
"""


def parse_post(path: Path) -> dict:
    text = path.read_text()
    meta = {}
    body = text

    if text.startswith("---"):
        _, front, rest = text.split("---", 2)
        body = rest.strip()
        for line in front.strip().splitlines():
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip()

    return {"meta": meta, "body": body, "slug": path.stem}


def md_to_html(md: str) -> str:
    """Bare-minimum markdown to HTML. Handles headers, paragraphs, bold, images, inline code, and raw HTML blocks."""
    lines = md.split("\n")
    html_parts = []
    in_paragraph = False
    in_html_block = False
    html_block_lines = []
    html_block_depth = 0
    html_block_tag = ""

    for line in lines:
        stripped = line.strip()

        # Raw HTML block passthrough: accumulate lines between opening and closing tags
        if in_html_block:
            html_block_lines.append(line)
            html_block_depth += len(re.findall(rf"<{html_block_tag}[\s>]", line))
            html_block_depth -= len(re.findall(rf"</{html_block_tag}>", line))
            if html_block_depth <= 0:
                html_parts.append("\n".join(html_block_lines))
                html_block_lines = []
                in_html_block = False
            continue

        if m := re.match(r"^<(div|style|script|section)[\s>]", stripped):
            if in_paragraph:
                html_parts.append("</p>")
                in_paragraph = False
            html_block_tag = m.group(1)
            html_block_depth = 1
            html_block_depth -= len(re.findall(rf"</{html_block_tag}>", stripped))
            html_block_lines = [line]
            if html_block_depth <= 0:
                html_parts.append("\n".join(html_block_lines))
                html_block_lines = []
            else:
                in_html_block = True
            continue

        if not stripped:
            if in_paragraph:
                html_parts.append("</p>")
                in_paragraph = False
            continue

        # Headers
        if m := re.match(r"^(#{1,6})\s+(.*)", stripped):
            if in_paragraph:
                html_parts.append("</p>")
                in_paragraph = False
            level = len(m.group(1))
            html_parts.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue

        # Images
        if m := re.match(r"^!\[([^\]]*)\]\(([^)]+)\)", stripped):
            if in_paragraph:
                html_parts.append("</p>")
                in_paragraph = False
            html_parts.append(f'<img src="{m.group(2)}" alt="{m.group(1)}">')
            continue

        if not in_paragraph:
            html_parts.append("<p>")
            in_paragraph = True
        else:
            html_parts.append(" ")

        html_parts.append(inline(stripped))

    if in_paragraph:
        html_parts.append("</p>")

    return "\n".join(html_parts)


def inline(text: str) -> str:
    """Handle bold and inline code (but not $ -- KaTeX handles that client-side)."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def build():
    OUTPUT_DIR.mkdir(exist_ok=True)
    ASSETS_DST.mkdir(exist_ok=True)

    # Copy assets
    src_assets = Path("assets")
    if src_assets.exists():
        for f in src_assets.iterdir():
            shutil.copy2(f, ASSETS_DST / f.name)

    posts = sorted(
        (parse_post(p) for p in POSTS_DIR.glob("*.md")),
        key=lambda p: p["meta"].get("date", ""),
        reverse=True,
    )

    for post in posts:
        html_body = md_to_html(post["body"])
        html = TEMPLATE.format(
            title=post["meta"].get("title", post["slug"]),
            date=post["meta"].get("date", ""),
            body=html_body,
        )
        (OUTPUT_DIR / f"{post['slug']}.html").write_text(html)
        print(f"  built {post['slug']}.html")

    entries = "\n".join(
        f'<li><a href="{p["slug"]}.html">{p["meta"].get("title", p["slug"])}</a>'
        f'<span class="date">{p["meta"].get("date", "")}</span></li>'
        for p in posts
    )
    (OUTPUT_DIR / "index.html").write_text(INDEX_TEMPLATE.format(entries=entries))
    print(f"  built index.html ({len(posts)} posts)")


if __name__ == "__main__":
    build()
