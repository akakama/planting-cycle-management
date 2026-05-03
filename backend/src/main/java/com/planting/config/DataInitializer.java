package com.planting.config;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.planting.entity.Crop;
import com.planting.entity.HarvestRecord;
import com.planting.entity.Material;
import com.planting.entity.PestKnowledge;
import com.planting.entity.PhenologyRecord;
import com.planting.entity.Plot;
import com.planting.entity.PlantingPlan;
import com.planting.entity.YieldPrediction;
import com.planting.mapper.CropMapper;
import com.planting.mapper.HarvestRecordMapper;
import com.planting.mapper.MaterialMapper;
import com.planting.mapper.PestKnowledgeMapper;
import com.planting.mapper.PhenologyRecordMapper;
import com.planting.mapper.PlotMapper;
import com.planting.mapper.PlantingPlanMapper;
import com.planting.mapper.UserMapper;
import com.planting.mapper.YieldPredictionMapper;
import com.planting.entity.User;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * 数据初始化器
 * 在应用启动时自动初始化测试数据
 */
@Slf4j
@Component
public class DataInitializer implements CommandLineRunner {

    @Resource
    private JdbcTemplate jdbcTemplate;
    
    @Resource
    private PlotMapper plotMapper;
    
    @Resource
    private CropMapper cropMapper;
    
    @Resource
    private MaterialMapper materialMapper;
    
    @Resource
    private PlantingPlanMapper plantingPlanMapper;
    
    @Resource
    private PhenologyRecordMapper phenologyRecordMapper;
    
    @Resource
    private PestKnowledgeMapper pestKnowledgeMapper;
    
    @Resource
    private HarvestRecordMapper harvestRecordMapper;
    
    @Resource
    private YieldPredictionMapper yieldPredictionMapper;
    
    @Resource
    private UserMapper userMapper;

    @Override
    public void run(String... args) {
        log.info("开始初始化测试数据...");
        
        try {
            // 先创建表结构
            createTables();
            
            // 然后初始化数据
            initUserData();
            initPlotData();
            initCropData();
            initMaterialData();
            initPlantingPlanData();
            initPhenologyRecordData();
            initPestKnowledgeData();
            initHarvestRecordData();
            initYieldPredictionData();
            
            log.info("测试数据初始化完成!");
        } catch (Exception e) {
            log.error("初始化测试数据失败: {}", e.getMessage(), e);
        }
    }
    
    /**
     * 创建表结构
     */
    private void createTables() {
        log.info("开始创建表结构...");
        
        try {
            // 删除旧表以确保结构正确
            try {
                jdbcTemplate.execute("DROP TABLE IF EXISTS plot");
                log.info("删除旧的plot表");
            } catch (Exception e) {
                log.info("plot表不存在或删除失败: {}", e.getMessage());
            }
            
            // 创建用户表
            jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS sys_user (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY," +
                "username VARCHAR(50) NOT NULL UNIQUE," +
                "password VARCHAR(100) NOT NULL," +
                "real_name VARCHAR(50)," +
                "email VARCHAR(100)," +
                "phone VARCHAR(20)," +
                "status INT DEFAULT 1," +
                "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "deleted INT DEFAULT 0" +
                ")");
            
            // 创建地块表
            jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS plot (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY," +
                "code VARCHAR(50) NOT NULL UNIQUE," +
                "name VARCHAR(100) NOT NULL," +
                "area DECIMAL(10,2) NOT NULL," +
                "location VARCHAR(200)," +
                "soil_type VARCHAR(50)," +
                "longitude DECIMAL(10,6)," +
                "latitude DECIMAL(10,6)," +
                "remark TEXT," +
                "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "deleted INT DEFAULT 0" +
                ")");
            
            // 创建作物表
            jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS crop (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY," +
                "name VARCHAR(100) NOT NULL UNIQUE," +
                "variety VARCHAR(100)," +
                "growth_cycle INT," +
                "planting_requirements TEXT," +
                "phenology_definition VARCHAR(500)," +
                "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "deleted INT DEFAULT 0" +
                ")");
            
            // 创建农资表
            jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS material (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY," +
                "name VARCHAR(100) NOT NULL," +
                "type VARCHAR(20) NOT NULL," +
                "specification VARCHAR(100)," +
                "stock_quantity DECIMAL(10,2) NOT NULL DEFAULT 0," +
                "unit VARCHAR(20) NOT NULL," +
                "supplier VARCHAR(100)," +
                "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "version INT DEFAULT 0," +
                "deleted INT DEFAULT 0" +
                ")");
            
            // 创建种植计划表
            jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS planting_plan (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY," +
                "crop_id BIGINT NOT NULL," +
                "plot_id BIGINT NOT NULL," +
                "planting_date DATE NOT NULL," +
                "expected_harvest_date DATE," +
                "status VARCHAR(50) NOT NULL DEFAULT '未开始'," +
                "remark TEXT," +
                "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "deleted INT DEFAULT 0" +
                ")");
            
            // 创建物候期记录表
            jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS phenology_record (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY," +
                "plan_id BIGINT NOT NULL," +
                "phenology_name VARCHAR(100) NOT NULL," +
                "record_date DATE NOT NULL," +
                "description TEXT," +
                "environmental_data TEXT," +
                "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "deleted INT DEFAULT 0" +
                ")");
            
            // 创建病虫害知识库表
            jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS pest_knowledge (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY," +
                "pest_name VARCHAR(100) NOT NULL," +
                "pest_type VARCHAR(50) NOT NULL," +
                "affected_crops TEXT NOT NULL," +
                "symptoms TEXT NOT NULL," +
                "visual_features TEXT NOT NULL," +
                "season VARCHAR(50)," +
                "severity VARCHAR(50)," +
                "treatment_methods TEXT NOT NULL," +
                "prevention_methods TEXT," +
                "image_patterns TEXT," +
                "confidence_score DECIMAL(5,2) DEFAULT 80.00," +
                "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "deleted INT DEFAULT 0" +
                ")");
            
            // 创建采收记录表
            jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS harvest_record (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY," +
                "plan_id BIGINT NOT NULL," +
                "harvest_date DATE NOT NULL," +
                "harvest_quantity DECIMAL(10,2) NOT NULL," +
                "harvest_method VARCHAR(50)," +
                "buyer VARCHAR(100)," +
                "sale_amount DECIMAL(10,2)," +
                "unit VARCHAR(20)," +
                "quality_grade VARCHAR(50) NOT NULL DEFAULT '普通'," +
                "moisture_content DECIMAL(5,2)," +
                "protein_content DECIMAL(5,2)," +
                "harvest_area DECIMAL(10,2)," +
                "remark TEXT," +
                "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "deleted INT DEFAULT 0" +
                ")");
            
            // 创建产量预估表
            jdbcTemplate.execute("CREATE TABLE IF NOT EXISTS yield_prediction (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY," +
                "plan_id BIGINT NOT NULL," +
                "prediction_date DATE NOT NULL," +
                "predicted_yield DECIMAL(10,2) NOT NULL," +
                "confidence_level VARCHAR(50)," +
                "growth_stage VARCHAR(50)," +
                "weather_impact TEXT," +
                "fertilizer_impact TEXT," +
                "water_impact TEXT," +
                "remark TEXT," +
                "create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP," +
                "deleted INT DEFAULT 0" +
                ")");
            
            log.info("表结构创建完成!");
        } catch (Exception e) {
            log.error("创建表结构失败: {}", e.getMessage(), e);
        }
    }
    
