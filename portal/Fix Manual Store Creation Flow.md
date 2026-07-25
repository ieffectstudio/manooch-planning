Context: Phase 7 of the Super Admin PRD. We need to fix the manual "+ افزودن فروشگاه" (Add Store) flow. Because we merged the "Seller" and "Store" entities in Phase 1, the old fields for creating a store are no longer correct. We need a proper creation flow that handles both the store data and the owner assignment in one go.

Tasks:
1. Redesign the "Add Store" Modal/Page: Triggered from the main Stores list view.
2. Step 1: Owner Assignment (مالک فروشگاه):
   - Allow the admin to search for an existing user (by mobile number) to assign as the owner, OR fill in fields to create a new owner profile right here (Full Name, Mobile Number, National ID).
3. Step 2: Store Identity (هویت فروشگاه):
   - Required fields: Store Name (نام فروشگاه), Store Subdomain/Domain (دامنه - must be validated for uniqueness), and Category/Industry.
4. Step 3: Initial Configuration (تنظیمات اولیه):
   - Required fields: Select an Initial Plan (from the global plans list), and set Initial Status (Active/Inactive).
5. Post-Creation Flow: Upon successful creation, immediately redirect the Super Admin to the newly created Store's full Edit Page (the vertical layout we built in Phase 2).

Confirm when the manual store creation fields and flow are corrected to match the new architecture.