--
-- Estructura BD
--

-- Crear la taula categories
CREATE TABLE categories (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	slug TEXT UNIQUE
);

-- Crear la taula users
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	email TEXT UNIQUE,
	password TEXT,
	role TEXT,
	created DATETIME NOT NULL DEFAULT (DATETIME('now')),
	updated DATETIME NOT NULL DEFAULT (DATETIME('now'))

);

-- Crear la taula products
CREATE TABLE products (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT,
	description TEXT,
	photo TEXT,
	price DECIMAL(10, 2),
	category_id INTEGER,
	seller_id INTEGER,
	created DATETIME NOT NULL DEFAULT (DATETIME('now')),
	updated DATETIME NOT NULL DEFAULT (DATETIME('now')),
	FOREIGN KEY (category_id) REFERENCES categories(id),
	FOREIGN KEY (seller_id) REFERENCES users(id)
);

-- Crear la taula orders
CREATE TABLE orders (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	product_id INTEGER,
	buyer_id INTEGER,
	created DATETIME NOT NULL DEFAULT (DATETIME('now')),
	CONSTRAINT uc_product_buyer UNIQUE (product_id, buyer_id),
	FOREIGN KEY (product_id) REFERENCES products(id),
	FOREIGN KEY (buyer_id) REFERENCES users(id)
);

-- Crear la taula confirmed_orders
CREATE TABLE confirmed_orders (
	order_id INTEGER PRIMARY KEY,
	created DATETIME NOT NULL DEFAULT (DATETIME('now')),
	FOREIGN KEY (order_id) REFERENCES orders(id)
);


CREATE TABLE blocked_user (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    blocked_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id)
);
CREATE TABLE banned_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reason TEXT,
    created DATETIME NOT NULL DEFAULT (DATETIME('now')),
    product_id INTEGER REFERENCES products(id)
);
