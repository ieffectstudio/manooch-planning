Below is a **complete production-grade prompt** you can paste directly into Claude to implement the updated Check + Receipt upload system exactly as designed in your prototype.

This prompt assumes:

- ✅ Nuxt 3  
- ✅ TypeScript  
- ✅ Tailwind v4  
- ✅ Manooch Design System tokens already configured  
- ✅ Supabase (DB + Storage + RLS)  
- ✅ Existing Order system with status machine  

---

# ✅ FULL CLAUDE IMPLEMENTATION PROMPT  
## Feature: Conditional Payment – Check BottomSheet + Receipt Upload

---

You are implementing a production-ready feature for Manooch (Nuxt 3 + TypeScript + Tailwind v4 + Supabase).

Follow ALL instructions precisely.

This is NOT a prototype. This must be clean, modular, typed, scalable production code.

---

# 🎯 FEATURE OVERVIEW

We are implementing the **Customer Document Upload system** for `CONDITIONAL` orders.

The customer must be able to:

1. Upload multiple **bank checks**
   - Each check includes:
     - `check_no`
     - `price`
     - `date_of_check`
     - `bank_name?` (optional)
     - `image` (required)
   - Added via **BottomSheet form**
   - Editable
   - Deletable

2. Upload optional **cash receipt**
   - Single image only
   - Replaceable
   - Deletable

3. Submit all documents
   - At least **one check OR receipt must exist**
   - After submission → order transitions:
     `AWAITING_DOCUMENTS → PENDING_APPROVAL`

---

# 🧱 ARCHITECTURE RULES

Follow project conventions:

```
components/order/
components/ui/
composables/
stores/
server/api/orders/
types/
utils/
```

Use:

- ✅ Pinia
- ✅ Supabase Storage
- ✅ Zod validation
- ✅ Order state machine
- ✅ Design tokens
- ✅ Strict TypeScript

NO any types.  
NO inline styles.  
NO logic in template.  
NO duplication.  

---

# 🗂 FILES TO CREATE / UPDATE

Create the following:

---

## ✅ 1️⃣ TYPES

### `types/check.ts`

```ts
export interface CheckInput {
  id?: string
  check_no: string
  price: number
  date_of_check: string
  bank_name?: string
  image_url: string
  file_name: string
  file_size: number
}
```

---

## ✅ 2️⃣ DATABASE CHANGES

Extend `order_documents` table:

```sql
ALTER TABLE order_documents
ADD COLUMN check_no TEXT,
ADD COLUMN check_price BIGINT,
ADD COLUMN check_due_date DATE,
ADD COLUMN bank_name TEXT;
```

Only used when `document_type = 'BANK_CHECK'`.

---

## ✅ 3️⃣ STORAGE BUCKET

Bucket: `order-documents`

Path:

```
order-documents/{store_id}/{order_id}/{uuid}.jpg
```

Private bucket.  
Use signed URLs for viewing.

---

# 🧠 STATE MANAGEMENT

---

## ✅ 4️⃣ Pinia Store

### `stores/orderDocuments.ts`

Store responsibilities:

```ts
state:
  checks: CheckInput[]
  receipt: {
    image_url: string | null
    file_name: string | null
  }
  loading: boolean

getters:
  hasAnyDocument: boolean

actions:
  addCheck(check: CheckInput)
  updateCheck(index: number, check: CheckInput)
  removeCheck(index: number)
  setReceipt(image_url: string, file_name: string)
  removeReceipt()
  submitDocuments(orderId: string)
```

`submitDocuments`:
- Validates minimum requirement
- Calls API
- Clears local state on success

---

# 🧩 COMPONENTS

---

## ✅ 5️⃣ Bottom Sheet Component

### `components/ui/BaseBottomSheet.vue`

Must support:

- v-model:open
- Backdrop
- Slide animation
- Scroll lock
- Slot content
- Sticky footer slot

Animation:
- translateY(100%) → 0
- Backdrop fade

Use design tokens.

---