    /**
     * 初始化地块数据
     */
    private void initPlotData() {
        // 强制重新初始化地块数据
        log.info("开始初始化地块数据...");
        
        // 清空现有数据
        try {
            jdbcTemplate.execute("DELETE FROM plot");
        } catch (Exception e) {
            log.info("清空plot表失败: {}", e.getMessage());
        }
        
        Plot plot1 = new Plot();
        plot1.setCode("P001");
        plot1.setName("平原一号田");
        plot1.setArea(new BigDecimal("8500"));
        plot1.setLocation("山东省德州市平原县");
        plot1.setSoilType("壤土");
        plot1.setRemark("优质小麦种植基地，灌溉条件良好");
        plotMapper.insert(plot1);

        Plot plot2 = new Plot();
        plot2.setCode("P002");
        plot2.setName("平原二号田");
        plot2.setArea(new BigDecimal("7200"));
        plot2.setLocation("山东省德州市平原县");
        plot2.setSoilType("沙壤土");
        plot2.setRemark("玉米种植区，排水系统完善");
        plotMapper.insert(plot2);

        Plot plot3 = new Plot();
        plot3.setCode("P003");
        plot3.setName("平原三号田");
        plot3.setArea(new BigDecimal("6800"));
        plot3.setLocation("山东省德州市平原县");
        plot3.setSoilType("黑土");
        plot3.setRemark("水稻种植试验田，水源充足");
        plotMapper.insert(plot3);

        Plot plot4 = new Plot();
        plot4.setCode("P004");
        plot4.setName("禹城一号田");
        plot4.setArea(new BigDecimal("9200"));
        plot4.setLocation("山东省德州市禹城市");
        plot4.setSoilType("棕壤土");
        plot4.setRemark("大豆种植基地，土壤肥力高");
        plotMapper.insert(plot4);

        Plot plot5 = new Plot();
        plot5.setCode("P005");
        plot5.setName("禹城二号田");
        plot5.setArea(new BigDecimal("5600"));
        plot5.setLocation("山东省德州市禹城市");
        plot5.setSoilType("黄褐土");
        plot5.setRemark("马铃薯种植区，土层深厚");
        plotMapper.insert(plot5);

        Plot plot6 = new Plot();
        plot6.setCode("P006");
        plot6.setName("齐河一号田");
        plot6.setArea(new BigDecimal("7800"));
        plot6.setLocation("山东省德州市齐河县");
        plot6.setSoilType("潮土");
        plot6.setRemark("小麦玉米轮作区，机械化程度高");
        plotMapper.insert(plot6);

        Plot plot7 = new Plot();
        plot7.setCode("P007");
        plot7.setName("齐河二号田");
        plot7.setArea(new BigDecimal("6400"));
        plot7.setLocation("山东省德州市齐河县");
        plot7.setSoilType("盐碱土");
        plot7.setRemark("改良盐碱地试验田，种植耐盐作物");
        plotMapper.insert(plot7);

        Plot plot8 = new Plot();
        plot8.setCode("P008");
        plot8.setName("乐陵一号田");
        plot8.setArea(new BigDecimal("5100"));
        plot8.setLocation("山东省德州市乐陵市");
        plot8.setSoilType("沙土");
        plot8.setRemark("红枣种植基地，适宜果树生长");
        plotMapper.insert(plot8);

        Plot plot9 = new Plot();
        plot9.setCode("P009");
        plot9.setName("宁津一号田");
        plot9.setArea(new BigDecimal("7300"));
        plot9.setLocation("山东省德州市宁津县");
        plot9.setSoilType("壤土");
        plot9.setRemark("有机蔬菜种植基地，无公害认证");
        plotMapper.insert(plot9);

        Plot plot10 = new Plot();
        plot10.setCode("P010");
        plot10.setName("陵城一号田");
        plot10.setArea(new BigDecimal("8900"));
        plot10.setLocation("山东省德州市陵城区");
        plot10.setSoilType("黑钙土");
        plot10.setRemark("粮食高产创建示范田，亩产水平高");
        plotMapper.insert(plot10);
        
        log.info("地块数据初始化完成,共插入10条记录");
    }
    
    /**
     * 初始化作物数据
     */
    private void initCropData() {
        long cropCount = cropMapper.selectCount(null);
        if (cropCount > 0) {
            log.info("作物数据已存在,跳过初始化");
            return;
        }
        
        log.info("开始初始化作物数据...");
        
        Crop crop1 = new Crop();
        crop1.setName("小麦");
        crop1.setVariety("济麦22");
        crop1.setGrowthCycle(220);
        crop1.setPlantingRequirements("适宜在秋季播种,春季收获,需要充足的光照和水分");
        crop1.setPhenologyDefinition("播种期,出苗期,分蘖期,拔节期,抽穗期,开花期,灌浆期,成熟期");
        cropMapper.insert(crop1);
        
        Crop crop2 = new Crop();
        crop2.setName("水稻");
        crop2.setVariety("杂交水稻");
        crop2.setGrowthCycle(150);
        crop2.setPlantingRequirements("适宜在水田种植,需要充足的灌溉,温度要求较高");
        crop2.setPhenologyDefinition("播种期,出苗期,分蘖期,拔节期,抽穗期,开花期,灌浆期,成熟期");
        cropMapper.insert(crop2);
        
        Crop crop3 = new Crop();
        crop3.setName("玉米");
        crop3.setVariety("郑单958");
        crop3.setGrowthCycle(120);
        crop3.setPlantingRequirements("适宜在春季播种,秋季收获,需要充足的阳光和水分");
        crop3.setPhenologyDefinition("播种期,出苗期,拔节期,抽穗期,开花期,灌浆期,成熟期");
        cropMapper.insert(crop3);
        
        Crop crop4 = new Crop();
        crop4.setName("大豆");
        crop4.setVariety("黑农44");
        crop4.setGrowthCycle(120);
        crop4.setPlantingRequirements("适宜在春季播种,秋季收获,对土壤要求不高");
        crop4.setPhenologyDefinition("播种期,出苗期,开花期,结荚期,鼓粒期,成熟期");
        cropMapper.insert(crop4);
        
        Crop crop5 = new Crop();
        crop5.setName("马铃薯");
        crop5.setVariety("费乌瑞它");
        crop5.setGrowthCycle(100);
        crop5.setPlantingRequirements("适宜在春季或秋季播种,对土壤要求疏松");
        crop5.setPhenologyDefinition("播种期,出苗期,现蕾期,开花期,块茎膨大期,成熟期");
        cropMapper.insert(crop5);
        
        log.info("作物数据初始化完成,共插入5条记录");
    }
    
