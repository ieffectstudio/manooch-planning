import { config } from './config.js';

export class ZarinpalError extends Error {
  constructor(code, message, raw) {
    super(message || `ZarinPal error ${code}`);
    this.name = 'ZarinpalError';
    this.code = code;
    this.raw = raw;
  }
}

// Codes that mean "our setup is broken / something suspicious" -> page ops.
export const ALERT_CODES = new Set([-10, -11, -14, -15, -16, -17, -19, -50, -53]);

export const ERROR_FA = {
  '-9': 'خطای اعتبارسنجی اطلاعات ارسالی',
  '-10': 'مرچنت کد یا آی‌پی پذیرنده معتبر نیست',
  '-11': 'درگاه فعال نیست',
  '-12': 'تلاش بیش از حد مجاز، کمی بعد دوباره امتحان کنید',
  '-13': 'محدودیت تراکنش درگاه',
  '-14': 'آدرس بازگشت با دامنه ثبت‌شده مغایرت دارد',
  '-15': 'درگاه تعلیق شده است',
  '-16': 'سطح تایید پذیرنده کافی نیست',
  '-17': 'محدودیت پذیرنده در سطح آبی',
  '-19': 'امکان ایجاد تراکنش برای این درگاه وجود ندارد',
  '-41': 'حداکثر مبلغ پرداختی ۱۰۰ میلیون تومان است',
  '-50': 'مبلغ پرداخت‌شده با مبلغ ارسالی مغایرت دارد',
  '-51': 'پرداخت ناموفق بود',
  '-52': 'خطای غیرمنتظره، با پشتیبانی تماس بگیرید',
  '-53': 'این پرداخت متعلق به این پذیرنده نیست',
  '-54': 'شناسه مرجع (authority) نامعتبر است',
  '100': 'عملیات موفق',
  '101': 'تراکنش قبلاً تایید شده است',
};

async function post(path, body) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), config.requestTimeoutMs);
  let res;
  try {
    res = await fetch(`${config.baseUrl}${path}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json', accept: 'application/json' },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
  } catch (err) {
    throw new ZarinpalError('NETWORK', `network error calling ${path}: ${err.message}`);
  } finally {
    clearTimeout(timer);
  }

  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new ZarinpalError('BAD_RESPONSE', `non-JSON response (${res.status}): ${text.slice(0, 200)}`);
  }

  // ZarinPal returns errors either as an object or an empty array.
  const errors = json.errors;
  const hasError = errors && !Array.isArray(errors) && errors.code !== undefined;
  if (hasError) {
    throw new ZarinpalError(errors.code, ERROR_FA[String(errors.code)] || errors.message, json);
  }
  if (!json.data || json.data.code === undefined) {
    throw new ZarinpalError('BAD_RESPONSE', 'missing data.code in response', json);
  }
  return json.data;
}

/**
 * Step 1 — create a payment. Returns { authority, startPayUrl, fee, feeType }.
 */
export async function createPayment({ amount, description, mobile, email, orderId }) {
  if (!Number.isInteger(amount)) throw new Error('amount must be an integer');
  if (amount < config.minAmount) {
    throw new ZarinpalError('LOCAL_MIN', `amount below minimum ${config.minAmount} ${config.currency}`);
  }
  if (amount > config.maxAmount) {
    throw new ZarinpalError('LOCAL_MAX', `amount above maximum ${config.maxAmount} ${config.currency}`);
  }
  if (!description) throw new Error('description is required');

  const metadata = {};
  if (mobile) metadata.mobile = mobile;
  if (email) metadata.email = email;
  if (orderId) metadata.order_id = String(orderId);

  const data = await post('/v4/payment/request.json', {
    merchant_id: config.merchantId,
    amount,
    currency: config.currency,
    description: description.slice(0, 500),
    callback_url: config.callbackUrl,
    metadata,
  });

  if (data.code !== 100) {
    throw new ZarinpalError(data.code, ERROR_FA[String(data.code)] || data.message, data);
  }
  return {
    authority: data.authority,
    startPayUrl: `${config.baseUrl}/StartPay/${data.authority}`,
    fee: data.fee,
    feeType: data.fee_type,
  };
}

/**
 * Step 2 — verify. Safe to retry: repeats return code 101.
 * Returns { code, alreadyVerified, refId, cardPan, cardHash, fee, feeType }.
 */
export async function verifyPayment({ authority, amount }) {
  let lastErr;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const data = await post('/v4/payment/verify.json', {
        merchant_id: config.merchantId,
        amount,
        authority,
      });
      if (data.code !== 100 && data.code !== 101) {
        throw new ZarinpalError(data.code, ERROR_FA[String(data.code)] || data.message, data);
      }
      return {
        code: data.code,
        alreadyVerified: data.code === 101,
        refId: String(data.ref_id ?? ''),
        cardPan: data.card_pan ?? null,
        cardHash: data.card_hash ?? null,
        fee: data.fee ?? null,
        feeType: data.fee_type ?? null,
      };
    } catch (err) {
      lastErr = err;
      // Only retry transient failures; business errors are final.
      const transient = err.code === 'NETWORK' || err.code === 'BAD_RESPONSE' || err.code === -12;
      if (!transient || attempt === 3) throw err;
      await new Promise((r) => setTimeout(r, 500 * 2 ** (attempt - 1)));
    }
  }
  throw lastErr;
}
