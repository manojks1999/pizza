-- Local database definition.

DROP DATABASE IF EXISTS local_db;

CREATE DATABASE local_db;

USE local_db;

DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;

CREATE TABLE items (
    id VARCHAR(255) DEFAULT (uuid()) NOT NULL PRIMARY KEY,
    name VARCHAR(255),
    price INT,
    category VARCHAR(50)
);

CREATE TABLE orders (
    id VARCHAR(255) DEFAULT (uuid()) NOT NULL PRIMARY KEY,
    quantity INT,
    total_price FLOAT,
    item JSON,
    ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(255) DEFAULT 'Placed'
);

INSERT INTO items (name, price, category) VALUES ('Thin Crust', 500, 'base');
INSERT INTO items (name, price, category) VALUES ('Normal', 400, 'base');
INSERT INTO items (name, price, category) VALUES ('Cheese Burst', 200, 'base');



-- Insert the first topping
INSERT INTO items (name, price, category) VALUES ('Marinara sauce', 20, 'topping');

-- Insert the second topping
INSERT INTO items (name, price, category) VALUES ('Chicken breast', 30, 'topping');

-- Insert the third topping
INSERT INTO items (name, price, category) VALUES ('Green peppers', 15, 'topping');

-- Insert the fourth topping
INSERT INTO items (name, price, category) VALUES ('Black olives', 45, 'topping');

-- Insert the fifth topping
INSERT INTO items (name, price, category) VALUES ('Spinach', 20, 'topping');

-- Insert the sixth topping
INSERT INTO items (name, price, category) VALUES ('Mushrooms', 15, 'topping');

-- Insert the seventh topping
INSERT INTO items (name, price, category) VALUES ('Onions', 10, 'topping');




-- Insert the first cheese item
INSERT INTO items (name, price, category) VALUES ('Mozzarella Cheese', 20, 'cheese');

-- Insert the second cheese item
INSERT INTO items (name, price, category) VALUES ('Provolone Cheese', 30, 'cheese');

-- Insert the third cheese item
INSERT INTO items (name, price, category) VALUES ('Cheddar Cheese', 15, 'cheese');

-- Insert the fourth cheese item
INSERT INTO items (name, price, category) VALUES ('Gouda', 45, 'cheese');
