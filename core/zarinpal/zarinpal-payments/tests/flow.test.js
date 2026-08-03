/**
 * End-to-end tests against the dummy gateway. No network, no real money.
 * Run: npm test   (server must NOT already be running on the same port)
 */
process.env.ZARINPAL_MODE = 'dummy';
process.env.PORT = process.env.PORT || '3999';
process.env.APP_URL = `http://localhost:${process.env.PORT}`;
process.env.ZARINPAL_MERCHANT_ID = 'c3e83cb7-e3ca-4a18-8836-64e8191bfec9';
process.env.ZARINPAL_CURRENCY = 'IRT';

const BASE = process.env.APP_URL;
let passed = 0, failed = 0;

function ok(name, cond, extra = '') {
  if (cond) { passed++; console.log(`  ✅ ${name}`); }
  else { failed++; console.log(`  ❌ ${name} ${extra}`); }
}

const j = async (path, opts) => {
  const r = await fetch(BASE + path, opts);
  return { status: r.status, body: await r.json().catch(() => null) };
};
const post = (path, body) =>
  j(path, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body || {}) });

async function newPending(amount = 5000) {
  const { body: order } = await post('/api/orders', { amount });
  const { body: co } = await post('/api/payments/checkout', { orderId: order.id });
  return { order, authority: co.authority, redirectUrl: co.redirectUrl };
}
const finish = (authority, outcome) =>
  fetch(`${BASE}/__mock/pg/finish/${authority}/${outcome}`, { redirect: 'follow' });

async function run() {
  const { store } = await import('../src/db.js');
  store.reset();
  await import('../src/server.js');
  await new Promise((r) => setTimeout(r, 400));

  console.log('\nT1 happy path');
  {
    const { order, authority } = await newPending(5000);
    await finish(authority, 'ok');
    const { body: p } = await j(`/api/payments/${authority}`);
    ok('status = paid', p.status === 'paid', p.status);
    ok('ref_id present', !!p.ref_id);
    ok('card_pan masked', /\*/.test(p.card_pan || ''), p.card_pan);
    ok('order fulfilled once', store.getOrder(order.id).fulfilledCount === 1);
  }

  console.log('\nT2 user cancels');
  {
    const { authority } = await newPending();
    await finish(authority, 'cancel');
    const { body: p } = await j(`/api/payments/${authority}`);
    ok('status = canceled', p.status === 'canceled', p.status);
    ok('no ref_id', !p.ref_id);
  }

  console.log('\nT3 bank failure');
  {
    const { authority } = await newPending();
    await finish(authority, 'fail');
    const { body: p } = await j(`/api/payments/${authority}`);
    ok('status = canceled (Status=NOK)', p.status === 'canceled', p.status);
  }

  console.log('\nT4 double callback / refresh -> idempotent');
  {
    const { order, authority } = await newPending(7000);
    await finish(authority, 'ok');
    // simulate the user refreshing the callback page 3 more times
    for (let i = 0; i < 3; i++) {
      await fetch(`${BASE}/api/payments/callback?Authority=${authority}&Status=OK`);
    }
    const { body: p } = await j(`/api/payments/${authority}`);
    ok('still paid', p.status === 'paid');
    ok('fulfilled exactly once', store.getOrder(order.id).fulfilledCount === 1,
       `count=${store.getOrder(order.id).fulfilledCount}`);
  }

  console.log('\nT5 tampered / unknown authority');
  {
    const r = await fetch(`${BASE}/api/payments/callback?Authority=A_does_not_exist&Status=OK`);
    ok('404 on unknown authority', r.status === 404, r.status);
  }

  console.log('\nT6 amount mismatch -> -50');
  {
    const { authority } = await newPending(5000);
    await fetch(`${BASE}/__mock/pg/finish/${authority}/ok`, { redirect: 'manual' });
    const r = await fetch(`${BASE}/__mock/pg/v4/payment/verify.json`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ merchant_id: process.env.ZARINPAL_MERCHANT_ID, authority, amount: 999999 }),
    });
    const b = await r.json();
    ok('gateway returns -50', b.errors?.code === -50, JSON.stringify(b));
  }

  console.log('\nT7 amount below minimum rejected locally');
  {
    const { body: order } = await post('/api/orders', { amount: 100 });
    const { status, body } = await post('/api/payments/checkout', { orderId: order.id });
    ok('checkout rejected', status === 502 && String(body.code).includes('LOCAL_MIN'),
       `${status} ${JSON.stringify(body)}`);
  }

  console.log('\nT8 reconciliation of abandoned payment');
  {
    const { order, authority } = await newPending(3000);
    // user paid at the bank but never came back to our site
    await fetch(`${BASE}/__mock/pg/finish/${authority}/ok`, { redirect: 'manual' });
    // age the row past the 20-minute threshold
    store.updatePayment(authority, { created_at: new Date(Date.now() - 60 * 60 * 1000).toISOString() });
    const { body } = await post('/api/payments/reconcile');
    ok('reconcile picked it up', body.results.some((r) => r.authority === authority && r.result === 'paid'),
       JSON.stringify(body.results));
    ok('order fulfilled once', store.getOrder(order.id).fulfilledCount === 1);
  }

  console.log('\nT9 verify repeat returns 101 (not a second success)');
  {
    const { authority } = await newPending(4000);
    await fetch(`${BASE}/__mock/pg/finish/${authority}/ok`, { redirect: 'manual' });
    const call = () => fetch(`${BASE}/__mock/pg/v4/payment/verify.json`, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ merchant_id: process.env.ZARINPAL_MERCHANT_ID, authority, amount: 4000 }),
    }).then((r) => r.json());
    const first = await call(); const second = await call();
    ok('first = 100', first.data.code === 100, first.data.code);
    ok('second = 101', second.data.code === 101, second.data.code);
    ok('same ref_id', first.data.ref_id === second.data.ref_id);
  }

  console.log(`\n${passed} passed, ${failed} failed\n`);
  process.exit(failed ? 1 : 0);
}

run();
