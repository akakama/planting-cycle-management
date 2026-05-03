package com.planting.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;

/**
 * 聊天请求DTO
 */
@Data
public class ChatRequest {

    @NotBlank(message = "提问内容不能为空")
    private String message;

    private String conversationId;
}
