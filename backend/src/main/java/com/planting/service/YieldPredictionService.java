package com.planting.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.planting.entity.YieldPrediction;

/**
 * 产量预估服务接口
 */
public interface YieldPredictionService extends IService<YieldPrediction> {

    /**
     * 获取产量预估列表
     */
    Page<YieldPrediction> listYieldPredictions(Integer page, Integer size, Long planId);

    /**
     * 创建产量预估
     */
    YieldPrediction createYieldPrediction(YieldPrediction prediction);

    /**
     * 删除产量预估
     */
    void deleteYieldPrediction(Long id);
}
