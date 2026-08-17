# -*- coding: utf-8 -*-
"""Generate a self-contained RTL pricing page for Manooch from the R&D markdown."""
import base64, re, html

MD = open('uploads/manooch-pricing-rnd-final.md', encoding='utf-8').read()

# ---------- parse markdown tables ----------
lines = MD.splitlines()
tables, cur = [], []
for ln in lines:
    if ln.strip().startswith('|'):
        cur.append(ln.strip())
    else:
        if cur:
            tables.append(cur); cur = []
if cur:
    tables.append(cur)

def parse_table(rows):
    out = []
    for r in rows:
        cells = [c.strip() for c in r.strip().strip('|').split('|')]
        out.append(cells)
    return out

plans_md   = parse_table(tables[0])   # header, sep, 3 rows
big_md     = parse_table(tables[1])   # 121 data rows
plugins_md = parse_table(tables[2])

# ---------- fonts ----------
WEIGHTS = {
    'Ravi-Regular.woff2': 400,
    'Ravi-Medium.woff2': 500,
    'Ravi-SemiBold.woff2': 600,
    'Ravi-Bold.woff2': 700,
    'Ravi-ExtraBlack.woff2': 900,
}
font_faces = []
for fname, w in WEIGHTS.items():
    b64 = base64.b64encode(open(f'Ravi/{fname}', 'rb').read()).decode()
    font_faces.append(
        f"@font-face{{font-family:'Ravi';font-style:normal;font-weight:{w};font-display:swap;"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
    )
FONT_CSS = "\n".join(font_faces)

# ---------- cell rendering helpers ----------
def render_plan_cell(v):
    v = v.strip()
    if v == '✅':
        return '<span class="chk yes"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>'
    if v == '❌':
        return '<span class="chk no"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></span>'
    plain = v.replace('**', '')
    if plain == 'نامحدود':
        return '<span class="pill inf">نامحدود</span>'
    if plain == 'جدا':
        return '<span class="pill sep">جدا</span>'
    # bold inline
    v = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', v)
    return f'<span class="pval">{v}</span>'

def render_price_cell(v):
    v = v.strip()
    if v in ('—', ''):
        return '<span class="muted dash">—</span>'
    if v in ('همراه ماژول',):
        return '<span class="chip">همراه ماژول</span>'
    if v.startswith('زیرمجموعه'):
        return f'<span class="chip sub">{v}</span>'
    if v == 'بر اساس مصرف':
        return '<span class="muted small">بر اساس مصرف</span>'
    v = re.sub(r'\*\*(.+?)\*\*', r'<b class="price">\1</b>', v)
    return f'<span class="pval">{v}</span>'

# ---------- plans overview cards ----------
PLAN_CARDS = [
    # name, price, tagline, tag, tagclass
    ("پایه", "۶۹۰٬۰۰۰", "تومان / ماه", "شروع فروش آنلاین", None, None),
    ("استاندارد", "۱٬۲۹۰٬۰۰۰", "تومان / ماه", "مدیریت حرفه‌ای فروش", "پیشنهاد منوچ", "hot"),
    ("پرو", "۲٬۴۹۰٬۰۰۰", "تومان / ماه", "رشد، اتوماسیون و وفادارسازی", None, None),
]

cards_html = []
for name, price, unit, tagline, tag, tagcls in PLAN_CARDS:
    tag_html = f'<span class="ptag {tagcls}">{tag}</span>' if tag else ''
    card_cls = 'pcard hot' if tagcls == 'hot' else ('pcard dark' if name == 'پرو' else 'pcard')
    cards_html.append(f'''
      <article class="{card_cls}">
        {tag_html}
        <h3 class="pname">{name}</h3>
        <p class="ptagline">{tagline}</p>
        <div class="pprice"><span class="num">{price}</span><span class="unit">{unit}</span></div>
        <a class="pcta" href="#">شروع با {name}</a>
      </article>''')
CARDS_HTML = "\n".join(cards_html)

# ---------- big comparison table ----------
# rows: [category, feature, base, std, pro, standalone]
data_rows = big_md[2:]  # skip header + separator

body_groups = []   # list of (category, [rows])
for cat, feat, base, std, pro, price in data_rows:
    if cat.startswith('**'):
        body_groups.append((cat.strip('*'), []))
    body_groups[-1][1].append((feat, base, std, pro, price))

def group_html(cat, rows):
    trs = []
    for feat, base, std, pro, price in rows:
        trs.append(
            f'<tr><td class="feat">{feat}</td>'
            f'<td class="p p-base">{render_plan_cell(base)}</td>'
            f'<td class="p p-std">{render_plan_cell(std)}</td>'
            f'<td class="p p-pro">{render_plan_cell(pro)}</td>'
            f'<td class="pl">{render_price_cell(price)}</td></tr>'
        )
    return (
        f'<tr class="grouph"><td colspan="5"><span class="gname">{html.escape(cat)}</span></td></tr>'
        + "\n".join(trs)
    )

