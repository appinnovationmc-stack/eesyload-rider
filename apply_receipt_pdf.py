#!/usr/bin/env python3
"""Replace stub downloadReceipt() with printable tax-style invoice / PDF."""
from pathlib import Path
import sys

HTML = Path(__file__).resolve().parent / "www" / "index.html"
if not HTML.exists():
    print("www/index.html missing", file=sys.stderr)
    sys.exit(1)

text = HTML.read_text(encoding="utf-8")

OLD = """function downloadReceipt(){
  alert('PDF export requires the EesyLoad backend to be connected. This will generate a downloadable PDF once wired to the server.');
}"""

NEW = r'''function downloadReceipt(){
  const loads=getLoads();
  const load=loads.find(l=>l.id===openLoadId)||loads[0];
  if(!load){alert('No receipt data available.');return;}
  const addonRows=(load.addons||[]).map(a=>
    `<tr><td style="padding:8px 0;border-bottom:1px solid #eee;">${a.name}</td><td style="text-align:right;padding:8px 0;border-bottom:1px solid #eee;">R${Number(a.price).toFixed(2)}</td></tr>`
  ).join('');
  const addonsTotal=(load.addons||[]).reduce((s,a)=>s+Number(a.price||0),0);
  const fare=Number(load.fare)||0;
  const base=Math.max(0,fare-addonsTotal);
  // SA-style tax invoice layout (VAT line shown as incl. — adjust when company VAT number is set)
  const vatRate=0.15;
  const totalIncl=fare;
  const net=totalIncl/(1+vatRate);
  const vat=totalIncl-net;
  const invNo=String(load.id||'').slice(0,8).toUpperCase();
  const paidAt=load.date?(load.date+(load.time?(' '+load.time):'')):(new Date().toLocaleString('en-ZA'));
  const html=`<!DOCTYPE html><html><head><meta charset="utf-8"><title>EesyLoad Invoice ${invNo}</title>
<style>
  body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#111;max-width:640px;margin:40px auto;padding:0 24px;}
  h1{font-size:22px;margin:0 0 4px;} .muted{color:#666;font-size:13px;}
  .hdr{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:28px;}
  .brand{font-weight:800;font-size:20px;color:#BB2235;}
  table{width:100%;border-collapse:collapse;margin:16px 0;}
  th{text-align:left;font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:#666;border-bottom:2px solid #111;padding:8px 0;}
  .totals td{padding:6px 0;}
  .totals .grand{font-size:18px;font-weight:800;}
  .box{background:#f7f7f8;border-radius:12px;padding:14px 16px;margin:16px 0;font-size:14px;line-height:1.5;}
  @media print{body{margin:0;} .noprint{display:none;}}
</style></head><body>
  <div class="hdr">
    <div>
      <div class="brand">EesyLoad</div>
      <div class="muted">On-demand goods transport · South Africa</div>
      <div class="muted" style="margin-top:8px;">support@eesyload.com</div>
    </div>
    <div style="text-align:right;">
      <h1>Tax Invoice</h1>
      <div class="muted">Invoice #EL-${invNo}</div>
      <div class="muted">${paidAt}</div>
    </div>
  </div>
  <div class="box">
    <strong>Trip</strong><br>
    From: ${load.pickup||'—'}<br>
    To: ${load.dropoff||'—'}<br>
    Driver: ${load.driverName||'—'} · ${load.driverVehicle||''}
  </div>
  <table>
    <thead><tr><th>Description</th><th style="text-align:right;">Amount (ZAR)</th></tr></thead>
    <tbody>
      <tr><td style="padding:8px 0;border-bottom:1px solid #eee;">Vehicle fare</td><td style="text-align:right;padding:8px 0;border-bottom:1px solid #eee;">R${base.toFixed(2)}</td></tr>
      ${addonRows}
    </tbody>
  </table>
  <table class="totals">
    <tr><td>Subtotal (excl. VAT)</td><td style="text-align:right;">R${net.toFixed(2)}</td></tr>
    <tr><td>VAT (15%)</td><td style="text-align:right;">R${vat.toFixed(2)}</td></tr>
    <tr><td class="grand">Total (incl. VAT)</td><td class="grand" style="text-align:right;">R${totalIncl.toFixed(2)}</td></tr>
  </table>
  <p class="muted" style="margin-top:28px;">Payment method: ${load.paymentMethod||load.payment_method||'In-app'} · Status: Paid / Completed</p>
  <p class="muted">This is a computer-generated tax invoice from EesyLoad. For company VAT number and formal B2B invoicing, contact support@eesyload.com.</p>
  <p class="noprint" style="margin-top:32px;">
    <button onclick="window.print()" style="background:#BB2235;color:#fff;border:0;padding:12px 20px;border-radius:10px;font-weight:600;cursor:pointer;">Print / Save as PDF</button>
  </p>
  <script>setTimeout(function(){try{window.print();}catch(e){}},400);<\/script>
</body></html>`;
  const w=window.open('','_blank');
  if(!w){alert('Please allow pop-ups to download the receipt.');return;}
  w.document.open();w.document.write(html);w.document.close();
}
'''

if "Tax Invoice" in text and "window.print()" in text and "function downloadReceipt" in text:
    print("✓ downloadReceipt already generates tax invoice")
elif OLD in text:
    text = text.replace(OLD, NEW, 1)
    HTML.write_text(text, encoding="utf-8")
    print("✓ downloadReceipt now opens printable tax invoice (Save as PDF)")
else:
    # Try looser match
    import re
    m = re.search(r"function downloadReceipt\(\)\{[^}]*\}", text)
    if m and "window.print" not in m.group(0):
        text = text[: m.start()] + NEW + text[m.end() :]
        HTML.write_text(text, encoding="utf-8")
        print("✓ downloadReceipt replaced (loose match)")
    else:
        print("! downloadReceipt pattern not found or already updated", file=sys.stderr)
        sys.exit(0)

print("Done.")