    /**
     * 初始化农资数据
     */
    private void initMaterialData() {
        long materialCount = materialMapper.selectCount(null);
        if (materialCount > 0) {
            log.info("农资数据已存在,跳过初始化");
            return;
        }
        
        log.info("开始初始化农资数据...");
        
        Material material1 = new Material();
        material1.setName("尿素");
        material1.setType("FERTILIZER");
        material1.setSpecification("46%含氮量");
        material1.setStockQuantity(new BigDecimal("1000.00"));
        material1.setUnit("千克");
        material1.setSupplier("化肥公司");
        materialMapper.insert(material1);
        
        Material material2 = new Material();
        material2.setName("复合肥");
        material2.setType("FERTILIZER");
        material2.setSpecification("NPK 15-15-15");
        material2.setStockQuantity(new BigDecimal("800.00"));
        material2.setUnit("千克");
        material2.setSupplier("化肥公司");
        materialMapper.insert(material2);
        
        Material material3 = new Material();
        material3.setName("多菌灵");
        material3.setType("PESTICIDE");
        material3.setSpecification("50%可湿性粉剂");
        material3.setStockQuantity(new BigDecimal("200.00"));
        material3.setUnit("千克");
        material3.setSupplier("农药公司");
        materialMapper.insert(material3);
        
        Material material4 = new Material();
        material4.setName("吡虫啉");
        material4.setType("PESTICIDE");
        material4.setSpecification("20%可湿性粉剂");
        material4.setStockQuantity(new BigDecimal("150.00"));
        material4.setUnit("千克");
        material4.setSupplier("农药公司");
        materialMapper.insert(material4);
        
        Material material5 = new Material();
        material5.setName("小麦种子");
        material5.setType("SEED");
        material5.setSpecification("济麦22");
        material5.setStockQuantity(new BigDecimal("500.00"));
        material5.setUnit("千克");
        material5.setSupplier("种子公司");
        materialMapper.insert(material5);
        
        Material material6 = new Material();
        material6.setName("水稻种子");
        material6.setType("SEED");
        material6.setSpecification("杂交水稻");
        material6.setStockQuantity(new BigDecimal("400.00"));
        material6.setUnit("千克");
        material6.setSupplier("种子公司");
        materialMapper.insert(material6);
        
        log.info("农资数据初始化完成,共插入6条记录");
    }
    
    /**
     * 初始化用户数据
     */
    private void initUserData() {
        long userCount = userMapper.selectCount(null);
        if (userCount > 0) {
            log.info("用户数据已存在,跳过初始化");
            return;
        }
        
        log.info("开始初始化用户数据...");
        
        BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
        
        User admin = new User();
        admin.setUsername("admin");
        admin.setPassword(passwordEncoder.encode("admin123"));
        admin.setRealName("系统管理员");
        admin.setEmail("admin@planting.com");
        admin.setPhone("13800138000");
        admin.setStatus(1);
        userMapper.insert(admin);
        
        log.info("用户数据初始化完成,共插入1条记录");
    }
    
