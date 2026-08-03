import express from 'express';
import crypto from 'node:crypto';
import { config, describeConfig } from './config.js';
import { store } from './db.js';
import { mockGateway } from './mockGateway.js';
import { createPayment, verifyPayment, ZarinpalError, ALERT_CODES, ERROR_FA } from './zarinpal.js';

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

if (config.mode === 'dummy') {
  app.use('/__mock/pg', mockGateway(config.appUrl));
}

function alertOps(code, ctx) {
  if (ALERT_CODES.has(code)) {
    console.error(`[ALERT] ZarinPal code ${code} — ${ERROR_FA[String(code)] || ''}`, ctx);
  }
}

// --- demo: create an order so there is something to pay for -----------------
app.post('/api/orders', (req, res) => {
  const amount = Number(req.body?.amount ?? 1000);
  const title = req.body?.title ?? 'سفارش آزمایشی';
  res.json(store.createOrder({ amount, title }));
});

// --- step 1: checkout -------------------------------------------------------
app.post('/api/payments/checkout', async (req, res) => {
  const { orderId, mobile, email } = req.body || {};
  const order = store.getOrder(orderId);
  if (!order) return res.status(404).json({ error: 'order not found' });
  if (order.status === 'paid') return res.status(409).json({ error: 'order already paid' });

  // R3: amount comes from the DB, never from the client.
  const amount = order.amount;

  try {
    const { authority, startPayUrl, fee, feeType } = await createPayment({
      amount,
      description: `پرداخت سفارش ${order.id} - ${order.title}`,
      mobile,
      email,
      orderId: order.id,
    });

    // R7: persist before redirecting the user away.
    store.createPayment({
      id: 'pay_' + crypto.randomBytes(6).toString('hex'),
      order_id: order.id,
      authority,
      amount,
      currency: config.currency,
      status: 'pending',
      ref_id: null,
      card_pan: null,
      card_hash: null,
      fee,
      fee_type: feeType,
      error_code: null,
      error_message: null,
      mode: config.mode,
      created_at: new Date().toISOString(),
      verified_at: null,
    });

    res.json({ authority, redirectUrl: startPayUrl });
  } catch (err) {
    if (err instanceof ZarinpalError) alertOps(err.code, { orderId });
    console.error('[checkout]', err.code, err.message);
    res.status(502).json({ error: err.message, code: err.code });
  }
});

// convenience: browser-friendly redirect version
app.get('/pay/:orderId', async (req, res) => {
  const r = await fetch(`${config.appUrl}/api/payments/checkout`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ orderId: req.params.orderId }),
  });
  const j = await r.json();
  if (!r.ok) return res.status(r.status).send(`<pre dir="ltr">${JSON.stringify(j, null, 2)}</pre>`);
  res.redirect(j.redirectUrl);
});

// --- step 2: callback + verify ---------------------------------------------
app.get('/api/payments/callback', async (req, res) => {
  const authority = req.query.Authority || req.query.authority;
  const status = req.query.Status || req.query.status;

  const payment = authority ? store.getPayment(authority) : null;
  if (!payment) return res.status(404).send(page('پرداخت یافت نشد', 'شناسه مرجع نامعتبر است.', false));

  // R4: Status=OK alone proves nothing, but Status=NOK is a definitive no.
  if (status !== 'OK') {
    if (payment.status === 'pending') store.updatePayment(authority, { status: 'canceled' });
    return res.send(page('پرداخت انجام نشد', 'تراکنش لغو شد یا ناموفق بود.', false));
  }

  // R2: already settled? show the receipt, don't fulfil again.
  if (payment.status === 'paid') {
    return res.send(page('پرداخت موفق', `شماره پیگیری: ${payment.ref_id}`, true));
  }

  try {
    const v = await verifyPayment({ authority, amount: payment.amount }); // R1 + same amount
    const fulfilled = store.markPaid(authority, {
      ref_id: v.refId,
      card_pan: v.cardPan,
      card_hash: v.cardHash,
      fee: v.fee,
      fee_type: v.feeType,
      error_code: null,
      error_message: null,
    });
    if (fulfilled) {
      // >>> business fulfilment goes here, exactly once <<<
      console.log(`[fulfil] order ${payment.order_id} ref_id ${v.refId}`);
    }
    res.send(page('پرداخت موفق', `شماره پیگیری: ${v.refId}`, true));
  } catch (err) {
    const code = err instanceof ZarinpalError ? err.code : 'ERR';
    alertOps(code, { authority, orderId: payment.order_id });
    store.updatePayment(authority, {
      status: 'failed',
      error_code: typeof code === 'number' ? code : null,
      error_message: err.message,
    });
    res.send(page('پرداخت ناموفق', err.message, false));
  }
});

