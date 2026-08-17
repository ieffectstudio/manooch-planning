# -*- coding: utf-8 -*-
"""Build menuch-article.html — صفحه داخلی مقاله (سازگار با دیزاین‌سیستم منوچ)"""
import base64, json, re

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

# hero cover image (reuse b1) + related card images
blog_imgs = json.load(open('_blog_b64.json'))

# ---------------- template html ----------------
page = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>چرا وبسایت دردسر داره؟ — مقالات منوچ</title>
<style>
__FONT__
:root{
  --brand:#4B45E6; --ink:#202A37; --title:#3D4350; --body:#737377; --muted:#A2A2A5;
  --black:#16161D; --line:#E0E2E7; --paper:#FEFEFE; --soft:#FAFAFA;
  --lav:#ECEbfd; --lav-2:#ACA9F4; --banner:#BABDC1; --chip-black:#171E27; --muted-2:#A2A2A5;
  --radius:12px; --font:'Ravi','Estedad',Tahoma,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);color:var(--ink);background:var(--paper);line-height:1.9;direction:rtl}
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

/* ---------- بردکرامب ---------- */
.crumb{display:flex;align-items:center;gap:10px;margin:24px 0 4px;font-size:14px;color:var(--muted)}
.crumb a:hover{color:var(--brand)}
.crumb .on{color:var(--brand);font-weight:600}

/* ---------- مقاله ---------- */
.article{max-width:860px;margin:0 auto}
.ahead{margin-top:40px;text-align:right}
.ahead .tags{display:flex;gap:8px;flex-wrap:wrap}
.tag{display:inline-block;background:rgba(75,69,230,.1);color:var(--brand);font-size:12.5px;font-weight:700;padding:6px 14px;border-radius:8px}
.ahead h1{font-size:clamp(24px,3.4vw,38px);font-weight:800;color:var(--black);line-height:1.6;margin-top:16px}
.ahead .lede{font-size:clamp(15px,1.5vw,18px);color:var(--body);line-height:2.1;margin-top:12px}
.ameta{display:flex;align-items:center;gap:10px;margin-top:18px;font-size:13px;color:var(--muted);flex-wrap:wrap}
.ameta .vsep{width:1px;height:14px;background:var(--line);display:inline-block}
.ameta .read{display:inline-flex;align-items:center;gap:6px}
.cover{border-radius:20px;overflow:hidden;margin-top:28px;box-shadow:0 18px 44px rgba(32,42,55,.14)}
.cover img{width:100%;aspect-ratio:860/460;object-fit:cover}

.article__body{margin-top:34px;font-size:16px;color:var(--ink);line-height:2.2}
.article__body h2{font-size:22px;font-weight:700;color:var(--black);margin:36px 0 12px;line-height:1.6}
.article__body h3{font-size:18px;font-weight:700;color:var(--title);margin:28px 0 10px}
.article__body p{margin:12px 0}
.article__body ul,.article__body ol{margin:14px 0;padding-inline-start:22px}
.article__body li{margin:8px 0}
.article__body blockquote{background:rgba(75,69,230,.06);border-inline-start:4px solid var(--brand);border-radius:12px;padding:18px 22px;margin:22px 0;color:var(--title);font-size:15.5px;line-height:2.1}
.article__body .imgin{border-radius:16px;overflow:hidden;margin:22px 0}
.article__body .imgin img{width:100%}
.article__body .imgin span{display:block;text-align:center;font-size:12.5px;color:var(--muted);margin-top:8px}

