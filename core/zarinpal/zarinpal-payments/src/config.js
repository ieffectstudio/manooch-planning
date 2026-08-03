import 'dotenv/config';

const MODES = {
  dummy: null, // resolved at runtime to http://localhost:PORT/__mock/pg
  sandbox: 'https://sandbox.zarinpal.com/pg',
  production: 'https://payment.zarinpal.com/pg',
};

const mode = process.env.ZARINPAL_MODE || 'dummy';
if (!(mode in MODES)) {
  throw new Error(
    `ZARINPAL_MODE must be one of: ${Object.keys(MODES).join(', ')} (got "${mode}")`
  );
}

const port = Number(process.env.PORT || 3000);
const appUrl = (process.env.APP_URL || `http://localhost:${port}`).replace(/\/$/, '');
const merchantId = process.env.ZARINPAL_MERCHANT_ID || '';
const currency = (process.env.ZARINPAL_CURRENCY || 'IRT').toUpperCase();

if (!['IRR', 'IRT'].includes(currency)) {
  throw new Error('ZARINPAL_CURRENCY must be IRR or IRT');
}

// Boot-time guardrails: fail loudly instead of charging people wrongly.
if (mode === 'production') {
  const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  if (!uuid.test(merchantId)) {
    throw new Error('production mode requires a valid 36-char UUID ZARINPAL_MERCHANT_ID');
  }
  if (!appUrl.startsWith('https://')) {
    throw new Error('production mode requires an https APP_URL (callback domain must match the panel)');
  }
} else if (merchantId.length !== 36) {
  // sandbox / dummy accept any 36 characters
  console.warn(`[config] merchant_id is ${merchantId.length} chars; sandbox expects 36.`);
}

// ZarinPal minimums: 1,000 toman == 10,000 rial. Max 100,000,000 toman.
const minAmount = currency === 'IRT' ? 1_000 : 10_000;
const maxAmount = currency === 'IRT' ? 100_000_000 : 1_000_000_000;

export const config = {
  mode,
  port,
  appUrl,
  merchantId,
  currency,
  minAmount,
  maxAmount,
  baseUrl: mode === 'dummy' ? `http://localhost:${port}/__mock/pg` : MODES[mode],
  callbackUrl: `${appUrl}/api/payments/callback`,
  requestTimeoutMs: 15_000,
};

export function describeConfig() {
  return {
    mode: config.mode,
    baseUrl: config.baseUrl,
    currency: config.currency,
    callbackUrl: config.callbackUrl,
    merchantId: config.merchantId
      ? `${config.merchantId.slice(0, 8)}…${config.merchantId.slice(-4)}`
      : '(unset)',
  };
}
