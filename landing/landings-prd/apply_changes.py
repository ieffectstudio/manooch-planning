# -*- coding: utf-8 -*-
import re

h = open('menuch-landing.html', encoding='utf-8').read()

# ============================================================
# 1) Reduce all font weights (skip @font-face lines)
# ============================================================
style_open = h.find('<style>')
style_close = h.find('</style>')
assert style_open != -1 and style_close != -1
head_style = h[style_open:style_close]
body_after_style = h[style_close:]

W = {900: 600, 800: 600, 700: 500, 600: 400, 500: 400}

def mapw(m):
    n = int(m.group(2))
    return m.group(1) + str(W.get(n, n))   # preserve original spacing

css_inner = head_style[len('<style>'):]
lines = css_inner.split('\n')
out = []
mapped = 0
for ln in lines:
    if '@font-face' in ln:
        out.append(ln); continue
    new, cnt = re.subn(r'(font-weight:\s*)(\d{3})', mapw, ln)
    mapped += cnt
    out.append(new)
new_css = '\n'.join(out)
new_css += "\n\n/* کاهش وزن کلی متن‌های بولد */\nb, strong { font-weight: 500; }\n"
head_style = '<style>' + new_css
body_after_style, cnt2 = re.subn(r'(font-weight:\s*)(\d{3})', mapw, body_after_style)
h = head_style + body_after_style
print("weights mapped in style:", mapped, "| inline:", cnt2)

# ============================================================
# 2) Smaller hero stats (match post-mapping block: 800->600)
# ============================================================
old_stats = """.mn-hero__stats {
  margin-top: 26px;
  display: flex; align-items: stretch; justify-content: center; flex-wrap: wrap;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.14);
  border-radius: 18px;
  padding: 18px 6px;
  -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
}
.mn-stat {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 5px; padding: 2px 28px; min-width: 168px;
  border-inline-start: 1px solid rgba(255,255,255,.14);
}
.mn-stat:first-child { border-inline-start: none; }
.mn-stat strong {
  font-size: clamp(19px, 2vw, 25px); font-weight: 600; color: #fff; line-height: 1.4; white-space: nowrap;
}
.mn-stat span { font-size: clamp(12px, 1.15vw, 14px); color: rgba(219, 216, 255, .85); white-space: nowrap; }
@media (max-width: 760px) {
  .mn-stat { min-width: 46%; border-inline-start: none; padding: 10px 8px; }
  .mn-hero__stats { gap: 6px; padding: 14px 6px; }
}"""
new_stats = """.mn-hero__stats {
  margin-top: 20px;
  display: flex; align-items: stretch; justify-content: center; flex-wrap: wrap;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.14);
  border-radius: 14px;
  padding: 10px 4px;
  -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px);
}
.mn-stat {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 2px; padding: 2px 16px; min-width: 118px;
  border-inline-start: 1px solid rgba(255,255,255,.14);
}
.mn-stat:first-child { border-inline-start: none; }
.mn-stat strong {
  font-size: clamp(14px, 1.4vw, 17px); font-weight: 500; color: #fff; line-height: 1.4; white-space: nowrap;
}
.mn-stat span { font-size: clamp(10.5px, .95vw, 12px); color: rgba(219, 216, 255, .85); white-space: nowrap; }
@media (max-width: 760px) {
  .mn-stat { min-width: 46%; border-inline-start: none; padding: 6px 6px; }
  .mn-hero__stats { gap: 4px; padding: 10px 4px; }
}"""
assert h.count(old_stats) == 1, f"stats css found {h.count(old_stats)}"
h = h.replace(old_stats, new_stats)

# ============================================================
# 3) Custom plans (R&D): base / standard / pro
# ============================================================
h = h.replace(
    ".mn-plan {\n  background: #fefefe; border: 1px solid var(--line); border-radius: var(--radius);\n  min-height: 1058px;",
    ".mn-plan {\n  background: #fefefe; border: 1px solid var(--line); border-radius: var(--radius);\n  min-height: 640px;")
h = h.replace(
    ".mn-plan__price b { font-size: 29px; font-weight: 600; color: var(--brand); }",
    ".mn-plan__price b { font-size: clamp(20px, 2vw, 27px); font-weight: 600; color: var(--brand); }")

