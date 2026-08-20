# کارت‌های فارسی Trello — اتصال پیامک باشگاه مشتریان

این فایل برای کپی‌کردن مستقیم عنوان، توضیحات و چک‌لیست هر کارت در Trello آماده شده است.

## ساختار پیشنهادی برد

**لیست‌ها:**

1. `Backlog`
2. `Ready`
3. `Doing`
4. `Code Review`
5. `QA / Staging`
6. `Done`
7. `Blocked`

**لیبل‌ها:**

- `P0 - زیرساخت`
- `P1 - ضروری لانچ`
- `Backend`
- `Database`
- `Queue/Scheduler`
- `Security`
- `SMS Provider`
- `Reports`
- `QA`

---

## کارت FND-01 — مدل داده، Tenant Isolation و Transactional Outbox

**لیبل:** `P0 - زیرساخت`, `Backend`, `Database`, `Security`

**توضیحات کارت:**

زیرساخت مشترک تمام پیامک‌ها پیاده‌سازی شود. تمام رکوردها باید `seller_id` داشته باشند و ساخت پیامک از طریق Transactional Outbox انجام شود. هیچ Worker پیامکی اجازه تغییر امتیاز، اعتبار، موجودی، جایزه یا پاسخ نظرسنجی را ندارد.

**مستند مرجع:** `docs/00-architecture-and-data-model.md`

**چک‌لیست:**

- [ ] جدول `seller_sms_profiles` ایجاد شود.
- [ ] جدول `seller_sender_lines` ایجاد شود.
- [ ] جدول versioned برای `seller_sms_templates` ایجاد شود.
- [ ] جدول `sms_outbox` با وضعیت‌ها و `idempotency_key` ایجاد شود.
- [ ] جدول یک‌ردیف‌به‌ازای‌گیرنده `sms_messages` ایجاد شود.
- [ ] جدول `customer_sms_preferences` ایجاد شود.
- [ ] جدول suppression برای محدودیت‌های زمانی ایجاد شود.
- [ ] همه کلیدهای Provider به‌صورت string ذخیره شوند.
- [ ] Unique constraintهای seller-scoped تعریف شوند.
- [ ] ساخت Business Record و Outbox در یک Transaction انجام شود.
- [ ] تست Rollback تراکنش نوشته شود.
- [ ] تست دسترسی Seller A به داده Seller B نوشته و Fail شود.
- [ ] سیاست نگهداری Snapshot سرخط، قالب و متغیرها پیاده‌سازی شود.

**معیار Done:** Migrationها اعمال شده، تست‌های تراکنش و tenant isolation سبز باشند و حداقل یک Outbox آزمایشی قابل پردازش باشد.

---

## کارت FND-02 — پیاده‌سازی Armaghan V2 Adapter

**لیبل:** `P0 - زیرساخت`, `Backend`, `SMS Provider`, `Security`

**توضیحات کارت:**

یک Adapter مستقل برای عملیات مستندشده Armaghan v2 ساخته شود. HTTP 200 به‌تنهایی موفقیت نیست و `errorModel.errorCode` باید همیشه بررسی شود.

**مستند مرجع:** `docs/01-armaghan-v2-adapter.md`

**چک‌لیست:**

- [ ] Config برای Base URL، Prefix، Username، Password و Timeout تعریف شود.
- [ ] `sendMessageOneToMany` پیاده‌سازی شود.
- [ ] `sendMessageManyToMany` پیاده‌سازی شود.
- [ ] `getMessageState` پیاده‌سازی شود.
- [ ] `getUserInfo` پیاده‌سازی شود.
- [ ] `getReceivedMessages` پیاده‌سازی شود.
- [ ] Error codeهای `-101`, `-103`, `-104`, `-105`, `-107`, `-110`, `-119`, `-201` Map شوند.
- [ ] Timeout بعد از ارسال درخواست به وضعیت `ambiguous/unknown` تبدیل شود.
- [ ] Retry فقط برای خطاهای امن و با Backoff/Jitter انجام شود.
- [ ] Circuit Breaker برای خطاهای Account-Level اضافه شود.
- [ ] لاگ‌ها Credential، متن کامل و شماره کامل نداشته باشند.
- [ ] تست Unit برای Payload و Error Mapping نوشته شود.
- [ ] تست Mock برای پاسخ موفق، خطای دائمی و Timeout مبهم نوشته شود.

