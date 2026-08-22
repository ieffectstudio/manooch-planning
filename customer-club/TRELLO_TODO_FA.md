# کارت‌های Feature-Based برای Trello — سیستم پیامک باشگاه مشتریان

این برد براساس **فیچر کامل End-to-End** تنظیم شده است. برای هر فیچر فقط یک کارت ساخته می‌شود و کارهای دیتابیس، منطق، API، صف، اتصال Armaghan، رابط کاربری، گزارش و تست همگی داخل همان کارت قرار می‌گیرند.

> برای یک فیچر کارت جداگانه Backend و Frontend نسازید. کارت فقط زمانی Done می‌شود که کل جریان فیچر از UI تا Provider و گزارش نهایی کامل باشد.

## لیست‌های پیشنهادی برد

1. `Backlog`
2. `Ready`
3. `Doing`
4. `Review & QA`
5. `Done`
6. `Blocked`

## لیبل‌های پیشنهادی

- `P0 - هسته مشترک`
- `P1 - فیچر لانچ`
- `Automation`
- `Campaign`
- `Loyalty`
- `Reports`
- `Compliance`

---

# کارت 00 — تنظیم و اتصال هسته مشترک سیستم SMS

**لیبل:** `P0 - هسته مشترک`

## توضیحات

تمام زیرساخت مشترک موردنیاز فیچرهای پیامکی به‌صورت یک جریان کامل پیاده‌سازی شود: تنظیم Seller، سرخط واقعی، قالب‌های داینامیک، Outbox، Adapter نسخه ۲ ارمغان، اعتبار داخلی، Eligibility، Opt-out، وضعیت تحویل و ابزارهای مشترک UI. این کارت پیش‌نیاز فعال‌سازی کارت‌های فیچری است.

**مستندات:**

- `docs/00-architecture-and-data-model.md`
- `docs/01-armaghan-v2-adapter.md`
- `docs/02-seller-sender-configuration.md`
- `docs/03-dynamic-template-management.md`
- `docs/19-template-id-and-binding-decision.md`

## چک‌لیست

- [ ] مدل‌های `seller_sms_profiles`، `seller_sender_lines` و `seller_sms_templates` ایجاد شوند.
- [ ] مدل‌های `sms_outbox` و `sms_messages` با Idempotency و Snapshot ایجاد شوند.
- [ ] مدل Opt-out، Suppression و App Credit ایجاد شود.
- [ ] Adapter عملیات One-to-Many، Many-to-Many، Message State، Credit و Incoming ساخته شود.
- [ ] Error Codeهای مستندشده Armaghan مدیریت شوند.
- [ ] Timeout مبهم بدون Retry کور مدیریت شود.
- [ ] سرخط واقعی هر Seller ثبت، تست و انتخاب شود.
- [ ] شماره تصادفی Prototype حذف شود.
- [ ] قالب پیش‌فرض هر Feature به Seller Template مستقل تبدیل شود.
- [ ] Preview، Test Send، Versioning و کنترل متغیرها پیاده‌سازی شوند.
- [ ] نرمال‌سازی، Dedupe، Opt-out، Daily Cap و Business Hours مشترک ساخته شوند.
- [ ] Signature و محدودیت نهایی ۳۲۰ کاراکتر اعمال شوند.
- [ ] اعتبار داخلی Seller مستقل از Provider Credit رزرو و Reconcile شود.
- [ ] تنظیمات سرخط، قالب و تست پیام از UI به API واقعی متصل شوند.
- [ ] تمام Queryها و اکشن‌ها Seller-Scoped باشند.
- [ ] Credentialها در Secret Manager باشند و در UI/Log نمایش داده نشوند.
- [ ] تست Cross-Seller، Error Mapping، Idempotency و Ambiguous Timeout سبز باشد.

## معیار Done

