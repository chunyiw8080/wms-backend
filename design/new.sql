-- 创建 user 表
CREATE TABLE user (
    user_id CHAR(10) NOT NULL PRIMARY KEY,
    username CHAR(10) NOT NULL,
    password CHAR(30) NOT NULL,
    employee_id CHAR(10) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN NOT NULL DEFAULT TRUE,
    privilege CHAR(1) NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- 创建 employee 表
CREATE TABLE employee (
    employee_id CHAR(10) NOT NULL PRIMARY KEY,
    employee_name CHAR(15) NOT NULL,
    gender CHAR(1) NOT NULL DEFAULT '1',
    position CHAR(10) NOT NULL
);

-- 创建 inventory 表
CREATE TABLE inventory (
    cargo_id CHAR(20) NOT NULL PRIMARY KEY,
    cargo_name CHAR(15) NOT NULL,
    model CHAR(15) NOT NULL,
    categories CHAR(20) NOT NULL,
    count INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- 创建 orders 表
CREATE TABLE orders (
    order_id CHAR(12) NOT NULL PRIMARY KEY,
    order_type CHAR(8) NOT NULL,
    cargo_id CHAR(20) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    provider CHAR(30),
    project CHAR(30),
    status CHAR(7) NOT NULL,
    employee_id CHAR(10) NOT NULL,
    published_at DATE NOT NULL,
    processed_at DATE,
    FOREIGN KEY (cargo_id) REFERENCES inventory(cargo_id),
    FOREIGN KEY (provider) REFERENCES provider(provider_name),
    FOREIGN KEY (project) REFERENCES project(project_name),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- 创建 history 表
CREATE TABLE history (
    id CHAR(6) NOT NULL PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    cargo_name CHAR(15) NOT NULL,
    model CHAR(15) NOT NULL,
    categories CHAR(20) NOT NULL,
    starting_price DECIMAL(10, 2) NOT NULL,
    starting_count INT NOT NULL,
    starting_total_price DECIMAL(10, 2) NOT NULL,
    closing_count INT,
    closing_price DECIMAL(10, 2),
    closing_total_price DECIMAL(10, 2)
);

-- 创建 provider 表
CREATE TABLE provider (
    provider_name CHAR(30) NOT NULL PRIMARY KEY
);

-- 创建 project 表
CREATE TABLE project (
    project_name CHAR(30) NOT NULL PRIMARY KEY
);