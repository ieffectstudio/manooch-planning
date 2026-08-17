# Manooch (منوچ) — Marketing Website PRD
**Reference path:** `manooch-planings\landing\landings-prd`
**Version:** 1.0 · **Date:** 2026-08-17 · **Owner:** Effect Studio (استودیو اثر)
**Source of truth:** the six approved HTML mockups — `menuch-landing.html`, `menuch-pricing.html`, `menuch-plans.html`, `menuch-blog.html`, `menuch-article.html`, `menuch-academy.html`

> Scope note: this document specifies **what** must be built — pages, sections, content, states, data, rules and acceptance criteria. It deliberately contains **no implementation logic**: no code, no framework choices, no CSS/JS, no API contracts, no data schemas.

---

## 1. Product Overview

### 1.1 What Manooch is
Manooch is an Iranian SaaS store-builder ("فروشگاه‌ساز") that lets a small or medium business publish an online shop without technical skills, sell products and services, take payments, and retain customers through loyalty and marketing modules.

### 1.2 What this project is
A **public, RTL, Persian-language marketing website** consisting of six page types. Its job is to explain the product, prove credibility, present pricing transparently, and convert visitors into two actions: **starting a plan** and **requesting a consultation**.

### 1.3 Business objectives
| # | Objective | Success measure |
|---|---|---|
| O1 | Generate qualified leads | Consultation form submissions per week |
| O2 | Drive plan starts | Clicks on "شروع کنید" / plan CTAs → signup |
| O3 | Make pricing self-serve and unambiguous | Reduced pre-sale pricing questions to support |
| O4 | Build organic traffic | Indexed blog/academy pages, search impressions |
| O5 | Establish trust | Scroll depth to customers/testimonials, video plays |

### 1.4 Target audience
- **Primary:** Iranian shop owners, wholesalers (بنکدار), workshops, boutiques, and service providers who currently sell via Instagram/messengers and have no website.
- **Secondary:** Businesses already on a legacy site-builder looking to migrate; accountants/ops staff evaluating warehouse + accounting sync.
- **Technical literacy assumption:** low. Copy must stay conversational and jargon-light; English terms only where already established (Excel, SSL, QR Code, Social Marketing, BNPL brand names).

### 1.5 Positioning statement (already reflected in copy)
> «منوچ، دستیار رشد کسب‌وکارت» — رشد کسب‌وکار و نگهداری مشتری، یکجا توی منوچ.

---

## 2. Global Requirements (apply to every page)

### 2.1 Language & direction
- `lang = fa`, `dir = rtl` on every page.
- Entire layout mirrors right-to-left: navigation starts from the right, breadcrumbs read right-to-left, tables place the label column on the right, sidebars sit on the **left** of the content column.
- All numerals rendered as **Persian digits** (۰۱۲۳۴۵۶۷۸۹) with the Persian thousands separator (٬) — e.g. `۱٬۲۹۰٬۰۰۰`.
- Dates use the **Jalali calendar** with Persian month names (e.g. «یکشنبه ۱۲ مرداد ۱۴۰۵»).
- Zero-width non-joiner (نیم‌فاصله) must be preserved in compound words (فروشگاه‌ساز، کسب‌وکار، دسته‌بندی).

### 2.2 Typography
- Primary typeface: **Ravi** (weights 400 / 500 / 600 / 700 / 900).
- Fallback chain: Estedad → Tahoma → generic sans-serif.
- Base body line-height is generous (≈1.8–2.1) — Persian text requires more leading than Latin.
- Headings scale fluidly between mobile and desktop; hero title is the largest type on the site.

### 2.3 Design tokens (single shared palette — must not diverge per page)
| Token | Value | Usage |
|---|---|---|
| Brand | `#4B45E6` | Primary accent, active nav item, links, primary emphasis |
| Ink | `#202A37` | Body text, dark buttons, footer card background |
| Title | `#3D4350` | Section and card headings |
| Body | `#737377` | Paragraph text |
| Muted | `#A2A2A5` / `#A3A9B6` | Meta text, breadcrumbs, disabled |
| Black | `#16161D` | Deepest surfaces |
| Chip black | `#171E27` | Banner countdown chip |
| Line | `#E0E2E7` | Borders, dividers |
| Line soft | `#F2F2F5` | Subtle separators |
| Paper | `#FEFEFE` | Page background |
| Soft | `#FAFAFA` | Alternate surface, text on dark |
| Lavender | `#ECEBFD` | Brand tint background |
| Lavender-2 | `#ACA9F4` | Secondary brand tint |
| Banner grey | `#BABDC1` | Top promo strip |
| Red | `#D80027` | Errors / negative state |
| Radius | `12px` (default), `20px` (large), `29px` (footer card) | Corner rounding |

**Feature-icon accent set** (used across hero cards, feature grid, phone steps): `#4B45E6`, `#10B981`, `#F59E0B`, `#EC4899`, `#0EA5E9`, `#8B5CF6`. Each feature keeps a consistent color across all pages.

### 2.4 Layout system
- Content container max width **1280px**; wide variants **1664px** (bands) and **1920px** (hero).
- Horizontal page padding is fluid: ~16px on mobile up to ~40px (standard) / ~132px (hero) on large screens.
- Vertical rhythm between major sections: **96px** desktop, proportionally reduced on mobile.
- Responsive breakpoints to honor: **1500px, 1200px, 1100px, 1024px, 900px, 760px, 640px, 560px**.

### 2.5 Global promo banner (all pages, top-most element)
| Element | Content | Behavior |
|---|---|---|
| Deal label | «پیشنهاد ویژه» | Brand-colored, fixed width slot |
| Message | «فروشگاه آنلاینت رو با منوچ بساز؛ همین حالا با ۱۴ روز تست رایگان شروع کن» | Truncates with ellipsis rather than wrapping |
| Timer chip | «فقط تا ۳۰ آذر» | Dark chip; **hidden below 560px** |
- Height 60px; the whole strip is content-managed (text + deadline must be editable without a release).
- Below 560px the remaining items center themselves.

### 2.6 Global navigation bar (all pages)
- **Sticky** to the top of the viewport, above all content, with a translucent blurred background and a hairline bottom border.
- Height 80px.
- Right side: Manooch logo (links to home).
- Center-right link set, in this exact order:
  1. منوچ → home
  2. مشتریان → home `#customers`
  3. ویژگی‌ها → home `#features`
  4. تعرفه → pricing page
  5. مقالات → blog index
  6. سوالات متداول → home `#faq`
  7. **آکادمی** → academy page — visually separated by a vertical divider, brand-colored, with a leading icon
- Left side (actions):
  - Trust pill: «مورد اعتمادِ ۳٬۰۰۰+ کسب‌وکار» with a shield icon on a brand-tinted background. Static, non-clickable.
  - Primary dark button: «شروع کنید» → pricing/signup. Lifts slightly on hover.
- **Active-state rule:** the nav item corresponding to the current page is brand-colored (تعرفه on pricing/plans, مقالات on blog/article, آکادمی on academy).
- **Mobile requirement:** below 900px the link list must collapse into a drawer/menu pattern; the trust pill may be hidden, but the «شروع کنید» button must remain visible at all times.

### 2.7 Global footer (all pages)
Dark rounded card (radius 29px), minimum height ~496px, containing four columns:
1. **Brand column** — logo, contact block («ایمیل: info@manooch.ir», «مشاوره: 0938 025 2088»), and five social icons (Instagram, Telegram, YouTube, LinkedIn, Facebook).
2. **دسترسی سریع** — چرا منوچ؟ / مشتریان ما / ویژگی‌ها / پلن های ما / سوالات متداول / درخواست مشاوره.
3. **مقالات** — چرا منوچ رو باید داشته باشیم / منوچ مناسب چه کسب‌وکاریه؟ / بنکدارا خیالشون راحت باشه / واحد فروش پیشرفته.
4. **نمادها** — trust badges (نماد اعتماد, زرین‌پال).

Bottom bar (two lines / two sides): «تمامی حقوق برای استودیو اثر محفوظ است.» and «All rights are reserved | Effect Studio 2025».

**Requirement:** the email address must be delivered as a real, clickable `mailto:` link on every page — the landing mockup currently renders it through an email-obfuscation placeholder and must be normalized.

### 2.8 Cross-page linking map
| From | To |
|---|---|
| Landing `#plans` → «مشاهده بیشتر» | Pricing page |
| Landing `#academy` → «مشاهده همه» | Academy page |
| Landing `#blog` → «مشاهده همه» | Blog index |
| Blog card / featured → «مشاهده مقاله» | Article page |
| Article breadcrumb | Home → Blog → current article |
| Academy breadcrumb | Home → Academy |
| Academy sidebar CTAs | Pricing page, Home `#contact` |
| Pricing ↔ Plans | Both reachable from تعرفه; Plans is the deep comparison view |