یک Seller بتواند سرخط واقعی و قالب خودش را تنظیم کند، پیام تست واقعی ارسال کند، Provider Reference دریافت کند و وضعیت پیام را بدون استفاده از Fixture مشاهده کند.

---

# کارت 01 — تنظیم و اتصال ساختار SMS خوش‌آمدگویی

**لیبل:** `P1 - فیچر لانچ`, `Loyalty`

## توضیحات

جریان خوش‌آمدگویی برای عضو جدید آنلاین و مشتری ثبت‌شده از Keypad حضوری به‌صورت کامل متصل شود. ثبت مشتری، امتیاز خوش‌آمدگویی، ساخت Outbox، ارسال از سرخط Seller، نمایش نتیجه در UI و تاریخچه همگی در همین کارت انجام شوند.

**مستند:** `docs/04-welcome-and-walk-in.md`

## چک‌لیست

- [ ] قالب `member.welcome` برای هر Seller ایجاد و قابل ویرایش شود.
- [ ] متغیرهای `name`، `store_name`، `points` و `balance` متصل شوند.
- [ ] فرم عضویت و Keypad حضوری به یک جریان واقعی متصل شوند.
- [ ] موبایل در محدوده همان Seller نرمال و یکتا شود.
- [ ] Customer و Welcome Points فقط یک‌بار و در یک Transaction ثبت شوند.
- [ ] Outbox خوش‌آمدگویی در همان Transaction ساخته شود.
- [ ] پیام از سرخط Default همان Seller ارسال شود.
- [ ] Preview و Test Send از صفحه تنظیمات قابل اجرا باشند.
- [ ] مشتری موجود دوباره امتیاز و پیام Welcome نگیرد.
- [ ] Failure پیامک عضویت یا امتیاز را Rollback نکند.
- [ ] Resend پیام، امتیاز جدید تولید نکند.
- [ ] وضعیت Queued/Accepted/Delivered/Failed در UI نمایش داده شود.
- [ ] تاریخچه پیام در گزارش مشتری ثبت شود.
- [ ] تست ثبت آنلاین، حضوری، Duplicate و Cross-Seller نوشته شود.

## معیار Done

عضو جدید دقیقاً یک Welcome Point Entry و یک Message Intent دریافت کند و تمام نتیجه از UI تا Provider و History قابل مشاهده باشد.

---

# کارت 02 — تنظیم و اتصال ساختار SMS کمپین دستی

**لیبل:** `P1 - فیچر لانچ`, `Campaign`

## توضیحات

ساخت، Preview، ارسال فوری، زمان‌بندی، لغو و گزارش کمپین دستی به‌صورت End-to-End متصل شود. Audience، قالب، Sender، Linked Tool، اعتبار، Provider Submission و UI Report در همان فیچر تکمیل شوند.

**مستند:** `docs/05-manual-campaigns.md`

## چک‌لیست

- [ ] ساختار Campaign، Run و Recipient ایجاد شود.
- [ ] فرم ساخت کمپین Prototype به API واقعی متصل شود.
- [ ] Audience، Template و Linked Tool متعلق به Seller بررسی شوند.
- [ ] Preview شامل تعداد اولیه، واجدشرایط، حذف‌شده و هزینه باشد.
- [ ] Template، Sender، Audience و Tool هنگام ثبت Snapshot شوند.
- [ ] Send Now و Schedule در UI و Backend متصل شوند.
- [ ] زمان Seller با `Asia/Tehran` به UTC تبدیل و ذخیره شود.
- [ ] Eligibility و Opt-out در زمان ارسال دوباره بررسی شوند.
- [ ] اعتبار داخلی فقط برای Eligibleهای نهایی رزرو شود.
- [ ] متن یکسان با One-to-Many و متن شخصی با Many-to-Many ارسال شود.
- [ ] Idempotency برای Run و هر Recipient اعمال شود.
- [ ] Cancel فقط گیرنده‌های ارسال‌نشده را متوقف کند.
- [ ] وضعیت واقعی هر Run در صفحه کمپین نمایش داده شود.
- [ ] درصدهای Fixture با داده Provider جایگزین شوند.
- [ ] تست Send Now، Schedule، Cancel، Retry و Cross-Seller سبز باشد.