**معیار Done:** Adapter از طریق Interface داخلی قابل استفاده باشد، تست‌ها سبز باشند و هیچ Credential در Log دیده نشود.

---

## کارت FND-03 — تنظیم سرخط واقعی هر فروشنده و Test Send

**لیبل:** `P0 - زیرساخت`, `Backend`, `Database`, `SMS Provider`

**توضیحات کارت:**

برای هر فروشنده فقط سرخط واقعی و از قبل تأییدشده Armaghan در دیتابیس ثبت شود. شماره تصادفی Prototype حذف شود. Seller فقط Internal ID سرخط‌های خودش را ببیند و انتخاب کند.

**مستند مرجع:** `docs/02-seller-sender-configuration.md`

**چک‌لیست:**

- [ ] API ادمین برای ثبت سرخط تأییدشده ایجاد شود.
- [ ] Originator به‌صورت string ذخیره شود.
- [ ] وضعیت‌های `pending`, `verified`, `disabled` اعمال شوند.
- [ ] برای هر Seller فقط یک Default Active Line مجاز باشد.
- [ ] API لیست سرخط‌های Seller با شماره Mask شده ایجاد شود.
- [ ] API انتخاب Default Line ایجاد شود.
- [ ] API Test Send واقعی ایجاد شود.
- [ ] Test Send با `sendMessageOneToMany` و یک گیرنده مجاز انجام شود.
- [ ] خطای `-103` سرخط را غیرفعال و Alert ایجاد کند.
- [ ] Test Send از KPI کمپین حذف ولی Audit/Cost شود.
- [ ] هیچ Originator آزاد از Frontend پذیرفته نشود.
- [ ] تست Cross-Tenant برای List/Select/Test نوشته شود.

**معیار Done:** یک Seller بتواند فقط سرخط واقعی خودش را انتخاب و تست کند و سرخط Fixture در UI/Backend وجود نداشته باشد.

---

## کارت FND-04 — قالب‌های داینامیک Seller-Scoped

**لیبل:** `P0 - زیرساخت`, `Backend`, `Database`, `Security`

**توضیحات کارت:**

قالب‌ها در دیتابیس برنامه نگهداری شوند و برای ۱۴ فیچر فعلی Template ID پنل Armaghan استفاده نشود. هر Seller برای هر Feature یک نسخه فعال مستقل داشته باشد.

**مستند مرجع:** `docs/03-dynamic-template-management.md`, `docs/19-template-id-and-binding-decision.md`

**چک‌لیست:**

- [ ] Platform Default برای هر `feature_key` تعریف شود.
- [ ] هنگام فعال‌سازی فیچر، Default به Seller Template کپی شود.
- [ ] API ساخت، ویرایش، لیست، Preview و Test قالب ایجاد شود.
- [ ] ویرایش قالب Version جدید بسازد.
- [ ] متغیرهای Canonical مانند `{name}` و `{store_name}` پیاده‌سازی شوند.
- [ ] Unknown Variable رد شود.
- [ ] Missing Required Variable رد شود.
- [ ] متغیر حل‌نشده `{...}` اجازه ارسال نداشته باشد.
- [ ] Signature قبل از کنترل طول اضافه شود.
- [ ] طول نهایی ۳۲۰ کاراکتر Server-Side کنترل شود.
- [ ] Snapshot نسخه قالب در Outbox ذخیره شود.
- [ ] Seller A نتواند Template Seller B را استفاده کند.
- [ ] برای متن یکسان One-to-Many و متن شخصی‌سازی‌شده Many-to-Many انتخاب شود.

**معیار Done:** قالب‌های مستقل Seller قابل Preview/Test باشند و هیچ Armaghan Template ID برای این Scope لازم نباشد.

