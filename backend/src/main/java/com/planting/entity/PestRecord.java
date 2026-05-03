package com.planting.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 病虫害记录实体类
 */
@Data
@TableName("pest_record")
public class PestRecord {

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
     * 病虫害名称
     */
    @TableField("pest_name")
    @NotBlank(message = "病虫害名称不能为空")
    private String pestName;

    /**
     * 发现日期
     */
    @TableField("discovery_date")
    @NotNull(message = "发现日期不能为空")
    private LocalDate discoveryDate;

    /**
     * 严重程度（轻微、中等、严重）
     */
    @TableField("severity")
    private String severity;

    /**
     * 状态（未处理、处理中、已处理）
     */
    @TableField("status")
    private String status;

    /**
     * 描述
     */
    @TableField("description")
    private String description;

    /**
     * 图片URL
     */
    @TableField("image_url")
    private String imageUrl;

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