### 2.9 Accessibility requirements
- All interactive controls reachable and operable by keyboard, with a visible focus indicator.
- Every image carries meaningful Persian alt text; decorative shapes are hidden from assistive technology.
- Icon-only buttons (video play, pagination arrows, share, socials) carry descriptive Persian labels.
- FAQ accordions and comment forms announce their expanded/collapsed state.
- Color contrast: body text on paper and white text on the hero gradient must both pass WCAG AA.
- **Reduced-motion:** when the user requests reduced motion, all marquees, auto-scrolling card tracks, parallax glow and fade-up entrances must stop or become instant.

### 2.10 Performance & delivery requirements
- Fonts must be served as optimized web fonts with swap behavior; the current mockups embed multi-hundred-kilobyte base64 fonts inline — this must **not** ship. Target: font payload served once, cached, subset to Persian + Latin.
- Images must be responsive and lazy-loaded below the fold; hero/first-fold media loads eagerly.
- Target: Largest Contentful Paint under 2.5s on a mid-range Android over 3G-fast in Iran; total initial payload for the landing page under 1.5MB including hero media.
- Videos are poster-image first; no autoplay of sound. Media only loads on user intent.

### 2.11 SEO requirements
- Unique title and meta description per page. Approved titles:
  - Landing: «منوچ — دستیار رشد کسب‌وکارت»
  - Pricing: «تعرفه‌های منوچ — پلن‌ها و افزونه‌ها»
  - Plans: «پلن‌های منوچ — مقایسه کامل تعرفه‌ها»
  - Blog: «مقالات کاربردی — منوچ»
  - Article: «{عنوان مقاله} — مقالات منوچ»
  - Academy: «آکادمی منوچ — آموزش‌های قدم‌به‌قدم»
- Exactly one H1 per page; heading levels never skip.
- Human-readable Persian-slug or transliterated URLs for articles and academy videos.
- Structured data required for: Organization, Product/Offer (pricing), Article (blog post), VideoObject (academy), FAQPage (landing FAQ), BreadcrumbList.
- Canonical URLs, Open Graph and Twitter card images per page.
- XML sitemap covering all static pages plus every article and academy video.

### 2.12 Analytics requirements (events to capture)
Banner click · nav CTA click · hero primary CTA («درخواست مشاوره») · hero secondary CTA («با ۶۹۰ هزار تومان شروع کن») · hero video play · feature "show more" expand · plan period toggle (with selected period) · plan CTA click (with plan name) · testimonial reel play · academy video play · blog search query · blog category filter · article scroll depth 25/50/75/100 · article share (per channel) · comment submitted · consultation form submitted (and per-field abandonment) · footer link clicks.

### 2.13 Content management requirements
The following must be editable by a non-developer without a release: promo banner text and deadline, hero stats, customer logos list, feature cards, plan names/prices/feature bullets, add-on prices, testimonials, academy videos, blog posts, FAQ items, footer links and contact details.

---

## 3. Page 1 — Landing / Home (`menuch-landing.html`)

**Purpose:** the primary conversion page. Explains the product end to end and funnels to plan start or consultation.
**Anchors that must exist:** `#customers`, `#app`, `#features`, `#plans`, `#testimonials`, `#academy`, `#blog`, `#faq`, `#contact`.
**Section order is fixed** and must not be rearranged without approval.

### 3.1 Hero
- Full-bleed **dark violet gradient** stage (deep indigo → violet → blue) with four soft glowing orbs layered on top.
- Orbs drift subtly toward the pointer position (a slow, damped parallax). This is decorative and must be disabled under reduced-motion.
- Three-column composition on desktop:
  - **Right column:** a vertical, continuously auto-scrolling track of translucent glass feature cards (scrolling upward).
  - **Center column:** the message stack.
  - **Left column:** a second vertical auto-scrolling track (opposite direction feel).
- Card tracks loop seamlessly (content is duplicated so there is no visible seam), pause on hover, and freeze under reduced-motion.
- Below ~1024px the side tracks collapse away (or convert to a single horizontal marquee) and the center column becomes full width.

**Center content (exact copy):**
| Element | Copy |
|---|---|
| H1 | منوچ، دستیار رشد کسب‌وکارت |
| Subtitle | رشد کسب‌وکار و نگهداری مشتری، یکجا توی منوچ |
| Description | فروشگاهت رو می‌سازی، مشتری‌هات رو نگه می‌داری و بدون اضافه‌کردن نیرو بیشتر می‌فروشی؛ منوچ ابزار فروش، بازاریابی و وفادارسازی رو یکجا در اختیارت می‌ذاره. |
| Primary CTA | درخواست مشاوره → `#contact` |
| Secondary CTA | با ۶۹۰ هزار تومان شروع کن → `#plans` |

**Stat row (4 items):** ۱۴ روز / تست رایگان · میلیاردها تومان / درآمد ماهانه · ۳٬۰۰۰+ / سایت ساخته شده با منوچ · ۹۹٪ / رضایت فروشنده‌ها.

**Hero video:** a rounded 16:9 poster with a large centered play affordance and a thin progress bar. Clicking plays the intro video (modal or inline — must not navigate away).

**Right-track cards:** کالاها · خدمات · دسته‌بندی · ویژگی‌ها · ویس محصول · ورودی با اکسل · گالری · محصولات ارزی · QR Code · شخصی‌سازی.
**Left-track cards:** درگاه پرداخت · کارت‌به‌کارت · فروش اقساطی · تخفیف · نظرات · فروش حضوری · انبار · گزارش فروش · Social Marketing · اتصال حسابداری · باشگاه مشتریان.
Each card = colored icon + title + one-line descriptor.

### 3.2 Customers band (`#customers`)
- A single horizontal, infinitely looping marquee of customer cards, moving right-to-left, seamless (set is duplicated), **paused on hover**.
- Card: 316×194, colored gradient header holding the customer logo, white body with the customer name and a «مشاهده لینک» link with a leading icon. Lifts on hover.
- Seed set with their header gradients:
  | Customer | Gradient |
  |---|---|
  | تپسی | `#FFBE8D → #E36A0E` |
  | اسنپ | `#8DFF91 → #278809` |
  | شرکت لیمو هاست | `#F9FF8D → #758809` |
  | تولید و پخش یگانه | `#8DD3FF → #094088` |
  | استودیو اثر | `#B38DFF → #6F0988` |
  | بدلیجات تاج محل | `#8DFFC4 → #098816` |
- Duplicated cards must be hidden from assistive technology.

### 3.3 App showcase (`#app`)
Two-column: text on one side, a realistic phone mockup on the other, on a soft halo.

- Kicker: «اپلیکیشن فروشگاهت تو جیبته»
- H2: «قابلیت‌هایی که فروشت رو حرفه‌ای می‌کنه»
- Subtitle: «از فروش اقساطی تا اتصال حسابداری — همه‌چیز یکجا توی منوچ، توی جیبت.»
- **Numbered steps (order matters, each with its own accent color):**
  1. `#0EA5E9` **فروش اقساطی** — با اسنپ‌پی، ترب‌پی و دیجی‌پی؛ مشتری قسطی می‌خره، تو نقدی می‌گیری.
  2. `#4B45E6` **اتصال به حسابداری** — همگام‌سازی خودکار کالا و موجودی با نرم‌افزار حسابداریت.
  3. `#F59E0B` **افزودن محصولات ارزی** — قیمت‌گذاری و فروش محصولات ارزی مستقیم توی فروشگاهت.
  4. `#10B981` **سرویس خدمات** — علاوه بر کالا، خدماتت رو هم تعریف کن و بفروش.
- CTA: «شروع راه‌اندازی فروشگاه».
- **Phone mockup content (a designed illustration of the product, not a live app):** status bar «۹:۴۱ / 5G»; shop header «بوتیک نگار — فروشگاه آنلاین • فعال» with avatar and bell; a search field placeholder «جستجوی محصول…»; a 2×2 product grid — کراپ تاپ سفید ۲۴۹ هزار تومان، کیف چرم عسلی ۴۲۰ هزار تومان، ساعت مینیمال ۸۹۰ هزار تومان، شال ابریشم ۱۸۵ هزار تومان; a booking confirmation row «نوبت فردا ساعت ۵ — رزرو شد ✓»; a payment row «پرداخت امن — درگاه پرداخت منوچ / ادامه ←»; a bottom tab bar with a floating action button.
- The whole mockup is decorative and hidden from assistive technology.

