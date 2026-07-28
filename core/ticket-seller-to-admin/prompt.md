Here is the fully updated and comprehensive Product Requirements Document (PRD) for the Manooch Ticketing System.

Per your standing instructions, I have run this request through the **`/human`** (User Experience & Psychology) and **`/blindspot`** (Edge Cases & Hidden Risks) frameworks before generating the final PRD.

All coding logic, database schemas, and architectural jargon have been strictly excluded to focus purely on product behavior and business rules.

---

### 🧠 Pre-PRD Analysis

#### 👤 `/human` (User Experience & Psychology)

* **The Seller's State of Mind:** When a seller opens a ticket, they are usually blocked, frustrated, or anxious (e.g., delayed payouts, product rejection, a system bug). The system must feel transparent and reassuring. Seeing exactly when a ticket was read or when a reply is expected lowers anxiety.
* **The Super Admin's Cognitive Load:** Super Admins will be managing dozens of tickets. A simple chronological list will quickly become overwhelming. They need visual cues (e.g., color-coded urgency tags based on topics like "Finance") to avoid burnout and prioritize effectively.

#### 🔍 `/blindspot` (Edge Cases & Hidden Risks)

* **The Re-open Dilemma:** If a Super Admin marks a ticket as "Closed" but the seller's issue isn't actually fixed, what happens? If they can't re-open it, they will just create a duplicate ticket, cluttering the queue. **Fix:** Allow sellers to reply to a closed ticket within 48 hours to automatically revert it to "Open."
* **The "Heavy Upload" Trap:** You mentioned allowing image attachments. If sellers upload raw 20MB photos directly from their phones, it will break the UI and exhaust storage. **Fix:** Institute strict business rules for file size/type constraints at the upload stage.
* **Collision (Concurrency):** What if two Super Admins open the same ticket and start typing a reply at the same time? **Fix:** The MVP must at least visually show if a ticket is "Claimed" by another Super Admin or strictly assign it upon opening.

---

### 📄 Fully Updated PRD: Ticketing System (Seller ↔ Super Admin)

**Project Context:** Manooch Platform
**Objective:** Establish a direct, reliable, and auditable communication channel between Sellers (Store Admins) and Platform Operators (Super Admins) to handle support, financial, and moderation inquiries.

#### **1. Core Business Logic & Ticket Lifecycle**

The system operates on a linear progression to prevent communication gaps and ensure accountability.

**Ticket Status Definitions & Transitions:**

| Status | Business Meaning | Next Action Required By |
| --- | --- | --- |
| **Open** | Ticket created by Seller OR the Seller just replied to a previous Admin message. | Super Admin |
| **Answered** | Super Admin has replied. The issue is pending Seller review or clarification. | Seller |
| **Closed** | Issue resolved. Thread locked from active queue but saved in history. | None (Archived) |

**Status Rules:**

* A ticket automatically shifts to **Open** the moment a Seller submits a new message in the thread.
* A ticket automatically shifts to **Answered** the moment a Super Admin sends a reply.
* Only a Super Admin can manually change the status to **Closed**.
* *(Blindspot Fix)* **Re-opening Rule:** If a Seller replies to a "Closed" ticket within 48 hours of closure, it automatically reverts to **Open**. After 48 hours, the input field is disabled, and they must create a new ticket.

#### **2. User Capabilities & Workflows**

**A. The Seller Experience (Admin Panel)**

* **Dashboard Overview:** Sellers see a clear, chronological history of their tickets. The dashboard uses simple tab filters: "Active" (Open/Answered) and "Resolved" (Closed).
* **Drafting a Request:** * Sellers must select a **Topic** from a predefined dropdown (e.g., *Financial/Payout, Technical Bug, Moderation/Policy, General*).
* They provide a Subject line and a detailed description.
* They can attach a single image (e.g., screenshot, receipt).


* **Continuing the Conversation:** The UI behaves like a chat thread. Sellers can read Admin responses, view attachments, and seamlessly type a reply to keep the conversation going.

**B. The Super Admin Experience (Portal Panel)**

* **Global Queue (Mission Control):** Super Admins view a master table of all platform tickets.
* **Mandatory Sorting:** The default view *must* push "Open" (unanswered) tickets to the very top, sorted by oldest first.
* **Filtering:** Admins can filter by Seller Name, Ticket Topic, and Status.


* **Issue Resolution (Thread View):** Admins can read the full context, expand the Seller's image evidence, and write a reply.
* **Closing the Loop:** Once resolved (e.g., payout approved), the Admin clicks a prominent "Mark as Closed" button.

#### **3. Operational & Evidence Rules**

* **Visibility Boundaries:** Sellers can *only* view tickets they created. They have zero visibility into other stores. Super Admins have global visibility.
* **Evidence Collection (Attachments):** * Users (both Sellers and Admins) can attach exactly **one image** per message.
* *Constraint Rule:* The system must block non-image files (PDFs, docs) and enforce a strict UI warning if the image exceeds the allowed file size (e.g., 5MB).


* **Notification Triggers:** * When a Super Admin replies, an in-app visual notification (red dot/badge) must appear on the Seller's dashboard support icon.
* When a Seller replies or creates a ticket, the ticket bumps to the top of the Super Admin's "Open" queue.



#### **4. Prototype Implementation Plan (UI Blueprints)**

These are the exact views your frontend team must build in the designated directories, based purely on business needs.

**Phase 1: Seller Interface**
**Directory:** `manooch-planings\ticket-seller-to-admin\admin`

1. **`ticket-list-view`:**
* **Primary Action:** "Create New Ticket" button.
* **Display:** Table listing Ticket ID, Subject/Topic, Date Submitted, and Status (with clear color coding: Open = Red/Orange, Answered = Blue/Yellow, Closed = Gray/Green).


2. **`ticket-creation-view`:**
* **Form Interface:** Dropdown menu for Topics, Subject Line input, Large text area for description.
* **Attachment Interface:** A drag-and-drop or click-to-upload area for a single image, clearly stating file limits.
* **Action:** "Submit Request" button (disabled until Topic and Description are filled).


3. **`ticket-thread-view`:**
* **Display:** Conversational layout (chat-bubbles). Seller messages aligned to one side, Super Admin messages on the other. Timestamp on every message.
* **Input Interface:** Sticky reply box at the bottom with an image-attachment icon.



**Phase 2: Super Admin Interface**
**Directory:** `manooch-planings\ticket-seller-to-admin\portal`

1. **`master-support-queue`:**
* **Display:** Comprehensive data table (Columns: Seller Name, Store Name, Ticket ID, Topic, Date, Status).
* **Tools:** Search bar (find by Seller or Ticket ID), Status Toggle (Show All vs. Show Open Only), and Topic Filter.


2. **`ticket-resolution-view`:**
* **Header Info:** Seller name, Store Details, and Ticket Topic permanently visible at the top.
* **Display:** The full conversation thread. Image viewer that expands screenshots on click.
* **Input Interface:** Text area for Admin response.
* **Action:** Two distinct buttons: "Reply & Keep Open" and "Mark as Closed."