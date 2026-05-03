package com.planting.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.planting.common.ApiResponse;
import com.planting.entity.Plot;
import com.planting.service.PlotService;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

/**
 * 地块管理控制器
 */
@Slf4j
@RestController
@RequestMapping("/plots")
public class PlotController {

    @Autowired
    private PlotService plotService;

    /**
     * 获取地块列表
     */
    @GetMapping
    @PreAuthorize("hasAuthority('plot:read')")
    public ApiResponse<Page<Plot>> listPlots(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {

        try {
            Page<Plot> plotPage = plotService.listPlots(page, size);
            return ApiResponse.success(plotPage);
        } catch (Exception e) {
            log.error("获取地块列表失败", e);
            return ApiResponse.error("获取地块列表失败: " + e.getMessage());
        }
    }

    /**
     * 获取地块详情
     */
    @GetMapping("/{id}")
    @PreAuthorize("hasAuthority('plot:read')")
    public ApiResponse<Plot> getPlotById(
            @PathVariable Long id) {

        Plot plot = plotService.getPlotById(id);
        return ApiResponse.success(plot);
    }

    /**
     * 添加地块
     */
    @PostMapping
    @PreAuthorize("hasAuthority('plot:write')")
    public ApiResponse<Plot> createPlot(@Validated @RequestBody Plot plot) {
        Plot createdPlot = plotService.createPlot(plot);
        return ApiResponse.success(createdPlot);
    }

    /**
     * 更新地块
     */
    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('plot:write')")
    public ApiResponse<Plot> updatePlot(
            @PathVariable Long id,
            @Validated @RequestBody Plot plot) {

        Plot updatedPlot = plotService.updatePlot(id, plot);
        return ApiResponse.success(updatedPlot);
    }
}
