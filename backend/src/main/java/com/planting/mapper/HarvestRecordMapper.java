package com.planting.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.planting.entity.HarvestRecord;
import org.apache.ibatis.annotations.Mapper;

/**
 * 采收记录Mapper接口
 */
@Mapper
public interface HarvestRecordMapper extends BaseMapper<HarvestRecord> {
}
