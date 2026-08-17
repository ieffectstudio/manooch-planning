# -*- coding: utf-8 -*-
"""Build menuch-pricing.html from manooch-pricing-structure-latest.md"""
import base64

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

# ---------------- render helpers ----------------
def cell(v):
    v = v.strip()
    if v == '✅':
        return '<span class="chk yes"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>'
    if v == '❌':
        return '<span class="chk no"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></span>'
    if v == 'نامحدود':
        return '<span class="pill inf">نامحدود</span>'
    return f'<span class="pval">{v}</span>'

# ---------------- plans ----------------
PLANS = [
    ("پایه", "۶۹۰٬۰۰۰", "شروع فروش آنلاین", False, None),
    ("استاندارد", "۱٬۲۹۰٬۰۰۰", "مدیریت حرفه‌ای فروش", True, "پیشنهاد منوچ"),
    ("پرو", "۲٬۴۹۰٬۰۰۰", "رشد، اتوماسیون و وفادارسازی", False, None),
]
cards = []
for name, price, tagline, hot, tag in PLANS:
    tag_html = f'<span class="ptag">{tag}</span>' if tag else ''
    cls = 'pcard hot' if hot else ('pcard dark' if name == 'پرو' else 'pcard')
    cards.append(f'''<article class="{cls}">{tag_html}
        <h3 class="pname">{name}</h3><p class="ptagline">{tagline}</p>
        <div class="pprice"><span class="num">{price}</span><span class="unit">تومان / ماه</span></div>
        <a class="pcta" href="#">شروع با {name}</a></article>''')
CARDS = "\n".join(cards)

# ---------------- subscription periods table (section 2.2) ----------------
PERIODS = [
    ("پایه", "۶۹۰٬۰۰۰", "۱٬۹۶۰٬۰۰۰", "۳٬۷۹۰٬۰۰۰"),
    ("استاندارد", "۱٬۲۹۰٬۰۰۰", "۳٬۶۶۰٬۰۰۰", "۷٬۰۹۰٬۰۰۰"),
    ("پرو", "۲٬۴۹۰٬۰۰۰", "۷٬۰۷۰٬۰۰۰", "۱۳٬۶۹۰٬۰۰۰"),
]
period_rows = "\n".join(
    f'<tr><td class="feat">{n}</td><td class="c">{p}</td>'
    f'<td class="c">{q}</td><td class="c">{s}</td></tr>'
    for n, p, q, s in PERIODS
)

# ---------------- summary table (section 25) ----------------
SUMMARY = [
    ("قیمت ماهانه", "۶۹۰٬۰۰۰", "۱٬۲۹۰٬۰۰۰", "۲٬۴۹۰٬۰۰۰"),
    ("قیمت سه‌ماهه", "۱٬۹۶۰٬۰۰۰", "۳٬۶۶۰٬۰۰۰", "۷٬۰۷۰٬۰۰۰"),
    ("قیمت شش‌ماهه", "۳٬۷۹۰٬۰۰۰", "۷٬۰۹۰٬۰۰۰", "۱۳٬۶۹۰٬۰۰۰"),
    ("تعداد محصول", "۱۰۰", "۱٬۰۰۰", "نامحدود"),
    ("عکس هر محصول", "۲", "۳", "۵"),
    ("ویس محصول", "❌", "✅", "✅"),
    ("افزودن کالا", "✅", "✅", "✅"),
    ("افزودن خدمات", "✅", "✅", "✅"),
    ("محصولات ارزی", "❌", "❌", "✅"),
    ("ویژگی محصول", "✅", "✅", "✅"),
    ("حذف پس‌زمینه", "❌", "✅", "✅"),
    ("توضیحات کالا با AI", "❌", "✅", "✅"),
    ("واحد فروش پیشرفته", "❌", "✅", "✅"),
    ("انبار", "❌", "✅", "✅"),
    ("Excel", "❌", "✅", "✅"),
    ("نوع پرداخت", "✅", "✅", "✅"),
    ("فروش حضوری", "❌", "✅", "✅"),
    ("فروش اقساطی", "❌", "❌", "✅"),
    ("تخفیف", "❌", "✅", "✅"),
    ("محتوا", "✅", "✅", "✅"),
    ("Notification", "✅", "✅", "✅"),
    ("نظرات", "❌", "✅", "✅"),
    ("گزارش فروش", "❌", "✅", "✅"),
    ("Social Marketing", "❌", "✅", "✅"),
    ("اتصال حسابداری", "❌", "❌", "✅"),
    ("باشگاه مشتریان", "❌", "❌", "✅"),
]
sum_rows = "\n".join(
    f'<tr><td class="feat">{f}</td><td class="c">{cell(b)}</td><td class="c">{cell(s)}</td><td class="c">{cell(p)}</td></tr>'
    for f, b, s, p in SUMMARY
)

