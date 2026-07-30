with open('index.html', 'r') as f:
    content = f.read()

old = "if(id==='booking')initBookingDefaults();"
new = "if(id==='booking'){initBookingDefaults();initAddressAutocomplete();}"

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: autocomplete wired into booking screen")
