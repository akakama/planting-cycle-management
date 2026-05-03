package com.planting.dto;

import lombok.Data;

/**
 * 诊断请求DTO
 */
@Data
public class DiagnoseRequest {

    private Long planId;

    private String imageBase64;
}