### 3.4 Features grid (`#features`)
- Heading: «ویژگی‌های پلتفرم منوچ» / «همه ابزارهایی که برای راه‌اندازی و رشد فروشگاهت لازم داری، یکجا توی منوچ».
- 3-column grid of icon + title + description cards; 2 columns on tablet, 1 on mobile.
- **Progressive disclosure:** only the first **9** cards are visible initially. A centered «مشاهده بیشتر» control reveals the remaining cards with a staggered fade-up and relabels itself «مشاهده کمتر». Collapsing scrolls the user back to the top of the section.
- The control must expose its expanded/collapsed state to assistive technology.

**First 9 (always visible):** کالاها · خدمات · محصولات ارزی · دسته‌بندی · ویژگی‌ها · ورودی با اکسل · کارت‌به‌کارت · گالری · سوالات پرتکرار.
**Revealed on expand:** آدرس و مسیریابی · تیکت پشتیبانی · همگام‌سازی با بله · دامنه اختصاصی · درگاه پرداخت · شخصی‌سازی · QR Code · واحد فروش پیشرفته · انبار · فروش حضوری · فروش اقساطی · تخفیف · نظرات · گزارش فروش · Social Marketing · اتصال حسابداری · باشگاه مشتریان.

### 3.5 Plans teaser (`#plans`)
- Heading: «پلن های منوچ» / «اشتراک ماهانه، سه‌ماهه و شش‌ماهه + افزونه‌های ساختاری مستقل — پلن بالاتر یعنی باندل اقتصادی‌تر همان ماژول‌ها».
- **Period toggle** with three options: ماهانه (default) · سه ماهه · شش ماهه. Selecting a period updates every card's price **and** the period caption underneath it, in place, with no page reload.
- Three plan cards, 405px wide each, centered, equal height. The middle card («پلن استاندارد») is highlighted with a brand border and a «پیشنهاد منوچ» badge.
- Each card: plan name · one-line description · price (amount + «تومان» + period label) · grouped feature list where each row is marked included or excluded · full-width CTA.
- **Prices (must match the pricing pages exactly):**
  | Plan | ماهانه | سه‌ماهه | شش‌ماهه |
  |---|---|---|---|
  | پلن پایه | ۶۹۰٬۰۰۰ | ۱٬۹۶۰٬۰۰۰ | ۳٬۷۹۰٬۰۰۰ |
  | پلن استاندارد | ۱٬۲۹۰٬۰۰۰ | ۳٬۶۶۰٬۰۰۰ | ۷٬۰۹۰٬۰۰۰ |
  | پلن پرو | ۲٬۴۹۰٬۰۰۰ | ۷٬۰۷۰٬۰۰۰ | ۱۳٬۶۹۰٬۰۰۰ |
- **Card bullet groups:**
  - *پایه — «فروشگاه و محصول»:* ۱۰۰ محصول فعال، ۲ عکس برای هر محصول، افزودن کالا و خدمات، دسته‌بندی، ویژگی محصول، دامنه اختصاصی + SSL، ✗ ویس محصول. *«فروش و پرداخت»:* سبد خرید و مدیریت سفارش، پرداخت آنلاین (زرین‌پال، زیبال، بانکی)، پرداخت در محل + کارت‌به‌کارت، دفترچه مشتریان و تاریخچه خرید، محتوا (بنر، گالری، سوالات متداول). *«رشد و اتوماسیون» (all excluded):* واحد فروش پیشرفته، انبار و ورود با Excel، فروش اقساطی، باشگاه مشتریان.
  - *استاندارد — «همه امکانات پایه، به‌علاوه»:* ۱٬۰۰۰ محصول فعال، ۳ عکس + ویس محصول، حذف پس‌زمینه + توضیحات با هوش مصنوعی، واحد فروش پیشرفته، انبار + ورود اطلاعات با Excel، لینک پرداخت + پرداخت توافقی، فروش حضوری. *«بازاریابی و گزارش»:* تخفیف و نظرات مشتریان، گزارش فروش کامل، Social Marketing. *«فقط در پلن پرو» (excluded):* محصولات ارزی، فروش اقساطی، اتصال حسابداری، باشگاه مشتریان.
  - *پرو — «همه امکانات استاندارد، به‌علاوه»:* محصولات نامحدود + ۵ عکس، محصولات ارزی، فروش اقساطی (اسنپ‌پی، ترب‌پی، دیجی‌پی)، اتصال حسابداری. *«باشگاه مشتریان کامل»:* امتیاز، سطح‌بندی و کمپین، SMS Marketing و پیامک گروهی، گزارش باشگاه.
- CTAs: «شروع با پلن پایه» / «شروع با پلن استاندارد» / «شروع با پلن پرو».
- Below the row, a centered «مشاهده بیشتر» link to the full pricing page.

### 3.6 Testimonial reels (`#testimonials`)
- Full-width band with its own background treatment.
- Kicker «تجربه‌ها»; H2 «مشتریان پس از استفاده از منوچ چه تجربه‌ای دارند؟»; subtitle «تجربه‌های واقعی کسب‌وکارها — کوتاه، صادقانه، از دل مغازه و کارگاه»; a «همه تجربه‌ها» link.
- A row of four vertical video reels. Each reel: portrait thumbnail, duration chip, centered play button with a descriptive label, and a pull-quote overlay.
  | Person | Duration | Quote |
  |---|---|---|
  | نگار محمدی | ۰۰:۴۵ | «اولین هفته فروشم دو برابر شد؛ مشتری‌ها خودشون نوبت می‌گیرن!» |
  | امیر رضایی | ۰۱:۱۲ | «سفارش‌ها مستقیم از فروشگاهم می‌آد — دیگه واسطه ندارم» |
  | حسین کریمی | ۰۰:۵۸ | «نوبت‌گیری خودکار منوچ زندگیمو نجات داد» |
  | سارا احمدی | ۰۲:۰۵ | «بدون یک خط کد فروشگاهم راه افتاد؛ مشتری عاشقشه» |
- On mobile the row becomes a horizontally swipeable carousel with snap points.

### 3.7 Academy teaser (`#academy`)
- Heading: «آکادمی منوچ» / «آموزش‌های قدم‌به‌قدم تا با منوچ حرفه‌ای کار کنی و بیشتر بفروشی».
- Layout: one large featured video (768px), a column of three small thumbnails (240px), and a «مشاهده همه» panel (224px) linking to the Academy page.
- Featured video overlay: badge «آموزش رایگان» + title «راه‌اندازی فروشگاه در ۱۰ دقیقه».

### 3.8 Blog teaser (`#blog`)
- Heading: «مقالات کاربردی» / «نکته‌ها و راهنمایی‌های کاربردی برای فروش آنلاین».
- Row of four post cards (240px) plus a «مشاهده همه» panel (224px) linking to the blog index.
- Card: cover image (240:183) · title · one-line excerpt · meta line «۱۲:۳۰ | یکشنبه ۱۲ مرداد ۱۴۰۵» · «مشاهده مقاله» link with icon. Card lifts on hover.
- Seed posts: چرا وبسایت دردسر داره؟ · سئو چقدر مهمه؟ · چرا سایت‌سازها؟ · فروش چجوری انجام می‌شه؟

### 3.9 FAQ (`#faq`)
- Preceded by a horizontal divider.
- Heading: «سوالات متداول» / «پاسخ سوال‌هایی که بیشتر از همه از ما می‌پرسید».
- Accordion rows; the **first row is open by default**; each row has a chevron that rotates on open. Multiple rows may be open simultaneously.
- Seed items:
  1. «منوچ چطور به فروش بیشترم کمک می‌کنه؟» → «منوچ مثل یه شاگرد فروش همیشه‌بیدار کنار شماست؛ محصولاتتون رو معرفی می‌کنه، با مشتری گفت‌وگو می‌کنه، نوبت می‌گیره و فروش رو تا انتها پیگیری می‌کنه.»
  2. «راه‌اندازی فروشگاه چقدر زمان می‌بره؟» → «با چند کلیک و در کمتر از یک روز فروشگاهت آنلاین می‌شه؛ حتی بدون دانش فنی.»
  3. «پلن‌ها و قیمت‌ها چطوریه؟» → «سه پلن با دوره‌های ماهانه، سه‌ماهه و شش‌ماهه داریم؛ ۱۴ روز تست رایگان و افزونه‌هایی که می‌تونی جداگانه بخری.»
  4. «اگه به مشکل خوردم چیکار کنم؟» → «تیم پشتیبانی از ۸ صبح تا ۱۰ شب همراهته و از طریق تیکت پاسخگوت هستیم.»

### 3.10 Consultation (`#contact`)
Two-column: information (768px) + form (464px).

- H2 «درخواست مشاوره»; body «تیم ما همه‌روزه از ساعت ۸ صبح تا ۱۰ شب پاسخگوست؛ درخواستت رو ثبت کن تا حداکثر ۴ ساعت بعد باهات تماس بگیریم.»; a team photo.
- **Form fields (in order):**
  | Label | Type | Placeholder | Required |
  |---|---|---|---|
  | نام و نام خانوادگی | text | محمد گندمی | Yes |
  | شماره تماس | tel | ۰۹۱۵ | Yes |
  | کسب و کار | text | مبلمان | No |
  | توضیحات | textarea | من نیاز به مشاوره دارم | No |
