# -*- coding: utf-8 -*-
"""Build menuch-blog.html — صفحه مقالات مطابق دیزاین فیگما"""
import base64, json

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

blog_imgs = json.load(open('_blog_b64.json'))

# ---------------- articles ----------------
POSTS = [
    ("چرا وبسایت دردسر داره؟", "آشنایی با دردسرهای رایج سایت‌سازها و راه‌حل منوچ", "۱۲:۳۰", "یکشنبه ۱۲ مرداد ۱۴۰۵", "b1"),
    ("سئو چقدر مهمه؟", "چطور با سئو مشتری بیشتری به فروشگاهت بیاری", "۱۲:۳۰", "یکشنبه ۱۲ مرداد ۱۴۰۵", "b2"),
    ("چرا سایت‌سازها؟", "مقایسه سایت‌سازها؛ کدوم برای کسب‌وکار تو بهتره", "۱۲:۳۰", "یکشنبه ۱۲ مرداد ۱۴۰۵", "b3"),
    ("فروش چجوری انجام می‌شه؟", "مسیر کامل فروش در منوچ؛ از سفارش تا تسویه", "۱۲:۳۰", "یکشنبه ۱۲ مرداد ۱۴۰۵", "b4"),
    ("باشگاه مشتریان چطور کار می‌کنه؟", "امتیاز، سطح‌بندی، کمپین و SMS برای نگه‌داشتن مشتری", "۰۹:۱۵", "سه‌شنبه ۱۴ مرداد ۱۴۰۵", "b2"),
    ("فروش اقساطی در فروشگاهت", "اسنپ‌پی، ترب‌پی و دیجی‌پی؛ فروش اعتباری و دریافت نقدی", "۱۴:۴۰", "پنجشنبه ۱۶ مرداد ۱۴۰۵", "b1"),
    ("راه‌اندازی درگاه پرداخت", "زرین‌پال، زیبال و کارت‌به‌کارت؛ تسویه سریع بدون واسطه", "۱۰:۰۵", "شنبه ۱۸ مرداد ۱۴۰۵", "b3"),
    ("مدیریت انبار با Excel", "ورود گروهی موجودی، قیمت و Export اطلاعات", "۱۶:۲۰", "دوشنبه ۲۰ مرداد ۱۴۰۵", "b4"),
]

def card(t, d, time, date, img):
    return f'''<article class="mn-post">
      <img src="data:image/webp;base64,{blog_imgs[img]}" alt="{t}">
      <div class="mn-post__body">
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="mn-post__meta">
          <svg class="mn-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>{time}
          <span class="vsep"></span>{date}
        </div>
        <a href="#" class="mn-post__btn">
          <span class="mn-ricon" style="width:16px;height:16px"><svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10.8637 24.8753C11.3928 24.4318 12.1812 24.5013 12.6247 25.0304L14.5833 27.3673V18.3333C14.5833 17.6429 15.143 17.0833 15.8333 17.0833C16.5237 17.0833 17.0833 17.6429 17.0833 18.3333V27.3666L19.0421 25.0302C19.4856 24.5012 20.274 24.4319 20.8031 24.8754C21.3321 25.3189 21.4014 26.1073 20.9579 26.6364L17.8885 30.2974C17.3564 30.9322 16.5948 31.2498 15.8333 31.25C15.0714 31.2501 14.3095 30.9326 13.7772 30.2974L10.7086 26.6362C10.2652 26.1071 10.3346 25.3187 10.8637 24.8753Z" fill="#3D4350"/><path fill-rule="evenodd" clip-rule="evenodd" d="M22.5546 2.91663C24.1726 2.91663 25.6624 3.75554 26.9313 4.85893C28.218 5.97779 29.4204 7.49122 30.4869 9.12469C32.6197 12.3914 34.3413 16.3433 35.1727 19.1732C35.3495 19.7748 35.4166 20.3781 35.4166 20.9599V30C35.4166 33.912 32.2453 37.0833 28.3333 37.0833H11.6666C7.75463 37.0833 4.58331 33.912 4.58331 30V9.99996C4.58331 6.08794 7.75463 2.91663 11.6666 2.91663H22.5546Z" fill="#3D4350"/></svg></span>مشاهده مقاله
        </a>
      </div>
    </article>'''

