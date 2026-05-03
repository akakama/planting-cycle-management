package com.planting.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.planting.entity.Plot;
import com.planting.exception.BusinessException;
import com.planting.mapper.PlotMapper;
import com.planting.service.PlotService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

/**
 * 地块服务实现类
 */
@Slf4j
@Service
public class PlotServiceImpl extends ServiceImpl<PlotMapper, Plot> implements PlotService {

    @Override
    // @Cacheable(value = "plot", key = "'list:' + #page + ':' + #size")
    public Page<Plot> listPlots(Integer page, Integer size) {
        Page<Plot> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<Plot> wrapper = new LambdaQueryWrapper<>();
        wrapper.orderByDesc(Plot::getCreateTime);
        return page(pageParam, wrapper);
    }

    @Override
    // @Cacheable(value = "plot", key = "#id")
    public Plot getPlotById(Long id) {
        Plot plot = getById(id);
        if (plot == null) {
            throw new BusinessException("地块不存在");
        }
        return plot;
    }

    @Override
    // @CacheEvict(value = "plot", allEntries = true)
    public Plot createPlot(Plot plot) {
        save(plot);
        log.info("创建地块成功，地块ID: {}, 地块名称: {}", plot.getId(), plot.getName());
        return plot;
    }

    @Override
    // @CacheEvict(value = "plot", allEntries = true)
    public Plot updatePlot(Long id, Plot plot) {
        Plot existingPlot = getById(id);
        if (existingPlot == null) {
            throw new BusinessException("地块不存在");
        }

        plot.setId(id);
        updateById(plot);
        log.info("更新地块成功，地块ID: {}", id);
        return plot;
    }

    @Override
    public Page<Plot> queryPlotsForAI(String name) {
        Page<Plot> pageParam = new Page<>(1, 20);
        LambdaQueryWrapper<Plot> wrapper = new LambdaQueryWrapper<>();
        
        if (name != null && !name.isEmpty()) {
            wrapper.like(Plot::getName, name);
        }
        
        wrapper.orderByDesc(Plot::getCreateTime);
        return page(pageParam, wrapper);
    }
}