- Submit: «ثبت درخواست مشاوره».
- **Required behaviors:** inline per-field validation with Persian error messages; Iranian mobile-number format validation; numeric input accepts both Persian and Latin digits; a loading state on submit; a clear success confirmation replacing or following the form; a distinct failure message with a retry path; spam protection; no double submission.

### 3.11 Landing acceptance criteria
- All ten sections render in the specified order with working anchor navigation from the nav bar and footer.
- Feature "show more" toggles both content and label, and restores scroll position on collapse.
- Plan period toggle updates all three cards' prices and period captions consistently.
- Both marquees loop without a visible seam and pause on hover.
- All motion halts under reduced-motion preference.
- Layout is intact and legible at 360px, 768px, 1024px, 1440px and 1920px widths.

---

## 4. Page 2 — Pricing (`menuch-pricing.html`)

**Purpose:** the public, marketing-facing pricing page — the destination of «تعرفه» and every «مشاهده بیشتر» pricing link.

> **Gap to close:** the current mockup for this page renders **without the global banner, nav bar and footer**. The shipped page **must** include all three global shells.

### 4.1 Page header
- Kicker «تعرفه و پلن‌ها»; H1 «پلن‌های قیمت‌گذاری منوچ»; subtitle «اشتراک دوره‌ای + افزونه‌های ساختاری قابل خرید مستقل — پلن بالاتر یعنی Bundle اقتصادی‌تر همان ماژول‌ها.»

### 4.2 Pricing model explainer
Two chips stating the mental model:
- **Plan** = پکیج اقتصادی قابلیت‌ها
- **Plugin** = امکان شخصی‌سازی پکیج

### 4.3 Plan cards
Three cards — پایه / استاندارد (highlighted, badge «پیشنهاد منوچ») / پرو (dark treatment) — each with tagline, monthly price + «تومان / ماه», and CTA («شروع با پایه» / «شروع با استاندارد» / «شروع با پرو»).
Taglines: شروع فروش آنلاین · مدیریت حرفه‌ای فروش · رشد، اتوماسیون و وفادارسازی.
Footnote: «قیمت پلن‌ها در هر سه دوره (ماهانه، سه‌ماهه و شش‌ماهه) نهایی شده و مبنای فعلی قیمت‌گذاری منوچ هستند.»

### 4.4 Subscription periods table
- Heading «دوره‌های اشتراک» / «اشتراک ماهانه، سه‌ماهه و شش‌ماهه؛ در ساختار فعلی اشتراک سالانه نداریم.»
- Columns: پلن | ماهانه | سه‌ماهه | شش‌ماهه — populated with the price matrix from §3.5.

### 4.5 Plan overview table
Heading «نمای کلی پلن‌ها» / «خلاصه قابلیت‌های اصلی در هر پلن؛ جزئیات کامل در ادامه.»
Rows (پایه | استاندارد | پرو):

| Row | پایه | استاندارد | پرو |
|---|---|---|---|
| قیمت ماهانه | ۶۹۰٬۰۰۰ | ۱٬۲۹۰٬۰۰۰ | ۲٬۴۹۰٬۰۰۰ |
| قیمت سه‌ماهه | ۱٬۹۶۰٬۰۰۰ | ۳٬۶۶۰٬۰۰۰ | ۷٬۰۷۰٬۰۰۰ |
| قیمت شش‌ماهه | ۳٬۷۹۰٬۰۰۰ | ۷٬۰۹۰٬۰۰۰ | ۱۳٬۶۹۰٬۰۰۰ |
| تعداد محصول | ۱۰۰ | ۱٬۰۰۰ | نامحدود |
| عکس هر محصول | ۲ | ۳ | ۵ |
| ویس محصول | ✗ | ✓ | ✓ |
| افزودن کالا | ✓ | ✓ | ✓ |
| افزودن خدمات | ✓ | ✓ | ✓ |
| محصولات ارزی | ✗ | ✗ | ✓ |
| ویژگی محصول | ✓ | ✓ | ✓ |
| حذف پس‌زمینه | ✗ | ✓ | ✓ |
| توضیحات کالا با AI | ✗ | ✓ | ✓ |
| واحد فروش پیشرفته | ✗ | ✓ | ✓ |
| انبار | ✗ | ✓ | ✓ |
| Excel | ✗ | ✓ | ✓ |
| نوع پرداخت | ✓ | ✓ | ✓ |
| فروش حضوری | ✗ | ✓ | ✓ |
| فروش اقساطی | ✗ | ✗ | ✓ |
| تخفیف | ✗ | ✓ | ✓ |
| محتوا | ✓ | ✓ | ✓ |
| Notification | ✓ | ✓ | ✓ |
| نظرات | ✗ | ✓ | ✓ |
| گزارش فروش | ✗ | ✓ | ✓ |
| Social Marketing | ✗ | ✓ | ✓ |
| اتصال حسابداری | ✗ | ✗ | ✓ |
| باشگاه مشتریان | ✗ | ✗ | ✓ |

### 4.6 Full module & capability table
Heading «جزئیات ماژول‌ها و قابلیت‌ها» / «قانون کلی: ظرفیت‌ها (Limitها) قیمت مستقل ندارند؛ فقط فیچرهای ساختاری قابل خرید جداگانه‌اند.»
Columns: قابلیت | پایه | استاندارد | پرو | **قیمت مستقل / ماه**.
The table is grouped; each group header shows a group name, a classification chip, and an optional clarification note. Full contents are specified once in **§5.3** (the Plans page uses the identical table) and must not diverge between the two pages.

### 4.7 Structural add-ons (افزونه‌های ساختاری قابل خرید مستقل)
Heading + subtitle «هر افزونه یک ماژول کامل است؛ Integrationهای زیرمجموعه‌اش جداگانه فروخته نمی‌شوند.»

| Add-on | Monthly price (تومان) |
|---|---|
| واحد فروش پیشرفته | ۲۹۰٬۰۰۰ |
| انبار | ۲۹۰٬۰۰۰ |
| فروش حضوری | ۱۹۰٬۰۰۰ |
| فروش اقساطی | ۳۹۰٬۰۰۰ |
| تخفیف | ۹۹٬۰۰۰ |
| نظرات | ۷۹٬۰۰۰ |
| گزارش فروش | ۱۹۰٬۰۰۰ |
| Social Marketing | ۳۹۰٬۰۰۰ |
| اتصال حسابداری | ۲۹۰٬۰۰۰ |
| باشگاه مشتریان | ۶۹۰٬۰۰۰ |

Adjacent guidance panel:
- مشتری کوچک → با پلن پایه شروع می‌کند
- مشتری با یک نیاز خاص → همان ماژول را جدا می‌خرد
- مشتری با چند نیاز حرفه‌ای → به استاندارد یا پرو ارتقا می‌دهد
- Providerها و Integrationها → جداگانه فروخته نمی‌شوند

Note: «در صورت خرید مستقل، نسخه کامل همان ماژول فعال می‌شود؛ نسخه Lite یا Limited نداریم.»

### 4.8 Consumption policies (سیاست‌های مصرف)
Three policy cards, each with a title, a badge, a paragraph, and bullet points:

| Policy | Badge | Key points |
|---|---|---|
| سیاست اعتبار پیامک | هر پیامک ۳۲۰ تومان | قیمت هر پیامک: ۳۲۰ تومان · پلن پرو = پیامک نامحدود نیست · هزینه ارسال از اعتبار شارژشده کسر می‌شود |
| سیاست AI | بدون Token فروشی | سیستم Token فروشی تعریف نشده · کیف پول AI جداگانه تعریف نشده · محدودیت مصرف AI جداگانه لحاظ نشده |
| سیاست Storage | بدون Limit جداگانه | افزونه مستقل نیست · قیمت مستقل ندارد · در جدول قیمت‌گذاری تفکیک نمی‌شود |

Body text for each is fixed as written in the mockup and must be reproduced verbatim.

### 4.9 Explicitly not add-ons (مواردی که افزونه مستقل نیستند)
Subtitle: «این موارد فقط برای تفکیک پلن‌ها هستند و قیمت جداگانه ندارند.»
List: تعداد محصول · تعداد عکس · ویس محصول · ویژگی محصول · رنگ · سایز · محصولات ارزی · Excel · Notification · حذف پس‌زمینه · تولید توضیحات با AI · Providerهای پرداخت آنلاین · Providerهای فروش اقساطی · Connectorهای Social Marketing · Providerهای حسابداری · زیرقابلیت‌های باشگاه مشتریان · Storage.