CARDS = "\n".join(card(*p) for p in POSTS)

# ---------------- assemble ----------------
page = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مقالات کاربردی — منوچ</title>
<style>
__FONT__
:root{
  --brand:#4B45E6; --ink:#202A37; --title:#3D4350; --body:#737377; --muted:#A2A2A5;
  --black:#16161D; --line:#E0E2E7; --paper:#FEFEFE; --soft:#FAFAFA;
  --lav:#ECEbfd; --lav-2:#ACA9F4; --banner:#BABDC1; --chip-black:#171E27; --muted-2:#A2A2A5;
  --radius:12px; --font:'Ravi','Estedad',Tahoma,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);color:var(--ink);background:var(--paper);line-height:1.8;direction:rtl}
a{text-decoration:none;color:inherit}
img{display:block;max-width:100%}
.wrap{max-width:1280px;margin-inline:auto;padding-inline:clamp(16px,2.5vw,40px)}
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
@media (max-width:900px){.mn-nav__links{display:none}}

/* ---------- بردکرامب ---------- */
.crumb{display:flex;align-items:center;gap:10px;margin:24px 0 4px;font-size:14px;color:var(--muted)}
.crumb .on{color:var(--brand)}

/* ---------- هدر سکشن ---------- */
.mn-sechead{text-align:center;margin-top:96px}
.mn-sechead h2{font-size:clamp(25px,2.6vw,33px);font-weight:700;line-height:1.95;color:var(--title)}
.mn-sechead>p{font-size:clamp(14px,1.5vw,19px);color:var(--body);margin-top:12px;line-height:2.1}

