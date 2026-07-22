implment the C:\Sanji\Manooch-Deps\manooch-planings\cart-flow\final\index.html its totaly ok except cart page and these changes i say (its should move to own task) 

Please execute these fixes step-by-step:

1. Admin: Add Product Bottom Sheet (Unit Flow)

Do not change the existing unit selection flow. * Simply add a new input field for "Minimum Order" (حداقل سفارش) inside the current Unit Bottom Sheet. Bind it to the existing form state so it saves correctly per unit.

2. Storefront: Price Inquiry (استعلام قیمت) Display

Admin Rule: Keep the current logic exactly as it is (when "Inquiry" toggle is ON, price/discount inputs are disabled/hidden, but attribute stock remains). Do not remove this. the Inquiry in admin add product should not change its ok

Storefront Fix: In the Storefront ProductCard and the PDP price section, add a conditional render. If the product has price inquiry enabled, completely replace the price and discount UI elements with the text "استعلام قیمت".

3. Dynamic Subdomain & Panel Routing Bug

Fix the "Visit Shop" link (on the seller registration complete page) and the "Go to panel" link (in the Storefront hamburger menu).

They currently route to the wrong URLs. Implement dynamic environment checking:

If development: Store URLs must resolve to http://[shopname].localhost:3700 and Admin Panel URLs must resolve to http://localhost:3701.

If production: Use the standard production domain setup.

4. Auth Flow: Registration Complete Redirect

On the Seller Registration "Complete" page, the button "ورود به پنل" (Login to panel) currently redirects to the login page.

Fix this: The user is already authenticated at this step. Change the redirect/link to push the user directly to the /dashboard page.

5. Auth Flow: Error Handling & Toasts (Login/Register)

Remove 429 Text: Intercept or suppress the 429 (Too Many Requests) error explicitly in the auth flow. Remove the text "بیش از حد مجازش".

Add Toasts: Currently, no toasts appear when a user enters wrong credentials or fails registration. Wire up the existing toast.error() or toast() UI component to properly display the backend error messages during the onError state of the Login and Register mutations.

Execute these surgical patches and confirm when each step is completed. Do not over-engineer the solutions

give me full plan to fix this also create brnach and push changes on repo you need