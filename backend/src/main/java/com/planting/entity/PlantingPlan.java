package com.planting.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import javax.validation.constraints.NotNull;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 种植计划实体类
 */
@Data
@TableName("planting_plan")
public class PlantingPlan {

    /**
     * 计划ID
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /**
     * 作物ID
     */
    @TableField("crop_id")
    @NotNull(message = "作物ID不能为空")
    private Long cropId;

    /**
     * 地块ID
     */
    @TableField("plot_id")
    @NotNull(message = "地块ID不能为空")
    private Long plotId;

    /**
     * 种植日期
     */
    @TableField("planting_date")
    @NotNull(message = "种植日期不能为空")
    private LocalDate plantingDate;

    /**
     * 预计收获日期
     */
    @TableField("expected_harvest_date")
    private LocalDate expectedHarvestDate;

    /**
     * 状态（未开始、进行中、已完成）
     */
    @TableField("status")
    private String status;

    /**
     * 备注
     */
    @TableField("remark")
    private String remark;

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
