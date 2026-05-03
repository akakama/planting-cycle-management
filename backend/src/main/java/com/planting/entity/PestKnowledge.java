package com.planting.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 病虫害知识库实体类
 */
@Data
@TableName("pest_knowledge")
public class PestKnowledge {

    /**
     * 知识库ID
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /**
     * 病虫害名称
     */
    @TableField("pest_name")
    private String pestName;

    /**
     * 病虫害类型（真菌病害、细菌病害、病毒病害、昆虫害虫等）
     */
    @TableField("pest_type")
    private String pestType;

    /**
     * 受害作物（逗号分隔）
     */
    @TableField("affected_crops")
    private String affectedCrops;

    /**
     * 症状描述
     */
    @TableField("symptoms")
    private String symptoms;

    /**
     * 视觉特征（用于图片识别）
     */
    @TableField("visual_features")
    private String visualFeatures;

    /**
     * 发生季节
     */
    @TableField("season")
    private String season;

    /**
     * 严重程度（轻微、中等、严重）
     */
    @TableField("severity")
    private String severity;

    /**
     * 治疗方法
     */
    @TableField("treatment_methods")
    private String treatmentMethods;

    /**
     * 预防方法
     */
    @TableField("prevention_methods")
    private String preventionMethods;

    /**
     * 图像模式（用于图片识别的关键词）
     */
    @TableField("image_patterns")
    private String imagePatterns;

    /**
     * 置信度分数（0-100）
     */
    @TableField("confidence_score")
    private BigDecimal confidenceScore;

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