package com.planting.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import javax.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 产量预估实体类
 */
@Data
@TableName("yield_prediction")
public class YieldPrediction {

    /**
     * 预估ID
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
     * 预估日期
     */
    @TableField("prediction_date")
    @NotNull(message = "预估日期不能为空")
    private LocalDate predictionDate;

    /**
     * 预估产量
     */
    @TableField("predicted_yield")
    @NotNull(message = "预估产量不能为空")
    private BigDecimal predictedYield;

    /**
     * 预测方法
     */
    @TableField("prediction_method")
    private String predictionMethod;

    /**
     * 置信度等级
     */
    @TableField("confidence_level")
    private String confidenceLevel;

    /**
     * 生长阶段
     */
    @TableField("growth_stage")
    private String growthStage;

    /**
     * 天气影响
     */
    @TableField("weather_impact")
    private String weatherImpact;

    /**
     * 肥料影响
     */
    @TableField("fertilizer_impact")
    private String fertilizerImpact;

    /**
     * 水分影响
     */
    @TableField("water_impact")
    private String waterImpact;

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
