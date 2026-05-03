package com.planting.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 作物DTO
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CropDTO {

    private Long id;

    private String name;

    private String variety;

    private Integer growthCycle;

    private String plantingRequirements;

    private String phenologyDefinition;

    private LocalDateTime createTime;

    private LocalDateTime updateTime;
}