---

## کارت FND-05 — سرویس مشترک Eligibility، نرمال‌سازی و اعتبار پیامک

**لیبل:** `P0 - زیرساخت`, `Backend`, `Security`, `Database`

**توضیحات کارت:**

یک سرویس مشترک برای نرمال‌سازی شماره، حذف تکراری، Opt-out، محدودیت روزانه، Business Hours، Suppression و رزرو اعتبار داخلی Seller ساخته شود تا همه فیچرها از یک منطق استفاده کنند.

**مستند مرجع:** `docs/00-architecture-and-data-model.md`

**چک‌لیست:**

- [ ] شماره‌های فارسی/عربی/لاتین نرمال شوند.
- [ ] یک فرمت Canonical برای موبایل ایران انتخاب شود.
- [ ] شماره نامعتبر قبل از رزرو اعتبار حذف شود.
- [ ] Dedupe براساس موبایل نرمال‌شده انجام شود.
- [ ] Opt-out براساس Seller و Mobile بررسی شود.
- [ ] Daily Cap و Suppression بررسی شوند.
- [ ] Business Hours براساس timezone فروشگاه بررسی شوند.
- [ ] Signature و Final Length کنترل شوند.
- [ ] App Credit از Provider Credit جدا باشد.
- [ ] Reserve/Commit/Release اعتبار داخلی پیاده‌سازی شود.
- [ ] دلیل حذف هر گیرنده در گزارش ذخیره شود.
- [ ] همان Eligibility قبل از Provider Call دوباره بررسی شود.
- [ ] تست Race برای Opt-out همزمان با Dispatch نوشته شود.

**معیار Done:** همه مسیرهای ارسال از این سرویس مشترک استفاده کنند و امکان دورزدن Opt-out/Quota/Credit وجود نداشته باشد.

---

## کارت SMS-01 — پیام خوش‌آمدگویی و ثبت مشتری حضوری

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Database`

**توضیحات کارت:**

برای عضو واقعاً جدید، مشتری و امتیاز خوش‌آمدگویی یک‌بار ثبت شوند و پیام Seller-Scoped ارسال شود. مسیر Online و Keypad حضوری از یک منطق Backend استفاده کنند.

**مستند مرجع:** `docs/04-welcome-and-walk-in.md`

**چک‌لیست:**

- [ ] API ثبت مشتری حضوری ایجاد شود.
- [ ] موبایل در محدوده Seller یکتا شود.
- [ ] Find-or-Create داخل Transaction انجام شود.
- [ ] Welcome Points Ledger فقط یک‌بار ثبت شود.
- [ ] Outbox در همان Transaction ساخته شود.
- [ ] Idempotency با `welcome:{sellerId}:{customerId}` اعمال شود.
- [ ] پیام با سرخط و قالب Seller ارسال شود.
- [ ] مشتری موجود دوباره امتیاز یا پیام Welcome نگیرد.
- [ ] Failure پیامک عضویت/امتیاز را Rollback نکند.
- [ ] Resend امتیاز جدید تولید نکند.
- [ ] Prototype Keypad به API واقعی متصل شود.
- [ ] تاریخچه پیام در گزارش مشتری نمایش داده شود.

**معیار Done:** عضو جدید دقیقاً یک امتیاز و یک Message Intent داشته باشد و Retry باعث تکرار نشود.

---

## کارت SMS-02 — کمپین دستی و زمان‌بندی‌شده

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Queue/Scheduler`, `Reports`

**توضیحات کارت:**

Seller بتواند کمپین را Preview، ایجاد، ارسال فوری/زمان‌بندی، لغو و گزارش‌گیری کند. Audience و ابزار متصل باید متعلق به همان Seller باشند.

**مستند مرجع:** `docs/05-manual-campaigns.md`

**چک‌لیست:**

