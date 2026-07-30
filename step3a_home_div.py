with open('index.html', 'r') as f:
    content = f.read()

old = '<div class="map-wrap"><canvas id="mc" width="393" height="500" style="width:100%;height:500px;display:block;"></canvas></div>'
new = '<div class="map-wrap"><div id="hmap" style="width:100%;height:500px;"></div></div>'

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: home canvas replaced with real map div")
