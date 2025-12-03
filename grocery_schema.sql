PRAGMA foreign_keys = ON;

CREATE TABLE manager (
    ID INTEGER PRIMARY KEY,
    name TEXT,
    salary INTEGER
);

CREATE TABLE department (
    name TEXT PRIMARY KEY,
    section TEXT UNIQUE,
    manager_ID INTEGER,
    FOREIGN KEY (manager_ID) REFERENCES manager(ID),
    CONSTRAINT CK_department_section CHECK (section GLOB '[A-Za-z]')
);

CREATE TABLE associate (
    ID INTEGER PRIMARY KEY,
    name TEXT,
    salary INTEGER,
    dept_name TEXT,
    FOREIGN KEY (dept_name) REFERENCES department(name)
);

CREATE TABLE aisle (
    ID TEXT UNIQUE,
    dept_name TEXT,
    FOREIGN KEY (dept_name) REFERENCES department(name),
    PRIMARY KEY (dept_name, ID)
);

CREATE TABLE product (
    ID INTEGER PRIMARY KEY,
    name TEXT,
    brand TEXT,
    price REAL,
    quantity_in_stock INTEGER,
    date_added TEXT,
    aisle_id TEXT,
    dept_name TEXT,
    FOREIGN KEY (aisle_id) REFERENCES aisle(ID),
    FOREIGN KEY (dept_name) REFERENCES department(name)
);

CREATE TABLE supplier (
    supplier_ID INTEGER PRIMARY KEY,
    name TEXT,
    phone_Number TEXT,
    dept_name TEXT,
    FOREIGN KEY (dept_name) REFERENCES department(name)
);

CREATE TABLE member (
    ID INTEGER PRIMARY KEY,
    name TEXT,
    points INTEGER,
    date_joined TEXT,
    email_address TEXT UNIQUE,
    password TEXT
);

CREATE TABLE works (
    associate_ID INTEGER PRIMARY KEY,
    dept_name TEXT,
    FOREIGN KEY (associate_ID) REFERENCES associate(ID),
    FOREIGN KEY (dept_name) REFERENCES department(name)
);

CREATE TABLE oversee (
    manager_ID INTEGER PRIMARY KEY,
    dept_name TEXT,
    FOREIGN KEY (manager_ID) REFERENCES manager(ID),
    FOREIGN KEY (dept_name) REFERENCES department(name)
);

CREATE TABLE product_aisle (
    product_ID INTEGER PRIMARY KEY,
    aisle_ID TEXT,
    dept_name TEXT,
    FOREIGN KEY (product_ID) REFERENCES product(ID),
    FOREIGN KEY (aisle_ID) REFERENCES aisle(ID),
    FOREIGN KEY (dept_name) REFERENCES department(name)
);

CREATE TABLE supplies (
    product_ID INTEGER PRIMARY KEY,
    supplier_ID INTEGER,
    FOREIGN KEY (product_ID) REFERENCES product(ID),
    FOREIGN KEY (supplier_ID) REFERENCES supplier(supplier_ID)
);

CREATE TABLE purchase (
    member_ID INTEGER,
    product_ID INTEGER,
    quantity INTEGER,
    date_purchased TEXT,
    FOREIGN KEY (product_ID) REFERENCES product(ID),
    FOREIGN KEY (member_ID) REFERENCES member(ID),
    PRIMARY KEY (member_ID, product_ID)
);
