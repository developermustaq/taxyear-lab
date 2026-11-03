"""Render the closing two slides (repo map, QR code) as 1920x1080 images.

Usage: python3 -I slides/endslides.py <qr-ledgerlab.svg> <qr-taxyear.svg>
Writes slides/out/90-ledgerlab-map.png and slides/out/91-qr.png. Needs Google Chrome (headless).
"""

import html
import subprocess
import sys
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = Path(__file__).resolve().parent / "out"
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800'
         '&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">')
BASE = """body{margin:0;width:1920px;height:1080px;font-family:'Plus Jakarta Sans',sans-serif;overflow:hidden}
code{font-family:'JetBrains Mono',monospace;font-size:.86em}"""

# what you learned today -> what it becomes in ledgerlab
ROWS = [
    ("The case", "Release v0.8.0 blocked: a PAID invoice moves back to DRAFT. Unit tests pass; the CI contract check fails.", "npm run ci:contract"),
    ("Context", "A 2,000-line CI log with one real error. Measure reading it all vs searching it.", "npm run measure:haystack"),
    ("CLAUDE.md", "Rules plus progress.md let a fresh session recover all seven constraints.", "npm run measure:recovery"),
    ("Skill", "release-triage: evidence first, smallest fix, approval, verify.", "/release-triage"),
    ("Agents", "developer-reviewer, qa-investigator, ops-reviewer in parallel, read-only.", "npm run measure:agents"),
    ("MCP", "Resolve incident INC-104 over MCP or the web UI. Its note claims a fix: check it.", "npm run incidents:web"),
    ("Permissions", "Denied: fixtures, .env, curl. Writes to the incident system need a human.", ".claude/settings.json"),
    ("Checkpoints", "Four branches from blocked to fixed. npm run where tells you your step.", "npm run where"),
]


def map_page():
    e = html.escape
    rows = "".join(
        f"<div class='row'><div class='k'>{e(k)}</div><div class='v'>{e(v)}</div><div class='c'><code>{e(c)}</code></div></div>"
        for k, v, c in ROWS)
    css = BASE + """
body{background:#F8F3F0;color:#14284B}
.bar{position:absolute;left:90px;top:70px;width:270px;height:7px;background:#3CC6D8}
.label{position:absolute;left:90px;top:100px;font-size:24px;font-weight:800;letter-spacing:.06em;color:#5B6B85}
h1{position:absolute;left:90px;top:140px;margin:0;font-size:68px;font-weight:800;color:#014BAA;text-transform:uppercase}
.sub{position:absolute;left:90px;top:232px;font-size:28px;color:#5B6B85}
.grid{position:absolute;left:90px;top:300px;width:1740px}
.row{display:flex;align-items:center;background:#fff;border-radius:14px;margin-bottom:12px;height:76px}
.k{width:230px;padding-left:28px;font-size:26px;font-weight:800;color:#014BAA}
.v{flex:1;font-size:23px;padding-right:20px}
.c{width:400px;font-size:23px;color:#A8620F;font-weight:700}
.foot{position:absolute;left:90px;bottom:34px;font-size:20px;font-weight:700;color:#5B6B85}
"""
    return (f"<!doctype html><html><head><meta charset='utf-8'>{FONTS}<style>{css}</style></head><body>"
            "<div class='bar'></div><div class='label'>WHAT'S IN THE REPO</div>"
            "<h1>Today's ideas, at full size.</h1>"
            "<div class='sub'>LedgerLab: the same workflow on a real-shaped problem. Synthetic data, two systems, a CI gate.</div>"
            f"<div class='grid'>{rows}</div>"
            "<div class='foot'>github.com/developermustaq/ledgerlab · start at walkthrough/00-start-here.md</div></body></html>")


def qr_page(qr_main, qr_warm):
    css = BASE + """
body{background:#014BAA;color:#fff}
.bar{position:absolute;left:90px;top:70px;width:270px;height:7px;background:#3CC6D8}
.label{position:absolute;left:90px;top:100px;font-size:24px;font-weight:800;letter-spacing:.06em;color:#BFD4F2}
h1{position:absolute;left:90px;top:150px;width:1000px;margin:0;font-size:96px;line-height:1.02;font-weight:800;text-transform:uppercase}
.p{position:absolute;left:90px;top:540px;width:960px;font-size:32px;line-height:1.45;color:#E6EEF8}
.url{position:absolute;left:90px;top:760px;font-size:40px;font-weight:800;color:#3CC6D8}
.warm{position:absolute;left:90px;top:840px;font-size:24px;color:#BFD4F2}
.qr{position:absolute;left:1210px;top:150px;width:620px;height:620px;background:#fff;border-radius:28px;padding:30px;box-sizing:border-box}
.qr svg{width:100%;height:100%}
.qrcap{position:absolute;left:1210px;top:800px;width:620px;text-align:center;font-size:26px;font-weight:700}
.foot{position:absolute;left:90px;bottom:34px;font-size:20px;font-weight:700;color:#BFD4F2}
"""
    return (f"<!doctype html><html><head><meta charset='utf-8'>{FONTS}<style>{css}</style></head><body>"
            "<div class='bar'></div><div class='label'>YOUR TURN · AFTER THE SESSION</div>"
            "<h1>Learnt something? Put it to the test.</h1>"
            "<div class='p'>Clone LedgerLab, read the CI failure, and take it from blocked to green "
            "with CLAUDE.md, a skill, agents, MCP and permissions. Every step has a checkpoint.</div>"
            "<div class='url'>github.com/developermustaq/ledgerlab</div>"
            "<div class='warm'>Warm-up from today's slides: github.com/developermustaq/taxyear-lab</div>"
            f"<div class='qr'>{qr_main}</div><div class='qrcap'>Scan for LedgerLab</div>"
            "<div class='foot'>Synthetic data only · never put client data or keys in a sandbox</div></body></html>")


def render(name, doc):
    f = OUT / f"{name}.html"
    f.write_text(doc)
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--disable-gpu", "--window-size=1920,1080",
                    "--virtual-time-budget=8000", f"--screenshot={OUT / (name + '.png')}", f.as_uri()],
                   check=True, capture_output=True)
    f.unlink()
    print("rendered", name)


if __name__ == "__main__":
    qr_main = Path(sys.argv[1]).read_text().split("?>", 1)[-1]
    qr_warm = Path(sys.argv[2]).read_text().split("?>", 1)[-1]
    OUT.mkdir(exist_ok=True)
    render("90-ledgerlab-map", map_page())
    render("91-qr", qr_page(qr_main, qr_warm))
