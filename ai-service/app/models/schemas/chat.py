"""
对话相关的数据模型
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum


class Role(str, Enum):
    """消息角色枚举"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """消息模型"""
    role: Role = Field(..., description="消息角色")
    content: str = Field(..., min_length=1, description="消息内容")


class ToolFunction(BaseModel):
    """工具函数模型"""
    name: str = Field(..., description="工具名称")
    description: str = Field(..., description="工具描述")
    parameters: Dict[str, Any] = Field(default={}, description="工具参数")


class Tool(BaseModel):
    """工具模型"""
    type: str = Field(default="function", description="工具类型")
    function: ToolFunction = Field(..., description="工具函数")


class ChatCompletionRequest(BaseModel):
    """对话请求模型"""
    model: str = Field(..., pattern=r"^qwen2\.5-7b$", description="模型名称")
    messages: List[Message] = Field(..., min_length=1, description="消息列表")
    temperature: Optional[float] = Field(0.7, ge=0, le=2, description="温度参数")
    max_tokens: Optional[int] = Field(2048, gt=0, le=4096, description="最大生成 token 数")
    tools: Optional[List[Tool]] = Field(None, description="可用工具列表")


class ChatCompletionMessage(BaseModel):
    """对话响应消息模型"""
    role: str = Field(..., description="消息角色")
    content: Optional[str] = Field(None, description="消息内容")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(None, description="工具调用")


class ChatCompletionChoice(BaseModel):
    """对话选项模型"""
    index: int = Field(..., description="选项索引")
    message: ChatCompletionMessage = Field(..., description="消息内容")
    finish_reason: str = Field(..., description="结束原因")


class Usage(BaseModel):
    """Token 使用统计模型"""
    prompt_tokens: int = Field(..., description="提示词 token 数")
    completion_tokens: int = Field(..., description="完成 token 数")
    total_tokens: int = Field(..., description="总 token 数")


class ChatCompletionResponse(BaseModel):
    """对话响应模型"""
    id: str = Field(..., description="请求 ID")
    object: str = Field(default="chat.completion", description="对象类型")
    created: int = Field(..., description="创建时间戳")
    model: str = Field(..., description="模型名称")
    choices: List[ChatCompletionChoice] = Field(..., description="选项列表")
    usage: Usage = Field(..., description="Token 使用统计")
