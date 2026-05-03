# 智能种植周期管理系统后端

## 项目简介

这是智能种植周期管理系统的后端服务,基于Spring Boot 2.7.x构建,提供完整的RESTful API接口,支持用户认证、作物管理、种植计划、物候期监测、病虫害管理、农资管理、采收管理、产量预估和AI智能问答等功能。

## 技术栈

- **框架**: Spring Boot 2.7.18
- **数据库**: H2 (开发环境) / MySQL 8.0 (生产环境)
- **ORM**: MyBatis-Plus 3.5.5
- **安全**: Spring Security + JWT
- **缓存**: Redis 6.x+
- **API文档**: Knife4j 3.0.3
- **工具库**: Hutool 5.8.24, Lombok

## 项目结构

```
backend/
├── src/main/java/com/planting/
│   ├── controller/          # 控制器层
│   │   ├── AuthController.java
│   │   ├── CropController.java
│   │   ├── PlantingPlanController.java
│   │   ├── PlotController.java
│   │   ├── PhenologyRecordController.java
│   │   ├── PestRecordController.java
│   │   ├── MaterialController.java
│   │   ├── HarvestController.java
│   │   ├── YieldPredictionController.java
│   │   └── AIController.java
│   ├── service/             # 服务层接口
│   │   ├── UserService.java
│   │   ├── CropService.java
│   │   ├── PlantingPlanService.java
│   │   ├── PlotService.java
│   │   ├── PhenologyRecordService.java
│   │   ├── PestRecordService.java
│   │   ├── MaterialService.java
│   │   ├── HarvestService.java
│   │   ├── YieldPredictionService.java
│   │   └── AIService.java
│   ├── service/impl/        # 服务层实现
│   ├── mapper/              # 数据访问层
│   ├── entity/              # 实体类
│   ├── dto/                 # 数据传输对象
│   ├── config/              # 配置类
│   ├── common/              # 公共类
│   ├── exception/           # 异常类
│   └── util/                # 工具类
├── src/main/resources/
│   ├── application.yml      # 应用配置
│   └── schema.sql           # 数据库初始化脚本
└── pom.xml                  # Maven配置
```

## 快速开始

### 环境要求

- JDK 11+
- Maven 3.6+
- Redis 6.x+ (可选,用于缓存)

### 安装依赖

```bash
cd backend
mvn clean install
```

### 配置数据库

开发环境使用H2数据库,无需额外配置。生产环境需要配置MySQL:

1. 修改 `src/main/resources/application.yml` 中的数据库配置:

```yaml
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/planting_db?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: your_password
```

2. 创建数据库并执行初始化脚本:

```sql
CREATE DATABASE planting_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE planting_db;
SOURCE src/main/resources/schema.sql;
```

### 启动应用

```bash
mvn spring-boot:run
```

或者使用IDE运行 `PlantingApplication.java` 主类。

### 访问应用

- **应用地址**: http://localhost:8080/api
- **API文档**: http://localhost:8080/api/doc.html
- **默认账号**: admin / admin123

## API接口说明

### 认证接口

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `GET /api/auth/current-user` - 获取当前用户信息

### 作物管理接口

- `GET /api/crops` - 获取作物列表
- `GET /api/crops/{id}` - 获取作物详情
- `POST /api/crops` - 添加作物
- `PUT /api/crops/{id}` - 更新作物
- `DELETE /api/crops/{id}` - 删除作物

### 种植计划接口

- `GET /api/planting-plans` - 获取种植计划列表
- `GET /api/planting-plans/{id}` - 获取种植计划详情
- `POST /api/planting-plans` - 添加种植计划
- `PUT /api/planting-plans/{id}` - 更新种植计划
- `DELETE /api/planting-plans/{id}` - 删除种植计划
- `PUT /api/planting-plans/{id}/status` - 更新种植状态
- `GET /api/planting-calendar` - 获取种植日历

### 地块管理接口

- `GET /api/plots` - 获取地块列表
- `GET /api/plots/{id}` - 获取地块详情
- `POST /api/plots` - 添加地块
- `PUT /api/plots/{id}` - 更新地块

### 物候期记录接口

- `GET /api/phenology-records` - 获取物候期记录列表
- `POST /api/phenology-records` - 添加物候期记录
- `PUT /api/phenology-records/{id}` - 更新物候期记录
- `DELETE /api/phenology-records/{id}` - 删除物候期记录

### 病虫害记录接口

