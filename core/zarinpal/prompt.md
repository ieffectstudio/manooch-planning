# Task — Fix the Zarinpal (dummy) payment gateway: share-payment flow, checkout page, and result pages

## 1. Context

The project is **manooch-planings**. The Zarinpal integration lives under `core/zarinpal/`.

A **complete, working Zarinpal payment example** (documentation + code) is available at
`manooch-planings/core/zarinpal/zarinpal-payments`. Treat that example as the **source of truth** for how the
gateway is supposed to behave. Our current implementation deviates from it and is broken in several places.

A reference UI screenshot of the target end state is at
`manooch-planings/core/zarinpal/Screenshot 2026-08-03 154843.png`.

## 2. Ground rules

- **Dummy / sandbox mode only.** Do **not** wire up real money movement, real settlement, or a production
  gateway. Everything must be simulated so the full flow can be exercised end to end.
- Merchant ID to use for the dummy setup: `c3e83cb7-e3ca-4a18-8836-64e8191bfec9`
- All work must be done on the **`feat-payment`** branch.
- Align behaviour, naming, states, and terminology with the reference example in `zarinpal-payments`
  rather than inventing a parallel approach.
- Keep the existing design system: new or corrected controls must match the styling, colour, placement,
  and interaction pattern of the app's existing equivalents — no one-off styles.

## 3. What I want from you

1. **First, a written plan** describing how you will repair the share-payment feature and the checkout page:
   what is broken, in what order you will fix it, and what each fix changes from the user's point of view.
2. Then the implementation, on `feat-payment`.

Do not skip straight to code. I want the plan reviewable before anything is changed.

---

## 4. Problems to fix

### P1 — The dummy gateway itself is not working

**Current:** The Zarinpal dummy gateway does not complete a payment cycle. Because of this, both the
share-payment feature and the checkout page are unusable.

**Expected:** A fully simulated Zarinpal flow that can be run repeatedly in development: a payment can be
initiated, can sit in a pending state, and can be driven to both a successful and a failed outcome —
using the dummy merchant ID above, without touching a real payment provider.

---

### P2 — Checkout page is broken

**Current:** The checkout page does not work correctly against the dummy gateway.

**Expected:** Checkout works end to end in dummy mode and mirrors the behaviour shown in the
`zarinpal-payments` example, including how it reacts to a successful payment and to a failed/cancelled one.

---

### P3 — Missing result pages (success / error)

**Current:** A success page appears to exist already, but it is not verified as working. There is no
error/failure page at all.

**Expected:**
- Verify and fix the existing **success** page so a completed dummy payment lands on it correctly.
- Add an **error / failure** page for cancelled, failed, or expired payments.
- Both pages must be reachable from the real flow (not just directly by URL) and must clearly communicate
  the outcome to the user.

---

### P4 — Payment link is missing share and "change amount" actions

**Current:** After a payment link exists, the user has no way to share it and no way to change the amount.

**Expected:** On the payment-link view (the state shown in the reference screenshot) there must be:
- a **share** action that opens the device/native share sheet for the payment link, and
- a **change amount** action that lets the user edit the amount.

Both are presented as icon buttons next to the QR code, exactly as in
`Screenshot 2026-08-03 154843.png`.

---

### P5 — Missing helper text above/near the QR code

**Current:** The instruction line **«برای دریافت پول، کد QR خود را نمایش دهید»** is not displayed.

**Expected:** This text must be shown on the payment-link / QR screen, as in the reference screenshot.

---

### P6 — «ایجاد لینک پرداخت» button uses the wrong pattern

**Current:** The «ایجاد لینک پرداخت» button is rendered as an ordinary inline button.

**Expected:** It must be a **floating CTA**, consistent with the floating CTA pattern already used
elsewhere in the app (same placement behaviour, same visual treatment).

---

### P7 — "Create new ticket" button is visually inconsistent

**Current:** The **create new ticket** button does not match the app's other buttons — its style and colour
are off.

**Expected:** Restyle it so its shape, size, and colour follow the same rules as the app's other primary
buttons. No custom colour that exists nowhere else.

---

### P8 — Amount cannot be updated while the payment is pending

**Current:** Once a link is shared, the amount is effectively frozen.

**Expected:** While the payment status is **"Waiting for payment"**, the user must be able to update the
amount, and the shared link must reflect the updated amount. Updating must not be allowed once the payment
has already succeeded or failed.

---

### P9 — Unnecessary page navigation just to open the amount bottom sheet ⚠️ (main UX bug)

**Current:** On the list page, tapping «ایجاد لینک پرداخت» navigates the user away to the
`payment-link/create` page, and the only thing that page does is open the «افزودن مبلغ» bottom sheet.
The whole page transition exists for no reason.

**Note:** The *creation logic itself is fine* — this is purely about the navigation/presentation being wrong.

**Expected:** Tapping «ایجاد لینک پرداخت» **on the list page** should:
1. open the «افزودن مبلغ» bottom sheet in place, with **no page navigation**;
2. after the amount is entered and confirmed, show the **QR code** together with the **share** and
   **change amount** icon buttons — the layout shown in `Screenshot 2026-08-03 154843.png`.

The user should never leave the list page for this flow.

---

## 5. Definition of done

- [ ] Dummy Zarinpal gateway completes a full simulated payment cycle with merchant ID
      `c3e83cb7-e3ca-4a18-8836-64e8191bfec9`.
- [ ] Checkout page works end to end in dummy mode.
- [ ] Success page verified working; error page added and reachable.
- [ ] Payment-link view matches the reference screenshot: QR code, «برای دریافت پول، کد QR خود را نمایش دهید»,
      share icon button, change-amount icon button.
- [ ] «ایجاد لینک پرداخت» is a floating CTA consistent with other CTAs.
- [ ] "Create new ticket" button matches the app's standard button style and colour.
- [ ] Amount is editable while status is "Waiting for payment", and the shared link reflects the change.
- [ ] No navigation to `payment-link/create` when opening the «افزودن مبلغ» bottom sheet from the list page.
- [ ] All changes committed on the `feat-payment` branch.

## 6. Out of scope

- Real payments, real settlement, production credentials, or going live.
- Any redesign beyond making the listed elements consistent with what already exists.