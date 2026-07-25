Here is the comprehensive Product Requirements Document (PRD) based on the prototype you provided. I have stripped away all technical architecture and coding logic to focus entirely on product behavior, user flows, business rules, and edge cases.

---

# **Product Requirements Document (PRD): Complete Checkout & Order Flow**

## **1. Product Overview**

The product is a specialized e-commerce checkout and order management flow designed to handle both standard B2C retail transactions and complex, high-ticket (B2B-style) negotiated transactions. It accommodates immediate online payments, manual bank transfers, and a multi-step conditional payment process involving physical bank checks and admin negotiations.

## **2. User Roles**

* **Customer (Buyer):** Browses the cart, selects payment methods, uploads financial documents (receipts/checks), and tracks order status.
* **Seller (Admin):** Manages negotiated orders, contacts buyers, reviews uploaded financial documents, and moves orders through fulfillment states.

---

## **3. Core User Flows & Screen Requirements**

### **3.1 Cart Management (Screen: Cart)**

* **Conditions:** The cart calculates the total order value dynamically.
* **Rules:**
* Calculation Formula: `(Sum of Items) + (Shipping Cost) - (Total Discounts) = Final Payable Amount`.
* Users can increment or decrement item quantities.
* If quantity reaches zero, the item should be removed (implied rule).
* Discounts (e.g., "15% off") and shipping perks (e.g., "Free Shipping") must be clearly badged on the item level.



### **3.2 Checkout & Payment Selection (Screen: Checkout)**

This is a high-complexity screen where the user selects how they will pay. The choice dictates the entire downstream order flow.

* **Option A: Online Gateway (درگاه آنلاین)**
* *Behavior:* Standard redirect to a payment gateway (e.g., Zarinpal).


* **Option B: Bank Receipt Upload (ثبت با بارگذاری رسید)**
* *Behavior:* Exposes an upload zone for the user to attach a screenshot of a manual bank transfer.
* *Validation:* Only JPG/PNG, max 5MB.
* *Rule:* The user *cannot* submit the order unless a file is successfully attached.


* **Option C: Conditional / Negotiation (شرایطی - مذاکره با ادمین)**
* *Behavior:* Displays a warning that an admin will contact them. No payment is collected upfront.
* *Rule:* Submitting this creates an order in a "Pending Negotiation" state.



### **3.3 Dynamic Order Tracking (Screen: Order Tracking)**

The tracking timeline (stepper) is dynamic and changes completely based on the payment method chosen during checkout.

* **Gateway Path:** Registered ➔ Paid ➔ Preparing ➔ Shipped ➔ Delivered.
* **Receipt Path:** Registered ➔ **Verifying Receipt (Admin Action)** ➔ Preparing ➔ Shipped ➔ Delivered.
* **Conditional Path (Highest Complexity):** Registered ➔ **Negotiation** ➔ **Awaiting Documents** ➔ **Admin Approval** ➔ Preparing ➔ Shipped ➔ Delivered.

### **3.4 Document Upload Hub (For Conditional Orders Only)**

Once a seller successfully negotiates a conditional order, the buyer's tracking screen morphs into a document upload hub.

* **Check Uploads (چک‌های بانکی):**
* Users can add multiple bank checks via a Bottom Sheet form.
* *Mandatory fields:* Check Image, Check Number, Amount, Due Date.
* *Optional fields:* Bank Name.
* Users can edit or delete checks before final submission.


* **Cash Receipt (رسید پرداخت نقد):**
* Users can upload a single image representing a cash deposit (optional, but acts as a supplement to checks).


* **Submission Rule:** The "Submit All Documents" button is only actionable if *at least one* check OR *one* cash receipt is uploaded.

---

## **4. Seller Admin Flow (Screen: Seller Admin)**

The seller interface allows the admin to process complex "Conditional" orders. This involves a two-phase state machine.

### **Phase 1: Negotiation (مرحله مذاکره)**

* **Trigger:** Customer places a "Conditional" order.
* **Actions Available to Seller:**
1. **Call Customer:** Deep link to phone dialer.
2. **Add Notes:** Internal text area for negotiation details.
3. **Success (موفقیت مذاکره):** Pushes the order back to the buyer, unlocking the "Document Upload Hub" on the buyer's tracking page.
4. **Cancel Order (لغو سفارش):** Terminates the order if an agreement isn't reached.



### **Phase 2: Document Approval (بررسی مدارک ارسالی)**

* **Trigger:** Customer finishes uploading checks/receipts and submits them.
* **Actions Available to Seller:**
1. **Review Docs:** View thumbnails, amounts, and dates of the submitted checks/receipts.
2. **Approve Order (تایید سفارش):** Marks the financial step complete. The order moves to "Preparing."
3. **Reject Documents (رد مدارک):** Bounces the order back to the "Negotiation" phase, forcing the buyer to re-upload or renegotiate.



---

## **5. Complexities & Edge Cases**

1. **State Reversals (The Loop):** In the Conditional flow, if a seller rejects the uploaded checks (e.g., the image is blurry or the date is wrong), the system must cleanly revert the buyer's state back to "Awaiting Documents" without wiping out all their previously entered check data, allowing them to fix the specific issue.
2. **Form Validation & Currency Formatting:** When adding checks in the bottom sheet, the "Amount" input must format numbers dynamically into currency formats (e.g., adding commas) in real-time to prevent high-value typos, while converting Persian numerals to English numerals for backend processing.
3. **File Management:** The system requires temporary file storage. If a user uploads a receipt during checkout but abandons the page, or if they upload 3 checks and delete 1 before final submission, the system must handle the cleanup of those orphaned image files.
4. **Concurrent Status Viewing:** The buyer and seller are interacting with the same order state simultaneously. If the seller clicks "Success" on a negotiation, the buyer's tracking screen must reflect the new "Upload Documents" state without requiring a hard refresh (implies a need for real-time state polling or webhooks).

---

*Let me know if you need to drill down into the specific data schemas required to support these rules or if you need the PRD expanded into user stories.*