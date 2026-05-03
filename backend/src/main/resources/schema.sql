-- 智能种植周期管理系统数据库初始化脚本 (H2数据库版本)

-- ============================================
-- 1. 用户相关表
-- ============================================

-- 用户表
CREATE TABLE IF NOT EXISTS sys_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    real_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    status TINYINT NOT NULL DEFAULT 1,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 角色表
CREATE TABLE IF NOT EXISTS sys_role (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    role_code VARCHAR(50) NOT NULL UNIQUE,
    role_name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 用户角色关联表
CREATE TABLE IF NOT EXISTS sys_user_role (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, role_id),
    deleted INT DEFAULT 0
);

-- 权限表
CREATE TABLE IF NOT EXISTS sys_permission (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    permission_code VARCHAR(100) NOT NULL UNIQUE,
    permission_name VARCHAR(50) NOT NULL,
    resource_type VARCHAR(20) NOT NULL,
    resource_url VARCHAR(200),
    parent_id BIGINT DEFAULT 0,
    sort_order INT DEFAULT 0,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 角色权限关联表
CREATE TABLE IF NOT EXISTS sys_role_permission (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- ============================================
-- 2. 业务数据表
-- ============================================

-- 作物表
CREATE TABLE IF NOT EXISTS crop (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    variety VARCHAR(100),
    growth_cycle INT,
    planting_requirements TEXT,
    phenology_definition VARCHAR(500),
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 地块表
CREATE TABLE IF NOT EXISTS plot (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50),
    name VARCHAR(100) NOT NULL,
    area DECIMAL(10,2),
    location VARCHAR(200),
    soil_type VARCHAR(50),
    longitude DECIMAL(10,6),
    latitude DECIMAL(10,6),
    remark VARCHAR(500),
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 种植计划表
CREATE TABLE IF NOT EXISTS planting_plan (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    crop_id BIGINT NOT NULL,
    plot_id BIGINT NOT NULL,
    planting_date DATE NOT NULL,
    expected_harvest_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'NOT_STARTED',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 物候期记录表
CREATE TABLE IF NOT EXISTS phenology_record (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    plan_id BIGINT NOT NULL,
    phenology_name VARCHAR(50) NOT NULL,
    record_date DATE NOT NULL,
    description TEXT,
    environmental_data VARCHAR(500),
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 病虫害记录表
CREATE TABLE IF NOT EXISTS pest_record (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    plan_id BIGINT NOT NULL,
    pest_name VARCHAR(100) NOT NULL,
    discovery_date DATE NOT NULL,
    severity VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    description TEXT,
    image_url VARCHAR(500),
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 农资表
CREATE TABLE IF NOT EXISTS material (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    specification VARCHAR(100),
    stock_quantity DECIMAL(10,2) NOT NULL DEFAULT 0,
    unit VARCHAR(20) NOT NULL,
    supplier VARCHAR(100),
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    version INT DEFAULT 0,
    deleted INT DEFAULT 0
);

-- 农资使用记录表
CREATE TABLE IF NOT EXISTS material_usage (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    material_id BIGINT NOT NULL,
    plan_id BIGINT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    usage_date DATE NOT NULL,
    purpose VARCHAR(200),
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 采收记录表
CREATE TABLE IF NOT EXISTS harvest_record (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    plan_id BIGINT NOT NULL,
    harvest_date DATE NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    quality_grade VARCHAR(20) NOT NULL,
    description TEXT,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 产量预估表
CREATE TABLE IF NOT EXISTS yield_prediction (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    plan_id BIGINT NOT NULL,
    prediction_date DATE NOT NULL,
    predicted_yield DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    prediction_method VARCHAR(50) NOT NULL,
    parameters VARCHAR(500),
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- 对话历史表
CREATE TABLE IF NOT EXISTS chat_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    conversation_id VARCHAR(100) NOT NULL,
    user_message TEXT NOT NULL,
    ai_reply TEXT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted INT DEFAULT 0
);

-- ============================================
-- 3. 插入默认数据
-- ============================================

INSERT INTO sys_user (username, password, real_name, status) VALUES
('admin', '$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG', '系统管理员', 1);

-- 插入默认角色
INSERT INTO sys_role (role_code, role_name, description) VALUES
('ADMIN', '管理员', '系统管理员,拥有所有权限'),
('FARM_MANAGER', '农场管理员', '农场管理员,负责农场管理'),
('TECHNICIAN', '农业技术人员', '农业技术人员,负责技术指导');

-- 插入默认权限
INSERT INTO sys_permission (permission_code, permission_name, resource_type, resource_url, parent_id, sort_order) VALUES
('user:view', '查看用户', 'API', '/api/users/*', 0, 1),
('user:create', '创建用户', 'API', '/api/users', 0, 2),
('crop:view', '查看作物', 'API', '/api/crops/*', 0, 11),
('crop:create', '创建作物', 'API', '/api/crops', 0, 12),
('crop:update', '更新作物', 'API', '/api/crops/*', 0, 13),
('crop:delete', '删除作物', 'API', '/api/crops/*', 0, 14),
('plan:view', '查看种植计划', 'API', '/api/planting-plans/*', 0, 21),
('plan:create', '创建种植计划', 'API', '/api/planting-plans', 0, 22),
('plan:update', '更新种植计划', 'API', '/api/planting-plans/*', 0, 23),
('plan:delete', '删除种植计划', 'API', '/api/planting-plans/*', 0, 24),
('plot:view', '查看地块', 'API', '/api/plots/*', 0, 31),
('plot:create', '创建地块', 'API', '/api/plots', 0, 32),
('plot:update', '更新地块', 'API', '/api/plots/*', 0, 33),
('phenology:view', '查看物候期记录', 'API', '/api/phenology-records/*', 0, 41),
('phenology:create', '创建物候期记录', 'API', '/api/phenology-records', 0, 42),
('phenology:update', '更新物候期记录', 'API', '/api/phenology-records/*', 0, 43),
('phenology:delete', '删除物候期记录', 'API', '/api/phenology-records/*', 0, 44),
('pest:view', '查看病虫害记录', 'API', '/api/pest-records/*', 0, 51),
('pest:create', '创建病虫害记录', 'API', '/api/pest-records', 0, 52),
('pest:update', '更新病虫害记录', 'API', '/api/pest-records/*', 0, 53),
('pest:delete', '删除病虫害记录', 'API', '/api/pest-records/*', 0, 54),
('pest:diagnose', '病虫害诊断', 'API', '/api/pest-records/diagnose', 0, 55),
('material:view', '查看农资', 'API', '/api/materials/*', 0, 61),
('material:create', '创建农资', 'API', '/api/materials', 0, 62),
('material:update', '更新农资', 'API', '/api/materials/*', 0, 63),
('material:stock-in', '农资入库', 'API', '/api/materials/*/stock-in', 0, 64),
('material:view-usage', '查看农资使用记录', 'API', '/api/material-usage', 0, 65),
('material:create-usage', '创建农资使用记录', 'API', '/api/material-usage', 0, 66),
('harvest:view', '查看采收记录', 'API', '/api/harvest-records/*', 0, 71),
('harvest:create', '创建采收记录', 'API', '/api/harvest-records', 0, 72),
('harvest:update', '更新采收记录', 'API', '/api/harvest-records/*', 0, 73),
('harvest:delete', '删除采收记录', 'API', '/api/harvest-records/*', 0, 74),
('yield:view', '查看产量预估', 'API', '/api/yield-predictions/*', 0, 81),
('yield:create', '创建产量预估', 'API', '/api/yield-predictions', 0, 82),
('yield:update', '更新产量预估', 'API', '/api/yield-predictions/*', 0, 83),
('yield:delete', '删除产量预估', 'API', '/api/yield-predictions/*', 0, 84),
('ai:chat', 'AI聊天', 'API', '/api/ai/chat', 0, 91),
('ai:history', '查看聊天历史', 'API', '/api/ai/history', 0, 92),
('ai:knowledge', '知识检索', 'API', '/api/ai/knowledge/search', 0, 93),
('ai:tools', '工具调用', 'API', '/api/ai/tools/*', 0, 94);

-- 为管理员角色分配所有权限
INSERT INTO sys_role_permission (role_id, permission_id)
SELECT 1, id FROM sys_permission;

-- 为管理员分配角色
INSERT INTO sys_user_role (user_id, role_id) VALUES (1, 1);

-- 插入默认作物数据
INSERT INTO crop (name, variety, growth_cycle, planting_requirements, phenology_definition) VALUES
('小麦', '济麦22', 220, '适宜在秋季播种,春季收获,需要充足的光照和水分', '播种期,出苗期,分蘖期,拔节期,抽穗期,开花期,灌浆期,成熟期'),
('水稻', '杂交水稻', 150, '适宜在水田种植,需要充足的灌溉,温度要求较高', '播种期,出苗期,分蘖期,拔节期,抽穗期,开花期,灌浆期,成熟期'),
('玉米', '郑单958', 120, '适宜在春季播种,秋季收获,需要充足的阳光和水分', '播种期,出苗期,拔节期,抽穗期,开花期,灌浆期,成熟期'),
('大豆', '黑农44', 120, '适宜在春季播种,秋季收获,对土壤要求不高', '播种期,出苗期,开花期,结荚期,鼓粒期,成熟期'),
('马铃薯', '费乌瑞它', 100, '适宜在春季或秋季播种,对土壤要求疏松', '播种期,出苗期,现蕾期,开花期,块茎膨大期,成熟期');

-- 插入默认地块数据（经纬度基于山东省德州市各县区的实际地理位置推算）
-- 平原县：东经116.5°，北纬37.0°
-- 禹城市：东经116.8°，北纬36.9°
-- 齐河县：东经116.8°，北纬36.8°
-- 乐陵市：东经117.2°，北纬37.7°
-- 宁津县：东经116.8°，北纬37.5°
-- 陵城区：东经116.6°，北纬37.3°
INSERT INTO plot (code, name, area, location, soil_type, longitude, latitude, remark) VALUES
('PLOT-001', '平原一号田', 8500, '山东省德州市平原县', '壤土', 116.5430, 37.0630, '平原县核心地块'),
('PLOT-002', '平原二号田', 7200, '山东省德州市平原县', '沙壤土', 116.5280, 37.0510, '平原县辅助地块'),
('PLOT-003', '平原三号田', 6800, '山东省德州市平原县', '黑土', 116.5120, 37.0380, '平原县试验田'),
('PLOT-004', '禹城一号田', 9200, '山东省德州市禹城市', '棕壤土', 116.8250, 36.9480, '禹城市核心地块'),
('PLOT-005', '禹城二号田', 5600, '山东省德州市禹城市', '黄褐土', 116.8420, 36.9320, '禹城市辅助地块'),
('PLOT-006', '齐河一号田', 7800, '山东省德州市齐河县', '潮土', 116.7950, 36.7850, '齐河县核心地块'),
('PLOT-007', '齐河二号田', 6400, '山东省德州市齐河县', '盐碱土', 116.8120, 36.7680, '齐河县辅助地块'),
('PLOT-008', '乐陵一号田', 5100, '山东省德州市乐陵市', '沙土', 117.2150, 37.7280, '乐陵市核心地块'),
('PLOT-009', '宁津一号田', 7300, '山东省德州市宁津县', '壤土', 116.8350, 37.5120, '宁津县核心地块'),
('PLOT-010', '陵城一号田', 8900, '山东省德州市陵城区', '黑土', 116.5750, 37.3250, '陵城区核心地块');

-- 插入默认农资数据
INSERT INTO material (name, type, specification, stock_quantity, unit, supplier) VALUES
('尿素', 'FERTILIZER', '46%含氮量', 1000.00, '千克', '化肥公司'),
('复合肥', 'FERTILIZER', 'NPK 15-15-15', 800.00, '千克', '化肥公司'),
('多菌灵', 'PESTICIDE', '50%可湿性粉剂', 200.00, '千克', '农药公司'),
('吡虫啉', 'PESTICIDE', '20%可湿性粉剂', 150.00, '千克', '农药公司'),
('小麦种子', 'SEED', '济麦22', 500.00, '千克', '种子公司'),
('水稻种子', 'SEED', '杂交水稻', 400.00, '千克', '种子公司');
