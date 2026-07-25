Here is the fully updated, consolidated Product Requirements Document (PRD). It retains the entire end-to-end user journey and integrates the two new business rules regarding Cart Line Item separation (Variants and Units).

As strictly requested, all code logic, state management architecture, and backend structure have been excluded.

---

# Product Requirements Document (PRD): End-to-End E-commerce & Order Flow

**Product:** Manooch E-commerce Platform

**Scope:** Product Listing ➔ Product Detail ➔ Cart ➔ Checkout (3 Payment Methods) ➔ Order Tracking

## 1. Executive Summary

This product flow facilitates a specialized e-commerce experience designed to handle both standard retail transactions and complex, high-ticket (B2B-style) negotiated transactions. The system guides users from discovering products to cart management, and finally through a multi-tiered checkout process that supports instant online payments, manual bank transfers, and a conditional payment process involving physical bank checks and admin negotiations.

## 2. Core User Flows: Discovery to Cart

### 2.1 Product Listing Page (PLP)

* **Search & Filtering:** A persistent search bar and horizontal scrollable category filters (e.g., Hand-woven carpets, Copper & Brass, Ceramics, Wood).
* **Dynamic Badges:** Product cards visually indicate business logic:
* *Discount Badge:* Shows percentage off.
* *Variant Badge:* Indicates multiple options (Color/Size) are available.
* *Wholesale Badge:* Indicates bulk ordering rules apply.



### 2.2 Product Detail Page (PDP)

* **Variant Selection:** Users must select mandatory attributes (e.g., Color, Size). The UI updates text labels dynamically to reflect the chosen option (e.g., "رنگ زمینه : لاکی").
* **Dynamic Pricing & Conversions:** If a user changes a unit of measurement (e.g., Meter to Yard) or selects a different size, the base price and aggregate total update instantly on the screen.
* **Quantity Management (MOQ):** The quantity stepper strictly enforces the Minimum Order Quantity (MOQ) defined by the seller. The UI blocks the user from decrementing below this limit.

### 2.3 Cart Management & Line Item Rules

* **Calculations:** The cart dynamically calculates: `(Sum of Items) + (Shipping Cost) - (Total Discounts) = Final Payable Amount`.
* **Line Item Uniqueness (Variants):** If a user adds a product with a specific attribute (e.g., Color: Blue), and then adds the *same* product with a different attribute (e.g., Color: Red), the cart must store and display them as **two completely separate line items**. They must not merge.
* **Line Item Uniqueness (Units):** If a user adds a product with a specific unit (e.g., 2 Bags), and then adds the *same* product with a different unit (e.g., 3 Cans), the cart must store and display them as **two completely separate line items**.
* **Line Item Clarity (UI):** Each item in the cart must explicitly display the user's chosen configuration on the product card:
* The selected variant must be shown as a clear text label (e.g., "رنگ : آبی").
* The quantity counter must explicitly render the name of the chosen unit next to the number, rather than a generic default (e.g., "۲ گونی" instead of "۲ عدد").



## 3. Checkout & The 3 Payment Methods

When the user proceeds to checkout, they are presented with three distinct payment pathways based on the seller's configuration.

### Method 1: Online Gateway (درگاه پرداخت آنلاین)

* **Flow:** Standard instant payment via providers like Zarinpal or Zipal.
* **Action:** User is redirected to the banking portal.
* **State Resolution:** * *Success:* Order status instantly becomes **Processing / Approved**.
* *Failure/Cancel:* Order status becomes **Payment Failed**, prompting the user to try again.



### Method 2: Receipt Upload (فیش واریزی)

* **Flow:** The user performs a manual bank transfer (Card-to-Card or Sheba) outside the platform and uploads the proof of payment.
* **Customer Action:** User uploads the transaction receipt image and submits the order.
* **System State:** Order is submitted with a **Pending Approval** status.
* **Seller Action:** The seller sees the uploaded receipt in their Admin panel.
* *Approve:* Seller clicks "Approve Receipt". Order moves to **Preparing / Shipped**.
* *Reject:* Seller clicks "Reject". Order is flagged, and the customer is prompted to re-upload valid proof.



### Method 3: Conditional / Negotiation (پرداخت شرایطی / چکی)

* **Flow:** Used for high-ticket or wholesale orders where the buyer and seller must agree on custom payment terms (e.g., paying via physical bank checks).
* **Phase 1: Negotiation Initialization**
* Customer selects "Conditional Payment". No money is requested upfront.
* Order is submitted with a **Negotiation** status.
* Seller receives a notification. Both parties review the order and negotiate terms (e.g., via phone).


* **Phase 2: Agreement & Document Hub (check-upload flow)**
* If terms are agreed upon, the seller updates the system, unlocking the "Document Upload Hub" on the customer's tracking page.
* **Customer Action:** The user adds their financial documents:
* *Bank Checks:* User opens a bottom sheet to add checks. They enter the Amount, Due Date, Bank Name, and Check Serial Number, then upload an image of the check. (Multiple checks can be added).
* *Cash Receipt:* User can toggle and upload an image of a cash deposit receipt if the agreement included a partial cash upfront payment.


* Customer clicks "Submit All Documents".


* **Phase 3: Final Approval**
* Seller reviews the uploaded checks and receipts (amounts, dates, images).
* *Approve:* Order moves to **Processing / Shipped**.
* *Reject:* Order state reverts back to the document upload phase, forcing the buyer to fix the issues.



## 4. Order Tracking & Stepper UI (The Shared Dashboard)

A critical requirement is that **both the Customer and the Seller (Admin) must see the exact same visual progress of the order** to avoid confusion.

### 4.1 Dynamic Progress Bar (Stepper)

The visual stepper dynamically changes its labels based on the chosen payment method:

* **For Receipt Flow:** `Pending Approval` ➔ `Approved` ➔ `Processing` ➔ `Shipped`.
* **For Negotiation Flow:** `Negotiation` ➔ `Agreement Reached` ➔ `Receipt/Check Uploaded` ➔ `Shipped`.

### 4.2 Seller (Admin) Action Hooks

The Seller's UI injects contextual action buttons directly tied to the current step on the progress bar:

* *If PENDING_RECEIPT_APPROVAL:* Show "Approve Receipt" (تایید فیش) and "Reject" buttons.
* *If NEGOTIATION:* Show "Confirm Negotiation & Request Payment" (تایید توافق).
* *If APPROVED/PROCESSING:* Show "Mark as Shipped" (ارسال شد).

## 5. Business Rules & UI/UX Constraints

1. **Strict State Reversals:** In the Conditional (چکی) flow, rejecting an uploaded check does not cancel the order; it cleanly reverts the order state back one step, allowing the customer to upload a corrected document.
2. **Input Formatting (Currency):** Whenever a user is typing a monetary amount (e.g., adding the amount to a bank check), the input field must dynamically format the numbers (adding commas every 3 digits) to prevent high-value typos. It must also support and standardize Persian numerals.
3. **Mandatory Document Enforcement:** The system strictly blocks users from clicking "Submit" in the Receipt or Conditional upload stages unless at least one valid media file (image) has been attached.
4. **No Cart Bypassing:** The "Add to Cart" and "Checkout" buttons must remain completely disabled or block progression if mandatory product variants (Color/Size) are unselected or if the MOQ is not met.
5. **Strict Cart Separation Rules:** A product is only considered a "duplicate" in the cart if the Base Product, the Selected Variant/Attribute, AND the Selected Unit of Measurement are all completely identical. If any of these differ, the system must strictly create a separate line item.