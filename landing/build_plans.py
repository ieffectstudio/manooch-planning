# -*- coding: utf-8 -*-
"""Build menuch-plans.html — جدول مقایسه پلن‌ها (مثل صفحه تعرفه، بدون کارت‌های مجزا)"""
import base64, re

# ---------------- fonts ----------------
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

# ---------------- extracted pieces from pricing page ----------------
table_css = open('_table_css.txt', encoding='utf-8').read()
summ_html = open('_summ.html', encoding='utf-8').read()
cmp_html = open('_cmp.html', encoding='utf-8').read()
plug_html = open('_plug.html', encoding='utf-8').read()

# ---------------- assets from blog page ----------------
blog = open('menuch-blog.html', encoding='utf-8').read()
navblock = re.search(r'<div class="mn-banner">.*?</div>\n\n<header class="mn-nav">.*?</header>', blog, re.DOTALL).group(0)
navblock = navblock.replace('<a href="menuch-pricing.html" class="">تعرفه</a>', '<a href="menuch-plans.html" class="accent">تعرفه</a>')
navblock = navblock.replace('<a href="menuch-blog.html" class="accent">مقالات</a>', '<a href="menuch-blog.html" class="">مقالات</a>')

fstart = blog.find('<footer class="mn-footer">')
fend = blog.find('</footer>', fstart) + len('</footer>')
footer = blog[fstart:fend]

# ---------------- assemble ----------------
page = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>پلن‌های منوچ — مقایسه کامل تعرفه‌ها</title>
<style>
__FONT__
:root{
  --brand:#4B45E6; --ink:#202A37; --title:#3D4350; --body:#737377; --muted:#A2A2A5;
  --black:#16161D; --line:#E0E2E7; --paper:#FEFEFE; --soft:#FAFAFA; --card:#FFFFFF;
  --lav:#ECEbfd; --lav-2:#ACA9F4; --banner:#BABDC1; --chip-black:#171E27; --muted-2:#A2A2A5;
  --green:#12A15A; --green-bg:#EAF7F0; --red:#E5484D; --red-bg:#FDECEC; --amber:#B45309; --amber-bg:#FEF3C7;
  --radius:12px; --font:'Ravi','Estedad',Tahoma,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);color:var(--ink);background:var(--paper);line-height:1.8;direction:rtl}
a{text-decoration:none;color:inherit}
img{display:block;max-width:100%}
.wrap{max-width:1280px;margin-inline:auto;padding-inline:clamp(16px,2.5vw,40px)}
.mn-wrap { max-width: 1280px; margin-inline: auto; padding-inline: clamp(16px, 2.5vw, 40px); }
.mn-ico{width:22px;height:22px;flex:none;display:inline-block;vertical-align:middle}
.mn-ricon{display:inline-block;flex:none;line-height:0}
.mn-ricon img,.mn-ricon svg{width:100%!important;height:100%!important;display:block}