anchor = """.mn-plan__group-label::before {
  content: \"\"; display: inline-block; width: 7px; height: 7px; border-radius: 2px;
  background: var(--brand); margin-inline-end: 8px; vertical-align: 1px; opacity: .85;
}"""
add_css = anchor + """

/* ---------- پلن پیشنهادی (کاستوم) ---------- */
.mn-plan--hot { position: relative; border: 2px solid var(--brand); box-shadow: 0 18px 44px rgba(75, 69, 230, .16); }
.mn-plan__badge {
  position: absolute; top: -15px; inset-inline: 0; margin-inline: auto; width: max-content;
  background: var(--brand); color: #fff; font-size: 12.5px; font-weight: 500;
  padding: 6px 20px; border-radius: 999px; white-space: nowrap; letter-spacing: .2px;
}
.mn-plans__note { text-align: center; color: var(--muted); font-size: 12.5px; margin-top: 20px; }"""
assert h.count(anchor) == 1, f"anchor found {h.count(anchor)}"
h = h.replace(anchor, add_css)

CHECK = '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path opacity="0.4" d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" fill="#4B45E6"/>
<path d="M10.58 15.5801C10.38 15.5801 10.19 15.5001 10.05 15.3601L7.22 12.5301C6.93 12.2401 6.93 11.7601 7.22 11.4701C7.51 11.1801 7.99 11.1801 8.28 11.4701L10.58 13.7701L15.72 8.6301C16.01 8.3401 16.49 8.3401 16.78 8.6301C17.07 8.9201 17.07 9.4001 16.78 9.6901L11.11 15.3601C10.97 15.5001 10.78 15.5801 10.58 15.5801Z" fill="#4B45E6"/>
</svg>'''
NO = '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path opacity="0.4" d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" fill="#EB0000"/>
<path d="M13.06 12.0001L15.36 9.70011C15.65 9.41011 15.65 8.93011 15.36 8.64011C15.07 8.35011 14.59 8.35011 14.3 8.64011L12 10.9401L9.69998 8.64011C9.40998 8.35011 8.92999 8.35011 8.63999 8.64011C8.34999 8.93011 8.34999 9.41011 8.63999 9.70011L10.94 12.0001L8.63999 14.3001C8.34999 14.5901 8.34999 15.0701 8.63999 15.3601C8.78999 15.5101 8.97999 15.5801 9.16999 15.5801C9.35999 15.5801 9.54998 15.5101 9.69998 15.3601L12 13.0601L14.3 15.3601C14.45 15.5101 14.64 15.5801 14.83 15.5801C15.02 15.5801 15.21 15.5101 15.36 15.3601C15.65 15.0701 15.65 14.5901 15.36 14.3001L13.06 12.0001Z" fill="#EB0000"/>
</svg>'''

def item(txt, ok=True):
    ic = CHECK if ok else NO
    cls = ' mn-plan__item--no' if not ok else ''
    return f'<div class="mn-plan__item{cls}"><span class="mn-ricon" style="width:22px;height:22px">{ic}</span><span class="txt">{txt}</span></div>'

def group(label, items):
    return (f'<div class="mn-plan__group"><span class="mn-plan__group-label">{label}</span>'
            + ''.join(item(t, ok) for t, ok in items) + '</div>')

def card(name, desc, price, groups, hot=False, badge=None):
    badge_html = f'<span class="mn-plan__badge">{badge}</span>' if badge else ''
    cls = ' mn-plan--hot' if hot else ''
    gh = ''.join(group(g[0], g[1]) for g in groups)
    return (f'<article class="mn-plan{cls}">{badge_html}'
            f'<h3 class="mn-plan__name">{name}</h3>'
            f'<p class="mn-plan__desc">{desc}</p>'
            f'<div class="mn-plan__price"><b>{price}</b><span>تومان</span><em>ماهانه</em></div>'
            f'<div class="mn-plan__list">{gh}</div>'
            f'<button class="mn-plan__cta" type="button">شروع با {name}</button>'
            f'</article>')

