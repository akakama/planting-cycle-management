-- 更新plot表结构，添加经纬度和编码字段

-- 添加code字段（如果不存在）
ALTER TABLE plot ADD COLUMN IF NOT EXISTS code VARCHAR(50);

-- 添加longitude字段（如果不存在）
ALTER TABLE plot ADD COLUMN IF NOT EXISTS longitude DECIMAL(10,6);

-- 添加latitude字段（如果不存在）
ALTER TABLE plot ADD COLUMN IF NOT EXISTS latitude DECIMAL(10,6);

-- 添加remark字段（如果不存在）
ALTER TABLE plot ADD COLUMN IF NOT EXISTS remark VARCHAR(500);

-- 更新现有数据的经纬度（根据位置推算）
UPDATE plot SET 
    code = CASE 
        WHEN location = '农场东区' AND name = '东区1号田' THEN 'PLOT-E001'
        WHEN location = '农场东区' AND name = '东区2号田' THEN 'PLOT-E002'
        WHEN location = '农场西区' AND name = '西区1号田' THEN 'PLOT-W001'
        WHEN location = '农场西区' AND name = '西区2号田' THEN 'PLOT-W002'
        WHEN location = '农场南区' AND name = '南区1号田' THEN 'PLOT-S001'
        ELSE CONCAT('PLOT-', id)
    END,
    longitude = CASE 
        WHEN location = '农场东区' THEN 125.0150 + (id * 0.005)
        WHEN location = '农场西区' THEN 124.9850 - (id * 0.005)
        WHEN location = '农场南区' THEN 125.0000
        ELSE 125.0000
    END,
    latitude = CASE 
        WHEN location = '农场东区' THEN 45.0080 - (id * 0.003)
        WHEN location = '农场西区' THEN 45.0100 - (id * 0.005)
        WHEN location = '农场南区' THEN 44.9920
        ELSE 45.0000
    END,
    remark = CASE 
        WHEN location = '农场东区' THEN '东区核心地块'
        WHEN location = '农场西区' THEN '西区核心地块'
        WHEN location = '农场南区' THEN '南区核心地块'
        ELSE '标准地块'
    END
WHERE longitude IS NULL OR latitude IS NULL;
