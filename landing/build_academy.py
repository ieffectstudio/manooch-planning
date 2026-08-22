# -*- coding: utf-8 -*-
"""Build menuch-academy.html — مطابق دیزاین فیگما (node 1043:13565)"""
import base64

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

FEATURED = {
    "title": "آموزش افزودن کالا",
    "desc": "توی این ویدئو قدم‌به‌قدم یاد می‌گیری چطور کالا، خدمات و ویژگی‌های محصول رو به فروشگاهت اضافه کنی.",
    "date": "۲۴ اردیبهشت ۱۴۰۵",
    "time": "۱۲:۳۰",
    "tag": "افزونه",
    "count": "5",
    "overlay": "آموزش افزودن کالا",
}

VIDEOS = [
    ("راه‌اندازی فروشگاه در ۱۰ دقیقه", "از ثبت‌نام تا آنلاین‌شدن فروشگاهت؛ قدم‌به‌قدم و بدون دانش فنی.", "۲۴ اردیبهشت ۱۴۰۵", "۱۲:۳۰", "شروع کار"),
    ("ورود گروهی محصولات با اکسل", "ورود کالا، قیمت و موجودی با فایل اکسل در چند دقیقه.", "۱۰ خرداد ۱۴۰۵", "۱۵:۰۰", "افزونه"),
    ("مدیریت انبار و هشدار موجودی", "مدیریت موجودی، هشدار کمبود و Export اطلاعات.", "۵ تیر ۱۴۰۵", "۱۱:۰۰", "افزونه"),
    ("اتصال درگاه پرداخت و تسویه", "زرین‌پال، زیبال و کارت‌به‌کارت؛ تسویه سریع بدون واسطه.", "۲۰ مرداد ۱۴۰۵", "۱۸:۳۰", "کارگاه"),
    ("فروش اقساطی با اسنپ‌پی و ترب‌پی", "فعال‌سازی فروش اعتباری و دریافت نقدی مبلغ.", "۱۵ شهریور ۱۴۰۵", "۱۴:۰۰", "دوره آنلاین"),
    ("Social Marketing و انتشار خودکار", "انتشار محصول در تلگرام، بله و سایر کانال‌ها به‌صورت زمان‌بندی‌شده.", "۳۰ مهر ۱۴۰۵", "۱۰:۰۰", "وبینار"),
    ("اتصال حسابداری و همگام‌سازی", "Sync کالا و موجودی با نرم‌افزارهای حسابداری.", "۱۵ آبان ۱۴۰۵", "۱۴:۰۰", "کارگاه تخصصی"),
    ("باشگاه مشتریان و کمپین", "امتیاز، سطح‌بندی، SMS Marketing و گزارش باشگاه.", "۲۰ آذر ۱۴۰۵", "۱۶:۰۰", "دوره آموزشی"),
    ("گزارش فروش و تحلیل درآمد", "درآمد، محصولات پرفروش و مشتریان برتر رو تحلیل کن.", "۵ دی ۱۴۰۵", "۱۱:۰۰", "سمینار"),
]

THUMB_GRADS = [
    "linear-gradient(135deg,#4B45E6,#7C5CFC)",
    "linear-gradient(135deg,#0EA5E9,#22D3EE)",
    "linear-gradient(135deg,#10B981,#34D399)",
    "linear-gradient(135deg,#8B5CF6,#A78BFA)",
    "linear-gradient(135deg,#F59E0B,#FBBF24)",
    "linear-gradient(135deg,#EC4899,#F472B6)",
    "linear-gradient(135deg,#0EA5E9,#38BDF8)",
    "linear-gradient(135deg,#8B5CF6,#C084FC)",
    "linear-gradient(135deg,#10B981,#4ADE80)",
]

def play_icon(size=22):
    return f'<svg viewBox="0 0 24 24" fill="currentColor" style="width:{size}px;height:{size}px"><path d="M8 5.5v13l11-6.5-11-6.5Z"/></svg>'