// --- status lookup ----------------------------------------------------------
app.get('/api/payments/:authority', (req, res) => {
  const p = store.getPayment(req.params.authority);
  if (!p) return res.status(404).json({ error: 'not found' });
  res.json(p);
});

// --- R6: reconciliation (run from cron every ~15 min) -----------------------
app.post('/api/payments/reconcile', async (_req, res) => {
  const stale = store.stalePending(20 * 60 * 1000);
  const results = [];
  for (const p of stale) {
    try {
      const v = await verifyPayment({ authority: p.authority, amount: p.amount });
      const fulfilled = store.markPaid(p.authority, { ref_id: v.refId, card_pan: v.cardPan });
      if (fulfilled) console.log(`[fulfil:reconcile] order ${p.order_id} ref_id ${v.refId}`);
      results.push({ authority: p.authority, result: 'paid', refId: v.refId });
    } catch (err) {
      store.updatePayment(p.authority, {
        status: 'expired',
        error_code: typeof err.code === 'number' ? err.code : null,
        error_message: err.message,
      });
      results.push({ authority: p.authority, result: 'expired', code: err.code });
    }
  }
  res.json({ checked: stale.length, results });
});

app.get('/health', (_req, res) => res.json({ ok: true, ...describeConfig() }));

function page(title, subtitle, ok) {
  return `<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>${title}</title>
<style>body{font-family:system-ui,sans-serif;background:#0f172a;color:#e2e8f0;display:grid;place-items:center;height:100vh;margin:0}
.c{background:#1e293b;padding:2.5rem;border-radius:16px;text-align:center;min-width:320px}
h1{color:${ok ? '#22c55e' : '#ef4444'};margin:0 0 .5rem}p{color:#94a3b8}</style></head>
<body><div class="c"><h1>${title}</h1><p>${subtitle}</p><p><a style="color:#60a5fa" href="/">بازگشت</a></p></div></body></html>`;
}

app.get('/', (_req, res) => {
  res.type('html').send(`<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<title>ZarinPal demo</title><style>body{font-family:system-ui,sans-serif;background:#0f172a;color:#e2e8f0;
display:grid;place-items:center;height:100vh;margin:0}.c{background:#1e293b;padding:2rem;border-radius:16px;min-width:340px}
button{width:100%;padding:.8rem;border:0;border-radius:10px;background:#eab308;font-weight:700;cursor:pointer}
input{width:100%;padding:.6rem;border-radius:8px;border:1px solid #334155;background:#0f172a;color:#e2e8f0;margin:.4rem 0}
small{color:#94a3b8}</style></head><body><div class="c">
<h2>پرداخت آزمایشی زرین‌پال</h2>
<small>حالت: <b>${config.mode}</b> — واحد: ${config.currency}</small>
<input id="amt" type="number" value="1000">
<button onclick="go()">پرداخت</button>
<script>async function go(){
 const amount=Number(document.getElementById('amt').value);
 const o=await (await fetch('/api/orders',{method:'POST',headers:{'content-type':'application/json'},
   body:JSON.stringify({amount})})).json();
 const r=await fetch('/api/payments/checkout',{method:'POST',headers:{'content-type':'application/json'},
   body:JSON.stringify({orderId:o.id})});
 const j=await r.json();
 if(j.redirectUrl) location.href=j.redirectUrl; else alert(JSON.stringify(j));
}</script></div></body></html>`);
});

app.listen(config.port, () => {
  console.log(`▶ http://localhost:${config.port}`, describeConfig());
});

export default app;