## معیار Done

Seller بتواند یک کمپین واقعی را از UI ایجاد و ارسال/زمان‌بندی کند و گزارش واقعی هر گیرنده را مشاهده کند.

---

# کارت 03 — تنظیم و اتصال ساختار SMS گروهی

**لیبل:** `P1 - فیچر لانچ`, `Campaign`

## توضیحات

ارسال گروهی به چند Segment با Union واقعی، حذف شماره تکراری، فیلتر Opt-out، محاسبه هزینه، ارسال Batch، وضعیت تحویل و اتصال کامل Composer/History پیاده‌سازی شود.

**مستند:** `docs/06-bulk-sms.md`

## چک‌لیست

- [ ] انتخاب چند Segment در UI به API واقعی متصل شود.
- [ ] Segmentها فقط از Seller جاری Resolve شوند.
- [ ] Union اعضا ساخته و Countها مستقیم جمع نشوند.
- [ ] موبایل‌ها نرمال و Deduplicate شوند.
- [ ] دلیل حذف Invalid/Opt-out/Cap/Suppression ذخیره شود.
- [ ] تعداد Eligible و هزینه زنده به UI برگردد.
- [ ] قالب سریع، متغیرها، Preview و محدودیت ۳۲۰ کاراکتر متصل شوند.
- [ ] Send Now، Schedule و Test Send واقعی شوند.
- [ ] App Credit قبل از ارسال رزرو شود.
- [ ] Batch Size قابل تنظیم باشد.
- [ ] Contents و Destinations همیشه از یک آرایه Recipient ساخته شوند.
- [ ] One-to-Many/Many-to-Many براساس متن نهایی انتخاب شود.
- [ ] Retry گیرنده Accepted یا Unknown را دوباره ارسال نکند.
- [ ] History و Delivery Report واقعی در UI نمایش داده شوند.
- [ ] تست Segment هم‌پوشان، Batch Boundary و Array Alignment سبز باشد.

## معیار Done

ارسال گروهی واقعی بدون Duplicate و با گزارش کامل Eligible/Excluded/Delivery از UI قابل انجام باشد.

---

# کارت 04 — تنظیم و اتصال ساختار SMS شخصی

**لیبل:** `P1 - فیچر لانچ`, `Campaign`

## توضیحات

ارسال پیام مستقیم به یک مشتری، شماره دستی مجاز یا یک Segment به‌صورت کامل پیاده‌سازی شود. انتخاب گیرنده، قالب ذخیره‌شده، پیام سریع، Opt-out، Provider و History در یک فیچر متصل شوند.

**مستند:** `docs/07-personal-messages.md`

## چک‌لیست

- [ ] حالت Customer، Manual Mobile و Segment در UI متصل شوند.
- [ ] Customer فقط در Seller جاری Resolve شود.
- [ ] شماره دستی نرمال و Actor/Reason آن Audit شود.
- [ ] Manual Mode متغیرهای وابسته به Customer را رد کند.
- [ ] Segment Mode از همان Bulk Pipeline استفاده کند.
- [ ] Saved Messageها Seller-Scoped و Versioned باشند.
- [ ] Preview نهایی قبل از ارسال نمایش داده شود.
- [ ] Opt-out، Daily Cap و Business Hours بررسی شوند.
- [ ] ارسال تک‌گیرنده با One-to-Many انجام شود.
- [ ] از GET One-to-One استفاده نشود.
- [ ] Client Command ID از ارسال تکراری جلوگیری کند.
- [ ] Resend کنترل‌شده به Message اصلی لینک شود.
- [ ] وضعیت ارسال در همان بخش Personal Message نمایش داده شود.
- [ ] تست هر سه Mode، Duplicate و Cross-Seller سبز باشد.

