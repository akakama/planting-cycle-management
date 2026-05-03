package com.planting.dto;

import com.planting.entity.PlantingPlan;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.math.BigDecimal;

/**
 * 种植计划DTO，包含关联信息
 */
@Data
@EqualsAndHashCode(callSuper = true)
public class PlantingPlanDTO extends PlantingPlan {

    /**
     * 作物名称
     */
    private String cropName;

    /**
     * 地块名称
     */
    private String plotName;

    /**
     * 种植面积（亩）
     */
    private BigDecimal plantingArea;

    /**
     * 预计产量（kg）
     */
    private BigDecimal expectedYield;
}
