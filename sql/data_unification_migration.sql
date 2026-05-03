-- 数据统一与接口一致性 - 数据库迁移脚本
-- 版本：v2.0.0
-- 日期：2025-06-18

-- ============================================================
-- 1. 种植计划表（planting_plan）
-- ============================================================

-- 添加缺失字段（如果不存在）
ALTER TABLE planting_plan 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE planting_plan 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- 修改status字段类型（如果需要）
-- ALTER TABLE planting_plan MODIFY COLUMN status INT DEFAULT 0 COMMENT '状态（0-草稿，1-已提交，2-已审核，3-进行中，4-已完成，5-已取消）';

-- ============================================================
-- 2. 物候期记录表（phenology_record）
-- ============================================================

-- 添加缺失字段
ALTER TABLE phenology_record 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE phenology_record 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- 添加物候期状态字段
ALTER TABLE phenology_record 
ADD COLUMN IF NOT EXISTS phenology_status INT DEFAULT 1 COMMENT '物候期状态（1-正常，2-异常，3-延迟，4-提前）';

-- 添加预期日期字段（用于对比计划日期和实际日期）
ALTER TABLE phenology_record 
ADD COLUMN IF NOT EXISTS expected_date DATE COMMENT '预期日期';

-- ============================================================
-- 3. 病虫害记录表（pest_record）
-- ============================================================

-- 添加缺失字段
ALTER TABLE pest_record 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE pest_record 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- 修改severity字段类型为INT（如果需要）
-- ALTER TABLE pest_record MODIFY COLUMN severity INT COMMENT '严重程度（1-低，2-中，3-高，4-严重）';

-- 添加预防措施字段
ALTER TABLE pest_record 
ADD COLUMN IF NOT EXISTS prevention_measures TEXT COMMENT '预防措施';

-- ============================================================
-- 4. 采收记录表（harvest_record）
-- ============================================================

-- 添加缺失字段
ALTER TABLE harvest_record 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE harvest_record 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- 修改qualityGrade字段类型为INT（如果需要）
-- ALTER TABLE harvest_record MODIFY COLUMN quality_grade INT COMMENT '质量等级（1-优，2-良，3-中，4-差）';

-- 添加采收人员字段
ALTER TABLE harvest_record 
ADD COLUMN IF NOT EXISTS harvester VARCHAR(50) COMMENT '采收人员';

-- 添加采收批次号字段
ALTER TABLE harvest_record 
ADD COLUMN IF NOT EXISTS batch_number VARCHAR(50) COMMENT '采收批次号';

-- 添加仓储位置字段
ALTER TABLE harvest_record 
ADD COLUMN IF NOT EXISTS storage_location VARCHAR(100) COMMENT '仓储位置';

-- ============================================================
-- 5. 农资使用记录表（material_usage）
-- ============================================================

-- 添加缺失字段
ALTER TABLE material_usage 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE material_usage 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- 添加单位字段
ALTER TABLE material_usage 
ADD COLUMN IF NOT EXISTS unit VARCHAR(20) COMMENT '单位（kg、升、袋等）';

-- 添加单价字段
ALTER TABLE material_usage 
ADD COLUMN IF NOT EXISTS unit_price DECIMAL(10, 2) COMMENT '单价（元）';

-- 添加总价字段
ALTER TABLE material_usage 
ADD COLUMN IF NOT EXISTS total_price DECIMAL(10, 2) COMMENT '总价（元）';

-- 添加推荐类型字段
ALTER TABLE material_usage 
ADD COLUMN IF NOT EXISTS recommend_type VARCHAR(20) DEFAULT 'manual' COMMENT '推荐类型（auto-自动推荐，manual-手动添加）';

-- ============================================================
-- 6. 作物表（crop）
-- ============================================================

-- 添加缺失字段（如果表存在）
ALTER TABLE crop 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE crop 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- ============================================================
-- 7. 地块表（plot）
-- ============================================================

-- 添加缺失字段（如果表存在）
ALTER TABLE plot 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE plot 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- ============================================================
-- 8. 农资表（agricultural_material）
-- ============================================================

-- 添加缺失字段（如果表存在）
ALTER TABLE agricultural_material 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE agricultural_material 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- ============================================================
-- 9. 产量预测表（yield_prediction）
-- ============================================================

-- 添加缺失字段（如果表存在）
ALTER TABLE yield_prediction 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE yield_prediction 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- ============================================================
-- 10. AI聊天记录表（ai_chat_record）
-- ============================================================

-- 添加缺失字段（如果表存在）
ALTER TABLE ai_chat_record 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE ai_chat_record 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- ============================================================
-- 11. 用户表（user）
-- ============================================================

-- 添加缺失字段（如果表存在）
ALTER TABLE user 
ADD COLUMN IF NOT EXISTS version INT DEFAULT 0 COMMENT '版本号（乐观锁）';

ALTER TABLE user 
ADD COLUMN IF NOT EXISTS tenant_id BIGINT DEFAULT 0 COMMENT '租户ID';

-- ============================================================
-- 索引优化
-- ============================================================

-- 为关联字段添加索引
CREATE INDEX IF NOT EXISTS idx_phenology_plan_id ON phenology_record(plan_id);
CREATE INDEX IF NOT EXISTS idx_pest_plan_id ON pest_record(plan_id);
CREATE INDEX IF NOT EXISTS idx_harvest_plan_id ON harvest_record(plan_id);
CREATE INDEX IF NOT EXISTS idx_material_plan_id ON material_usage(plan_id);
CREATE INDEX IF NOT EXISTS idx_material_material_id ON material_usage(material_id);
CREATE INDEX IF NOT EXISTS idx_yield_plan_id ON yield_prediction(plan_id);

