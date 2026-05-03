package com.planting.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.planting.entity.Plot;

/**
 * 地块服务接口
 */
public interface PlotService extends IService<Plot> {

    /**
     * 获取地块列表
     */
    Page<Plot> listPlots(Integer page, Integer size);

    /**
     * 获取地块详情
     */
    Plot getPlotById(Long id);

    /**
     * 创建地块
     */
    Plot createPlot(Plot plot);

    /**
     * 更新地块
     */
    Plot updatePlot(Long id, Plot plot);

    /**
     * AI查询地块信息
     */
    Page<Plot> queryPlotsForAI(String name);
}
