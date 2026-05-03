package com.planting.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 物候期记录实体类
 */
@Data
@TableName("phenology_record")
public class PhenologyRecord {

    /**
     * 记录ID
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /**
     * 种植计划ID
     */
    @TableField("plan_id")
    @NotNull(message = "种植计划ID不能为空")
    private Long planId;

    /**
     * 物候期名称
     */
    @TableField("phenology_name")
    @NotBlank(message = "物候期名称不能为空")
    private String phenologyName;

    /**
     * 记录日期
     */
    @TableField("record_date")
    @NotNull(message = "记录日期不能为空")
    private LocalDate recordDate;

    /**
     * 描述
     */
    @TableField("description")
    private String description;

    /**
     * 环境数据（JSON格式）
     */
    @TableField("environmental_data")
    private String environmentalData;

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
