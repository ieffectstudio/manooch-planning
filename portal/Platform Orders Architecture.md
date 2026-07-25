Context: Phase 4 of the Super Admin PRD. We are redefining the "Orders" concept. The Super Admin panel should NO LONGER show end-customer orders across all stores. "Orders" now strictly means "Platform Orders" (Manooch's own orders where stores purchase plans, plugins, or services).

Tasks (Establish the data architecture for Platform Orders):
1. Create the data structure for Platform Orders, ensuring it is entirely separate from store-level customer orders.
2. Support these specific Order Types: خرید پلن (Plan Purchase), تمدید پلن (Plan Renewal), ارتقای پلن (Plan Upgrade), تنزل پلن (Plan Downgrade), خرید افزونه (Add-on Purchase), سرویس سفارشی (Custom Service).
3. Support these Statuses: جدید (New), در انتظار پرداخت (Awaiting Payment), پرداخت شده (Paid), فعال‌سازی شده (Activated), لغو شده (Cancelled), بازپرداخت شده (Refunded), منقضی شده (Expired).
4. Required Fields: order number, associated store, order type, item details (plan/duration), original amount, discount amount, final amount, payment status, payment method, payment reference, creation date, paid date, activation date, expiry date, and admin notes.

Confirm when the data model is established and ready for the UI.