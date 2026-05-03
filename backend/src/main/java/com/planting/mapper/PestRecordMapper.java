package com.planting.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.planting.entity.PestRecord;
import org.apache.ibatis.annotations.Mapper;

/**
 * 病虫害记录Mapper接口
 */
@Mapper
public interface PestRecordMapper extends BaseMapper<PestRecord> {
}
