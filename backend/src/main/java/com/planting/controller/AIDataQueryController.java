package com.planting.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.planting.common.ApiResponse;
import com.planting.entity.*;
import com.planting.service.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * AI数据查询控制器
 * 提供统一的数据查询接口供AI服务调用
 */
@Slf4j
@RestController
@RequestMapping("/ai/data")
public class AIDataQueryController {

    @Autowired
    private PlotService plotService;

    @Autowired
    private CropService cropService;

    @Autowired
    private MaterialService materialService;

    @Autowired
    private HarvestService harvestService;

    /**
     * AI查询地块信息
     */
    @GetMapping("/plots")
    public ApiResponse<?> queryPlotsForAI(
            @RequestParam(required = false) String name) {
        Page<Plot> plots = plotService.queryPlotsForAI(name);
        return ApiResponse.success(plots);
    }

    /**
     * AI查询作物信息
     */
    @GetMapping("/crops")
    public ApiResponse<?> queryCropsForAI(
            @RequestParam(required = false) String name) {
        // 暂时返回空结果，后续实现
        return ApiResponse.success("功能开发中");
    }

    /**
     * AI查询农资信息
     */
    @GetMapping("/materials")
    public ApiResponse<?> queryMaterialsForAI(
            @RequestParam(required = false) String type,
            @RequestParam(required = false) String name) {
        // 暂时返回空结果，后续实现
        return ApiResponse.success("功能开发中");
    }

    /**
     * AI查询采收记录
     */
    @GetMapping("/harvest-records")
    public ApiResponse<?> queryHarvestRecordsForAI(
            @RequestParam(required = false) Long planId,
            @RequestParam(required = false) String startDate,
            @RequestParam(required = false) String endDate) {
        // 暂时返回空结果，后续实现
        return ApiResponse.success("功能开发中");
    }
}