- [ ] جدول Campaign، Run و Recipient ایجاد شود.
- [ ] API Preview با Gross/Eligible/Excluded/Cost ساخته شود.
- [ ] API Create/Send/Cancel/Report ساخته شود.
- [ ] Template، Sender، Audience و Linked Tool Snapshot شوند.
- [ ] زمان Local با `Asia/Tehran` به UTC تبدیل و هر دو ذخیره شوند.
- [ ] Scheduler برای Run موعدرسیده Lock بگیرد.
- [ ] Audience در زمان اجرا دوباره Resolve شود.
- [ ] Eligibility نهایی و Dedupe اجرا شود.
- [ ] App Credit قبل از Provider Call رزرو شود.
- [ ] Endpoint مناسب One-to-Many/Many-to-Many انتخاب شود.
- [ ] Idempotency هر Run/Recipient اعمال شود.
- [ ] Cancel فقط موارد ارسال‌نشده را متوقف کند.
- [ ] گزارش واقعی جایگزین درصدهای Fixture شود.

**معیار Done:** Send Now، Schedule، Cancel و Report در Staging با یک Seller واقعی و بدون Duplicate کار کنند.

---

## کارت SMS-03 — پیامک گروهی چندبخشی

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Queue/Scheduler`, `Reports`

**توضیحات کارت:**

Union چند Segment Seller ساخته شود، شماره‌ها Deduplicate و فیلتر شوند و پیام یکسان یا شخصی‌سازی‌شده با Batch امن ارسال شود.

**مستند مرجع:** `docs/06-bulk-sms.md`

**چک‌لیست:**

- [ ] API Estimate/Run/Cancel/Detail/Test ایجاد شود.
- [ ] Segment Ownership بررسی شود.
- [ ] Union اعضا ساخته شود؛ Countها مستقیم جمع نشوند.
- [ ] Dedupe موبایل نرمال‌شده انجام شود.
- [ ] Exclusion Reason ذخیره شود.
- [ ] App Credit براساس Eligible نهایی رزرو شود.
- [ ] Batch Size قابل تنظیم باشد.
- [ ] Content/Destination از یک آرایه Object ساخته شوند.
- [ ] تطابق Index در Many-to-Many تست شود.
- [ ] Overlapping Segment فقط یک پیام تولید کند.
- [ ] Test Send از KPI اصلی جدا شود.
- [ ] Timeout مبهم باعث ارسال مجدد کور نشود.
- [ ] گزارش Partial/Unknown نمایش داده شود.

**معیار Done:** تست Segmentهای هم‌پوشان، Batch Boundary و Personalized Array Alignment سبز باشد.

---

## کارت SMS-04 — پیام شخصی و مستقیم

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Security`

**توضیحات کارت:**

ارسال به یک Customer، شماره دستی مجاز، یا Segment پیاده‌سازی شود. حالت Segment باید وارد Bulk Pipeline شود و کنترل‌ها را دور نزند.

**مستند مرجع:** `docs/07-personal-messages.md`

**چک‌لیست:**

- [ ] API Preview/Send/History ساخته شود.
- [ ] Customer ID فقط در Seller جاری Resolve شود.
- [ ] Manual Mobile نرمال و Actor/Reason آن Audit شود.
- [ ] Manual Mode متغیرهای Customer را نپذیرد.
- [ ] Segment Mode به Bulk Run تبدیل شود.
- [ ] Opt-out و Daily Cap بررسی شوند.
- [ ] Idempotency با Client Command ID اعمال شود.
- [ ] ارسال تک‌گیرنده با One-to-Many انجام شود.
- [ ] از GET One-to-One استفاده نشود.
- [ ] Saved Messageها Versioned و Seller-Scoped باشند.
- [ ] Resend کنترل‌شده Message Intent جدید و مرتبط بسازد.
- [ ] شماره و متن کامل در Log قرار نگیرد.

**معیار Done:** هر سه Mode با کنترل Tenant/Consent درست کار کنند و Replay پیام تکراری نسازد.

---

