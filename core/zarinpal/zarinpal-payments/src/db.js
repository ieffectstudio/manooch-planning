/**
 * Tiny JSON-file store standing in for your real database.
 * Swap for Postgres/Prisma; keep the same method signatures.
 *
 * The important bit is `markPaid()`: it is a compare-and-set on status,
 * which is what makes fulfilment idempotent under concurrent callbacks.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const FILE = path.join(process.cwd(), 'data', 'payments.json');

function load() {
  try {
    return JSON.parse(fs.readFileSync(FILE, 'utf8'));
  } catch {
    return { orders: {}, payments: {} };
  }
}
function save(db) {
  fs.mkdirSync(path.dirname(FILE), { recursive: true });
  fs.writeFileSync(FILE, JSON.stringify(db, null, 2));
}

let db = load();

export const store = {
  reset() {
    db = { orders: {}, payments: {} };
    save(db);
  },

  // --- orders (stand-in for your catalogue/cart) ---
  createOrder({ amount, title }) {
    const id = 'ord_' + crypto.randomBytes(6).toString('hex');
    db.orders[id] = { id, amount, title, status: 'unpaid', fulfilledCount: 0 };
    save(db);
    return db.orders[id];
  },
  getOrder(id) {
    return db.orders[id] || null;
  },

  // --- payments ---
  createPayment(row) {
    db.payments[row.authority] = row;
    save(db);
    return row;
  },
  getPayment(authority) {
    return db.payments[authority] || null;
  },
  updatePayment(authority, patch) {
    const p = db.payments[authority];
    if (!p) return null;
    Object.assign(p, patch);
    save(db);
    return p;
  },

  /**
   * Atomic-ish transition pending -> paid. Returns true only for the caller
   * that actually performed the transition (that caller fulfils the order).
   */
  markPaid(authority, patch) {
    const p = db.payments[authority];
    if (!p) return false;
    if (p.status === 'paid') {
      Object.assign(p, patch); // refresh ref_id etc, but don't re-fulfil
      save(db);
      return false;
    }
    Object.assign(p, patch, { status: 'paid', verified_at: new Date().toISOString() });
    const order = db.orders[p.order_id];
    if (order) {
      order.status = 'paid';
      order.fulfilledCount += 1;
    }
    save(db);
    return true;
  },

  stalePending(olderThanMs) {
    const cutoff = Date.now() - olderThanMs;
    return Object.values(db.payments).filter(
      (p) => p.status === 'pending' && new Date(p.created_at).getTime() < cutoff
    );
  },

  all() {
    return Object.values(db.payments);
  },
};