### 4.10 Open decisions (موارد باقی‌مانده برای تصمیم بعدی)
Subtitle «موارد زیر هنوز در R&D نهایی نشده‌اند.» — numbered list:
1. بررسی نهایی اقتصاد افزونه‌ها در برابر Upgrade پلن
2. تعیین مبلغ بسته‌های شارژ اعتبار پیامک
3. بررسی نحوه نمایش «صرفه‌جویی» دوره سه‌ماهه و شش‌ماهه در صفحه Pricing

> **Product decision required:** this block is internal R&D content. Decide before launch whether it is removed from the public page or moved to an internal document. Default recommendation: **remove from the public site.**

### 4.11 Page footer strip
«مدل فعلی: اشتراک ماهانه / سه‌ماهه / شش‌ماهه + افزونه‌های ساختاری + اعتبار پیامک مصرفی» — then the global footer.

### 4.12 Pricing acceptance criteria
- Global banner, nav (with تعرفه active) and footer are present.
- Every price on this page matches the landing teaser and the Plans page — a single source of truth.
- All tables are horizontally scrollable on narrow screens with the label column remaining readable, and never break the page layout.
- Included/excluded markers are distinguishable without relying on color alone.

---

## 5. Page 3 — Plans / Full comparison (`menuch-plans.html`)

**Purpose:** the deep, exhaustive comparison view for evaluators who want every row. Reachable from the nav «تعرفه» and from the pricing page.

### 5.1 Shell and header
- Full global banner + nav (تعرفه active) + footer — already present in the mockup.
- Kicker «تعرفه و پلن‌ها»; H1 «پلن‌های منوچ»; subtitle «اشتراک ماهانه، سه‌ماهه و شش‌ماهه + افزونه‌های ساختاری قابل خرید مستقل — پلن بالاتر یعنی باندل اقتصادی‌تر همان ماژول‌ها.»

### 5.2 Period tabs
- Three tabs: ماهانه (default active) · سه ماهه · شش ماهه.
- **Behavior:** selecting a tab **highlights the corresponding column** in the period summary table. It does not hide the other columns; all three remain visible for comparison.
- Section «نمای کلی پلن‌ها» / «خلاصه قابلیت‌های اصلی در هر پلن؛ جزئیات کامل در جدول پایین.» with the same price matrix as §3.5.

### 5.3 Master comparison table (canonical dataset)
Heading «جزئیات ماژول‌ها و قابلیت‌ها» / «ظرفیت‌ها (Limitها) قیمت مستقل ندارند؛ فقط فیچرهای ساختاری قابل خرید جداگانه‌اند.»
Columns: قابلیت | پایه | استاندارد | پرو | قیمت مستقل / ماه.
Group header rows carry: group name, a classification chip (`افزونه نیست` / `هسته محصول` / `در همه پلن‌ها` / `در پلن‌ها` / `افزونه مستقل`), and an optional note. Sub-rows of a paid module show «همراه ماژول» in the price column.

**Group 1 — ظرفیت‌های پلن** `[افزونه نیست]`
*Note:* ظرفیت‌ها فقط برای تفکیک پلن‌ها استفاده می‌شوند و قیمت مستقل ندارند. سیاست یا محدودیت جداگانه‌ای برای Storage تعریف نشده است.
| قابلیت | پایه | استاندارد | پرو | قیمت |
|---|---|---|---|---|
| تعداد محصول فعال | ۱۰۰ | ۱٬۰۰۰ | نامحدود | — |
| تعداد عکس هر محصول | ۲ | ۳ | ۵ | — |
| ویس محصول | ✗ | ✓ | ✓ | — |

**Group 2 — انواع قابل افزودن** `[هسته محصول]`
*Note:* محصولات ارزی فقط در پلن پرو فعال است و روی پایه یا استاندارد جداگانه خریداری نمی‌شود. چیزی با عنوان «فایل دیجیتال» نداریم.
افزودن کالا ✓✓✓ — · افزودن خدمات ✓✓✓ — · افزودن محصولات ارزی ✗✗✓ —

**Group 3 — افزودن کالا** `[هسته محصول]`
*Note:* «حذف پس‌زمینه» و «تولید توضیحات با AI» زیرمجموعه افزودن کالا هستند و افزونه ساختاری مستقل نیستند.
افزودن کالا ✓✓✓ · افزودن تصویر کالا ✓✓✓ · ویژگی کالا ✓✓✓ · قیمت‌گذاری کالا ✓✓✓ · فعال/غیرفعال کردن کالا ✓✓✓ · ویس محصول ✗✓✓ · حذف پس‌زمینه تصویر کالا ✗✓✓ · تولید توضیحات کالا با هوش مصنوعی ✗✓✓ — all price «—»

**Group 4 — فروشگاه و کاتالوگ** `[در همه پلن‌ها]`
*Note:* چیزی با عنوان «زیردسته‌بندی» یا «چینش بخش‌های فروشگاه» نداریم.
ساخت فروشگاه اینترنتی · ساب‌دامنه منوچ · دامنه اختصاصی · SSL · شخصی‌سازی رنگ و فونت · لینکدونی · دسته‌بندی · قیمت‌گذاری ساده · قیمت استعلامی · فعال/غیرفعال کردن محصول — all ✓✓✓, price «—»

**Group 5 — ویژگی محصول** `[افزونه نیست]`
*Note:* ویژگی بخشی از هسته محصول است و از پلن پایه فعال است.
ویژگی محصول · رنگ · سایز · مشخصات · تعریف مقادیر ویژگی — all ✓✓✓, price «—»

**Group 6 — واحد فروش پیشرفته** `[افزونه مستقل]` — **۲۹۰٬۰۰۰**
*Note:* ماژول مستقل و متفاوت از «ویژگی محصول» است.
واحد فروش پیشرفته ✗✓✓ ۲۹۰٬۰۰۰ · تعریف واحدهای فروش · قیمت هر واحد · موجودی هر واحد · حداقل سفارش هر واحد — ✗✓✓، «همراه ماژول»

**Group 7 — انبار** `[افزونه مستقل]` — **۲۹۰٬۰۰۰**
*Note:* Excel فیچر مستقل نیست و کاملاً زیرمجموعه انبار است؛ با فعال‌شدن انبار، قابلیت‌های Excel مربوط به آن نیز فعال می‌شوند.
انبار ✗✓✓ ۲۹۰٬۰۰۰ · مدیریت موجودی · هشدار کمبود موجودی · مدیریت موجودی کالاها · ورود گروهی با Excel · Import موجودی با Excel · Import قیمت با Excel · Export اطلاعات — ✗✓✓، «همراه ماژول»

**Group 8 — نوع پرداخت / روش‌های پرداخت** `[در پلن‌ها]`
*Note:* زرین‌پال، زیبال، درگاه‌های بانکی و سایر Gatewayها زیرمجموعه پرداخت آنلاین هستند و جداگانه قیمت‌گذاری نمی‌شوند.
پرداخت آنلاین ✓✓✓ · پرداخت در محل ✓✓✓ · کارت‌به‌کارت / آپلود فیش ✓✓✓ · پرداخت توافقی / چکی ✗✓✓ · لینک پرداخت ✗✓✓ · پرداخت اعتباری / اقساطی ✗✗✓ — all price «—»

**Group 9 — فروش اقساطی** `[افزونه مستقل]` — **۳۹۰٬۰۰۰**
*Note:* Providerهای BNPL (اسنپ‌پی، ترب‌پی، دیجی‌پی و…) زیرمجموعه این ماژول هستند و جداگانه فروخته نمی‌شوند.
فروش اقساطی ✗✗✓ ۳۹۰٬۰۰۰ · اسنپ‌پی · ترب‌پی · دیجی‌پی · سایر سرویس‌های اعتباری — ✗✗✓، «همراه ماژول»

**Group 10 — فروش حضوری** `[افزونه مستقل]` — **۱۹۰٬۰۰۰**
فروش حضوری ✗✓✓ ۱۹۰٬۰۰۰ · انتخاب مشتری · افزودن کالا · ثبت فروش · ثبت سفارش پرداخت‌شده · آمار فروش روزانه — ✗✓✓، «همراه ماژول»

**Group 11 — تخفیف** `[افزونه مستقل]` — **۹۹٬۰۰۰**
تخفیف ✗✓✓ ۹۹٬۰۰۰ · تخفیف درصدی · تخفیف مبلغی · تخفیف محصول · تخفیف دسته‌بندی · تخفیف مشتری — ✗✓✓، «همراه ماژول»

**Group 12 — مشتریان** `[در همه پلن‌ها]`
دفترچه مشتریان · پروفایل مشتری · تاریخچه خرید · جستجوی مشتری — ✓✓✓، «—»