## کارت SMS-05 — یادآوری عدم خرید

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Queue/Scheduler`

**توضیحات کارت:**

Ruleهای ۱ تا ۳۶۵ روز براساس آخرین سفارش Paid/Completed Seller اجرا شوند و محدودیت پیش‌فرض ۳۰ روز بین Reminderها رعایت شود.

**مستند مرجع:** `docs/08-inactivity-reminders.md`

**چک‌لیست:**

- [ ] جدول Rule و Delivery History ایجاد شود.
- [ ] API Create/Edit/Preview/Status/History ساخته شود.
- [ ] فقط Orderهای Paid/Completed مبنای Last Purchase باشند.
- [ ] Scheduler براساس timezone Seller اجرا شود.
- [ ] Lock `(rule, local date)` پیاده‌سازی شود.
- [ ] قبل از Queue خرید جدید دوباره بررسی شود.
- [ ] Suppression ۳۰ روزه اعمال شود.
- [ ] Rule Days خارج ۱ تا ۳۶۵ رد شود.
- [ ] متغیرهای Days/Points/Date از Server ساخته شوند.
- [ ] Discount Code فقط در صورت وجود واقعی Render شود.
- [ ] Idempotency Window برای هر Customer اعمال شود.
- [ ] History شامل Exclusion و Provider State باشد.

**معیار Done:** Duplicate Worker و خرید همزمان باعث Reminder اشتباه/تکراری نشوند.

---

## کارت SMS-06 — تولد و مناسبت سفارشی

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Queue/Scheduler`

**توضیحات کارت:**

پیام تولد سالانه و مناسبت دارای تاریخ/زمان/Audience اجرا شوند. تاریخ‌ها Canonical ذخیره و فقط برای UI به فارسی نمایش داده شوند.

**مستند مرجع:** `docs/09-birthday-and-occasions.md`

**چک‌لیست:**

- [ ] مدل Occasion/Run/Recipient ایجاد شود.
- [ ] Birthday به‌عنوان System Occasion غیرقابل حذف Seed شود.
- [ ] API Create/Edit/Status/Preview/History ساخته شود.
- [ ] مناسبت بدون تاریخ/زمان فعال نشود.
- [ ] سیاست Calendar و Leap Day تعیین شود.
- [ ] Scheduler در Local Time Seller اجرا شود.
- [ ] Birthday سالانه Idempotent باشد.
- [ ] Audience/Consent/Cap فیلتر شوند.
- [ ] Discount Code جعلی Render نشود.
- [ ] Template/Sender Snapshot ذخیره شود.
- [ ] Business-Hour Adjustment ثبت شود.
- [ ] گزارش Run واقعی ساخته شود.

**معیار Done:** یک Customer در یک Seller در هر سال فقط یک Birthday Intent دریافت کند و تست Leap Day سبز باشد.

---

## کارت SMS-07 — اعلان انقضای امتیاز

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Database`, `Queue/Scheduler`

**توضیحات کارت:**

اعلان انقضا براساس Points Lotهای دارای Remaining Amount ساخته شود؛ نه فقط Balance کل. خرج‌شدن همزمان امتیاز باید قبل از Dispatch دوباره بررسی شود.

**مستند مرجع:** `docs/10-points-expiry.md`

**چک‌لیست:**

- [ ] Points Lot و Remaining/Expiry قابل Query باشند.
- [ ] Settings روز هشدار و ساعت ارسال ایجاد شود.
- [ ] API Settings/Preview/History ساخته شود.
- [ ] Lotهای یک Customer/Expiry Date طبق Policy تجمیع شوند.
- [ ] Lot خرج‌شده/Reversed/Expired حذف شود.
- [ ] Transaction Snapshot برای مبلغ انقضا ساخته شود.
- [ ] قبل از Provider Call Remaining دوباره بررسی شود.
- [ ] Idempotency Seller/Customer/Expiry Date اعمال شود.
- [ ] متغیرهای Points/Balance/Date از Ledger ساخته شوند.
- [ ] Race Test با خرج همزمان نوشته شود.
- [ ] Failure پیامک هیچ Pointی تغییر ندهد.
- [ ] History به Lot IDها متصل باشد.

**معیار Done:** پیام فقط برای امتیاز واقعاً باقی‌مانده Queue شود و Race با Spend کنترل شده باشد.

---

## کارت SMS-08 — اعلان Retargeting و Cashback

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Database`, `Queue/Scheduler`

