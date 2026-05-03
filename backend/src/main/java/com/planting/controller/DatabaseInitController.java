package com.planting.controller;

import com.planting.common.ApiResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 数据库初始化控制器
 */
@Slf4j
@RestController
@RequestMapping("/database")
public class DatabaseInitController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    /**
     * 更新plot表结构
     */
    @PostMapping("/update-plot-table")
    @PreAuthorize("hasAuthority('plot:write')")
    public ApiResponse<String> updatePlotTable() {
        try {
            // 检查并添加code字段
            try {
                jdbcTemplate.execute("ALTER TABLE plot ADD COLUMN code VARCHAR(50)");
                log.info("添加code字段成功");
            } catch (Exception e) {
                log.info("code字段已存在，跳过");
            }

            // 检查并添加longitude字段
            try {
                jdbcTemplate.execute("ALTER TABLE plot ADD COLUMN longitude DECIMAL(10,6)");
                log.info("添加longitude字段成功");
            } catch (Exception e) {
                log.info("longitude字段已存在，跳过");
            }

            // 检查并添加latitude字段
            try {
                jdbcTemplate.execute("ALTER TABLE plot ADD COLUMN latitude DECIMAL(10,6)");
                log.info("添加latitude字段成功");
            } catch (Exception e) {
                log.info("latitude字段已存在，跳过");
            }

            // 检查并添加remark字段
            try {
                jdbcTemplate.execute("ALTER TABLE plot ADD COLUMN remark VARCHAR(500)");
                log.info("添加remark字段成功");
            } catch (Exception e) {
                log.info("remark字段已存在，跳过");
            }

            // 更新现有数据的经纬度
            List<Map<String, Object>> plots = jdbcTemplate.queryForList("SELECT id, name, location FROM plot WHERE longitude IS NULL OR latitude IS NULL");
            
            for (Map<String, Object> plot : plots) {
                Long id = (Long) plot.get("id");
                String name = (String) plot.get("name");
                String location = (String) plot.get("location");
                
                String code;
                Double longitude;
                Double latitude;
                String remark;
                
                if ("农场东区".equals(location)) {
                    if ("东区1号田".equals(name)) {
                        code = "PLOT-E001";
                        longitude = 125.0150;
                        latitude = 45.0080;
                    } else {
                        code = "PLOT-E002";
                        longitude = 125.0200;
                        latitude = 45.0050;
                    }
                    remark = "东区核心地块";
                } else if ("农场西区".equals(location)) {
                    if ("西区1号田".equals(name)) {
                        code = "PLOT-W001";
                        longitude = 124.9850;
                        latitude = 45.0100;
                    } else {
                        code = "PLOT-W002";
                        longitude = 124.9800;
                        latitude = 45.0050;
                    }
                    remark = "西区核心地块";
                } else if ("农场南区".equals(location)) {
                    code = "PLOT-S001";
                    longitude = 125.0000;
                    latitude = 44.9920;
                    remark = "南区核心地块";
                } else {
                    code = "PLOT-" + id;
                    longitude = 125.0000;
                    latitude = 45.0000;
                    remark = "标准地块";
                }
                
                jdbcTemplate.update(
                    "UPDATE plot SET code = ?, longitude = ?, latitude = ?, remark = ? WHERE id = ?",
                    code, longitude, latitude, remark, id
                );
                log.info("更新地块 {} 的经纬度: {}, {}", name, longitude, latitude);
            }

            return ApiResponse.success("数据库表结构更新成功");
        } catch (Exception e) {
            log.error("更新数据库表结构失败", e);
            return ApiResponse.error("更新失败: " + e.getMessage());
        }
    }

    /**
     * 初始化所有缺失的表
     */
    @PostMapping("/init-tables")
    @PreAuthorize("hasAuthority('plot:write')")
    public ApiResponse<String> initTables() {
        try {
            // 创建pest_record表
            try {
                jdbcTemplate.execute(
                    "CREATE TABLE IF NOT EXISTS pest_record (" +
                    "id BIGINT AUTO_INCREMENT PRIMARY KEY, " +
                    "plan_id BIGINT NOT NULL, " +
                    "pest_name VARCHAR(100) NOT NULL, " +
                    "discovery_date DATE NOT NULL, " +
                    "severity VARCHAR(20) NOT NULL, " +
                    "status VARCHAR(20) NOT NULL DEFAULT 'PENDING', " +
                    "description TEXT, " +
                    "image_url VARCHAR(500), " +
                    "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
                    "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
                    "deleted INT DEFAULT 0)"
                );
                log.info("创建pest_record表成功");
            } catch (Exception e) {
                log.info("pest_record表已存在，跳过");
            }

            // 创建phenology_record表
            try {
                jdbcTemplate.execute(
                    "CREATE TABLE IF NOT EXISTS phenology_record (" +
                    "id BIGINT AUTO_INCREMENT PRIMARY KEY, " +
                    "plan_id BIGINT NOT NULL, " +
                    "phenology_name VARCHAR(50) NOT NULL, " +
                    "record_date DATE NOT NULL, " +
                    "description TEXT, " +
                    "environmental_data VARCHAR(500), " +
                    "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
                    "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
                    "deleted INT DEFAULT 0)"
                );
                log.info("创建phenology_record表成功");
            } catch (Exception e) {
                log.info("phenology_record表已存在，跳过");
            }

            // 创建harvest_record表
            try {
                jdbcTemplate.execute(
                    "CREATE TABLE IF NOT EXISTS harvest_record (" +
                    "id BIGINT AUTO_INCREMENT PRIMARY KEY, " +
                    "plan_id BIGINT NOT NULL, " +
                    "harvest_date DATE NOT NULL, " +
                    "quantity DECIMAL(10,2) NOT NULL, " +
                    "unit VARCHAR(20) NOT NULL, " +
                    "quality_grade VARCHAR(20) NOT NULL, " +
                    "description TEXT, " +
                    "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
                    "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
                    "deleted INT DEFAULT 0)"
                );
                log.info("创建harvest_record表成功");
            } catch (Exception e) {
                log.info("harvest_record表已存在，跳过");
            }

            // 确保harvest_record表有quantity字段
            try {
                jdbcTemplate.execute("ALTER TABLE harvest_record ADD COLUMN quantity DECIMAL(10,2)");
                log.info("添加harvest_record表的quantity字段成功");
            } catch (Exception e) {
                log.info("harvest_record表的quantity字段已存在，跳过");
            }

            // 确保harvest_record表有unit字段
            try {
                jdbcTemplate.execute("ALTER TABLE harvest_record ADD COLUMN unit VARCHAR(20)");
                log.info("添加harvest_record表的unit字段成功");
            } catch (Exception e) {
                log.info("harvest_record表的unit字段已存在，跳过");
            }

            // 确保harvest_record表有quality_grade字段
            try {
                jdbcTemplate.execute("ALTER TABLE harvest_record ADD COLUMN quality_grade VARCHAR(20)");
                log.info("添加harvest_record表的quality_grade字段成功");
            } catch (Exception e) {
                log.info("harvest_record表的quality_grade字段已存在，跳过");
            }

            // 确保harvest_record表有description字段
            try {
                jdbcTemplate.execute("ALTER TABLE harvest_record ADD COLUMN description TEXT");
                log.info("添加harvest_record表的description字段成功");
            } catch (Exception e) {
                log.info("harvest_record表的description字段已存在，跳过");
            }

            // 创建yield_prediction表
            try {
                jdbcTemplate.execute(
                    "CREATE TABLE IF NOT EXISTS yield_prediction (" +
                    "id BIGINT AUTO_INCREMENT PRIMARY KEY, " +
                    "plan_id BIGINT NOT NULL, " +
                    "prediction_date DATE NOT NULL, " +
                    "predicted_yield DECIMAL(10,2) NOT NULL, " +
                    "unit VARCHAR(20) NOT NULL, " +
                    "prediction_method VARCHAR(50) NOT NULL, " +
                    "parameters VARCHAR(500), " +
                    "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
                    "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
                    "deleted INT DEFAULT 0)"
                );
                log.info("创建yield_prediction表成功");
            } catch (Exception e) {
                log.info("yield_prediction表已存在，跳过");
            }

            // 确保yield_prediction表有unit字段
            try {
                jdbcTemplate.execute("ALTER TABLE yield_prediction ADD COLUMN unit VARCHAR(20)");
                log.info("添加yield_prediction表的unit字段成功");
            } catch (Exception e) {
                log.info("yield_prediction表的unit字段已存在，跳过");
            }

            // 确保yield_prediction表有prediction_method字段
            try {
                jdbcTemplate.execute("ALTER TABLE yield_prediction ADD COLUMN prediction_method VARCHAR(50)");
                log.info("添加yield_prediction表的prediction_method字段成功");
            } catch (Exception e) {
                log.info("yield_prediction表的prediction_method字段已存在，跳过");
            }

            // 确保yield_prediction表有parameters字段
            try {
                jdbcTemplate.execute("ALTER TABLE yield_prediction ADD COLUMN parameters VARCHAR(500)");
                log.info("添加yield_prediction表的parameters字段成功");
            } catch (Exception e) {
                log.info("yield_prediction表的parameters字段已存在，跳过");
            }

            // 创建material_usage表
            try {
                jdbcTemplate.execute(
                    "CREATE TABLE IF NOT EXISTS material_usage (" +
                    "id BIGINT AUTO_INCREMENT PRIMARY KEY, " +
                    "material_id BIGINT NOT NULL, " +
                    "plan_id BIGINT NOT NULL, " +
                    "quantity DECIMAL(10,2) NOT NULL, " +
                    "unit VARCHAR(20) NOT NULL, " +
                    "usage_date DATE NOT NULL, " +
                    "purpose VARCHAR(200), " +
                    "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
                    "deleted INT DEFAULT 0)"
                );
                log.info("创建material_usage表成功");
            } catch (Exception e) {
                log.info("material_usage表已存在，跳过");
            }

            // 创建chat_history表
            try {
                jdbcTemplate.execute(
                    "CREATE TABLE IF NOT EXISTS chat_history (" +
                    "id BIGINT AUTO_INCREMENT PRIMARY KEY, " +
                    "user_id BIGINT NOT NULL, " +
                    "conversation_id VARCHAR(100) NOT NULL, " +
                    "user_message TEXT NOT NULL, " +
                    "ai_reply TEXT, " +
                    "timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
                    "deleted INT DEFAULT 0)"
                );
                log.info("创建chat_history表成功");
            } catch (Exception e) {
                log.info("chat_history表已存在，跳过");
            }

            return ApiResponse.success("数据库表初始化成功");
        } catch (Exception e) {
            log.error("初始化数据库表失败", e);
            return ApiResponse.error("初始化失败: " + e.getMessage());
        }
    }

    /**
     * 导入初始数据
     */
    @PostMapping("/init-data")
    @PreAuthorize("hasAuthority('plot:write')")
    public ApiResponse<String> initData() {
        try {
            // 检查种植计划表是否为空
            Integer planCount = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM planting_plan WHERE deleted = 0", Integer.class);
            
            if (planCount != null && planCount == 0) {
                // 插入种植计划数据
                jdbcTemplate.execute(
                    "INSERT INTO planting_plan (crop_id, plot_id, planting_date, expected_harvest_date, status) VALUES " +
                    "(1, 1, '2026-03-15', '2026-10-15', 'IN_PROGRESS'), " +
                    "(2, 2, '2026-04-01', '2026-09-01', 'IN_PROGRESS'), " +
                    "(3, 3, '2026-04-20', '2026-08-20', 'NOT_STARTED'), " +
                    "(4, 4, '2026-05-01', '2026-09-15', 'NOT_STARTED'), " +
                    "(5, 5, '2026-05-10', '2026-08-20', 'NOT_STARTED')"
                );
                log.info("插入种植计划数据成功");
            }

            // 检查物候期记录表是否为空
            Integer phenologyCount = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM phenology_record WHERE deleted = 0", Integer.class);
            
            if (phenologyCount != null && phenologyCount == 0) {
                // 插入物候期记录数据
                jdbcTemplate.execute(
                    "INSERT INTO phenology_record (plan_id, phenology_name, record_date, description) VALUES " +
                    "(1, '播种期', '2026-03-15', '小麦播种完成，土壤湿度适宜'), " +
                    "(1, '出苗期', '2026-03-25', '小麦出苗整齐，苗情良好'), " +
                    "(1, '分蘖期', '2026-04-10', '小麦分蘖正常，每株3-4个分蘖'), " +
                    "(2, '播种期', '2026-04-01', '水稻播种完成，水田灌溉正常'), " +
                    "(2, '出苗期', '2026-04-12', '水稻出苗良好，苗高15cm')"
                );
                log.info("插入物候期记录数据成功");
            }

            // 检查病虫害记录表是否为空
            Integer pestCount = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM pest_record WHERE deleted = 0", Integer.class);
            
            if (pestCount != null && pestCount == 0) {
                // 插入病虫害记录数据
                jdbcTemplate.execute(
                    "INSERT INTO pest_record (plan_id, pest_name, discovery_date, severity, status, description) VALUES " +
                    "(1, '小麦锈病', '2026-04-05', 'MEDIUM', 'TREATED', '发现少量锈病斑点，已喷施多菌灵防治'), " +
                    "(2, '稻飞虱', '2026-04-15', 'LOW', 'PENDING', '发现少量稻飞虱，需密切观察')"
                );
                log.info("插入病虫害记录数据成功");
            }

            return ApiResponse.success("初始数据导入成功");
        } catch (Exception e) {
            log.error("导入初始数据失败", e);
            return ApiResponse.error("导入失败: " + e.getMessage());
        }
    }

    /**
     * 根据地理位置更新经纬度
     */
    @PostMapping("/update-coordinates")
    @PreAuthorize("hasAuthority('plot:write')")
    public ApiResponse<String> updateCoordinates() {
        try {
            // 根据地理位置更新经纬度
            // 山东省德州市各县区的实际经纬度
            jdbcTemplate.update("UPDATE plot SET longitude = 116.5430, latitude = 37.0630 WHERE location LIKE '%平原县%'");
            jdbcTemplate.update("UPDATE plot SET longitude = 116.8250, latitude = 36.9480 WHERE location LIKE '%禹城市%'");
            jdbcTemplate.update("UPDATE plot SET longitude = 116.7950, latitude = 36.7850 WHERE location LIKE '%齐河县%'");
            jdbcTemplate.update("UPDATE plot SET longitude = 117.2150, latitude = 37.7280 WHERE location LIKE '%乐陵市%'");
            jdbcTemplate.update("UPDATE plot SET longitude = 116.8350, latitude = 37.5120 WHERE location LIKE '%宁津县%'");
            jdbcTemplate.update("UPDATE plot SET longitude = 116.5750, latitude = 37.3250 WHERE location LIKE '%陵城区%'");
            
            log.info("根据地理位置更新经纬度成功");
            return ApiResponse.success("经纬度更新成功");
        } catch (Exception e) {
            log.error("更新经纬度失败", e);
            return ApiResponse.error("更新失败: " + e.getMessage());
        }
    }

    /**
     * 添加更多作物和种植计划
     */
    @PostMapping("/add-more-data")
    @PreAuthorize("hasAuthority('plot:write')")
    public ApiResponse<String> addMoreData() {
        try {
            // 添加更多作物
            jdbcTemplate.execute(
                "INSERT IGNORE INTO crop (name, variety, growth_cycle, planting_requirements, phenology_definition) VALUES " +
                "('棉花', '鲁棉研28', 180, '适宜在春季播种，秋季收获，需要充足的光照和温暖气候', '播种期,出苗期,现蕾期,开花期,吐絮期,成熟期'), " +
                "('花生', '花育33', 130, '适宜在春季播种，秋季收获，喜温作物', '播种期,出苗期,开花期,下针期,结荚期,饱果期,成熟期'), " +
                "('西瓜', '京欣1号', 90, '适宜在春季播种，夏季收获，需要充足光照和水分', '播种期,出苗期,伸蔓期,开花期,坐果期,膨瓜期,成熟期'), " +
                "('大白菜', '北京新3号', 70, '适宜在秋季播种，冬季收获，耐寒性强', '播种期,出苗期,莲座期,结球期,成熟期'), " +
                "('番茄', '中蔬4号', 100, '适宜在春季播种，夏季收获，需要支架栽培', '播种期,出苗期,定植期,开花期,坐果期,膨果期,成熟期')"
            );
            log.info("添加更多作物成功");

            // 清空现有种植计划
            jdbcTemplate.execute("DELETE FROM planting_plan");
            log.info("清空现有种植计划");

            // 添加匹配地块的种植计划（每个地块一个种植计划）
            jdbcTemplate.execute(
                "INSERT INTO planting_plan (crop_id, plot_id, planting_date, expected_harvest_date, status, remark) VALUES " +
                "(1, 1, '2026-03-15', '2026-10-15', 'IN_PROGRESS', '平原一号田小麦种植，长势良好'), " +
                "(2, 2, '2026-04-01', '2026-09-01', 'IN_PROGRESS', '平原二号田水稻种植，灌溉正常'), " +
                "(3, 3, '2026-04-20', '2026-08-20', 'NOT_STARTED', '平原三号田玉米种植计划'), " +
                "(4, 4, '2026-05-01', '2026-09-15', 'NOT_STARTED', '禹城一号田大豆种植计划'), " +
                "(5, 5, '2026-05-10', '2026-08-20', 'NOT_STARTED', '禹城二号田马铃薯种植计划'), " +
                "(6, 6, '2026-04-15', '2026-10-15', 'NOT_STARTED', '齐河一号田棉花种植计划'), " +
                "(7, 7, '2026-05-05', '2026-09-15', 'NOT_STARTED', '齐河二号田花生种植计划'), " +
                "(8, 8, '2026-04-10', '2026-07-10', 'NOT_STARTED', '乐陵一号田西瓜种植计划'), " +
                "(9, 9, '2026-08-15', '2026-11-15', 'NOT_STARTED', '宁津一号田大白菜种植计划'), " +
                "(10, 10, '2026-03-20', '2026-07-01', 'IN_PROGRESS', '陵城一号田番茄种植，已开花')"
            );
            log.info("添加种植计划成功");

            // 获取刚插入的种植计划ID
            List<Long> planIds = jdbcTemplate.queryForList(
                "SELECT id FROM planting_plan ORDER BY id", Long.class);

            // 清空现有物候期记录
            jdbcTemplate.execute("DELETE FROM phenology_record");
            log.info("清空现有物候期记录");

            // 添加物候期记录，使用实际的种植计划ID
            if (planIds.size() >= 10) {
                jdbcTemplate.update(
                    "INSERT INTO phenology_record (plan_id, phenology_name, record_date, description) VALUES " +
                    "(?, '播种期', '2026-03-15', '小麦播种完成，土壤湿度适宜，播种深度3-5cm')",
                    planIds.get(0)
                );
                jdbcTemplate.update(
                    "INSERT INTO phenology_record (plan_id, phenology_name, record_date, description) VALUES " +
                    "(?, '出苗期', '2026-03-25', '小麦出苗整齐，苗情良好，基本苗数30万/亩')",
                    planIds.get(0)
                );
                jdbcTemplate.update(
                    "INSERT INTO phenology_record (plan_id, phenology_name, record_date, description) VALUES " +
                    "(?, '分蘖期', '2026-04-10', '小麦分蘖正常，每株3-4个分蘖，群体结构合理')",
                    planIds.get(0)
                );
                jdbcTemplate.update(
                    "INSERT INTO phenology_record (plan_id, phenology_name, record_date, description) VALUES " +
                    "(?, '播种期', '2026-04-01', '水稻播种完成，水田灌溉正常，秧田面积2亩')",
                    planIds.get(1)
                );
                jdbcTemplate.update(
                    "INSERT INTO phenology_record (plan_id, phenology_name, record_date, description) VALUES " +
                    "(?, '出苗期', '2026-04-12', '水稻出苗良好，苗高15cm，叶龄3.5叶')",
                    planIds.get(1)
                );
                jdbcTemplate.update(
                    "INSERT INTO phenology_record (plan_id, phenology_name, record_date, description) VALUES " +
                    "(?, '播种期', '2026-03-20', '番茄播种完成，温室育苗，温度控制25-28°C')",
                    planIds.get(9)
                );
                jdbcTemplate.update(
                    "INSERT INTO phenology_record (plan_id, phenology_name, record_date, description) VALUES " +
                    "(?, '出苗期', '2026-03-28', '番茄出苗整齐，子叶展开，真叶1-2片')",
                    planIds.get(9)
                );
                jdbcTemplate.update(
                    "INSERT INTO phenology_record (plan_id, phenology_name, record_date, description) VALUES " +
                    "(?, '定植期', '2026-04-15', '番茄定植完成，株距40cm，行距60cm')",
                    planIds.get(9)
                );
                jdbcTemplate.update(
                    "INSERT INTO phenology_record (plan_id, phenology_name, record_date, description) VALUES " +
                    "(?, '开花期', '2026-05-10', '番茄开花正常，第一花序开花，需及时整枝')",
                    planIds.get(9)
                );
            }
            log.info("添加物候期记录成功");

            // 清空现有病虫害记录
            jdbcTemplate.execute("DELETE FROM pest_record");
            log.info("清空现有病虫害记录");

            // 添加病虫害记录，使用实际的种植计划ID
            if (planIds.size() >= 10) {
                jdbcTemplate.update(
                    "INSERT INTO pest_record (plan_id, pest_name, discovery_date, severity, status, description) VALUES " +
                    "(?, '小麦锈病', '2026-04-05', 'MEDIUM', 'TREATED', '发现少量锈病斑点，已喷施15%三唑酮可湿性粉剂防治')",
                    planIds.get(0)
                );
                jdbcTemplate.update(
                    "INSERT INTO pest_record (plan_id, pest_name, discovery_date, severity, status, description) VALUES " +
                    "(?, '蚜虫', '2026-04-18', 'LOW', 'PENDING', '发现少量蚜虫，需密切观察，必要时喷施吡虫啉')",
                    planIds.get(0)
                );
                jdbcTemplate.update(
                    "INSERT INTO pest_record (plan_id, pest_name, discovery_date, severity, status, description) VALUES " +
                    "(?, '稻飞虱', '2026-04-15', 'LOW', 'PENDING', '发现少量稻飞虱，需加强田间管理，保持浅水层')",
                    planIds.get(1)
                );
                jdbcTemplate.update(
                    "INSERT INTO pest_record (plan_id, pest_name, discovery_date, severity, status, description) VALUES " +
                    "(?, '番茄早疫病', '2026-05-08', 'MEDIUM', 'TREATED', '发现早疫病病斑，已喷施75%百菌清可湿性粉剂')",
                    planIds.get(9)
                );
            }
            log.info("添加病虫害记录成功");

            // 添加产量预估数据，根据历史数据和病虫害情况推理
            if (planIds.size() >= 10) {
                // 小麦：有锈病(MEDIUM)和蚜虫(LOW)，实际产量4350，预估4500，置信度85%
                jdbcTemplate.update(
                    "INSERT INTO yield_prediction (plan_id, prediction_date, predicted_yield, unit, prediction_method, confidence_level, growth_stage, weather_impact, fertilizer_impact, water_impact, remark) VALUES " +
                    "(?, '2026-04-20', 4500.00, '千克', 'MACHINE_LEARNING', 85.0, '成熟期', '良好', '充足', '适中', '基于历史数据预测，考虑锈病和蚜虫影响，预计产量4500kg，实际产量4350kg，预测准确率96.7%')",
                    planIds.get(0)
                );
                // 水稻：有稻飞虱(LOW)，实际产量5650，预估5800，置信度88%
                jdbcTemplate.update(
                    "INSERT INTO yield_prediction (plan_id, prediction_date, predicted_yield, unit, prediction_method, confidence_level, growth_stage, weather_impact, fertilizer_impact, water_impact, remark) VALUES " +
                    "(?, '2026-04-20', 5800.00, '千克', 'MACHINE_LEARNING', 88.0, '成熟期', '良好', '充足', '充足', '基于历史数据预测，稻飞虱影响较小，预计产量5800kg，实际产量5650kg，预测准确率97.4%')",
                    planIds.get(1)
                );
                // 玉米：无病虫害，实际产量6100，预估6200，置信度90%
                jdbcTemplate.update(
                    "INSERT INTO yield_prediction (plan_id, prediction_date, predicted_yield, unit, prediction_method, confidence_level, growth_stage, weather_impact, fertilizer_impact, water_impact, remark) VALUES " +
                    "(?, '2026-04-20', 6200.00, '千克', 'MACHINE_LEARNING', 90.0, '成熟期', '良好', '充足', '适中', '基于历史数据预测，无病虫害影响，预计产量6200kg，实际产量6100kg，预测准确率98.4%')",
                    planIds.get(2)
                );
                // 大豆：无病虫害，实际产量2750，预估2800，置信度82%
                jdbcTemplate.update(
                    "INSERT INTO yield_prediction (plan_id, prediction_date, predicted_yield, unit, prediction_method, confidence_level, growth_stage, weather_impact, fertilizer_impact, water_impact, remark) VALUES " +
                    "(?, '2026-04-20', 2800.00, '千克', 'MACHINE_LEARNING', 82.0, '成熟期', '一般', '适中', '适中', '基于历史数据预测，生长条件一般，预计产量2800kg，实际产量2750kg，预测准确率98.2%')",
                    planIds.get(3)
                );
                // 马铃薯：无病虫害，实际产量3400，预估3500，置信度87%
                jdbcTemplate.update(
                    "INSERT INTO yield_prediction (plan_id, prediction_date, predicted_yield, unit, prediction_method, confidence_level, growth_stage, weather_impact, fertilizer_impact, water_impact, remark) VALUES " +
                    "(?, '2026-04-20', 3500.00, '千克', 'MACHINE_LEARNING', 87.0, '成熟期', '良好', '充足', '适中', '基于历史数据预测，生长条件良好，预计产量3500kg，实际产量3400kg，预测准确率97.1%')",
                    planIds.get(4)
                );
                // 棉花：无病虫害，实际产量4100，预估4200，置信度86%
                jdbcTemplate.update(
                    "INSERT INTO yield_prediction (plan_id, prediction_date, predicted_yield, unit, prediction_method, confidence_level, growth_stage, weather_impact, fertilizer_impact, water_impact, remark) VALUES " +
                    "(?, '2026-04-20', 4200.00, '千克', 'MACHINE_LEARNING', 86.0, '成熟期', '良好', '充足', '适中', '基于历史数据预测，生长条件良好，预计产量4200kg，实际产量4100kg，预测准确率97.6%')",
                    planIds.get(5)
                );
                // 花生：无病虫害，实际产量3700，预估3800，置信度84%
                jdbcTemplate.update(
                    "INSERT INTO yield_prediction (plan_id, prediction_date, predicted_yield, unit, prediction_method, confidence_level, growth_stage, weather_impact, fertilizer_impact, water_impact, remark) VALUES " +
                    "(?, '2026-04-20', 3800.00, '千克', 'MACHINE_LEARNING', 84.0, '成熟期', '良好', '适中', '适中', '基于历史数据预测，生长条件良好，预计产量3800kg，实际产量3700kg，预测准确率97.4%')",
                    planIds.get(6)
                );
                // 西瓜：无病虫害，实际产量24500，预估25000，置信度89%
                jdbcTemplate.update(
                    "INSERT INTO yield_prediction (plan_id, prediction_date, predicted_yield, unit, prediction_method, confidence_level, growth_stage, weather_impact, fertilizer_impact, water_impact, remark) VALUES " +
                    "(?, '2026-04-20', 25000.00, '千克', 'MACHINE_LEARNING', 89.0, '成熟期', '良好', '充足', '充足', '基于历史数据预测，生长条件优良，预计产量25000kg，实际产量24500kg，预测准确率98.0%')",
                    planIds.get(7)
                );
                // 大白菜：无病虫害，实际产量44000，预估45000，置信度91%
                jdbcTemplate.update(
                    "INSERT INTO yield_prediction (plan_id, prediction_date, predicted_yield, unit, prediction_method, confidence_level, growth_stage, weather_impact, fertilizer_impact, water_impact, remark) VALUES " +
                    "(?, '2026-04-20', 45000.00, '千克', 'MACHINE_LEARNING', 91.0, '成熟期', '良好', '充足', '充足', '基于历史数据预测，生长条件优良，预计产量45000kg，实际产量44000kg，预测准确率97.8%')",
                    planIds.get(8)
                );
                // 番茄：有早疫病(MEDIUM)，实际产量54000，预估55000，置信度83%
                jdbcTemplate.update(
                    "INSERT INTO yield_prediction (plan_id, prediction_date, predicted_yield, unit, prediction_method, confidence_level, growth_stage, weather_impact, fertilizer_impact, water_impact, remark) VALUES " +
                    "(?, '2026-04-20', 55000.00, '千克', 'MACHINE_LEARNING', 83.0, '成熟期', '良好', '充足', '适中', '基于历史数据预测，考虑早疫病影响，预计产量55000kg，实际产量54000kg，预测准确率98.2%')",
                    planIds.get(9)
                );
                log.info("添加产量预估数据成功");
            }

            // 添加采收记录数据，基于产量预估的真实数据
            if (planIds.size() >= 10) {
                jdbcTemplate.update(
                    "INSERT INTO harvest_record (plan_id, harvest_date, harvest_quantity, unit, quality_grade, harvest_method, buyer, sale_amount, remark) VALUES " +
                    "(?, '2026-10-15', 4350.00, '千克', 'A', '机械采收', '面粉厂', 8700.00, '小麦采收完成，产量略低于预期，品质优良，蛋白质含量12.5%')",
                    planIds.get(0)
                );
                jdbcTemplate.update(
                    "INSERT INTO harvest_record (plan_id, harvest_date, harvest_quantity, unit, quality_grade, harvest_method, buyer, sale_amount, remark) VALUES " +
                    "(?, '2026-09-01', 5650.00, '千克', 'A', '机械采收', '米厂', 16950.00, '水稻采收完成，产量接近预期，米质优良，出米率72%')",
                    planIds.get(1)
                );
                jdbcTemplate.update(
                    "INSERT INTO harvest_record (plan_id, harvest_date, harvest_quantity, unit, quality_grade, harvest_method, buyer, sale_amount, remark) VALUES " +
                    "(?, '2026-08-20', 6100.00, '千克', 'A', '机械采收', '饲料厂', 12200.00, '玉米采收完成，产量符合预期，颗粒饱满，水分含量14%')",
                    planIds.get(2)
                );
                jdbcTemplate.update(
                    "INSERT INTO harvest_record (plan_id, harvest_date, harvest_quantity, unit, quality_grade, harvest_method, buyer, sale_amount, remark) VALUES " +
                    "(?, '2026-09-15', 2750.00, '千克', 'B', '机械采收', '油厂', 8250.00, '大豆采收完成，产量略低于预期，品质良好，含油率18%')",
                    planIds.get(3)
                );
                jdbcTemplate.update(
                    "INSERT INTO harvest_record (plan_id, harvest_date, harvest_quantity, unit, quality_grade, harvest_method, buyer, sale_amount, remark) VALUES " +
                    "(?, '2026-08-20', 3400.00, '千克', 'A', '人工采收', '批发市场', 6800.00, '马铃薯采收完成，产量接近预期，大小均匀，淀粉含量16%')",
                    planIds.get(4)
                );
                jdbcTemplate.update(
                    "INSERT INTO harvest_record (plan_id, harvest_date, harvest_quantity, unit, quality_grade, harvest_method, buyer, sale_amount, remark) VALUES " +
                    "(?, '2026-10-15', 4100.00, '千克', 'A', '人工采收', '纺织厂', 20500.00, '棉花采收完成，产量符合预期，纤维品质优良，衣分率38%')",
                    planIds.get(5)
                );
                jdbcTemplate.update(
                    "INSERT INTO harvest_record (plan_id, harvest_date, harvest_quantity, unit, quality_grade, harvest_method, buyer, sale_amount, remark) VALUES " +
                    "(?, '2026-09-15', 3700.00, '千克', 'A', '机械采收', '油厂', 11100.00, '花生采收完成，产量接近预期，颗粒饱满，含油率45%')",
                    planIds.get(6)
                );
                jdbcTemplate.update(
                    "INSERT INTO harvest_record (plan_id, harvest_date, harvest_quantity, unit, quality_grade, harvest_method, buyer, sale_amount, remark) VALUES " +
                    "(?, '2026-07-10', 24500.00, '千克', 'A', '人工采收', '水果批发', 49000.00, '西瓜采收完成，产量符合预期，甜度高，中心糖度12度')",
                    planIds.get(7)
                );
                jdbcTemplate.update(
                    "INSERT INTO harvest_record (plan_id, harvest_date, harvest_quantity, unit, quality_grade, harvest_method, buyer, sale_amount, remark) VALUES " +
                    "(?, '2026-11-15', 44000.00, '千克', 'A', '人工采收', '蔬菜批发', 88000.00, '大白菜采收完成，产量接近预期，包心紧实，单株重2.5kg')",
                    planIds.get(8)
                );
                jdbcTemplate.update(
                    "INSERT INTO harvest_record (plan_id, harvest_date, harvest_quantity, unit, quality_grade, harvest_method, buyer, sale_amount, remark) VALUES " +
                    "(?, '2026-07-01', 54000.00, '千克', 'A', '人工采收', '蔬菜批发', 162000.00, '番茄采收完成，产量符合预期，果色鲜红，可溶性固形物5%')",
                    planIds.get(9)
                );
                log.info("添加采收记录数据成功");
            }

            return ApiResponse.success("数据添加成功");
        } catch (Exception e) {
            log.error("添加数据失败", e);
            return ApiResponse.error("添加失败: " + e.getMessage());
        }
    }

    /**
     * 重置数据库（删除所有表并重新初始化）
     */
    @PostMapping("/reset-database")
    @PreAuthorize("hasAuthority('plot:write')")
    public ApiResponse<String> resetDatabase() {
        try {
            // 删除所有表
            jdbcTemplate.execute("DROP TABLE IF EXISTS yield_prediction");
            jdbcTemplate.execute("DROP TABLE IF EXISTS pest_record");
            jdbcTemplate.execute("DROP TABLE IF EXISTS phenology_record");
            jdbcTemplate.execute("DROP TABLE IF EXISTS harvest_record");
            jdbcTemplate.execute("DROP TABLE IF EXISTS material_usage");
            jdbcTemplate.execute("DROP TABLE IF EXISTS material");
            jdbcTemplate.execute("DROP TABLE IF EXISTS planting_plan");
            jdbcTemplate.execute("DROP TABLE IF EXISTS plot");
            jdbcTemplate.execute("DROP TABLE IF EXISTS crop");
            jdbcTemplate.execute("DROP TABLE IF EXISTS chat_history");
            jdbcTemplate.execute("DROP TABLE IF EXISTS sys_role_permission");
            jdbcTemplate.execute("DROP TABLE IF EXISTS sys_user_role");
            jdbcTemplate.execute("DROP TABLE IF EXISTS sys_permission");
            jdbcTemplate.execute("DROP TABLE IF EXISTS sys_role");
            jdbcTemplate.execute("DROP TABLE IF EXISTS sys_user");
            log.info("删除所有表成功");
            
            return ApiResponse.success("数据库重置成功，请重启服务以重新初始化");
        } catch (Exception e) {
            log.error("重置数据库失败", e);
            return ApiResponse.error("重置失败: " + e.getMessage());
        }
    }

    /**
     * 查询地块数据（调试用）
     */
    @GetMapping("/query-plots")
    @PreAuthorize("hasAuthority('plot:read')")
    public ApiResponse<String> queryPlots() {
        try {
            String result = jdbcTemplate.queryForObject(
                "SELECT CONCAT('ID:', id, ', Name:', name, ', Area:', area) FROM plot LIMIT 1", 
                String.class
            );
            return ApiResponse.success(result);
        } catch (Exception e) {
            log.error("查询地块失败", e);
            return ApiResponse.error("查询失败: " + e.getMessage());
        }
    }
}
