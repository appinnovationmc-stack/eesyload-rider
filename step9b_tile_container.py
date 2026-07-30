with open('index.html', 'r') as f:
    content = f.read()

old = """      <div class="tile-row">
        <div class="tile on" onclick="selTile(this)">
          <div class="ti"><svg width="40" height="24" viewBox="0 0 50 28" fill="none"><rect x="14" y="3" width="32" height="16" rx="2.5" stroke="white" stroke-width="1.8"/><path d="M3 13h11l5-10h6" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 13v8h47v-8" stroke="white" stroke-width="1.8" stroke-linecap="round"/><circle cx="12" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="39" cy="24" r="4" stroke="white" stroke-width="1.8"/></svg></div>
          <span class="tl">Bakkie</span>
        </div>
        <div class="tile" onclick="selTile(this)">
          <div class="ti"><svg width="40" height="24" viewBox="0 0 52 28" fill="none"><rect x="2" y="4" width="32" height="16" rx="2" stroke="white" stroke-width="1.8"/><path d="M34 9h12l5 8v4H34V9z" stroke="white" stroke-width="1.8" stroke-linejoin="round"/><circle cx="11" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="26" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="43" cy="24" r="4" stroke="white" stroke-width="1.8"/></svg></div>
          <span class="tl">Truck</span>
        </div>
        <div class="tile" onclick="selTile(this)">
          <div class="ti"><svg width="40" height="24" viewBox="0 0 50 28" fill="none"><path d="M2 20V11c0-2 1.5-4 3-4L22 4h22a3 3 0 013 3v13" stroke="white" stroke-width="1.8" stroke-linecap="round"/><path d="M2 20h46" stroke="white" stroke-width="1.8" stroke-linecap="round"/><rect x="6" y="7" width="9" height="7" rx="1.5" stroke="white" stroke-width="1.5"/><rect x="18" y="7" width="9" height="7" rx="1.5" stroke="white" stroke-width="1.5"/><circle cx="11" cy="24" r="4" stroke="white" stroke-width="1.8"/><circle cx="37" cy="24" r="4" stroke="white" stroke-width="1.8"/></svg></div>
          <span class="tl">Van</span>
        </div>
        <div class="tile" onclick="selTile(this)">
          <div class="ti"><svg width="36" height="24" viewBox="0 0 42 26" fill="none"><circle cx="9" cy="20" r="5.5" stroke="white" stroke-width="1.8"/><circle cx="33" cy="20" r="5.5" stroke="white" stroke-width="1.8"/><path d="M14.5 20H27.5M21 20V9" stroke="white" stroke-width="1.8" stroke-linecap="round"/><path d="M15 9h12l4 6H11l4-6z" stroke="white" stroke-width="1.8" stroke-linejoin="round"/><path d="M21 9V4l5-3" stroke="white" stroke-width="1.8" stroke-linecap="round"/></svg></div>
          <span class="tl">Moto</span>
        </div>
        <div class="tile" onclick="selTile(this)">
          <div class="ti"><svg width="34" height="24" viewBox="0 0 38 26" fill="none"><circle cx="12" cy="7" r="4" stroke="white" stroke-width="1.8"/><path d="M4 24c0-4.4 3.6-7 8-7s8 2.6 8 7" stroke="white" stroke-width="1.8" stroke-linecap="round"/><circle cx="27" cy="6" r="3.2" stroke="white" stroke-width="1.6"/><path d="M20 24c0-3.5 3-6 7-6" stroke="white" stroke-width="1.6" stroke-linecap="round"/></svg></div>
          <span class="tl">Helpers</span>
        </div>
      </div>"""

new = '      <div class="tile-row" id="tileRow"></div>'

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: static tiles replaced with dynamic container")