**توضیحات کارت:**

پس از ثبت قطعی اعتبار بازگشت/Cashback و قبل از انقضای اعتبار استفاده‌نشده، اعلان Seller-Scoped ارسال شود. SMS Worker به Ledger مالی دست نزند.

**مستند مرجع:** `docs/11-retargeting-notifications.md`

**چک‌لیست:**

- [ ] Credit Ledger و Notification Record ایجاد شود.
- [ ] Grant Ruleها Server-Side محاسبه شوند.
- [ ] Grant و Outbox در یک Transaction ساخته شوند.
- [ ] Manual Grant شامل Actor و Reason باشد.
- [ ] Grant Message با Credit ID Idempotent باشد.
- [ ] Expiry Scheduler فقط Remaining مثبت را انتخاب کند.
- [ ] Credit مصرف‌شده/منقضی/Reversed حذف شود.
- [ ] Grant و Expiry Template جدا باشند.
- [ ] Amount/Date از Snapshot Ledger Render شوند.
- [ ] Failure پیامک Credit را حذف/تکرار نکند.
- [ ] Reversal یک Ledger Event جدا باشد.
- [ ] History به Credit و Provider Reference متصل شود.

**معیار Done:** یک Source فقط یک Credit و یک Grant Notification Intent تولید کند.

---

## کارت SMS-09 — پیام دعوت و پاداش Referral

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Security`

**توضیحات کارت:**

لینک دعوت امن و Seller-Scoped ارسال شود و پاداش فقط بعد از Qualification معتبر و یک‌بار ثبت شود.

**مستند مرجع:** `docs/12-referral-messages.md`

**چک‌لیست:**

- [ ] مدل Referral، Invite و Reward ایجاد شود.
- [ ] Token/Link تصادفی، Signed و Expiring باشد.
- [ ] API ارسال دعوت ایجاد شود.
- [ ] Self-Referral رد شود.
- [ ] Rate Limit روزانه Inviter/Destination/IP اعمال شود.
- [ ] Token فقط در Seller خودش Resolve شود.
- [ ] Qualification ثبت‌نام/اولین خرید معتبر بررسی شود.
- [ ] Reward Ledgerها اتمیک و Unique باشند.
- [ ] Reward Outbox در همان Transaction ساخته شود.
- [ ] متن فقط Reward واقعاً تنظیم‌شده را وعده دهد.
- [ ] Failure پیامک Reward را تکرار/برگشت ندهد.
- [ ] تست Abuse و Cross-Seller نوشته شود.

**معیار Done:** Replay Qualification یا Token نتواند پاداش دوباره یا Cross-Tenant ایجاد کند.

---

## کارت SMS-10 — پیام دعوت گردونه و اعلام برنده

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Security`, `Database`

**توضیحات کارت:**

دعوت با لینک امن ارسال شود و پیام برنده فقط بعد از Spin قطعی Server-Side ساخته شود. نتیجه JavaScript Prototype معتبر نیست.

**مستند مرجع:** `docs/13-wheel-messages.md`

**چک‌لیست:**

- [ ] Ownership/Active Period گردونه بررسی شود.
- [ ] تعداد جایزه ۲ تا ۸ و مجموع Chance دقیقاً ۱۰۰٪ باشد.
- [ ] Invitation Link Seller/Wheel/Customer Scoped باشد.
- [ ] Daily Spin Cap Server-Side اعمال شود.
- [ ] Entry Cost و Participation Reward جدا باشند.
- [ ] Spin با Secure Randomness Server-Side انجام شود.
- [ ] Points/Prize/Code/Outbox در یک Transaction ثبت شوند.
- [ ] Spin Command Idempotent باشد.
- [ ] Winner Message از Prize Snapshot ساخته شود.
- [ ] SMS Failure باعث Reroll/Reaward نشود.
- [ ] Resend همان Code را استفاده کند.
- [ ] گزارش Invitation/Winner با Provider Reference ساخته شود.

