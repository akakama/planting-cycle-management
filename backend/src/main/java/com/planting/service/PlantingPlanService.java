package com.planting.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.planting.entity.PlantingPlan;

import java.time.LocalDate;
import java.util.List;

/**
 * 种植计划服务接口
 */
public interface PlantingPlanService extends IService<PlantingPlan> {

    /**
     * 获取种植计划列表
     */
    Page<PlantingPlan> listPlantingPlans(Integer page, Integer size, String status, Long cropId, Long plotId);

    /**
     * 获取种植计划详情
     */
    PlantingPlan getPlantingPlanById(Long id);

    /**
     * 创建种植计划
     */
    PlantingPlan createPlantingPlan(PlantingPlan plan);

    /**
     * 更新种植计划
     */
    PlantingPlan updatePlantingPlan(Long id, PlantingPlan plan);

    /**
     * 删除种植计划
     */
    void deletePlantingPlan(Long id);

    /**
     * 更新种植状态
     */
    void updateStatus(Long id, String status);

    /**
     * 验证状态转换规则
     */
    boolean validateStatusTransition(String currentStatus, String newStatus);

    /**
     * 根据作物名称查询种植计划（供AI调用）
     */
    Page<PlantingPlan> queryPlansByCropName(String cropName);

    /**
     * AI查询种植计划（多条件查询）
     */
    Page<PlantingPlan> queryPlansForAI(String cropName, String status, String date, String startDate, String endDate);
}