**Group 13 — محتوا** `[در همه پلن‌ها]`
*Note:* Notification زیرمجموعه محتواست؛ محتوا در ساختار فعلی افزونه مستقل قیمت‌دار در نظر گرفته نمی‌شود.
محتوا · Banner · Gallery · FAQ · Team · Bank Cards · Notification — ✓✓✓، «—»

**Group 14 — نظرات** `[افزونه مستقل]` — **۷۹٬۰۰۰**
*Note:* نظرات یک افزونه مستقل است.
نظرات مشتریان ✗✓✓ ۷۹٬۰۰۰ · امتیازدهی · ثبت نظر · تأیید / رد نظر — ✗✓✓، «همراه ماژول»

**Group 15 — گزارش فروش** `[افزونه مستقل]` — **۱۹۰٬۰۰۰**
گزارش فروش ✗✓✓ ۱۹۰٬۰۰۰ · درآمد · گزارش روزانه · گزارش هفتگی · گزارش ماهانه · محصولات پرفروش · مشتریان برتر — ✗✓✓، «همراه ماژول»

**Group 16 — Social Marketing** `[افزونه مستقل]` — **۳۹۰٬۰۰۰**
*Note:* کاربر Social Marketing را می‌خرد، نه اتصال تلگرام، بله یا هر قابلیت انتشار را جداگانه.
Social Marketing ✗✓✓ ۳۹۰٬۰۰۰ · اتصال تلگرام · اتصال بله · اتصال سایر کانال‌ها · انتشار محصول · انتشار تصاویر و اطلاعات محصول · انتشار گروهی · انتشار خودکار · زمان‌بندی انتشار — ✗✓✓، «همراه ماژول»

**Group 17 — اتصال حسابداری** `[افزونه مستقل]` — **۲۹۰٬۰۰۰**
*Note:* فقط داخل پلن پرو فعال است؛ کاربر پایه یا استاندارد می‌تواند این ماژول را جداگانه خریداری کند. Providerهای حسابداری جداگانه قیمت‌گذاری نمی‌شوند.
اتصال حسابداری ✗✗✓ ۲۹۰٬۰۰۰ · اتصال نرم‌افزارهای حسابداری · Sync کالا · Sync موجودی — ✗✗✓، «همراه ماژول»

**Group 18 — باشگاه مشتریان** `[افزونه مستقل]` — **۶۹۰٬۰۰۰**
*Note:* چه با پلن پرو و چه با خرید جداگانه، تمام قابلیت‌ها فعال می‌شود؛ نسخه Lite یا Limited نداریم.
باشگاه مشتریان ✗✗✓ ۶۹۰٬۰۰۰ · امتیاز خوش‌آمدگویی · امتیاز بر اساس خرید · مصرف امتیاز · انقضای امتیاز · قوانین امتیازدهی · تاریخچه امتیازات · افزایش / کاهش دستی امتیاز · Segmentation مشتری · New / Loyal / VIP / At Risk · SMS Marketing · ارسال گروهی پیامک · زمان‌بندی پیامک · قالب پیامک · Delivery Report · کمپین‌ها · گزارش باشگاه — ✗✗✓، «همراه ماژول»

### 5.4 Add-on cards section
A grid of ten add-on cards, each showing name, monthly price, and a one-line description:
| Add-on | Price | Description |
|---|---|---|
| واحد فروش پیشرفته | ۲۹۰٬۰۰۰ | واحدهای فروش با قیمت و موجودی مستقل |
| انبار | ۲۹۰٬۰۰۰ | مدیریت موجودی، هشدار کمبود و ورود گروهی با Excel |
| فروش حضوری | ۱۹۰٬۰۰۰ | ثبت فروش در مغازه و آمار فروش روزانه |
| فروش اقساطی | ۳۹۰٬۰۰۰ | اسنپ‌پی، ترب‌پی و دیجی‌پی؛ فروش اعتباری |
| تخفیف | ۹۹٬۰۰۰ | تخفیف درصدی، مبلغی و دسته‌بندی |
| نظرات | ۷۹٬۰۰۰ | امتیازدهی و ثبت نظر مشتریان |
| گزارش فروش | ۱۹۰٬۰۰۰ | درآمد، محصولات پرفروش و مشتریان برتر |
| Social Marketing | ۳۹۰٬۰۰۰ | انتشار محصول در تلگرام، بله و سایر کانال‌ها |
| اتصال حسابداری | ۲۹۰٬۰۰۰ | همگام‌سازی کالا و موجودی با نرم‌افزار حسابداری |
| باشگاه مشتریان | ۶۹۰٬۰۰۰ | امتیاز، سطح‌بندی، کمپین و SMS Marketing |

### 5.5 Plans acceptance criteria
- The master table renders all 18 groups with correct chips, notes and per-row states.
- Period tabs highlight the correct column and default to ماهانه on load.
- Table remains usable on mobile (horizontal scroll with a persistent label column).
- Every value is identical to the pricing page.

### 5.6 Pricing vs Plans — required product decision
Two pages currently present overlapping content (both contain the price matrix, the full comparison table and the add-on list). Before build, decide one of:
- **(A)** Pricing = marketing page with cards, add-ons and policies; Plans = the exhaustive comparison, linked as «مقایسه کامل». *(Recommended.)*
- **(B)** Merge into a single Pricing page with a "full comparison" expansion.
Either way, **the pricing dataset must live in one place and be referenced by both views** so they can never drift.

---

## 6. Page 4 — Blog index (`menuch-blog.html`)

**Purpose:** discovery hub for organic traffic; routes readers to articles and, from there, to conversion.

### 6.1 Structure
1. Global banner + nav (مقالات active).
2. Breadcrumb: منوچ / **مقالات**.
3. Hero: kicker «مقالات منوچ»; H1 «یاد بگیر، رشد کن، بیشتر بفروش»; subtitle «مقالات کاربردی درباره فروشگاه آنلاین، بازاریابی و نگه‌داشتن مشتری؛ قدم‌به‌قدم با منوچ.»; a search field with placeholder «جستجو در مقالات…».
4. Featured strip — one large cover-style card plus two standard cards:
   - **چرا وبسایت دردسر داره؟** — badge «مقاله ویژه», cover treatment with gradient shade, «آشنایی با دردسرهای رایج سایت‌سازها و راه‌حل منوچ.»
   - **سئو چقدر مهمه؟** — badge «آموزش»
   - **فروش چجوری انجام می‌شه؟** — badge «راهنما»
5. Section heading «مقالات کاربردی» / «نکته‌ها و راهنمایی‌های کاربردی برای فروش آنلاین و رشد کسب‌وکارت».
6. Category filter chips: **همه** (default) · فروش · پرداخت · بازاریابی · راهنما · مشتریان · انبار.
7. Post grid.
8. Empty state.
9. Pagination.
10. Global footer.

### 6.2 Search & filter behavior
- Search filters the visible posts as the user types, matching against the full text of each card.
- **Persian normalization is mandatory:** Arabic ي/ك must match Persian ی/ک, zero-width non-joiner is treated as a space, repeated whitespace collapses, matching is case-insensitive.
- Category chips are single-select; selecting one deactivates the others.
- Search and category combine (AND).
- While any filter is active, **pagination is hidden**.
- When filters match nothing, show: «مقاله‌ای با این فیلتر پیدا نشد؛ عبارت یا دستهٔ دیگری را امتحان کن.»
- Clearing the search and returning to «همه» restores the full list and pagination.

### 6.3 Post cards (seed content)
| Title | Excerpt | Category | Time · Date |
|---|---|---|---|
| چرا وبسایت دردسر داره؟ | آشنایی با دردسرهای رایج سایت‌سازها و راه‌حل منوچ | راهنما | ۱۲:۳۰ · یکشنبه ۱۲ مرداد ۱۴۰۵ |
| سئو چقدر مهمه؟ | چطور با سئو مشتری بیشتری به فروشگاهت بیاری | بازاریابی | ۱۲:۳۰ · یکشنبه ۱۲ مرداد ۱۴۰۵ |
| چرا سایت‌سازها؟ | مقایسه سایت‌سازها؛ کدوم برای کسب‌وکار تو بهتره | راهنما | ۱۲:۳۰ · یکشنبه ۱۲ مرداد ۱۴۰۵ |
| فروش چجوری انجام می‌شه؟ | مسیر کامل فروش در منوچ؛ از سفارش تا تسویه | فروش | ۱۲:۳۰ · یکشنبه ۱۲ مرداد ۱۴۰۵ |
| باشگاه مشتریان چطور کار می‌کنه؟ | امتیاز، سطح‌بندی، کمپین و SMS برای نگه‌داشتن مشتری | مشتریان | ۰۹:۱۵ · سه‌شنبه ۱۴ مرداد ۱۴۰۵ |
| فروش اقساطی در فروشگاهت | اسنپ‌پی، ترب‌پی و دیجی‌پی؛ فروش اعتباری و دریافت نقدی | فروش | ۱۴:۴۰ · پنجشنبه ۱۶ مرداد ۱۴۰۵ |
| راه‌اندازی درگاه پرداخت | زرین‌پال، زیبال و کارت‌به‌کارت؛ تسویه سریع بدون واسطه | پرداخت | ۱۰:۰۵ · شنبه ۱۸ مرداد ۱۴۰۵ |
| مدیریت انبار با Excel | ورود گروهی موجودی، قیمت و Export اطلاعات | انبار | ۱۶:۲۰ · دوشنبه ۲۰ مرداد ۱۴۰۵ |

