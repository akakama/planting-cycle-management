package com.planting.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.planting.entity.YieldPrediction;
import org.apache.ibatis.annotations.Mapper;

/**
 * 产量预估Mapper接口
 */
@Mapper
public interface YieldPredictionMapper extends BaseMapper<YieldPrediction> {
}