def tag_badge(tag, count="5"):
    return (f'<span class="tag">'
            f'<span class="tag-x"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></span>'
            f'<span class="tag-n">{count}</span>'
            f'<span class="tag-t">{tag}</span>'
            f'</span>')

rows = []
for i, (title, desc, date, time, tag) in enumerate(VIDEOS):
    rows.append(f'''<article class="vrow">
      <div class="vthumb" style="background:{THUMB_GRADS[i]}">
        <span class="vplay">{play_icon(18)}</span>
      </div>
      <div class="vinfo">
        <h3>{title}</h3>
        <p>{desc}</p>
        <div class="vmeta">
          {tag_badge(tag)}
          <span class="vdt"><span>{date}</span><span class="sep">/</span><span>{time}</span></span>
        </div>
      </div>
    </article>''')
ROWS = "\n".join(rows)

POSTS = [
    ("چرا وبسایت دردسر داره؟", "آشنایی با دردسرهای رایج سایت‌سازها و راه‌حل منوچ"),
    ("سئو چقدر مهمه؟", "چطور با سئو مشتری بیشتری به فروشگاهت بیاری"),
    ("چرا سایت‌سازها؟", "مقایسه سایت‌سازها؛ کدوم برای کسب‌وکار تو بهتره"),
    ("فروش چجوری انجام می‌شه؟", "مسیر کامل فروش در منوچ؛ از سفارش تا تسویه"),
]
post_cards = "\n".join(
    f'''<article class="post">
      <div class="thumb" style="background:{g}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 9h6M9 13h6M9 17h4"/></svg></div>
      <div class="body">
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="meta"><span>۱۲:۳۰</span><span> | </span><span>یکشنبه ۱۲ مرداد ۱۴۰۵</span></div>
        <a class="more" href="#">مشاهده مقاله</a>
      </div>
    </article>'''
    for (t, d), g in zip(POSTS, ["linear-gradient(135deg,#EDE9FE,#DDD6FE)","linear-gradient(135deg,#DBEAFE,#BFDBFE)","linear-gradient(135deg,#FEF3C7,#FDE68A)","linear-gradient(135deg,#FCE7F3,#FBCFE8)"])
)

FAQS = [
    ("منوچ چطور به فروش بیشترم کمک می‌کنه؟", "منوچ مثل یه دستیار فروش همیشه‌بیدار کنار شماست؛ محصولاتتون رو معرفی می‌کنه، با مشتری گفت‌وگو می‌کنه و فروش رو تا انتها پیگیری می‌کنه.", True),
    ("راه‌اندازی فروشگاه چقدر زمان می‌بره؟", "با چند کلیک و در کمتر از یک روز فروشگاهت آنلاین می‌شه؛ حتی بدون دانش فنی.", False),
    ("پلن‌ها و قیمت‌ها چطوریه؟", "سه پلن با دوره‌های ماهانه، سه‌ماهه و شش‌ماهه داریم؛ ۱۴ روز تست رایگان و افزونه‌هایی که می‌تونی جداگانه بخری.", False),
    ("اگه به مشکل خوردم چیکار کنم؟", "تیم پشتیبانی از ۸ صبح تا ۱۰ شب همراهته و از طریق تیکت پاسخگوت هستیم.", False),
]
faq_rows = "\n".join(
    f'<details class="faq__row"{" open" if o else ""}><summary><h3>{q}</h3><span class="chev">‹</span></summary><p class="ans">{a}</p></details>'
    for q, a, o in FAQS
)

page = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>آکادمی منوچ — آموزش‌های قدم‌به‌قدم</title>
<style>
__FONT__
:root{
  --brand:#4B45E6; --ink:#202A37; --title:#3D4350; --body:#737377; --muted:#A2A2A5;
  --black:#16161D; --line:#E0E2E7; --paper:#FEFEFE; --soft:#FAFAFA;
  --radius:12px; --font:'Ravi','Estedad',Tahoma,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);color:var(--ink);background:var(--paper);line-height:1.8;direction:rtl}