## معیار Done

اپراتور بتواند از UI یک پیام مستقیم واقعی ارسال کند و نتیجه آن را بدون دورزدن Consent یا Tenant Isolation ببیند.

---

# کارت 05 — تنظیم و اتصال ساختار SMS یادآوری عدم خرید

**لیبل:** `P1 - فیچر لانچ`, `Automation`

## توضیحات

Ruleهای یادآوری براساس آخرین سفارش Paid/Completed ایجاد و خودکار اجرا شوند. تنظیم Rule، Preview، Scheduler، Suppression، ارسال و History در یک فیچر کامل شوند.

**مستند:** `docs/08-inactivity-reminders.md`

## چک‌لیست

- [ ] فرم ساخت/ویرایش Rule به API واقعی متصل شود.
- [ ] Rule Days بین ۱ تا ۳۶۵ کنترل شود.
- [ ] Audience و Template متعلق به Seller بررسی شوند.
- [ ] فقط سفارش Paid/Completed مبنای آخرین خرید باشد.
- [ ] Scheduler براساس timezone Seller اجرا شود.
- [ ] برای هر Rule/Local Date قفل اجرا ایجاد شود.
- [ ] قبل از Queue، خرید جدید دوباره بررسی شود.
- [ ] Suppression پیش‌فرض ۳۰ روز اعمال شود.
- [ ] متغیرهای Name/Days/Points/Date از داده واقعی ساخته شوند.
- [ ] Discount Code فقط در صورت وجود واقعی استفاده شود.
- [ ] ارسال شخصی‌سازی‌شده از سرخط Seller انجام شود.
- [ ] Settings، History و Delivery State در UI نمایش داده شوند.
- [ ] Duplicate Worker پیام تکراری نسازد.
- [ ] تست Timezone، Suppression، New Purchase و Cross-Seller سبز باشد.

## معیار Done

Rule از UI تنظیم شود، در زمان صحیح اجرا شود و فقط مشتری واقعاً واجدشرایط یک پیام Idempotent دریافت کند.

---

# کارت 06 — تنظیم و اتصال ساختار SMS تولد و مناسبت‌ها

**لیبل:** `P1 - فیچر لانچ`, `Automation`

## توضیحات

پیام تولد سالانه و مناسبت سفارشی دارای تاریخ، ساعت و Audience به‌صورت کامل متصل شوند. مدیریت مناسبت، تقویم، Scheduler، قالب، ارسال و گزارش در همان کارت انجام شوند.

**مستند:** `docs/09-birthday-and-occasions.md`

## چک‌لیست

- [ ] Birthday به‌عنوان مناسبت سیستمی غیرقابل حذف ساخته شود.
- [ ] فرم مناسبت جدید/ویرایش/فعال‌سازی به API متصل شود.
- [ ] مناسبت بدون تاریخ، ساعت، Audience و Template فعال نشود.
- [ ] تاریخ Canonical ذخیره و برای UI فارسی نمایش داده شود.
- [ ] سیاست Leap Day و نوع تقویم مشخص و تست شود.
- [ ] Scheduler در ساعت محلی Seller اجرا شود.
- [ ] Birthday برای هر Customer/Year فقط یک‌بار Queue شود.
- [ ] Audience، Opt-out، Cap و Business Hours اعمال شوند.
- [ ] Template و Sender Seller استفاده شوند.
- [ ] Discount Code غیرواقعی در متن قرار نگیرد.
- [ ] Preview مناسبت از UI قابل مشاهده باشد.
- [ ] History و Delivery Report واقعی نمایش داده شوند.
- [ ] تست Birthday Duplicate، Custom Occasion و Calendar سبز باشد.

## معیار Done

Seller بتواند مناسبت را کامل تنظیم کند و پیام در تاریخ صحیح، یک‌بار و با گزارش واقعی ارسال شود.

---