# ---------------- modules ----------------
# badge: ('price', val) | ('core', label)
MODULES = [
    dict(title="ظرفیت‌های پلن", badge=("core", "افزونه نیست"),
         note="ظرفیت‌ها فقط برای تفکیک پلن‌ها استفاده می‌شوند و قیمت مستقل ندارند. سیاست یا محدودیت جداگانه‌ای برای Storage تعریف نشده است.",
         rows=[("تعداد محصول فعال", "۱۰۰", "۱٬۰۰۰", "نامحدود"),
               ("تعداد عکس هر محصول", "۲", "۳", "۵"),
               ("ویس محصول", "❌", "✅", "✅")]),
    dict(title="انواع قابل افزودن", badge=("core", "هسته محصول"),
         note="محصولات ارزی فقط در پلن پرو فعال است و روی پایه یا استاندارد جداگانه خریداری نمی‌شود. چیزی با عنوان «فایل دیجیتال» نداریم.",
         rows=[("افزودن کالا", "✅", "✅", "✅"),
               ("افزودن خدمات", "✅", "✅", "✅"),
               ("افزودن محصولات ارزی", "❌", "❌", "✅")]),
    dict(title="افزودن کالا", badge=("core", "هسته محصول"),
         note="«حذف پس‌زمینه» و «تولید توضیحات با AI» زیرمجموعه افزودن کالا هستند و افزونه ساختاری مستقل نیستند.",
         rows=[("افزودن کالا", "✅", "✅", "✅"),
               ("افزودن تصویر کالا", "✅", "✅", "✅"),
               ("ویژگی کالا", "✅", "✅", "✅"),
               ("قیمت‌گذاری کالا", "✅", "✅", "✅"),
               ("فعال / غیرفعال کردن کالا", "✅", "✅", "✅"),
               ("ویس محصول", "❌", "✅", "✅"),
               ("حذف پس‌زمینه تصویر کالا", "❌", "✅", "✅"),
               ("تولید توضیحات کالا با هوش مصنوعی", "❌", "✅", "✅")]),
    dict(title="فروشگاه و کاتالوگ", badge=("core", "در همه پلن‌ها"),
         note="چیزی با عنوان «زیردسته‌بندی» یا «چینش بخش‌های فروشگاه» نداریم.",
         rows=[("ساخت فروشگاه اینترنتی", "✅", "✅", "✅"),
               ("ساب‌دامنه منوچ", "✅", "✅", "✅"),
               ("دامنه اختصاصی", "✅", "✅", "✅"),
               ("SSL", "✅", "✅", "✅"),
               ("شخصی‌سازی رنگ و فونت", "✅", "✅", "✅"),
               ("لینکدونی", "✅", "✅", "✅"),
               ("دسته‌بندی", "✅", "✅", "✅"),
               ("قیمت‌گذاری ساده", "✅", "✅", "✅"),
               ("قیمت استعلامی", "✅", "✅", "✅"),
               ("فعال / غیرفعال کردن محصول", "✅", "✅", "✅")]),
    dict(title="ویژگی محصول", badge=("core", "افزونه نیست"),
         note="ویژگی بخشی از هسته محصول است و از پلن پایه فعال است.",
         rows=[("ویژگی محصول", "✅", "✅", "✅"),
               ("رنگ", "✅", "✅", "✅"),
               ("سایز", "✅", "✅", "✅"),
               ("مشخصات", "✅", "✅", "✅"),
               ("تعریف مقادیر ویژگی", "✅", "✅", "✅")]),
    dict(title="واحد فروش پیشرفته", badge=("price", "۲۹۰٬۰۰۰"),
         note="ماژول مستقل و متفاوت از «ویژگی محصول» است.",
         rows=[("واحد فروش پیشرفته", "❌", "✅", "✅"),
               ("تعریف واحدهای فروش", "❌", "✅", "✅"),
               ("قیمت هر واحد", "❌", "✅", "✅"),
               ("موجودی هر واحد", "❌", "✅", "✅"),
               ("حداقل سفارش هر واحد", "❌", "✅", "✅")]),
    dict(title="انبار", badge=("price", "۲۹۰٬۰۰۰"),
         note="Excel فیچر مستقل نیست و کاملاً زیرمجموعه انبار است؛ با فعال‌شدن انبار، قابلیت‌های Excel مربوط به آن نیز فعال می‌شوند.",
         rows=[("انبار", "❌", "✅", "✅"),
               ("مدیریت موجودی", "❌", "✅", "✅"),
               ("هشدار کمبود موجودی", "❌", "✅", "✅"),
               ("مدیریت موجودی کالاها", "❌", "✅", "✅"),
               ("ورود گروهی با Excel", "❌", "✅", "✅"),
               ("Import موجودی با Excel", "❌", "✅", "✅"),
               ("Import قیمت با Excel", "❌", "✅", "✅"),
               ("Export اطلاعات", "❌", "✅", "✅")]),
    dict(title="نوع پرداخت / روش‌های پرداخت", badge=("core", "در پلن‌ها"),
         note="زرین‌پال، زیبال، درگاه‌های بانکی و سایر Gatewayها زیرمجموعه پرداخت آنلاین هستند و جداگانه قیمت‌گذاری نمی‌شوند.",
         rows=[("پرداخت آنلاین", "✅", "✅", "✅"),
               ("پرداخت در محل", "✅", "✅", "✅"),
               ("کارت‌به‌کارت / آپلود فیش", "✅", "✅", "✅"),
               ("پرداخت توافقی / چکی", "❌", "✅", "✅"),
               ("لینک پرداخت", "❌", "✅", "✅"),
               ("پرداخت اعتباری / اقساطی", "❌", "❌", "✅")]),
    dict(title="فروش اقساطی", badge=("price", "۳۹۰٬۰۰۰"),
         note="Providerهای BNPL (اسنپ‌پی، ترب‌پی، دیجی‌پی و…) زیرمجموعه این ماژول هستند و جداگانه فروخته نمی‌شوند.",
         rows=[("فروش اقساطی", "❌", "❌", "✅"),
               ("اسنپ‌پی", "❌", "❌", "✅"),
               ("ترب‌پی", "❌", "❌", "✅"),
               ("دیجی‌پی", "❌", "❌", "✅"),
               ("سایر سرویس‌های اعتباری", "❌", "❌", "✅")]),
    dict(title="فروش حضوری", badge=("price", "۱۹۰٬۰۰۰"),
         note=None,
         rows=[("فروش حضوری", "❌", "✅", "✅"),
               ("انتخاب مشتری", "❌", "✅", "✅"),
               ("افزودن کالا", "❌", "✅", "✅"),
               ("ثبت فروش", "❌", "✅", "✅"),
               ("ثبت سفارش پرداخت‌شده", "❌", "✅", "✅"),
               ("آمار فروش روزانه", "❌", "✅", "✅")]),
    dict(title="تخفیف", badge=("price", "۹۹٬۰۰۰"),
         note=None,
         rows=[("تخفیف", "❌", "✅", "✅"),
               ("تخفیف درصدی", "❌", "✅", "✅"),
               ("تخفیف مبلغی", "❌", "✅", "✅"),
               ("تخفیف محصول", "❌", "✅", "✅"),
               ("تخفیف دسته‌بندی", "❌", "✅", "✅"),
               ("تخفیف مشتری", "❌", "✅", "✅")]),
    dict(title="مشتریان", badge=("core", "در همه پلن‌ها"),
         note=None,
         rows=[("دفترچه مشتریان", "✅", "✅", "✅"),
               ("پروفایل مشتری", "✅", "✅", "✅"),
               ("تاریخچه خرید", "✅", "✅", "✅"),
               ("جستجوی مشتری", "✅", "✅", "✅")]),
    dict(title="محتوا", badge=("core", "در همه پلن‌ها"),
         note="Notification زیرمجموعه محتواست؛ محتوا در ساختار فعلی افزونه مستقل قیمت‌دار در نظر گرفته نمی‌شود.",
         rows=[("محتوا", "✅", "✅", "✅"),
               ("Banner", "✅", "✅", "✅"),
               ("Gallery", "✅", "✅", "✅"),
               ("FAQ", "✅", "✅", "✅"),
               ("Team", "✅", "✅", "✅"),
               ("Bank Cards", "✅", "✅", "✅"),
               ("Notification", "✅", "✅", "✅")]),
    dict(title="نظرات", badge=("price", "۷۹٬۰۰۰"),
         note="نظرات یک افزونه مستقل است.",
         rows=[("نظرات مشتریان", "❌", "✅", "✅"),
               ("امتیازدهی", "❌", "✅", "✅"),
               ("ثبت نظر", "❌", "✅", "✅"),
               ("تأیید / رد نظر", "❌", "✅", "✅")]),
    dict(title="گزارش فروش", badge=("price", "۱۹۰٬۰۰۰"),
         note=None,
         rows=[("گزارش فروش", "❌", "✅", "✅"),
               ("درآمد", "❌", "✅", "✅"),
               ("گزارش روزانه", "❌", "✅", "✅"),
               ("گزارش هفتگی", "❌", "✅", "✅"),
               ("گزارش ماهانه", "❌", "✅", "✅"),
               ("محصولات پرفروش", "❌", "✅", "✅"),
               ("مشتریان برتر", "❌", "✅", "✅")]),
    dict(title="Social Marketing", badge=("price", "۳۹۰٬۰۰۰"),
         note="کاربر Social Marketing را می‌خرد، نه اتصال تلگرام، بله یا هر قابلیت انتشار را جداگانه.",
         rows=[("Social Marketing", "❌", "✅", "✅"),
               ("اتصال تلگرام", "❌", "✅", "✅"),
               ("اتصال بله", "❌", "✅", "✅"),
               ("اتصال سایر کانال‌ها", "❌", "✅", "✅"),
               ("انتشار محصول", "❌", "✅", "✅"),
               ("انتشار تصاویر و اطلاعات محصول", "❌", "✅", "✅"),
               ("انتشار گروهی", "❌", "✅", "✅"),
               ("انتشار خودکار", "❌", "✅", "✅"),
               ("زمان‌بندی انتشار", "❌", "✅", "✅")]),
    dict(title="اتصال حسابداری", badge=("price", "۲۹۰٬۰۰۰"),
         note="فقط داخل پلن پرو فعال است؛ کاربر پایه یا استاندارد می‌تواند این ماژول را جداگانه خریداری کند. Providerهای حسابداری جداگانه قیمت‌گذاری نمی‌شوند.",
         rows=[("اتصال حسابداری", "❌", "❌", "✅"),
               ("اتصال نرم‌افزارهای حسابداری", "❌", "❌", "✅"),
               ("Sync کالا", "❌", "❌", "✅"),
               ("Sync موجودی", "❌", "❌", "✅")]),
    dict(title="باشگاه مشتریان", badge=("price", "۶۹۰٬۰۰۰"),
         note="چه با پلن پرو و چه با خرید جداگانه، تمام قابلیت‌ها فعال می‌شود؛ نسخه Lite یا Limited نداریم.",
         rows=[("باشگاه مشتریان", "❌", "❌", "✅"),
               ("امتیاز خوش‌آمدگویی", "❌", "❌", "✅"),
               ("امتیاز بر اساس خرید", "❌", "❌", "✅"),
               ("مصرف امتیاز", "❌", "❌", "✅"),
               ("انقضای امتیاز", "❌", "❌", "✅"),
               ("قوانین امتیازدهی", "❌", "❌", "✅"),
               ("تاریخچه امتیازات", "❌", "❌", "✅"),
               ("افزایش / کاهش دستی امتیاز", "❌", "❌", "✅"),
               ("Segmentation مشتری", "❌", "❌", "✅"),
               ("New / Loyal / VIP / At Risk", "❌", "❌", "✅"),
               ("SMS Marketing", "❌", "❌", "✅"),
               ("ارسال گروهی پیامک", "❌", "❌", "✅"),
               ("زمان‌بندی پیامک", "❌", "❌", "✅"),
               ("قالب پیامک", "❌", "❌", "✅"),
               ("Delivery Report", "❌", "❌", "✅"),
               ("کمپین‌ها", "❌", "❌", "✅"),
               ("گزارش باشگاه", "❌", "❌", "✅")]),
]

