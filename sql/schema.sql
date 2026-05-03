-- 种植周期管理系统 - 数据库建表脚本
-- MySQL 8.0, utf8mb4

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 1. 用户表
CREATE TABLE IF NOT EXISTS `user` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
  `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
  `password` VARCHAR(100) NOT NULL COMMENT '加密密码',
  `real_name` VARCHAR(50) COMMENT '真实姓名',
  `phone` VARCHAR(20) COMMENT '联系电话',
  `email` VARCHAR(100) COMMENT '邮箱',
  `role` ENUM('ADMIN', 'TECHNICIAN', 'FARMER', 'MANAGER') NOT NULL DEFAULT 'FARMER' COMMENT '角色',
  `avatar` VARCHAR(255) COMMENT '头像URL',
  `status` TINYINT DEFAULT 1 COMMENT '状态：0禁用 1启用',
  `last_login_time` DATETIME COMMENT '最后登录时间',
  `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_username` (`username`),
  INDEX `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 2. 作物信息表
CREATE TABLE IF NOT EXISTS `crop` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '作物ID',
  `name` VARCHAR(50) NOT NULL COMMENT '作物名称',
  `variety` VARCHAR(50) COMMENT '品种',
  `category` VARCHAR(50) COMMENT '作物类别',
  `growth_cycle_days` INT COMMENT '生长周期天数',
  `planting_season` VARCHAR(100) COMMENT '适宜种植季节',
  `description` TEXT COMMENT '描述信息',
  `image_url` VARCHAR(255) COMMENT '图片URL',
  `created_by` BIGINT COMMENT '创建人ID',
  `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_name` (`name`),
  INDEX `idx_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='作物信息表';

-- 3. 种植地块表
CREATE TABLE IF NOT EXISTS `plot` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '地块ID',
  `plot_code` VARCHAR(50) NOT NULL UNIQUE COMMENT '地块编号',
  `plot_name` VARCHAR(100) NOT NULL COMMENT '地块名称',
  `area` DECIMAL(10,2) COMMENT '面积(亩)',
  `soil_type` VARCHAR(50) COMMENT '土壤类型',
  `location` VARCHAR(255) COMMENT '地理位置',
  `longitude` DECIMAL(10,7) COMMENT '经度',
  `latitude` DECIMAL(10,7) COMMENT '纬度',
  `status` ENUM('IDLE', 'PLANTING', 'FALLOW') DEFAULT 'IDLE' COMMENT '状态',
  `responsible_person` VARCHAR(50) COMMENT '负责人',
  `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_plot_code` (`plot_code`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='种植地块表';

-- 4. 种植计划表
CREATE TABLE IF NOT EXISTS `planting_plan` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '计划ID',
  `plan_code` VARCHAR(50) NOT NULL UNIQUE COMMENT '计划编号',
  `plot_id` BIGINT NOT NULL COMMENT '地块ID',
  `crop_id` BIGINT NOT NULL COMMENT '作物ID',
  `plan_start_date` DATE NOT NULL COMMENT '计划开始日期',
  `plan_end_date` DATE COMMENT '计划结束日期',
  `actual_start_date` DATE COMMENT '实际开始日期',
  `actual_end_date` DATE COMMENT '实际结束日期',
  `expected_yield` DECIMAL(10,2) COMMENT '预期产量(kg)',
  `actual_yield` DECIMAL(10,2) COMMENT '实际产量(kg)',
  `status` ENUM('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED') DEFAULT 'PLANNED' COMMENT '状态',
  `remarks` VARCHAR(500) COMMENT '备注',
  `created_by` BIGINT COMMENT '创建人ID',
  `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  FOREIGN KEY (`plot_id`) REFERENCES `plot`(`id`),
  FOREIGN KEY (`crop_id`) REFERENCES `crop`(`id`),
  INDEX `idx_plan_code` (`plan_code`),
  INDEX `idx_status` (`status`),
  INDEX `idx_plan_date` (`plan_start_date`, `plan_end_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='种植计划表';

-- 5. 物候期记录表
CREATE TABLE IF NOT EXISTS `phenology_record` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
  `plan_id` BIGINT NOT NULL COMMENT '种植计划ID',
  `stage` VARCHAR(50) NOT NULL COMMENT '生育阶段',
  `start_date` DATE COMMENT '开始日期',
  `end_date` DATE COMMENT '结束日期',
  `description` VARCHAR(500) COMMENT '阶段描述',
  `image_urls` TEXT COMMENT '图片URL列表(JSON格式)',
  `notes` TEXT COMMENT '观察记录',
  `recorded_by` BIGINT COMMENT '记录人ID',
  `recorded_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  FOREIGN KEY (`plan_id`) REFERENCES `planting_plan`(`id`),
  INDEX `idx_plan_id` (`plan_id`),
  INDEX `idx_stage` (`stage`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='物候期记录表';

-- 6. 环境监测数据表
CREATE TABLE IF NOT EXISTS `environment_data` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '数据ID',
  `plot_id` BIGINT NOT NULL COMMENT '地块ID',
  `device_id` VARCHAR(50) COMMENT '设备ID',
  `temperature` DECIMAL(5,2) COMMENT '温度(℃)',
  `humidity` DECIMAL(5,2) COMMENT '湿度(%)',
  `soil_temperature` DECIMAL(5,2) COMMENT '土壤温度(℃)',
  `soil_moisture` DECIMAL(5,2) COMMENT '土壤湿度(%)',
  `light_intensity` DECIMAL(10,2) COMMENT '光照强度(lux)',
  `co2_concentration` DECIMAL(8,2) COMMENT 'CO2浓度(ppm)',
  `ph_value` DECIMAL(3,2) COMMENT 'pH值',
  `ec_value` DECIMAL(5,2) COMMENT 'EC值(ms/cm)',
  `record_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  FOREIGN KEY (`plot_id`) REFERENCES `plot`(`id`),
  INDEX `idx_plot_id` (`plot_id`),
  INDEX `idx_record_time` (`record_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='环境监测数据表';

-- 7. 农资信息表
CREATE TABLE IF NOT EXISTS `agricultural_material` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '农资ID',
  `material_code` VARCHAR(50) NOT NULL UNIQUE COMMENT '农资编号',
  `name` VARCHAR(100) NOT NULL COMMENT '农资名称',
  `category` ENUM('FERTILIZER', 'PESTICIDE', 'SEED', 'TOOL', 'OTHER') NOT NULL COMMENT '类别',
  `specification` VARCHAR(100) COMMENT '规格',
  `unit` VARCHAR(20) COMMENT '单位',
  `stock_quantity` DECIMAL(10,2) DEFAULT 0 COMMENT '库存数量',
  `min_stock_warning` DECIMAL(10,2) COMMENT '最低库存预警',
  `price` DECIMAL(10,2) COMMENT '单价(元)',
  `supplier` VARCHAR(100) COMMENT '供应商',
  `description` TEXT COMMENT '描述',
  `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_category` (`category`),
  INDEX `idx_stock` (`stock_quantity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='农资信息表';

-- 8. 农资使用记录表
CREATE TABLE IF NOT EXISTS `material_usage` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '使用记录ID',
  `plan_id` BIGINT NOT NULL COMMENT '种植计划ID',
  `material_id` BIGINT NOT NULL COMMENT '农资ID',
  `usage_quantity` DECIMAL(10,2) NOT NULL COMMENT '使用数量',
  `usage_date` DATE NOT NULL COMMENT '使用日期',
  `application_method` VARCHAR(100) COMMENT '施用方式',
  `operator` VARCHAR(50) COMMENT '操作人',
  `remarks` VARCHAR(500) COMMENT '备注',
  `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`plan_id`) REFERENCES `planting_plan`(`id`),
  FOREIGN KEY (`material_id`) REFERENCES `agricultural_material`(`id`),
  INDEX `idx_plan_id` (`plan_id`),
  INDEX `idx_material_id` (`material_id`),
  INDEX `idx_usage_date` (`usage_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='农资使用记录表';

-- 9. 采收记录表
CREATE TABLE IF NOT EXISTS `harvest_record` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '采收记录ID',
  `plan_id` BIGINT NOT NULL COMMENT '种植计划ID',
  `harvest_date` DATE NOT NULL COMMENT '采收日期',
  `quantity` DECIMAL(10,2) NOT NULL COMMENT '采收数量(kg)',
  `quality_grade` ENUM('A', 'B', 'C') COMMENT '品质等级',
  `batch_number` VARCHAR(50) COMMENT '批次号',
  `image_urls` TEXT COMMENT '图片URL',
  `remarks` VARCHAR(500) COMMENT '备注',
  `recorded_by` BIGINT COMMENT '记录人ID',
  `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`plan_id`) REFERENCES `planting_plan`(`id`),
  INDEX `idx_plan_id` (`plan_id`),
  INDEX `idx_harvest_date` (`harvest_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='采收记录表';

-- 10. 病虫害记录表
CREATE TABLE IF NOT EXISTS `pest_record` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
  `plan_id` BIGINT NOT NULL COMMENT '种植计划ID',
  `pest_type` VARCHAR(50) NOT NULL COMMENT '病虫害类型',
  `pest_name` VARCHAR(100) COMMENT '病虫害名称',
  `severity` ENUM('MILD', 'MODERATE', 'SEVERE') COMMENT '严重程度',
  `affected_area` DECIMAL(10,2) COMMENT '受影响面积',
  `symptoms` TEXT COMMENT '症状描述',
  `detection_method` VARCHAR(100) COMMENT '检测方式(人工/图像识别)',
  `image_urls` TEXT COMMENT '图片URL',
  `treatment_advice` TEXT COMMENT '处理建议',
  `is_resolved` TINYINT DEFAULT 0 COMMENT '是否解决',
  `resolved_time` DATETIME COMMENT '解决时间',
  `recorded_by` BIGINT COMMENT '记录人ID',
  `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  FOREIGN KEY (`plan_id`) REFERENCES `planting_plan`(`id`),
  INDEX `idx_plan_id` (`plan_id`),
  INDEX `idx_pest_type` (`pest_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='病虫害记录表';

-- 11. AI对话记录表
CREATE TABLE IF NOT EXISTS `ai_chat_record` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '对话ID',
  `user_id` BIGINT NOT NULL COMMENT '用户ID',
  `session_id` VARCHAR(100) NOT NULL COMMENT '会话ID',
  `question` TEXT NOT NULL COMMENT '用户问题',
  `answer` TEXT COMMENT 'AI回答',
  `context` TEXT COMMENT '上下文信息',
  `knowledge_retrieved` TEXT COMMENT '检索的知识片段',
  `tools_called` VARCHAR(500) COMMENT '调用的工具',
  `response_time_ms` INT COMMENT '响应时间(ms)',
  `feedback_score` TINYINT COMMENT '用户反馈评分(1-5)',
  `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_user_id` (`user_id`),
  INDEX `idx_session_id` (`session_id`),
  INDEX `idx_created_time` (`created_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI对话记录表';

-- 12. 产量预估记录表
CREATE TABLE IF NOT EXISTS `yield_prediction` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '预估ID',
  `plan_id` BIGINT NOT NULL COMMENT '种植计划ID',
  `prediction_date` DATE NOT NULL COMMENT '预估日期',
  `predicted_yield` DECIMAL(10,2) COMMENT '预估产量(kg)',
  `confidence_level` DECIMAL(3,2) COMMENT '置信度(0-1)',
  `prediction_model` VARCHAR(50) COMMENT '预估模型',
  `factors` TEXT COMMENT '影响因素(JSON)',
  `actual_yield` DECIMAL(10,2) COMMENT '实际产量(kg)',
  `error_rate` DECIMAL(5,2) COMMENT '误差率(%)',
  `created_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (`plan_id`) REFERENCES `planting_plan`(`id`),
  INDEX `idx_plan_id` (`plan_id`),
  INDEX `idx_prediction_date` (`prediction_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产量预估记录表';

SET FOREIGN_KEY_CHECKS = 1;