base = card("پلن پایه", "شروع فروش آنلاین", "۶۹۰٬۰۰۰", [
    ("فروشگاه و محصول", [
        ("۱۰۰ محصول فعال", 1), ("۲ عکس برای هر محصول", 1),
        ("افزودن کالا و خدمات", 1), ("دسته‌بندی و زیردسته", 1),
        ("ویژگی محصول (رنگ، سایز، مشخصات)", 1), ("دامنه اختصاصی + SSL", 1),
        ("ویس محصول", 0)]),
    ("فروش و سفارش", [
        ("سبد خرید و مدیریت سفارش", 1),
        ("درگاه پرداخت (زرین‌پال، زیبال، بانکی)", 1),
        ("پرداخت در محل + آپلود فیش", 1),
        ("روش و هزینه ارسال", 1),
        ("دفترچه مشتریان و تاریخچه خرید", 1)]),
    ("رشد و اتوماسیون", [
        ("واحد فروش پیشرفته", 0), ("فروش اقساطی", 0), ("باشگاه مشتریان", 0)]),
])

std = card("پلن استاندارد", "مدیریت حرفه‌ای فروش", "۱٬۲۹۰٬۰۰۰", [
    ("همه امکانات پایه، به‌علاوه", [
        ("۱٬۰۰۰ محصول فعال", 1), ("۳ عکس برای هر محصول + ویس محصول", 1),
        ("واحد فروش پیشرفته", 1), ("ورود اطلاعات با اکسل (Import / Export)", 1),
        ("لینک پرداخت + پرداخت توافقی", 1), ("فروش حضوری", 1)]),
    ("بازاریابی و گزارش", [
        ("تخفیف‌ها، نظرات و اعلان‌ها", 1), ("گزارش فروش کامل", 1),
        ("Social Marketing (تلگرام، بله و ...)", 1), ("اتصال حسابداری", 1)]),
    ("در پلن پرو", [
        ("محصولات ارزی", 0), ("فروش اقساطی", 0), ("باشگاه مشتریان", 0)]),
], hot=True, badge="پیشنهاد منوچ")

pro = card("پلن پرو", "رشد، اتوماسیون و وفادارسازی", "۲٬۴۹۰٬۰۰۰", [
    ("همه امکانات استاندارد، به‌علاوه", [
        ("محصولات نامحدود + ۵ عکس", 1), ("محصولات ارزی", 1),
        ("فروش اقساطی (اسنپ‌پی، ترب‌پی، دیجی‌پی)", 1)]),
    ("باشگاه مشتریان کامل", [
        ("امتیاز، سطح‌بندی و کمپین", 1),
        ("SMS Marketing و پیامک گروهی", 1),
        ("گزارش باشگاه", 1)]),
    ("اتوماسیون و وفادارسازی", [
        ("همه افزونه‌ها بدون هزینه جداگانه", 1),
        ("گزارش پیشرفته فروش", 1)]),
])

new_section = f'''    <section class="mn-plans mn-section" id="plans">
      <div class="mn-wrap">
        <div class="mn-sechead"><h2>پلن های منوچ</h2><p>اشتراک ماهانه + افزونه‌های ساختاری مستقل — پلن بالاتر یعنی باندل اقتصادی‌تر همان افزونه‌ها</p></div>
        <div class="mn-plans__row">{base}{std}{pro}</div>
        <p class="mn-plans__note">قیمت‌ها خروجی فعلی R&amp;D هستند و هنوز قیمت نهایی تجاری محسوب نمی‌شوند.</p>
      </div>
    </section>'''

start = h.find('<section class="mn-plans mn-section" id="plans">')
end = h.find('</section>', start) + len('</section>')
assert start != -1 and end > start
h = h[:start] + new_section + h[end:]

open('menuch-landing.html', 'w', encoding='utf-8').write(h)
print("plans replaced. new length:", len(h))
print("hot card:", h.count('mn-plan--hot'), "| badge:", h.count('mn-plan__badge'), "| note:", h.count('mn-plans__note'))
print("old prices still present:", any(x in h for x in ["۲۶۹","۴۴۹","۹۸۰"]))
print("toggle present:", 'mn-toggle' in h)