/* ---------- بلاگ ---------- */
.mn-blog__row{margin-top:32px;display:grid;grid-template-columns:repeat(4,264px);justify-content:center;gap:24px;align-items:stretch}
.mn-post{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;transition:transform .18s ease,box-shadow .18s ease}
.mn-post:hover{transform:translateY(-4px);box-shadow:0 16px 36px rgba(32,42,55,.1)}
.mn-post>img{width:100%;aspect-ratio:240/183;object-fit:cover}
.mn-post__body{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.mn-post__body h3{font-size:16px;font-weight:600;color:var(--black)}
.mn-post__body>p{font-size:13px;color:var(--muted-2)}
.mn-post__meta{font-size:11px;color:var(--muted-2);display:flex;align-items:center;gap:6px}
.mn-post__meta .mn-ico{width:13px;height:13px}
.mn-post__meta .vsep{width:1px;height:12px;background:var(--line);display:inline-block}
.mn-post__btn{margin-top:auto;background:rgba(75,69,230,.2);color:var(--brand);text-align:center;font-size:13px;font-weight:400;padding:10px;border-radius:12px;display:inline-flex;align-items:center;justify-content:center;gap:6px;transition:all .15s ease}
.mn-post__btn .mn-ricon{width:16px;height:16px}
.mn-post__btn:hover{background:var(--brand);color:#fff}
@media (max-width:1180px){.mn-blog__row{grid-template-columns:repeat(3,264px)}}
@media (max-width:900px){.mn-blog__row{grid-template-columns:repeat(2,264px)}}
@media (max-width:600px){.mn-blog__row{grid-template-columns:1fr}}

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

<header class="mn-nav">
  <div class="mn-wrap mn-nav__in">
    <a href="menuch-landing.html" class="mn-nav__logo" aria-label="منوچ"><img src="__LOGO__" alt="منوچ"></a>
    <nav class="mn-nav__links" aria-label="ناوبری اصلی"><a href="menuch-landing.html" class="">منوچ</a><a href="menuch-landing.html#customers" class="">مشتریان</a><a href="menuch-landing.html#features" class="">ویژگی‌ها</a><a href="menuch-pricing.html" class="">تعرفه</a><a href="menuch-blog.html" class="accent">مقالات</a><a href="menuch-landing.html#faq" class="">سوالات متداول</a><a href="menuch-academy.html" class=""><span class="divider"></span><span class="mn-ricon" style="width:24px;height:24px"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12.0099 17C11.1599 17 10.2999 16.78 9.62995 16.35L3.60995 12.42C2.48995 11.69 1.81995 10.46 1.81995 9.12C1.81995 7.78 2.48995 6.55 3.60995 5.82L9.63995 1.9C10.9799 1.03 13.0699 1.03 14.3999 1.91L20.3899 5.84C21.4999 6.57 22.1699 7.8 22.1699 9.13C22.1699 10.46 21.4999 11.69 20.3899 12.42L14.3999 16.35C13.7299 16.79 12.8699 17 12.0099 17ZM12.0099 2.75C11.4399 2.75 10.8699 2.88 10.4599 3.16L4.43995 7.08C3.73995 7.54 3.32995 8.28 3.32995 9.12C3.32995 9.96 3.72995 10.7 4.43995 11.16L10.4599 15.09C11.2899 15.63 12.7499 15.63 13.5799 15.09L19.5699 11.16C20.2699 10.7 20.6699 9.96 20.6699 9.12C20.6699 8.28 20.2699 7.54 19.5699 7.08L13.5799 3.15C13.1599 2.89 12.5899 2.75 12.0099 2.75Z" fill="#4B45E6"/><path d="M12.0001 22.75C11.5601 22.75 11.1101 22.69 10.7501 22.57L7.56006 21.51C6.05006 21.01 4.86006 19.36 4.87006 17.77L4.88006 13.08C4.88006 12.67 5.22006 12.33 5.63006 12.33C6.04006 12.33 6.38006 12.67 6.38006 13.08L6.37006 17.77C6.37006 18.71 7.15006 19.79 8.04006 20.09L11.2301 21.15C11.6301 21.28 12.3701 21.28 12.7701 21.15L15.9601 20.09C16.8501 19.79 17.6301 18.71 17.6301 17.78V13.14C17.6301 12.73 17.9701 12.39 18.3801 12.39C18.7901 12.39 19.1301 12.73 19.1301 13.14V17.78C19.1301 19.37 17.9501 21.01 16.4401 21.52L13.2501 22.58C12.8901 22.69 12.4401 22.75 12.0001 22.75Z" fill="#4B45E6"/><path d="M21.4 15.75C20.99 15.75 20.65 15.41 20.65 15V9C20.65 8.59 20.99 8.25 21.4 8.25C21.81 8.25 22.15 8.59 22.15 9V15C22.15 15.41 21.81 15.75 21.4 15.75Z" fill="#4B45E6"/></svg></span>آکادمی</a></nav>
    <div class="mn-nav__actions">
      <span class="mn-trust"><span class="mn-ricon" style="width:24px;height:24px"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M17.2 12.4C14.55 12.4 12.4 14.55 12.4 17.2C12.4 18.1 12.65 18.95 13.1 19.67C13.93 21.06 15.45 22 17.2 22C18.95 22 20.48 21.06 21.3 19.67C21.74 18.95 22 18.1 22 17.2C22 14.55 19.85 12.4 17.2 12.4ZM19.58 16.57L17.02 18.93C16.88 19.06 16.69 19.13 16.51 19.13C16.32 19.13 16.13 19.06 15.98 18.91L14.8 17.73C14.51 17.44 14.51 16.96 14.8 16.67C15.09 16.38 15.57 16.38 15.86 16.67L16.53 17.34L18.56 15.46C18.86 15.18 19.34 15.2 19.62 15.5C19.9 15.81 19.88 16.29 19.58 16.57Z" fill="#4B45E6"/><path opacity="0.4" d="M22 8.69C22 9.88 21.81 10.98 21.48 12C21.27 12.67 21 13.31 20.68 13.9C19.8 12.97 18.57 12.4 17.2 12.4C14.55 12.4 12.4 14.55 12.4 17.2C12.4 18.43 12.87 19.55 13.63 20.4C13.26 20.57 12.92 20.71 12.62 20.81C12.28 20.93 11.72 20.93 11.38 20.81C8.97 19.99 4.1 17 2.52 12C2.19 10.98 2 9.88 2 8.69C2 5.6 4.49 3.10001 7.56 3.10001C9.37 3.10001 10.99 3.97999 12 5.32999C13.01 3.97999 14.63 3.10001 16.44 3.10001C19.51 3.10001 22 5.6 22 8.69Z" fill="#4B45E6"/></svg></span>مورد اعتمادِ ۳٬۰۰۰+ کسب‌وکار</span>
      <a class="mn-btn-dark" href="menuch-pricing.html"><span class="mn-ricon" style="width:24px;height:24px"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11.79 11.88C11.25 11.88 10.7 11.78 10.27 11.59L4.36999 8.97C2.86999 8.3 2.64999 7.4 2.64999 6.91C2.64999 6.42 2.86999 5.52 4.36999 4.85L10.27 2.23C11.14 1.84 12.45 1.84 13.32 2.23L19.23 4.85C20.72 5.51 20.95 6.42 20.95 6.91C20.95 7.4 20.73 8.3 19.23 8.97L13.32 11.59C12.88 11.79 12.34 11.88 11.79 11.88ZM11.79 3.44C11.45 3.44 11.12 3.49 10.88 3.6L4.97999 6.22C4.36999 6.5 4.14999 6.78 4.14999 6.91C4.14999 7.04 4.36999 7.33 4.96999 7.6L10.87 10.22C11.35 10.43 12.22 10.43 12.7 10.22L18.61 7.6C19.22 7.33 19.44 7.04 19.44 6.91C19.44 6.78 19.22 6.49 18.61 6.22L12.71 3.6C12.47 3.5 12.13 3.44 11.79 3.44Z" fill="#FAFAFA"/><path d="M12 17.09C11.62 17.09 11.24 17.01 10.88 16.85L4.09 13.83C3.06 13.38 2.25 12.13 2.25 11C2.25 10.59 2.59 10.25 3 10.25C3.41 10.25 3.75 10.59 3.75 11C3.75 11.55 4.2 12.24 4.7 12.47L11.49 15.49C11.81 15.63 12.18 15.63 12.51 15.49L19.3 12.47C19.8 12.25 20.25 11.55 20.25 11C20.25 10.59 20.59 10.25 21 10.25C21.41 10.25 21.75 10.59 21.75 11C21.75 12.13 20.94 13.38 19.91 13.84L13.12 16.86C12.76 17.01 12.38 17.09 12 17.09Z" fill="#FAFAFA"/><path d="M12 22.09C11.62 22.09 11.24 22.01 10.88 21.85L4.09 18.83C2.97 18.33 2.25 17.22 2.25 15.99C2.25 15.58 2.59 15.24 3 15.24C3.41 15.24 3.75 15.59 3.75 16C3.75 16.63 4.12 17.21 4.7 17.47L11.49 20.49C11.81 20.63 12.18 20.63 12.51 20.49L19.3 17.47C19.88 17.21 20.25 16.64 20.25 16C20.25 15.59 20.59 15.25 21 15.25C21.41 15.25 21.75 15.59 21.75 16C21.75 17.23 21.03 18.34 19.91 18.84L13.12 21.86C12.76 22.01 12.38 22.09 12 22.09Z" fill="#FAFAFA"/></svg></span>شروع کنید</a>
    </div>
  </div>
</header>

<main class="wrap">
  <nav class="crumb">
    <a href="menuch-landing.html">منوچ</a><span>/</span><span class="on">مقالات</span>
  </nav>

  <section>
    <div class="mn-sechead"><h2>مقالات کاربردی</h2><p>نکته‌ها و راهنمایی‌های کاربردی برای فروش آنلاین و رشد کسب‌وکارت</p></div>
    <div class="mn-blog__row">
__CARDS__
    </div>
  </section>
</main>

<footer class="mn-footer">
  <div class="mn-footer__card">
    <div class="mn-footer__in">
      <div class="mn-footer__brandcol">
        <img class="mn-footer__logo" src="__FLOGO__" alt="منوچ — فروشگاه‌ساز آنلاین">
        <div class="mn-footer__contact">
          <div><svg class="mn-ico " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m4 8 8 5.5L20 8"/></svg><b>ایمیل:</b><span><a href="mailto:info@manooch.ir">info@manooch.ir</a></span></div>
          <div><svg class="mn-ico " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 4h3l1.5 4.5L10 10a12 12 0 0 0 4 4l1.5-2.5L20 13v3.5a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 6 6.2 2 2 0 0 1 8 4Z"/></svg><b>مشاوره:</b><span>0938 025 2088</span></div>
        </div>
        <div class="mn-footer__socials"><a href="#" aria-label="instagram"><svg class="mn-ico " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="3.8"/><circle cx="17" cy="7" r="0.8" fill="currentColor"/></svg></a><a href="#" aria-label="telegram"><svg class="mn-ico " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 4.5 3.5 11l5.3 2 2 5.3 3-2.8 4.5 3.2 2.2-14.2Zm-12.3 8.6 11-7"/></svg></a><a href="#" aria-label="youtube"><svg class="mn-ico " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="6" width="18" height="12" rx="3.5"/><path d="m10.2 9.5 4.8 2.5-4.8 2.5v-5Z" fill="currentColor" stroke="none"/></svg></a><a href="#" aria-label="linkedin"><svg class="mn-ico " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="3.5"/><path d="M8 10.5V17M8 7.6v.2M12.2 17v-3.6c0-1.4 1-2.4 2.3-2.4s2.3 1 2.3 2.4V17"/></svg></a><a href="#" aria-label="facebook"><svg class="mn-ico " viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 8.5V7a1.5 1.5 0 0 1 1.5-1.5h1.5V3h-2.6A4 4 0 0 0 11 7v1.5H8.5V11H11v9.5h3.5V11h2.4l.5-2.5H14.5Z"/></svg></a></div>
      </div>
      <div class="mn-footer__col"><h4>دسترسی سریع</h4><ul><li><a href="menuch-landing.html#features">چرا منوچ؟</a></li><li><a href="menuch-landing.html#customers">مشتریان ما</a></li><li><a href="menuch-landing.html#features">ویژگی‌ها</a></li><li><a href="menuch-pricing.html">پلن های ما</a></li><li><a href="menuch-landing.html#faq">سوالات متداول</a></li><li><a href="menuch-landing.html#contact">درخواست مشاوره</a></li></ul></div><div class="mn-footer__col"><h4>مقالات</h4><ul><li><a href="menuch-blog.html">چرا منوچ رو باید داشته باشیم</a></li><li><a href="menuch-blog.html">منوچ مناسب چه کسب‌وکاریه؟</a></li><li><a href="menuch-blog.html">بنکدارا خیالشون راحت باشه</a></li><li><a href="menuch-blog.html">واحد فروش پیشرفته</a></li></ul></div>
      <div class="mn-footer__col">
        <h4>نمادها</h4>
        <div class="mn-footer__badges">
          <img src="__BADGE1__" alt="نماد اعتماد">
          <img src="__BADGE2__" alt="نماد اعتماد">
        </div>
      </div>
    </div>
    <div class="mn-footer__bar">
      <span>تمامی حقوق برای استودیو اثر محفوظ است.</span>
      <span>All rights are reserved  |   Effect Studio  2025</span>
    </div>
  </div>
</footer>

</body>
</html>
"""

# extract assets from academy (which already has them from landing)
import re
academy = open('menuch-academy.html', encoding='utf-8').read()

logo_m = re.search(r'<a href="menuch-landing\.html" class="mn-nav__logo"[^>]*><img src="(data:image/webp;base64,[A-Za-z0-9+/=]+)"', academy)
flogo_m = re.search(r'<img class="mn-footer__logo" src="(data:image/webp;base64,[A-Za-z0-9+/=]+)"', academy)
badges = re.findall(r'<img src="(data:image/webp;base64,[A-Za-z0-9+/=]+)" alt="(?:نماد|Symbol|enamad|samandehi)[^"]*"', academy)

page = page.replace('__FONT__', FONT_CSS)
page = page.replace('__CARDS__', CARDS)
page = page.replace('__LOGO__', logo_m.group(1))
page = page.replace('__FLOGO__', flogo_m.group(1))

# find badges from academy footer
badge_imgs = re.findall(r'(<img src="data:image/webp;base64,[A-Za-z0-9+/=]+" alt="[^"]*">)', academy)
fb = academy.find('<div class="mn-footer__badges">')
fe = academy.find('</div>', fb)
badges_html = academy[fb:fe+6]
page = page.replace('          <img src="__BADGE1__" alt="نماد اعتماد">\n          <img src="__BADGE2__" alt="نماد اعتماد">\n', badges_html)

open('menuch-blog.html', 'w', encoding='utf-8').write(page)
print("written menuch-blog.html, length:", len(page))
print("cards:", len(POSTS))
print("unresolved placeholders:", page.count('__'))
