package com.planting.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.time.LocalDateTime;

/**
 * 作物实体类
 */
@Data
@TableName("crop")
public class Crop {

    /**
     * 作物ID
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /**
     * 作物名称
     */
    @TableField("name")
    @NotBlank(message = "作物名称不能为空")
    @Size(max = 100, message = "作物名称长度不能超过100个字符")
    private String name;

    /**
     * 品种
     */
    @TableField("variety")
    @Size(max = 100, message = "品种长度不能超过100个字符")
    private String variety;

    /**
     * 生长周期（天）
     */
    @TableField("growth_cycle")
    @NotNull(message = "生长周期不能为空")
    private Integer growthCycle;

    /**
     * 种植要求
     */
    @TableField("planting_requirements")
    private String plantingRequirements;

    /**
     * 物候期定义（JSON格式）
     */
    @TableField("phenology_definition")
    private String phenologyDefinition;

    /**
     * 创建时间
     */
    @TableField(value = "create_time", fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    /**
     * 更新时间
     */
    @TableField(value = "update_time", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;

    /**
     * 逻辑删除标记（0-未删除，1-已删除）
     */
    @TableLogic
    @TableField("deleted")
    private Integer deleted;
}
