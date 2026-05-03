package com.planting.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 诊断响应DTO
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DiagnoseResponse {

    private String pestName;

    private String pestType;

    private String cropType;

    private String symptoms;

    private String treatmentMethods;

    private String preventionMethods;

    private String severity;

    private String season;

    private Double confidence;

    private boolean highConfidence;
}