**معیار Done:** Duplicate Spin دقیقاً یک Outcome و یک Message Intent داشته باشد.

---

## کارت SMS-11 — دعوت و یادآوری نظرسنجی

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Security`, `Queue/Scheduler`

**توضیحات کارت:**

برای هر گیرنده لینک امن اختصاصی ارسال شود، پاسخ و پاداش حداکثر یک‌بار ثبت شوند و Reminder فقط برای Non-Respondentهای Run اولیه ارسال شود.

**مستند مرجع:** `docs/14-survey-messages.md`

**چک‌لیست:**

- [ ] Survey دارای ۲ تا ۶ Option معتبر باشد.
- [ ] Run/Audience/Template Snapshot شود.
- [ ] Token اختصاصی Seller/Survey/Run/Customer ساخته شود.
- [ ] Invitation با Many-to-Many و لینک‌های هم‌تراز ارسال شود.
- [ ] Public GET/POST Token Endpoint ساخته شود.
- [ ] Token Signature/Expiry/Scope بررسی شود.
- [ ] Option متعلق به Snapshot Survey باشد.
- [ ] یک Response و یک Reward حداکثر ثبت شود.
- [ ] Response/Reward اتمیک باشند.
- [ ] Reminder فقط Recipientهای دعوت‌شده و بدون پاسخ را بگیرد.
- [ ] Survey پایان‌یافته رفتار مشخص داشته باشد.
- [ ] Funnel Invite/Delivery/Response واقعی گزارش شود.

**معیار Done:** یک Customer نتواند دوبار پاسخ/پاداش بگیرد و Respondent Reminder دریافت نکند.

---

## کارت SMS-12 — تأیید پیامکی خرید از Club

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Database`, `Security`

**توضیحات کارت:**

کسر امتیاز، کاهش موجودی، ساخت Redemption و Code و Outbox در یک Transaction انجام شوند. پیام شکست‌خورده نباید Redemption را ناقص کند.

**مستند مرجع:** `docs/15-club-redemption.md`

**چک‌لیست:**

- [ ] API Redemption و Resend ساخته شود.
- [ ] Seller/Customer/Item Ownership بررسی شود.
- [ ] Stock و Point Balance Lock/Version شوند.
- [ ] Active/Stock/Balance/Daily Cap بررسی شوند.
- [ ] Client Command ID یکتا باشد.
- [ ] Points Ledger و Stock Update اتمیک باشند.
- [ ] Redemption Code امن و یکتا ساخته شود.
- [ ] Outbox در همان Transaction ساخته شود.
- [ ] UI بلافاصله Code قطعی را نمایش دهد.
- [ ] Message از Snapshot Item/Cost/Balance ساخته شود.
- [ ] Resend همان Redemption/Code را استفاده کند.
- [ ] تست Concurrent Redemption نوشته شود.

**معیار Done:** Double Click و همزمانی Stock/Points باعث خرید یا پیام تکراری نشوند.

---

