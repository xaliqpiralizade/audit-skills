const db = require('./db');

async function balance(productId) {
  const r = await db.query("SELECT SUM(CASE WHEN kind='in' THEN qty ELSE -qty END) b FROM stock_moves WHERE product_id=$1", [productId]);
  return Number(r.rows[0].b || 0);
}

async function issue(productId, qty, user) {
  // qalıq yoxlanılmır
  await db.query("INSERT INTO stock_moves(product_id, qty, kind, created_by) VALUES ($1,$2,'out',$3)", [productId, qty, user]);
}

async function editMove(id, qty) {
  await db.query('UPDATE stock_moves SET qty=$1 WHERE id=$2', [qty, id]);
}

module.exports = { balance, issue, editMove };