    /**
     * 初始化种植计划数据
     */
    private void initPlantingPlanData() {
        log.info("开始初始化种植计划数据...");
        
        // 强制重新初始化种植计划数据
        try {
            jdbcTemplate.execute("DELETE FROM planting_plan");
            log.info("清空现有种植计划数据");
        } catch (Exception e) {
            log.error("清空种植计划数据失败: {}", e.getMessage());
        }
        
        LocalDate today = LocalDate.now();
        
        // 获取地块和作物数据
        List<Plot> plots = plotMapper.selectList(null);
        List<Crop> crops = cropMapper.selectList(null);
        
        if (plots.isEmpty() || crops.isEmpty()) {
            log.warn("地块或作物数据为空,跳过种植计划初始化");
            return;
        }
        
        // 创建20条多样化的种植计划
        PlantingPlan plan;
        
        // 1. 小麦种植（不同地块，不同时间）
        plan = new PlantingPlan();
        plan.setCropId(crops.get(0).getId()); // 小麦
        plan.setPlotId(plots.get(0).getId()); // 平原一号田
        plan.setPlantingDate(today);
        plan.setExpectedHarvestDate(today.plusDays(220));
        plan.setStatus("进行中");
        plan.setRemark("春季小麦播种，优质品种");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(0).getId()); // 小麦
        plan.setPlotId(plots.get(5).getId()); // 齐河一号田
        plan.setPlantingDate(today.plusWeeks(3));
        plan.setExpectedHarvestDate(today.plusWeeks(3).plusDays(220));
        plan.setStatus("未开始");
        plan.setRemark("小麦玉米轮作区，第二季小麦");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(0).getId()); // 小麦
        plan.setPlotId(plots.get(9).getId()); // 陵城一号田
        plan.setPlantingDate(today.minusMonths(2));
        plan.setExpectedHarvestDate(today.minusMonths(2).plusDays(220));
        plan.setStatus("已完成");
        plan.setRemark("高产创建示范田，春季小麦");
        plantingPlanMapper.insert(plan);
        
        // 2. 水稻种植
        plan = new PlantingPlan();
        plan.setCropId(crops.get(1).getId()); // 水稻
        plan.setPlotId(plots.get(2).getId()); // 平原三号田
        plan.setPlantingDate(today.plusWeeks(2));
        plan.setExpectedHarvestDate(today.plusWeeks(2).plusDays(150));
        plan.setStatus("未开始");
        plan.setRemark("水稻试验田，杂交水稻品种");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(1).getId()); // 水稻
        plan.setPlotId(plots.get(6).getId()); // 齐河二号田
        plan.setPlantingDate(today.plusWeeks(4));
        plan.setExpectedHarvestDate(today.plusWeeks(4).plusDays(150));
        plan.setStatus("未开始");
        plan.setRemark("改良盐碱地种植耐盐水稻");
        plantingPlanMapper.insert(plan);
        
        // 3. 玉米种植（多种地块和时间）
        plan = new PlantingPlan();
        plan.setCropId(crops.get(2).getId()); // 玉米
        plan.setPlotId(plots.get(1).getId()); // 平原二号田
        plan.setPlantingDate(today.plusWeeks(1));
        plan.setExpectedHarvestDate(today.plusWeeks(1).plusDays(120));
        plan.setStatus("进行中");
        plan.setRemark("春季玉米播种，郑单958品种");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(2).getId()); // 玉米
        plan.setPlotId(plots.get(5).getId()); // 齐河一号田
        plan.setPlantingDate(today.plusWeeks(5));
        plan.setExpectedHarvestDate(today.plusWeeks(5).plusDays(120));
        plan.setStatus("未开始");
        plan.setRemark("小麦收获后种植夏玉米");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(2).getId()); // 玉米
        plan.setPlotId(plots.get(3).getId()); // 禹城一号田
        plan.setPlantingDate(today.minusMonths(3));
        plan.setExpectedHarvestDate(today.minusMonths(3).plusDays(120));
        plan.setStatus("已完成");
        plan.setRemark("早熟玉米品种，已收获");
        plantingPlanMapper.insert(plan);
        
        // 4. 大豆种植
        plan = new PlantingPlan();
        plan.setCropId(crops.get(3).getId()); // 大豆
        plan.setPlotId(plots.get(3).getId()); // 禹城一号田
        plan.setPlantingDate(today.plusWeeks(3));
        plan.setExpectedHarvestDate(today.plusWeeks(3).plusDays(120));
        plan.setStatus("未开始");
        plan.setRemark("大豆种植基地，黑农44品种");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(3).getId()); // 大豆
        plan.setPlotId(plots.get(4).getId()); // 禹城二号田
        plan.setPlantingDate(today.plusWeeks(6));
        plan.setExpectedHarvestDate(today.plusWeeks(6).plusDays(120));
        plan.setStatus("未开始");
        plan.setRemark("大豆玉米间作试验");
        plantingPlanMapper.insert(plan);
        
        // 5. 马铃薯种植
        plan = new PlantingPlan();
        plan.setCropId(crops.get(4).getId()); // 马铃薯
        plan.setPlotId(plots.get(4).getId()); // 禹城二号田
        plan.setPlantingDate(today);
        plan.setExpectedHarvestDate(today.plusDays(100));
        plan.setStatus("进行中");
        plan.setRemark("春季马铃薯，费乌瑞它品种");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(4).getId()); // 马铃薯
        plan.setPlotId(plots.get(7).getId()); // 乐陵一号田
        plan.setPlantingDate(today.plusWeeks(2));
        plan.setExpectedHarvestDate(today.plusWeeks(2).plusDays(100));
        plan.setStatus("未开始");
        plan.setRemark("沙土地种植马铃薯，品质优良");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(4).getId()); // 马铃薯
        plan.setPlotId(plots.get(8).getId()); // 宁津一号田
        plan.setPlantingDate(today.minusMonths(1));
        plan.setExpectedHarvestDate(today.minusMonths(1).plusDays(100));
        plan.setStatus("已完成");
        plan.setRemark("早春马铃薯，已收获");
        plantingPlanMapper.insert(plan);
        
        // 6. 混合种植计划（不同时间跨度）
        plan = new PlantingPlan();
        plan.setCropId(crops.get(0).getId()); // 小麦
        plan.setPlotId(plots.get(6).getId()); // 齐河二号田
        plan.setPlantingDate(today.minusMonths(4));
        plan.setExpectedHarvestDate(today.minusMonths(4).plusDays(220));
        plan.setStatus("已完成");
        plan.setRemark("盐碱地改良种植小麦");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(1).getId()); // 水稻
        plan.setPlotId(plots.get(8).getId()); // 宁津一号田
        plan.setPlantingDate(today.plusWeeks(8));
        plan.setExpectedHarvestDate(today.plusWeeks(8).plusDays(150));
        plan.setStatus("未开始");
        plan.setRemark("有机蔬菜基地轮作水稻");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(3).getId()); // 大豆
        plan.setPlotId(plots.get(7).getId()); // 乐陵一号田
        plan.setPlantingDate(today.plusWeeks(10));
        plan.setExpectedHarvestDate(today.plusWeeks(10).plusDays(120));
        plan.setStatus("未开始");
        plan.setRemark("果树间作大豆");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(2).getId()); // 玉米
        plan.setPlotId(plots.get(8).getId()); // 宁津一号田
        plan.setPlantingDate(today.minusWeeks(2));
        plan.setExpectedHarvestDate(today.minusWeeks(2).plusDays(120));
        plan.setStatus("进行中");
        plan.setRemark("有机蔬菜基地轮作玉米");
        plantingPlanMapper.insert(plan);
        
        plan = new PlantingPlan();
        plan.setCropId(crops.get(0).getId()); // 小麦
        plan.setPlotId(plots.get(7).getId()); // 乐陵一号田
        plan.setPlantingDate(today.plusWeeks(12));
        plan.setExpectedHarvestDate(today.plusWeeks(12).plusDays(220));
        plan.setStatus("未开始");
        plan.setRemark("红枣基地间作小麦");
        plantingPlanMapper.insert(plan);
        
        log.info("种植计划数据初始化完成,共插入20条记录");
    }
    
    /**
     * 初始化物候期记录数据
     */
    private void initPhenologyRecordData() {
        log.info("开始初始化物候期记录数据...");
        
        // 强制重新初始化物候期记录数据
        try {
            jdbcTemplate.execute("DELETE FROM phenology_record");
            log.info("清空现有物候期记录数据");
        } catch (Exception e) {
            log.error("清空物候期记录数据失败: {}", e.getMessage());
        }
        
        LocalDate today = LocalDate.now();
        
        // 获取种植计划数据
        List<PlantingPlan> plans = plantingPlanMapper.selectList(null);
        
        if (plans.isEmpty()) {
            log.warn("种植计划数据为空,跳过物候期记录初始化");
            return;
        }
        
        // 创建真实的物候期记录
        PhenologyRecord record;
        
        // 找到对应的种植计划（通过作物和地块匹配）
        // plans.get(0) = 小麦-平原一号田 (id=13)
        // plans.get(5) = 玉米-平原二号田 (id=18)
        // plans.get(10) = 马铃薯-禹城二号田 (id=23)
        // plans.get(11) = 马铃薯-乐陵一号田 (id=24)
        // plans.get(8) = 大豆-禹城一号田 (id=21)
        // plans.get(16) = 玉米-宁津一号田 (id=29)
        // plans.get(17) = 小麦-乐陵一号田 (id=30)
        
        // 1. 小麦物候期记录（春季小麦）- 平原一号田
        if (plans.size() > 0) {
            record = new PhenologyRecord();
            record.setPlanId(plans.get(0).getId()); // 平原一号田种植小麦 (id=13)
            record.setPhenologyName("播种期");
            record.setRecordDate(today.minusDays(15));
            record.setDescription("春季小麦播种完成，播种深度3-4cm，行距20cm，播种量180kg/公顷");
            record.setEnvironmentalData("{\"temperature\":15,\"humidity\":65,\"soilMoisture\":70,\"weather\":\"晴\"}");
            phenologyRecordMapper.insert(record);
            
            record = new PhenologyRecord();
            record.setPlanId(plans.get(0).getId());
            record.setPhenologyName("出苗期");
            record.setRecordDate(today.minusDays(7));
            record.setDescription("小麦出苗整齐，出苗率达到95%，苗高8-10cm，叶片3-4片");
            record.setEnvironmentalData("{\"temperature\":18,\"humidity\":60,\"soilMoisture\":68,\"weather\":\"多云\"}");
            phenologyRecordMapper.insert(record);
            
            record = new PhenologyRecord();
            record.setPlanId(plans.get(0).getId());
            record.setPhenologyName("分蘖期");
            record.setRecordDate(today);
            record.setDescription("小麦进入分蘖期，平均分蘖数3-4个，植株生长健壮，叶色浓绿");
            record.setEnvironmentalData("{\"temperature\":20,\"humidity\":55,\"soilMoisture\":65,\"weather\":\"晴\"}");
            phenologyRecordMapper.insert(record);
        }
        
        // 2. 玉米物候期记录 - 平原二号田
        if (plans.size() > 5) {
            record = new PhenologyRecord();
            record.setPlanId(plans.get(5).getId()); // 平原二号田种植玉米 (id=18)
            record.setPhenologyName("播种期");
            record.setRecordDate(today.minusDays(10));
            record.setDescription("春季玉米播种完成，品种郑单958，播种深度5cm，株距30cm");
            record.setEnvironmentalData("{\"temperature\":17,\"humidity\":58,\"soilMoisture\":72,\"weather\":\"晴\"}");
            phenologyRecordMapper.insert(record);
            
            record = new PhenologyRecord();
            record.setPlanId(plans.get(5).getId());
            record.setPhenologyName("出苗期");
            record.setRecordDate(today.minusDays(5));
            record.setDescription("玉米出苗整齐，出苗率92%，苗高12-15cm，叶片4-5片");
            record.setEnvironmentalData("{\"temperature\":19,\"humidity\":62,\"soilMoisture\":70,\"weather\":\"多云\"}");
            phenologyRecordMapper.insert(record);
        }
        
        // 3. 水稻物候期记录 - 平原三号田
        if (plans.size() > 3) {
            record = new PhenologyRecord();
            record.setPlanId(plans.get(3).getId()); // 平原三号田种植水稻 (id=16)
            record.setPhenologyName("播种期");
            record.setRecordDate(today.minusDays(3));
            record.setDescription("水稻秧田播种完成，品种杂交水稻，播种量30kg/亩，秧田管理良好");
            record.setEnvironmentalData("{\"temperature\":22,\"humidity\":75,\"soilMoisture\":80,\"weather\":\"阴\"}");
            phenologyRecordMapper.insert(record);
        }
        
        // 4. 马铃薯物候期记录 - 禹城二号田
        if (plans.size() > 10) {
            record = new PhenologyRecord();
            record.setPlanId(plans.get(10).getId()); // 禹城二号田种植马铃薯 (id=23)
            record.setPhenologyName("播种期");
            record.setRecordDate(today.minusDays(20));
            record.setDescription("马铃薯播种完成，品种费乌瑞它，切块播种，行距70cm，株距25cm");
            record.setEnvironmentalData("{\"temperature\":14,\"humidity\":52,\"soilMoisture\":60,\"weather\":\"晴\"}");
            phenologyRecordMapper.insert(record);
        }
        
        // 马铃薯物候期记录 - 乐陵一号田
        if (plans.size() > 11) {
            record = new PhenologyRecord();
            record.setPlanId(plans.get(11).getId()); // 乐陵一号田种植马铃薯 (id=24)
            record.setPhenologyName("出苗期");
            record.setRecordDate(today.minusDays(12));
            record.setDescription("马铃薯出苗整齐，出苗率90%，苗高15-18cm，叶片展开良好");
            record.setEnvironmentalData("{\"temperature\":16,\"humidity\":55,\"soilMoisture\":62,\"weather\":\"多云\"}");
            phenologyRecordMapper.insert(record);
            
            record = new PhenologyRecord();
            record.setPlanId(plans.get(11).getId());
            record.setPhenologyName("现蕾期");
            record.setRecordDate(today.minusDays(5));
            record.setDescription("马铃薯进入现蕾期，植株生长旺盛，开始形成块茎");
            record.setEnvironmentalData("{\"temperature\":18,\"humidity\":58,\"soilMoisture\":65,\"weather\":\"晴\"}");
            phenologyRecordMapper.insert(record);
        }
        
        // 5. 大豆物候期记录 - 禹城一号田
        if (plans.size() > 8) {
            record = new PhenologyRecord();
            record.setPlanId(plans.get(8).getId()); // 禹城一号田种植大豆 (id=21)
            record.setPhenologyName("播种期");
            record.setRecordDate(today.minusDays(8));
            record.setDescription("大豆播种完成，品种黑农44，播种深度3-4cm，行距50cm");
            record.setEnvironmentalData("{\"temperature\":16,\"humidity\":60,\"soilMoisture\":68,\"weather\":\"多云\"}");
            phenologyRecordMapper.insert(record);
            
            record = new PhenologyRecord();
            record.setPlanId(plans.get(8).getId());
            record.setPhenologyName("出苗期");
            record.setRecordDate(today.minusDays(3));
            record.setDescription("大豆出苗整齐，出苗率88%，苗高10-12cm，子叶完全展开");
            record.setEnvironmentalData("{\"temperature\":18,\"humidity\":62,\"soilMoisture\":70,\"weather\":\"晴\"}");
            phenologyRecordMapper.insert(record);
        }
        
        // 6. 小麦成熟期记录 - 齐河一号田（已完成）
        if (plans.size() > 1) {
            record = new PhenologyRecord();
            record.setPlanId(plans.get(1).getId()); // 齐河一号田种植小麦 (id=14)
            record.setPhenologyName("成熟期");
            record.setRecordDate(today.minusDays(30));
            record.setDescription("小麦进入成熟期，籽粒饱满，含水量降至18%以下，准备收获");
            record.setEnvironmentalData("{\"temperature\":25,\"humidity\":45,\"soilMoisture\":50,\"weather\":\"晴\"}");
            phenologyRecordMapper.insert(record);
            
            record = new PhenologyRecord();
            record.setPlanId(plans.get(1).getId());
            record.setPhenologyName("收获期");
            record.setRecordDate(today.minusDays(25));
            record.setDescription("小麦收获完成，亩产550公斤，品质优良，籽粒饱满");
            record.setEnvironmentalData("{\"temperature\":26,\"humidity\":42,\"soilMoisture\":48,\"weather\":\"晴\"}");
            phenologyRecordMapper.insert(record);
        }
        
        // 7. 玉米拔节期记录 - 禹城一号田（已完成）
        if (plans.size() > 7) {
            record = new PhenologyRecord();
            record.setPlanId(plans.get(7).getId()); // 禹城一号田种植玉米 (id=20)
            record.setPhenologyName("拔节期");
            record.setRecordDate(today.minusDays(45));
            record.setDescription("玉米进入拔节期，株高80-100cm，茎秆粗壮，叶片深绿");
            record.setEnvironmentalData("{\"temperature\":24,\"humidity\":55,\"soilMoisture\":60,\"weather\":\"多云\"}");
            phenologyRecordMapper.insert(record);
            
            record = new PhenologyRecord();
            record.setPlanId(plans.get(7).getId());
            record.setPhenologyName("抽穗期");
            record.setRecordDate(today.minusDays(35));
            record.setDescription("玉米抽穗整齐，雄穗抽出，雌穗开始吐丝，授粉良好");
            record.setEnvironmentalData("{\"temperature\":26,\"humidity\":58,\"soilMoisture\":62,\"weather\":\"晴\"}");
            phenologyRecordMapper.insert(record);
        }
        
        // 8. 水稻分蘖期记录 - 齐河二号田
        if (plans.size() > 4) {
            record = new PhenologyRecord();
            record.setPlanId(plans.get(4).getId()); // 齐河二号田种植水稻 (id=17)
            record.setPhenologyName("分蘖期");
            record.setRecordDate(today.minusDays(60));
            record.setDescription("水稻分蘖旺盛，有效分蘖数达到12-15个，植株生长健壮");
            record.setEnvironmentalData("{\"temperature\":28,\"humidity\":70,\"soilMoisture\":75,\"weather\":\"阴\"}");
            phenologyRecordMapper.insert(record);
        }
        
        log.info("物候期记录数据初始化完成,共插入15条记录");
    }
    
    /**
     * 初始化病虫害知识库数据
     */
    private void initPestKnowledgeData() {
        log.info("开始初始化病虫害知识库数据...");
        
        long knowledgeCount = pestKnowledgeMapper.selectCount(null);
        if (knowledgeCount > 0) {
            log.info("病虫害知识库数据已存在,跳过初始化");
            return;
        }
        
        // 创建真实的病虫害知识库
        PestKnowledge knowledge;
        
        // 1. 小麦赤霉病
        knowledge = new PestKnowledge();
        knowledge.setPestName("小麦赤霉病");
        knowledge.setPestType("真菌病害");
        knowledge.setAffectedCrops("小麦,大麦");
        knowledge.setSymptoms("穗部出现粉红色霉层，后期产生黑色子囊壳，籽粒皱缩干瘪");
        knowledge.setVisualFeatures("穗部粉红色霉层,黑色小颗粒,籽粒发瘪");
        knowledge.setSeason("春季,初夏");
        knowledge.setSeverity("严重");
        knowledge.setTreatmentMethods("发病初期喷施多菌灵、甲基硫菌灵等杀菌剂，严重时需及时收割");
        knowledge.setPreventionMethods("选用抗病品种，合理密植，及时排水，避免偏施氮肥");
        knowledge.setImagePatterns("穗部粉红色,霉层覆盖,黑色颗粒");
        knowledge.setConfidenceScore(new BigDecimal("92.50"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 2. 小麦白粉病
        knowledge = new PestKnowledge();
        knowledge.setPestName("小麦白粉病");
        knowledge.setPestType("真菌病害");
        knowledge.setAffectedCrops("小麦");
        knowledge.setSymptoms("叶片表面出现白色粉状霉斑，后期霉斑上产生黑色小点");
        knowledge.setVisualFeatures("白色粉状霉斑,叶片背面霉斑,黑色小点");
        knowledge.setSeason("春季");
        knowledge.setSeverity("中等");
        knowledge.setTreatmentMethods("发病初期喷施三唑类杀菌剂，如戊唑醇、腈菌唑");
        knowledge.setPreventionMethods("选用抗病品种，合理施肥，及时清除病残体");
        knowledge.setImagePatterns("白色粉状物,叶片霉斑,圆形斑点");
        knowledge.setConfidenceScore(new BigDecimal("88.30"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 3. 玉米大斑病
        knowledge = new PestKnowledge();
        knowledge.setPestName("玉米大斑病");
        knowledge.setPestType("真菌病害");
        knowledge.setAffectedCrops("玉米");
        knowledge.setSymptoms("叶片出现长梭形病斑，灰褐色，中央颜色较浅，边缘深褐色");
        knowledge.setVisualFeatures("长梭形病斑,灰褐色,边缘深褐色");
        knowledge.setSeason("夏季,秋季");
        knowledge.setSeverity("严重");
        knowledge.setTreatmentMethods("发病初期喷施代森锰锌、百菌清等保护性杀菌剂");
        knowledge.setPreventionMethods("选用抗病品种，合理密植，增施有机肥");
        knowledge.setImagePatterns("长条形病斑,灰褐色斑,叶脉平行");
        knowledge.setConfidenceScore(new BigDecimal("90.20"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 4. 玉米小斑病
        knowledge = new PestKnowledge();
        knowledge.setPestName("玉米小斑病");
        knowledge.setPestType("真菌病害");
        knowledge.setAffectedCrops("玉米");
        knowledge.setSymptoms("叶片出现椭圆形或近圆形病斑，黄褐色，边缘深褐色");
        knowledge.setVisualFeatures("椭圆形病斑,黄褐色,同心轮纹");
        knowledge.setSeason("夏季");
        knowledge.setSeverity("中等");
        knowledge.setTreatmentMethods("发病初期喷施苯醚甲环唑、嘧菌酯等杀菌剂");
        knowledge.setPreventionMethods("轮作倒茬，清除病残体，加强田间管理");
        knowledge.setImagePatterns("小圆形病斑,黄褐色,同心轮纹");
        knowledge.setConfidenceScore(new BigDecimal("85.70"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 5. 水稻稻瘟病
        knowledge = new PestKnowledge();
        knowledge.setPestName("水稻稻瘟病");
        knowledge.setPestType("真菌病害");
        knowledge.setAffectedCrops("水稻");
        knowledge.setSymptoms("叶片出现梭形病斑，中央灰白色，边缘褐色，严重时叶片枯死");
        knowledge.setVisualFeatures("梭形病斑,灰白色中心,褐色边缘");
        knowledge.setSeason("夏季");
        knowledge.setSeverity("严重");
        knowledge.setTreatmentMethods("发病初期喷施三环唑、稻瘟灵等专用杀菌剂");
        knowledge.setPreventionMethods("选用抗病品种，合理施肥，浅水勤灌");
        knowledge.setImagePatterns("梭形病斑,叶尖枯死,灰白色中心");
        knowledge.setConfidenceScore(new BigDecimal("94.10"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 6. 水稻纹枯病
        knowledge = new PestKnowledge();
        knowledge.setPestName("水稻纹枯病");
        knowledge.setPestType("真菌病害");
        knowledge.setAffectedCrops("水稻");
        knowledge.setSymptoms("叶鞘出现椭圆形水渍状病斑，后期云纹状，边缘褐色，中央灰白色");
        knowledge.setVisualFeatures("云纹状病斑,褐色边缘,灰白色中心");
        knowledge.setSeason("夏季");
        knowledge.setSeverity("中等");
        knowledge.setTreatmentMethods("发病初期喷施井冈霉素、己唑醇等杀菌剂");
        knowledge.setPreventionMethods("合理密植，浅水勤灌，及时晒田");
        knowledge.setImagePatterns("云纹状,病斑连片,叶鞘发病");
        knowledge.setConfidenceScore(new BigDecimal("87.40"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 7. 马铃薯晚疫病
        knowledge = new PestKnowledge();
        knowledge.setPestName("马铃薯晚疫病");
        knowledge.setPestType("真菌病害");
        knowledge.setAffectedCrops("马铃薯,番茄");
        knowledge.setSymptoms("叶片出现水渍状病斑，边缘不明显，潮湿时病斑上产生白色霉层");
        knowledge.setVisualFeatures("水渍状病斑,白色霉层,叶尖枯死");
        knowledge.setSeason("春季,秋季");
        knowledge.setSeverity("严重");
        knowledge.setTreatmentMethods("发病初期喷施甲霜灵锰锌、烯酰吗啉等杀菌剂");
        knowledge.setPreventionMethods("选用抗病品种，避免连作，及时排水");
        knowledge.setImagePatterns("水渍状斑点,白色霉粉,叶片腐烂");
        knowledge.setConfidenceScore(new BigDecimal("93.80"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 8. 马铃薯早疫病
        knowledge = new PestKnowledge();
        knowledge.setPestName("马铃薯早疫病");
        knowledge.setPestType("真菌病害");
        knowledge.setAffectedCrops("马铃薯,番茄");
        knowledge.setSymptoms("叶片出现圆形或不规则形病斑，黑褐色，有同心轮纹");
        knowledge.setVisualFeatures("同心轮纹,黑褐色病斑,圆形斑点");
        knowledge.setSeason("春季,夏季");
        knowledge.setSeverity("中等");
        knowledge.setTreatmentMethods("发病初期喷施代森锰锌、百菌清等保护性杀菌剂");
        knowledge.setPreventionMethods("轮作倒茬，增施有机肥，及时清除病残体");
        knowledge.setImagePatterns("同心轮纹,黑褐色斑点,叶片枯死");
        knowledge.setConfidenceScore(new BigDecimal("89.60"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 9. 大豆根腐病
        knowledge = new PestKnowledge();
        knowledge.setPestName("大豆根腐病");
        knowledge.setPestType("真菌病害");
        knowledge.setAffectedCrops("大豆");
        knowledge.setSymptoms("根部出现褐色病斑，根部腐烂，植株萎蔫，叶片发黄");
        knowledge.setVisualFeatures("根部褐色,根部腐烂,植株萎蔫");
        knowledge.setSeason("苗期,生长期");
        knowledge.setSeverity("严重");
        knowledge.setTreatmentMethods("播种前进行种子处理，发病初期灌根防治");
        knowledge.setPreventionMethods("选用抗病品种，合理轮作，避免低洼地种植");
        knowledge.setImagePatterns("根部腐烂,褐色斑点,植株矮小");
        knowledge.setConfidenceScore(new BigDecimal("86.90"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 10. 蚜虫类害虫
        knowledge = new PestKnowledge();
        knowledge.setPestName("蚜虫");
        knowledge.setPestType("昆虫害虫");
        knowledge.setAffectedCrops("小麦,玉米,水稻,大豆,马铃薯");
        knowledge.setSymptoms("成虫和若虫群集在嫩叶、嫩茎、花蕾上吸食汁液，导致叶片卷曲、发黄");
        knowledge.setVisualFeatures("小型昆虫,绿色或黄色,群集为害");
        knowledge.setSeason("春季,夏季");
        knowledge.setSeverity("中等");
        knowledge.setTreatmentMethods("喷施吡虫啉、噻虫嗪等杀虫剂，保护天敌");
        knowledge.setPreventionMethods("清除田间杂草，保护天敌，黄色粘板诱杀");
        knowledge.setImagePatterns("小虫群集,叶片卷曲,蜜露痕迹");
        knowledge.setConfidenceScore(new BigDecimal("91.30"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 11. 粘虫
        knowledge = new PestKnowledge();
        knowledge.setPestName("粘虫");
        knowledge.setPestType("昆虫害虫");
        knowledge.setAffectedCrops("小麦,玉米,水稻");
        knowledge.setSymptoms("幼虫咬食叶片，造成缺刻，严重时仅剩叶脉");
        knowledge.setVisualFeatures("幼虫体色多变,头部有八字形纹,夜间为害");
        knowledge.setSeason("夏季,秋季");
        knowledge.setSeverity("严重");
        knowledge.setTreatmentMethods("幼虫低龄期喷施氯虫苯甲酰胺、甲维盐等杀虫剂");
        knowledge.setPreventionMethods("成虫期使用性诱剂诱杀，幼虫期及时防治");
        knowledge.setImagePatterns("叶片缺刻,幼虫为害,粪便痕迹");
        knowledge.setConfidenceScore(new BigDecimal("88.90"));
        pestKnowledgeMapper.insert(knowledge);
        
        // 12. 稻飞虱
        knowledge = new PestKnowledge();
        knowledge.setPestName("稻飞虱");
        knowledge.setPestType("昆虫害虫");
        knowledge.setAffectedCrops("水稻");
        knowledge.setSymptoms("成虫和若虫群集在稻株基部吸食汁液，导致稻株枯死");
        knowledge.setVisualFeatures("小型飞虫,褐色或灰白色,群集基部");
        knowledge.setSeason("夏季,秋季");
        knowledge.setSeverity("严重");
        knowledge.setTreatmentMethods("喷施噻嗪酮、吡蚜酮等专用杀虫剂");
        knowledge.setPreventionMethods("选用抗虫品种，合理施肥，保护天敌");
        knowledge.setImagePatterns("飞虫群集,基部为害,虫粪堆积");
        knowledge.setConfidenceScore(new BigDecimal("92.70"));
        pestKnowledgeMapper.insert(knowledge);
        
        log.info("病虫害知识库数据初始化完成,共插入12条记录");
    }
    
    /**
     * 初始化采收记录数据
     */
    private void initHarvestRecordData() {
        log.info("开始初始化采收记录数据...");
        
        // 强制重新初始化采收记录数据
        try {
            jdbcTemplate.execute("DELETE FROM harvest_record");
            log.info("清空现有采收记录数据");
        } catch (Exception e) {
            log.error("清空采收记录数据失败: {}", e.getMessage());
        }
        
        long harvestCount = harvestRecordMapper.selectCount(null);
        if (harvestCount > 0) {
            log.info("采收记录数据已存在,跳过初始化");
            return;
        }
        
        LocalDate today = LocalDate.now();
        
        // 获取种植计划数据
        List<PlantingPlan> plans = plantingPlanMapper.selectList(null);
        
        if (plans.isEmpty()) {
            log.warn("种植计划数据为空,跳过采收记录初始化");
            return;
        }
        
        // 创建真实的采收记录
        HarvestRecord record;
        
        // 1. 小麦采收记录（已完成）
        record = new HarvestRecord();
        record.setPlanId(plans.get(1).getId()); // 陵城一号田种植小麦（已完成）
        record.setHarvestDate(today.minusDays(25));
        record.setHarvestQuantity(new BigDecimal("550.00"));
        record.setQualityGrade("优质");
        record.setMoistureContent(new BigDecimal("12.50"));
        record.setProteinContent(new BigDecimal("14.20"));
        record.setHarvestArea(new BigDecimal("8900.00"));
        record.setRemark("优质小麦品种，籽粒饱满，品质优良，达到一等品标准");
        harvestRecordMapper.insert(record);
        
        // 2. 玉米采收记录（已完成）
        record = new HarvestRecord();
        record.setPlanId(plans.get(10).getId()); // 禹城一号田种植玉米（已完成）
        record.setHarvestDate(today.minusDays(10));
        record.setHarvestQuantity(new BigDecimal("720.00"));
        record.setQualityGrade("良好");
        record.setMoistureContent(new BigDecimal("13.80"));
        record.setProteinContent(new BigDecimal("9.50"));
        record.setHarvestArea(new BigDecimal("9200.00"));
        record.setRemark("玉米品质良好，颗粒饱满，含水率适中");
        harvestRecordMapper.insert(record);
        
        // 3. 马铃薯采收记录（已完成）
        record = new HarvestRecord();
        record.setPlanId(plans.get(6).getId()); // 宁津一号田种植马铃薯（已完成）
        record.setHarvestDate(today.minusDays(5));
        record.setHarvestQuantity(new BigDecimal("2800.00"));
        record.setQualityGrade("普通");
        record.setMoistureContent(new BigDecimal("78.50"));
        record.setProteinContent(new BigDecimal("2.10"));
        record.setHarvestArea(new BigDecimal("7300.00"));
        record.setRemark("马铃薯产量一般，个头均匀，适合市场销售");
        harvestRecordMapper.insert(record);
        
        // 4. 大豆采收记录（已完成）
        record = new HarvestRecord();
        record.setPlanId(plans.get(9).getId()); // 齐河二号田种植水稻（已完成）
        record.setHarvestDate(today.minusDays(15));
        record.setHarvestQuantity(new BigDecimal("380.00"));
        record.setQualityGrade("优质");
        record.setMoistureContent(new BigDecimal("11.20"));
        record.setProteinContent(new BigDecimal("42.50"));
        record.setHarvestArea(new BigDecimal("6400.00"));
        record.setRemark("大豆品质优良，蛋白质含量高，达到一等品标准");
        harvestRecordMapper.insert(record);
        
        log.info("采收记录数据初始化完成,共插入4条记录");
    }
    
    /**
     * 初始化产量预估数据
     */
    private void initYieldPredictionData() {
        log.info("开始初始化产量预估数据...");
        
        // 强制重新初始化产量预估数据
        try {
            jdbcTemplate.execute("DELETE FROM yield_prediction");
            log.info("清空现有产量预估数据");
        } catch (Exception e) {
            log.error("清空产量预估数据失败: {}", e.getMessage());
        }
        
        LocalDate today = LocalDate.now();
        
        // 获取种植计划数据
        List<PlantingPlan> plans = plantingPlanMapper.selectList(null);
        
        if (plans.isEmpty()) {
            log.warn("种植计划数据为空,跳过产量预估初始化");
            return;
        }
        
        // 为所有种植计划创建产量预估数据
        YieldPrediction prediction;
        int count = 0;
        
        // 预测方法数组
        String[] methods = {"历史数据预测", "生长模型预测", "机器学习预测", "专家经验预测"};
        
        for (int i = 0; i < plans.size(); i++) {
            PlantingPlan plan = plans.get(i);
            prediction = new YieldPrediction();
            prediction.setPlanId(plan.getId());
            prediction.setPredictionDate(today);
            
            // 根据索引循环使用不同的预测方法
            String method = methods[i % methods.length];
            prediction.setPredictionMethod(method);
            
            // 根据作物类型设置不同的产量预估
            Long cropId = plan.getCropId();
            if (cropId == 1) { // 小麦
                prediction.setPredictedYield(new BigDecimal("520.00"));
                prediction.setConfidenceLevel("高");
                prediction.setGrowthStage("分蘖期");
                prediction.setWeatherImpact("天气条件良好，有利于小麦生长");
                prediction.setFertilizerImpact("施肥充足，营养供给良好");
                prediction.setWaterImpact("灌溉条件良好，水分充足");
                prediction.setRemark("预计亩产520公斤，优质小麦品种");
            } else if (cropId == 2) { // 水稻
                prediction.setPredictedYield(new BigDecimal("620.00"));
                prediction.setConfidenceLevel("高");
                prediction.setGrowthStage("播种期");
                prediction.setWeatherImpact("预计气候条件适宜");
                prediction.setFertilizerImpact("土壤肥力良好");
                prediction.setWaterImpact("水源充足，灌溉条件好");
                prediction.setRemark("预计亩产620公斤，杂交水稻品种优势明显");
            } else if (cropId == 3) { // 玉米
                prediction.setPredictedYield(new BigDecimal("680.00"));
                prediction.setConfidenceLevel("中");
                prediction.setGrowthStage("出苗期");
                prediction.setWeatherImpact("气温适宜，光照充足");
                prediction.setFertilizerImpact("基肥充足，需追肥");
                prediction.setWaterImpact("土壤湿度适中");
                prediction.setRemark("预计亩产680公斤，需注意病虫害防治");
            } else if (cropId == 4) { // 大豆
                prediction.setPredictedYield(new BigDecimal("350.00"));
                prediction.setConfidenceLevel("中");
                prediction.setGrowthStage("出苗期");
                prediction.setWeatherImpact("气温适宜，降雨适中");
                prediction.setFertilizerImpact("氮磷钾配比合理");
                prediction.setWaterImpact("排水良好，无积水");
                prediction.setRemark("预计亩产350公斤，需注意后期管理");
            } else if (cropId == 5) { // 马铃薯
                prediction.setPredictedYield(new BigDecimal("2500.00"));
                prediction.setConfidenceLevel("高");
                prediction.setGrowthStage("现蕾期");
                prediction.setWeatherImpact("温度适宜，光照充足");
                prediction.setFertilizerImpact("钾肥充足，有利于块茎形成");
                prediction.setWaterImpact("土壤湿度适中");
                prediction.setRemark("预计亩产2500公斤，块茎品质优良");
            } else {
                prediction.setPredictedYield(new BigDecimal("500.00"));
                prediction.setConfidenceLevel("中");
                prediction.setGrowthStage("生长期");
                prediction.setWeatherImpact("气候条件正常");
                prediction.setFertilizerImpact("肥料供应充足");
                prediction.setWaterImpact("水分供应正常");
                prediction.setRemark("预计亩产500公斤");
            }
            
            yieldPredictionMapper.insert(prediction);
            count++;
        }
        
        log.info("产量预估数据初始化完成,共插入{}条记录", count);
    }
}
