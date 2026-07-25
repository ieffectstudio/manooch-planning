Context: Phase 2 of the Super Admin PRD. We are completely redesigning the Store Edit page to replace the unscalable horizontal tabs with a vertical section-navigation layout (sticky scroll, 240px width).

Tasks:
1. Build a persistent Top Header displaying: Store Avatar, Store Name, Domain, Status Toggle, Current Plan Badge (color-coded), "تغییر پلن" button, Creation Date, and Quick Stats (Orders, Products, Followers, Revenue).
2. Implement the Status Toggle user flow:
   - Activate: Confirmation modal "فروشگاه فعال شود؟" -> Save -> Success Toast -> Green badge.
   - Deactivate: Modal requiring a reason field -> Save -> Success Toast -> Red badge.
3. Build the Section Navigation (Left Sidebar) with these exact groups:
   - Group 1 (اطلاعات اصلی): اطلاعات کلی, مالک فروشگاه (displaying the merged seller data from Phase 1), پلن و اشتراک, دامنه, درگاه پرداخت.
   - Group 2 (افزونه‌ها): Dynamically list ALL available platform plugins. If installed on this store, show the management UI and a green dot badge. If not, show an inactive state with an "Activate" button.
   - Group 4 (ناحیه خطر): Suspend, Delete (requires typing name to confirm), Transfer Ownership, and Data Export.
4. Build the Plan Change Modal: Triggered by "تغییر پلن", showing current plan, a selector for new plans (رایگان, پایه, حرفه‌ای, سازمانی), Start Date (Jalali picker), End Date, and an Admin Note field.

Confirm when the layout and these core flows are implemented.