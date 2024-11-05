INSERT INTO provider (provider_name)
VALUES
('京东供应商'),
('天猫供应商'),
('苏宁供应商');

INSERT INTO project (project_name)
VALUES
('2024年仓库建设项目'),
('物流系统升级项目'),
('IT设备采购项目');

INSERT INTO orders (order_id, order_type, cargo_name, model, price, provider, project, status, employee_name, published_at, processed_at)
VALUES
('O001', 'inbound', '笔记本电脑', 'XPS13', 7000.00, '京东供应商', '2024年仓库建设项目', '已完成', '张三', '2024-04-01', '2024-04-02'),
('O002', 'outbound', '鼠标', 'MXMaster3', 500.00, '天猫供应商', '物流系统升级项目', '处理中', '李四', '2024-04-15', '2024-04-16'),
('O003', 'inbound', '键盘', 'K380', 300.00, '苏宁供应商', 'IT设备采购项目', '未处理', '王五', '2024-05-01', NULL);

INSERT INTO employee (employee_id, employee_name, gender, position)
VALUES
('E001', '张三', 'M', '仓库主管'),
('E002', '李四', 'F', '采购经理'),
('E003', '王五', 'M', '配送员');

INSERT INTO user (user_id, username, password, employee_name, created_at, status, privilege)
VALUES
('U001', 'zhangsan', 'password123', '张三', '2024-01-01', TRUE, 'A'),
('U002', 'lisi', 'password456', '李四', '2024-02-15', TRUE, 'B'),
('U003', 'wangwu', 'password789', '王五', '2024-03-10', FALSE, 'C');

INSERT INTO inventory (cargo_id, cargo_name, model, categories, count, price)
VALUES
('lapxps13', '笔记本电脑', 'XPS13', '电子产品', 50, 7000.00),
('micemxmaster3', '鼠标', 'MXMaster3', '外设', 100, 500.00),
('keyboardk380', '键盘', 'K380', '外设', 80, 300.00);
