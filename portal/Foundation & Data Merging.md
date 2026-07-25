Context: We are restructuring the Manooch Super Admin Panel. This is Phase 1 of the PRD. The goal is to merge the "Seller" entity entirely into the "Store" entity (1:1 relationship) and update the initial UI to reflect this.

Tasks:
1. Update the core data structure: The Store entity must now absorb all seller information. Add an owner profile to the store containing: full name, mobile, email, national ID, avatar, date joined, identity verified status, and bank account info.
2. Data Flow: Ensure all data requests that previously fetched "Sellers" now fetch this data directly from the newly structured "Store" owner data.
3. Sidebar UI: Completely remove the "فروشندگان" (Sellers) menu item from the navigation.
4. Store List View UI: Update the main stores table columns to display: لوگو (Logo), نام (Name), مالک (Owner - format: Name + Mobile), دامنه (Domain), پلن (Plan), وضعیت (Status), محصولات (Products).
5. Add Quick Actions per row in the list view: [مشاهده] [غیرفعال کردن] [تغییر پلن].

Confirm when this conceptual data merge and list view update is complete.