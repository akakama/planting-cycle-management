# 种植周期管理系统 - 前端

基于 Vue 3 + Element Plus + Vite 的种植周期管理系统前端应用。

## 技术栈

- **框架**: Vue 3.4.0
- **UI组件库**: Element Plus 2.4.4
- **构建工具**: Vite 5.0.0
- **状态管理**: Pinia 2.1.7
- **路由管理**: Vue Router 4.2.5
- **HTTP客户端**: Axios 1.6.0
- **图表库**: ECharts 5.4.3
- **样式预处理**: SCSS

## 功能模块

- **资源管理**: 作物列表、地块列表
- **种植规划**: 种植计划列表、种植日历
- **物候期监测**: 物候期记录、环境监测、病虫害管理
- **农资管理**: 农资管理
- **采收管理**: 采收记录
- **产量预估**: 产量预估
- **AI智能问答**: AI聊天

## 安装依赖

```bash
npm install
```

## 环境配置

复制 `.env.example` 为 `.env.development`（开发环境）或 `.env.production`（生产环境），并根据实际情况修改配置：

```bash
cp .env.example .env.development
```

环境变量说明：

- `VITE_BASE_API`: 后端API基础URL
- `VITE_UPLOAD_URL`: 文件上传URL
- `VITE_APP_TITLE`: 应用标题
- `NODE_ENV`: 环境配置

## 开发模式运行

```bash
npm run dev
```

访问 http://localhost:5173

## 生产环境构建

```bash
npm run build
```

构建产物将生成在 `dist` 目录中。

## 预览生产构建

```bash
npm run preview
```

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API接口
│   │   ├── request.js     # Axios封装
│   │   ├── auth.js        # 认证接口
│   │   ├── crop.js        # 作物接口
│   │   ├── plot.js        # 地块接口
│   │   └── ...
│   ├── assets/            # 资源文件
│   ├── components/        # 公共组件
│   │   ├── ListLayout.vue     # 列表布局组件
│   │   ├── FormDialog.vue     # 表单对话框组件
│   │   ├── ImageUpload.vue    # 图片上传组件
│   │   └── StatusTag.vue      # 状态标签组件
│   ├── router/            # 路由配置
│   │   └── index.js
│   ├── store/             # 状态管理
│   │   └── user.js
│   ├── styles/            # 全局样式
│   │   └── global.scss
│   ├── views/             # 页面组件
│   │   ├── login/         # 登录页
│   │   ├── layout/        # 布局组件
│   │   ├── resource/      # 资源管理
│   │   ├── planning/      # 种植规划
│   │   ├── phenology/     # 物候期监测
│   │   ├── material/      # 农资管理
│   │   ├── harvest/       # 采收管理
│   │   ├── yield/         # 产量预估
│   │   └── ai-chat/       # AI智能问答
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── .env.example           # 环境变量示例
├── .env.development       # 开发环境配置
├── .env.production        # 生产环境配置
├── index.html             # HTML模板
├── package.json           # 项目依赖
└── vite.config.js         # Vite配置
```

## 开发说明

### API接口封装

所有API接口都在 `src/api/` 目录下，使用统一的request实例：

```javascript
import request from './request'

export const cropApi = {
  getList(params) {
    return request({ url: '/crops', method: 'get', params })
  },
  add(data) {
    return request({ url: '/crops', method: 'post', data })
  }
}
```

### 状态管理

使用Pinia进行状态管理，用户状态存储在 `src/store/user.js`：

```javascript
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
userStore.login(username, password)
```

### 路由配置

路由配置在 `src/router/index.js`，包含路由守卫和懒加载：

```javascript
const routes = [
  {
    path: '/resource/crops',
    name: 'Crops',
    component: () => import('@/views/resource/CropList.vue')
  }
]
```

### 公共组件

项目中提供了多个公共组件，可以在页面中直接使用：

- `ListLayout`: 列表页面布局组件
- `FormDialog`: 表单对话框组件
- `ImageUpload`: 图片上传组件
- `StatusTag`: 状态标签组件

### 样式规范

全局样式定义在 `src/styles/global.scss`，包含：

- 主题色变量
- 全局样式重置
- 组件样式优化
- 工具类
- 响应式设计

## 注意事项

1. **后端API**: 确保后端服务正常运行，默认端口为8082
2. **登录认证**: 所有API请求（除登录外）都需要JWT Token
3. **图片上传**: 当前使用URL方式，实际使用时需要对接文件上传API
4. **ECharts**: 环境监测页面使用了ECharts，确保已正确安装
5. **图标**: 部分页面使用了Element Plus图标，确保已正确安装

## 浏览器支持

- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

## 许可证

MIT

## 联系方式

如有问题，请联系开发团队。
