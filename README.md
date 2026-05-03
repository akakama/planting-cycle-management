# 智能种植周期管理系统 - 完整文档

## 📋 目录

1. [项目简介](#项目简介)
2. [快速开始](#快速开始)
3. [病虫害图片识别系统](#病虫害图片识别系统)
4. [知识库系统](#知识库系统)
5. [技术架构](#技术架构)
6. [部署指南](#部署指南)
7. [API接口](#api接口)
8. [常见问题](#常见问题)

---

## 项目简介

### 系统概述

本项目是一个基于千问大模型（Qwen2.5-7B）的智能种植周期管理系统，旨在为农业生产提供全方位的数字化管理解决方案。系统集成了大模型AI能力，能够提供智能决策支持，帮助农户和农业企业实现科学化、精细化的种植管理。

### 核心功能

- **资源管理**：管理作物品种、种植地块等基础资源信息
- **种植规划**：制定种植计划，生成种植日历，优化种植布局
- **物候期监测**：记录和跟踪作物生长阶段，监测环境数据
- **病虫害图片识别**：基于MobileNetV3深度学习模型的智能病虫害识别系统（38类，98.69%准确率）
- **病虫害管理**：记录病虫害信息，支持图像识别诊断
- **农资管理**：管理农资库存，记录农资使用情况
- **采收管理**：记录采收信息，统计分析品质数据
- **产量预估**：基于物候期和环境数据，智能预估产量
- **AI智能问答**：集成千问大模型，提供农业知识问答和决策支持

### 技术特色

- **大模型集成**：基于Qwen2.5-7B大模型，提供智能化的农业知识问答
- **向量检索**：使用ChromaDB向量数据库，实现精准的农业知识检索
- **图像识别**：基于MobileNetV3深度学习模型（PlantVillage数据集38类），准确率98.69%
- **工具调用**：支持农药查询、天气查询等外部工具调用
- **全栈开发**：采用Vue 3 + Spring Boot + FastAPI技术栈

---

## 快速开始

### 环境要求

- **Node.js**: >= 16.0.0
- **Java**: >= 11
- **Python**: >= 3.8
- **MySQL**: >= 8.0（生产环境）
- **Redis**: >= 6.0（生产环境）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/akakama/planting-cycle-management.git
cd planting-cycle-management
```

2. **安装前端依赖**
```bash
cd frontend
npm install
```

3. **安装后端依赖**
```bash
cd ../backend
mvn clean install
```

4. **安装AI服务依赖**
```bash
cd ../ai-service
pip install -r requirements.txt
```

### 启动服务

#### 方式一：快速启动（推荐）

**启动后端服务**：
```bash
cd backend
# 使用现有的JAR文件启动
java -jar target/planting-backend-1.0.0.jar
# 或使用Maven启动
mvn spring-boot:run
```

**启动前端服务**：
```bash
cd frontend
npm run dev
```

#### 方式二：完整启动（包含AI服务）

**启动后端服务**：
```bash
cd backend
mvn spring-boot:run
```

**启动vLLM服务**：
```bash
cd ai-service
python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2.5-7B-Instruct --port 8001
```

**启动FastAPI服务**：
```bash
cd ai-service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**启动前端服务**：
```bash
cd frontend
npm run dev
```

### 访问应用

- **前端应用**: http://localhost:5173 或 http://localhost:5174
- **后端API**: http://localhost:8082/api
- **API文档**: http://localhost:8082/api/doc.html（如启用Knife4j）
- **AI服务文档**: http://localhost:8000/docs

### 默认账号

- **用户名**: admin
- **密码**: admin123

---

## 病虫害图片识别系统

### 系统概述

病虫害图片识别系统基于MobileNetV3深度学习模型，使用PlantVillage数据集训练，能够识别38类农作物病害（含健康叶片），模型准确率达到98.69%。系统通过完整的调用链路实现端到端推理：前端上传图片 → 后端Spring Boot → AI服务FastAPI → MobileNetV3模型推理。

### 模型信息

| 项目 | 详情 |
|------|------|
| 模型架构 | MobileNetV3 Large |
| 训练数据集 | PlantVillage (Kaggle) |
| 类别数 | 38类 |
| 验证准确率 | 98.69% |
| 模型大小 | 16.41 MB |
| 推理框架 | PyTorch |
| 训练时长 | 31.25 分钟 (GPU) |

### 识别范围

**14种作物，38个类别**：

- **苹果 (Apple)**：黑星病、黑腐病、锈病、健康
- **蓝莓 (Blueberry)**：健康
- **樱桃 (Cherry)**：白粉病、健康
- **玉米 (Corn)**：灰斑病、锈病、大斑病、健康
- **葡萄 (Grape)**：黑腐病、黑疹病、叶枯病、健康
- **柑橘 (Orange)**：黄龙病
- **桃 (Peach)**：细菌性斑点、健康
- **辣椒 (Pepper)**：细菌性斑点、健康
- **马铃薯 (Potato)**：早疫病、晚疫病、健康
- **覆盆子 (Raspberry)**：健康
- **大豆 (Soybean)**：健康
- **南瓜 (Squash)**：白粉病
- **草莓 (Strawberry)**：叶焦病、健康
- **番茄 (Tomato)**：细菌性斑点、早疫病、晚疫病、叶霉病、壳针孢叶斑病、二斑叶螨、靶斑病、黄化曲叶病毒病、花叶病毒病、健康

### 核心功能

#### 1. 深度学习模型推理

- 基于MobileNetV3 Large架构，轻量高效
- 输入图片自动预处理（resize 224x224, 归一化）
- Softmax输出38类概率分布
- 返回Top-1预测结果及置信度

#### 2. 完整调用链路

```
前端 PestList.vue
    ↓ 图片转Base64
POST /api/pest-records/diagnose {planId, imageBase64}
    ↓
后端 PestRecordServiceImpl
    ↓ RestTemplate转发
POST /api/image/diagnose {planId, imageBase64}
    ↓ Base64解码 → 图像字节
AI服务 image_recognition.py
    ↓ MobileNetV3推理
DiagnoseResponse {pestName, confidence, treatmentMethods, highConfidence}
```

#### 3. 结果展示

**展示信息**：
- 病虫害名称（含中英文对照）
- 置信度（百分比，高置信度>70%标记）
- 严重程度（高/中/低）
- 防治建议（针对性方案）
- 预防措施
- 识别模式说明（深度学习模型 - MobileNetV3）

### 准确度指标

| 指标 | 数值 |
|------|------|
| 识别类别 | 38类 |
| 验证集准确率 | 98.69% |
| 覆盖作物 | 14种 |
| 高置信度阈值 | 70% |
| 识别速度 | < 1秒 |

### 使用流程

```
上传病虫害图片
    ↓
图片转Base64编码
    ↓
后端转发至AI服务
    ↓
MobileNetV3模型推理
    ↓
返回识别结果 + 防治建议
```

### 测试建议

#### 推荐测试图片

**番茄病害**（测试最丰富，11个类别）：
- 细菌性斑点、早疫病、晚疫病、叶霉病
- 壳针孢叶斑病、靶斑病、黄化曲叶病毒病、花叶病毒病
- 二斑叶螨、健康叶片

**苹果病害**：
- 黑星病、黑腐病、锈病、健康

**玉米病害**：
- 灰斑病、锈病、大斑病、健康

**葡萄病害**：
- 黑腐病、黑疹病、叶枯病、健康

#### 测试步骤

1. **启动AI服务**：`cd ai-service && uvicorn app.main:app --port 8000`
2. **启动后端服务**：`cd backend && mvn spring-boot:run`
3. **启动前端**：`cd frontend && npm run dev`
4. **访问系统**：http://localhost:5174/
5. **登录**：admin / admin123
6. **进入页面**：病虫害图片识别
7. **上传图片**：选择病虫害图片
8. **查看结果**：查看MobileNetV3模型识别结果

---

## 知识库系统

### 知识库概述

病虫害知识库是系统的辅助组件，用于AI问答中的农业知识检索和模型推理结果的防治方案补充。核心识别能力由MobileNetV3深度学习模型提供。

### 知识库用途

- AI问答系统的知识检索（ChromaDB向量数据库）
- 模型识别结果的防治方案补充
- 农业标准和药剂推荐数据

---

## 技术架构

### 技术栈

| 模块 | 技术组件 | 版本 | 说明 |
|------|---------|------|------|
| **前端** | Vue 3 | 3.x | 渐进式JavaScript框架 |
| | Element Plus | 2.x | Vue 3组件库 |
| | Axios | 1.x | HTTP客户端 |
| | ECharts | 5.x | 数据可视化库 |
| | Vite | 4.x | 前端构建工具 |
| | Vue Router | 4.x | 路由管理 |
| | Pinia | 2.x | 状态管理 |
| **后端** | Spring Boot | 2.7.x | Java应用框架 |
| | MyBatis-Plus | 3.x | ORM框架 |
| | Spring Security | 5.x | 安全框架 |
| | JWT | - | 身份认证 |
| | H2/MySQL | - | 数据库（开发/生产） |
| | Redis | 6.x+ | 缓存数据库 |
| **AI服务** | FastAPI | 0.x | Python Web框架 |
| | vLLM | 0.x | 大模型推理框架 |
| | Qwen2.5-7B | 2.5 | 千问大模型 |
| | ChromaDB | 0.x | 向量数据库 |
| | PyTorch | 2.x | 深度学习框架 |
| | MobileNetV3 | - | 图像识别模型 |

### 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     前端层 (Vue 3)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │资源管理  │  │种植规划  │  │物候监测  │  │病虫害识别│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │农资管理  │  │采收管理  │  │产量预估  │  │AI智能问答│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   API网关层 (Nginx)                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  后端层 (Spring Boot)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │资源管理  │  │种植规划  │  │物候监测  │  │病虫害管理│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │农资管理  │  │采收管理  │  │产量预估  │  │用户认证  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   数据层 (MySQL + Redis)                  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                   AI服务层 (FastAPI)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │大模型问答│  │知识检索  │  │图像识别  │  │工具调用  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│             AI模型层 (Qwen2.5-7B + ChromaDB)              │
└─────────────────────────────────────────────────────────┘
```

### 目录结构

```
planting-cycle-management/
├── frontend/                       # 前端Vue 3项目
│   ├── public/                     # 静态资源
│   ├── src/                        # 源代码
│   │   ├── api/                    # API接口封装
│   │   ├── assets/                 # 资源文件
│   │   ├── components/             # 公共组件
│   │   ├── views/                  # 页面组件
│   │   ├── router/                 # 路由配置
│   │   ├── store/                  # 状态管理
│   │   ├── utils/                  # 工具函数
│   │   ├── data/                   # 数据文件
│   │   │   └── pestKnowledgeBase.js # 病虫害知识库（75种）
│   │   ├── App.vue                 # 根组件
│   │   └── main.js                 # 入口文件
│   ├── package.json                # 依赖配置
│   ├── vite.config.js              # Vite配置
│   └── README.md                   # 前端说明文档
│
├── backend/                        # 后端Spring Boot项目
│   ├── src/main/java/com/planting/
│   │   ├── controller/             # 控制器层
│   │   ├── service/                # 服务层
│   │   ├── mapper/                 # 数据访问层
│   │   ├── entity/                 # 实体类
│   │   ├── dto/                    # 数据传输对象
│   │   ├── config/                 # 配置类
│   │   └── common/                 # 公共类
│   ├── src/main/resources/
│   │   ├── application.yml         # 应用配置
│   │   └── db/schema.sql           # 数据库脚本
│   ├── pom.xml                     # Maven配置
│   └── README.md                   # 后端说明文档
│
├── ai-service/                     # AI服务FastAPI项目
│   ├── app/                        # 应用代码
│   │   ├── main.py                 # 应用入口
│   │   ├── chat.py                 # 对话接口
│   │   ├── retrieve.py             # 检索接口
│   │   └── image_recognition.py    # 图像识别接口
│   ├── knowledge/                  # 知识库
│   ├── models/                     # 模型文件
│   ├── requirements.txt            # Python依赖
│   ├── config.yaml                 # 配置文件
│   └── README.md                   # AI服务说明文档
│
├── sql/                            # 数据库脚本
│   └── schema.sql                  # 建表脚本
│
└── README.md                       # 项目说明文档（本文件）
```

---

## 部署指南

### 开发环境部署

#### 前端部署

1. **安装依赖**
```bash
cd frontend
npm install
```

2. **启动开发服务器**
```bash
npm run dev
```

3. **访问应用**
```
http://localhost:5173
```

#### 后端部署

1. **配置数据库**
```yaml
# application.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/planting_db
    username: root
    password: your_password
```

2. **启动服务**
```bash
cd backend
mvn spring-boot:run
```

3. **访问API**
```
http://localhost:8082/api
```

#### AI服务部署

1. **安装依赖**
```bash
cd ai-service
pip install -r requirements.txt
```

2. **启动vLLM服务**
```bash
python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2.5-7B-Instruct --port 8001
```

3. **启动FastAPI服务**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. **访问AI服务**
```
http://localhost:8000/docs
```

### 生产环境部署

#### 前端部署

1. **构建生产版本**
```bash
cd frontend
npm run build
```

2. **部署到Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/planting-cycle-management/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8082/api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 后端部署

1. **打包应用**
```bash
cd backend
mvn clean package
```

2. **部署到服务器**
```bash
java -jar target/planting-backend-1.0.0.jar
```

3. **配置 systemd 服务**
```ini
[Unit]
Description=Planting Backend Service
After=syslog.target network.target

[Service]
Type=simple
User=planting
WorkingDirectory=/opt/planting/backend
ExecStart=/usr/bin/java -jar /opt/planting/backend/target/planting-backend-1.0.0.jar
Restart=always

[Install]
WantedBy=multi-user.target
```

#### AI服务部署

1. **配置守护进程**
```bash
# 使用supervisor或systemd管理AI服务
```

2. **配置负载均衡**
```bash
# 使用Nginx或HAProxy进行负载均衡
```

---

## API接口

### 主要接口

#### 认证接口

**登录**
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

Response:
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "userInfo": {
      "id": 1,
      "username": "admin",
      "role": "admin"
    }
  }
}
```

#### 病虫害识别接口

**诊断病虫害（MobileNetV3模型）**
```
POST /api/pest-records/diagnose
Content-Type: application/json
Authorization: Bearer {token}

{
  "planId": 1,
  "imageBase64": "base64编码的图片数据"
}

Response:
{
  "code": 200,
  "message": "诊断成功",
  "data": {
    "pestName": "番茄晚疫病（Tomato Late Blight）",
    "pestType": "病害",
    "symptoms": "",
    "treatmentMethods": "喷施甲霜灵或烯酰吗啉，降低田间湿度",
    "preventionMethods": "",
    "severity": "中",
    "confidence": 95.6,
    "highConfidence": true
  }
}
```

#### AI问答接口

**智能问答**
```
POST /api/ai/chat
Content-Type: application/json
Authorization: Bearer {token}

{
  "question": "如何防治稻瘟病？"
}

Response:
{
  "code": 200,
  "message": "问答成功",
  "data": {
    "answer": "稻瘟病的防治方法包括...",
    "sources": [...]
  }
}
```

### 完整API文档

详细的API文档请参考：
- **API概览**: `docs/api-summary.md`
- **农业API**: `docs/农业API接口文档.md`
- **智能知识API**: `docs/智能农业知识API文档.md`

---

## 常见问题

### 启动相关

**Q: 前端启动失败，提示端口被占用？**

A: 修改 `vite.config.js` 中的端口号：
```javascript
server: {
  port: 5174, // 修改为其他端口
  host: '0.0.0.0'
}
```

**Q: 后端启动失败，提示数据库连接错误？**

A: 检查数据库配置：
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/planting_db
    username: root
    password: your_password
```

**Q: AI服务启动失败，提示模型加载错误？**

A: 确保模型文件已下载并放置在正确位置：
```bash
# 检查模型文件
ls ai-service/models/Qwen2.5-7B-Instruct
```

### 功能相关

**Q: 病虫害识别不准确？**

A: 确保上传的图片：
- 清晰度高，光线适当
- 包含明显的病虫害特征
- 图片格式为JPG、JPEG、PNG
- 文件大小不超过10MB
- 当前模型基于PlantVillage数据集（38类），覆盖14种作物

**Q: AI服务连接失败？**

A: 检查AI服务是否启动：
```bash
curl http://localhost:8000/docs
```
确保后端 `application.yml` 中AI服务地址配置正确（`http://localhost:8000`）

**Q: 如何更换或微调模型？**

A: 替换 `ai-service/models/mobilenetv3_best.pth` 文件，并更新 `class_mapping.json` 类别映射

### 性能相关

**Q: 识别速度慢？**

A: 优化建议：
- 压缩图片大小
- 使用CDN加速图片加载
- 优化网络连接
- 升级服务器配置

**Q: 前端页面加载慢？**

A: 优化建议：
- 启用Gzip压缩
- 使用CDN加速静态资源
- 优化代码分割
- 减少HTTP请求

---

## 更新日志

### v3.0.0 (2026-05-03)

**MobileNetV3深度学习模型集成**：
- 集成MobileNetV3 Large模型（PlantVillage 38类，98.69%准确率）
- 实现前端→后端→AI服务→模型推理完整调用链路
- AI服务支持JSON请求体和响应格式匹配
- 前端改为调用后端AI接口，不再使用本地知识库匹配
- 修复后端AI服务URL路径和端口配置
- 识别置信度从30%（知识库匹配）提升至95%+（深度学习模型）

### v2.0.0 (2025-06-18)

**系统功能完善**：
- 病虫害知识库扩充
- 集成千问大模型AI问答
- 完成文档体系

### v1.0.0 (2025-06-18)

**初始版本发布**：
- 实现核心功能模块
- 基础病虫害识别功能

---

## 致谢

感谢以下开源项目：

- [Vue.js](https://vuejs.org/)
- [Spring Boot](https://spring.io/projects/spring-boot)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Qwen](https://github.com/QwenLM/Qwen)
- [vLLM](https://github.com/vllm-project/vllm)
- [ChromaDB](https://www.trychroma.com/)
- [Element Plus](https://element-plus.org/)

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

- **项目维护者**: CodeArts Agent
- **项目主页**: https://github.com/akakama/planting-cycle-management
- **问题反馈**: https://github.com/akakama/planting-cycle-management/issues

---

**最后更新**: 2026-05-03

🎯
