package com.planting.dto;

import lombok.Data;

import javax.validation.constraints.Min;
import javax.validation.constraints.Size;

/**
 * 更新作物请求DTO
 */
@Data
public class UpdateCropRequest {

    @Size(max = 100, message = "作物名称长度不能超过100个字符")
    private String name;

    @Size(max = 100, message = "品种长度不能超过100个字符")
    private String variety;

    @Min(value = 1, message = "生长周期必须大于0")
    private Integer growthCycle;

    private String plantingRequirements;

    private String phenologyDefinition;
}