def gchip_html(kind, val):
    if kind == "price":
        return '<span class="gchip price">افزونه مستقل</span>'
    return f'<span class="gchip core">{val}</span>'

def price_cell(kind, val, idx):
    if kind == "core":
        return '<span class="muted dash">—</span>'
    if idx == 0:
        return f'<b class="price">{val}</b>'
    return '<span class="chip sub">همراه ماژول</span>'

group_rows = []
for m in MODULES:
    kind, val = m["badge"]
    note = f'<span class="gnote">{m["note"]}</span>' if m["note"] else ''
    group_rows.append(
        f'<tr class="grouph"><td colspan="5">'
        f'<div class="ghead"><span class="gname">{m["title"]}</span>{gchip_html(kind, val)}</div>'
        f'{note}</td></tr>')
    for i, (f, b, s, p) in enumerate(m["rows"]):
        feat_cls = 'feat bold' if i == 0 else 'feat'
        group_rows.append(
            f'<tr><td class="{feat_cls}">{f}</td>'
            f'<td class="p p-b">{cell(b)}</td><td class="p p-s">{cell(s)}</td><td class="p p-p">{cell(p)}</td>'
            f'<td class="pl">{price_cell(kind, val, i)}</td></tr>')
MODS = "\n".join(group_rows)

