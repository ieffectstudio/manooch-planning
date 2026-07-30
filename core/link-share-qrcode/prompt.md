Got it ✅  
You’re clarifying that:

> **`entry.html` is the exact public link page that customers open to view the restaurant menu.**  
It is NOT the dashboard share UI.

So the structure changes.

Let’s fix everything clearly and give you the correct Claude prompt.

---

# ✅ Correct Feature Understanding

## ✅ What Each File Actually Is

### 1️⃣ `entry.html`
- ✅ This is the **public restaurant link**
- ✅ Customers open this link
- ✅ This is the actual menu/view page
- Example:
  ```
  https://manooch.app/menu/{restaurant-slug}
  ```
- This is NOT a dashboard page.

---

### 2️⃣ `dashboard-entry.html`
- ✅ This is inside the seller dashboard
- ✅ Shows the seller their public link
- ✅ Has buttons:
  - Copy link
  - Show QR
  - Print
- This is the management/share UI

---

### 3️⃣ `view.html`
- ✅ This is a clean printable QR page
- ✅ Designed for printing & putting on tables/walls
- ✅ Contains:
  - Restaurant name
  - Logo
  - Large QR code
  - Public URL (entry.html link)
  - “Scan to view our menu”

---

# ✅ Correct User Flow

```
Customer Flow:
Customer scans QR
        ↓
Opens entry.html
        ↓
Sees restaurant menu

Seller Flow:
Seller opens dashboard
        ↓
Sees dashboard-entry.html
        ↓
Copies link OR prints QR (view.html)
```

---

# ✅ Correct Feature Description (Clear Version)

The seller can:

1. Copy their public restaurant link (entry.html)
2. Generate a QR code for that link
3. Print a branded QR page (view.html)

The public link always points to:
```
entry.html
```

---

# ✅ Fixed Claude Prompt (Correct Version)

Use this instead 👇

---

```
I am building a feature called "link-share-qrcode" for my restaurant 
management app called Manooch.

Important clarification:

- entry.html is the public restaurant page.
  This is the actual link customers open to view the restaurant menu.
  Example format:
  https://manooch.app/menu/{restaurant-slug}

- dashboard-entry.html is inside the seller dashboard.
  It allows the seller to:
    1. Copy the public link (entry.html)
    2. View a QR code generated from that link
    3. Print a QR page

- view.html is a clean, printable page.
  It contains:
    - Restaurant logo
    - Restaurant name
    - Large QR code
    - The public URL (entry.html link)
    - Text: "Scan to view our menu"
  This page is print-optimized and contains no navigation or dashboard UI.

There is no backend logic.
Treat restaurant name, slug, and logo as placeholder variables.
Use plain HTML and CSS only unless specified.

Now generate [specify which file] based on this structure.
```

---

# ✅ Implementation Plan (Corrected)

## Branch:
```
feat-link-share-qrcode
```

---

## Step 1 — dashboard-entry.html

Inside dashboard:
- Show public link (entry.html URL)
- Copy button
- “Show QR” button
- “Print QR” button → opens view.html

---

## Step 2 — view.html

Clean printable layout:
- Centered design
- Big QR
- Restaurant branding
- Print-ready CSS

---

## Step 3 — entry.html

This remains the public menu page.
No dashboard logic inside it.
No QR generation here.

---

# ✅ Final Clear Structure

```
core/link-share-qrcode/html/
│
├── entry.html              → Public restaurant page (customer view)
├── dashboard-entry.html    → Seller share UI
└── view.html               → Printable QR page
```

---

If you want, I can now:

- ✅ Create the final polished feature documentation
- ✅ Write a production-level implementation plan
- ✅ Create a clean PR description for GitHub
- ✅ Refine UI/UX flow for better product thinking

Tell me which one you want 🚀