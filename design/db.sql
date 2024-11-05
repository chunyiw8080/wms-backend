-- 创建 provider 表
CREATE TABLE provider (
    provider_name CHAR(30) NOT NULL,
    PRIMARY KEY (provider_name)
);

-- 创建 project 表
CREATE TABLE project (
    project_name CHAR(30) NOT NULL,
    PRIMARY KEY (project_name)
);

-- 创建 inventory 表
CREATE TABLE inventory (
    cargo_id CHAR(20) NOT NULL,
    cargo_name CHAR(15) NOT NULL,
    model CHAR(15) NOT NULL,
    categories CHAR(10) NOT NULL,
    count INT NOT NULL,
    price DECIMAL NOT NULL,
    PRIMARY KEY (cargo_id)
);

-- 创建 employee 表
CREATE TABLE employee (
    employee_id CHAR(20) NOT NULL,
    employee_name CHAR(15) NOT NULL,
    gender CHAR(1) NOT NULL DEFAULT '1',
    position CHAR(10) NOT NULL,
    PRIMARY KEY (employee_id)
);

-- 创建 user 表
CREATE TABLE user (
    user_id CHAR(20) NOT NULL,
    username CHAR(10) NOT NULL,
    password CHAR(30) NOT NULL,
    employee_id CHAR(20) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN NOT NULL DEFAULT TRUE,
    privilege CHAR(1) NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- 创建 orders 表
CREATE TABLE orders (
    order_id CHAR(12) NOT NULL,
    order_type CHAR(8) NOT NULL,
    cargo_id CHAR(20) NOT NULL,
    cargo_name CHAR(15) NOT NULL,
    model CHAR(15) NOT NULL,
    price DECIMAL NOT NULL,
    provider CHAR(30),
    project CHAR(30),
    status CHAR(7) NOT NULL,
    employee_id CHAR(20) NOT NULL,
    published_at DATE NOT NULL,
    processed_at DATE NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (cargo_id) REFERENCES inventory(cargo_id),
    FOREIGN KEY (provider) REFERENCES provider(provider_name),
    FOREIGN KEY (project) REFERENCES project(project_name),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

