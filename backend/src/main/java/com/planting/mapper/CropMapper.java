package com.planting.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.planting.entity.Crop;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

/**
 * 作物Mapper接口
 */
@Mapper
public interface CropMapper extends BaseMapper<Crop> {

    /**
     * 根据名称查询作物
     *
     * @param name 作物名称
     * @return 作物信息
     */
    @Select("SELECT * FROM crop WHERE name = #{name} AND deleted = 0")
    Crop selectByName(@Param("name") String name);

    /**
     * 统计作物被使用的次数
     *
     * @param cropId 作物ID
     * @return 使用次数
     */
    @Select("SELECT COUNT(*) FROM planting_plan WHERE crop_id = #{cropId} AND deleted = 0")
    Long countUsageByCropId(@Param("cropId") Long cropId);
}
