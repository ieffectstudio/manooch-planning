# Manooch — Product Requirements Document

**Status:** Describes the product as implemented on the `main` branch of all Manooch repositories, as of **August 11, 2026**.
**Scope:** Every feature that is actually shipped and working today, organized by product domain. A dedicated closing section, **Known Gaps & Limitations**, lists the things that exist in the product (a field, a setting, a screen) but are not yet functionally complete — so this document can be trusted as a description of reality, not of intent.
**Audience:** Anyone who needs a complete, accurate picture of what Manooch does — product, design, support, new engineers, or stakeholders — without needing to read code.

---

## How to read this document

Manooch is built from four applications working together:

- **Storefront** — the public website a store's own customers shop on.
- **Admin** — the control panel a seller uses to run their store.
- **Portal** — the internal control panel Manooch's own staff use to run the platform.
- **Website** — the public marketing site (manooch.site) where prospective sellers learn about and sign up for Manooch.

Each feature below is described once, from the point of view of the domain it belongs to, and notes which application(s) it appears in and who uses it.

---

## Table of Contents

**Part I — The Product**
1. [What Manooch Is](#1-what-manooch-is)
2. [Who Uses Manooch](#2-who-uses-manooch)
3. [The Four Applications](#3-the-four-applications)
4. [How a Store Is Reached](#4-how-a-store-is-reached)
5. [The Commercial Model](#5-the-commercial-model)

**Part II — Product Domains**
6. [Identity & Access](#6-identity--access)
7. [Becoming a Seller: Onboarding](#7-becoming-a-seller-onboarding)
8. [Custom Domains](#8-custom-domains)
9. [Store Configuration & Personalization](#9-store-configuration--personalization)
10. [The Plugin System](#10-the-plugin-system)
11. [Product Catalog](#11-product-catalog)
12. [Inventory & Pricing](#12-inventory--pricing)
13. [Discount Codes](#13-discount-codes)
14. [The Storefront Experience](#14-the-storefront-experience)
15. [Cart & Checkout](#15-cart--checkout)
16. [Payments](#16-payments)
17. [Orders](#17-orders)
18. [In-Person Order Intake](#18-in-person-order-intake)
19. [Customers & the Customer Directory](#19-customers--the-customer-directory)
20. [Loyalty Points](#20-loyalty-points)
21. [SMS Marketing & Campaigns](#21-sms-marketing--campaigns)
22. [Shipping](#22-shipping)
23. [Support Tickets](#23-support-tickets)
24. [Seller Referral Program](#24-seller-referral-program)
25. [Reports](#25-reports)
26. [Platform Administration (Portal)](#26-platform-administration-portal)
27. [Subscription Plans & Platform Billing](#27-subscription-plans--platform-billing)
28. [Marketing Website & Content Management](#28-marketing-website--content-management)

**Part III — Cross-Cutting Product Qualities**
29. [Persian-First, Right-to-Left](#29-persian-first-right-to-left)
30. [Media Handling](#30-media-handling)
31. [Geography](#31-geography)
32. [Communication Channels](#32-communication-channels)
33. [Security & Trust Posture](#33-security--trust-posture)

**Part IV — Reference**
34. [Known Gaps & Limitations](#34-known-gaps--limitations)
35. [Glossary](#35-glossary)

---

# Part I — The Product

## 1. What Manooch Is

Manooch is a **store-building platform for Iranian merchants** — the same category of product as Shopify or Wix, adapted for the Iranian market. A merchant signs up, picks a web address, describes their business, and within a few onboarding steps has a live, mobile-first, Persian-language online store they can start adding products to and selling from.

**Important framing:** Manooch is not a marketplace. There is no single shared catalog that customers browse across sellers, and there is no network of affiliates earning commission on each other's sales. Each store is its own independent shop with its own catalog, its own customers, its own orders, and its own money. Manooch's business is providing the software each shop runs on, and selling that software to merchants on a subscription basis — the merchant then owns the relationship with their own end customers.

Two internal product names are easy to misread and are clarified here up front:

- **"Customer club"** is a loyalty-points-and-SMS-marketing toolkit a merchant can turn on for their own store, to retain their own customers. It is not a multi-level marketing or referral-commission system.
- **"Marketing plan"** refers only to the pricing plans shown to prospective merchants on the public marketing website. It is a presentation concept, not an operational one — see [Section 27](#27-subscription-plans--platform-billing) for why it is deliberately kept separate from the real subscription plans a merchant is actually billed under.

## 2. Who Uses Manooch

| Actor | What they do |
|---|---|
| **Merchant / seller** | Owns a business and one storefront built on Manooch. Manages catalog, pricing, orders, customers, and marketing through the Admin app. |
| **Merchant's customer** | Shops on one merchant's storefront. Has an account scoped to that relationship — a phone number that shops at three different Manooch stores is three separate customer memberships. |
| **Platform operator** | Manooch's own staff. Runs the business behind the scenes: reviewing merchants, managing subscriptions, handling cross-store support, and monitoring the health of the whole platform, through the Portal app. |
| **Prospective merchant / site visitor** | Anyone browsing the public marketing site to learn about Manooch, read the blog or academy content, or request a sales consultation, before signing up. |

## 3. The Four Applications

| App | Address (development ports shown) | Built for | In one line |
|---|---|---|---|
| **Storefront** | port 3700, and every merchant's live subdomain/custom domain | Merchants' own customers | The actual shop a customer buys from. |
| **Admin** | port 3701 | Merchants | The seller's back office: catalog, orders, marketing, settings. |
| **Website** | port 3702 (public: manooch.site) | Prospective merchants, the public | Marketing site, pricing, blog, academy, lead capture. |
| **Portal** | port 3703 | Manooch's own staff | Platform-wide operations across every store on Manooch. |

All four are built as one connected Persian, right-to-left product family sharing a single visual design system, so the experience feels the same whether a merchant is managing their store or a customer is buying from it.

## 4. How a Store Is Reached

Every store gets a **subdomain** on the platform's root domain the moment it's created (for example, `<store>.manooch.site`), based on a unique **slug** the merchant chooses during onboarding. This is the store's address from day one — no extra step required.

A merchant can additionally **connect a custom domain** they own (see [Section 8](#8-custom-domains)) so the store appears under their own brand's web address instead of (or alongside) the manooch.site subdomain. Once verified, either address reaches the same storefront.

## 5. The Commercial Model

Manooch's revenue comes from **subscriptions merchants pay to use the platform**, not from a cut of each sale. A merchant picks a subscription tier, gets billed for it, and everything they sell to their own customers is theirs — Manooch does not touch that money flow beyond providing the optional payment-processing plumbing (see [Section 16](#16-payments)).

Subscription tiers, their pricing, and the store-level entitlements they're supposed to unlock are described in [Section 27](#27-subscription-plans--platform-billing) — including an honest note on what is enforced today versus what is presently just informational.

---

# Part II — Product Domains

## 6. Identity & Access

### One identity: a phone number

There is a single way for anyone — merchant or shopper — to prove who they are on Manooch: **their mobile phone number, verified with a one-time code (OTP)**. There is no separate password-based account for merchants or customers, and no email or social sign-in.

The sign-in and sign-up flow are **unified**: a person enters their phone number, requests a code, and enters it. If this is their first time, an account is created automatically at that moment — there is no separate "register" step before verification. The flow can optionally be told up front whether it expects an existing account ("sign in") or a fresh one ("sign up"); signing in to a phone number with no account fails with a clear "account not found" message, while signing up always succeeds and creates the account if needed.

### The one-time code

- A requested code is valid for **two minutes**.
- A phone number may request a new code no more than **three times in a ten-minute window**.
- After **five wrong attempts**, verification for that phone number is **locked for one hour**.
- In non-production/testing environments, when live SMS sending is turned off, a fixed demonstration code is used and shown directly in the response so the flow can be tested without a real phone — this never happens once live SMS is enabled.

### Sessions and devices

Once verified, a person is signed in for **30 days**. Every sign-in is a distinct, trackable **session** ("device") — a customer or merchant can open a list of every device currently signed in to their account, see when each was last active, and remotely sign any one of them out (for example, if they signed in on a shared computer and want to revoke it later). Signing out only ends the current session; other sessions are unaffected unless removed individually.

### Merchant profile

Alongside the phone number, every person can hold a **profile**: first and last name, gender, national ID number, date of birth, avatar photo, email, and province/city of residence. This is collected during merchant onboarding (see [Section 7](#7-becoming-a-seller-onboarding)) and can be completed or edited later from account settings in both the Storefront and Admin apps.

### Platform operator sign-in

Manooch's own staff (the Portal app) sign in differently from merchants and customers: with a **phone number and password**, since operator accounts are provisioned internally rather than self-registered. Five failed password attempts locks that operator account for **15 minutes**.

## 7. Becoming a Seller: Onboarding

After verifying their phone number for the first time, a new merchant walks through a short guided setup before their store goes live:

1. **Personal information** — name, gender, national ID, and other profile basics.
2. **Business information** — the business's display name and the **store's web address**, chosen as a short, URL-safe slug. The slug must be unique across the whole platform; a small set of words (like "admin," "api," "www," "store," "help," "support," "blog") are reserved and cannot be used as a store's slug, since they're needed for the platform itself.
3. **Business category** — chosen from a large predefined taxonomy of business types (over 20 broad groups such as Electronics & Gadgets or Fashion & Apparel, each with many specific sub-categories), which shapes defaults and how the store is later organized in platform-wide reporting.
4. **Location information** — the business's province, city, and address, plus a support phone number customers can reach.
5. **Completion** — the store is created and activated immediately; the merchant lands in their new Admin dashboard.

**One business per phone number.** A single verified phone number can complete this onboarding flow — and therefore own a store — only once. A merchant who wants a second, independent store needs a second phone number, or must have Manooch's own platform operators create it for them on the Portal side, which is the one path that bypasses the one-store limit.

Every plugin in the platform's plugin catalog (see [Section 10](#10-the-plugin-system)) is switched to its default on/off state automatically the moment a store is created, so a brand-new store already has a sensible starting toolkit rather than an empty shell.

## 8. Custom Domains

A merchant can attach a domain name they already own to their store, so it's reachable at their own brand's address instead of only the manooch.site subdomain.

- The merchant registers the domain from their Admin panel and is shown the exact DNS record they need to point at Manooch.
- The system verifies the domain by checking that DNS record actually resolves to Manooch's servers before marking it active; verification can be re-checked, but there is a **cooldown between verification attempts** so a merchant can't hammer the check every second while waiting on DNS propagation.
- A small list of domains that belong to the platform itself is blocked from ever being registered as a "custom" domain by a merchant, to prevent someone from hijacking a platform-owned address.
- Once verified, the platform automatically provisions HTTPS (a secure padlock) for the domain — no manual certificate work for the merchant.
- Each store may have **one active custom domain** at a time; registering a new one retires the previous one. A domain already claimed by another store cannot be claimed again until it's released.

## 9. Store Configuration & Personalization

From the Admin app, a merchant tailors how their storefront looks and behaves, all captured in one flexible settings profile per store:

- **Branding** — a primary brand color, a choice of Persian typefaces, and a decorative icon pattern used across the storefront.
- **Selling mode** — how the store actually transacts with customers: a full **shopping cart** experience, sending inquiries through **Telegram**, or simply displaying a **phone number to call**. This single choice reshapes the buying flow across the whole storefront.
- **Catalog display style** — whether product types are browsed via **tabs** or a **horizontal scroll**, and whether the storefront uses an **advanced**, **full**, or **compact/mini** product layout.
- **Discovery controls** — toggles for whether search is available, whether filters are shown, whether a dedicated categories page exists, and whether categories display their icons.
- **Section ordering** — merchants can reorder the blocks that make up their storefront home page (banner, products, gallery, about, FAQ, and so on).
- **Payment method toggles** — which of the payment options described in [Section 15](#15-cart--checkout) are actually offered to that store's customers (online gateway, receipt upload, negotiated/conditional payment), and whether the store absorbs shipping cost itself.
- **Support contacts** — a support phone number shown to customers.
- **Enamad trust seal** — an Iranian e-commerce trust certification badge a merchant can register and choose to display on their storefront, alongside their online payment gateway configuration.

## 10. The Plugin System

Manooch is organized around a **plugin catalog** — a fixed menu of 15 optional capabilities a merchant can turn on or off per store, so a store only carries the complexity it actually needs. The catalog spans two kinds of plugins:

- **Core sales plugins**, which most stores keep on from day one: **Product catalog**, **Categories**, **Attributes**, **Units**, **Customers**, **Discounts**, **Notifications**, and **Reviews**.
- **Optional / helper plugins**, off by default until a merchant opts in: **Banner**, **Gallery**, **FAQ**, **Team**, **Bank Cards**, **In-Person Order Intake**, and **Customer Club** (loyalty + SMS marketing).

Some plugins **depend on another being active first** — for example, Categories, Attributes, Units, Discounts, and Reviews all depend on the Product catalog plugin being on, and Customer Club depends on the Customers plugin. Turning a plugin off hides the corresponding section from the merchant's own admin navigation and, for storefront-facing plugins like Gallery, FAQ, and Team, removes that section from the public store entirely until switched back on.

Platform operators additionally hold a global override in the Portal: any plugin can be disabled platform-wide as a kill switch, independent of what individual merchants have chosen, and a registry lets operators manage the full catalog of plugins offered across the platform.

## 11. Product Catalog

A store's catalog is built from **products**, organized into merchant-defined, nestable **categories** (categories can have sub-categories). Each product is one of three types:

- **Goods** — physical items.
- **Service** — a bookable or purchasable service rather than a shipped item.
- **File** — a digital/downloadable product.

### Pricing methods

Every product uses exactly **one** of four mutually exclusive pricing approaches, chosen per product:

1. **Simple** — a single price (and optional discounted price) for the whole product.
2. **Units** — the product is sold by named units (e.g., different package sizes or measures), each with its own price, stock, and minimum order quantity.
3. **Attributes** — the product varies by one or more selectable attributes (color, size, or free-form specs), and price/stock can differ per selected attribute value.
4. **Price on inquiry** — no price is shown publicly; a customer must contact the merchant to learn the price (used with the "call" or "Telegram" selling modes, or for custom-quote items).

### Supporting catalog data

- **Attributes** are grouped by type — **color** (with an actual color swatch), **size**, or free-form **specs** — and each attribute has a merchant-defined list of possible values.
- **Units** are a per-store dictionary of measurement/packaging units a merchant defines once and reuses across products.
- Every product can carry **multiple images**, one **audio clip** (useful for voice-note style listings), and is given an **auto-generated product code** for internal reference.
- Products can be individually switched **active/inactive**; there is no formal publishing-approval workflow — a merchant's own toggle is the only gate before something appears live on their storefront.

## 12. Inventory & Pricing

### Stock tracking

Stock is tracked at the level that matches a product's pricing method: a single quantity for Simple products, or a quantity per unit / per attribute value for Units and Attributes products. A merchant can instead mark a product as having **unlimited stock**, which bypasses all stock checks for it entirely.

Each product carries a **low-stock threshold** (defaulting to 5); the storefront and admin panel surface three stock states derived from it — **in stock**, **low stock** (at or below the threshold), and **out of stock** (zero or fewer) — as a visible badge merchants and customers can both see.

### Discounts on individual variants

Beyond store-wide discount codes (see [Section 13](#13-discount-codes)), every priced line — the product itself, each unit, and each priced attribute value — can carry its **own discount percentage**, set directly in the pricing editor. This is what lets a merchant discount one size or color of a product without discounting the whole listing. When a customer picks a specific unit or set of attributes, the price they're shown and ultimately charged reflects that specific line's own discount, not just the product's base price — this per-variant discount is honored consistently everywhere a price is calculated, including in the cart and at checkout.

When a product has no single price to show up front (because it's priced by unit or attribute), the storefront instead shows a **"starting from"** price — the lowest available price among its variants — so a product card is never blank or zero.

### The pricing & stock editor

Merchants manage price and stock from a dedicated editor per product, matching the product's chosen pricing method. Switching a product **between Unit pricing and Attribute pricing is destructive** — the rows belonging to whichever method is being switched away from are discarded — while switching to or from Simple pricing preserves the other data so it's there if the merchant switches back.

### Bulk tools

- A merchant can **download their entire catalog as a spreadsheet** for offline editing or as a backup.
- A merchant can **bulk-import prices and stock from a spreadsheet**, using a provided template, to update many products at once without editing them one by one in the UI. Import validates the file type and size and reports clearly when a row references a product code that doesn't exist in the store.

## 13. Discount Codes

Independent of per-variant discounts, a merchant can create standalone **discount codes** for their store:

- A discount can be a **percentage off** or a **flat cash amount off**.
- A discount can be **targeted** at a specific product, an entire category, or even a specific individual customer.
- A discount can be given a **start time** and, optionally, a **duration**, after which it automatically stops applying.
- Discount codes can be turned active/inactive, and the system can auto-generate a random unique code for a merchant who doesn't want to type one by hand.
- If a product qualifies for both a product-specific and a category-wide discount at the same time, the **product-specific one wins** — discounts are not stacked.

## 14. The Storefront Experience

This is what a merchant's own customers see and do on the public-facing store.

### Home & discovery
The store's home page is assembled from the sections the merchant has enabled and ordered (see [Section 9](#9-store-configuration--personalization)): a promotional banner, the product listing, an image gallery, an about block, FAQ, and more. Customers can **browse by category**, **search** by keyword, apply **filters**, and **sort** results (e.g., newest, cheapest, most expensive). Listings are paginated.

### Product detail
A product page shows its image gallery, description, and — depending on its pricing method — either a straightforward price, a picker for units or attribute combinations (updating price and stock live as the customer chooses), or a prompt to contact the merchant for pricing. Stock status and any active discount are shown alongside the price.

### Store content sections
- **Banner** — rotating promotional imagery on the store home page.
- **Gallery** — a general-purpose image showcase.
- **FAQ** — a merchant-authored question-and-answer list.
- **About page** — free-form store description plus working hours.
- **Team** — staff profiles (name, role, photo, phone) that visitors can "like."
- **Bank Cards** — the merchant's bank card details (card number, account holder, IBAN/Sheba) displayed so customers can pay via manual bank transfer.

### Reviews
Customers can leave a **rating and written review**, and optionally mark whether they'd recommend the product or store, targeting either a specific product or the store overall. Every review enters a **moderation queue** and only becomes publicly visible once a merchant approves it (or is hidden if rejected). Other customers can "like" an approved review. Editing an already-approved review sends it back into moderation.

### Personal features
Signed-in customers can **bookmark** products to revisit later, **follow** a store to keep track of it, and see **in-app notifications** the merchant has published (each notification is shown for a merchant-set number of days and can optionally link somewhere).

### "Linkdooni" — link-in-bio page
Each store has a lightweight, shareable **link-in-bio style page** (branded "Linkdooni") — a simple public page useful for social-media bios that points visitors toward the store and its offerings, in the style of a Linktree-type page.

### Customer account area
A signed-in customer has their own profile, a saved **address book** (with a designated default address), an order history (see [Section 17](#17-orders)), and access to their bookmarks and notifications, all scoped to that one store.

## 15. Cart & Checkout

A signed-in customer has **one active shopping cart per store**. Guest checkout is not available — a customer must be signed in to add to cart.

- Adding the same product with the **same unit and same selected attributes** to an already-in-progress cart merges into that existing line and increases its quantity, rather than creating a duplicate line; a different unit or different attribute selection creates a new line.
- The price shown for each cart line is **captured at the moment it's added**; editing the quantity later only recalculates the line total at that captured price, it does not re-fetch a fresh price.

### Checking out
At checkout, the customer selects a saved address and a shipping method (see [Section 22](#22-shipping)), then a payment method — the set of available payment methods depends entirely on what the merchant has switched on for their store (see [Section 9](#9-store-configuration--personalization)):

- **Online gateway** — pay immediately through an integrated payment gateway (see [Section 16](#16-payments)).
- **Cash on delivery**.
- **Receipt upload** — the customer pays by bank transfer outside the app and uploads a photo of the receipt for the merchant to confirm; this requires a receipt image to be attached before the order can be placed.
- **Conditional / negotiated payment** — used for arrangements like post-dated cheques, where the order is placed first and payment terms are agreed and documented afterward (see [Section 17](#17-orders)).

Available stock is checked at the moment of checkout, and the order is only created if every line still has enough stock; stock is deducted from the catalog the instant the order is placed, and restored automatically if the order is later cancelled.

## 16. Payments

Manooch integrates with an online **payment gateway** so customers can pay by card at checkout or via a standalone payment link.

- Initiating a payment creates a pending payment record and sends the customer to the gateway's hosted payment page.
- When the customer returns from the gateway, the payment is **verified server-side** before it is ever marked successful — a customer simply landing back on a "success" URL is never, by itself, treated as proof of payment.
- Marking a payment as paid is done in a way that's **safe to happen twice** — if the gateway's callback fires more than once for the same payment, the second call is a harmless no-op rather than double-crediting anything.
- A payment that is initiated but never completed **automatically expires after 15 minutes**, freeing the customer to try again without their order being stuck in limbo.
- **Payment links** — a merchant can generate a standalone, shareable payment link for a specific amount (useful for custom invoices or phone/Telegram sales), with its own expiry window, independent of a cart-based order.
- **Refunds** are available as an admin action on a paid order, recording that the payment has been refunded.
- Merchants configure their own **payment gateway credentials** and **Enamad trust-seal status** per store from their settings.

## 17. Orders

An order moves through a well-defined lifecycle of states depending on how it was paid and how far along fulfillment is: **pending payment**, **awaiting confirmation**, **pending receipt approval**, **negotiation**, **agreement reached**, **processing**, **shipped**, **delivered**, or **cancelled**. Delivered and cancelled are final — an order does not move again once it reaches either.

Which starting state an order lands in depends on the payment method chosen at checkout: a receipt-upload order starts in **pending receipt approval** (waiting on the merchant to confirm the uploaded receipt), a conditional/negotiated order starts in **negotiation**, and everything else starts in **pending payment**.

### The merchant's order workflow
From the Admin app, a merchant sees a filterable, sortable queue of all orders for their store (by status, by date range, by amount), can open any order's full detail (customer, delivery address, shipping method, items, any uploaded receipt or post-dated cheques), and can move an order forward — individually or in bulk — along its allowed next steps. Every status change is recorded in that order's history, along with who made it and, for cancellations, an optional reason.

**Cancelling an order automatically restores the stock** that was reserved for it back to the catalog.

### Negotiated / conditional payment documents
For the conditional-payment flow, a customer can submit supporting payment documents directly to the order — for example, photos of one or more **post-dated bank cheques**, or a **cash receipt** — which the merchant then reviews. If the merchant rejects the submission, the order simply reverts to the negotiation stage rather than losing what was submitted, so the customer can add to it rather than starting over.

### The customer's order experience
A customer sees their own order history for a store, can open any order of theirs to track its status, and — for the flows that require it — can upload a receipt or the negotiated payment documents themselves. A **"reorder"** view surfaces products the customer has bought before, so they can quickly buy them again.

### Loyalty payoff
The moment an order reaches **delivered**, if the store has its loyalty program active, the customer automatically earns loyalty points for that purchase (see [Section 20](#20-loyalty-points)) — this only ever happens once per order, even if the delivered status were somehow triggered more than once.

## 18. In-Person Order Intake

For merchants who also sell face-to-face (a physical counter, a market stall, a home visit), Manooch offers a lightweight **in-person order intake** tool from the Admin app: the merchant picks an already-known customer of theirs, adds products to a quick order, and records it as paid immediately — the money has already changed hands in person, so unlike a normal online order this one starts life already marked **paid** and **processing**, with no address or shipping step. A running daily counter shows the merchant how many in-person orders and how much income they've taken in that day.

## 19. Customers & the Customer Directory

Each store keeps its own **directory of customers** — everyone who has ever transacted or been added to that particular store, independent of what other stores that same phone number might also shop at. A merchant can search this directory (by exact phone or by prefix), tag customers into custom categories/segments for their own organizational purposes, and see each customer's purchase history and loyalty balance in one place.

The directory automatically classifies every customer into one of four **lifecycle segments**, so a merchant can see at a glance who needs attention:

- **New** — joined within a recent window.
- **Loyal** — an established, regularly active customer.
- **VIP** — a customer whose loyalty point balance has crossed a high-value threshold.
- **At risk** — a customer who hasn't visited in a long while and may be drifting away.

A customer's "last visit" is tracked specifically for genuine in-person or intentional store visits — routine background activity (like simply signing in) does not, by itself, count as a visit for this purpose.

## 20. Loyalty Points

Loyalty is a per-store points program a merchant can turn on as part of the Customer Club toolkit, with its own configurable policy:

- **Welcome points** — a one-time bonus (defaulting to 100 points) awarded the first time a customer joins that store's loyalty program.
- **Earn rate** — points are earned on purchase, calculated from how much was spent relative to a configurable "toman per point" rate (defaulting to one point per 10,000 Toman spent), rounded according to the merchant's chosen rounding rule.
- **Redemption** — points can be redeemed once a customer holds at least a configurable minimum (defaulting to 500 points), in configurable "redemption units" (defaulting to 100 points redeemable per 10,000 Toman of value).
- **Expiry** — earned points expire a configurable number of months after they were earned (defaulting to 12 months). When points expire, the **oldest points are always the ones spent or expired first** (first-earned, first-used), so a customer's balance behaves predictably rather than expiring newer points ahead of older ones.
- **Manual adjustments** — a merchant can manually credit or debit a customer's balance directly, for example as a goodwill gesture or to correct an error; manual debits are the one case allowed to go below the normal minimum-redemption floor.
- A full **ledger** of every point-earning and point-spending event is kept per customer, viewable by the merchant.
- Loyalty accounts additionally carry a **tier** concept (bronze, silver, gold, diamond) intended to reflect a customer's standing — see the gaps section for its current status.

## 21. SMS Marketing & Campaigns

Manooch lets a merchant send **bulk SMS messages** to their own customer base, governed by a set of guardrails designed to keep messaging respectful and compliant:

- Each store has an **SMS credit balance**; every message sent costs a fixed amount (250 Toman) deducted from that balance.
- Messages are only sent within the store's configured **business hours** (defaulting to 9:00–21:00 local Tehran time) — nothing is delivered outside that window.
- A **daily cap per customer** (defaulting to 2 messages) prevents any one customer from being flooded with messages in a single day.
- A store can be configured to **stop messaging customers who've gone inactive** for a configurable number of days (defaulting to 60), so lapsed customers aren't repeatedly targeted.
- Messages have a maximum length (320 characters) and are composed and sent as **batches** — a merchant writes a message, targets it, and can **schedule** it for a future time or send immediately; a scheduled batch can still be **cancelled** before it goes out.
- Every batch produces a **delivery report** (sent, delivered, failed counts), and every reason a message might be skipped (outside business hours, over the daily cap, inactive customer, insufficient credit, invalid number, or the customer opted out) is tracked and shown back to the merchant.
- Reusable **message templates**, categorized by purpose (welcome, birthday, expiry reminder, festival greeting, retargeting, and more), let a merchant save and reuse message copy.

### Automated campaigns
Beyond manual sends, a merchant can define **automated campaigns** that trigger SMS sends based on customer behavior. The trigger types available are: **welcome** (on joining), **birthday**, **points about to expire**, **abandoned cart**, **days since last purchase**, and **manual**. See the gaps section for which of these are fully wired up to actually fire automatically today.

## 22. Shipping

A merchant defines one or more **shipping methods** for their store, each with a name, a flat base price, and an estimated delivery time shown to customers. A store can alternatively be configured to **absorb shipping cost itself**, in which case checkout shows no shipping charge to the customer regardless of which method is chosen.

## 23. Support Tickets

Merchants can open a **support ticket** directly to Manooch's own operations team from the Admin app, categorized by topic (**financial**, **technical**, **moderation**, or **general**). A ticket is a threaded conversation — the merchant and a platform operator exchange messages, each side sees an **unread indicator** when the other has replied, and an operator can formally **close** a resolved ticket. On the Portal side, operators work from a shared queue of all tickets across every store, with a summary of how many are currently open, answered, or closed.

## 24. Seller Referral Program

Manooch has a lightweight, **single-level referral program** for merchants: every merchant is given their own personal referral code, which they can share with someone they know. If that person signs up using the code and successfully completes their own store onboarding, the referral is marked **successful**, and the referring merchant sees it reflected as a completed invite along with a running count of bonus "pro credit days" earned from successful referrals.

This program is intentionally flat — it is a single act of "you brought someone in," not a multi-level structure. There is no tree of sub-referrals, no ranks, and no ongoing commission on anything the referred merchant later sells. Note the gaps section regarding how the earned credit days are currently applied.

## 25. Reports

The Admin app gives merchants two dedicated reporting views:

- **Sales report** — order volume and revenue charted by day, week, or month, alongside a breakdown of the store's top customers (by spend and visit frequency) and top-selling products (by quantity sold).
- **Customer club report** — a dashboard for the loyalty and SMS marketing program: how many messages were sent and their delivery rate, how many loyalty points were issued versus redeemed over a selected time range (today, this month, the last 3 months, or the last year), weekly send volume, customer growth trend, performance broken out per marketing tool/campaign, and a simple funnel of new versus returning versus churned customers.

## 26. Platform Administration (Portal)

The Portal is Manooch's internal control room, used only by the platform's own operations staff, giving them a cross-tenant view across **every** store on the platform (something no individual merchant can see).

- **Store management** — see every store on the platform, drill into any one of them (its products, orders, banners, gallery, FAQ, discounts, reviews, team, followers, customers, domains, payment settings, and plugins), change a store's ownership, and directly **activate, suspend, or archive** a store.
- **Subscription plan management** — create and edit the platform's subscription tiers and their pricing (see [Section 27](#27-subscription-plans--platform-billing)), and manually assign or change which plan a given store is on.
- **Platform billing records** — a full audit trail of plan purchases, renewals, upgrades, downgrades, add-ons, and custom services billed to stores, each moving through its own status lifecycle (new, awaiting payment, paid, activated, refunded, cancelled, or expired).
- **Identity & operator management** — manage every customer/merchant identity on the platform, including the ability to promote someone to platform-operator status; separately manage the platform's own internal operator accounts.
- **Plugin registry** — manage the master catalog of plugins offered platform-wide, including global on/off overrides that take precedence over any individual store's own plugin choice.
- **Business taxonomy & geography** — maintain the business-category taxonomy used during onboarding, and the underlying province/city reference data used throughout the platform.
- **Cross-tenant monitors** — a unified view of orders across every store, and of the seller referral program across every merchant.
- **Support queue** — the shared ticket inbox described in [Section 23](#23-support-tickets).
- **OTP monitor** — operators can view recently sent one-time codes platform-wide, primarily to help diagnose sign-in issues merchants or customers report (see the security note on this in [Section 33](#33-security--trust-posture)).
- **Dashboard** — top-line platform KPIs at a glance: total stores, active stores, number of distinct merchants, number of customers, total orders, total revenue across the platform, and a recent-activity feed of newly created stores and newly placed orders.

## 27. Subscription Plans & Platform Billing

Manooch offers merchants **three subscription tiers** — **Basic**, **Economy**, and **Advanced** — each with its own set of feature highlights and a choice of **monthly, quarterly, or semi-annual** billing, with longer commitments priced at a discount versus paying monthly.

A store's plan and its active date window are recorded against the store itself, and a platform operator can assign or change a store's plan directly, with the change captured as a billing record (see [Section 26](#26-platform-administration-portal)). Each plan can also carry intended entitlement limits, such as a maximum product count or a storage allowance — see the gaps section for whether these limits are actually enforced today versus just recorded.

**Marketing pricing vs. operational pricing are deliberately two separate things.** The pricing tiers a visitor sees on the public marketing website (see [Section 28](#28-marketing-website--content-management)) are maintained independently by content editors and are not the same records as the operational subscription tiers described here — editing the marketing copy for a plan does not change what any merchant is actually billed, and the two are kept in sync manually if that's ever needed. This separation is intentional: it lets marketing iterate on pricing presentation freely without any risk of accidentally changing what a real merchant is charged.

## 28. Marketing Website & Content Management

The public marketing site (manooch.site) is where prospective merchants first encounter Manooch, and it is entirely powered by a content management system that Manooch's marketing team edits directly, without needing engineering involvement for routine content changes.

### What the marketing site shows
- A **home page** assembled from independently editable sections: a top promotional banner, a hero introduction with feature highlights, a feature/benefit showcase, a customer-logo showcase, a **pricing plans** section, a **plugins showcase** section, an **academy** video preview strip, a **blog** teaser, an **FAQ** accordion, a contact section, and a footer.
- A full **blog**, with a listing page and individual post pages.
- **Academy** video content — an educational video library for merchants.
- A **consultation request form**, letting a visitor leave their contact details to be reached by Manooch's sales team.

### How content editing works
Every section of the home page is independently optional — if an editor hasn't published a section, or a piece of content is temporarily unavailable, that one section simply doesn't render rather than breaking or blanking the whole page. When an editor publishes or updates content, the change is designed to **appear on the live site within moments**, without waiting for a slow rebuild.

### Marketing plans and plugin showcase — deliberately decoupled
The **pricing plans** and **plugin showcase** shown on the marketing site are authored purely as marketing content — copy, images, and a features checklist — independent of the platform's real operational subscription tiers and real plugin catalog described in Sections 27 and 10. This is a conscious design choice: it lets the marketing team craft the sales pitch and pricing presentation freely, without that content being able to accidentally alter what a real merchant is billed or which plugins actually function on a real store.

---

# Part III — Cross-Cutting Product Qualities

## 29. Persian-First, Right-to-Left

Manooch is built Persian-first from the ground up, not translated after the fact: every screen across all four applications reads **right-to-left**, uses Persian-appropriate typefaces (with a choice of a few different Persian fonts available for a merchant's own storefront branding), and defaults to **Iranian Rial** as the currency and **Asia/Tehran** as the operating timezone — used consistently for things like business-hour windows for SMS sending and daily counters for in-person sales. The product today operates in a single language (Persian); there is currently no secondary-language mode.

## 30. Media Handling

When a merchant uploads an image (for a product, a banner, a gallery item, and so on), Manooch automatically prepares it for fast loading everywhere it's used: it generates several appropriately sized versions for different contexts (a small thumbnail, and progressively larger versions for cards, detail views, and full-size display), plus a soft blurred placeholder that shows instantly while the real image loads in. Uploads are capped at 5 MB by default, and the system verifies that an uploaded file's actual content matches an accepted image type, rather than trusting a file's stated type at face value.

## 31. Geography

Manooch ships with a built-in, ready-to-use reference dataset of **every Iranian province and city** (31 provinces and 344 cities), used consistently throughout the product wherever a location needs to be picked — merchant business address during onboarding, customer shipping addresses, and profile location — so users select from an accurate, standardized list rather than typing free text.

## 32. Communication Channels

Today, Manooch reaches customers and merchants through two channels: **SMS** (for one-time codes and customer-club marketing messages) and **in-app notifications** (for storefront announcements). There is currently no email notification channel and no push-notification channel.

## 33. Security & Trust Posture

A few product-level trust characteristics are worth stating plainly:

- **Session control is real and customer-facing** — anyone can see every device currently signed in to their account and revoke any one individually, without needing to change their phone number or contact support.
- **Stores are fully isolated from one another** — a merchant can only ever see and manage their own store's data; there is no cross-store visibility except from the platform-operator Portal, which exists specifically for platform-wide oversight.
- **Reviews are moderated before they're public** — nothing a customer writes appears on a storefront until a merchant (or, implicitly, until reviewed) approves it.
- **Payment return links are checked for safety** — the addresses a customer is redirected to after paying are validated so a payment flow can't be abused to redirect someone somewhere unintended.
- **Domain verification is strict by design** — a custom domain is only ever marked verified after an actual DNS check succeeds; an unconfigured or missing verification target is treated as a failure, never silently treated as a pass.

---

# Part IV — Reference

## 34. Known Gaps & Limitations

This section exists so the document stays honest: these are things that have a visible setting, field, or screen in the product today, but whose underlying behavior is not yet fully built out. None of these are secret — they are simply the current edges of the product as it exists on `main`.

| Area | What's visible today | What's actually missing |
|---|---|---|
| Discount codes | A full discount-code management screen and validation | A validated discount code does not currently reduce the amount charged at checkout |
| Self-serve subscriptions | Plan browsing and a "subscribe" action for merchants | Self-serve subscribing is not yet functional; plan assignment today happens only via a platform operator |
| Plan limits | Product-count and storage limits recorded per plan | These limits are stored but not currently enforced against a store's actual usage |
| Refunds | A "refund" action on a paid order | Marks the order as refunded, but does not currently reverse the payment at the gateway, restore stock, or support a partial amount |
| Loyalty tiers | Bronze/Silver/Gold/Diamond tier field on every loyalty account | No account currently advances past the starting "Bronze" tier |
| Loyalty point reasons | Several point reasons are defined (reward, referral, survey, spin-wheel) | These reasons are not currently triggered by any live feature — only welcome, purchase, redemption, expiry, and manual adjustment are active today |
| Automated campaigns | All six campaign trigger types can be configured | Only the "days since last purchase" trigger actually fires automatically today; welcome, points-expiry, abandoned-cart, and manual triggers are not yet wired to send, and birthday campaigns have no birthdate data to trigger from |
| Referral credit days | Successful referrals report accumulated "pro credit days" | Those credited days are currently reported as a number only and are not yet applied to extend anything |
| Shipping | Shipping methods and a shipping log concept | Shipping cost is a simple flat rate per method today — no live carrier tracking integration exists yet, and an "API-based" shipping method type is defined but not yet implemented |
| Identity verification | A national ID field and an "identity verified" flag on every profile | No verification step currently checks or sets this — it is captured as self-reported data only |
| Payment gateway | Full checkout and gateway integration flow | The live/production version of the payment gateway is not yet enabled — the payment flow currently runs against a safe testing/simulation mode; other gateway options are configurable but not yet wired to actually route payments |
| Checkout stock check | A stock check runs at checkout for every order | For products priced by unit or attribute, the check currently validates against the product's overall stock rather than the specific unit's or attribute's own stock, which can allow overselling a specific variant in edge cases |
| OTP rate limits | Per-phone-number request and lockout limits | These limits are currently tracked per running instance of the service rather than shared platform-wide, so they reset if the service restarts |
| OTP visibility for operators | An OTP monitor in the Portal, for diagnosing sign-in issues | Currently shows the live, actual one-time codes rather than a redacted view — a meaningful privacy consideration worth tightening |
| Bank card storage | A "Bank Cards" storefront feature for displaying merchant payment details | Card numbers and IBAN/Sheba values are currently stored as plain text rather than masked/encrypted at rest |
| Scheduled background jobs | Automated jobs handle payment expiry, SMS dispatch, point expiry, and campaign runs | These jobs currently assume a single running instance of the backend service; running multiple instances in parallel would need additional coordination to avoid a job double-firing |

## 35. Glossary

| Term | Meaning |
|---|---|
| **Store / storefront** | A single merchant's independent shop on Manooch, with its own catalog, customers, and orders. |
| **Business** | The merchant account that owns a store; today, one business owns exactly one store. |
| **Slug** | The short, unique, URL-safe name a merchant picks for their store, used in its manooch.site subdomain. |
| **Plugin** | One of 15 optional capabilities a merchant can switch on or off per store (see [Section 10](#10-the-plugin-system)). |
| **Work field / business category** | The predefined business-type taxonomy chosen during onboarding. |
| **Customer club** | The per-store loyalty-points and SMS-marketing toolkit (not a multi-level or affiliate program). |
| **Marketing plan** | The pricing-tier content shown on the public marketing website, kept deliberately separate from real billing. |
| **Linkdooni** | A store's shareable, link-in-bio-style public page. |
| **Order intake** | The tool for recording a face-to-face / in-person sale directly as an already-paid order. |
| **Payment link** | A standalone, shareable link for collecting a specific payment amount, independent of a cart order. |
| **Platform order** | An internal billing record of a store's subscription purchase, renewal, upgrade, downgrade, or other platform-billed charge. |
| **Enamad** | An Iranian e-commerce trust-seal certification a merchant can register and display on their storefront. |
| **Portal** | The internal application used only by Manooch's own operations staff for cross-store administration. |
| **Admin** | The application a merchant uses to run their own store. |
| **Storefront** | The public application a merchant's own customers shop on. |
| **Website** | The public marketing site used to attract and sign up new merchants. |
