with open('index.html', 'r') as f:
    content = f.read()

old = """        <div class="ref-code" id="ref-code">—</div>
        <div class="ref-code-sub">Your unique referral code</div>"""

new = """        <div class="ref-code" id="ref-code">—</div>
        <div class="ref-code-sub">Your unique referral code</div>
      </div>
      <div class="ref-code-box" id="enterCodeBox">
        <div style="font-size:13px;font-weight:700;margin-bottom:10px;">Have a friend's code?</div>
        <input id="friendCodeInput" placeholder="Enter code" style="width:100%;background:var(--s2);border:1px solid var(--b);border-radius:10px;padding:10px 12px;font-family:var(--f);font-size:14px;color:var(--w);margin-bottom:10px;">
        <button class="cta" onclick="submitFriendCode()" style="width:100%;">Apply code</button>
        <div id="friendCodeMsg" style="font-size:12px;margin-top:8px;"></div>"""

if old not in content:
    print("ERROR: exact match not found")
else:
    content = content.replace(old, new, 1)
    with open('index.html', 'w') as f:
        f.write(content)
    print("SUCCESS: enter friend code UI added")
