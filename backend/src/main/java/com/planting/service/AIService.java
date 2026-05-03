package com.planting.service;

import com.planting.dto.ChatRequest;
import com.planting.dto.ChatResponse;

/**
 * AI服务接口
 */
public interface AIService {

    /**
     * AI聊天
     */
    ChatResponse chat(ChatRequest request, String username);

    /**
     * 获取聊天历史
     */
    Object getChatHistory(Integer page, Integer size);
}
