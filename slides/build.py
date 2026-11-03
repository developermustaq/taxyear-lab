"""Frame the recorded screenshots as 1920x1080 slide images.

Usage: python3 -I slides/build.py
Reads slides/raw/*.jpg, writes slides/out/<name>.png. Needs Google Chrome (headless).
"""

import html
import subprocess
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE = Path(__file__).resolve().parent

# name, step label, title, bullets, caption
SHOTS = [
    ("01-the-case", "THE CASE", "5 April lands in the wrong tax year.",
     ["All 5 tests pass.", "taxYear(2026-04-05) returns 2026/27.", "It should be 2025/26: the tax year ends on 5 April."],
     "Green tests are not the same as correct code."),
    ("02-haystack", "CONTEXT", "Same answer. A third of the tokens.",
     ["A: read all 2,000 log lines: 203,336 input tokens, 4 turns.", "B: search for the error line: 72,753 input tokens, 2 turns.",
      "Both quote line 1424."],
     "One run each, same model. Not a benchmark."),
    ("03-claude-md", "CLAUDE.md", "/clear wipes the chat. Not the rules.",
     ["Fresh session, no history.", "Claude still knows the tax-year rules.", "They come from CLAUDE.md, loaded every session."],
     "Durable rules live in files, not in the conversation."),
    ("04-fix-t20", "SKILL · /fix-bug", "Reproduce. Smallest fix. Prove it.",
     ["The skill names the CLAUDE.md rule the code breaks.", "One line changes; the signature stays.", "Then it runs npm test."],
     "The procedure lives in .claude/skills/fix-bug/SKILL.md."),
    ("04a-red", "VERIFY · RED", "The new test fails on the old code.",
     ["Claude added: keeps 5 April in the old tax year.", "Expected 2025/26, received 2026/27.", "1 failed, 5 passed."],
     "Re-run with the fix set aside (git stash) to show the red step."),
    ("04c-green", "VERIFY · GREEN", "With the fix: 6 of 6 pass.",
     ["Same test, fixed code.", "The old 5 tests still pass.", "This output is the evidence."],
     "Claude says it's fixed. The test suite proves it."),
    ("04d-diff", "THE DIFF", "The whole fix: one line becomes two.",
     ["Before: month >= April.", "After: after April, or April from the 6th.", "Review the diff yourself before you commit."],
     "Small, readable, reviewable."),
    ("04-fix-t40", "FACT OR ASSERTION?", "What is proven, believed and unknown.",
     ["FACT: what the test output proves.", "INFERENCE: believed, not proven.", "UNKNOWN: nobody has checked yet."],
     "Ask for this split on every report."),
    ("05-agents", "PARALLEL AGENTS", "Three reviewers: faster, not cheaper.",
     ["One agent: 200,671 tokens, 39 s.", "Three parallel read-only reviewers: 319,530 tokens, 19 s.",
      "Same main finding."],
     "One run each. Measure your own task."),
    ("06a-mcp-list", "MCP", "One project server. One tool.",
     [".mcp.json registers tax-calendar.", "/mcp shows it connected.", "Tool: get_tax_year_dates(startYear)."],
     "MCP gives Claude named tools with typed arguments."),
    ("06b-mcp-call", "MCP", "Ask the system of record, then check the code.",
     ["called tax-calendar: 2025-04-06 to 2026-04-05.", "taxYear(2026-04-05) gives 2026/27: wrong.", "No files edited."],
     "The tool result is data. The code check is the proof."),
    ("07b-deny-rule", "PERMISSIONS", "A deny rule is enforced, not requested.",
     ["settings.json denies Bash(git push *).", "Asked to push, Claude Code blocks it.", "The command never ran."],
     "CLAUDE.md asks. Permission rules enforce."),
]

CSS = """
body{margin:0;width:1920px;height:1080px;background:#F8F3F0;font-family:'Plus Jakarta Sans',sans-serif;color:#14284B;overflow:hidden}
.bar{position:absolute;left:90px;top:70px;width:270px;height:7px;background:#3CC6D8}
.label{position:absolute;left:90px;top:100px;font-size:24px;font-weight:800;letter-spacing:.06em;color:#5B6B85}
.tag{display:inline-block;margin-left:14px;padding:4px 12px;border-radius:14px;background:#014BAA;color:#fff;font-size:18px;letter-spacing:.08em}
h1{position:absolute;left:90px;top:150px;width:470px;margin:0;font-size:54px;line-height:1.08;font-weight:800;color:#014BAA;text-transform:uppercase}
ul{position:absolute;left:90px;top:560px;width:470px;margin:0;padding:0;list-style:none}
li{font-size:24px;line-height:1.35;margin:0 0 18px;padding-left:22px;position:relative}
li:before{content:'';position:absolute;left:0;top:13px;width:9px;height:9px;border-radius:5px;background:#3CC6D8}
.shot{position:absolute;left:600px;top:100px;width:1230px;height:738px;border-radius:14px;overflow:hidden;
      box-shadow:0 18px 50px rgba(20,40,75,.22);border:1px solid #d9d2cc}
.shot img{width:100%;height:100%;display:block}
.cap{position:absolute;left:600px;top:870px;width:1230px;font-size:30px;font-weight:800;color:#A8620F}
.foot{position:absolute;left:90px;bottom:34px;font-size:20px;font-weight:700;color:#5B6B85}
"""

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800'
         '&display=swap" rel="stylesheet">')


def page(name, label, title, bullets, caption):
    e = html.escape
    items = "".join(f"<li>{e(b)}</li>" for b in bullets)
    img = (HERE / "raw" / f"{name}.jpg").as_uri()
    return (f"<!doctype html><html><head><meta charset='utf-8'>{FONTS}<style>{CSS}</style></head><body>"
            f"<div class='bar'></div><div class='label'>{e(label)}<span class='tag'>RECORDED RUN</span></div>"
            f"<h1>{e(title)}</h1><ul>{items}</ul>"
            f"<div class='shot'><img src='{img}'></div><div class='cap'>{e(caption)}</div>"
            f"<div class='foot'>TAXYEAR-LAB · VS CODE + CLAUDE CODE · REAL OUTPUT, 2026-11-04</div></body></html>")


if __name__ == "__main__":
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    for name, *rest in SHOTS:
        f = out / f"{name}.html"
        f.write_text(page(name, *rest))
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--disable-gpu", "--allow-file-access-from-files",
                        "--window-size=1920,1080", "--virtual-time-budget=8000",
                        f"--screenshot={out / (name + '.png')}", f.as_uri()], check=True, capture_output=True)
        f.unlink()
        print("rendered", name)
