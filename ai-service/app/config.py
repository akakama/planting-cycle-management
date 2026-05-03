"""
配置管理模块
支持从配置文件和环境变量加载配置
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import yaml
import os


class AppConfig(BaseSettings):
    """应用配置"""
    host: str = Field(default="0.0.0.0", description="服务监听地址")
    port: int = Field(default=8000, description="服务监听端口")
    debug: bool = Field(default=False, description="调试模式")

    class Config:
        env_prefix = "APP_"


class VLLMConfig(BaseSettings):
    """vLLM 配置"""
    api_url: str = Field(default="http://localhost:8001", description="vLLM API 地址")
    model_name: str = Field(default="qwen2.5-7b", description="模型名称")
    max_tokens: int = Field(default=2048, gt=0, le=4096, description="最大生成 token 数")
    temperature: float = Field(default=0.7, ge=0, le=2, description="温度参数")

    class Config:
        env_prefix = "VLLM_"


class ChromaDBConfig(BaseSettings):
    """ChromaDB 配置"""
    host: str = Field(default="localhost", description="ChromaDB 主机")
    port: int = Field(default=8000, description="ChromaDB 端口")
    collection_name: str = Field(default="planting_knowledge", description="集合名称")

    class Config:
        env_prefix = "CHROMADB_"


class ImageRecognitionConfig(BaseSettings):
    """图像识别配置"""
    model_path: str = Field(default="ai-service/models/mobilenetv3.pth", description="模型路径")
    confidence_threshold: float = Field(default=0.6, ge=0, le=1, description="置信度阈值")
    max_image_size: int = Field(default=10485760, gt=0, description="最大图像大小（字节）")
    supported_formats: str = Field(
        default='["image/jpeg", "image/jpg", "image/png"]',
        description="支持的图像格式"
    )

    class Config:
        env_prefix = "IMAGE_RECOGNITION_"


class ToolsConfig(BaseSettings):
    """工具配置"""
    weather_api_key: str = Field(default="", description="天气 API 密钥")
    weather_api_url: str = Field(
        default="https://api.weather.example.com",
        description="天气 API 地址"
    )
    pesticide_db_path: str = Field(default="data/pesticides.db", description="农药数据库路径")
    backend_url: str = Field(default="http://localhost:8080", description="后端API地址")

    class Config:
        env_prefix = "TOOLS_"


class LoggingConfig(BaseSettings):
    """日志配置"""
    level: str = Field(default="INFO", description="日志级别")
    file: str = Field(default="logs/ai-service.log", description="日志文件路径")
    rotation: str = Field(default="10 MB", description="日志轮转大小")
    retention: str = Field(default="7 days", description="日志保留时间")

    class Config:
        env_prefix = "LOGGING_"


class Config:
    """全局配置类"""

    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置

        Args:
            config_file: 配置文件路径，默认为 config.yaml
        """
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

        # 从配置文件加载
        self._load_from_file(config_file)

        # 初始化各配置类（环境变量优先级更高）
        self.app = AppConfig()
        self.vllm = VLLMConfig()
        self.chromadb = ChromaDBConfig()
        self.image_recognition = ImageRecognitionConfig()
        self.tools = ToolsConfig()
        self.logging = LoggingConfig()

    def _load_from_file(self, config_file: str):
        """从 YAML 配置文件加载配置"""
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                if config_data:
                    # 将配置数据设置为环境变量（Pydantic Settings 会读取）
                    self._set_env_from_dict(config_data)

    def _set_env_from_dict(self, config_dict: dict, prefix: str = ""):
        """递归地将字典转换为环境变量"""
        for key, value in config_dict.items():
            env_key = f"{prefix}{key.upper()}"
            if isinstance(value, dict):
                self._set_env_from_dict(value, f"{env_key}_")
            else:
                os.environ[env_key] = str(value)


# 创建全局配置实例
config = Config()
