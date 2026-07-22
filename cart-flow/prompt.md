Claude, we are implementing the final integration of the Cart and Order flow. You must use the finalized HTML/Tailwind assets located at C:\Sanji\Manooch-Deps\manooch-planings\cart-flow\final and wire them directly into our NextJS/React application.

CRITICAL CONSTRAINT: We do NOT have a live payment gateway active yet. You must mock the online payment routing. Execute this integration in 4 strict phases. Do not change our existing backend database schema; focus entirely on the frontend state machine and UI rendering.

PHASE 1: PDP to Cart Wiring

Ensure the useCart store correctly accepts the variant-aware and unit-aware payloads from the PDP.

The Cart List page must render the exact UI from the final directory, displaying selected colors/units accurately.

PHASE 2: Checkout & Mock Payment Routing
Implement the Checkout page with 3 distinct payment methods.

Online Gateway (درگاه پرداخت): If selected, clicking "Submit" must bypass all API calls and immediately execute router.push('/checkout/success').

Upload Receipt (کارت به کارت/فیش): If selected, render an image upload component. Submitting the order places it in a PENDING_RECEIPT_APPROVAL state.

Conditional/Negotiation (پرداخت شرایطی): If enabled by the seller, selecting this bypasses upload/payment and submits the order directly into a NEGOTIATION state.

PHASE 3: Customer Order Detail & Stepper UI

Create a dynamic visual Progress Bar (Stepper) component for the Customer Order Detail page.

The stepper must clearly reflect the exact level of the process based on the payment type:

Receipt Flow: Pending Approval -> Approved -> Processing -> Shipped.

Negotiation Flow: Negotiation -> Agreement Reached -> Receipt Uploaded -> Shipped.

Use strict RTL styling (dir="rtl") and our standard p-6 md:p-8 bg-white rounded-2xl card aesthetics for these screens.

PHASE 4: Seller Dashboard (Admin) Order Hooks

The Seller's Order Detail panel must use the exact same visual Stepper component so the seller and customer see the identical state.

Inject Action Buttons for the Seller based on the current state:

If PENDING_RECEIPT_APPROVAL: Show "Approve Receipt" (تایید فیش) and "Reject" buttons.

If NEGOTIATION: Show "Confirm Negotiation & Request Payment" (تایید توافق).

If Approved: Show "Mark as Shipped" (ارسال شد).

Analyze the UI assets in C:\Sanji\Manooch-Deps\manooch-planings\cart-flow\final and \modules\order to extract the HTML structures, then implement these 4 phases natively in NextJS. Confirm when you have mapped the state logic.