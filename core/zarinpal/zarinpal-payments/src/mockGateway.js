/**
 * Local dummy gateway: mimics ZarinPal's v4 API well enough to test the whole
 * flow offline, including the error codes that matter (-50, -51, -54, 101).
 * Mounted at /__mock/pg and only enabled when ZARINPAL_MODE=dummy.
 */
import express from 'express';
import crypto from 'node:crypto';

const sessions = new Map(); // authority -> session

export function mockGateway(appUrl) {
  const r = express.Router();
  r.use(express.json());

  r.post('/v4/payment/request.json', (req, res) => {
    const { merchant_id, amount, callback_url, description } = req.body || {};
    if (!merchant_id || merchant_id.length !== 36) {
      return res.json({ data: [], errors: { code: -10, message: 'Terminal is not valid' } });
    }
    if (!amount || !callback_url || !description) {
      return res.json({ data: [], errors: { code: -9, message: 'Validation error' } });
    }
    const authority = 'A' + crypto.randomBytes(18).toString('hex').slice(0, 35);
    sessions.set(authority, {
      authority,
      amount,
      callback_url,
      status: 'created',
      verified: false,
      ref_id: null,
    });
    res.json({
      data: { code: 100, message: 'Success', authority, fee_type: 'Merchant', fee: 0 },
      errors: [],
    });
  });

  // Fake bank page with explicit outcome buttons.
  r.get('/StartPay/:authority', (req, res) => {
    const s = sessions.get(req.params.authority);
    if (!s) return res.status(404).send('Invalid authority');
    const a = s.authority;
    res.type('html').send(`<!doctype html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8">
<title>درگاه آزمایشی</title>
<style>
 body{font-family:system-ui,sans-serif;background:#0f172a;color:#e2e8f0;display:grid;
      place-items:center;height:100vh;margin:0}
 .card{background:#1e293b;padding:2rem;border-radius:16px;width:340px;text-align:center;
       box-shadow:0 10px 40px #0006}
 h1{font-size:1.1rem;margin:0 0 .25rem} .amt{font-size:1.8rem;font-weight:700;margin:.5rem 0 1.5rem}
 a{display:block;padding:.8rem;border-radius:10px;margin:.5rem 0;text-decoration:none;font-weight:600}
 .ok{background:#22c55e;color:#04120a}.fail{background:#ef4444;color:#fff}.cancel{background:#475569;color:#e2e8f0}
 code{font-size:.7rem;color:#94a3b8;word-break:break-all}
</style></head><body><div class="card">
 <h1>درگاه پرداخت آزمایشی (DUMMY)</h1>
 <div class="amt">${Number(s.amount).toLocaleString('fa-IR')}</div>
 <a class="ok"     href="/__mock/pg/finish/${a}/ok">پرداخت موفق</a>
 <a class="fail"   href="/__mock/pg/finish/${a}/fail">پرداخت ناموفق</a>
 <a class="cancel" href="/__mock/pg/finish/${a}/cancel">انصراف</a>
 <p><code>${a}</code></p>
</div></body></html>`);
  });

  r.get('/finish/:authority/:outcome', (req, res) => {
    const s = sessions.get(req.params.authority);
    if (!s) return res.status(404).send('Invalid authority');
    const { outcome } = req.params;
    s.status = outcome === 'ok' ? 'paid' : outcome === 'fail' ? 'failed' : 'canceled';
    const status = outcome === 'ok' ? 'OK' : 'NOK';
    const url = new URL(s.callback_url);
    url.searchParams.set('Authority', s.authority);
    url.searchParams.set('Status', status);
    res.redirect(url.toString());
  });

  r.post('/v4/payment/verify.json', (req, res) => {
    const { authority, amount } = req.body || {};
    const s = sessions.get(authority);
    if (!s) return res.json({ data: [], errors: { code: -54, message: 'Invalid authority' } });
    if (Number(amount) !== Number(s.amount)) {
      return res.json({ data: [], errors: { code: -50, message: 'amounts values is not the same' } });
    }
    if (s.status !== 'paid') {
      return res.json({ data: [], errors: { code: -51, message: 'session is not active paid try' } });
    }
    const first = !s.verified;
    if (first) {
      s.verified = true;
      s.ref_id = Math.floor(1e8 + Math.random() * 9e8);
    }
    res.json({
      data: {
        code: first ? 100 : 101,
        message: first ? 'Verified' : 'Verified',
        card_hash: 'MOCKHASH' + '0'.repeat(56),
        card_pan: '502229******5995',
        ref_id: s.ref_id,
        fee_type: 'Merchant',
        fee: 0,
      },
      errors: [],
    });
  });

  return r;
}