-- 为状态字段添加索引
CREATE INDEX IF NOT EXISTS idx_plan_status ON planting_plan(status);
CREATE INDEX IF NOT EXISTS idx_phenology_status ON phenology_record(phenology_status);
CREATE INDEX IF NOT EXISTS idx_pest_severity ON pest_record(severity);
CREATE INDEX IF NOT EXISTS idx_harvest_quality ON harvest_record(quality_grade);

-- 为日期字段添加索引
CREATE INDEX IF NOT EXISTS idx_phenology_date ON phenology_record(phenology_date);
CREATE INDEX IF NOT EXISTS idx_pest_date ON pest_record(occurrence_date);
CREATE INDEX IF NOT EXISTS idx_harvest_date ON harvest_record(harvest_date);
CREATE INDEX IF NOT EXISTS idx_material_date ON material_usage(usage_date);

-- 为租户ID添加索引
CREATE INDEX IF NOT EXISTS idx_plan_tenant ON planting_plan(tenant_id);
CREATE INDEX IF NOT EXISTS idx_phenology_tenant ON phenology_record(tenant_id);
CREATE INDEX IF NOT EXISTS idx_pest_tenant ON pest_record(tenant_id);
CREATE INDEX IF NOT EXISTS idx_harvest_tenant ON harvest_record(tenant_id);
CREATE INDEX IF NOT EXISTS idx_material_tenant ON material_usage(tenant_id);
CREATE INDEX IF NOT EXISTS idx_yield_tenant ON yield_prediction(tenant_id);

-- ============================================================
-- 数据迁移
-- ============================================================

-- 更新现有数据的status字段（字符串转整数）
UPDATE planting_plan SET status = 0 WHERE status = '草稿' OR status IS NULL;
UPDATE planting_plan SET status = 1 WHERE status = '已提交';
UPDATE planting_plan SET status = 2 WHERE status = '已审核';
UPDATE planting_plan SET status = 3 WHERE status = '进行中';
UPDATE planting_plan SET status = 4 WHERE status = '已完成';
UPDATE planting_plan SET status = 5 WHERE status = '已取消';

-- 更新现有数据的severity字段（字符串转整数）
UPDATE pest_record SET severity = 1 WHERE severity = '低' OR severity IS NULL;
UPDATE pest_record SET severity = 2 WHERE severity = '中';
UPDATE pest_record SET severity = 3 WHERE severity = '高';
UPDATE pest_record SET severity = 4 WHERE severity = '严重';

-- 更新现有数据的qualityGrade字段（字符串转整数）
UPDATE harvest_record SET quality_grade = 1 WHERE quality_grade = '优' OR quality_grade IS NULL;
UPDATE harvest_record SET quality_grade = 2 WHERE quality_grade = '良';
UPDATE harvest_record SET quality_grade = 3 WHERE quality_grade = '中';
UPDATE harvest_record SET quality_grade = 4 WHERE quality_grade = '差';

-- 初始化version字段
UPDATE planting_plan SET version = 0 WHERE version IS NULL;
UPDATE phenology_record SET version = 0 WHERE version IS NULL;
UPDATE pest_record SET version = 0 WHERE version IS NULL;
UPDATE harvest_record SET version = 0 WHERE version IS NULL;
UPDATE material_usage SET version = 0 WHERE version IS NULL;
UPDATE crop SET version = 0 WHERE version IS NULL;
UPDATE plot SET version = 0 WHERE version IS NULL;
UPDATE agricultural_material SET version = 0 WHERE version IS NULL;
UPDATE yield_prediction SET version = 0 WHERE version IS NULL;
UPDATE ai_chat_record SET version = 0 WHERE version IS NULL;
UPDATE user SET version = 0 WHERE version IS NULL;

-- 初始化tenant_id字段
UPDATE planting_plan SET tenant_id = 0 WHERE tenant_id IS NULL;
UPDATE phenology_record SET tenant_id = 0 WHERE tenant_id IS NULL;
UPDATE pest_record SET tenant_id = 0 WHERE tenant_id IS NULL;
UPDATE harvest_record SET tenant_id = 0 WHERE tenant_id IS NULL;
UPDATE material_usage SET tenant_id = 0 WHERE tenant_id IS NULL;
UPDATE crop SET tenant_id = 0 WHERE tenant_id IS NULL;
UPDATE plot SET tenant_id = 0 WHERE tenant_id IS NULL;
UPDATE agricultural_material SET tenant_id = 0 WHERE tenant_id IS NULL;
UPDATE yield_prediction SET tenant_id = 0 WHERE tenant_id IS NULL;
UPDATE ai_chat_record SET tenant_id = 0 WHERE tenant_id IS NULL;
UPDATE user SET tenant_id = 0 WHERE tenant_id IS NULL;

-- 初始化phenology_status字段
UPDATE phenology_record SET phenology_status = 1 WHERE phenology_status IS NULL;

-- ============================================================
-- 完成
-- ============================================================

-- 显示迁移完成信息
SELECT '数据迁移完成！' AS message;
SELECT COUNT(*) AS total_plans FROM planting_plan;
SELECT COUNT(*) AS total_phenology FROM phenology_record;
SELECT COUNT(*) AS total_pests FROM pest_record;
SELECT COUNT(*) AS total_harvests FROM harvest_record;
SELECT COUNT(*) AS total_materials FROM material_usage;
