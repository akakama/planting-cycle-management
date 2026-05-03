package com.planting.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.planting.entity.YieldPrediction;
import com.planting.exception.BusinessException;
import com.planting.mapper.YieldPredictionMapper;
import com.planting.service.YieldPredictionService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * 产量预估服务实现类
 */
@Slf4j
@Service
public class YieldPredictionServiceImpl extends ServiceImpl<YieldPredictionMapper, YieldPrediction>
        implements YieldPredictionService {

    @Override
    public Page<YieldPrediction> listYieldPredictions(Integer page, Integer size, Long planId) {
        Page<YieldPrediction> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<YieldPrediction> wrapper = new LambdaQueryWrapper<>();

        if (planId != null) {
            wrapper.eq(YieldPrediction::getPlanId, planId);
        }

        wrapper.orderByDesc(YieldPrediction::getPredictionDate);
        return page(pageParam, wrapper);
    }

    @Override
    public YieldPrediction createYieldPrediction(YieldPrediction prediction) {
        save(prediction);
        log.info("创建产量预估成功，预估ID: {}", prediction.getId());
        return prediction;
    }

    @Override
    public void deleteYieldPrediction(Long id) {
        YieldPrediction prediction = getById(id);
        if (prediction == null) {
            throw new BusinessException("产量预估不存在");
        }

        removeById(id);
        log.info("删除产量预估成功，预估ID: {}", id);
    }
}
