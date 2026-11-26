"""Builds the no-server replay pages from one recording:
  control/control_replay_offline.html   full page, opens from disk (presentation fallback)
  control/control_replay_artifact.html  fragment for publishing as an Artifact"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
name = sys.argv[1]
rec = (ROOT / "recordings" / f"{name}.json").read_text()
html = (ROOT / "control/index.html").read_text()
tag = '<script id="inline-recording" type="application/json">' + rec.replace("</", "<\\/") + "</script>\n<script>"
html = html.replace("<script>\n(() => {", tag + "\n(() => {", 1)
(ROOT / "control/control_replay_offline.html").write_text(html)
head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
body = re.search(r"<body>(.*)</body>", html, re.S).group(1)
head = re.sub(r'<meta charset="utf-8">\s*|<meta name="viewport"[^>]*>\s*', "", head)
(ROOT / "control/control_replay_artifact.html").write_text(head.strip() + "\n" + body.strip() + "\n")
print(f"built offline + artifact pages from {name} ({len(html) // 1024} KB)")