# کارت 07 — تنظیم و اتصال ساختار SMS انقضای امتیاز

**لیبل:** `P1 - فیچر لانچ`, `Automation`, `Loyalty`

## توضیحات

هشدار انقضای امتیاز براساس Points Lotهای باقی‌مانده تنظیم و اجرا شود. Settings، محاسبه امتیاز، Race با Spend، پیام و History در یک فیچر پیاده‌سازی شوند.

**مستند:** `docs/10-points-expiry.md`

## چک‌لیست

- [ ] تنظیم Days Before Expiry، ساعت و Template به UI متصل شود.
- [ ] Points Lot با Remaining و Expiry از Ledger خوانده شود.
- [ ] Lotهای خرج‌شده/Reversed/Expired حذف شوند.
- [ ] Lotهای یک تاریخ طبق Policy تجمیع شوند.
- [ ] مبلغ Expiring Points در Transaction Snapshot شود.
- [ ] Idempotency برای Seller/Customer/Expiry Date اعمال شود.
- [ ] قبل از Provider Call Remaining دوباره بررسی شود.
- [ ] Name/Points/Balance/Date از داده واقعی Render شوند.
- [ ] Opt-out/Classification و Business Hours اعمال شوند.
- [ ] پیام شخصی از سرخط Seller ارسال شود.
- [ ] Preview و History در UI نمایش داده شوند.
- [ ] Failure پیامک Pointها را تغییر ندهد.
- [ ] تست Spend همزمان، چند Lot و Duplicate Scheduler سبز باشد.

## معیار Done

هشدار فقط برای امتیاز واقعاً باقی‌مانده ارسال شود و خرج همزمان باعث پیام اشتباه نشود.

---

# کارت 08 — تنظیم و اتصال ساختار SMS هدف‌گیری مجدد

**لیبل:** `P1 - فیچر لانچ`, `Automation`, `Loyalty`

## توضیحات

اعلان ثبت اعتبار بازگشت/Cashback و هشدار انقضای آن به Ledger واقعی متصل شوند. تنظیمات، Grant، Scheduler، پیام و History به‌صورت End-to-End تکمیل شوند.

**مستند:** `docs/11-retargeting-notifications.md`

## چک‌لیست

- [ ] تنظیمات Grant و Expiry Notification به UI/API متصل شوند.
- [ ] مقدار Credit با Ruleهای Server-Side محاسبه شود.
- [ ] Credit Ledger و Grant Outbox در یک Transaction ثبت شوند.
- [ ] Manual Grant شامل Actor و Reason باشد.
- [ ] Grant برای Source یک‌بار ثبت شود.
- [ ] Scheduler فقط Credit استفاده‌نشده و مثبت را انتخاب کند.
- [ ] Credit Expired/Used/Reversed حذف شود.
- [ ] قالب Grant و Expiry جدا و Seller-Scoped باشند.
- [ ] Amount/Balance/Date از Snapshot Ledger Render شوند.
- [ ] ارسال از سرخط Seller انجام شود.
- [ ] Failure پیامک Credit را تغییر یا تکرار نکند.
- [ ] Settings، KPIs و History از داده واقعی نمایش داده شوند.
- [ ] تست Duplicate Grant، Expiry و Reversal سبز باشد.

## معیار Done

ثبت یا انقضای Credit دقیقاً یک Message Intent ایجاد کند و Ledger مستقل از نتیجه SMS صحیح باقی بماند.

---

# کارت 09 — تنظیم و اتصال ساختار SMS دعوت دوستان

**لیبل:** `P1 - فیچر لانچ`, `Loyalty`, `Compliance`

## توضیحات

ارسال دعوت Referral، لینک امن، Qualification و پیام پاداش به‌صورت یک فیچر کامل متصل شوند. کنترل سوءاستفاده و Tenant Isolation بخشی از همان کارت است.

**مستند:** `docs/12-referral-messages.md`

## چک‌لیست

