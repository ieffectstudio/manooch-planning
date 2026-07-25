Alright, A.Mammad, here is the fully updated Product Requirements Document (PRD). It integrates your new logic for dynamic Minimum Order Quantity (MOQ) configuration on the seller side and the default pricing behavior for variant products on the customer side.

All coding logic and technical architecture have been stripped out to focus entirely on user flows, product behavior, and strict business rules.

---

## **Product Requirements Document (PRD): E-commerce Product Flow (List ➔ PDP ➔ Cart)**

### **1. Product Overview**

This product is a mobile-optimized e-commerce discovery and selection flow for a specialized handicraft store ("Manooch"). It handles a diverse catalog, accommodating everything from simple fixed-price retail items to complex wholesale goods that require unit conversions, multi-attribute variant selection, and dynamic minimum order quantities.

### **2. User Roles**

* **Customer (Buyer):** Browses products, views dynamic pricing, selects variants/units, adheres to order minimums, and adds items to the cart.
* **Seller (Admin):** Configures product catalog, sets inventory, defines variant pricing, and establishes minimum order rules per product.

---

### **3. Seller Admin Flow: Product Configuration**

To support the complex frontend logic, the seller must have specific controls during the "Add/Edit Product" phase.

* **Minimum Order Quantity (MOQ) Configuration:**
* **Behavior:** The seller interface includes a numeric input field labeled **"حداقل سفارش" (Minimum Order Quantity)** grouped with stock/inventory settings.
* **Rules:** * The default value is strictly `1`.
* The value cannot be less than `1` and cannot exceed the total available stock.


* **Frontend Trigger:** If the seller sets this value greater than `1`, the product automatically inherits wholesale properties: the orange "عمده" (Wholesale) badge appears on the PLP, and MOQ warnings/stepper limits activate on the PDP.


* **Variant & Default Price Setup:**
* **Behavior:** When a seller creates a product with multiple variants (e.g., sizes or colors with different prices), the system must establish a "Starting Price."
* **Rules:** The system automatically calculates the cheapest available variant and sets it as the product's baseline default price to display on catalog pages.



---

### **4. Core Customer Flows & Screen Requirements**

#### **4.1 Product Listing Page (PLP)**

* **Search & Filtering:** Includes a persistent search bar and a horizontally scrollable category filter (e.g., All, Hand-woven carpets, Copper & Brass, Ceramics, Wood).
* **Product Cards:** Cards dynamically display badges based on the seller's configuration:
* *Discount Badge:* Shows percentage off (e.g., 15%).
* *Variant Badge:* Indicates multiple options (Color/Size).
* *Wholesale Badge:* Triggered automatically if the seller set the MOQ > 1.


* **Dynamic Pricing Display (The "From" Rule):** * If a product is simple (no variants), it shows the exact price.
* If a product has variants with varying prices, the card must display the lowest variant price prepended with **"از" (From)** (e.g., `از ۱۲,۰۰۰,۰۰۰ تومان`).



#### **4.2 Product Detail Page (PDP) Archetypes**

The PDP dynamically morphs into four distinct archetypes based on the product's complexity.

**Archetype 1: Simple Product (Retail)**

* **Behavior:** Fixed price, no variations. MOQ is 1.
* **Rules:** Shows original price (strike-through) and discounted price. Can be added to the cart immediately.

**Archetype 2: Variant Product (Retail)**

* **Behavior:** Requires configuration (e.g., Color, Size).
* **Initial Load Rule (Default Selection):** Upon opening the page, the system must **automatically pre-select** the attributes of the cheapest variant. This prevents a blank or `null` price state and immediately gives the user a valid price calculation.
* **Rules:** Mandatory fields are marked with `*`. Out-of-stock variations must be visually disabled (crossed out/dimmed) and unselectable.

**Archetype 3: Bulk / Wholesale Product**

* **Behavior:** Designed for bulk materials. Introduces customizable measurement units and strict minimums.
* **Rules:**
* **Unit Selection:** Users choose the measurement unit (Meter, Zar, Yard). Changing the unit instantly recalculates the base price.
* **MOQ Enforcement:** The quantity stepper defaults to the seller-defined MOQ (e.g., 5). The UI displays a persistent warning ("حداقل سفارش: ۵ متر").
* **Dynamic Total:** Features a breakdown showing Unit Price × Quantity = Total.

**Archetype 4: Complex Product (Wholesale + Variants)**

* **Behavior:** Combines all complexities (variants + seller-defined MOQ).
* **Initial Load Rule:** Automatically pre-selects the cheapest variant combination and defaults the stepper to the seller-defined MOQ.
* **Rules:** Includes a "Selection Summary" before the final sticky CTA to ensure the buyer understands their complex configuration and total cost.

#### **4.3 Cart Preview (Screen: Cart)**

* **Behavior:** Acts as an interstitial confirmation screen after an item is added.
* **Rules:** * Displays a success banner indicating the current cart count.
* Line items explicitly display the user's chosen configuration (e.g., "طلایی · سایز ۵۴ · ۱ عدد" or "۵ متر").
* Calculates Subtotal, applies Shipping Costs, and displays the Final Total.



---

### **5. Complexities & Global Business Rules**

**Rule 1: Strict MOQ Validation**

* The quantity stepper on the PDP can never be decremented below the seller-defined MOQ.
* If a user attempts manual bypass, the system must block it and flash the localized warning box. The "Add to Cart" button strictly validates against this minimum before proceeding.

**Rule 2: Real-Time Dynamic Pricing & Unit Conversions**

* The UI must react instantly without page reloads.
* If a user changes a unit (e.g., Meter to Yard) or selects a larger size variant, the base price and the aggregate total (Quantity × New Base Price) must update simultaneously on the screen.

**Rule 3: Mandatory Variant Enforcement**

* Users cannot add products to the cart unless all mandatory attributes (Color, Size) are actively selected. (Handled gracefully by the new Default Selection rule upon page load).

**Rule 4: State Preservation & Accessibility**

* When a user selects a variant (e.g., Color), the label above the selection chips must dynamically update to explicitly state the chosen option in text (e.g., "رنگ زمینه * : لاکی") to ensure clarity before adding to the cart.