with open('index.html', 'r') as f:
    content = f.read()

old = """  <div id="booking" class="scr">
    <div class="scroll" style="padding-bottom:150px;">"""

new = """  <div id="booking" class="scr">
    <div class="scroll" style="padding-bottom:260px;">"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: booking screen padding increased to clear footer overlay")
