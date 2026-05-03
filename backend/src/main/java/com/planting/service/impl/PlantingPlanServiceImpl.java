package com.planting.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.planting.entity.Crop;
import com.planting.entity.PlantingPlan;
import com.planting.exception.BusinessException;
import com.planting.mapper.CropMapper;
import com.planting.mapper.PlantingPlanMapper;
import com.planting.service.PlantingPlanService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.time.LocalDate;

/**
 * 种植计划服务实现类
 */
@Slf4j
@Service
public class PlantingPlanServiceImpl extends ServiceImpl<PlantingPlanMapper, PlantingPlan>
        implements PlantingPlanService {

    @Autowired
    private CropMapper cropMapper;

    @Override
    public Page<PlantingPlan> listPlantingPlans(Integer page, Integer size, String status, Long cropId, Long plotId) {
        Page<PlantingPlan> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<PlantingPlan> wrapper = new LambdaQueryWrapper<>();

        if (StringUtils.hasText(status)) {
            wrapper.eq(PlantingPlan::getStatus, status);
        }
        if (cropId != null) {
            wrapper.eq(PlantingPlan::getCropId, cropId);
        }
        if (plotId != null) {
            wrapper.eq(PlantingPlan::getPlotId, plotId);
        }

        wrapper.orderByAsc(PlantingPlan::getId);
        return page(pageParam, wrapper);
    }

    @Override
    public PlantingPlan getPlantingPlanById(Long id) {
        PlantingPlan plan = getById(id);
        if (plan == null) {
            throw new BusinessException("种植计划不存在");
        }
        return plan;
    }

    @Override
    public PlantingPlan createPlantingPlan(PlantingPlan plan) {
        // 设置默认状态
        if (plan.getStatus() == null) {
            plan.setStatus("未开始");
        }
        save(plan);
        log.info("创建种植计划成功，计划ID: {}", plan.getId());
        return plan;
    }

    @Override
    public PlantingPlan updatePlantingPlan(Long id, PlantingPlan plan) {
        PlantingPlan existingPlan = getById(id);
        if (existingPlan == null) {
            throw new BusinessException("种植计划不存在");
        }

        plan.setId(id);
        updateById(plan);
        log.info("更新种植计划成功，计划ID: {}", id);
        return plan;
    }

    @Override
    public void deletePlantingPlan(Long id) {
        PlantingPlan plan = getById(id);
        if (plan == null) {
            throw new BusinessException("种植计划不存在");
        }

        // 检查状态，已完成的计划不允许删除
        if ("已完成".equals(plan.getStatus())) {
            throw new BusinessException("已完成的种植计划不允许删除");
        }

        removeById(id);
        log.info("删除种植计划成功，计划ID: {}", id);
    }

    @Override
    public void updateStatus(Long id, String status) {
        PlantingPlan plan = getById(id);
        if (plan == null) {
            throw new BusinessException("种植计划不存在");
        }

        // 验证状态转换规则
        if (!validateStatusTransition(plan.getStatus(), status)) {
            throw new BusinessException("无效的状态转换");
        }

        plan.setStatus(status);
        updateById(plan);
        log.info("更新种植计划状态成功，计划ID: {}, 新状态: {}", id, status);
    }

    @Override
    public boolean validateStatusTransition(String currentStatus, String newStatus) {
        // 定义允许的状态转换规则
        if ("未开始".equals(currentStatus)) {
            return "进行中".equals(newStatus);
        } else if ("进行中".equals(currentStatus)) {
            return "已完成".equals(newStatus) || "未开始".equals(newStatus);
        } else if ("已完成".equals(currentStatus)) {
            return "进行中".equals(newStatus);
        }
        return false;
    }

    @Override
    public Page<PlantingPlan> queryPlansByCropName(String cropName) {
        // 根据作物名称查询作物ID
        Crop crop = cropMapper.selectByName(cropName);
        if (crop == null) {
            // 如果没有找到作物，返回空结果
            return new Page<>(1, 10);
        }

        // 根据作物ID查询种植计划
        Page<PlantingPlan> pageParam = new Page<>(1, 10);
        LambdaQueryWrapper<PlantingPlan> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(PlantingPlan::getCropId, crop.getId());
        wrapper.orderByDesc(PlantingPlan::getCreateTime);

        return page(pageParam, wrapper);
    }

    @Override
    public Page<PlantingPlan> queryPlansForAI(String cropName, String status, String date, String startDate, String endDate) {
        Page<PlantingPlan> pageParam = new Page<>(1, 20);
        LambdaQueryWrapper<PlantingPlan> wrapper = new LambdaQueryWrapper<>();

        // 按作物名称查询
        if (cropName != null && !cropName.isEmpty()) {
            Crop crop = cropMapper.selectByName(cropName);
            if (crop != null) {
                wrapper.eq(PlantingPlan::getCropId, crop.getId());
            }
        }

        // 按状态查询
        if (status != null && !status.isEmpty()) {
            wrapper.eq(PlantingPlan::getStatus, status);
        }

        // 按日期查询（查询某一天的计划）
        if (date != null && !date.isEmpty()) {
            try {
                LocalDate queryDate = LocalDate.parse(date);
                wrapper.eq(PlantingPlan::getPlantingDate, queryDate);
            } catch (Exception e) {
                log.warn("日期格式错误: {}", date);
            }
        }

        // 按日期范围查询
        if (startDate != null && !startDate.isEmpty() && endDate != null && !endDate.isEmpty()) {
            try {
                LocalDate start = LocalDate.parse(startDate);
                LocalDate end = LocalDate.parse(endDate);
                wrapper.between(PlantingPlan::getPlantingDate, start, end);
            } catch (Exception e) {
                log.warn("日期范围格式错误: {} - {}", startDate, endDate);
            }
        }

        wrapper.orderByDesc(PlantingPlan::getCreateTime);
        return page(pageParam, wrapper);
    }
}
