Claude, we are building a simple, streamlined "Stock and Pricing" feature for the Manooch Seller Admin Panel. This is an MVP feature; do not over-engineer it with complex warehouse management or ERP logic.

Target Directory: manooch-planings\stock

Task 1: Generate stock-list.html

Create a mobile-first PWA layout (max-w-md mx-auto relative min-h-screen bg-gray-50 pb-20, dir="rtl"). Include the standard 4-item Sarnakh fixed bottom navigation bar.

Add a Header: "انبار و قیمت‌گذاری" (Inventory & Pricing).

Add a sticky search bar right below the header to filter products.

Create a list of 3 Product Cards. Each card must show:

A small placeholder thumbnail.

Product Title.

Current Price (e.g., 250,000 تومان).

Stock Status Badge (Create 3 states: Green "موجود" with quantity, Yellow "رو به اتمام" for low stock, Red "ناموجود" for 0 stock).

An "Edit" (ویرایش) icon button.

Task 2: Generate stock-edit.html

Use the same global wrapper (pb-20 + standard bottom nav).

Add a Header with a Back button and title: "بروزرسانی قیمت و موجودی" (Update Price & Stock).

Add a summary card at the top showing the selected product's name and thumbnail so the user knows what they are editing.

Create a Form section inside a clean white card (bg-white p-4 rounded-xl shadow-sm):

Pricing Type Toggle: A segmented control or simple radio toggle between "قیمت ساده" (Simple Price) and "قیمت متغیر/ویژگی" (Variable/Attribute Price).

Simple Mode UI: Add numeric inputs for "قیمت اصلی" (Base Price), "قیمت با تخفیف" (Discounted Price - optional), and "موجودی کل" (Total Stock).

Variable Mode UI (Simulated): Add a visually distinct section (maybe slightly gray background) simulating a list of attributes (e.g., "سایز L", "سایز XL") where each row has a mini input for Price and Stock.

Add a large, primary "ثبت تغییرات" (Save Changes) sticky button at the bottom (just above the bottom nav).

Design Constraints:

Strictly use standard Tailwind CSS classes.

The entire document MUST be RTL (dir="rtl"). Do not use flex-row-reverse.

Match the clean, Shadcn-like aesthetic of the existing app.

Confirm when the HTML/Tailwind files have been successfully generated in the directory.