- [ ] UI دعوت دوست به API واقعی متصل شود.
- [ ] Referral Token تصادفی، Expiring و Seller-Scoped باشد.
- [ ] شماره دعوت‌شونده نرمال و Opt-out بررسی شود.
- [ ] Self-Referral رد شود.
- [ ] محدودیت روزانه Inviter/Destination/IP اعمال شود.
- [ ] لینک دعوت در قالب Seller Render شود.
- [ ] Qualification ثبت‌نام/اولین خرید معتبر بررسی شود.
- [ ] پاداش Inviter/Invitee حداکثر یک‌بار و اتمیک ثبت شود.
- [ ] Reward Outbox در همان Transaction ساخته شود.
- [ ] پیام فقط Reward واقعاً تنظیم‌شده را اعلام کند.
- [ ] Failure پیامک پاداش را تکرار یا حذف نکند.
- [ ] Funnel و History واقعی در UI نمایش داده شوند.
- [ ] تست Abuse، Replay، Cross-Seller و Reward Uniqueness سبز باشد.

## معیار Done

دعوت از UI تا پیام و Qualification کامل باشد و هیچ مسیر تکرار یا سوءاستفاده برای پاداش وجود نداشته باشد.

---

# کارت 10 — تنظیم و اتصال ساختار SMS گردونه شانس

**لیبل:** `P1 - فیچر لانچ`, `Loyalty`

## توضیحات

پیام دعوت به گردونه و پیام اعلام برنده به Spin قطعی Server-Side متصل شوند. تنظیمات گردونه، لینک، نتیجه، جایزه، Code، پیام و History در یک کارت تکمیل شوند.

**مستند:** `docs/13-wheel-messages.md`

## چک‌لیست

- [ ] تنظیمات گردونه و جوایز از UI در Backend ذخیره شوند.
- [ ] تعداد Prize بین ۲ تا ۸ و مجموع Chance دقیقاً ۱۰۰٪ باشد.
- [ ] دعوت با لینک Seller/Wheel/Customer Scoped ساخته شود.
- [ ] پیام دعوت با لینک شخصی از سرخط Seller ارسال شود.
- [ ] Daily Spin Cap و Entry Cost Server-Side اعمال شوند.
- [ ] Spin با Secure Randomness Server-Side انجام شود.
- [ ] Points/Prize/Code/Outbox در یک Transaction ثبت شوند.
- [ ] Duplicate Spin فقط یک Outcome داشته باشد.
- [ ] پیام Winner از Prize Snapshot قطعی ساخته شود.
- [ ] Failure پیامک باعث Reroll/Reaward نشود.
- [ ] Resend همان Code و Prize را استفاده کند.
- [ ] Winners و Delivery History واقعی در UI نمایش داده شوند.
- [ ] تست Concurrency، Chance، Duplicate و Cross-Seller سبز باشد.

## معیار Done

از دعوت تا Spin و پیام برنده، کل جریان Server-Authoritative، Idempotent و قابل گزارش باشد.

---

# کارت 11 — تنظیم و اتصال ساختار SMS نظرسنجی

**لیبل:** `P1 - فیچر لانچ`, `Campaign`, `Loyalty`

## توضیحات

دعوت نظرسنجی، لینک اختصاصی، ثبت پاسخ، پاداش و Reminder افراد بی‌پاسخ به‌صورت یک فیچر کامل متصل شوند.

**مستند:** `docs/14-survey-messages.md`

## چک‌لیست

