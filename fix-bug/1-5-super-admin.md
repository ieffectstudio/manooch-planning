# Full PRD: Manooch Super Admin Panel Restructuring

## Document Info
| Field | Value |
|---|---|
| **Product** | Manooch Super Admin Panel |
| **Version** | 2.0 |
| **Author** | Product Team |
| **Date** | 2025 |
| **Status** | Draft for Review |

---

## 1. Executive Summary

Manooch is an **e-commerce SaaS platform** that provides online stores to sellers. The Super Admin panel is the internal management dashboard used by the Manooch team to manage stores, subscriptions, plugins, and platform-level orders (plan purchases). 

This PRD addresses critical UX and architectural issues in the current Super Admin panel:

1. **Store Edit Page** — Missing plugins, poor tab UI, no toggle/plan management, no business/personalization config
2. **Orders Page** — Shows all customer orders across stores (irrelevant); should only show Manooch's own plan/subscription orders
3. **Sellers Menu** — Redundant; should be merged into the Store entity (1 seller = 1 store)

---

## 2. Problem Statements

### Problem 1: Store Edit Page — Incomplete Plugin Coverage
**Current State:** The store edit page shows a limited set of tabs (اطلاعات کلی, افزونه‌ها, دامنه, درگاه پرداخت, محصولات, سفارش‌ها, بنرها, گالری, سوالات متداول, تخفیف‌ها, نظرات, تیم, دنبال‌کنندگان, مشتریان).

**Issue:** The store's actual plugin ecosystem (image 2) includes additional plugins: کالا, دسته‌بندی, ویژگی‌ها, واحدها, بنر, کارت بانکی, اخبار, گالری, مشتریان, نظرات, سوالات, تیم, تخفیف, ارسال, افزونه. As Super Admin, **all installed and available plugins** should be visible and manageable.

### Problem 2: Store Edit Page — No Toggle & No Plan Management
**Current State:** The "Basic Info" section displays store status as a static badge ("فعال") and plan as a static label ("بدون پلن"). 

**Issue:** Super Admin cannot:
- Toggle store active/inactive directly
- Change or assign a subscription plan from this view

### Problem 3: Store Edit Page — Tab UI Doesn't Scale
**Current State:** Horizontal tab bar with 14+ tabs.

**Issue:** With all plugins represented, this could grow to 20+ tabs. Horizontal scrolling tabs are:
- Hard to navigate
- Items get hidden off-screen
- No visual grouping or hierarchy

### Problem 4: Store Edit Page — No Business & Personalization Config
**Current State:** No section for business-specific settings (tax config, invoice settings, store policies, SEO, branding, theme, custom domain settings, notification preferences, etc.)

**Issue:** Seller-facing configuration options that affect the store's business behavior and appearance are not manageable by Super Admin.

### Problem 5: Orders Page — Wrong Scope
**Current State:** The orders page (سفارش‌ها) in the sidebar shows "نمای سراسری سفارش‌های ثبت‌شده در تمام فروشگاه‌ها" — all customer orders from all stores.

**Issue:** Manooch is a SaaS platform, not a marketplace aggregator. Viewing end-customer orders across all stores provides no value. The Super Admin's "orders" should be **Manooch's own orders** — i.e., stores purchasing subscription plans, add-on plugins, and services from Manooch.

### Problem 6: Sellers Menu — Redundant Entity
**Current State:** Sidebar has a separate "فروشندگان" (Sellers) menu item alongside "فروشگاه‌ها" (Stores).

**Issue:** Each seller is bound to exactly one store (1:1 relationship). Maintaining a separate sellers list creates:
- Data fragmentation
- Confusion about where to find/edit seller info
- Redundant navigation

---

## 3. Goals & Success Metrics

| Goal | Success Metric |
|---|---|
| Super Admin can manage all plugin data for any store from one page | 100% of installed plugins accessible in store edit view |
| Super Admin can toggle store status inline | Toggle action completes in < 1 second with confirmation |
| Super Admin can change store plan inline | Plan change reflected immediately; billing event triggered |
| Store edit page scales to 20+ sections without UX degradation | No horizontal overflow; all sections discoverable within 2 clicks |
| Orders page shows only Manooch plan orders | Zero end-customer orders visible; only subscription/plan purchase orders shown |
| Seller data merged into store | "فروشندگان" menu removed; seller info lives inside store detail |
| Business/personalization config accessible | Super Admin can view and override all seller-configurable settings |

---

## 4. Scope

### In Scope
- Redesign Store Edit page layout and navigation
- Add all plugins as manageable sections
- Add store toggle (active/inactive)
- Add inline plan management (view/change/assign plan)
- Add business config and personalization sections
- Redesign Orders page to show only Manooch platform orders (plan purchases)
- Remove Sellers sidebar menu
- Merge seller data into Store entity
- Update sidebar navigation

