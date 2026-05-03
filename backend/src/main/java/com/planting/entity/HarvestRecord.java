package com.planting.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import javax.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 采收记录实体类
 */
@Data
@TableName("harvest_record")
public class HarvestRecord {

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
     * 采收日期
     */
    @TableField("harvest_date")
    @NotNull(message = "采收日期不能为空")
    private LocalDate harvestDate;

    /**
     * 采收数量
     */
    @TableField("harvest_quantity")
    @NotNull(message = "采收数量不能为空")
    private BigDecimal harvestQuantity;

    /**
     * 采收方式
     */
    @TableField("harvest_method")
    private String harvestMethod;

    /**
     * 买家
     */
    @TableField("buyer")
    private String buyer;

    /**
     * 销售金额
     */
    @TableField("sale_amount")
    private BigDecimal saleAmount;

    /**
     * 单位
     */
    @TableField("unit")
    private String unit;

    /**
     * 品质等级
     */
    @TableField("quality_grade")
    private String qualityGrade;

    /**
     * 含水率
     */
    @TableField("moisture_content")
    private BigDecimal moistureContent;

    /**
     * 蛋白质含量
     */
    @TableField("protein_content")
    private BigDecimal proteinContent;

    /**
     * 采收面积
     */
    @TableField("harvest_area")
    private BigDecimal harvestArea;

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
