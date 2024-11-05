-- 插入 employee 表测试数据
INSERT INTO employee (employee_id, employee_name, gender, position) VALUES
('E0001', 'Alice', 'F', 'Manager'),
('E0002', 'Bob', 'M', 'Engineer'),
('E0003', 'Charlie', 'M', 'Analyst'),
('E0004', 'Diana', 'F', 'Clerk'),
('E0005', 'Edward', 'M', 'Supervisor');

-- 插入 user 表测试数据
INSERT INTO user (user_id, username, password, employee_id, privilege) VALUES
('U0001', 'alice01', 'pass123', 'E0001', 'A'),
('U0002', 'bob02', 'pass234', 'E0002', 'B'),
('U0003', 'charlie03', 'pass345', 'E0003', 'B'),
('U0004', 'diana04', 'pass456', 'E0004', 'C'),
('U0005', 'edward05', 'pass567', 'E0005', 'C');

-- 插入 inventory 表测试数据
INSERT INTO inventory (cargo_id, cargo_name, model, categories, count, price) VALUES
('C0001', 'Laptop', 'Dell XPS 13', 'Electronics', 50, 1200.00),
('C0002', 'Mouse', 'Logitech M235', 'Electronics', 200, 25.00),
('C0003', 'Keyboard', 'HP K1500', 'Electronics', 150, 35.00),
('C0004', 'Monitor', 'Samsung S24', 'Electronics', 75, 200.00),
('C0005', 'Chair', 'ErgoChair 2', 'Furniture', 100, 150.00);

-- 插入 provider 表测试数据
INSERT INTO provider (provider_name) VALUES
('BestElectronics Inc.'),
('OfficeSupplies Ltd.'),
('TechGear Solutions'),
('HomeOffice Corp.'),
('ProFurniture');

-- 插入 project 表测试数据
INSERT INTO project (project_name) VALUES
('Project Alpha'),
('Project Beta'),
('Project Gamma'),
('Project Delta'),
('Project Omega');

-- 插入 orders 表测试数据
INSERT INTO orders (order_id, order_type, cargo_id, price, provider, project, status, employee_id, published_at, processed_at) VALUES
('O000000001', 'Purchase', 'C0001', 1200.00, 'BestElectronics Inc.', 'Project Alpha', 'Closed', 'E0001', '2024-01-10', '2024-01-15'),
('O000000002', 'Purchase', 'C0002', 25.00, 'TechGear Solutions', 'Project Beta', 'Open', 'E0002', '2024-02-20', '2024-02-25'),
('O000000003', 'Return', 'C0003', 35.00, 'OfficeSupplies Ltd.', 'Project Gamma', 'Closed', 'E0003', '2024-03-05', '2024-03-10'),
('O000000004', 'Purchase', 'C0004', 200.00, 'BestElectronics Inc.', 'Project Delta', 'Closed', 'E0004', '2024-04-15', '2024-04-20'),
('O000000005', 'Return', 'C0005', 150.00, 'ProFurniture', 'Project Omega', 'Open', 'E0005', '2024-05-01', '2024-05-05');

-- 插入 history 表测试数据
INSERT INTO history (id, year, month, cargo_name, model, categories, starting_price, starting_count, starting_total_price, closing_count, closing_price, closing_total_price) VALUES
('H0001', 2024, 1, 'Laptop', 'Dell XPS 13', 'Electronics', 1200.00, 50, 60000.00, 45, 1200.00, 54000.00),
('H0002', 2024, 2, 'Mouse', 'Logitech M235', 'Electronics', 25.00, 200, 5000.00, 180, 25.00, 4500.00),
('H0003', 2024, 3, 'Keyboard', 'HP K1500', 'Electronics', 35.00, 150, 5250.00, 130, 35.00, 4550.00),
('H0004', 2024, 4, 'Monitor', 'Samsung S24', 'Electronics', 200.00, 75, 15000.00, 70, 200.00, 14000.00),
('H0005', 2024, 5, 'Chair', 'ErgoChair 2', 'Furniture', 150.00, 100, 15000.00, 95, 150.00, 14250.00);
