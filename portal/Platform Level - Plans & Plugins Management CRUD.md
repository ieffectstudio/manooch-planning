Context: Phase 6 of the Super Admin PRD. We need to build the global management pages for "اشتراک‌ها و پلن‌ها" (Plans & Subscriptions) and "پلتفرم -> افزونه‌ها" (Platform Plugin Registry). This is where the Super Admin defines what plans and plugins exist on the platform.

Tasks:
1. Plans Management List & CRUD: 
   - Build a data table listing all global platform plans (e.g., رایگان, پایه, حرفه‌ای, سازمانی).
   - Build a Create/Edit Plan form. Required fields: Plan Name, Monthly Price, Annual Price, Limits (Max Products, Storage Limit), and a dynamic list of included features.
   - Add status toggles to activate or retire a plan (retired plans cannot be selected for new stores, but remain active for existing ones).
2. Plugin Registry List & CRUD:
   - Build a data table for the Global Plugin Registry.
   - Build a Create/Edit Plugin form. Required fields: Plugin Name, Identifier/Slug, Category (e.g., Sales, UI, Shipping), Description, Icon, and a Global Status Toggle (Active/Maintenance/Deprecated).
   - Rule: Any plugin created here automatically appears in the "افزونه‌ها" (Plugins) section of every individual Store Edit page (built in Phase 2).

Confirm when the UI and data flows for creating and managing global plans and plugins are complete.