/* ---------- بنر ---------- */
.mn-banner{background:var(--banner);height:60px}
.mn-banner__in{height:60px;max-width:1100px;margin-inline:auto;padding-inline:16px;display:flex;align-items:center;justify-content:space-between;gap:20px}
.mn-banner__deal{position:relative;width:270px;height:52px;flex:none;display:grid;place-items:center}
.mn-banner__deal span{position:relative;color:var(--brand);font-size:clamp(16px,1.5vw,26px);font-weight:600;white-space:nowrap}
.mn-banner__text{font-size:clamp(13px,1.25vw,23px);font-weight:500;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mn-banner__timer{background:var(--chip-black);color:var(--soft);font-size:clamp(12px,1vw,17px);font-weight:600;padding:11px 20px;border-radius:8px;white-space:nowrap}
@media (max-width:560px){.mn-banner__in{justify-content:center}.mn-banner__deal{width:200px;height:40px}.mn-banner__timer{display:none}}

/* ---------- نوبار ---------- */
.mn-nav{position:sticky;top:0;z-index:1000;background:rgba(255,255,255,.72);-webkit-backdrop-filter:blur(14px) saturate(1.4);backdrop-filter:blur(14px) saturate(1.4);border-bottom:1px solid rgba(32,42,55,.06);box-shadow:0 6px 24px rgba(32,42,55,.05)}
.mn-nav__in{height:80px;display:flex;align-items:center;gap:clamp(16px,2vw,40px)}
.mn-nav__logo img{height:38px;width:93px}
.mn-nav__links{display:flex;align-items:center;gap:6px;margin-inline-start:clamp(28px,2.7vw,52px)}
.mn-nav__links a{display:inline-flex;align-items:center;gap:6px;font-size:16px;font-weight:400;color:var(--ink);white-space:nowrap;padding:12px 10px;border-radius:12px;transition:color .15s,background .15s}
.mn-nav__links a:hover{color:var(--brand)}
.mn-nav__links a.accent{color:var(--brand)}
.mn-nav__links a.accent .mn-ricon{width:24px;height:24px}
.mn-nav__links a .divider{width:1px;height:24px;background:var(--line);display:inline-block}
.mn-nav__actions{display:flex;align-items:center;gap:12px;margin-inline-start:auto}
.mn-trust{display:inline-flex;align-items:center;gap:10px;background:rgba(75,69,230,.1);color:var(--brand);font-size:16px;padding:12px 18px;border-radius:12px;white-space:nowrap}
.mn-trust .mn-ricon{width:24px;height:24px}
.mn-btn-dark{display:inline-flex;align-items:center;gap:10px;background:var(--ink);color:var(--soft);font-size:16px;font-weight:400;font-family:var(--font);height:48px;padding-inline:24px;border-radius:12px;border:none;cursor:pointer;white-space:nowrap;transition:transform .15s ease}
.mn-btn-dark:hover{transform:translateY(-2px)}
.mn-btn-dark .mn-ricon{width:24px;height:24px}
@media (max-width:1200px){.mn-nav__links{margin-inline-start:16px}}
@media (max-width:900px){.mn-nav__links{display:none}.mn-nav__in{height:68px;justify-content:space-between}}
@media (max-width:560px){.mn-trust{display:none}}

/* ---------- هدر ---------- */
.phead{text-align:center;padding:64px 20px 8px}
.kicker{display:inline-block;background:rgba(75,69,230,.08);color:var(--brand);border:1px solid rgba(75,69,230,.22);font-size:13.5px;font-weight:700;padding:7px 16px;border-radius:999px;margin-bottom:16px}
.phead h1{font-size:clamp(28px,4vw,44px);font-weight:800;line-height:1.4}
.phead p{color:var(--body);font-size:clamp(14.5px,1.4vw,17px);max-width:640px;margin:12px auto 0}

/* ---------- تب دوره ---------- */
.tabs{display:flex;justify-content:center;gap:6px;margin:32px auto 8px}
.tabs button{border:1px solid var(--line);background:#fff;color:var(--title);font-family:var(--font);font-size:15px;font-weight:600;padding:11px 26px;border-radius:12px;cursor:pointer;transition:.15s}
.tabs button.on{background:var(--brand);color:#fff;border-color:var(--brand)}

/* ---------- سکشن‌ها ---------- */
.sec{margin-top:96px}
.sechead{text-align:center}
.sechead h2{font-size:clamp(24px,2.6vw,32px);font-weight:700;color:var(--title)}
.sechead p{font-size:14.5px;color:var(--body);margin-top:10px;max-width:620px;margin-inline:auto}
.note{margin:16px auto 0;max-width:760px;font-size:12.5px;color:var(--muted);background:rgba(75,69,230,.05);border:1px dashed rgba(75,69,230,.25);border-radius:12px;padding:10px 16px;text-align:center}

/* ---------- فوتر ---------- */
.mn-footer{margin-top:96px;padding:0 34px 32px}
.mn-footer__card{background:var(--ink);border-radius:29px;max-width:1852px;min-height:496px;margin-inline:auto}
.mn-footer__in{max-width:1596px;margin-inline:auto;padding:61px clamp(20px,3vw,48px) 0;display:grid;grid-template-columns:1.3fr 1fr 1fr .7fr;gap:clamp(24px,3vw,56px);color:#fff}
.mn-footer__logo{height:48px;width:auto}
.mn-footer__contact{margin-top:22px;display:flex;flex-direction:column;gap:12px;font-size:16px}
.mn-footer__contact div{display:flex;align-items:center;gap:8px}
.mn-footer__contact .mn-ico{width:20px;height:20px;opacity:.85}
.mn-footer__contact b{font-weight:400}
.mn-footer__contact span{color:var(--lav-2);direction:ltr;font-size:14.5px}
.mn-footer__contact a{color:inherit}
.mn-footer__socials{display:flex;gap:10px;margin-top:24px}
.mn-footer__socials a{width:42px;height:42px;border-radius:11px;background:rgba(255,255,255,.09);display:grid;place-items:center;color:#fff;transition:background .15s ease,transform .15s ease}
.mn-footer__socials a:hover{background:var(--brand);transform:translateY(-3px)}
.mn-footer__socials .mn-ico{width:19px;height:19px}
.mn-footer__col h4{font-size:16px;font-weight:400;color:var(--soft);margin-bottom:18px}
.mn-footer__col ul{display:flex;flex-direction:column;gap:13px;list-style:none}
.mn-footer__col a{color:rgba(255,255,255,.88);font-size:15px;transition:color .15s ease}
.mn-footer__col a:hover{color:var(--lav-2)}
.mn-footer__badges{display:flex;gap:12px}
.mn-footer__badges img{width:82px;height:89px;object-fit:contain}
.mn-footer__bar{max-width:1596px;margin:36px auto 0;border-top:1px solid rgba(172,169,244,.35);padding:22px clamp(20px,3vw,48px) 28px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:rgba(255,255,255,.78);font-size:14.5px}
@media (max-width:1100px){.mn-footer__in{grid-template-columns:1fr 1fr}}
@media (max-width:720px){.mn-footer__in{grid-template-columns:1fr;text-align:center}.mn-footer__contact div,.mn-footer__socials{justify-content:center}.mn-footer__logo{margin-inline:auto}.mn-footer__badges{justify-content:center}}
</style>
</head>
<body>

__NAVBLOCK__

<header class="phead">
  <span class="kicker">تعرفه و پلن‌ها</span>
  <h1>پلن‌های منوچ</h1>
  <p>اشتراک ماهانه، سه‌ماهه و شش‌ماهه + افزونه‌های ساختاری قابل خرید مستقل — پلن بالاتر یعنی باندل اقتصادی‌تر همان ماژول‌ها.</p>
</header>

<div class="wrap">
  <div class="tabs" role="tablist">
    <button type="button" data-period="m" class="on">ماهانه</button>
    <button type="button" data-period="q3">سه ماهه</button>
    <button type="button" data-period="q6">شش ماهه</button>
  </div>
</div>

<section class="wrap sec">
  <div class="sechead">
    <h2>نمای کلی پلن‌ها</h2>
    <p>خلاصه قابلیت‌های اصلی در هر پلن؛ جزئیات کامل در جدول پایین.</p>
  </div>
  <div class="tbl" style="margin-top:28px">
    __SUMM__
  </div>
</section>

<section class="wrap sec">
  <div class="sechead">
    <h2>جزئیات ماژول‌ها و قابلیت‌ها</h2>
    <p>ظرفیت‌ها (Limitها) قیمت مستقل ندارند؛ فقط فیچرهای ساختاری قابل خرید جداگانه‌اند.</p>
  </div>
  <div class="tbl" style="margin-top:28px">
    __CMP__
  </div>
  <p class="note">قیمت پلن‌ها در هر سه دوره (ماهانه، سه‌ماهه و شش‌ماهه) نهایی شده و مبنای فعلی قیمت‌گذاری منوچ هستند.</p>
</section>

<section class="wrap sec">
  <div class="sechead">
    <h2>افزونه‌های ساختاری قابل خرید مستقل</h2>
    <p>هر افزونه یک ماژول کامل است؛ Integrationهای زیرمجموعه‌اش جداگانه فروخته نمی‌شوند.</p>
  </div>
  <div class="tbl" style="margin-top:28px">
    __PLUG__
  </div>
</section>

__FOOTER__

<script>
(function () {
  var tabs = document.querySelectorAll('.tabs button');
  var priceRows = document.querySelectorAll('.summ td.c');
  tabs.forEach(function (btn) {
    btn.addEventListener('click', function () {
      tabs.forEach(function (b) { b.classList.remove('on'); });
      btn.classList.add('on');
    });
  });
})();
</script>
</body>
</html>
"""

# inject the table CSS before the closing style
page = page.replace('</style>', table_css + '</style>')

page = page.replace('__FONT__', FONT_CSS)
page = page.replace('__NAVBLOCK__', navblock)
page = page.replace('__FOOTER__', footer)
page = page.replace('__SUMM__', summ_html)
page = page.replace('__CMP__', cmp_html)
page = page.replace('__PLUG__', plug_html)

open('menuch-plans.html', 'w', encoding='utf-8').write(page)
print("written menuch-plans.html, length:", len(page))
print("unresolved:", page.count('__NAVBLOCK__')+page.count('__FOOTER__')+page.count('__SUMM__')+page.count('__CMP__')+page.count('__PLUG__')+page.count('__FONT__'))