- [ ] فرم ساخت Survey و ۲ تا ۶ Option به API متصل شود.
- [ ] Audience، Template و Schedule ذخیره و Snapshot شوند.
- [ ] برای هر گیرنده Token امن و اختصاصی ساخته شود.
- [ ] Invitation با لینک‌های شخصی Many-to-Many ارسال شود.
- [ ] صفحه عمومی مشاهده/ثبت پاسخ با Token متصل شود.
- [ ] Token Scope، Expiry و Option Ownership بررسی شوند.
- [ ] یک Response و Reward حداکثر یک‌بار ثبت شوند.
- [ ] Response و Reward در یک Transaction ثبت شوند.
- [ ] Reminder فقط برای Inviteeهای بدون پاسخ ارسال شود.
- [ ] Survey پایان‌یافته رفتار مشخص داشته باشد.
- [ ] Results، Invite Delivery و Response Funnel در UI واقعی شوند.
- [ ] Failure پیامک Survey State یا Reward را خراب نکند.
- [ ] تست Token، Duplicate Response، Reward و Reminder سبز باشد.

## معیار Done

Seller بتواند Survey را از UI اجرا کند و Funnel دعوت، تحویل و پاسخ واقعی را مشاهده کند.

---

# کارت 12 — تنظیم و اتصال ساختار SMS تأیید خرید کلاب

**لیبل:** `P1 - فیچر لانچ`, `Loyalty`

## توضیحات

خرید آیتم کلاب، کسر امتیاز، کاهش موجودی، ساخت Code، ارسال تأیید و نمایش History به‌صورت یک جریان کامل و اتمیک پیاده‌سازی شوند.

**مستند:** `docs/15-club-redemption.md`

## چک‌لیست

- [ ] صفحه خرید Customer به Redemption API واقعی متصل شود.
- [ ] Seller/Customer/Item Ownership بررسی شود.
- [ ] Stock و Points Balance Lock/Version شوند.
- [ ] Active/Stock/Balance/Daily Cap بررسی شوند.
- [ ] Client Command ID از Double Click جلوگیری کند.
- [ ] Points Ledger، Stock و Redemption در یک Transaction ثبت شوند.
- [ ] Redemption Code امن و یکتا ایجاد شود.
- [ ] Confirmation Outbox در همان Transaction ساخته شود.
- [ ] Code قطعی بلافاصله در UI نمایش داده شود.
- [ ] Message از Item/Cost/Balance Snapshot ساخته شود.
- [ ] Failure پیامک Redemption را ناقص یا برگشت ندهد.
- [ ] Resend همان Redemption و Code را استفاده کند.
- [ ] Purchase/Delivery History واقعی نمایش داده شود.
- [ ] تست Concurrent Stock/Points، Duplicate و Cross-Seller سبز باشد.

## معیار Done

خرید کلاب در هر شرایط فقط یک‌بار ثبت شود و پیام تأیید و History آن با همان Code قطعی متصل باشند.

---

# کارت 13 — تنظیم و اتصال ساختار گزارش وضعیت SMS

**لیبل:** `P1 - فیچر لانچ`, `Reports`

## توضیحات

Referenceهای Provider، Polling وضعیت و گزارش‌های Dashboard، Campaign، Tool و Message Detail به‌صورت کامل متصل شوند و تمام Fixtureها حذف شوند.

**مستند:** `docs/16-delivery-reports.md`

## چک‌لیست

- [ ] Referenceها به‌صورت string و به Recipient درست Map شوند.
- [ ] تعداد Reference و Destination Validate شود.
- [ ] Worker مربوط به `getMessageState` ساخته شود.
- [ ] Stateهای ۰ تا ۶ و `-100` Map شوند.
- [ ] State Terminal Regression نکند.
- [ ] Poll Backoff و Max Age قابل تنظیم باشند.
- [ ] Accepted/Sent/Delivered/Not Delivered/Unknown تفکیک شوند.
- [ ] API Summary، Run Report و Message Detail ساخته شود.
- [ ] Denominator نرخ تحویل مشخص باشد.
- [ ] Dashboard، Sheets و History به API واقعی متصل شوند.
- [ ] Unknown/Reference Missing در UI قابل مشاهده باشند.
- [ ] گزارش Seller-Scoped باشد.
- [ ] Totals با Recipient Rowها Reconcile شوند.
- [ ] تست Mapping، Out-of-Order State و Cross-Seller سبز باشد.

