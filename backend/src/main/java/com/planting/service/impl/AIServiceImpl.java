package com.planting.service.impl;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.planting.dto.ChatRequest;
import com.planting.dto.ChatResponse;
import com.planting.service.AIService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * AI服务实现类
 * 调用千问(Qwen2.5-7B)大模型进行智能问答
 */
@Slf4j
@Service
public class AIServiceImpl implements AIService {

    @Value("${ai.service.url:http://localhost:8001}")
    private String aiServiceUrl = "http://localhost:8001";
    
    @Value("${ai.service.model:qwen2.5-7b}")
    private String modelName;
    
    @Value("${ai.service.timeout:30000}")
    private int timeout;
    
    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public AIServiceImpl() {
        this.restTemplate = new RestTemplate();
        this.objectMapper = new ObjectMapper();
    }

    @Override
    public ChatResponse chat(ChatRequest request, String username) {
        log.info("AI聊天请求，用户: {}, 问题: {}", username, request.getMessage());

        try {
            // 构建请求体
            Map<String, Object> requestBody = buildChatRequest(request);
            
            // 设置请求头
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            // 发送请求
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);
            String url = aiServiceUrl + "/v1/chat/completions";
            
            log.info("调用AI服务: {}", url);
            
            ResponseEntity<String> response = restTemplate.exchange(
                url,
                HttpMethod.POST,
                entity,
                String.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                // 解析响应
                String reply = parseChatResponse(response.getBody());
                
                log.info("AI聊天响应成功");
                return ChatResponse.builder()
                        .reply(reply)
                        .conversationId(request.getConversationId())
                        .build();
            } else {
                log.error("AI服务返回错误状态: {}", response.getStatusCode());
                return ChatResponse.builder()
                        .reply("抱歉,AI服务暂时不可用,请稍后再试。")
                        .conversationId(request.getConversationId())
                        .build();
            }
            
        } catch (Exception e) {
            log.error("AI聊天失败: {}", e.getMessage(), e);
            return ChatResponse.builder()
                    .reply("抱歉,AI服务调用失败: " + e.getMessage())
                    .conversationId(request.getConversationId())
                    .build();
        }
    }

    /**
     * 构建聊天请求
     */
    private Map<String, Object> buildChatRequest(ChatRequest request) {
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("model", modelName);
        requestBody.put("temperature", 0.4);
        requestBody.put("max_tokens", 4096);
        
        // 构建消息列表
        List<Map<String, String>> messages = new ArrayList<>();
        
        // 添加系统提示
        Map<String, String> systemMessage = new HashMap<>();
        systemMessage.put("role", "system");
        systemMessage.put("content", "【角色定位】\n" +
            "你是农业种植专家，具备作物栽培、土壤肥料、植物保护等专业背景。\n\n" +
            "【核心能力】\n" +
            "• 作物栽培：播种、育苗、田间管理、采收\n" +
            "• 土壤肥料：土壤改良、科学施肥、养分管理\n" +
            "• 植物保护：病虫害诊断与防治、农药科学使用\n" +
            "• 农业气象：天气影响分析、农事时机建议\n\n" +
            "【回答策略】\n" +
            "请按以下步骤分析和回答问题：\n\n" +
            "第一步：识别问题类型\n" +
            "- 价格查询 → 使用实时数据直接回答\n" +
            "- 天气咨询 → 使用实时数据直接回答\n" +
            "- 种植计划 → 制定详细方案\n" +
            "- 技术咨询 → 专业解答\n\n" +
            "第二步：分析关键要素\n" +
            "- 明确作物类型、生长阶段、地区气候\n" +
            "- 识别病虫害症状、土壤条件、管理目标\n\n" +
            "第三步：组织专业回答\n" +
            "- 先给出结论或核心建议\n" +
            "- 再展开具体操作步骤\n" +
            "- 最后补充注意事项和科学原理\n\n" +
            "【回答要求】\n" +
            "• 专业准确：基于农学原理和科学依据\n" +
            "• 逻辑清晰：分点分段，层次分明\n" +
            "• 操作具体：给出明确的时间、用量、方法\n" +
            "• 实用性强：结合实际生产条件给出建议");
        messages.add(systemMessage);
        
        // 添加用户消息
        Map<String, String> userMessage = new HashMap<>();
        userMessage.put("role", "user");
        userMessage.put("content", request.getMessage());
        messages.add(userMessage);
        
        requestBody.put("messages", messages);
        
        return requestBody;
    }

    /**
     * 解析聊天响应
     */
    private String parseChatResponse(String responseBody) {
        try {
            JsonNode root = objectMapper.readTree(responseBody);
            
            // 解析choices数组
            JsonNode choices = root.get("choices");
            if (choices != null && choices.isArray() && choices.size() > 0) {
                JsonNode firstChoice = choices.get(0);
                JsonNode message = firstChoice.get("message");
                if (message != null) {
                    JsonNode content = message.get("content");
                    if (content != null) {
                        return content.asText();
                    }
                }
            }
            
            // 如果没有找到content,返回默认消息
            log.warn("无法解析AI响应内容: {}", responseBody);
            return "抱歉,无法解析AI响应。";
            
        } catch (JsonProcessingException e) {
            log.error("解析AI响应失败: {}", e.getMessage());
            return "抱歉,解析AI响应失败。";
        }
    }

    @Override
    public Object getChatHistory(Integer page, Integer size) {
        // TODO: 实现从数据库获取聊天历史
        log.info("获取聊天历史，页码: {}, 每页大小: {}", page, size);
        return Map.of(
            "total", 0,
            "records", new Object[0],
            "message", "聊天历史功能开发中..."
        );
    }
}
