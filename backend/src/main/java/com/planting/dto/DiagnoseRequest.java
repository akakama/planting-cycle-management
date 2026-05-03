package com.planting.dto;

import lombok.Data;

import javax.validation.constraints.NotNull;

/**
 * 诊断请求DTO
 */
@Data
public class DiagnoseRequest {

    @NotNull(message = "种植计划ID不能为空")
    private Long planId;

    @NotNull(message = "图片不能为空")
    private String imageBase64;
}
