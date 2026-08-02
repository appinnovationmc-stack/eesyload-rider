#!/usr/bin/env python3
"""
Patch: tokenize stray hardcoded colors in EesyLoad rider app.
Run from: ~/eesyload-rider
Usage: python3 patch_rider_tokens.py
"""
PATH = "index.html"

with open(PATH, "r", encoding="utf-8") as f:
    text = f.read()

changes = []

def apply(old, new, expected_count, label):
    global text
    count = text.count(old)
    if count != expected_count:
        print(f"SKIP [{label}] expected {expected_count} match(es), found {count}. No changes made for this item.")
        return
    text = text.replace(old, new)
    changes.append(label)
    print(f"OK [{label}] replaced {count} occurrence(s)")

# 1. Add --blu2 (and a matching light tint --blul) to dark :root
#    Rider's existing --blu is the darker brand blue #01649C
apply(
    "--ylw:#FFC043;--red:#FF3B30;--blu:#01649C;",
    "--ylw:#FFC043;--red:#FF3B30;--blu:#01649C;--blu2:#5B9CF6;--blul:rgba(91,156,246,.12);",
    1,
    "add --blu2 + --blul tokens (dark theme)"
)

# 2. Biz badge colour -> var(--blu2)
apply(
    "color:#5B9CF6;margin-bottom:14px;}",
    "color:var(--blu2);margin-bottom:14px;}",
    1,
    "biz-badge color -> var(--blu2)"
)

# 3. Error messages -> var(--red)
apply(
    'style="color:#FF3B30;font-size:13px;text-align:center;margin-top:8px;min-height:16px;"',
    'style="color:var(--red);font-size:13px;text-align:center;margin-top:8px;min-height:16px;"',
    1,
    "otp-error-msg -> var(--red)"
)
apply(
    'style="color:#FF3B30;font-size:13px;margin-top:4px;min-height:16px;"',
    'style="color:var(--red);font-size:13px;margin-top:4px;min-height:16px;"',
    1,
    "riderName-error-msg -> var(--red)"
)

# 4. Confirm overlay -> var(--bg)
apply(
    '<div style="flex:1;background:#080808;" onclick="closeConfirmIfSafe()"></div>',
    '<div style="flex:1;background:var(--bg);" onclick="closeConfirmIfSafe()"></div>',
    1,
    "confirm overlay -> var(--bg)"
)

# 5. Green strokes / fill (location pin, success checks, share)
apply(
    'stroke="#06C167"',
    'stroke="var(--grn)"',
    5,
    "green strokes -> var(--grn)"
)
apply(
    'fill="#06C167"',
    'fill="var(--grn)"',
    1,
    "green fill -> var(--grn)"
)

# 6. Brand-accent strokes (active nav, referral, search, SOS icons, etc.)
apply(
    'stroke="#BB2235"',
    'stroke="var(--acc)"',
    16,
    "accent strokes #BB2235 -> var(--acc)"
)

# 7. Star yellow
apply(
    'fill="#FFC043"',
    'fill="var(--ylw)"',
    1,
    "star fill -> var(--ylw)"
)
apply(
    'stroke="#FFC043"',
    'stroke="var(--ylw)"',
    5,
    "star strokes -> var(--ylw)"
)

# 8. Secondary grey #888
apply(
    'stroke="#888"',
    'stroke="var(--g40)"',
    27,
    "icon strokes #888 -> var(--g40)"
)
apply(
    'color:#888;margin-top:2px;',
    'color:var(--g40);margin-top:2px;',
    2,
    "subtitle #888 -> var(--g40)"
)

# 9. Red SOS / medical strokes -> var(--red)
apply(
    'stroke="#FF3B30"',
    'stroke="var(--red)"',
    3,
    "red strokes -> var(--red)"
)

if changes:
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\nSaved {PATH}. {len(changes)} patches applied.")
else:
    print("\nNo patches applied - file left unchanged.")
