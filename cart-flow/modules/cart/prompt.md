Here is the finalized PRD with the technology stack section removed.

---

# Manooch Advanced Checkout & Order Flow Engine — Complete Implementation PRD

## 1. Document Metadata

| Field | Value |
| --- | --- |
| **Document Title** | Advanced Checkout & Order Flow Engine — Full Implementation PRD |
| **Version** | 2.0 |
| **Status** | Approved & Ready for Implementation |
| **Prototype Reference** | `checkout-prototype.html` (Validated) |
| **Design System** | Manooch DS v1 (Ravi VF font, token-based) |

---

## 2. Executive Summary & System Context

### 2.1 Objective

Replace the existing basic checkout mechanism with an adaptive checkout engine supporting **three distinct payment architectures**:

* **Flow A** — Online Payment Gateway (Zarinpal / Zipal)
* **Flow B** — Transaction Receipt Upload (Manual bank transfer proof)
* **Flow C** — Conditional Payment / Negotiation (Offline seller-buyer consultation)

The system must maintain uniform processing visibility for both customers and sellers via synchronized state tracking, while providing manual intervention surfaces for offline-negotiated business models.

### 2.2 Success Criteria

* **100% Completion:** All three payment flows execute end-to-end.
* **State Integrity:** Order state transitions strictly adhere to the state machine.
* **Full CRUD:** Sellers can manage all order types via the admin panel.
* **Real-time Tracking:** Customers can track status across all phases dynamically.
* **Robust Uploads:** File uploads support up to 5MB (Image formats/PDF) for receipt and document flows.
* **UI/UX Fidelity:** Mobile-first, RTL layout with Persian typography is pixel-accurate to DS tokens.
* **Type Safety:** Zero TypeScript errors in strict mode.

---

## 3. Architecture Overview

### 3.1 Design System Integration

All components MUST use the Manooch design system tokens defined in `assets/css/main.css`. Reference the `@theme` block for:

* Colors: `var(--color-*)` CSS custom properties
* Spacing: `var(--spacing-*)`
* Radius: `var(--radius-*)`
* Typography: `var(--font-size-*)`, `var(--leading-*)`
* Font weights: mapped to Ravi VF rendering scale

---

## 4. Database Schema & Migrations

### 4.1 Enums & Primary Tables

```sql
-- Migration: 20250101000001_create_orders_table.sql

CREATE TYPE order_status AS ENUM (
  'PENDING_PAYMENT', 'NEGOTIATION', 'AWAITING_DOCUMENTS', 
  'PENDING_APPROVAL', 'PROCESSING', 'SHIPPED', 
  'DELIVERED', 'REJECTED_NEGOTIATION', 'CANCELLED'
);

CREATE TYPE payment_method AS ENUM ('GATEWAY', 'RECEIPT', 'CONDITIONAL');

CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_number SERIAL UNIQUE,
  customer_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE RESTRICT,
  store_id UUID NOT NULL REFERENCES stores(id) ON DELETE RESTRICT,
  status order_status NOT NULL DEFAULT 'PENDING_PAYMENT',
  payment_method payment_method NOT NULL,
  subtotal BIGINT NOT NULL CHECK (subtotal >= 0),
  shipping_cost BIGINT NOT NULL DEFAULT 0 CHECK (shipping_cost >= 0),
  discount_amount BIGINT NOT NULL DEFAULT 0 CHECK (discount_amount >= 0),
  total_amount BIGINT NOT NULL CHECK (total_amount >= 0),
  delivery_address JSONB NOT NULL,
  payment_metadata JSONB NOT NULL DEFAULT '{}',
  seller_notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  paid_at TIMESTAMPTZ,
  shipped_at TIMESTAMPTZ,
  delivered_at TIMESTAMPTZ
);

```

### 4.2 Support Tables

```sql
-- Migration: 20250101000002_create_order_items_table.sql
CREATE TABLE order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  product_title TEXT NOT NULL,
  product_image_url TEXT,
  variant_label TEXT,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price BIGINT NOT NULL CHECK (unit_price >= 0),
  discount_per_unit BIGINT NOT NULL DEFAULT 0,
  total_price BIGINT NOT NULL CHECK (total_price >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Migration: 20250101000003_create_order_documents_table.sql
CREATE TYPE document_type AS ENUM ('RECEIPT', 'BANK_CHECK', 'CASH_RECEIPT');

CREATE TABLE order_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  uploaded_by UUID NOT NULL REFERENCES auth.users(id),
  document_type document_type NOT NULL,
  file_url TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_size INTEGER NOT NULL CHECK (file_size > 0),
  mime_type TEXT NOT NULL,
  reviewed_by UUID REFERENCES auth.users(id),
  reviewed_at TIMESTAMPTZ,
  review_status TEXT CHECK (review_status IN ('pending', 'approved', 'rejected')),
  review_notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

```

### 4.3 Row Level Security (RLS)

* **Customers:** `SELECT` own orders, `INSERT` new orders/documents.
* **Sellers:** `SELECT` / `UPDATE` orders and documents associated with their `store_id`.

---

## 5. Order Lifecycle State Machine

### 5.1 Valid State Transitions

Enforced via `utils/order-state-machine.ts`:

* `PENDING_PAYMENT` $\rightarrow$ `PROCESSING` | `CANCELLED`
* `NEGOTIATION` $\rightarrow$ `AWAITING_DOCUMENTS` | `REJECTED_NEGOTIATION`
* `AWAITING_DOCUMENTS` $\rightarrow$ `PENDING_APPROVAL` | `CANCELLED`
* `PENDING_APPROVAL` $\rightarrow$ `PROCESSING` | `NEGOTIATION` | `AWAITING_DOCUMENTS` | `CANCELLED`
* `PROCESSING` $\rightarrow$ `SHIPPED` | `CANCELLED`
* `SHIPPED` $\rightarrow$ `DELIVERED`

