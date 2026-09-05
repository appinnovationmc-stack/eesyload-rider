#!/usr/bin/env python3
from pathlib import Path
import re
p = Path(__file__).resolve().parents[1] / "www" / "index.html"
t = p.read_text(encoding="utf-8")
names = [
    "submitBooking",
    "calculateRouteDistance",
    "routeAndUpdateEta",
    "_geocodeAddressText",
    "initBookingDefaults",
    "payAndFindDriver",
    "findDriver",
    "markDelivered",
]
changed = []
for name in names:
    old = f"function {name}("
    new = f"async function {name}("
    if old in t and f"async function {name}(" not in t:
        t = t.replace(old, new)
        changed.append(name)
# generic: function foo(){ await
pattern = re.compile(r"(?<!async )function ([A-Za-z0-9_]+)\(([^)]*)\)\{\s*await ")
def repl(m):
    changed.append(m.group(1))
    return f"async function {m.group(1)}({m.group(2)}){{\n  await "
t2, n = pattern.subn(repl, t)
t = t2
if "glass.css" not in t:
    t = t.replace("</head>", '<link rel="stylesheet" href="glass.css">\n</head>')
    changed.append("glass.css")
p.write_text(t, encoding="utf-8")
print("changed:", ", ".join(changed) if changed else "none")
print("has splash timeout", "go('onboard')" in t)
