package com.planting.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 地块实体类
 */
@Data
@TableName("plot")
public class Plot {

    /**
     * 地块ID
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /**
     * 地块编码
     */
    @TableField("code")
    private String code;

    /**
     * 地块名称
     */
    @TableField("name")
    private String name;

    /**
     * 面积（平方米）
     */
    @TableField("area")
    private BigDecimal area;

    /**
     * 位置
     */
    @TableField("location")
    private String location;

    /**
     * 土壤类型
     */
    @TableField("soil_type")
    private String soilType;

    /**
     * 经度
     */
    @TableField("longitude")
    private BigDecimal longitude;

    /**
     * 纬度
     */
    @TableField("latitude")
    private BigDecimal latitude;

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
