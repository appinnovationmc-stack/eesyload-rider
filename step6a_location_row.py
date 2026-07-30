with open('index.html', 'r') as f:
    content = f.read()

old = '      <div class="sec-lbl">Recents</div>'

new = """      <div class="row" onclick="useCurrentLocationForPickup()" id="useCurrentLocationRow">
        <div class="ri"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="#06C167" stroke-width="2"/><circle cx="12" cy="12" r="2.5" fill="#06C167"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3" stroke="#06C167" stroke-width="2" stroke-linecap="round"/></svg></div>
        <div class="rb"><div class="rt" id="useCurrentLocationLabel">Use current location</div></div>
        <svg class="chev" width="8" height="13" viewBox="0 0 8 14" fill="none"><path d="M1 1l6 6-6 6" stroke="#444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <div class="sec-lbl">Recents</div>"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: use current location row added")