cmp_tbody = "\n".join(group_html(c, r) for c, r in body_groups)

# ---------- plugins table ----------
plug_rows = plugins_md[2:]
plug_trs = []
for name, price in plug_rows:
    nm = re.sub(r'\*\*(.+?)\*\*', r'\1', name).strip()
    pr = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', price).strip()
    plug_trs.append(f'<tr><td class="feat">{html.escape(nm)}</td><td class="pl">{pr}</td></tr>')
PLUG_TBODY = "\n".join(plug_trs)

# ---------- non-standalone items (section 7) ----------
NONSTAND = ["تعداد محصول", "تعداد عکس محصول", "ویس محصول", "ویژگی محصول", "رنگ",
            "سایز", "ظرفیت ذخیره‌سازی", "محصولات ارزی", "سایر Limitهای پلن"]
chips = "\n".join(f'<li>{x}</li>' for x in NONSTAND)

# ---------- assemble ----------
page = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تعرفه‌های منوچ — پلن‌ها و افزونه‌ها</title>
<style>
{FONT_CSS}
:root{{
  --brand:#4B45E6; --brand-2:#7C5CFC; --ink:#202A37; --mut:#8A90A6;
  --bg:#f5f5fb; --line:#e8e8f2; --green:#12A15A; --green-bg:#EAF7F0;
  --red:#E5484D; --red-bg:#FDECEC; --card:#ffffff;
}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{
  font-family:'Ravi','Vazirmatn',Tahoma,sans-serif; color:var(--ink);
  background:var(--bg); line-height:1.75;
  background-image:radial-gradient(60% 40% at 100% 0%, rgba(124,92,252,.10), transparent 60%),
                   radial-gradient(50% 40% at 0% 10%, rgba(75,69,230,.08), transparent 60%);
}}
.wrap{{max-width:1180px;margin-inline:auto;padding-inline:20px}}
a{{text-decoration:none;color:inherit}}

/* ---------- header ---------- */
.phead{{text-align:center;padding:72px 20px 18px}}
.kicker{{
  display:inline-block;background:rgba(75,69,230,.08);color:var(--brand);
  border:1px solid rgba(75,69,230,.22);font-size:13.5px;font-weight:700;
  padding:7px 16px;border-radius:999px;margin-bottom:18px;
}}
.phead h1{{font-size:clamp(28px,4vw,44px);font-weight:900;margin:0 0 12px;line-height:1.35}}
.phead p{{color:var(--mut);font-size:clamp(14.5px,1.4vw,17px);max-width:640px;margin:0 auto}}