## معیار Done

تمام گزارش‌های SMS از داده واقعی Provider ساخته شوند و هیچ درصد یا Count ثابت Prototype باقی نماند.

---

# کارت 14 — تنظیم و اتصال ساختار دریافت SMS و لغو پیام تبلیغاتی

**لیبل:** `P1 - فیچر لانچ`, `Compliance`

## توضیحات

پیام ورودی Provider دریافت، با سرخط مقصد به Seller صحیح Route و پاسخ ۵ به Opt-out بازاریابی همان Seller تبدیل شود. وضعیت Opt-out در UI مشتری و تمام مسیرهای ارسال اعمال شود.

**مستند:** `docs/17-inbound-opt-out.md`

## چک‌لیست

- [ ] Polling `getReceivedMessages` و Checkpoint ایجاد شود.
- [ ] Inbox Provider ID به‌صورت Unique ذخیره شود.
- [ ] Destination به سرخط Seller Resolve شود.
- [ ] Destination ناشناخته وارد Review Queue شود.
- [ ] `5`، `۵` و `٥` یکسان نرمال شوند.
- [ ] Stop Wordهای دقیق و تأییدشده تعریف شوند.
- [ ] Opt-out فقط برای همان Seller ثبت شود.
- [ ] Marketing Messageهای ارسال‌نشده Cancel شوند.
- [ ] Eligibility قبل از Dispatch Opt-out را دوباره بررسی کند.
- [ ] وضعیت Opt-out در پروفایل Customer نمایش داده شود.
- [ ] امکان Audit منبع و زمان Opt-out وجود داشته باشد.
- [ ] Raw Message و Mobile طبق Retention/Privacy محافظت شوند.
- [ ] تست Replay Inbound، Unknown Line، Race و Cross-Seller سبز باشد.

## معیار Done

پاسخ ۵ به سرخط Seller A فقط پیام‌های بازاریابی Seller A را متوقف کند و در UI و Dispatch قابل مشاهده و غیرقابل دورزدن باشد.

---

# کارت 15 — نهایی‌سازی و لانچ کل ساختار SMS

**لیبل:** `P0 - هسته مشترک`, `P1 - فیچر لانچ`

## توضیحات

پس از تکمیل کارت‌های Feature-Based، کل سیستم با سناریوهای واقعی Staging، امنیت، Tenant Isolation، Provider Errors، Opt-out و گزارش‌ها بررسی و برای Production نهایی شود.

**مستند:** `docs/18-launch-checklist.md`

## چک‌لیست

- [ ] Credential افشاشده Rotate و Secret Manager فعال شود.
- [ ] سرخط واقعی و شماره تست مجاز برای هر Seller آماده باشد.
- [ ] One-to-Many واقعی از UI تا Delivery Report تست شود.
- [ ] Many-to-Many شخصی‌سازی‌شده از UI تا Report تست شود.
- [ ] Ambiguous Timeout بدون Duplicate تست شود.
- [ ] App Credit Reserve/Commit/Release تست شود.
- [ ] Schedule و Business Hours با timezone تهران تست شوند.
- [ ] Reply 5 و Opt-out End-to-End تست شوند.
- [ ] Cross-Seller Line/Template/Customer/Report تست شود.
- [ ] هیچ Credential، شماره کامل یا متن کامل در Log نباشد.
- [ ] تمام Fixtureها و Mutationهای Authoritative سمت Frontend حذف شوند.
- [ ] Alertهای Auth/Credit/IP/Service/Unknown فعال شوند.
- [ ] تمام Acceptance Testهای ۱۴ فیچر سبز باشند.
- [ ] Sign-off محصول، فنی، QA و امنیت ثبت شود.

## معیار Done

تمام کارت‌های فیچری Done باشند، Launch Checklist Evidence داشته باشد و سیستم بدون داده Fixture آماده Production باشد.