/* اشتراک‌گذاری */
.share{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-top:44px;padding-top:22px;border-top:1px solid var(--line);flex-wrap:wrap}
.share .lbl{font-size:14px;font-weight:700;color:var(--title)}
.share .icons{display:flex;gap:8px}
.share a{width:40px;height:40px;border-radius:11px;background:var(--soft);border:1px solid var(--line);display:grid;place-items:center;color:var(--ink);transition:.15s}
.share a:hover{background:var(--brand);color:#fff;border-color:var(--brand)}
.share svg{width:18px;height:18px}

/* ---------- مقالات مرتبط ---------- */
.related{margin-top:96px}
.related .mn-sechead{text-align:center}
.related .mn-sechead h2{font-size:clamp(22px,2.6vw,30px);font-weight:700;color:var(--title)}
.related .mn-sechead p{font-size:14px;color:var(--body);margin-top:8px}
.rel-row{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:32px}
@media (max-width:900px){.rel-row{grid-template-columns:1fr}}

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

<div class="mn-banner">
  <div class="mn-wrap mn-banner__in">
    <span class="mn-banner__deal">پیشنهاد ویژه</span>
    <p class="mn-banner__text">فروشگاه آنلاینت رو با منوچ بساز؛ همین حالا با ۱۴ روز تست رایگان شروع کن</p>
    <span class="mn-banner__timer">فقط تا ۳۰ آذر</span>
  </div>
</div>

__NAV__

<main class="wrap">
  <nav class="crumb">
    <a href="menuch-landing.html">منوچ</a><span>/</span><a href="menuch-blog.html">مقالات</a><span>/</span><span class="on">چرا وبسایت دردسر داره؟</span>
  </nav>

  <article class="article">
    <header class="ahead">
      <div class="tags"><span class="tag">راهنمای فروش</span><span class="tag">فروشگاه آنلاین</span></div>
      <h1>چرا وبسایت دردسر داره؟</h1>
      <p class="lede">راه‌اندازی وبسایت نباید وقت و انرژی کسب‌وکارت رو بگیره. توی این مقاله با دردسرهای رایج سایت‌سازها آشنا می‌شی و می‌بینی منوچ چطور این مسیر رو برایت ساده می‌کنه.</p>
      <div class="ameta">
        <span>۱۲:۳۰</span><span class="vsep"></span><span>یکشنبه ۱۲ مرداد ۱۴۰۵</span><span class="vsep"></span>
        <span class="read"><svg class="mn-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>۶ دقیقه مطالعه</span>
      </div>
    </header>

    <div class="cover">
      <img src="data:image/webp;base64,__COVER__" alt="چرا وبسایت دردسر داره؟">
    </div>

    <div class="article__body">
      <p>خیلی از صاحبان کسب‌وکار وقتی تصمیم می‌گیرن وارد فروش آنلاین بشن، اولین مانعی که بهش می‌خورن خودِ «ساختن وبسایت»ه. انتخاب دامنه، خرید هاست، طراحی قالب، اتصال درگاه پرداخت و... هرکدوم می‌تونه هفته‌ها وقت بگیره.</p>

      <h2>دردسر اول: هزینه‌های پنهان</h2>
      <p>سایت‌سازهای سنتی معمولاً با یه قیمت پایه شروع می‌شن، اما برای هر قابلیت اضافه باید جدا پول بدی: قالب حرفه‌ای، افزونهٔ فروشگاهی، درگاه پرداخت، گواهی SSL و ده‌ها مورد دیگه.</p>
      <p>توی منوچ، همهٔ چیزهای ضروری از روز اول توی پلن پایه هست؛ از دامنهٔ اختصاصی و SSL گرفته تا درگاه پرداخت و مدیریت سفارش.</p>

      <h2>دردسر دوم: نیاز به دانش فنی</h2>
      <p>نصب و نگهداری سایت معمولاً به یه توسعه‌دهنده نیاز داره. هر تغییر کوچیک یعنی کلی رفت‌وبرگشت و هزینه. منوچ طوری طراحی شده که بدون حتی یک خط کد، فروشگاهت رو خودت بسازی و مدیریت کنی.</p>

      <blockquote>«فروشگاهم رو توی یک روز و بدون هیچ دانش فنی با منوچ راه انداختم؛ دیگه به برنامه‌نویس نیازی نداشتم.»</blockquote>

      <h2>دردسر سوم: سردرگمی در مدیریت</h2>
      <p>پنل‌های پیچیده با ده‌ها منو و تنظیمات گیج‌کننده، خودش یه دردسر جدیه. توی منوچ همه‌چیز ساده و دسته‌بندی‌شده است:</p>
      <ul>
        <li>مدیریت کالا و خدمات در چند کلیک</li>
        <li>ورود گروهی محصولات با فایل اکسل</li>
        <li>گزارش فروش شفاف و قابل‌فهم</li>
        <li>پشتیبانی واقعی از ۸ صبح تا ۱۰ شب</li>
      </ul>

      <h2>راه‌حل منوچ چیه؟</h2>
      <p>منوچ به‌جای اینکه تو رو با جزئیات فنی درگیر کنه، مسیر فروش رو برات ساده می‌کنه: فروشگاهت رو می‌سازی، محصولاتت رو اضافه می‌کنی و شروع به فروش می‌کنی. باقی ماجرا — از پرداخت تا ارسال و پیگیری سفارش — با منوچه.</p>
      <p>می‌تونی همین حالا با ۱۴ روز تست رایگان شروع کنی و خودت ببینی چقدر ساده‌ست.</p>
    </div>

    <div class="share">
      <span class="lbl">این مقاله رو به اشتراک بذار</span>
      <div class="icons">
        <a href="#" aria-label="کپی لینک"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14a4 4 0 0 0 4 0l3-3a4 4 0 0 0-6-6l-1.5 1.5"/><path d="M14 10a4 4 0 0 0-4 0l-3 3a4 4 0 0 0 6 6l1.5-1.5"/></svg></a>
        <a href="#" aria-label="تلگرام"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="m20.5 4.5-16 7 5.5 2 2.5 6 3-3.5 4 3.5 1-15Z"/></svg></a>
        <a href="#" aria-label="واتساپ"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3Z"/><path d="M8.7 9.2c.2-.5.7-.6 1-.3l1.2 1.4c.2.3.2.7-.1 1l-.8.8c.4 1 1.3 1.9 2.3 2.3l.8-.8c.3-.3.7-.3 1-.1l1.4 1.2c.3.3.2.8-.3 1-.9.6-2 .5-3-.1a8 8 0 0 1-4.5-4.5c-.6-1-.7-2.1-.1-3Z"/></svg></a>
      </div>
    </div>
  </article>

  <section class="related">
    <div class="mn-sechead"><h2>مقالات مرتبط</h2><p>این مقاله‌ها هم برای شروع فروش آنلاین بهت کمک می‌کنن</p></div>
    <div class="rel-row">
__REL__
    </div>
  </section>
</main>

__FOOTER__

</body>
</html>
"""

# ---------------- assets from menuch-blog.html ----------------
blog = open('menuch-blog.html', encoding='utf-8').read()

# navbar (adjust مقالات to accent)
nav_m = re.search(r'<header class="mn-nav">.*?</header>', blog, re.DOTALL)
nav_html = nav_m.group(0)

# footer (only the <footer> block, not trailing </body></html>)
fstart = blog.find('<footer class="mn-footer">')
fend = blog.find('</footer>', fstart) + len('</footer>')
footer_html = blog[fstart:fend]

# cover image (b1 already sized 384x256, but we want 860x460) -> regenerate bigger
from PIL import Image
import io as _io
im = Image.open('blog_b1.png').convert('RGB')
w,h = im.size
target = 860/460
cur = w/h
if cur > target:
    nw=int(h*target); x0=(w-nw)//2; im=im.crop((x0,0,x0+nw,h))
else:
    nh=int(w/target); y0=(h-nh)//2; im=im.crop((0,y0,w,y0+nh))
im = im.resize((860,460), Image.LANCZOS)
buf=_io.BytesIO(); im.save(buf,'WEBP',quality=84)
COVER = base64.b64encode(buf.getvalue()).decode()

# related cards (3 posts) using blog card markup style
def rel_card(img_key, t, d, tm, dt):
    return f'''<article class="mn-post">
      <img src="data:image/webp;base64,{blog_imgs[img_key]}" alt="{t}">
      <div class="mn-post__body">
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="mn-post__meta"><span>{tm}</span><span class="vsep"></span><span>{dt}</span></div>
        <a href="menuch-article.html" class="mn-post__btn">مشاهده مقاله</a>
      </div>
    </article>'''

REL = "\n".join([
    rel_card("b2", "سئو چقدر مهمه؟", "چطور با سئو مشتری بیشتری به فروشگاهت بیاری.", "۱۲:۳۰", "یکشنبه ۱۲ مرداد ۱۴۰۵"),
    rel_card("b3", "چرا سایت‌سازها؟", "مقایسه سایت‌سازها؛ کدوم برای کسب‌وکار تو بهتره.", "۱۲:۳۰", "یکشنبه ۱۲ مرداد ۱۴۰۵"),
    rel_card("b4", "فروش چجوری انجام می‌شه؟", "مسیر کامل فروش در منوچ؛ از سفارش تا تسویه.", "۱۲:۳۰", "یکشنبه ۱۲ مرداد ۱۴۰۵"),
])

# inject related card CSS (reuse mn-post styles from blog)
rel_css = """
/* کارت مقاله (از صفحه مقالات) */
.mn-post{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;transition:transform .18s ease,box-shadow .18s ease}
.mn-post:hover{transform:translateY(-4px);box-shadow:0 16px 36px rgba(32,42,55,.1)}
.mn-post>img{width:100%;aspect-ratio:240/183;object-fit:cover}
.mn-post__body{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.mn-post__body h3{font-size:16px;font-weight:600;color:var(--black)}
.mn-post__body>p{font-size:13px;color:var(--muted-2)}
.mn-post__meta{font-size:11px;color:var(--muted-2);display:flex;align-items:center;gap:6px}
.mn-post__meta .vsep{width:1px;height:12px;background:var(--line);display:inline-block}
.mn-post__btn{margin-top:auto;background:rgba(75,69,230,.2);color:var(--brand);text-align:center;font-size:13px;font-weight:400;padding:10px;border-radius:12px;display:inline-flex;align-items:center;justify-content:center;gap:6px;transition:all .15s ease}
.mn-post__btn:hover{background:var(--brand);color:#fff}
"""
page = page.replace('</style>', rel_css + '</style>')

page = page.replace('__FONT__', FONT_CSS)
page = page.replace('__NAV__', nav_html)
page = page.replace('__FOOTER__', footer_html)
page = page.replace('__COVER__', COVER)
page = page.replace('__REL__', REL)

open('menuch-article.html', 'w', encoding='utf-8').write(page)
print("written menuch-article.html, length:", len(page))
print("unresolved placeholders:", page.count('__'))
