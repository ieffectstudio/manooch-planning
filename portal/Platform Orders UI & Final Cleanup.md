Context: Final phase of the Super Admin PRD. We need to implement the UI for the newly defined Platform Orders and clean up the old legacy navigation.

Tasks:
1. Sidebar: Rename "سفارش‌ها" to "سفارش‌های پلتفرم". 
2. Platform Orders List View: Build a data table with columns for: شماره (Order ID), فروشگاه (Store), نوع سفارش (Type), مبلغ (Amount), وضعیت (Status), تاریخ (Date). Add filters for Type, Status, Store, and Date Range.
3. Create Order Modal: Build a manual order creation form. Flow: Select Store -> Select Type (Plan/Add-on) -> Select Specific Item -> Auto-calculate amount -> Add optional discount -> Select Payment Method -> Add note -> Submit.
4. Order Detail View: Build a comprehensive page showing order details, audit logs, and action buttons: Mark as Paid, Activate Service, Cancel Order, Issue Refund, Extend Expiry, Add Note.
5. Cleanup 1: Finalize the Sidebar layout exactly as specified (Grouped by اصلی, پلتفرم, and توسعه).
6. Cleanup 2: Remove the old customer orders page. Move old store customer orders to only be accessible as a strictly read-only table inside the Store Edit Page -> Group 2 -> "سفارش‌های فروشگاه".

Confirm when the UI is implemented and the legacy items are cleaned up.
