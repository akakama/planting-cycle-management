package com.planting.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.planting.entity.PestKnowledge;
import org.apache.ibatis.annotations.Mapper;

/**
 * 病虫害知识库Mapper接口
 */
@Mapper
public interface PestKnowledgeMapper extends BaseMapper<PestKnowledge> {
}