# ---------------- plugins (section 26) ----------------
PLUGINS = [
    ("واحد فروش پیشرفته", "۲۹۰٬۰۰۰ تومان"),
    ("انبار", "۲۹۰٬۰۰۰ تومان"),
    ("فروش حضوری", "۱۹۰٬۰۰۰ تومان"),
    ("فروش اقساطی", "۳۹۰٬۰۰۰ تومان"),
    ("تخفیف", "۹۹٬۰۰۰ تومان"),
    ("نظرات", "۷۹٬۰۰۰ تومان"),
    ("گزارش فروش", "۱۹۰٬۰۰۰ تومان"),
    ("Social Marketing", "۳۹۰٬۰۰۰ تومان"),
    ("اتصال حسابداری", "۲۹۰٬۰۰۰ تومان"),
    ("باشگاه مشتریان", "۶۹۰٬۰۰۰ تومان"),
]
plug_rows = "\n".join(
    f'<tr><td class="feat">{n}</td><td class="pl"><b class="price">{p}</b></td></tr>'
    for n, p in PLUGINS
)

# ---------------- non-standalone (section 27) ----------------
NONSTAND = ["تعداد محصول", "تعداد عکس", "ویس محصول", "ویژگی محصول", "رنگ", "سایز",
            "محصولات ارزی", "Excel", "Notification", "حذف پس‌زمینه", "تولید توضیحات با AI",
            "Providerهای پرداخت آنلاین", "Providerهای فروش اقساطی", "Connectorهای Social Marketing",
            "Providerهای حسابداری", "زیرقابلیت‌های باشگاه مشتریان", "Storage"]