### Out of Scope
- Seller-facing panel changes (this PRD covers Super Admin only)
- Plugin marketplace / plugin installation flow redesign
- Billing engine changes (only the admin UI for assigning plans is in scope)
- End-customer order management (this is the store's responsibility)

---

## 5. Detailed Requirements

---

### 5.1 Remove "فروشندگان" (Sellers) Menu & Merge into Store

#### 5.1.1 Data Model Change
Each Store already has an owner. The seller entity should be **absorbed** into the Store entity:

```
Store {
  id
  name
  domain
  plan
  status (active/inactive/suspended)
  created_at
  
  // Merged from Seller:
  owner {
    id
    full_name
    mobile
    email
    national_id
    avatar
    date_joined
    identity_verified (boolean)
    bank_account_info {
      iban
      account_holder_name
      bank_name
    }
  }
  
  // Stats
  stats {
    total_orders
    total_products
    total_followers
    total_revenue
  }
  
  // ... plugins, config, etc.
}
```

#### 5.1.2 Sidebar Navigation Change

**Current Sidebar:**
```
اصلی
  ├── داشبورد
  ├── فروشگاه‌ها
  ├── فروشندگان        ← REMOVE
  ├── اشتراک‌ها و پلن‌ها
  ├── سفارش‌ها          ← REDEFINE
  ├── گزارش‌ها
پلتفرم
  ├── افزونه‌ها
  ├── دسته‌بندی‌ها
  ├── دعوت‌ها
  ├── کاربران پنل
  ├── تنظیمات
توسعه
  └── پایه‌های طراحی
```

**New Sidebar:**
```
اصلی
  ├── داشبورد
  ├── فروشگاه‌ها                    (stores list + edit)
  ├── اشتراک‌ها و پلن‌ها             (plan definitions)
  ├── سفارش‌های پلتفرم              ← RENAMED & REDEFINED
  ├── گزارش‌ها
پلتفرم
  ├── افزونه‌ها
  ├── دسته‌بندی‌ها
  ├── دعوت‌ها
  ├── کاربران پنل
  ├── تنظیمات
توسعه
  └── پایه‌های طراحی
```

#### 5.1.3 Migration of Existing Seller Data
- All existing seller profiles are linked to their store
- Any seller list views now become filterable from the stores list
- Seller-specific data (national ID, bank account, verification status) appears in the "Owner & Seller Info" section of the Store Edit page

---

### 5.2 Store Edit Page — Complete Redesign

#### 5.2.1 Layout: Replace Tabs with Left Sidebar Section Navigation

**Why:** Tabs don't scale. With 20+ sections, a vertical sidebar navigation (within the page) is far superior.

**New Layout Structure:**

```
┌─────────────────────────────────────────────────────────────────────┐
│  Breadcrumb: فروشگاه‌ها / تست                                       │
│                                                                     │
│  ┌──────────┐  تست  [فعال ● Toggle Switch]                         │
│  │  Store    │  test-shipo.manooch.com                              │
│  │  Avatar   │  پلن: رایگان  [تغییر پلن]                            │
│  └──────────┘                                                       │
├───────────────────┬─────────────────────────────────────────────────┤
│  Section Nav      │  Content Area                                   │
│  (Vertical List)  │                                                 │
│                   │                                                 │
│  ▸ اطلاعات کلی    │   [Dynamic content based on selected section]   │
│  ▸ مالک فروشگاه   │                                                 │
│  ▸ پلن و اشتراک   │                                                 │
│  ▸ دامنه          │                                                 │
│  ▸ درگاه پرداخت   │                                                 │
│                   │                                                 │
│  ── افزونه‌ها ──   │                                                 │
│  ▸ کالا           │                                                 │
│  ▸ دسته‌بندی       │                                                 │
│  ▸ ویژگی‌ها       │                                                 │
│  ▸ واحدها         │                                                 │
│  ▸ محصولات        │                                                 │
│  ▸ سفارش‌ها       │                                                 │
│  ▸ بنرها          │                                                 │
│  ▸ گالری          │                                                 │
│  ▸ اخبار          │                                                 │
│  ▸ تخفیف‌ها       │                                                 │
│  ▸ نظرات          │                                                 │
│  ▸ سوالات متداول  │                                                 │
│  ▸ کارت بانکی     │                                                 │
│  ▸ ارسال          │                                                 │
│  ▸ تیم            │                                                 │
│  ▸ مشتریان        │                                                 │
│  ▸ دنبال‌کنندگان  │                                                 │
│                   │                                                 │
│  ── تنظیمات ──    │                                                 │
│  ▸ تنظیمات کسب‌وکار│                                                │
│  ▸ شخصی‌سازی      │                                                 │
│  ▸ سئو            │                                                 │
│  ▸ اعلان‌ها       │                                                 │
│                   │                                                 │
│  ── خطر ──        │                                                 │
│  ▸ تعلیق/حذف     │                                                 │
└───────────────────┴─────────────────────────────────────────────────┘
```

#### 5.2.2 Store Header (Always Visible)

The top section of the store edit page is **always visible** regardless of which section is selected.

| Element | Description | Behavior |
|---|---|---|
| Store Avatar | Store logo/image | Clickable to view full size |
| Store Name | e.g., "تست" | Display only (editable in Basic Info section) |
| Domain | e.g., "test-shipo.manooch.com" | Display only (editable in Domain section) |
| Status Toggle | Active / Inactive switch | **Toggle switch** — clicking triggers confirmation modal: "آیا از غیرفعال کردن فروشگاه مطمئنید؟" → On confirm: API call to change status, toast notification |
| Current Plan Badge | e.g., "رایگان", "حرفه‌ای", "بدون پلن" | Badge with color coding |
| Change Plan Button | "تغییر پلن" | Opens plan selection modal (see 5.2.4) |
| Creation Date | e.g., "1405/05/01" | Display only |
| Quick Stats | Orders count, Products count, Followers count, Revenue | Display only, real-time |

#### 5.2.3 Section Navigation (Left Sidebar within Page)

**Grouped Sections:**

**Group 1: Core Info (اطلاعات اصلی)**
| Section | Content |
|---|---|
| اطلاعات کلی | Store name (editable), description, logo upload, category/industry, contact info (phone, email, address) |
| مالک فروشگاه | Owner name, mobile, email, national ID, avatar, identity verification status, bank account info (IBAN, holder name, bank), date joined. **All merged from the old Seller entity.** |
| پلن و اشتراک | Current plan details, plan history, plan expiry date, usage metrics (products used/limit, storage used/limit, etc.), manual plan override, billing history for this store |
| دامنه | Current domain, custom domain settings, SSL status, DNS records |
| درگاه پرداخت | Connected payment gateways, gateway credentials (masked), transaction summary |

**Group 2: Plugins (افزونه‌ها)**

This group dynamically lists **all plugins that exist on the platform**, showing each plugin's data for this specific store. For plugins not yet activated on the store, show an "inactive" state with option to activate.

| Section | Content |
|---|---|
| کالا (Products) | Product list for this store, add/edit/delete products, inventory status |
| دسته‌بندی (Categories) | Store's product categories, tree view, add/edit/delete |
| ویژگی‌ها (Attributes) | Product attributes/variants configuration |
| واحدها (Units) | Measurement units configured for this store |
| محصولات (Catalog) | Full catalog management if different from کالا |
| سفارش‌های فروشگاه (Store Orders) | **Read-only view** of this store's customer orders (for support/debugging purposes only) |
| بنرها (Banners) | Banner management for the store's frontend |
| گالری (Gallery) | Media library / gallery items |
| اخبار (News/Blog) | Store's blog/news posts |
| تخفیف‌ها (Discounts) | Discount codes, campaigns, rules |
| نظرات (Reviews) | Customer reviews on products |
| سوالات متداول (FAQ) | FAQ entries |
| کارت بانکی (Bank Cards) | Stored bank card configurations |
| ارسال (Shipping) | Shipping methods, zones, rates, courier integrations |
| تیم (Team) | Team members with roles and permissions within the store |
| مشتریان (Customers) | Customer list for this store |
| دنبال‌کنندگان (Followers) | Follower list / social followers |

> **Important:** This list must be **dynamically generated** from the platform's plugin registry. When a new plugin is added to the Manooch platform, it should automatically appear in this section nav for every store (showing its installed/not-installed state).

Each plugin section shows:
- **Installed status** badge (فعال / غیرفعال)
- If installed: Full data management UI
- If not installed: "This plugin is not active for this store" message + "Activate" button (if super admin wants to force-activate)

**Group 3: Business & Personalization Config (تنظیمات کسب‌وکار و شخصی‌سازی)**

This is the **new section** that doesn't exist in the current design.

| Section | Content |
|---|---|
| تنظیمات کسب‌وکار (Business Settings) | Tax configuration (tax rate, tax ID, tax-inclusive pricing), Invoice settings (invoice prefix, auto-numbering, footer text), Store policies (return policy, privacy policy, terms of service — text editor), Working hours / availability, Currency settings, Minimum order amount, Order confirmation method (auto/manual) |
| شخصی‌سازی (Personalization) | Theme selection / current theme, Color palette (primary, secondary, accent colors), Font selection, Homepage layout configuration, Custom CSS (read-only view of what seller has set), Favicon, Social media links (Instagram, Telegram, WhatsApp, etc.) |
| سئو (SEO) | Meta title, meta description, Open Graph settings, Google Analytics tracking ID, Google Search Console verification, Sitemap settings, Robots.txt config |
| اعلان‌ها (Notifications) | SMS notification settings (which events trigger SMS), Email notification settings, Push notification settings, Notification templates preview |

**Group 4: Danger Zone (ناحیه خطر)**

| Section | Content |
|---|---|
| تعلیق / حذف (Suspend / Delete) | Suspend store (temporary, reversible) — with reason field. Delete store (permanent, irreversible) — requires typing store name to confirm. Transfer ownership — assign store to different owner. Data export — trigger full data export for the store. |

#### 5.2.4 Plan Change Modal

When Super Admin clicks "تغییر پلن":

```
┌──────────────────────────────────────────┐
│         تغییر پلن فروشگاه                │
│         Store: تست (test-shipo)           │
│                                          │
│  پلن فعلی: بدون پلن                      │
│                                          │
│  انتخاب پلن جدید:                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │  رایگان   │ │  پایه    │ │ حرفه‌ای  │ │
│  │  Free     │ │ 99,000/mo│ │299,000/mo│ │
│  │ 10 product│ │100 produc│ │Unlimited │ │
│  │ 100MB     │ │ 1GB      │ │ 10GB     │ │
│  │  [فعلی]   │ │ [انتخاب] │ │ [انتخاب] │ │
│  └──────────┘ └──────────┘ └──────────┘ │
│                                          │
│  ┌──────────┐                            │
│  │  سازمانی  │                            │
│  │Enterprise │                            │
│  │  Custom   │                            │
│  │ [انتخاب]  │                            │
│  └──────────┘                            │
│                                          │
│  تاریخ شروع: [__________] (Jalali picker)│
│  تاریخ پایان: [__________]               │
│  یادداشت: [________________________]     │
│                                          │
│  ⚠️ این تغییر بلافاصله اعمال می‌شود       │
│                                          │
│  [انصراف]              [اعمال تغییرات]    │
└──────────────────────────────────────────┘
```

**Fields:**
- Plan selection (radio/card selection)
- Start date (defaults to now)
- End date (defaults based on plan billing cycle)
- Admin note (optional, for internal tracking)
- Billing impact warning (if downgrading, shows what features will be lost)

**Behavior:**
- On confirm: API call to update store plan
- Creates a billing record / platform order (ties into the new Orders page)
- Sends notification to store owner
- Logs the action in audit trail

#### 5.2.5 Status Toggle Behavior

| Action | Flow |
|---|---|
| Activate (غیرفعال → فعال) | Toggle → Confirmation: "فروشگاه فعال شود؟" → API call → Success toast → Badge updates to green "فعال" |
| Deactivate (فعال → غیرفعال) | Toggle → Modal with reason field (required): "دلیل غیرفعال‌سازی" + dropdown (violation, non-payment, owner request, other) → API call → Success toast → Badge updates to red "غیرفعال" → Notification sent to store owner |
| Suspend | Available in Danger Zone section → More severe than deactivation → Blocks all store operations and API access |

---

### 5.3 Orders Page — Redefine as Platform Orders

#### 5.3.1 New Definition

**Old:** "نمای سراسری سفارش‌های ثبت‌شده در تمام فروشگاه‌ها" (All customer orders across all stores)

**New:** "سفارش‌های پلتفرم — خرید پلن‌ها و سرویس‌های منوچ" (Platform Orders — Manooch Plan & Service Purchases)

This page shows orders where **Manooch is the seller** and **stores/sellers are the buyers**. These are:

1. **Plan subscriptions** — When a store purchases/upgrades a plan
2. **Plan renewals** — Recurring subscription payments
3. **Add-on purchases** — When a store buys additional plugins, storage, features
4. **Custom service orders** — Custom development, design, consulting services

#### 5.3.2 Orders List View

```
┌─────────────────────────────────────────────────────────────────┐
│  سفارش‌های پلتفرم                                                │
│  خرید پلن‌ها و سرویس‌های منوچ توسط فروشگاه‌ها                    │
│                                                                 │
│  [+ ثبت سفارش جدید]       [فیلتر ▼]  [خروجی اکسل]             │
│                                                                 │
│  Filters:                                                       │
│  [نوع سفارش ▼] [وضعیت ▼] [فروشگاه ▼] [تاریخ از-تا]           │
│                                                                 │
│  ┌─────┬──────────┬───────────┬─────────┬────────┬──────────┐  │
│  │ شماره│ فروشگاه  │ نوع سفارش │  مبلغ   │ وضعیت  │  تاریخ   │  │
│  ├─────┼──────────┼───────────┼─────────┼────────┼──────────┤  │
│  │ 1001│ تست      │ خرید پلن  │ 99,000  │ پرداخت │ 1405/5/1 │  │
│  │     │          │ حرفه‌ای   │  تومان  │  شده   │          │  │
│  ├─────┼──────────┼───────────┼─────────┼────────┼──────────┤  │
│  │ 1002│ شاپ من   │ تمدید پلن │ 99,000  │ در انتظار│1405/5/3│  │
│  │     │          │ پایه      │  تومان  │ پرداخت │          │  │
│  ├─────┼──────────┼───────────┼─────────┼────────┼──────────┤  │
│  │ 1003│ دیجیتال  │ افزونه    │ 29,000  │ لغو شده│ 1405/5/5│  │
│  │     │          │ ارسال     │  تومان  │        │          │  │
│  └─────┴──────────┴───────────┴─────────┴────────┴──────────┘  │
│                                                                 │
│  Showing 1-10 of 156 orders          [< 1 2 3 ... 16 >]       │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.3.3 Order Types

| Order Type | Description |
|---|---|
| خرید پلن (Plan Purchase) | First-time plan subscription |
| تمدید پلن (Plan Renewal) | Recurring renewal of existing plan |
| ارتقای پلن (Plan Upgrade) | Upgrading from lower to higher plan |
| تنزل پلن (Plan Downgrade) | Downgrading plan (with prorated refund) |
| خرید افزونه (Add-on Purchase) | Purchasing individual plugin/feature |
| سرویس سفارشی (Custom Service) | Custom development or consulting |

#### 5.3.4 Order Statuses

| Status | Color | Description |
|---|---|---|
| جدید (New) | Blue | Order created, awaiting payment |
| در انتظار پرداخت (Awaiting Payment) | Yellow | Invoice sent, payment pending |
| پرداخت شده (Paid) | Green | Payment confirmed |
| فعال‌سازی شده (Activated) | Green | Plan/service activated post-payment |
| لغو شده (Cancelled) | Red | Order cancelled |
| بازپرداخت شده (Refunded) | Gray | Payment refunded |
| منقضی شده (Expired) | Gray | Payment window expired |

#### 5.3.5 Create New Order (ثبت سفارش جدید)

Super Admin can manually create a platform order for a store:

```
┌──────────────────────────────────────────┐
│         ثبت سفارش جدید                    │
│                                          │
│  فروشگاه: [Search & Select Store ▼]      │
│                                          │
│  نوع سفارش: [Select Type ▼]             │
│    ○ خرید پلن                            │
│    ○ تمدید پلن                           │
│    ○ ارتقای پلن                          │
│    ○ خرید افزونه                         │
│    ○ سرویس سفارشی                        │
│                                          │
│  (If plan selected:)                     │
│  پلن: [Select Plan ▼]                   │
│  مدت: [1 ماهه / 3 ماهه / 6 ماهه / سالانه]│
│                                          │
│  (If add-on selected:)                   │
│  افزونه: [Select Plugin ▼]              │
│                                          │
│  مبلغ: [__________] تومان               │
│  تخفیف: [__________] تومان (اختیاری)     │
│  مبلغ نهایی: [auto-calculated]           │
│                                          │
│  روش پرداخت:                             │
│    ○ درگاه آنلاین                        │
│    ○ کارت به کارت                        │
│    ○ رایگان (هدیه/پروموشن)               │
│                                          │
│  یادداشت: [________________________]     │
│                                          │
│  [انصراف]              [ثبت سفارش]       │
└──────────────────────────────────────────┘
```

#### 5.3.6 Order Detail View

Clicking an order opens its detail:

| Field | Description |
|---|---|
| Order Number | Auto-generated unique ID |
| Store | Link to store edit page |
| Owner | Owner name & mobile (from merged seller data) |
| Order Type | Plan/Renewal/Upgrade/Add-on/Custom |
| Item Details | Plan name, duration, features included |
| Amount | Original amount |
| Discount | Discount amount & code if applicable |
| Final Amount | Amount after discount |
| Payment Status | Current status with timeline |
| Payment Method | Online gateway / Card transfer / Free |
| Payment Reference | Transaction ID / transfer receipt |
| Created Date | Order creation date |
| Paid Date | Payment confirmation date |
| Activation Date | Service activation date |
| Expiry Date | Plan/service expiry date |
| Admin Notes | Internal notes |
| Audit Log | All status changes with timestamps and actor |

**Actions Available:**
- Mark as Paid (if awaiting payment)
- Activate Service (if paid but not activated)
- Cancel Order
- Issue Refund
- Extend Expiry Date
- Add Note
- Send Payment Reminder to Store Owner

---

### 5.4 Updated Sidebar Navigation — Final State

```
اصلی
  ├── داشبورد
  │     └── Platform KPIs, revenue overview, active stores count,
  │         recent platform orders, expiring plans
  │
  ├── فروشگاه‌ها
  │     ├── List View (all stores with filters)
  │     └── Store Detail/Edit (new layout per 5.2)
  │
  ├── اشتراک‌ها و پلن‌ها
  │     ├── Plan Definitions (create/edit plans)
  │     ├── Plan Features Matrix
  │     └── Pricing Management
  │
  ├── سفارش‌های پلتفرم                     ← REDEFINED
  │     ├── All Platform Orders
  │     ├── New Order
  │     └── Order Detail
  │
  ├── گزارش‌ها
  │     ├── Revenue Reports
  │     ├── Store Growth Reports
  │     ├── Plugin Usage Reports
  │     └── Churn Reports
  │
پلتفرم
  ├── افزونه‌ها (Platform Plugin Registry)
  ├── دسته‌بندی‌ها (Platform Categories)
  ├── دعوت‌ها (Invitations)
  ├── کاربران پنل (Admin Users)
  ├── تنظیمات (Platform Settings)
  │
توسعه
  └── پایه‌های طراحی (Design System)
```

> **Note: "فروشندگان" is completely removed.** All seller information is accessed through فروشگاه‌ها → Store Detail → مالک فروشگاه section.

---

## 6. Store List View Updates

Since sellers are merged into stores, the stores list needs to show key seller info:

```
┌─────────────────────────────────────────────────────────────────┐
│  فروشگاه‌ها                                    [+ افزودن فروشگاه]│
│                                                                 │
│  [جستجو...] [وضعیت ▼] [پلن ▼] [تاریخ ایجاد ▼] [تعداد محصول ▼]│
│                                                                 │
│  ┌──────┬────────┬──────────┬────────┬───────┬───────┬───────┐ │
│  │ لوگو │ نام    │ مالک     │ دامنه  │  پلن  │وضعیت  │محصولات│ │
│  ├──────┼────────┼──────────┼────────┼───────┼───────┼───────┤ │
│  │ [img]│ تست    │ — (0992.)│test-shi│بدون پلن│ فعال  │   0   │ │
│  │ [img]│ شاپ من │علی(0912.)│shop-man│حرفه‌ای │ فعال  │  45   │ │
│  │ [img]│ دیجیتال│رضا(0935.)│digital │ پایه  │غیرفعال│  12   │ │
│  └──────┴────────┴──────────┴────────┴───────┴───────┴───────┘ │
│                                                                 │
│  Quick actions per row: [مشاهده] [غیرفعال کردن] [تغییر پلن]    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. API Requirements

### 7.1 Store APIs (Updated)

| Endpoint | Method | Description |
|---|---|---|
| `GET /admin/stores` | GET | List all stores (includes owner info) |
| `GET /admin/stores/:id` | GET | Get store detail (all sections) |
| `PATCH /admin/stores/:id` | PATCH | Update store basic info |
| `PATCH /admin/stores/:id/status` | PATCH | Toggle store active/inactive |
| `PATCH /admin/stores/:id/plan` | PATCH | Change store plan |
| `GET /admin/stores/:id/plugins` | GET | List all plugins with install status |
| `POST /admin/stores/:id/plugins/:pluginId/activate` | POST | Force-activate a plugin |
| `GET /admin/stores/:id/plugins/:pluginId/data` | GET | Get plugin-specific data |
| `GET /admin/stores/:id/config/business` | GET | Get business config |
| `PATCH /admin/stores/:id/config/business` | PATCH | Update business config |
| `GET /admin/stores/:id/config/personalization` | GET | Get personalization config |
| `PATCH /admin/stores/:id/config/personalization` | PATCH | Update personalization config |
| `GET /admin/stores/:id/config/seo` | GET | Get SEO config |
| `GET /admin/stores/:id/config/notifications` | GET | Get notification config |
| `GET /admin/stores/:id/owner` | GET | Get owner/seller info |
| `PATCH /admin/stores/:id/owner` | PATCH | Update owner info |
| `DELETE /admin/stores/:id` | DELETE | Delete store (requires confirmation) |
| `POST /admin/stores/:id/suspend` | POST | Suspend store |
| `POST /admin/stores/:id/unsuspend` | POST | Unsuspend store |
| `POST /admin/stores/:id/transfer` | POST | Transfer ownership |
| `POST /admin/stores/:id/export` | POST | Trigger data export |

### 7.2 Platform Orders APIs (New)

| Endpoint | Method | Description |
|---|---|---|
| `GET /admin/platform-orders` | GET | List platform orders (with filters) |
| `GET /admin/platform-orders/:id` | GET | Get order detail |
| `POST /admin/platform-orders` | POST | Create new platform order |
| `PATCH /admin/platform-orders/:id/status` | PATCH | Update order status |
| `POST /admin/platform-orders/:id/activate` | POST | Activate service for order |
| `POST /admin/platform-orders/:id/refund` | POST | Process refund |
| `POST /admin/platform-orders/:id/reminder` | POST | Send payment reminder |
| `GET /admin/platform-orders/stats` | GET | Order statistics/summary |

### 7.3 Deprecated APIs

| Endpoint | Status | Replacement |
|---|---|---|
| `GET /admin/sellers` | **DEPRECATED** | `GET /admin/stores` (includes owner info) |
| `GET /admin/sellers/:id` | **DEPRECATED** | `GET /admin/stores/:storeId/owner` |
| `PATCH /admin/sellers/:id` | **DEPRECATED** | `PATCH /admin/stores/:storeId/owner` |
| `GET /admin/orders` (all store orders) | **REMOVED** | N/A — store orders viewed within store detail |

---

## 8. Data Migration Plan

### 8.1 Seller → Store Merge

| Step | Action | Risk | Mitigation |
|---|---|---|---|
| 1 | Map each seller to their store (1:1) | Orphan sellers (no store) | Create placeholder stores or archive |
| 2 | Copy seller fields into store.owner | Data duplication during transition | Run in transaction, verify before committing |
| 3 | Update all foreign keys referencing seller_id to use store_id | Breaking existing queries | Feature flag for gradual rollout |
| 4 | Deprecate seller endpoints (return redirect responses) | External integrations breaking | 3-month deprecation window with warnings |
| 5 | Remove seller table (final cleanup) | Data loss | Full backup before removal |

### 8.2 Orders Migration

| Step | Action |
|---|---|
| 1 | Create new `platform_orders` table |
| 2 | Migrate any existing plan purchase records to `platform_orders` |
| 3 | Update sidebar and routes to point to new orders page |
| 4 | Old customer orders page removed from sidebar (data remains in DB, accessible only via store detail) |

---

## 9. Permissions & Access Control

| Action | Super Admin | Admin | Support |
|---|---|---|---|
| View store list | ✅ | ✅ | ✅ |
| View store detail (all sections) | ✅ | ✅ | ✅ (read-only) |
| Edit store basic info | ✅ | ✅ | ❌ |
| Toggle store status | ✅ | ✅ | ❌ |
| Change store plan | ✅ | ❌ | ❌ |
| View plugin data | ✅ | ✅ | ✅ (read-only) |
| Edit plugin data | ✅ | ✅ | ❌ |
| View business/personalization config | ✅ | ✅ | ✅ (read-only) |
| Edit business/personalization config | ✅ | ✅ | ❌ |
| Suspend/Delete store | ✅ | ❌ | ❌ |
| View platform orders | ✅ | ✅ | ✅ |
| Create platform order | ✅ | ✅ | ❌ |
| Process refund | ✅ | ❌ | ❌ |
| View owner/seller info | ✅ | ✅ | ✅ |
| Edit owner/seller info | ✅ | ❌ | ❌ |

---

## 10. UI/UX Specifications

### 10.1 Store Edit Page — Section Navigation

- **Position:** Left side (in RTL layout: right side) of content area, below the store header
- **Width:** 240px fixed
- **Behavior:** Sticky scroll (stays visible while scrolling content)
- **Active section:** Highlighted with primary color background + left border
- **Groups:** Collapsible with group header (اطلاعات اصلی, افزونه‌ها, تنظیمات, ناحیه خطر)
- **Plugin badge:** Each plugin section shows a small dot indicator (green = active, gray = inactive)
- **Search:** Optional search/filter within section nav for quick jump when list grows long

### 10.2 Status Toggle

- **Component:** Custom switch/toggle component
- **Colors:** Green = active, Red = inactive, Orange = suspended
- **Size:** Medium (visible but not dominant)
- **Position:** Next to store name in header

### 10.3 Plan Badge

- **Colors:** 
  - بدون پلن = Gray
  - رایگان = Blue
  - پایه = Green
  - حرفه‌ای = Purple
  - سازمانی = Gold
- **Position:** Below domain in header
- **"تغییر پلن" button:** Text button (link style) next to badge

### 10.4 Responsive Behavior

| Breakpoint | Section Nav Behavior |
|---|---|
| Desktop (>1280px) | Permanent sidebar |
| Tablet (768-1280px) | Collapsible sidebar with hamburger toggle |
| Mobile (<768px) | Full-screen overlay nav / dropdown selector |

---

## 11. Edge Cases & Error Handling

| Scenario | Handling |
|---|---|
| Super Admin deactivates a store with active subscription | Warning: "This store has an active plan expiring on [date]. Deactivating will not cancel the plan. Do you want to also cancel the plan?" with options: [Deactivate Only] [Deactivate & Cancel Plan] |
| Plan change to a lower plan when store exceeds new limits | Warning: "This store has 150 products. The selected plan allows 100. Downgrading will not delete products but will prevent adding new ones. Proceed?" |
| Deleting a store with active platform orders | Block deletion: "This store has unpaid platform orders. Please resolve them before deleting." |
| Network error during status toggle | Revert toggle to previous state, show error toast: "خطا در تغییر وضعیت. لطفاً دوباره تلاش کنید." |
| Store has no owner (orphan store) | Show "مالک تعیین نشده" in owner section with "Assign Owner" button |

---

## 12. Analytics & Tracking Events

| Event | Trigger | Data |
|---|---|---|
| `store.status.changed` | Toggle store active/inactive | store_id, new_status, admin_id, reason |
| `store.plan.changed` | Change store plan | store_id, old_plan, new_plan, admin_id |
| `platform_order.created` | New platform order created | order_id, store_id, type, amount, admin_id |
| `platform_order.paid` | Order marked as paid | order_id, payment_method, payment_ref |
| `platform_order.activated` | Service activated | order_id, activation_date, expiry_date |
| `platform_order.refunded` | Refund processed | order_id, refund_amount, reason |
| `store.suspended` | Store suspended | store_id, admin_id, reason |
| `store.deleted` | Store deleted | store_id, admin_id |

---

## 13. Implementation Phases

### Phase 1: Foundation (Sprint 1-2)
- [ ] Database: Add owner fields to store table
- [ ] API: Create store owner endpoints
- [ ] API: Deprecate seller endpoints (keep working with redirect)
- [ ] Frontend: Remove "فروشندگان" from sidebar
- [ ] Frontend: Update store list to include owner info columns

### Phase 2: Store Edit Redesign (Sprint 3-4)
- [ ] Frontend: Replace tab layout with section sidebar layout
- [ ] Frontend: Implement store header with toggle and plan badge
- [ ] Frontend: Build plan change modal
- [ ] API: Store status toggle endpoint
- [ ] API: Store plan change endpoint
- [ ] Frontend: Add all plugin sections dynamically

### Phase 3: Business Config & Personalization (Sprint 5)
- [ ] API: Business config endpoints
- [ ] API: Personalization config endpoints  
- [ ] API: SEO config endpoints
- [ ] API: Notification config endpoints
- [ ] Frontend: Build all four config sections

### Phase 4: Platform Orders (Sprint 6-7)
- [ ] Database: Create platform_orders table
- [ ] API: All platform order endpoints
- [ ] Frontend: Platform orders list page
- [ ] Frontend: Create order flow
- [ ] Frontend: Order detail page
- [ ] Migration: Move existing plan purchase records
- [ ] Frontend: Remove old orders page from sidebar

### Phase 5: Cleanup & Polish (Sprint 8)
- [ ] Remove old seller API endpoints completely
- [ ] Remove old customer orders page
- [ ] End-to-end testing
- [ ] Performance testing (store edit page with all sections)
- [ ] Documentation update

---

## 14. Success Criteria Checklist

- [ ] Super Admin can see ALL plugins for any store in the edit page
- [ ] Super Admin can toggle store active/inactive with one click + confirmation
- [ ] Super Admin can change any store's plan from the store edit page
- [ ] Store edit page handles 20+ sections without horizontal scrolling or tab overflow
- [ ] Business settings section exists and shows tax, invoice, policies, currency configs
- [ ] Personalization section exists and shows theme, colors, fonts, social links
- [ ] "فروشندگان" menu item is removed from sidebar
- [ ] Seller info (name, mobile, national ID, bank account) appears in store detail under "مالک فروشگاه"
- [ ] Orders page shows ONLY Manooch platform orders (plan purchases, renewals, add-ons)
- [ ] Super Admin can create a new platform order manually
- [ ] Old customer orders (from stores) are NOT shown in the main orders page
- [ ] Store customer orders are accessible only within store detail for support purposes (read-only)

---

## 15. Open Questions

| # | Question | Decision Needed By | Status |
|---|---|---|---|
| 1 | Should we keep a read-only "store orders" section within store detail for support debugging? | Product Lead | Proposed: Yes (read-only) |
| 2 | What happens to existing seller-specific reports? Merge into store reports? | Data Team | Open |
| 3 | Should platform orders support recurring billing automation or manual-only for MVP? | Product Lead | Open |
| 4 | Do we need an "impersonate store" feature for Super Admin to view the store as the seller sees it? | Engineering Lead | Open |
| 5 | Should the plugin section nav show only installed plugins or all available plugins? | Product Lead | Proposed: All (with install status) |