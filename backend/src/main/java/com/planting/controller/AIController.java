package com.planting.controller;

import com.planting.common.ApiResponse;
import com.planting.dto.ChatRequest;
import com.planting.dto.ChatResponse;
import com.planting.service.AIService;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

/**
 * AI智能问答控制器
 */
@Slf4j
@RestController
@RequestMapping("/ai")
public class AIController {

    @Autowired
    private AIService aiService;

    /**
     * AI聊天
     */
    @PostMapping("/chat")
    @PreAuthorize("hasAuthority('ai:chat')")
    public ApiResponse<ChatResponse> chat(
            @RequestBody ChatRequest request,
            Authentication authentication) {

        String username = authentication.getName();
        ChatResponse response = aiService.chat(request, username);
        return ApiResponse.success(response);
    }

    /**
     * 获取聊天历史
     */
    @GetMapping("/history")
    @PreAuthorize("hasAuthority('ai:chat')")
    public ApiResponse<?> getChatHistory(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size) {

        return ApiResponse.success(aiService.getChatHistory(page, size));
    }
}