chips = "\n".join(f'<li>{x}</li>' for x in NONSTAND)

# ---------------- open decisions (section 28) ----------------
DECISIONS = [
    "بررسی نهایی اقتصاد افزونه‌ها در برابر Upgrade پلن",
    "تعیین مبلغ بسته‌های شارژ اعتبار پیامک",
    "بررسی نحوه نمایش «صرفه‌جویی» دوره سه‌ماهه و شش‌ماهه در صفحه Pricing",
]
decisions = "\n".join(f'<li><span class="dnum">{i+1}</span>{d}</li>' for i, d in enumerate(DECISIONS))

# ---------------- policies (sections 22-24) ----------------
POLICIES = [
    ("سیاست اعتبار پیامک", "هر پیامک ۳۲۰ تومان",
     "اعتبار SMS مستقل از قیمت پلن و باشگاه مشتریان است؛ کاربر متناسب با مصرف، اعتبار پیامکی حسابش را شارژ می‌کند (Pay As You Use). پلن پرو یا خرید باشگاه به معنی پیامک نامحدود نیست و هزینه هر پیامک از اعتبار شارژشده کسر می‌شود.",
     ["قیمت هر پیامک: ۳۲۰ تومان", "پلن پرو = پیامک نامحدود نیست", "هزینه ارسال از اعتبار شارژشده کسر می‌شود"]),
    ("سیاست AI", "بدون Token فروشی",
     "در حال حاضر سیاست مصرف جداگانه‌ای برای AI تعریف نشده است؛ سیستم Token فروشی، کیف پول AI یا محدودیت مصرف جداگانه نداریم. «تولید توضیحات کالا با AI» در استاندارد و پرو فعال است و زیرمجموعه افزودن کالا محسوب می‌شود.",
     ["سیستم Token فروشی تعریف نشده", "کیف پول AI جداگانه تعریف نشده", "محدودیت مصرف AI جداگانه لحاظ نشده"]),
    ("سیاست Storage", "بدون Limit جداگانه",
     "در حال حاضر سیاست تجاری یا Limit جداگانه‌ای برای Storage تعریف نشده است؛ Storage افزونه مستقل نیست، قیمت مستقل ندارد و در جدول قیمت‌گذاری فعلی تفکیک نمی‌شود.",
     ["افزونه مستقل نیست", "قیمت مستقل ندارد", "در جدول قیمت‌گذاری تفکیک نمی‌شود"]),
]
pol_cards = []
for title, sub, body, points in POLICIES:
    lis = "\n".join(f'<li>{p}</li>' for p in points)
    pol_cards.append(f'''<article class="pol">
      <header class="pol__head"><h3>{title}</h3><span class="pol__badge">{sub}</span></header>
      <p class="pol__body">{body}</p>
      <ul class="pol__points">{lis}</ul>
    </article>''')
POLICIES_HTML = "\n".join(pol_cards)

# ---------------- assemble page ----------------
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
  --red:#E5484D; --red-bg:#FDECEC; --card:#ffffff; --amber:#B45309; --amber-bg:#FEF3C7;
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
.phead{{text-align:center;padding:68px 20px 16px}}
.kicker{{display:inline-block;background:rgba(75,69,230,.08);color:var(--brand);
  border:1px solid rgba(75,69,230,.22);font-size:13.5px;font-weight:700;
  padding:7px 16px;border-radius:999px;margin-bottom:18px}}
.phead h1{{font-size:clamp(28px,4vw,44px);font-weight:900;margin:0 0 12px;line-height:1.35}}
.phead p{{color:var(--mut);font-size:clamp(14.5px,1.4vw,17px);max-width:680px;margin:0 auto}}

/* ---------- model callout ---------- */
.model{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin:26px auto 8px}}
.model .chip{{background:var(--card);border:1px solid var(--line);border-radius:999px;
  padding:9px 20px;font-size:13.5px;font-weight:600;color:var(--ink)}}
.model .chip b{{color:var(--brand);font-weight:700}}