Every card ends with «مشاهده مقاله».

### 6.4 Pagination
- Numbered pages with a truncation ellipsis and previous/next arrows (visually mirrored for RTL).
- Previous is disabled on the first page; next is disabled on the last page.
- Seed: pages ۱ ۲ ۳ ۴ … ۱۲, page ۱ active.
- **Requirement:** pagination must load real additional posts (server-side or route-based), not merely re-style buttons as in the mockup.

### 6.5 Blog acceptance criteria
- Search returns correct results for queries typed with Arabic characters and with/without نیم‌فاصله.
- Category + search combined produce the intersection.
- Empty state appears only when filtering yields zero results.
- Pagination hides while filtering and reappears when filters clear.
- Cards keep equal height in a row regardless of title length.

---

## 7. Page 5 — Article detail (`menuch-article.html`)

**Purpose:** deliver the content, build trust, and route the reader onward (related articles → blog → product).

### 7.1 Structure
1. Global banner + nav (مقالات active).
2. Breadcrumb: منوچ / مقالات / **{article title}**.
3. Article header: tag chips (e.g. «راهنمای فروش», «فروشگاه آنلاین») · H1 · lede paragraph · meta line: time «۱۲:۳۰» · date «یکشنبه ۱۲ مرداد ۱۴۰۵» · reading time «۶ دقیقه مطالعه».
4. Cover image.
5. Article body.
6. Share row.
7. Comments.
8. Related articles.
9. Global footer.

### 7.2 Article body content model
The body must support and correctly style: paragraphs, H2 subheadings, unordered lists, and pull-quote blockquotes. Reference article «چرا وبسایت دردسر داره؟» contains:
- Intro paragraph on the barrier of building a website.
- H2 «دردسر اول: هزینه‌های پنهان» + two paragraphs.
- H2 «دردسر دوم: نیاز به دانش فنی» + paragraph.
- Blockquote: «فروشگاهم رو توی یک روز و بدون هیچ دانش فنی با منوچ راه انداختم؛ دیگه به برنامه‌نویس نیازی نداشتم.»
- H2 «دردسر سوم: سردرگمی در مدیریت» + paragraph + a 4-item list (مدیریت کالا و خدمات در چند کلیک · ورود گروهی محصولات با فایل اکسل · گزارش فروش شفاف و قابل‌فهم · پشتیبانی واقعی از ۸ صبح تا ۱۰ شب).
- H2 «راه‌حل منوچ چیه؟» + two closing paragraphs ending on the 14-day free trial.

Reading measure should stay comfortable (roughly 70–80 characters per line) and body line-height generous.

### 7.3 Share row
Label «این مقاله رو به اشتراک بذار» plus three actions: **کپی لینک**, **تلگرام**, **واتساپ**. Copy-link must give visible confirmation feedback.

### 7.4 Comments
- Heading «نظرات کاربران» with two summary stats: «میانگین امتیازات ۴٫۵» and «نظر ثبت شده ۲».
- Comment item: circular avatar with the first letter of the name, name, relative time («۲ روز پیش»), star rating, comment text, and a «پاسخ دادن» action.
  - Seed 1 — نگار محمدی · ۲ روز پیش · «مقاله خیلی کاربردی بود؛ مخصوصاً بخش دردسرهای سایت‌سازها دقیقاً همون چیزی بود که من تجربه کرده بودم. با منوچ توی یک روز فروشگاهم رو راه انداختم.»
  - Seed 2 — امیر رضایی · ۵ روز پیش · «جمع‌بندی خوبی بود. فقط کاش یه بخش هم درباره مهاجرت از سایت‌سازهای دیگه به منوچ اضافه می‌کردید.»
- A «ثبت نظر» button reveals the comment form and hides itself; the form scrolls into view.
- **Form:** interactive 5-star rating (labelled «امتیاز شما:»), «عنوان نظر» text field, «توضیحات» textarea, submit «ثبت نظر».
- **Required behaviors:** rating must be keyboard-operable and expose its value; validation with Persian messages; spam protection; comments enter a moderation queue and the user sees «نظر شما ثبت شد و پس از تأیید نمایش داده می‌شود»; average rating and count derive from approved comments only.
- **Not yet designed — must be specified before build:** the reply thread UI behind «پاسخ دادن».

### 7.5 Related articles
- Heading «مقالات مرتبط» / «این مقاله‌ها هم برای شروع فروش آنلاین بهت کمک می‌کنن».
- Three post cards (same card component as the blog) plus a «مشاهده همه» panel → blog index.

### 7.6 Article acceptance criteria
- Breadcrumb reflects the actual article title.
- Reading time is calculated from the article's own word count, not hard-coded.
- All body element types render correctly in RTL, including mixed Latin terms (Excel, SSL) without direction breakage.
- The comment form is fully keyboard-accessible, including the star rating.
- Share links produce a correct URL and title for each channel.

---

## 8. Page 6 — Academy (`menuch-academy.html`)

**Purpose:** the video learning hub — onboarding and activation content that reduces support load and increases retention.

### 8.1 Structure
1. Global banner + nav (**آکادمی** active).
2. Breadcrumb: منوچ / **آکادمی**.
3. Featured player block.
4. Two-column body: video list (right) + sidebar (left).
5. Blog teaser row.
6. Divider.
7. FAQ (same component and content as the landing FAQ).
8. Consultation section (same component and content as the landing form).
9. Global footer.

### 8.2 Featured player
- Asymmetric two-column: a large 768:410 player on the right, text on the left; stacks below 980px.
- Player: cover image, bottom gradient shade, centered circular play button that scales on hover, and an overlay row with the video title and a category tag.
- Featured video: **«آموزش افزودن کالا»** · tag «افزونه» · description «توی این ویدئو قدم‌به‌قدم یاد می‌گیری چطور کالا، خدمات و ویژگی‌های محصول رو به فروشگاهت اضافه کنی.» · meta ۲۴ اردیبهشت ۱۴۰۵ · ۱۲:۳۰.

### 8.3 Video list
- Header row: «آکادمی منوچ» with a count on the opposite side — «۲۴ ویدئو آموزشی» (must reflect the real count).
- Each row: 240px thumbnail with overlay and small play badge · title · two-line clamped description · meta footer with a category tag and date/time.
- Below 640px each row stacks vertically with a 16:9 thumbnail.
- **Seed videos:**
  | Title | Description | Tag | Date · Time |
  |---|---|---|---|
  | راه‌اندازی فروشگاه در ۱۰ دقیقه | از ثبت‌نام تا آنلاین‌شدن فروشگاهت؛ قدم‌به‌قدم و بدون دانش فنی. | شروع کار | ۲۴ اردیبهشت ۱۴۰۵ · ۱۲:۳۰ |
  | ورود گروهی محصولات با اکسل | ورود کالا، قیمت و موجودی با فایل اکسل در چند دقیقه. | افزونه | ۱۰ خرداد ۱۴۰۵ · ۱۵:۰۰ |
  | مدیریت انبار و هشدار موجودی | مدیریت موجودی، هشدار کمبود و Export اطلاعات. | افزونه | ۵ تیر ۱۴۰۵ · ۱۱:۰۰ |
  | اتصال درگاه پرداخت و تسویه | زرین‌پال، زیبال و کارت‌به‌کارت؛ تسویه سریع بدون واسطه. | کارگاه | ۲۰ مرداد ۱۴۰۵ · ۱۸:۳۰ |
  | فروش اقساطی با اسنپ‌پی و ترب‌پی | فعال‌سازی فروش اعتباری و دریافت نقدی مبلغ. | دوره آنلاین | ۱۵ شهریور ۱۴۰۵ · ۱۴:۰۰ |
  | Social Marketing و انتشار خودکار | انتشار محصول در تلگرام، بله و سایر کانال‌ها به‌صورت زمان‌بندی‌شده. | وبینار | ۳۰ مهر ۱۴۰۵ · ۱۰:۰۰ |
  | اتصال حسابداری و همگام‌سازی | Sync کالا و موجودی با نرم‌افزارهای حسابداری. | کارگاه تخصصی | ۱۵ آبان ۱۴۰۵ · ۱۴:۰۰ |
  | باشگاه مشتریان و کمپین | امتیاز، سطح‌بندی، SMS Marketing و گزارش باشگاه. | دوره آموزشی | ۲۰ آذر ۱۴۰۵ · ۱۶:۰۰ |
  | گزارش فروش و تحلیل | درآمد، محصولات پرفروش و مشتریان برتر رو تحلیل کن. | سمینار | ۵ دی ۱۴۰۵ · ۱۱:۰۰ |
