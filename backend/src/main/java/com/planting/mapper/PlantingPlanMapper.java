package com.planting.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.planting.entity.PlantingPlan;
import org.apache.ibatis.annotations.Mapper;

/**
 * 种植计划Mapper接口
 */
@Mapper
public interface PlantingPlanMapper extends BaseMapper<PlantingPlan> {
}