- `GET /api/pest-records` - 获取病虫害记录列表
- `POST /api/pest-records` - 添加病虫害记录
- `PUT /api/pest-records/{id}` - 更新病虫害记录
- `DELETE /api/pest-records/{id}` - 删除病虫害记录
- `POST /api/pest-records/diagnose` - 病虫害图片识别诊断

### 农资管理接口

- `GET /api/materials` - 获取农资列表
- `GET /api/materials/{id}` - 获取农资详情
- `PUT /api/materials/{id}/stock-in` - 农资入库
- `GET /api/material-usage` - 获取农资使用记录
- `POST /api/material-usage` - 添加农资使用记录

### 采收记录接口

- `GET /api/harvest-records` - 获取采收记录列表
- `POST /api/harvest-records` - 添加采收记录
- `PUT /api/harvest-records/{id}` - 更新采收记录
- `DELETE /api/harvest-records/{id}` - 删除采收记录

### 产量预估接口

- `GET /api/yield-predictions` - 获取产量预估列表
- `POST /api/yield-predictions` - 添加产量预估
- `PUT /api/yield-predictions/{id}` - 更新产量预估
- `DELETE /api/yield-predictions/{id}` - 删除产量预估

### AI智能问答接口

- `POST /api/ai/chat` - AI聊天
- `GET /api/ai/history` - 获取聊天历史
- `GET /api/ai/knowledge/search` - 知识检索
- `GET /api/ai/tools/pesticide-info` - 农药信息查询
- `GET /api/ai/tools/weather` - 天气查询

## 默认数据

系统初始化时会创建以下默认数据:

### 默认用户
- 用户名: `admin`
- 密码: `admin123`
- 角色: 管理员

### 默认作物
- 小麦 (济麦22)
- 水稻 (杂交水稻)
- 玉米 (郑单958)
- 大豆 (黑农44)
- 马铃薯 (费乌瑞它)

### 默认地块
- 东区1号田 (5000平方米)
- 东区2号田 (4500平方米)
- 西区1号田 (6000平方米)
- 西区2号田 (5500平方米)
- 南区1号田 (4800平方米)

### 默认农资
- 尿素 (1000千克)
- 复合肥 (800千克)
- 多菌灵 (200千克)
- 吡虫啉 (150千克)
- 小麦种子 (500千克)
- 水稻种子 (400千克)

## 开发说明

### 代码规范

- 使用Lombok简化代码
- 使用MyBatis-Plus简化CRUD操作
- 使用Spring注解进行依赖注入
- 使用`@Validated`进行参数校验
- 使用`@Transactional`进行事务管理
- 使用`@Cacheable`和`@CacheEvict`进行缓存管理

### 异常处理

系统使用全局异常处理器统一处理异常:

- `BusinessException` - 业务异常
- `MethodArgumentNotValidException` - 参数校验异常
- `AuthenticationException` - 认证异常
- `AccessDeniedException` - 权限异常

所有异常都返回统一的`ApiResponse`格式。

### 权限控制

使用Spring Security + JWT进行认证授权:

- JWT令牌有效期: 24小时
- 使用`@PreAuthorize`注解进行方法级权限控制
- 支持角色权限管理(RBAC)

## 测试

### 使用Knife4j测试API

访问 http://localhost:8080/api/doc.html,可以在线测试所有API接口。

### 使用Postman测试

1. 先调用登录接口获取JWT令牌
2. 在请求头中添加: `Authorization: Bearer {token}`
3. 调用其他受保护的接口

## 部署

### 打包应用

```bash
mvn clean package
```

生成的JAR文件位于 `target/planting-backend-1.0.0.jar`

### 运行应用

```bash
java -jar target/planting-backend-1.0.0.jar
```

### 生产环境配置

1. 修改数据库配置为MySQL
2. 配置Redis连接
3. 修改JWT密钥
4. 配置日志输出路径
5. 配置文件上传路径

## 常见问题

### 1. 数据库连接失败

检查 `application.yml` 中的数据库配置是否正确,确保数据库服务已启动。

### 2. Redis连接失败

如果使用Redis缓存,确保Redis服务已启动,或者禁用Redis缓存功能。

### 3. API文档无法访问

检查 `Knife4jConfig.java` 配置是否正确,确保应用已成功启动。

### 4. JWT令牌过期

默认JWT令牌有效期为24小时,过期后需要重新登录获取新令牌。

## 技术支持

如有问题,请查看项目文档或联系开发团队。

## 更新日志

### v1.0.0 (2025-01-21)
- 初始版本发布
- 完成所有核心功能模块
- 支持用户认证、作物管理、种植计划等10大功能模块
- 集成JWT认证、Redis缓存、API文档等