- Category tag vocabulary: شروع کار · افزونه · کارگاه · کارگاه تخصصی · دوره آنلاین · دوره آموزشی · وبینار · سمینار.

### 8.4 Sidebar (367px, sticky)
- Header: «کانال های ما» with «عضو شوید» on the opposite side.
- Ordered contents: promo image → dark CTA «با ۶۹۰ هزار تومان شروع کن» (→ pricing) → promo image → promo image → brand CTA «درخواست مشاوره» (→ home `#contact`).
- Promo slots are content-managed (image + destination link).
- Sidebar sticks below the nav while the video list scrolls; it moves below the content on screens under 980px.

### 8.5 Missing capabilities to specify
The mockup is a static list. Before build, decide and specify:
- Filtering by category tag (recommended, mirroring the blog chips).
- Pagination or infinite scroll once the library exceeds ~12 videos.
- Whether selecting a list item swaps the featured player or navigates to a dedicated video page (**recommendation: dedicated page**, for SEO and shareability).
- Video hosting/player source and whether captions/transcripts are provided.

### 8.6 Academy acceptance criteria
- Featured player and list render with correct RTL placement (player right, text left; list right, sidebar left).
- The video count matches the number of published videos.
- Sidebar stickiness never overlaps the nav bar or the footer.
- FAQ and consultation components are the same components as the landing page — not duplicated copies that can drift.

---

## 9. Shared components inventory

| # | Component | Used on |
|---|---|---|
| C1 | Promo banner | All |
| C2 | Sticky nav bar (+ mobile drawer) | All |
| C3 | Footer card | All |
| C4 | Section heading (title + subtitle) | All |
| C5 | Dark button / solid button / soft button / brand-tint pill | All |
| C6 | Feature card (icon + title + text) | Landing hero, features |
| C7 | Customer card | Landing |
| C8 | Plan card + period toggle | Landing, Pricing |
| C9 | Comparison table (grouped, with chips and notes) | Pricing, Plans |
| C10 | Add-on card | Plans (and Pricing list) |
| C11 | Policy card | Pricing |
| C12 | Blog post card | Landing, Blog, Article, Academy |
| C13 | Featured/cover post card | Blog |
| C14 | Category filter chips | Blog (and Academy, if adopted) |
| C15 | Pagination | Blog |
| C16 | Video player block (featured) | Landing, Academy |
| C17 | Video list row | Academy |
| C18 | Testimonial reel | Landing |
| C19 | FAQ accordion | Landing, Academy |
| C20 | Consultation form | Landing, Academy |
| C21 | Comment list + comment form + star rating | Article |
| C22 | Breadcrumb | Blog, Article, Academy |
| C23 | Tag / chip | Blog, Article, Academy |
| C24 | Marquee track (horizontal & vertical) | Landing |
| C25 | Phone mockup illustration | Landing |

**Rule:** each component has exactly one definition and one set of tokens. A component may not be re-styled per page.

---

## 10. Content & data inventory to be supplied

| Asset | Quantity | Owner | Status |
|---|---|---|---|
| Manooch logo (light + dark) | 2 | Design | In mockups |
| Customer logos | 6+ | Marketing | Placeholder |
| Hero intro video + poster | 1 | Marketing | Placeholder |
| Testimonial reels | 4 | Marketing | Placeholder |
| Academy videos + thumbnails | 24 (9 seeded) | Content | Partial |
| Blog articles + covers | 8 seeded, 12 pages implied | Content | Partial |
| Team/support photo | 1 | Marketing | Placeholder |
| Trust badges (نماد اعتماد, زرین‌پال) | 2 | Legal/Marketing | Placeholder |
| Sidebar promo creatives | 3 | Marketing | Placeholder |
| Feature icon set | ~30 | Design | In mockups |
| Ravi font licence & web files | 5 weights | Design/Legal | **Blocker — see §12** |

---

## 11. Non-functional requirements

| Area | Requirement |
|---|---|
| Browsers | Latest two versions of Chrome, Safari, Firefox, Edge; Samsung Internet; iOS Safari 15+ |
| Devices | 360px → 1920px; must be verified at 360, 768, 1024, 1440, 1920 |
| Performance | LCP < 2.5s, CLS < 0.1, INP < 200ms on mid-tier mobile |
| Accessibility | WCAG 2.1 AA |
| SEO | See §2.11 |
| Privacy | Consultation and comment forms collect personal data — a privacy notice and consent statement are required; retention policy must be defined |
| Security | Form spam protection, rate limiting, input sanitization for comments |
| Localization | Persian only at launch; layout must not hard-assume RTL in a way that blocks a future LTR locale |
| Analytics | See §2.12 |

---

## 12. Known gaps, risks and required decisions

| # | Issue | Impact | Required action |
|---|---|---|---|
| G1 | **Fonts embedded as inline base64** (hundreds of KB per page, repeated) | Severe performance hit | Serve subset web fonts from a cached source |
| G2 | **Ravi font licensing** for web distribution unconfirmed | Legal blocker | Confirm licence or replace with a licensed Persian family |
| G3 | Pricing page ships **without banner/nav/footer** | Broken navigation, dead end | Add the global shell |
| G4 | Landing footer email is rendered through an **email-obfuscation placeholder** | Broken contact link | Render a plain `mailto:` link |
| G5 | **Pricing vs Plans duplication** | Content drift, SEO cannibalization | Resolve per §5.6; single pricing data source |
| G6 | Internal **"موارد باقی‌مانده برای تصمیم بعدی"** block is publicly visible | Reveals unfinished commercial strategy | Remove from public page |
| G7 | No **mobile navigation** pattern designed | Nav unusable on phones | Design and specify a drawer |
| G8 | Blog **pagination is non-functional** | Only 8 posts reachable | Implement real paging |
| G9 | Academy has **no filtering or paging** | Unusable beyond ~12 videos | Specify per §8.5 |
| G10 | Video **hosting/player not chosen**; no captions or transcripts | Accessibility + delivery risk | Choose a provider; require captions |
| G11 | **Reply threads** on comments undesigned | Feature promised in UI, not built | Design or remove «پاسخ دادن» |
| G12 | Customer logos include large national brands (تپسی، اسنپ) | Legal/credibility risk if unverified | Verify permission to display |
| G13 | Banner deadline «فقط تا ۳۰ آذر» is hard-coded | Stale promo | Make date-driven and content-managed |
| G14 | Stat claims («میلیاردها تومان», «۹۹٪ رضایت», «۳٬۰۰۰+») unsourced | Credibility/legal | Substantiate or soften |
| G15 | Landing repeats the price ۶۹۰ هزار in the hero CTA | Breaks on any price change | Bind to the pricing data source |
| G16 | No 404 / error page defined | Poor UX on bad links | Design a 404 using the global shell |
| G17 | Consultation form has **no defined destination** (CRM/email/ticket) | Leads lost | Define the routing and SLA owner |
| G18 | Hero glow parallax and dual marquees are motion-heavy | Battery/CPU on low-end phones | Reduce or disable on mobile |

---

## 13. Delivery plan

**Phase 1 — Foundations:** design tokens, typography, RTL grid, global banner/nav/footer, mobile navigation, 404 page, base accessibility pass.
**Phase 2 — Landing:** all ten sections, marquees, feature disclosure, plan toggle, consultation form + routing, analytics events.
**Phase 3 — Pricing & Plans:** single pricing data source, plan cards, all tables, add-on grid, policy cards; resolve G5/G6.
**Phase 4 — Content pages:** blog index (search, filters, real pagination), article template (body styles, share, comments + moderation), academy (player, list, sidebar, filtering).
**Phase 5 — Hardening:** performance budget, SEO/structured data, accessibility audit, cross-browser and device QA, content load, launch checklist.

## 14. Definition of done
1. All six page types match the approved mockups at every specified breakpoint.
2. Every global component appears on every page, with the correct active nav state.
3. Every price and feature flag on the site traces to one shared pricing source.
4. All copy in this document is reproduced exactly, with Persian digits, Jalali dates and correct نیم‌فاصله.
5. Performance, accessibility and SEO targets in §11 are met and evidenced.
6. All analytics events in §2.12 fire with correct payloads.
7. Every item in §12 is either resolved or formally accepted as out of scope with a named owner.
