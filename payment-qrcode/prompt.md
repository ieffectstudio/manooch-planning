Claude, we need to significantly upgrade the Payment Link module in the Manooch Admin panel. I need you to create a new list view, update the existing QR code view, and ensure the global Sarnakh footer navigation is present.

Target Directory: C:\Sanji\prod-project\modules\payment-qrcode\html\

Task 1: Dashboard Text Update
Locate the dashboard file where the payment link entry is. Change the text "لینک پرداخت ارسال شده" to "لینک های پرداخت". Ensure there is a small counter/badge next to it representing the total count of links.

Task 2: Create payment-link-list.html (The New List View)

Create this new file. Wrap the main content with pb-20 and include the standard Sarnakh fixed bottom navigation bar (Home, Orders, Products, Profile).

Add a top header with the title "لینک‌های پرداخت".

Add a prominent button at the top: "ایجاد لینک پرداخت" (Create Payment Link) that visually looks like a primary CTA.

Below the button, build a list of past payment links. Each list item card should show: Amount (e.g., 500,000 تومان), Date, and a Status Badge. Create three examples using Tailwind badges for statuses: پرداخت شده (Green), منتظر پرداخت (Yellow), and کنسل شده (Red/Gray).

Task 3: Update payment-link-qrcode.html (The Share/Creation View)

Apply the same global wrapper (pb-20) and add the standard Sarnakh fixed bottom navigation bar.

Build the "Add Price" Bottom Sheet (HTML structure): Add a hidden overlay (fixed inset-0 bg-black/50 hidden) and a slide-up panel (fixed bottom-0 bg-white rounded-t-3xl p-6 hidden). Inside this sheet, put a number input for the price and a submit button "ثبت مبلغ".

Add basic inline JavaScript (for prototyping purposes) so that clicking "افزودن مبلغ" (Add Price) removes the hidden class from the bottom sheet.

Simulate the UI state change: When the bottom sheet submit button is clicked, hide the bottom sheet, display the entered price on the main page, and change the original button text from "افزودن مبلغ" to "ویرایش مبلغ" (Edit Price).

Design Constraints:

Strictly use standard Tailwind CSS classes.

The entire document MUST be RTL (dir="rtl"). Rely entirely on standard DOM order.

The design must feel like a native mobile app / PWA.

Confirm when these files are generated and updated.