## ✅ 6️⃣ Check Bottom Sheet Form

### `components/order/CheckFormSheet.vue`

Props:
- `modelValue?: CheckInput`
- `mode: 'create' | 'edit'`

Emits:
- `save(check: CheckInput)`
- `close`

Form fields:

- Image upload (required)
- Check number (required)
- Price (required, formatted input)
- Due date (required)
- Bank name (optional)

Validation via Zod:

```ts
check_no: string().min(3)
price: number().positive()
date_of_check: string().regex(/^\d{4}\/\d{2}\/\d{2}$/)
```

Price input:
- Persian formatted
- Store numeric internally

---

## ✅ 7️⃣ Check Upload Section

### `components/order/CheckUploadSection.vue`

Contains:

- Header
- Info banner
- Check list
- "افزودن تصویر چک" button

Features:

- Renders list from Pinia
- Each card shows:
  - Number badge
  - check_no
  - price
  - date
  - bank
  - edit button
  - delete button
- Opens CheckFormSheet

---

## ✅ 8️⃣ Receipt Upload Section

### `components/order/CashReceiptUpload.vue`

Single image only.

States:

- Empty
- Uploaded
- Replace
- Delete

Uses `useFileUpload` composable.

---

## ✅ 9️⃣ Submit Button Section

### `components/order/OrderDocumentSubmit.vue`

Button:
"ثبت همه مدارک و ارسال برای بررسی"

Disabled unless:
- at least 1 check OR receipt exists

On click:
- calls store.submitDocuments()
- show toast
- navigate

---

# 📤 FILE UPLOAD

---

## ✅ 10️⃣ useFileUpload composable

Must:

- Validate size ≤ 5MB
- Validate MIME
- Upload to Supabase
- Return public URL

Image only for:
- Check
- Receipt

---

# 🌐 API

---

## ✅ 11️⃣ API Route

### `POST /api/orders/[id]/documents`

Request:

```json
{
  checks: CheckInput[],
  receipt?: {
    image_url: string
  }
}
```

Logic:

1. Authenticate
2. Validate order belongs to user
3. Ensure order.status === AWAITING_DOCUMENTS
4. Insert each check as order_document (BANK_CHECK)
5. Insert receipt as order_document (CASH_RECEIPT)
6. Transition order → PENDING_APPROVAL
7. Insert status history
8. Return success

---

# 🎨 UI RULES

Must use Manooch tokens:

- Primary buttons → `bg-primary-500`
- Secondary → `bg-secondary-500`
- Success → `bg-success-600`
- Border → `border-frame-main`
- Radius → `rounded-2xl`
- Text sizes:
  - small: 11px
  - text: 13px

NO hardcoded hex.

---

# ✅ VALIDATION RULES

On submit:

If:
- checks.length === 0
- AND receipt is null

→ show error toast:

"حداقل یک چک یا رسید باید بارگذاری شود"

---

# ✅ UX REQUIREMENTS

- Smooth bottom sheet animation
- Prevent body scroll when sheet open
- Persian digit formatting
- Live validation errors
- Disable submit while loading
- Toast notifications for:
  - add
  - edit
  - delete
  - upload
  - submit

---

# ✅ SECURITY

- Never trust client
- Re-validate everything in API
- Only allow order owner
- Only allow correct status
- Reject invalid state transition

---

# ✅ STATE MACHINE

Transition:

```
AWAITING_DOCUMENTS → PENDING_APPROVAL
```

Use:

```
validateTransition(from, to)
```

---

# ✅ WHAT YOU MUST RETURN

Claude must generate:

1. All component files
2. Store file
3. Composable
4. API route
5. Zod schema
6. Types
7. Example integration in order detail page

Clean code.  
Fully typed.  
No explanations.  
Only production code.

---

If you want, I can now also generate:

- 🔥 A version optimized for Claude 3 Opus
- 🔥 A version optimized for Claude Sonnet
- 🔥 A shorter compressed prompt
- 🔥 A multi-step prompt strategy for large context builds