## کارت SMS-13 — Polling وضعیت و گزارش تحویل

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Reports`, `Queue/Scheduler`

**توضیحات کارت:**

Referenceهای Armaghan ذخیره و با `getMessageState` Poll شوند. درصدها و Countهای Fixture Prototype با داده واقعی جایگزین شوند.

**مستند مرجع:** `docs/16-delivery-reports.md`

**چک‌لیست:**

- [ ] Referenceها به‌صورت string ذخیره شوند.
- [ ] تعداد Reference و Destination برابر بودنشان Validate شود.
- [ ] Reference Index به Recipient درست Map شود.
- [ ] Poll Worker برای Stateهای Non-Terminal ساخته شود.
- [ ] Stateهای ۰ تا ۶ و `-100` Map شوند.
- [ ] State Terminal با پاسخ قدیمی Regression نکند.
- [ ] Poll Interval و Max Age قابل تنظیم باشند.
- [ ] Unknown/Reference Not Found قابل مشاهده باشند.
- [ ] API Summary/Run/Message Detail ساخته شود.
- [ ] Denominator نرخ تحویل مشخص و Label شود.
- [ ] Report Query همیشه Seller-Scoped باشد.
- [ ] Totals با Recipient Rowها Reconcile شوند.

**معیار Done:** Run آزمایشی از Accepted تا Delivered/Not Delivered قابل ردیابی و گزارش باشد.

---

## کارت SMS-14 — دریافت پیام و Opt-out با پاسخ ۵

**لیبل:** `P1 - ضروری لانچ`, `Backend`, `Security`, `Queue/Scheduler`

**توضیحات کارت:**

پیام‌های دریافتی با `getReceivedMessages` Poll شوند، براساس Destination Line به Seller درست Route شوند و پاسخ ۵ بازاریابی همان Seller را غیرفعال کند.

**مستند مرجع:** `docs/17-inbound-opt-out.md`

**چک‌لیست:**

- [ ] Checkpoint جدا برای هر Provider Account ایجاد شود.
- [ ] Inbox Provider ID یکتا ذخیره شود.
- [ ] Page کامل قبل از Advance Checkpoint Durable شود.
- [ ] Destination به `seller_sender_lines` Resolve شود.
- [ ] Destination ناشناخته وارد Dead-Letter شود.
- [ ] اعداد `5`, `۵`, `٥` یکسان Normalize شوند.
- [ ] Stop Words دقیق و Review شده باشند.
- [ ] از Substring Match وسیع جلوگیری شود.
- [ ] Preference Marketing Opt-out Seller-Scoped Upsert شود.
- [ ] پیام‌های Marketing ارسال‌نشده Cancel شوند.
- [ ] Dispatch آخرین‌لحظه Preference را دوباره بررسی کند.
- [ ] Raw Inbound Content دسترسی و Retention محدود داشته باشد.
- [ ] تست Opt-out Seller A و عدم اثر روی Seller B نوشته شود.

**معیار Done:** Reply 5 فقط Marketing همان Seller را متوقف کند و Race با Queue قابل دورزدن نباشد.

---

## کارت REL-01 — QA نهایی، امنیت و آماده‌سازی لانچ

**لیبل:** `P0 - زیرساخت`, `QA`, `Security`, `Reports`

**توضیحات کارت:**

تمام موارد Launch Checklist در Staging با سرخط تأییدشده و شماره‌های تست مجاز اجرا و Evidence ثبت شود.

**مستند مرجع:** `docs/18-launch-checklist.md`

**چک‌لیست:**

- [ ] Credential قبلی Rotate و Secret Manager فعال شود.
- [ ] هیچ Secret یا شماره واقعی در Repo/Log/Test نباشد.
- [ ] Migrationها و Rollback آنها تست شوند.
- [ ] One-to-Many واقعی در Staging تست شود.
- [ ] Many-to-Many شخصی‌سازی‌شده تست شود.
- [ ] Reference Mapping و Delivery Poll تست شوند.
- [ ] Ambiguous Timeout سناریو تست شود.
- [ ] Opt-out با پاسخ ۵ End-to-End تست شود.
- [ ] Tenant Isolation برای Line/Template/Customer/Report تست شود.
- [ ] App Credit Reserve/Release/Reconcile تست شود.
- [ ] Schedulerها با timezone تهران تست شوند.
- [ ] Dashboard/Sheets از Fixture به API واقعی منتقل شوند.
- [ ] Alert برای Auth/Credit/IP/Service/Unknown فعال شود.
- [ ] تمام چک‌لیست‌های Feature Cardها بسته شوند.
- [ ] Sign-off فنی، QA، امنیت و محصول ثبت شود.

**معیار Done:** همه موارد مرتبط `docs/18-launch-checklist.md` Evidence و تأیید داشته باشند و هیچ Fixture یا Mutation سمت Frontend منبع حقیقت نباشد.