### 5.2 Transition Permission Matrix

| Transition | Who Can Trigger | API Route |
| --- | --- | --- |
| `PENDING_PAYMENT` $\rightarrow$ `PROCESSING` | System (Gateway Callback) | `POST /api/payments/gateway/callback` |
| `NEGOTIATION` $\rightarrow$ `AWAITING_DOCUMENTS` | Seller Only | `POST /api/orders/[id]/status` |
| `AWAITING_DOCUMENTS` $\rightarrow$ `PENDING_APPROVAL` | System (Auto on upload) | `POST /api/orders/[id]/documents` |
| `PENDING_APPROVAL` $\rightarrow$ `PROCESSING` | Seller Only | `POST /api/orders/[id]/status` |
| `PENDING_APPROVAL` $\rightarrow$ `NEGOTIATION` | Seller (Reject & renegotiate) | `POST /api/orders/[id]/status` |
| `PROCESSING` $\rightarrow$ `SHIPPED` | Seller Only | `POST /api/orders/[id]/status` |

---

## 6. API Layer — Server Routes

* **`POST /api/orders`**: Creates order, checks stock snapshots, computes totals, handles initial state mapping based on payment choice.
* **`GET /api/orders/[id]`**: Retrieves full payload (items, status history, documents).
* **`POST /api/orders/[id]/status`**: Seller-only status execution endpoint. Requires `OrderStatus` transition validation.
* **`POST /api/orders/[id]/documents`**: Customer multi-file upload parser. Handles server-side storage interfacing.
* **`POST /api/payments/gateway/request` & `GET /.../callback**`: Handles the Zarinpal/Zipal handshakes.

---

## 7. Frontend State & Composables

### 7.1 Stores

* **Cart Store (`stores/cart.ts`)**: Groups items by `store_id`. Calculates per-store subtotals.
* **Order Store (`stores/order.ts`)**: Manages active checkout states, holds current order payload, handles realtime data subscriptions.
* **Seller Order Store (`stores/sellerOrder.ts`)**: Manages the admin-side dashboard state, filtering, and CRUD operations.

### 7.2 Core Composables

* `useOrderStepper(order)`: Computes the 5-step or 7-step visual progress bar logic dynamically based on `payment_method`.
* `useFileUpload(options)`: Handles 5MB constraints, MIME validation, and direct storage streams.
* `usePersianPrice()`: Localizes integers to Toman formats (`۸,۶۳۵,۰۰۰ تومان`).

---

## 8. View Structure & Component Mapping

### 8.1 Layouts

* `layouts/default.vue`: App header + Bottom Navigation.
* `layouts/checkout.vue`: Streamlined header + Sticky Footer CTA.
* `layouts/seller.vue`: Purple header branding + Admin bottom nav.

### 8.2 Component to Prototype Mapping

| Prototype Screen | Page Route | Core Components |
| --- | --- | --- |
| `screen-cart` | `pages/cart/index.vue` | `CartProductCard`, `CartQuantityControl`, `CartPriceSummary` |
| `screen-checkout` | `pages/checkout/index.vue` | `PaymentMethodSelector`, `ReceiptUploadZone`, `BaseStickyFooter` |
| `screen-success` | `pages/orders/success.vue` | Dynamic messaging based on `payment_method` |
| `screen-order-tracking` | `pages/orders/[id]/index.vue` | `OrderStepper`, `OrderContextBox`, `OrderDocumentUpload` |
| `screen-seller-admin` | `pages/seller/orders/[id]/index.vue` | `SellerCustomerContact`, `SellerNegotiationControls`, `SellerApprovalControls` |

---

## 9. File Upload System

| Parameter | Value |
| --- | --- |
| **Max file size** | 5 MB (5,242,880 bytes) |
| **Allowed MIME types** | `image/jpeg`, `image/png`, `image/webp`, `application/pdf` |
| **Buckets** | `order-receipts` (Flow B), `order-documents` (Flow C) |
| **Path pattern** | `{bucket}/{store_id}/{order_id}/{uuid}.{ext}` |
| **Security** | Private access (signed URLs required for rendering) |

---

## 10. Access Control & Security Rules

* **Middleware Checks:** Route guards (`middleware/auth.ts`, `middleware/seller.ts`) prevent unauthorized UI access.
* **Schema Validation:** All server inputs MUST route through strict schema checks (e.g., `CreateOrderSchema`, `UpdateOrderStatusSchema`).
* **Context Isolation:** Ensure `store_id` boundaries are rigidly enforced for seller API calls, rejecting attempts to poll or mutate competitor stores.

---

## 11. Implementation Sequence

* **Phase 1: Foundation (Days 1-3)** — Database migrations, RLS, Type Definitions, State Machine Utils, Base UI Components.
* **Phase 2: Cart System (Days 3-5)** — Store setup, Local persistence, Price summary components.
* **Phase 3: Checkout Flow (Days 5-8)** — Address selection, Radio group payment UI, Upload zones, Order instantiation.
* **Phase 4: Gateways (Days 8-10)** — Zarinpal integration, Webhooks, Timeout cron jobs.
* **Phase 5: Tracking (Days 10-13)** — Customer view, Stepper logic, Contextual alert boxes, Realtime toasts.
* **Phase 6: Documents (Days 13-15)** — Multi-slot upload UI, Storage bucket mapping, Auto-transitions.
* **Phase 7: Admin Panel (Days 15-19)** — Seller layouts, CRM contact cards, Negotiation controls, Document review frames.
* **Phase 8: Polish (Days 19-22)** — Skeletons, Error boundaries, Empty states, RTL micro-interactions.