/* ---------- plan cards ---------- */
.plans{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin:36px auto 14px;align-items:stretch}}
.pcard{{position:relative;background:var(--card);border:1px solid var(--line);
  border-radius:22px;padding:30px 28px;display:flex;flex-direction:column;
  transition:transform .2s ease, box-shadow .2s ease}}
.pcard:hover{{transform:translateY(-5px);box-shadow:0 24px 48px rgba(32,42,55,.12)}}
.pcard.hot{{border:2px solid var(--brand);box-shadow:0 18px 44px rgba(75,69,230,.16)}}
.pcard.dark{{color:#fff;border:none;
  background:radial-gradient(70% 60% at 88% -10%, rgba(139,92,246,.45), transparent 60%),
             linear-gradient(150deg,#232945,#2f2a63 55%,#3b34a8);
  box-shadow:0 24px 56px rgba(35,41,69,.35)}}
.ptag{{position:absolute;top:-14px;inset-inline-start:50%;transform:translateX(50%);
  background:var(--brand);color:#fff;font-size:12.5px;font-weight:700;
  padding:5px 16px;border-radius:999px;white-space:nowrap}}
.pname{{font-size:21px;font-weight:800;margin:0 0 4px}}
.pcard.dark .pname{{color:#fff}}
.ptagline{{color:var(--mut);font-size:13.5px;margin:0 0 20px;min-height:24px}}
.pcard.dark .ptagline{{color:rgba(255,255,255,.72)}}
.pprice{{display:flex;align-items:baseline;gap:8px;margin-bottom:22px}}
.pprice .num{{font-size:32px;font-weight:900;letter-spacing:-.5px}}
.pprice .unit{{color:var(--mut);font-size:13px}}
.pcard.dark .pprice .unit{{color:rgba(255,255,255,.65)}}
.pcta{{display:block;text-align:center;font-weight:700;font-size:15px;
  padding:13px 20px;border-radius:12px;background:var(--ink);color:#fff;
  transition:background .18s ease;margin-top:auto}}
.pcta:hover{{background:#151b28}}
.pcard.hot .pcta{{background:var(--brand)}}
.pcard.hot .pcta:hover{{background:#3a35c9}}
.pcard.dark .pcta{{background:#fff;color:#3b34a8}}
.pcard.dark .pcta:hover{{background:#f2f1ff}}

.note{{margin:12px auto 0;font-size:12.5px;color:var(--mut);
  background:rgba(75,69,230,.05);border:1px dashed rgba(75,69,230,.25);
  border-radius:12px;padding:10px 16px}}

/* ---------- sections ---------- */
.sec{{margin:56px auto 0}}
.sec-head{{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:18px;flex-wrap:wrap}}
.sec-head h2{{font-size:clamp(20px,2.4vw,28px);font-weight:800;margin:0}}
.sec-head p{{color:var(--mut);font-size:13.5px;margin:0;max-width:560px}}

/* ---------- table shell ---------- */
.tbl{{overflow-x:auto;border-radius:18px;border:1px solid var(--line);background:var(--card);box-shadow:0 10px 30px rgba(32,42,55,.05)}}
table{{border-collapse:separate;border-spacing:0;width:100%;font-size:13.5px}}
th,td{{padding:11px 16px;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}}
td.feat{{text-align:right;font-weight:500}}
td.feat.bold{{font-weight:800;color:var(--ink)}}
thead th{{position:sticky;top:0;z-index:5;background:#fff;font-weight:800;font-size:12.5px}}
tbody tr:last-child td{{border-bottom:none}}
tbody tr:hover td{{background:#fafaff}}
th.feat{{text-align:right}}

/* summary + period columns highlight */
.summ td.c:nth-child(2){{background:#fbfbfe}}
.summ td.c:nth-child(3){{background:#f4f3ff}}
.summ td.c:nth-child(4){{background:#efefff}}
.summ tbody tr:hover td.c{{background:#f2f1ff}}

/* icons & pills */
.chk{{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:7px}}
.chk .ico{{width:14px;height:14px}}
.chk.yes{{background:var(--green-bg);color:var(--green)}}
.chk.no{{background:var(--red-bg);color:var(--red)}}
.pill{{display:inline-block;font-size:11px;font-weight:700;padding:3px 11px;border-radius:999px;white-space:nowrap}}
.pill.inf{{background:var(--green-bg);color:var(--green)}}
.pval{{font-weight:700;font-size:13px}}

/* big comparison table */
table.cmp{{font-size:13.5px;min-width:860px}}
table.cmp th, table.cmp td{{padding:12px 16px}}
tr.grouph td{{
  background:linear-gradient(90deg,rgba(75,69,230,.10),rgba(124,92,252,.06));
  text-align:right;padding:12px 18px;border-bottom:1px solid rgba(75,69,230,.14);
}}
.ghead{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.gname{{font-weight:800;font-size:15px;color:#3730a3;display:flex;align-items:center;gap:8px}}
.gname::before{{content:"";width:8px;height:8px;border-radius:2px;background:var(--brand);transform:rotate(45deg);flex:none}}
.gchip{{display:inline-block;font-size:11px;font-weight:700;padding:3px 11px;border-radius:999px;white-space:nowrap}}
.gchip.price{{background:rgba(75,69,230,.12);color:var(--brand)}}
.gchip.core{{background:#fff;color:var(--mut);border:1px solid var(--line)}}
.gnote{{display:block;font-size:11.5px;color:var(--mut);margin-top:5px;font-weight:400;line-height:1.8}}
td.p-b{{background:#fbfbfe}}
td.p-s{{background:#f4f3ff}}
td.p-p{{background:#efefff}}
tbody tr:hover td.p-b{{background:#f6f6fb}}
tbody tr:hover td.p-s{{background:#efedff}}
tbody tr:hover td.p-p{{background:#e9e8ff}}
b.price{{color:var(--brand);font-size:13.5px;white-space:nowrap}}
.chip.sub{{display:inline-block;font-size:10.5px;font-weight:600;padding:3px 10px;border-radius:999px;background:#eef0ff;color:#4f46c5;white-space:nowrap}}
.chip.tbd{{display:inline-block;font-size:11px;font-weight:700;padding:4px 12px;border-radius:999px;background:var(--amber-bg);color:var(--amber);white-space:nowrap}}
.muted.dash{{opacity:.55}}
td.pl{{min-width:150px}}

/* plugins table */
table.plug td.pl{{text-align:left;min-width:180px}}
table.plug b.price{{color:var(--brand);font-weight:800;font-size:13.5px}}
.plug-grid{{display:grid;grid-template-columns:1.2fr 1fr;gap:22px;align-items:start}}
@media (max-width:900px){{.plug-grid{{grid-template-columns:1fr}}}}

/* policies */
.pols{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;align-items:stretch}}
@media (max-width:900px){{.pols{{grid-template-columns:1fr}}}}
.pol{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px;
  box-shadow:0 6px 20px rgba(32,42,55,.04);display:flex;flex-direction:column}}
.pol__head{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px;flex-wrap:wrap}}
.pol__head h3{{margin:0;font-size:16px;font-weight:800}}
.pol__badge{{display:inline-block;font-size:11px;font-weight:700;padding:4px 12px;border-radius:999px;
  background:rgba(75,69,230,.1);color:var(--brand);white-space:nowrap}}
.pol__body{{margin:0 0 12px;font-size:12.8px;color:var(--body, #737377);line-height:1.9}}
.pol__points{{list-style:none;margin:0;padding:12px 0 0;border-top:1px dashed var(--line);
  display:flex;flex-direction:column;gap:8px}}
.pol__points li{{font-size:12.3px;color:var(--ink);display:flex;align-items:center;gap:8px}}
.pol__points li::before{{content:"";flex:none;width:6px;height:6px;border-radius:50%;background:var(--brand);opacity:.7}}

/* non-standalone chips */
.ns-list{{list-style:none;display:flex;flex-wrap:wrap;gap:10px;margin:0;padding:0}}
.ns-list li{{background:#fff;border:1px solid var(--line);border-radius:999px;
  padding:8px 18px;font-size:13px;font-weight:600}}
.ns-list li::before{{content:"🚫";margin-inline-end:6px;font-size:11px}}

/* decisions */
.dec{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}}
.dec li{{display:flex;align-items:flex-start;gap:12px;background:#fff;border:1px solid var(--line);
  border-radius:12px;padding:13px 18px;font-size:13.5px}}
.dnum{{flex:none;width:26px;height:26px;border-radius:8px;background:rgba(75,69,230,.1);color:var(--brand);
  display:grid;place-items:center;font-weight:800;font-size:13px}}

/* footer */
.foot{{margin:56px auto 80px;text-align:center;color:var(--mut);font-size:12.5px}}
.foot b{{color:var(--ink)}}
@media (max-width:900px){{.plans{{grid-template-columns:1fr}}.pcard.hot{{order:-1}}}}
</style>
</head>
<body>

<header class="phead">
  <span class="kicker">تعرفه و پلن‌ها</span>
  <h1>پلن‌های قیمت‌گذاری منوچ</h1>
  <p>اشتراک دوره‌ای + افزونه‌های ساختاری قابل خرید مستقل — پلن بالاتر یعنی Bundle اقتصادی‌تر همان ماژول‌ها.</p>
</header>

<div class="wrap">
  <div class="model">
    <span class="chip"><b>Plan</b> = پکیج اقتصادی قابلیت‌ها</span>
    <span class="chip"><b>Plugin</b> = امکان شخصی‌سازی پکیج</span>
  </div>
  <section class="plans">
    {CARDS}
  </section>
  <p class="note">قیمت پلن‌ها در هر سه دوره (ماهانه، سه‌ماهه و شش‌ماهه) نهایی شده و مبنای فعلی قیمت‌گذاری منوچ هستند.</p>
</div>

<section class="wrap sec">
  <div class="sec-head">
    <h2>دوره‌های اشتراک</h2>
    <p>اشتراک ماهانه، سه‌ماهه و شش‌ماهه؛ در ساختار فعلی اشتراک سالانه نداریم.</p>
  </div>
  <div class="tbl">
    <table class="summ">
      <thead><tr><th class="feat">پلن</th><th>ماهانه</th><th>سه‌ماهه</th><th>شش‌ماهه</th></tr></thead>
      <tbody>
{period_rows}
      </tbody>
    </table>
  </div>
</section>

<section class="wrap sec">
  <div class="sec-head">
    <h2>نمای کلی پلن‌ها</h2>
    <p>خلاصه قابلیت‌های اصلی در هر پلن؛ جزئیات کامل در ادامه.</p>
  </div>
  <div class="tbl">
    <table class="summ">
      <thead><tr><th class="feat">قابلیت</th><th>پایه</th><th>استاندارد</th><th>پرو</th></tr></thead>
      <tbody>
{sum_rows}
      </tbody>
    </table>
  </div>
</section>

<section class="wrap sec">
  <div class="sec-head">
    <h2>جزئیات ماژول‌ها و قابلیت‌ها</h2>
    <p>قانون کلی: ظرفیت‌ها (Limitها) قیمت مستقل ندارند؛ فقط فیچرهای ساختاری قابل خرید جداگانه‌اند.</p>
  </div>
  <div class="tbl">
    <table class="cmp">
      <thead><tr><th class="feat">قابلیت</th><th>پایه</th><th>استاندارد</th><th>پرو</th><th>قیمت مستقل / ماه</th></tr></thead>
      <tbody>
{MODS}
      </tbody>
    </table>
  </div>
</section>

<section class="wrap sec">
  <div class="sec-head">
    <h2>افزونه‌های ساختاری قابل خرید مستقل</h2>
    <p>هر افزونه یک ماژول کامل است؛ Integrationهای زیرمجموعه‌اش جداگانه فروخته نمی‌شوند.</p>
  </div>
  <div class="plug-grid">
    <div class="tbl">
      <table class="plug">
        <thead><tr><th class="feat">افزونه ساختاری</th><th>قیمت ماهانه</th></tr></thead>
        <tbody>
{plug_rows}
        </tbody>
      </table>
    </div>
    <div>
      <div class="tbl">
        <table class="plug">
          <tbody>
            <tr><td class="feat">مشتری کوچک</td><td class="pl" style="color:var(--mut);font-size:12.5px">با پلن پایه شروع می‌کند</td></tr>
            <tr><td class="feat">مشتری با یک نیاز خاص</td><td class="pl" style="color:var(--mut);font-size:12.5px">همان ماژول را جدا می‌خرد</td></tr>
            <tr><td class="feat">مشتری با چند نیاز حرفه‌ای</td><td class="pl" style="color:var(--mut);font-size:12.5px">به استاندارد یا پرو ارتقا می‌دهد</td></tr>
            <tr><td class="feat">Providerها و Integrationها</td><td class="pl" style="color:var(--mut);font-size:12.5px">جداگانه فروخته نمی‌شوند</td></tr>
          </tbody>
        </table>
      </div>
      <p class="note">در صورت خرید مستقل، نسخه کامل همان ماژول فعال می‌شود؛ نسخه Lite یا Limited نداریم.</p>
    </div>
  </div>
</section>

<section class="wrap sec">
  <div class="sec-head">
    <h2>سیاست‌های مصرف</h2>
    <p>مدل شارژ و مصرف پیامک، AI و Storage.</p>
  </div>
  <div class="pols">
{POLICIES_HTML}
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
</section>

<section class="wrap sec">
  <div class="sec-head">
    <h2>موارد باقی‌مانده برای تصمیم بعدی</h2>
    <p>موارد زیر هنوز در R&amp;D نهایی نشده‌اند.</p>
  </div>
  <ol class="dec">
    {decisions}
  </ol>
</section>

<footer class="wrap foot">
  مدل فعلی: <b>اشتراک ماهانه / سه‌ماهه / شش‌ماهه + افزونه‌های ساختاری + اعتبار پیامک مصرفی</b>
</footer>

</body>
</html>
"""

open('menuch-pricing.html', 'w', encoding='utf-8').write(page)
print("written menuch-pricing.html, length:", len(page))
print("plan cards:", len(cards), "| modules:", len(MODULES), "| summary:", len(SUMMARY), "| plugins:", len(plug_rows), "| policies:", len(pol_cards))
