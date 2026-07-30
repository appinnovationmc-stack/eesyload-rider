with open('index.html', 'r') as f:
    content = f.read()

old = "  if(id==='home'){initHomeMap();}else{stopHomeMapWatch();}"
new = "  if(id==='home'){initHomeMap();renderSavedAddressesUI();}else{stopHomeMapWatch();}"

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: renderSavedAddressesUI wired into home screen load")
