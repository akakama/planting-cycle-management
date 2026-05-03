-- 数据库迁移脚本
-- 功能：删除环境监测表，修改病虫害记录表结构
-- 日期：2025-03-29

-- ==================== 第1部分：删除环境监测表 ====================

-- 备份数据（可选，如果需要保留数据则取消注释）
-- CREATE TABLE environment_monitoring_backup AS SELECT * FROM environment_monitoring;

-- 删除环境监测表
DROP TABLE IF EXISTS environment_monitoring;

-- ==================== 第2部分：修改pest_record表结构 ====================

-- 新增AI识别相关字段到pest_record表
ALTER TABLE pest_record
ADD COLUMN confidence DECIMAL(5,2) NULL COMMENT 'AI识别置信度（0-100）',
ADD COLUMN prevention_advice TEXT NULL COMMENT '防治建议',
ADD COLUMN is_ai_identified TINYINT(1) DEFAULT 0 COMMENT '是否AI识别（0-否，1-是）',
ADD COLUMN identify_time DATETIME NULL COMMENT '识别时间';

-- 为识别时间字段添加索引，提升查询性能
CREATE INDEX idx_identify_time ON pest_record(identify_time);

-- 为AI识别标识字段添加索引
CREATE INDEX idx_is_ai_identified ON pest_record(is_ai_identified);
