Claude, we are building a simple, streamlined "Stock and Pricing" feature for the Manooch Seller Admin Panel. This is an MVP feature; absolutely do not over-engineer it with complex warehouse management, database schemas, or ERP logic. We are strictly generating the frontend UI architecture right now.

**Target Directory:** `manooch-planings\stock`

Before you write any code, execute the following analytical directives:
**`/blindspot`**: Analyze my requirements below. Identify any frontend blindspots specifically related to PWA mobile constraints, RTL layout edge cases (e.g., input icons flipping incorrectly, text truncation on long product names), or missing UI states.
**`/human`**: Stop after your blindspot analysis. Present your findings to me concisely and ask for my explicit approval to proceed before you generate the files.

Once I approve, execute these two tasks exactly as specified:

**Task 1: Generate `stock-list.html**`

* **Layout:** Create a mobile-first PWA wrapper (`max-w-md mx-auto relative min-h-screen bg-gray-50 pb-20`, `dir="rtl"`).
* **Navigation:** Include the standard 4-item Sarnakh fixed bottom navigation bar at the base.
* **Header:** Add a clean header titled "انبار و قیمت‌گذاری" (Inventory & Pricing).
* **Search:** Add a sticky search bar right below the header to filter products.
* **Product List (3 Cards):** Create a list of 3 Product Cards. Each card MUST show:
1. A small placeholder thumbnail.
2. Product Title.
3. Current Price (e.g., 250,000 تومان).
4. Stock Status Badge. You must create 3 distinct visual states using Tailwind: Green "موجود" (In Stock) with the quantity, Yellow "رو به اتمام" (Low Stock), and Red "ناموجود" (Out of Stock / 0).
5. An "Edit" (ویرایش) icon button.



**Task 2: Generate `stock-edit.html**`

* **Layout:** Use the exact same global wrapper (`pb-20` + standard bottom nav).
* **Header:** Add a Header with a Back button and the title: "بروزرسانی قیمت و موجودی" (Update Price & Stock).
* **Context Card:** Add a summary card at the very top showing the selected product's name and thumbnail so the seller has visual confirmation of what they are editing.
* **Form Container:** Create a Form section inside a clean white card (`bg-white p-4 rounded-xl shadow-sm`).
* **Pricing Mode Toggle:** A segmented control or simple radio toggle between "قیمت ساده" (Simple Price) and "قیمت متغیر/ویژگی" (Variable/Attribute Price).
* **Simple Mode UI:** Add numeric inputs for "قیمت اصلی" (Base Price), "قیمت با تخفیف" (Discounted Price - optional), and "موجودی کل" (Total Stock).
* **Variable Mode UI (Simulated):** Add a visually distinct section (e.g., a slightly gray background container) simulating a list of attributes (e.g., "سایز L", "سایز XL"). Each row must have a mini input for its specific Price and Stock.
* **Sticky CTA:** Add a large, primary "ثبت تغییرات" (Save Changes) sticky button fixed at the bottom (sitting just above the bottom nav).

**Strict Design Constraints:**

1. Strictly use standard Tailwind CSS classes. No custom CSS files.
2. The entire document MUST be strictly RTL (`dir="rtl"`). Do not use `flex-row-reverse` hacks; rely on Tailwind's logical properties (`ms-`, `me-`, `ps-`, `pe-`) or standard flex with `dir="rtl"` taking over.
3. Match the clean, spacious, Shadcn-like aesthetic of the existing Manooch app.

Confirm when you understand these instructions and provide your `/blindspot` analysis.