package com.planting.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 农资实体类
 */
@Data
@TableName("material")
public class Material {

    /**
     * 农资ID
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /**
     * 农资名称
     */
    @TableField("name")
    @NotBlank(message = "农资名称不能为空")
    private String name;

    /**
     * 类型（种子、化肥、农药等）
     */
    @TableField("type")
    @NotBlank(message = "类型不能为空")
    private String type;

    /**
     * 规格
     */
    @TableField("specification")
    private String specification;

    /**
     * 库存数量
     */
    @TableField("stock_quantity")
    @NotNull(message = "库存数量不能为空")
    private BigDecimal stockQuantity;

    /**
     * 单位
     */
    @TableField("unit")
    private String unit;

    /**
     * 供应商
     */
    @TableField("supplier")
    private String supplier;

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

    /**
     * 版本号（乐观锁）
     */
    @Version
    @TableField("version")
    private Integer version;
}
