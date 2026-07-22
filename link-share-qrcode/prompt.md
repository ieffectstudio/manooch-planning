Claude, we are finalizing the "Share Store Link / QR Code" feature for the Manooch Admin panel. I need you to update and fix the main view file to ensure it matches our global app layout.

Target File: C:\Sanji\Manooch-Deps\manooch-planings\link-share-qrcode\html\view.html

Task 1: Implement the Missing Footer Navigation (Sarnakh Style)
The current view.html is missing the persistent bottom navigation bar.

Wrap the main content of the page in a container with padding at the bottom (e.g., pb-20) so content isn't hidden behind the footer.

Create a fixed bottom navigation bar (fixed bottom-0 w-full max-w-md mx-auto bg-white border-t border-gray-200 z-50).

Add 4 standard mobile app navigation items inside the footer (e.g., Home, Orders, Products, Profile) using SVG placeholders for the icons and small text labels below them. Space them evenly using Flexbox.

Task 2: Polish the Share View UI
Ensure the main content area of view.html contains:

A clean Header with a "Back" arrow and the title "اشتراک‌گذاری فروشگاه" (Share Store).

A central Card component displaying a placeholder QR Code image (assume the path is ../assets/qr-placeholder.png or use a generic styled div).

A "Copy Link" section below the QR code: an input field showing a dummy store URL (e.g., manooch.com/store/myshop) with a button attached to the side labeled "کپی" (Copy).

Design Constraints:

Strictly use standard Tailwind CSS classes.

The entire document MUST be RTL (dir="rtl"). Do not use flex-row-reverse.

Ensure the design feels like a native mobile app / PWA, mirroring a Shadcn-like clean aesthetic.

Read the existing view.html, apply these fixes, and overwrite the file with the complete, updated HTML structure. Confirm when done.