/* ---------- plan cards ---------- */
.plans{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin:44px auto 16px;align-items:stretch}}
.pcard{{
  position:relative;background:var(--card);border:1px solid var(--line);
  border-radius:22px;padding:30px 28px;display:flex;flex-direction:column;
  transition:transform .2s ease, box-shadow .2s ease;
}}
.pcard:hover{{transform:translateY(-5px);box-shadow:0 24px 48px rgba(32,42,55,.12)}}
.pcard.hot{{border:2px solid var(--brand);box-shadow:0 18px 44px rgba(75,69,230,.16)}}
.pcard.dark{{
  color:#fff;border:none;
  background:radial-gradient(70% 60% at 88% -10%, rgba(139,92,246,.45), transparent 60%),
             linear-gradient(150deg,#232945,#2f2a63 55%,#3b34a8);
  box-shadow:0 24px 56px rgba(35,41,69,.35);
}}
.ptag{{
  position:absolute;top:-14px;inset-inline-start:50%;transform:translateX(50%);
  background:var(--brand);color:#fff;font-size:12.5px;font-weight:700;
  padding:5px 16px;border-radius:999px;white-space:nowrap;
}}
.pname{{font-size:21px;font-weight:800;margin:0 0 4px}}
.pcard.dark .pname{{color:#fff}}
.ptagline{{color:var(--mut);font-size:13.5px;margin:0 0 20px;min-height:44px}}
.pcard.dark .ptagline{{color:rgba(255,255,255,.72)}}
.pprice{{display:flex;align-items:baseline;gap:8px;margin-bottom:22px}}
.pprice .num{{font-size:34px;font-weight:900;letter-spacing:-.5px}}
.pprice .unit{{color:var(--mut);font-size:13px}}
.pcard.dark .pprice .unit{{color:rgba(255,255,255,.65)}}
.pcta{{
  display:block;text-align:center;font-weight:700;font-size:15px;
  padding:13px 20px;border-radius:12px;background:var(--ink);color:#fff;
  transition:background .18s ease;margin-top:auto;
}}
.pcta:hover{{background:#151b28}}
.pcard.hot .pcta{{background:var(--brand)}}
.pcard.hot .pcta:hover{{background:#3a35c9}}
.pcard.dark .pcta{{background:#fff;color:#3b34a8}}
.pcard.dark .pcta:hover{{background:#f2f1ff}}

/* ---------- sections ---------- */
.sec{{margin:56px auto 0}}
.sec-head{{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:18px;flex-wrap:wrap}}
.sec-head h2{{font-size:clamp(20px,2.4vw,28px);font-weight:900;margin:0}}
.sec-head p{{color:var(--mut);font-size:13.5px;margin:0}}
.note{{
  margin:12px auto 0;font-size:12.5px;color:var(--mut);
  background:rgba(75,69,230,.05);border:1px dashed rgba(75,69,230,.25);
  border-radius:12px;padding:10px 16px;
}}

/* ---------- table shell ---------- */
.tbl-scroll{{overflow-x:auto;border-radius:18px;border:1px solid var(--line);background:var(--card);box-shadow:0 10px 30px rgba(32,42,55,.05)}}
table.cmp{{border-collapse:separate;border-spacing:0;width:100%;min-width:860px;font-size:14px}}
table.cmp th,table.cmp td{{padding:12px 16px;border-bottom:1px solid var(--line);text-align:center}}
table.cmp td.feat{{text-align:right;font-weight:500;white-space:nowrap}}
thead th{{
  position:sticky;top:0;z-index:5;background:#fff;font-weight:800;font-size:13.5px;
}}
thead th.pl-name .sub{{display:block;font-weight:500;font-size:11.5px;color:var(--mut)}}
thead th.pro-hd{{background:#232945;color:#fff}}
thead th.pro-hd .sub{{color:rgba(255,255,255,.65)}}
tbody tr:last-child td{{border-bottom:none}}
tbody tr:hover td{{background:#fafaff}}

tr.grouph td{{
  background:linear-gradient(90deg,rgba(75,69,230,.10),rgba(124,92,252,.06));
  text-align:right;padding:9px 16px;font-weight:800;font-size:13.5px;color:#3730a3;
  border-bottom:1px solid rgba(75,69,230,.14);
}}
.gname{{display:flex;align-items:center;gap:8px}}
.gname::before{{content:"";width:8px;height:8px;border-radius:2px;background:var(--brand);transform:rotate(45deg);flex:none}}

/* plan columns highlight */
td.p-base{{background:#fbfbfe}}
td.p-std{{background:#f4f3ff}}
td.p-pro{{background:#efefff}}
tbody tr:hover td.p-base{{background:#f6f6fb}}
tbody tr:hover td.p-std{{background:#efedff}}
tbody tr:hover td.p-pro{{background:#e9e8ff}}

/* icons */
.chk{{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:8px}}
.chk .ico{{width:15px;height:15px}}
.chk.yes{{background:var(--green-bg);color:var(--green)}}
.chk.no{{background:var(--red-bg);color:var(--red)}}
.pill{{display:inline-block;font-size:11.5px;font-weight:700;padding:3px 11px;border-radius:999px;white-space:nowrap}}
.pill.inf{{background:var(--green-bg);color:var(--green)}}
.pill.sep{{background:#f0f0f6;color:var(--mut)}}
.pval b{{font-weight:800}}
.chip{{display:inline-block;font-size:11px;font-weight:600;padding:3px 10px;border-radius:999px;background:#f0f0f6;color:var(--mut);white-space:nowrap}}
.chip.sub{{background:#eef0ff;color:#4f46c5}}
b.price{{color:var(--brand);font-size:13.5px;white-space:nowrap}}
.muted{{color:var(--mut)}}
.muted.dash{{opacity:.55}}
.muted.small{{font-size:11.5px;white-space:nowrap}}
td.pl{{min-width:150px}}

/* plugins table */
table.plug{{border-collapse:separate;border-spacing:0;width:100%;font-size:14px}}
table.plug td{{padding:12px 16px;border-bottom:1px solid var(--line)}}
table.plug tr:last-child td{{border-bottom:none}}
table.plug td.feat{{font-weight:600}}
table.plug td.pl{{text-align:left;min-width:170px}}
table.plug b{{color:var(--brand)}}
.plug-wrap{{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}}
@media (max-width:860px){{ .plug-wrap{{grid-template-columns:1fr}} }}

/* non-standalone chips */
.ns-list{{list-style:none;display:flex;flex-wrap:wrap;gap:10px;margin:0;padding:0}}
.ns-list li{{
  background:#fff;border:1px solid var(--line);border-radius:999px;
  padding:8px 18px;font-size:13.5px;font-weight:600;color:var(--ink);
}}
.ns-list li::before{{content:"🚫";margin-inline-end:6px;font-size:12px}}

/* footer */
.foot{{margin:56px auto 80px;text-align:center;color:var(--mut);font-size:12.5px}}
.foot b{{color:var(--ink)}}

/* responsive */
@media (max-width:900px){{
  .plans{{grid-template-columns:1fr}}
  .pcard.hot{{order:-1}}
}}
</style>
</head>
<body>

<header class="phead">
  <span class="kicker">تعرفه و پلن‌ها</span>
  <h1>پلن‌های قیمت‌گذاری منوچ</h1>
  <p>اشتراک ماهانه + افزونه‌های ساختاری قابل خرید مستقل — پلن بالاتر یعنی Bundle اقتصادی‌تر همان افزونه‌ها.</p>
</header>

<div class="wrap">
  <section class="plans">
    {CARDS_HTML}
  </section>
  <p class="note">قیمت‌های بالا خروجی فعلی R&amp;D هستند و هنوز قیمت نهایی تجاری محسوب نمی‌شوند.</p>
</div>

<section class="wrap sec">
  <div class="sec-head">
    <h2>جدول کامل مقایسه پلن‌ها</h2>
    <p>ظرفیت‌ها (Limitها) قیمت مستقل ندارند؛ فقط فیچرهای ساختاری قابل خرید جداگانه‌اند.</p>
  </div>
  <div class="tbl-scroll">
    <table class="cmp">
      <thead>
        <tr>
          <th style="text-align:right">قابلیت</th>
          <th class="pl-name">پایه<span class="sub">۶۹۰٬۰۰۰ تومان</span></th>
          <th class="pl-name">استاندارد<span class="sub">۱٬۲۹۰٬۰۰۰ تومان</span></th>
          <th class="pl-name pro-hd">پرو<span class="sub">۲٬۴۹۰٬۰۰۰ تومان</span></th>
          <th>قیمت مستقل / ماه</th>
        </tr>
      </thead>
      <tbody>
{cmp_tbody}
      </tbody>
    </table>
  </div>
</section>

<section class="wrap sec">
  <div class="sec-head">
    <h2>افزونه‌های ساختاری قابل خرید مستقل</h2>
    <p>هر افزونه یک ماژول کامل است؛ Integrationهای زیرمجموعه‌اش جداگانه فروخته نمی‌شوند.</p>
  </div>
  <div class="plug-wrap">
    <div class="tbl-scroll">
      <table class="plug">
        <tbody>
{plug_trs}
        </tbody>
      </table>
    </div>
    <div>
      <div class="tbl-scroll">
        <table class="plug">
          <tbody>
            <tr><td class="feat">مشتری با نیاز ساده</td><td class="pl muted small">پلن پایین‌تر را انتخاب می‌کند</td></tr>
            <tr><td class="feat">مشتری با یک نیاز خاص</td><td class="pl muted small">همان افزونه را جدا می‌خرد</td></tr>
            <tr><td class="feat">مشتری با چند نیاز حرفه‌ای</td><td class="pl muted small">ارتقای پلن برایش اقتصادی‌تر است</td></tr>
          </tbody>
        </table>
      </div>
      <p class="note">اصل مدل: <b>Plan = پکیج اقتصادی قابلیت‌ها</b> ، <b>Plugin = امکان شخصی‌سازی پکیج</b></p>
    </div>
  </div>
</section>

<section class="wrap sec">
  <div class="sec-head">
    <h2>مواردی که افزونه مستقل نیستند</h2>
    <p>این موارد فقط برای تفکیک پلن‌ها هستند و قیمت جداگانه ندارند.</p>
  </div>
  <ul class="ns-list">
    {chips}
  </ul>
  <p class="note">نکته: «افزودن محصولات ارزی» فقط در پلن پرو فعال است و در وضعیت فعلی با خرید جداگانه روی پایه یا استاندارد فعال نمی‌شود.</p>
</section>

<footer class="wrap foot">
  این سند نتیجه جلسات R&amp;D قیمت‌گذاری منوچ است — <b>مدل پیشنهادی: اشتراک ماهانه + افزونه‌های ساختاری</b>
</footer>

</body>
</html>
"""

open('menuch-pricing.html', 'w', encoding='utf-8').write(page)
print("written menuch-pricing.html, length:", len(page))
print("comparison data rows:", len(data_rows))
print("plugin rows:", len(plug_trs))
print("group headers:", len(body_groups))
