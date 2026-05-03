"""
自定义异常类
"""


class AIServiceError(Exception):
    """AI 服务基础异常"""
    pass


class ModelInferenceError(AIServiceError):
    """模型推理异常"""
    pass


class RetrievalError(AIServiceError):
    """检索异常"""
    pass


class ToolCallError(AIServiceError):
    """工具调用异常"""
    pass


class ImageProcessingError(AIServiceError):
    """图像处理异常"""
    pass