a{text-decoration:none;color:inherit}
img{display:block;max-width:100%}
.wrap{max-width:1280px;margin-inline:auto;padding-inline:20px}

/* ---------- banner ---------- */
.banner{background:var(--ink);color:#fff;font-size:14px;padding:12px 0}
.banner__in{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap}
.banner__deal{font-size:19px;font-weight:900;color:var(--brand)}
.banner__timer{background:#FAFAFA;color:var(--ink);font-weight:900;border-radius:999px;padding:4px 16px;font-size:13px}

/* ---------- navbar ---------- */
.nav{position:sticky;top:0;z-index:1000;background:rgba(255,255,255,.72);
  -webkit-backdrop-filter:blur(14px) saturate(1.4);backdrop-filter:blur(14px) saturate(1.4);
  border-bottom:1px solid rgba(32,42,55,.06);box-shadow:0 6px 24px rgba(32,42,55,.05)}
.nav__in{height:76px;display:flex;align-items:center;gap:20px}
.nav__logo{font-weight:900;font-size:20px;color:var(--ink)}
.nav__links{display:flex;align-items:center;gap:2px;margin-inline-start:6px}
.nav__links a{font-size:14.5px;color:var(--ink);padding:9px 11px;border-radius:10px;transition:.15s}
.nav__links a:hover{color:var(--brand)}
.nav__links a.on{color:var(--brand);font-weight:700}
.nav__actions{margin-inline-start:auto;display:flex;align-items:center;gap:14px}
.nav__trust{font-size:14px;color:var(--brand);font-weight:700}
.nav__cta{background:var(--ink);color:#FBFBFB;font-size:14px;font-weight:400;padding:11px 22px;border-radius:12px;transition:.15s}
.nav__cta:hover{background:var(--brand)}

/* ---------- breadcrumb ---------- */
.crumb{display:flex;align-items:center;gap:10px;margin:24px 0 4px;font-size:14px;color:var(--muted)}
.crumb .on{color:var(--brand)}

/* ---------- featured: player RIGHT, text LEFT ---------- */
.featured{display:grid;grid-template-columns:1.57fr 1fr;gap:24px;align-items:center;margin-top:6px}
@media (max-width:980px){.featured{grid-template-columns:1fr}}
.player{position:relative;border-radius:16px;overflow:hidden;aspect-ratio:768/410;
  background:linear-gradient(135deg,#33343C,#0E0E12)}
.player .pl-img{position:absolute;inset:0;background:
  radial-gradient(60% 60% at 80% 20%, rgba(139,92,246,.5), transparent 60%),
  linear-gradient(150deg,#232945,#2f2a63 55%,#3b34a8)}
.player .play{position:absolute;inset:0;margin:auto;width:72px;height:72px;border-radius:50%;
  background:rgba(255,255,255,.18);border:1.5px solid rgba(255,255,255,.55);display:grid;place-items:center;color:#fff;
  -webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);transition:.18s}
.player .play:hover{transform:scale(1.08)}
.player .pl-info{position:absolute;bottom:16px;inset-inline:16px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.player .pl-title{color:#fff;font-size:22px;font-weight:700;text-shadow:0 2px 10px rgba(0,0,0,.6)}

.finfo h1{font-size:23px;font-weight:700;color:var(--title);line-height:1.6;margin-top:16px}
.finfo p{font-size:16px;color:var(--body);margin-top:10px;line-height:2}
.fmeta{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:20px;font-size:13px;color:var(--body)}
.fmeta .vdt{display:inline-flex;align-items:center;gap:8px}
.fmeta .sep{color:var(--line)}

/* ---------- tag badge ---------- */
.tag{display:inline-flex;align-items:center;gap:4px;background:var(--soft);border:1px solid var(--line);
  border-radius:999px;padding:4px 6px 4px 4px;font-size:11px;color:var(--title);white-space:nowrap}
.tag-x{width:20px;height:20px;border-radius:50%;background:#fff;border:1px solid var(--line);display:grid;place-items:center;color:var(--title)}
.tag-x svg{width:8px;height:8px}
.tag-n{background:#fff;border:1px solid var(--line);border-radius:999px;padding:0 7px;font-size:11px;line-height:17px}
.tag-t{font-weight:600}

/* ---------- content: videos RIGHT, sidebar LEFT ---------- */
.content{display:grid;grid-template-columns:1fr 367px;gap:20px;margin-top:26px;align-items:start}
@media (max-width:980px){.content{grid-template-columns:1fr}}
.videos{display:flex;flex-direction:column;gap:16px}
.videos__head{display:flex;align-items:baseline;justify-content:space-between;gap:12px}
.videos__head h2{font-size:19px;font-weight:700;color:var(--title)}
.videos__head span{font-size:14px;color:var(--body)}

.vrow{display:flex;align-items:stretch;gap:16px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px}
.vthumb{flex:none;width:240px;min-height:136px;border-radius:6px;position:relative;display:grid;place-items:center}
.vplay{width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.22);border:1.5px solid rgba(255,255,255,.6);
  display:grid;place-items:center;color:#fff;-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)}
.vinfo{flex:1;display:flex;flex-direction:column;min-width:0}
.vinfo h3{font-size:19px;font-weight:700;color:var(--title);line-height:1.6;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.vinfo p{font-size:14px;color:var(--body);margin-top:4px;line-height:1.8;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.vmeta{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:auto;padding-top:8px;font-size:13px;color:var(--body)}
.vmeta .vdt{display:inline-flex;align-items:center;gap:8px}
.vmeta .sep{color:var(--line)}
@media (max-width:640px){.vrow{flex-direction:column}.vthumb{width:100%;aspect-ratio:16/9}.vinfo h3{white-space:normal}}

/* sidebar */
.sidebar{display:flex;flex-direction:column;gap:16px;position:sticky;top:96px}
.sidebox{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px;text-align:center}
.sidebox h4{font-size:19px;font-weight:700;color:var(--title)}
.sidebox .sub{font-size:14px;color:var(--body);margin-top:8px;line-height:1.9}
.sidebox--dark{color:#fff;border:none;
  background:radial-gradient(70% 60% at 88% -10%, rgba(139,92,246,.45), transparent 60%),
             linear-gradient(150deg,#232945,#2f2a63 55%,#3b34a8)}
.sidebox--dark h4{color:#fff}
.sidebox--dark .sub{color:rgba(255,255,255,.72)}
.socials{display:flex;justify-content:center;gap:10px;margin-top:14px}
.socials a{width:40px;height:40px;border-radius:12px;background:#fff;border:1px solid var(--line);display:grid;place-items:center;color:var(--ink);transition:.15s}
.socials a:hover{background:var(--brand);color:#fff;border-color:var(--brand)}
.socials svg{width:20px;height:20px}
.sbtn{display:block;width:100%;text-align:center;font-weight:400;font-size:15px;padding:13px 18px;border-radius:12px;margin-top:16px;transition:.15s}
.sbtn--dark{background:var(--ink);color:#FBFBFB}
.sbtn--dark:hover{background:var(--brand)}
.sbtn--light{background:#fff;color:var(--brand);border:1px solid var(--brand)}
.sbtn--light:hover{background:var(--brand);color:#fff}

/* ---------- blog ---------- */
.blog{margin-top:64px}
.sec-head{text-align:center}
.sec-head h2{font-size:26px;font-weight:700;color:var(--title)}
.sec-head p{font-size:15px;color:var(--body);margin-top:10px}
.blog__top{display:flex;align-items:center;justify-content:center;gap:16px;margin-top:26px;flex-wrap:wrap}
.blog__row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:8px}
.post{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}
.post .thumb{aspect-ratio:16/10;display:grid;place-items:center}
.post .thumb svg{width:40px;height:40px;color:var(--brand)}
.post .body{padding:16px;display:flex;flex-direction:column;flex:1}
.post h3{font-size:15px;font-weight:600;color:var(--black);line-height:1.6}
.post p{font-size:13px;color:var(--muted);margin-top:6px;line-height:1.8}
.post .meta{font-size:11px;color:var(--muted);margin-top:12px}
.post .more{font-size:13px;color:var(--brand);margin-top:auto;padding-top:12px}
.more-btn{border:1px solid var(--line);background:#fff;border-radius:12px;padding:10px 20px;font-size:14px;color:var(--ink);transition:.15s}
.more-btn:hover{border-color:var(--brand);color:var(--brand)}
@media (max-width:900px){.blog__row{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.blog__row{grid-template-columns:1fr}}

/* divider */
.divider{height:1px;background:var(--line);margin:64px auto;max-width:1280px}

/* faq */
.faq__rows{max-width:900px;margin:26px auto 0;display:flex;flex-direction:column;gap:12px}
.faq__row{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}
.faq__row summary{list-style:none;cursor:pointer;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.faq__row h3{font-size:17px;font-weight:700;color:var(--ink)}
.faq__row .chev{color:var(--brand);font-size:20px;transition:.2s;transform:rotate(90deg)}
.faq__row[open] .chev{transform:rotate(-90deg)}
.faq__row .ans{padding:0 20px 16px;font-size:14px;color:var(--body);line-height:1.9;max-width:80ch}

/* contact */
.contact{margin-top:64px}
.contact__grid{display:grid;grid-template-columns:1fr 1.2fr;gap:28px;align-items:start}
@media (max-width:900px){.contact__grid{grid-template-columns:1fr}}
.contact__info h2{font-size:19px;font-weight:700;color:var(--black)}
.contact__info p{font-size:14px;color:var(--body);margin-top:12px;line-height:2;max-width:52ch}
.form{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px;display:flex;flex-direction:column;gap:14px}
.field{display:flex;flex-direction:column;gap:6px}
.field label{font-size:13px;font-weight:600;color:var(--black)}
.field input,.field textarea{border:1px solid var(--line);border-radius:10px;padding:11px 14px;font-family:var(--font);font-size:13px;color:var(--ink);background:#fff}
.field textarea{min-height:90px;resize:vertical}
.field .hint{font-size:12px;color:var(--body)}
.form__submit{background:var(--ink);color:#FAFAFA;border:none;border-radius:12px;padding:14px;font-family:var(--font);font-size:15px;cursor:pointer;transition:.15s}
.form__submit:hover{background:var(--brand)}

/* footer */
.footer{margin-top:72px;background:#17181F;color:#fff;padding:56px 20px 24px}
.footer__in{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:36px;max-width:1280px;margin-inline:auto}
.footer__brand p{color:rgba(255,255,255,.65);font-size:13.5px;margin-top:12px;max-width:34ch;line-height:2}
.footer h4{font-size:15px;font-weight:700;margin-bottom:14px}
.footer ul{list-style:none;display:flex;flex-direction:column;gap:10px}
.footer a{color:rgba(255,255,255,.8);font-size:13.5px;transition:.15s}
.footer a:hover{color:#7C5CFC}
.footer__bar{border-top:1px solid rgba(255,255,255,.1);margin-top:40px;padding-top:20px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:12px;color:rgba(255,255,255,.5);max-width:1280px;margin-inline:auto}
.brand-mark{display:inline-flex;align-items:center;gap:8px;font-weight:900;font-size:18px;color:#7C5CFC}
.brand-mark .dot{width:10px;height:10px;border-radius:3px;background:#7C5CFC;transform:rotate(45deg)}
@media (max-width:900px){.footer__in{grid-template-columns:1fr}.nav__links{display:none}}
</style>
</head>
<body>

<div class="banner">
  <div class="wrap banner__in">
    <span class="banner__deal">پیشنهاد ویژه</span>
    <span>با منوچ کسب و کارت رونق می‌گیره؛ همین حالا با ۱۴ روز تست رایگان شروع کن</span>
    <span class="banner__timer">فقط تا ۳۰ آذر</span>
  </div>
</div>

<header class="nav">
  <div class="wrap nav__in">
    <a class="nav__logo" href="menuch-landing.html">منوچ</a>
    <nav class="nav__links">
      <a href="menuch-landing.html#customers">مشتریان</a>
      <a href="menuch-landing.html#features">ویژگی‌ها</a>
      <a href="menuch-pricing.html">تعرفه</a>
      <a href="menuch-landing.html#blog">مقالات</a>
      <a href="menuch-landing.html#faq">سوالات متداول</a>
      <a href="menuch-academy.html" class="on">آکادمی</a>
    </nav>
    <div class="nav__actions">
      <span class="nav__trust">مورد اعتماد : ۳۰۰۰ نفر</span>
      <a class="nav__cta" href="menuch-pricing.html">انتخاب پکیج</a>
    </div>
  </div>
</header>

<main class="wrap">
  <nav class="crumb">
    <a href="menuch-landing.html">منوچ</a><span>/</span><span class="on">آکادمی</span>
  </nav>

  <!-- featured: player (right) + text (left) -->
  <section class="featured">
    <div class="player">
      <div class="pl-img"></div>
      <span class="play">__PLAY__</span>
      <div class="pl-info"><span class="pl-title">__FEAT_OVERLAY__</span>__FEAT_TAG__</div>
    </div>
    <div class="finfo">
      <h1>__FEAT_TITLE__</h1>
      <p>__FEAT_DESC__</p>
      <div class="fmeta">
        __FEAT_TAG2__
        <span class="vdt"><span>__FEAT_DATE__</span><span class="sep">/</span><span>__FEAT_TIME__</span></span>
      </div>
    </div>
  </section>

  <!-- content: videos (right) + sidebar (left) -->
  <div class="content">
    <section class="videos">
      <div class="videos__head"><h2>آکادمی منوچ</h2><span>۲۴ ویدئو آموزشی</span></div>
      __ROWS__
    </section>
    <aside class="sidebar">
      <div class="sidebox sidebox--dark">
        <h4>عضو شوید</h4>
        <p class="sub">با عضویت در آکادمی منوچ، از آموزش‌های جدید و تخفیف دوره‌ها باخبر شو.</p>
        <a class="sbtn sbtn--light" href="#">عضویت در آکادمی</a>
      </div>
      <div class="sidebox">
        <h4>کانال های ما</h4>
        <p class="sub">آموزش‌های کوتاه رو هر روز ببین</p>
        <div class="socials">
          <a href="#" aria-label="اینستاگرام"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor" stroke="none"/></svg></a>
          <a href="#" aria-label="تلگرام"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m20.5 4.5-16 7 5.5 2 2.5 6 3-3.5 4 3.5 1-15Z"/></svg></a>
          <a href="#" aria-label="آپارات"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M10.5 9.5v5l4.5-2.5-4.5-2.5Z"/></svg></a>
        </div>
      </div>
      <div class="sidebox sidebox--dark">
        <h4>فروشگاهت رو بساز</h4>
        <p class="sub">با ۶۹۰ هزار تومان در ماه، فروش آنلاین رو شروع کن.</p>
        <a class="sbtn sbtn--light" href="menuch-pricing.html">با ۶۹۰ هزار تومان شروع کن</a>
      </div>
      <div class="sidebox">
        <h4>سوالی داری؟</h4>
        <p class="sub">تیم پشتیبانی هر روز از ۸ صبح تا ۱۰ شب پاسخگوست.</p>
        <a class="sbtn sbtn--dark" href="menuch-landing.html#contact">درخواست مشاوره</a>
      </div>
    </aside>
  </div>

  <!-- blog -->
  <section class="blog">
    <div class="sec-head">
      <h2>مقالات کاربردی</h2>
      <p>نکته‌ها و راهنمایی‌های کاربردی برای فروش آنلاین</p>
    </div>
    <div class="blog__top"><a class="more-btn" href="menuch-landing.html#blog">مشاهده همه</a></div>
    <div class="blog__row">
      __POSTS__
    </div>
  </section>
</main>

<div class="divider"></div>

<section class="faq wrap">
  <div class="sec-head">
    <h2>سوالات متداول</h2>
    <p>پاسخ سوال‌هایی که بیشتر از همه از ما می‌پرسید</p>
  </div>
  <div class="faq__rows">
    __FAQS__
  </div>
</section>

<section class="contact wrap">
  <div class="contact__grid">
    <div class="contact__info">
      <h2>درخواست مشاوره</h2>
      <p>تیم فروش و پشتیبانی ما از ساعت ۸ صبح تا ۱۰ شب پاسخگوی شماست؛ هر زمان درخواستی ثبت کنید حداکثر ۴ ساعت بعد با شما تماس می‌گیریم.</p>
    </div>
    <form class="form" onsubmit="return false">
      <div class="field"><label>نام و نام خانوادگی</label><input type="text" placeholder="محمد گندمی"></div>
      <div class="field"><label>شماره تماس</label><input type="tel" placeholder="۰۹۱۵"></div>
      <div class="field"><label>کسب و کار</label><input type="text" placeholder="مبلمان"></div>
      <div class="field"><label>توضیحات</label><textarea placeholder="من نیاز به مشاوره دارم"></textarea></div>
      <button class="form__submit" type="submit">ثبت درخواست مشاوره</button>
    </form>
  </div>
</section>

<footer class="footer">
  <div class="footer__in">
    <div class="footer__brand">
      <span class="brand-mark"><span class="dot"></span>منوچ</span>
      <p>فروشگاه‌ساز آنلاین و دستیار رشد کسب‌وکار؛ از راه‌اندازی فروشگاه تا نگه‌داشتن مشتری، یکجا توی منوچ.</p>
    </div>
    <div>
      <h4>دسترسی سریع</h4>
      <ul>
        <li><a href="menuch-landing.html">صفحه اصلی</a></li>
        <li><a href="menuch-pricing.html">تعرفه و پلن‌ها</a></li>
        <li><a href="menuch-landing.html#features">ویژگی‌ها</a></li>
        <li><a href="menuch-landing.html#faq">سوالات متداول</a></li>
      </ul>
    </div>
    <div>
      <h4>آکادمی</h4>
      <ul>
        <li><a href="#">شروع کار</a></li>
        <li><a href="#">فروش و پرداخت</a></li>
        <li><a href="#">بازاریابی</a></li>
        <li><a href="#">باشگاه مشتریان</a></li>
      </ul>
    </div>
  </div>
  <div class="footer__bar">
    <span>تمامی حقوق برای استودیو اثر محفوظ است.</span>
    <span>All rights are reserved | Effect Studio 2025</span>
  </div>
</footer>

</body>
</html>
"""

page = page.replace('__FONT__', FONT_CSS)
page = page.replace('__PLAY__', play_icon(30))
page = page.replace('__FEAT_TITLE__', FEATURED['title'])
page = page.replace('__FEAT_DESC__', FEATURED['desc'])
page = page.replace('__FEAT_DATE__', FEATURED['date'])
page = page.replace('__FEAT_TIME__', FEATURED['time'])
page = page.replace('__FEAT_OVERLAY__', FEATURED['overlay'])
page = page.replace('__FEAT_TAG__', tag_badge(FEATURED['tag'], FEATURED['count']))
page = page.replace('__FEAT_TAG2__', tag_badge(FEATURED['tag'], FEATURED['count']))
page = page.replace('__ROWS__', ROWS)
page = page.replace('__POSTS__', post_cards)
page = page.replace('__FAQS__', faq_rows)

open('menuch-academy.html', 'w', encoding='utf-8').write(page)
print("written menuch-academy.html, length:", len(page))
