CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  full_name TEXT NOT NULL,
  fin TEXT,
  phone TEXT,
  address TEXT,
  position TEXT,
  position_category TEXT,      -- 'worker' | 'specialist' | 'manager'
  department TEXT,
  salary REAL,
  health_notes TEXT,           -- xəstəlik vərəqələri, əlillik
  children_under_14 INTEGER DEFAULT 0,
  hire_date TEXT,
  termination_date TEXT
);
CREATE TABLE leaves (
  id INTEGER PRIMARY KEY,
  employee_id INTEGER REFERENCES employees(id),
  start_date TEXT,
  end_date TEXT,
  days INTEGER,
  type TEXT                     -- 'annual' | 'unpaid'
);
CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  employee_id INTEGER,
  kind TEXT,                    -- 'hire' | 'leave' | 'termination'
  body TEXT,
  created_at TEXT
);
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE,
  password_md5 TEXT,
  role TEXT                     -- 'admin' | 'hr' | 'employee'
);
