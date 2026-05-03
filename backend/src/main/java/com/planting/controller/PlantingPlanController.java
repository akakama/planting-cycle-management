package com.planting.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.planting.common.ApiResponse;
import com.planting.dto.PlantingPlanDTO;
import com.planting.entity.Crop;
import com.planting.entity.PlantingPlan;
import com.planting.entity.Plot;
import com.planting.entity.YieldPrediction;
import com.planting.mapper.CropMapper;
import com.planting.mapper.PlotMapper;
import com.planting.mapper.YieldPredictionMapper;
import com.planting.service.PlantingPlanService;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * 种植计划管理控制器
 */
@Slf4j
@RestController
@RequestMapping("/planting-plans")
public class PlantingPlanController {

    @Autowired
    private PlantingPlanService plantingPlanService;

    @Autowired
    private CropMapper cropMapper;

    @Autowired
    private PlotMapper plotMapper;

    @Autowired
    private YieldPredictionMapper yieldPredictionMapper;

    /**
     * 获取种植计划列表
     */
    @GetMapping
    @PreAuthorize("hasAuthority('plan:read')")
    public ApiResponse<Page<PlantingPlanDTO>> listPlantingPlans(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) Long cropId,
            @RequestParam(required = false) Long plotId) {

        Page<PlantingPlan> planPage = plantingPlanService.listPlantingPlans(page, size, status, cropId, plotId);
        
        // 转换为DTO并填充关联信息
        Page<PlantingPlanDTO> dtoPage = new Page<>();
        dtoPage.setCurrent(planPage.getCurrent());
        dtoPage.setSize(planPage.getSize());
        dtoPage.setTotal(planPage.getTotal());
        dtoPage.setPages(planPage.getPages());
        
        List<PlantingPlan> plans = planPage.getRecords();
        if (!plans.isEmpty()) {
            // 批量获取作物信息
            List<Long> cropIds = plans.stream().map(PlantingPlan::getCropId).distinct().collect(Collectors.toList());
            Map<Long, String> cropMap = cropMapper.selectBatchIds(cropIds).stream()
                    .collect(Collectors.toMap(Crop::getId, Crop::getName));
            
            // 批量获取地块信息
            List<Long> plotIds = plans.stream().map(PlantingPlan::getPlotId).distinct().collect(Collectors.toList());
            Map<Long, Plot> plotMap = plotMapper.selectBatchIds(plotIds).stream()
                    .collect(Collectors.toMap(Plot::getId, p -> p));
            
            // 批量获取产量预估信息
            List<Long> planIds = plans.stream().map(PlantingPlan::getId).collect(Collectors.toList());
            Map<Long, YieldPrediction> yieldMap = yieldPredictionMapper.selectList(
                    new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<YieldPrediction>()
                            .in(YieldPrediction::getPlanId, planIds)
            ).stream().collect(Collectors.toMap(YieldPrediction::getPlanId, y -> y, (a, b) -> a));
            
            // 转换为DTO
            List<PlantingPlanDTO> dtoList = plans.stream().map(plan -> {
                PlantingPlanDTO dto = new PlantingPlanDTO();
                org.springframework.beans.BeanUtils.copyProperties(plan, dto);
                
                // 填充作物名称
                dto.setCropName(cropMap.get(plan.getCropId()));
                
                // 填充地块信息
                Plot plot = plotMap.get(plan.getPlotId());
                if (plot != null) {
                    dto.setPlotName(plot.getName());
                    // 面积转换：平方米转亩（1亩=666.67平方米）
                    if (plot.getArea() != null) {
                        dto.setPlantingArea(plot.getArea().divide(new java.math.BigDecimal("666.67"), 2, java.math.RoundingMode.HALF_UP));
                    }
                }
                
                // 填充预计产量
                YieldPrediction yield = yieldMap.get(plan.getId());
                if (yield != null) {
                    dto.setExpectedYield(yield.getPredictedYield());
                }
                
                return dto;
            }).collect(Collectors.toList());
            
            dtoPage.setRecords(dtoList);
        }
        
        return ApiResponse.success(dtoPage);
    }

    /**
     * 获取种植计划详情
     */
    @GetMapping("/{id}")
    @PreAuthorize("hasAuthority('plan:read')")
    public ApiResponse<PlantingPlan> getPlantingPlanById(
            @PathVariable Long id) {

        PlantingPlan plan = plantingPlanService.getPlantingPlanById(id);
        return ApiResponse.success(plan);
    }

    /**
     * 添加种植计划
     */
    @PostMapping
    @PreAuthorize("hasAuthority('plan:write')")
    public ApiResponse<PlantingPlan> createPlantingPlan(
            @Validated @RequestBody PlantingPlan plan) {

        PlantingPlan createdPlan = plantingPlanService.createPlantingPlan(plan);
        return ApiResponse.success(createdPlan);
    }

    /**
     * 更新种植计划
     */
    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('plan:write')")
    public ApiResponse<PlantingPlan> updatePlantingPlan(
            @PathVariable Long id,
            @Validated @RequestBody PlantingPlan plan) {

        PlantingPlan updatedPlan = plantingPlanService.updatePlantingPlan(id, plan);
        return ApiResponse.success(updatedPlan);
    }

    /**
     * 删除种植计划
     */
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAuthority('plan:delete')")
    public ApiResponse<Void> deletePlantingPlan(
            @PathVariable Long id) {

        plantingPlanService.deletePlantingPlan(id);
        return ApiResponse.success("删除成功");
    }

    /**
     * 更新种植状态
     */
    @PutMapping("/{id}/status")
    @PreAuthorize("hasAuthority('plan:write')")
    public ApiResponse<Void> updateStatus(
            @PathVariable Long id,
            @RequestParam String status) {

        plantingPlanService.updateStatus(id, status);
        return ApiResponse.success("状态更新成功");
    }

    /**
     * AI查询种植计划（多条件查询）
     */
    @GetMapping("/ai/query")
    public ApiResponse<?> queryPlantingPlansForAI(
            @RequestParam(required = false) String cropName,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String date,
            @RequestParam(required = false) String startDate,
            @RequestParam(required = false) String endDate) {

        Page<PlantingPlan> plans = plantingPlanService.queryPlansForAI(cropName, status, date, startDate, endDate);
        return ApiResponse.success(plans);
    }
}
