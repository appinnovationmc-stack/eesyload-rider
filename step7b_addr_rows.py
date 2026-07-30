with open('index.html', 'r') as f:
    content = f.read()

old = """      <div class="row" onclick="go('booking')">
        <div class="ri"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="9,22 9,12 15,12 15,22" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div class="rb"><div class="rt">Home</div></div>
        <svg class="chev" width="8" height="13" viewBox="0 0 8 14" fill="none"><path d="M1 1l6 6-6 6" stroke="#444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <div class="row" onclick="go('booking')">
        <div class="ri"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="20" height="14" rx="2" stroke="#888" stroke-width="2"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2" stroke="#888" stroke-width="2"/></svg></div>
        <div class="rb"><div class="rt">Work</div></div>
        <svg class="chev" width="8" height="13" viewBox="0 0 8 14" fill="none"><path d="M1 1l6 6-6 6" stroke="#444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <div class="row" onclick="go('booking')">
        <div class="ri"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0118 0z" stroke="#888" stroke-width="2"/><circle cx="12" cy="10" r="3" stroke="#888" stroke-width="2"/></svg></div>
        <div class="rb"><div class="rt">Add new address</div></div>
        <svg class="chev" width="8" height="13" viewBox="0 0 8 14" fill="none"><path d="M1 1l6 6-6 6" stroke="#444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>"""

new = """      <div class="row" onclick="useOrAddSavedAddress('Home')">
        <div class="ri"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="9,22 9,12 15,12 15,22" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
        <div class="rb"><div class="rt">Home</div><div class="rs" id="savedAddrHomeSub" style="font-size:12px;color:#888;margin-top:2px;">Tap to add</div></div>
        <svg class="chev" width="8" height="13" viewBox="0 0 8 14" fill="none"><path d="M1 1l6 6-6 6" stroke="#444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <div class="row" onclick="useOrAddSavedAddress('Work')">
        <div class="ri"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="2" y="7" width="20" height="14" rx="2" stroke="#888" stroke-width="2"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2" stroke="#888" stroke-width="2"/></svg></div>
        <div class="rb"><div class="rt">Work</div><div class="rs" id="savedAddrWorkSub" style="font-size:12px;color:#888;margin-top:2px;">Tap to add</div></div>
        <svg class="chev" width="8" height="13" viewBox="0 0 8 14" fill="none"><path d="M1 1l6 6-6 6" stroke="#444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>
      <div class="row" onclick="addCustomSavedAddress()">
        <div class="ri"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0118 0z" stroke="#888" stroke-width="2"/><circle cx="12" cy="10" r="3" stroke="#888" stroke-width="2"/></svg></div>
        <div class="rb"><div class="rt">Add new address</div></div>
        <svg class="chev" width="8" height="13" viewBox="0 0 8 14" fill="none"><path d="M1 1l6 6-6 6" stroke="#444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: Home/Work/Add rows wired to real functions")
