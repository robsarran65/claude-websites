# Stripe Integration Plan — Sarran AI Solutions LLC

## Recommended approach

Use Stripe-hosted pages instead of collecting card details on `sarranai.com`. This keeps the
static Vercel website simple, reduces PCI scope, and lets Stripe handle payment authentication,
receipts, payment-method display, and checkout security.

## 1. Payments — AI Time Savings Assessment

- Product: **AI Time Savings Assessment**
- Price: **$250 USD, one time**
- Checkout: Stripe-hosted Payment Link
- Website flow: visitor first submits the simple “Find My Time Savings” form; after Robert
  confirms fit, the customer receives the secure payment link
- Checkout collects the individual name, optional business name, and email
- Stripe creates a Customer and a paid invoice for the completed one-time purchase
- The hosted confirmation tells the customer Robert will contact them within one business day

### Sandbox objects

- Product: `prod_VDGze1QgJjgDyB`
- Price: `price_1UCqRjDYh2dmOeqasU4KsAMM`
- Payment Link: `plink_1UCqSADYh2dmOeqa1yPmOJyv`
- Test checkout: `https://book.stripe.com/test_bJeeVd1ereVc4xT96ycEw00`

These are test-mode objects and must not be used as the public production checkout.

## 2. Invoicing — custom consulting and implementation

Start in the Stripe Dashboard rather than building an invoicing API:

1. Create the customer.
2. Add clear project or milestone line items.
3. Use the Stripe-hosted invoice page for payment.
4. Add payment terms such as due on receipt, Net 15, or Net 30 based on the agreement.
5. Use invoice reminders and Dashboard status tracking.

Use an invoice template with the Sarran AI logo, brand colors, footer, and optional purchase-order
field. Add ACH later for larger invoices if customers request it.

## 3. Billing — future recurring support plans

Create recurring products only after the plan names, prices, and included services are approved.
Use flat monthly prices, Stripe-hosted Checkout, and the Stripe Customer Portal. Recommended
defaults:

- Charge at the beginning of each billing period
- Cancel at the end of the current period
- Let customers update payment methods and download invoices in the Customer Portal
- Enable Smart Retries and automated failed-payment emails
- Use Stripe Quotes for custom recurring agreements

## 4. Payment status and automation

The Payment Link can launch without custom server code. Do not treat a browser redirect as proof
of payment. Before automatically scheduling or delivering paid work, add a Vercel serverless
webhook that verifies Stripe signatures and handles:

- `checkout.session.completed`
- `checkout.session.async_payment_succeeded`
- `payment_intent.payment_failed`
- `invoice.paid`
- `invoice.payment_failed`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `charge.refunded`

Store `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` only in Vercel environment variables. Never
place them in HTML, JavaScript sent to the browser, Git, or documentation. The publishable key is
not needed for the current Payment Link approach.

## 5. Test-to-live checklist

- Complete Stripe business verification and payout-bank setup
- Enable two-step authentication
- Configure the Sarran AI logo, brand color, support email, statement descriptor, privacy URL,
  and terms URL
- Run a successful sandbox checkout and confirm the invoice, receipt, customer, and payment record
- Run a declined-card sandbox test
- Confirm tax treatment with a qualified adviser; use Stripe Tax threshold monitoring until any
  collection obligations are established
- Recreate the product, price, and Payment Link in live mode
- Add only the live Payment Link to the production website or customer email
- Make one controlled live payment and refund test before advertising the checkout

## Official Stripe references

- No-code integration options: https://docs.stripe.com/no-code/get-started
- Payment Links: https://docs.stripe.com/payment-links
- Invoicing: https://docs.stripe.com/invoicing
- Billing: https://docs.stripe.com/billing
- Customer Portal: https://docs.stripe.com/customer-management
- Webhooks: https://docs.stripe.com/webhooks
