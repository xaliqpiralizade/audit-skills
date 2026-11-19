CREATE TABLE products (id SERIAL PRIMARY KEY, sku TEXT, name TEXT, unit TEXT);
CREATE TABLE stock_moves (
  id SERIAL PRIMARY KEY, product_id INT, qty NUMERIC, kind TEXT, -- 'in' | 'out'
  created_at TIMESTAMP DEFAULT now(), created_by TEXT
);
