# AI 服务模块

种植周期管理系统的 AI 服务模块，提供对话生成、向量检索、图像识别等功能。

## 功能特性

- **对话生成**: 基于 Qwen2.5-7B 大模型，支持多轮对话和上下文理解
- **知识检索**: 基于 ChromaDB 的向量检索，提供农业知识库查询
- **工具调用**: 支持农药查询和天气查询等外部工具
- **图像识别**: 基于 MobileNetV3 的病虫害图像识别

## 技术栈

- **框架**: FastAPI
- **大模型**: vLLM + Qwen2.5-7B
- **向量数据库**: ChromaDB
- **图像识别**: PyTorch + MobileNetV3
- **日志**: Loguru

## 目录结构

```
ai-service/
├── app/
│   ├── main.py                      # 应用入口
│   ├── chat.py                      # 对话接口
│   ├── retrieve.py                  # 检索接口
│   ├── image_recognition.py         # 图像识别接口
│   ├── config.py                    # 配置管理
│   ├── models/                      # 数据模型和服务
│   │   ├── schemas/                 # 数据模型
│   │   │   ├── common.py
│   │   │   ├── chat.py
│   │   │   ├── retrieve.py
│   │   │   └── image.py
│   │   ├── services/                # 业务服务
│   │   │   ├── chat_service.py
│   │   │   ├── retrieval_service.py
│   │   │   ├── tool_service.py
│   │   │   └── image_service.py
│   │   └── utils/                   # 工具类
│   │       ├── exceptions.py
│   │       ├── logger.py
│   │       └── middleware.py
│   └── tools/                       # 外部工具
│       ├── pesticide.py
│       └── weather.py
├── knowledge/                       # 知识库
├── models/                          # 模型文件
├── logs/                            # 日志文件
├── data/                            # 数据文件
├── tests/                           # 测试文件
├── requirements.txt                 # 依赖包
├── config.yaml                      # 配置文件
└── README.md                        # 说明文档
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

编辑 `config.yaml` 文件或通过环境变量配置：

```yaml
app:
  host: "0.0.0.0"
  port: 8000
  debug: false

vllm:
  api_url: "http://localhost:8001"
  model_name: "qwen2.5-7b"
  max_tokens: 2048
  temperature: 0.7

chromadb:
  host: "localhost"
  port: 8000
  collection_name: "planting_knowledge"

image_recognition:
  model_path: "models/mobilenetv3.pth"
  confidence_threshold: 0.6
  max_image_size: 10485760  # 10MB

tools:
  weather_api_key: ""
  weather_api_url: "https://api.weather.example.com"
  pesticide_db_path: "data/pesticides.db"
```

## 启动方式

### 1. 启动 vLLM 服务

```bash
python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2.5-7B-Instruct --port 8001
```

### 2. 启动 ChromaDB 服务

```bash
chroma-server --host localhost --port 8000
```

### 3. 启动 AI 服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

或直接运行：

```bash
python -m app.main
```

## API 接口

### 1. 对话生成

**接口**: `POST /v1/chat/completions`

**请求体**:
```json
{
  "model": "qwen2.5-7b",
  "messages": [
    {"role": "user", "content": "小麦白粉病如何防治？"}
  ],
  "temperature": 0.7,
  "max_tokens": 2048
}
```

**响应**:
```json
{
  "id": "uuid",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "qwen2.5-7b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "小麦白粉病的防治方法..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 100,
    "total_tokens": 120
  }
}
```

### 2. 向量检索

**接口**: `POST /api/retrieve`

**请求体**:
```json
{
  "query": "小麦种植技术",
  "top_k": 5
}
```

**响应**:
```json
{
  "documents": [
    {
      "content": "小麦种植技术...",
      "metadata": {},
      "score": 0.95
    }
  ],
  "total": 1
}
```

### 3. 图像识别

**接口**: `POST /api/image/diagnose`

**请求**: multipart/form-data，上传图像文件

**响应**:
```json
{
  "success": true,
  "result": {
    "disease_name": "小麦白粉病",
    "confidence": 0.85,
    "treatment_suggestion": "使用三唑酮等杀菌剂喷施"
  },
  "message": "识别成功"
}
```

### 4. 健康检查

**接口**: `GET /health`

**响应**:
```json
{
  "status": "healthy",
  "services": {
    "retrieval": true,
    "tool": true,
    "image": true,
    "chat": true
  }
}
```

## API 文档

启动服务后，访问以下地址查看 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 注意事项

1. **模型文件**: 需要下载 MobileNetV3 模型并放置在 `models/` 目录下
2. **知识库**: 需要先创建 ChromaDB 集合并导入农业知识库数据
3. **天气 API**: 如需真实天气数据，请配置有效的 API 密钥
4. **依赖服务**: 启动前需要确保 vLLM 和 ChromaDB 服务已运行

## 开发模式

```bash
# 启动开发模式（支持热重载）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 生产部署

```bash
# 启动生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 许可证

MIT License
