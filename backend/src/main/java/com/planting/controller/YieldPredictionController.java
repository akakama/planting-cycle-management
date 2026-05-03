package com.planting.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.planting.common.ApiResponse;
import com.planting.entity.YieldPrediction;
import com.planting.service.YieldPredictionService;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

/**
 * 产量预估管理控制器
 */
@Slf4j
@RestController
@RequestMapping("/yield-predictions")
public class YieldPredictionController {

    @Autowired
    private YieldPredictionService yieldPredictionService;

    /**
     * 获取产量预估列表
     */
    @GetMapping
    @PreAuthorize("hasAuthority('yield:read')")
    public ApiResponse<Page<YieldPrediction>> listYieldPredictions(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) Long planId) {

        Page<YieldPrediction> predictionPage = yieldPredictionService.listYieldPredictions(page, size, planId);
        return ApiResponse.success(predictionPage);
    }

    /**
     * 添加产量预估
     */
    @PostMapping
    @PreAuthorize("hasAuthority('yield:write')")
    public ApiResponse<YieldPrediction> createYieldPrediction(@RequestBody YieldPrediction prediction) {
        YieldPrediction createdPrediction = yieldPredictionService.createYieldPrediction(prediction);
        return ApiResponse.success(createdPrediction);
    }

    /**
     * 删除产量预估
     */
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAuthority('yield:write')")
    public ApiResponse<Void> deleteYieldPrediction(@PathVariable Long id) {
        yieldPredictionService.deleteYieldPrediction(id);
        return ApiResponse.success("删除成功");
    }
}
