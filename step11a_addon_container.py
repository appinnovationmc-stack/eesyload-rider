with open('index.html', 'r') as f:
    content = f.read()

old = """        <div class="vc-lbl" style="padding:0;margin-bottom:14px;">Add-ons</div>
        <div class="addon-row" data-price="80" onclick="togAddon(this)">
          <div class="addon-l"><div class="addon-ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="9" cy="7" r="3" stroke="white" stroke-width="2"/><path d="M3 21c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="white" stroke-width="2" stroke-linecap="round"/><circle cx="17" cy="7" r="3" stroke="white" stroke-width="2"/><path d="M14 21c0-2 1.5-5 6-5" stroke="white" stroke-width="2" stroke-linecap="round"/></svg></div><div><div class="addon-n">Loading helpers</div><div class="addon-s">+R80 · 2 trained movers</div></div></div>
          <div class="tog"><div class="togt"></div></div>
        </div>
        <div class="addon-row" data-price="45" onclick="togAddon(this)">
          <div class="addon-l"><div class="addon-ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M21 8H3a1 1 0 00-1 1v11a1 1 0 001 1h18a1 1 0 001-1V9a1 1 0 00-1-1z" stroke="white" stroke-width="2"/><path d="M9 8V5a1 1 0 011-1h4a1 1 0 011 1v3" stroke="white" stroke-width="2"/></svg></div><div><div class="addon-n">Packing blankets</div><div class="addon-s">+R45 · Straps & wraps included</div></div></div>
          <div class="tog"><div class="togt"></div></div>
        </div>
        <div class="addon-row" data-price="30" onclick="togAddon(this)">
          <div class="addon-l"><div class="addon-ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div><div><div class="addon-n">Cargo insurance</div><div class="addon-s">+R30 · Cover up to R10,000</div></div></div>
          <div class="tog on"><div class="togt"></div></div>
        </div>
        <div class="addon-row" data-price="20" onclick="togAddon(this)">
          <div class="addon-l"><div class="addon-ic"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="4" y1="22" x2="4" y2="15" stroke="white" stroke-width="2" stroke-linecap="round"/></svg></div><div><div class="addon-n">Priority matching</div><div class="addon-s">+R20 · Skip the queue</div></div></div>
          <div class="tog"><div class="togt"></div></div>
        </div>"""

new = """        <div class="vc-lbl" style="padding:0;margin-bottom:14px;">Add-ons</div>
        <div id="addonRow"></div>"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: addon rows replaced with dynamic container")
