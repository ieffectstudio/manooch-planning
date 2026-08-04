# PRD — Manouch: Visitor Ordering Module (Mobile)

| | |
|---|---|
| **Product** | "Manouch" store builder — Order-taking module for visitors |
| **Document version** | 1.0 |
| **Status** | In development (working prototype is ready) |
| **Date** | Mordad 11, 1405 (2026-08-02) |
| **Target platform** | Mobile-First — phone browser |

---

## 1. Executive Summary

The "Manouch" ordering module is a mobile dashboard that allows a **visitor** (mobile salesperson) to register orders for customers present on-site. A visitor may work with **multiple stores** simultaneously; therefore the dashboard must support **switching between stores**, and with each switch it must display **completely different data** (products, customers, and daily stats).

Main flow: **Select customer ← search ← filter ← add to cart ← view cart ← finalize ← final order registration**.

---

## 2. Goals and Non-Goals

### Goals
- Rapid order registration by the visitor on mobile with the minimum number of taps.
- Display the visitor's identity (name + photo) at the top of the page.
- Support for multiple stores and easy switching between them.
- Display daily stats (order count and today's income) per active store.
- Complete data separation (cart, customer, stats) between stores.
- Fully Persian/RTL design with Persian numerals.

### Non-Goals
- Product catalog management (add/edit/delete) in this module.
- Real online payment (in the current version, only payment method selection).
- Pending orders / order history management module (future version).
- Full desktop/tablet version.

---

## 3. User Persona

**Visitor (mobile salesperson):**
- Mobile-first user, usually at the store location or during a customer meeting.
- Works with multiple stores under the "Manouch" brand (e.g., café, restaurant, fast food).
- Needs to know in real time how many orders and what income they have for each store.
- Expects that by selecting a store, they see that store's menu, prices, customers, and stats.

---

## 4. User Stories

| # | User Story |
|---|---|
| US-1 | As a visitor, I want to see my name and photo at the top of the page to make sure I'm logged in with the correct account. |
| US-2 | As a visitor, I want to use the hamburger menu (☰) to see the list of my stores with their stats and switch between them. |
| US-3 | As a visitor, I want to see the number of orders and my income today **for that same active store**. |
| US-4 | As a visitor, I want to see a different menu, categories, customers, and stats when I change the store. |
| US-5 | As a visitor, I want to select a customer from the dropdown or create a new customer. |
| US-6 | As a visitor, I want to search products, filter by category, and add them to the cart. |
| US-7 | As a visitor, I want to view the cart, increase/decrease quantities, and proceed to checkout. |
| US-8 | As a visitor, I want to specify only the payment method and notes (no order type/table number) and finalize the order. |
| US-9 | As a visitor, I want to see the order number and its summary after registration, and be able to start a new order. |

---

## 5. Main User Flow

```
Visitor login
   │
   ▼
Header: ☰ + Visitor profile (name and photo) + active store name + clock + online status
   │
   ▼
Active store stats: today's orders | today's income | active customers
   │
   ▼
Select customer (dropdown + search + add new customer)
   │
   ▼
Search products ← category filter (chips)
   │
   ▼
Product list ← add to cart (+) / change quantity (+/−)
   │
   ▼
Sticky cart bar ← view cart (edit items)
   │
   ▼
Checkout: customer ← payment method ← notes ← invoice summary
   │
   ▼
Final registration ← success page (order number + summary) ← new order
```

**Parallel path (store switching):** at any moment via the hamburger menu ☰ ← "My Stores" ← select store; after switching, all data (menu, customers, stats, cart) changes to the new store.

---

## 6. Functional Requirements (Page Breakdown)

### 6.1 Header
- **Hamburger menu (☰):** opens the store-switching drawer. **The only store-switch point** in the entire app.
- **Visitor profile:** profile photo (with first-letter fallback) + visitor's name + active store name (with store emoji).
- Live (Shamsi/Jalali) clock and "Online" indicator.

### 6.2 Stats Bar (dependent on active store)
- Number of today's orders (base + current session).
- Today's income (format: million/thousand with Persian numerals).
- Number of active customers of the store.
- After each order registration, that store's stats are updated.

### 6.3 Customer Selection
- Dropdown (sheet) control with name search.
- Shows avatar (first letter), name, and phone number.
- "Add new customer" option (name + mobile) — the new customer is added to that store's list.
- Default customer selection: "Guest".

### 6.4 Search and Filter
- Search input with clear button (✕).
- Searches in the name and description of the active store's products.
- Category filter as horizontal chips (categories come from the store's data).

### 6.5 Product List
- Product card: emoji/tile, name, description, price (Toman, Persian numerals).
- Add button (+) which turns into a stepper (−/+ quantity) after adding.
- Empty/no-result state with an appropriate message.

### 6.6 Shopping Cart
- Sticky bar at the bottom of the page (only when the cart is non-empty): count, total amount, "View Cart" button.
- Cart sheet: item list with steppers and delete button (🗑), item total, payable amount.
- The cart is **stored separately per store** and is preserved after switching/returning.

### 6.7 Order Checkout
Only three sections (per the client's request, **without order type and table number**):
1. **Order on behalf of** — display/change the selected customer.
2. **Payment method** — on-site / card terminal / online (single selection).
3. **Notes (optional)** — multi-line text field.
4. **Order summary** — items (name × quantity, price), item total, final amount.
- "✅ Finalize order" button.

### 6.8 Success Page
- Checkmark animation.
- Order number (four digits).
- Summary: store, customer, payment method, item count, final amount.
- "Close" and "New Order" buttons.

### 6.9 Hamburger Menu (Store Switch)
- Full visitor profile card (photo, name, role, phone number).
- "My Stores" title + store list; each row: store emoji, name, city, today's orders, today's income.
- The active store is marked with a ✓ checkmark and highlight.
- "Log out" button (disabled in the prototype).
- **Store switching is done only from this menu; there is no store bar on the main page.**

---

## 7. Data Model (proposed for backend integration)

```js
// Visitor
VISITOR = {
  name: 'Arash Kamali', phone: '0912 123 4567',
  role: 'Sales visitor · Manouch', avatar: 'assets/avatar.png'
}

// Store (each store = an independent dataset)
STORES = [{
  id: 's1', name: 'Manouch Central Café', city: 'Tehran', emoji: '☕', tile: 't1',
  orders: 12,          // today's orders (base)
  income: 8400000,     // today's income (base)
  categories: ['All', 'Hot drinks', ...],
  products: [{ id, name, desc, price, cat, emoji, tile }],
  customers: [{ id, name, phone }]
}, ...]

// Session state
state = {
  storeId, cart,            // current cart of the active store
  carts: { sid: {pid: qty} },   // separate cart per store
  custSel: { sid: customerId },
  pay: 'cash', note: '',
  sessionStats: { sid: { orders, income } }  // session increments
}

// Registered order (proposed for the API)
ORDER = { storeId, customerId, items:[{pid, qty}], total,
          payMethod, note, createdAt, orderNo }
```

**Data rules:**
- Cart, selected customer, and session stats are separate per `storeId`.
- Upon order registration, `sessionStats[storeId]` is incremented and displayed in the stats.

---

## 8. Design System

| Element | Specification |
|---|---|
| **Page direction** | RTL |
| **Language/Numerals** | Persian + Persian numerals with thousands separator |
| **Primary font** | **Ravi** — ⚠️ Commercial font, requires web license (currently falls back to Vazirmatn) |
| **Main title** | **SemiBold (600)** weight |
| **Secondary title** | **Medium (500)** weight |
| **Body text** | **Regular (400)** weight |
| **Primary color** | **Stone charcoal** — `#37424C` (dark: `#262E35`, light: `#E9EDF0`) |
| **Complementary colors** | Background `#F4F3EE`, text `#1C2433`, muted text `#7A8194`, divider `#ECEBE4`, error `#E5484D`, warning `#F59E0B` |
| **Interactive components** | Chips/buttons/steppers: Medium (500) |
| **Visual style** | Rounded corners (18px), soft shadow, bottom sheets |

**Note:** The Ravi font is a product of "FontIran" (designer: Reza Bakhtiari Fard) and commercial/web/store-builder use requires purchasing a license. Until licensed files are obtained, the free "Vazirmatn" font is used as a fallback (CSS is ready).

---

## 9. Non-Functional Requirements

- **Mobile-first:** maximum frame width 460px; centered on desktop.
- **No external dependencies:** pure HTML/CSS/JS; local fonts; offline operation.
- **Performance:** re-render only the affected sections; light CSS animations.
- **Touch experience:** click areas ≥ 40px; `:active` press feedback.
- **Basic accessibility:** semantic labels, image fallback, adequate contrast.
- **Backend integration readiness:** data sits in two central objects, `VISITOR` and `STORES`, to be replaced with an API.

---

## 10. Acceptance Criteria

| # | Criterion |
|---|---|
| AC-1 | The visitor sees their name and photo at the top of the page. |
| AC-2 | "Today's orders" and "today's income" stats are shown for the active store. |
| AC-3 | Tapping ☰ opens the hamburger menu with the list of stores and each one's stats. |
| AC-4 | Store switching is possible only from the hamburger menu; there is no store button/bar on the main page. |
| AC-5 | After switching, the menu, categories, customers, and stats change to the new store's data. |
| AC-6 | Each store's cart is independent; it is preserved when switching and returning. |
| AC-7 | A customer is selected from the dropdown or a "new customer" is created (relevant to that store). |
| AC-8 | The full order registration flow (customer ← search ← filter ← add ← cart ← checkout ← register) works without errors. |
| AC-9 | Checkout contains only "customer, payment method, notes, summary"; there is no order type/table number/address field. |
| AC-10 | After registration, the order number and summary are shown, and the active store's stats increase. |
| AC-11 | Fonts: main title 600, secondary title 500, body 400; primary color stone charcoal. |

---

## 11. Out of Scope / Future Items

- Management of pending orders and order history.
- Receipt printing/sharing.
- Real online payment (payment gateway).
- Integration with the real Manouch API (visitor login, store list, order registration).
- Multi-user/role support (store manager).
- PWA version and installation on phone.

---

## 12. Dependencies and Open Questions

1. **Ravi font:** obtaining the web license and the `Ravi-Regular / Medium / SemiBold (woff2)` files and placing them in `fonts/` — until then the Vazirmatn fallback is active. *(Open question for the product owner)*
2. **Data source:** the Manouch store-builder API address for replacing the sample data.
3. **Visitor profile photo:** the real avatar link from the user account.
4. **Pricing/discount rules:** in the current version, discounts are zero and delivery fees are removed; add if needed.

---

## 13. Appendix: Prototype Implementation Status

| File | Description |
|---|---|
| `index.html` | The entire app (inline HTML + CSS + JS) — single file |
| `fonts/fonts.css` | Ravi font definition (ready) + Vazirmatn fallback |
| `fonts/vazir-*.woff2` | Local (offline) Vazirmatn font |
| `assets/avatar.png` | Sample visitor profile photo |

**Sample data:** 3 stores (Manouch Central Café ☕, Manouch Restaurant 🍽️, Manouch Fast Food 🍟) with independent menus, customers, and stats.

**Test status:** the main order registration flow, store switching, cart independence, and stats — all automatically tested and verified.
