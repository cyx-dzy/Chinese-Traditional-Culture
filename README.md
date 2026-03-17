# 溯光而行 - 中国古代建筑成就数字展

一个面向大众的中国古代建筑成就数字展，希望通过可视化与交互的方式，让更多人了解木构智慧与营造美学。

## 项目简介

本项目是一个前后端分离的Web应用，展示中国古代建筑的辉煌成就，包括：
- 建筑分类展示（木结构、砖石、园林、法式）
- 建筑详情介绍
- AI智能问答助手
- 历史时间轴
- 数据统计可视化

## 技术栈

### 后端
- **框架**: FastAPI 0.115.0
- **数据库**: MySQL
- **ORM**: SQLAlchemy 2.0.36
- **服务器**: Uvicorn 0.30.5
- **配置管理**: Pydantic Settings

### 前端
- **框架**: Vue 3.5.0
- **构建工具**: Vite 5.4.7
- **路由**: Vue Router 4.4.5
- **HTTP客户端**: Axios 1.7.7
- **语言**: TypeScript 5.6.3

## 环境要求

### 必需软件
- **Python**: 3.8 或更高版本
- **Node.js**: 16.0 或更高版本
- **MySQL**: 5.7 或更高版本
- **Git**: 用于版本控制

### 推荐工具
- **VSCode**: 代码编辑器
- **Postman**: API测试工具
- **MySQL Workbench**: 数据库管理工具

## 快速开始

### 1. 克隆项目

```bash
git clone <项目地址>
cd Chinese-Traditional-Culture
```

### 2. 数据库配置

#### 2.1 创建MySQL数据库

确保MySQL服务正在运行，然后创建数据库：

```sql
CREATE DATABASE IF NOT EXISTS ancient_building 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

#### 2.2 配置数据库连接

数据库配置通过环境变量管理，有以下两种方式：

**方式一：使用.env文件（推荐）**

在项目根目录创建 `.env` 文件：

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=ancient_building
```

**方式二：运行时输入密码**

使用项目提供的启动脚本，运行时会提示输入数据库密码。

### 3. 后端安装

#### 3.1 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 3.2 验证安装

```bash
python -c "import fastapi; print('FastAPI安装成功')"
```

### 4. 前端安装

#### 4.1 安装Node.js依赖

```bash
cd frontend
npm install
```

#### 4.2 验证安装

```bash
npm --version
node --version
```

### 5. 数据导入

项目提供了完整的数据库导入脚本，包括：
- 数据库和表结构创建
- CSV数据导入
- 图片资源配置

**使用启动脚本（推荐）：**

```bash
python start_servers.py
```

脚本会自动：
1. 提示输入数据库密码
2. 创建数据库和表结构
3. 导入所有数据
4. 启动前后端服务器

**手动导入数据：**

```bash
python backend/sql/writh_sql.py
```

### 6. 启动项目

#### 方式一：使用一键启动脚本（推荐）

```bash
python start_servers.py
```

启动脚本会：
1. 提示输入数据库密码
2. 自动导入数据库
3. 同时启动前后端服务器
4. 提供访问地址

#### 方式二：分别启动服务器

**启动后端服务器：**

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**启动前端服务器：**

```bash
cd frontend
npm run dev
```

### 7. 访问应用

启动成功后，可以通过以下地址访问：

- **前端应用**: http://127.0.0.1:5173/
- **后端API**: http://127.0.0.1:8000/
- **API文档**: http://127.0.0.1:8000/docs
- **健康检查**: http://127.0.0.1:8000/health

## 项目结构

```
Chinese-Traditional-Culture/
├── backend/                    # 后端代码
│   ├── routers/              # API路由
│   │   ├── buildings.py      # 建筑相关接口
│   │   ├── faq.py           # 常见问题接口
│   │   └── home.py          # 首页数据接口
│   ├── sql/                  # 数据库脚本和数据
│   │   ├── writh_sql.py     # 数据导入脚本
│   │   ├── buildings.csv      # 建筑数据
│   │   ├── building_details.csv
│   │   ├── images.csv
│   │   └── faq.csv
│   ├── config.py             # 配置管理
│   ├── database.py           # 数据库连接
│   ├── models.py            # 数据模型
│   ├── schemas.py           # Pydantic模型
│   ├── main.py              # FastAPI应用入口
│   └── requirements.txt      # Python依赖
├── frontend/                   # 前端代码
│   ├── src/
│   │   ├── components/      # Vue组件
│   │   │   └── MainLayout.vue
│   │   ├── pages/           # 页面组件
│   │   │   ├── HomePage.vue
│   │   │   ├── CategoryPage.vue
│   │   │   ├── BuildingDetailPage.vue
│   │   │   ├── AIAssistantPage.vue
│   │   │   └── AboutPage.vue
│   │   ├── router/          # 路由配置
│   │   │   └── index.ts
│   │   ├── services/        # API服务
│   │   │   └── api.ts
│   │   ├── App.vue          # 根组件
│   │   ├── main.ts          # 入口文件
│   │   └── styles.css       # 全局样式
│   ├── public/              # 静态资源
│   │   └── image/         # 图片资源
│   ├── package.json         # Node.js依赖
│   ├── vite.config.ts       # Vite配置
│   └── index.html          # HTML入口
├── start_servers.py            # 一键启动脚本
├── README.md                 # 项目说明
└── .env.example              # 环境变量示例
```

## 开发说明

### 后端开发

#### 添加新的API端点

1. 在 `backend/routers/` 中创建或修改路由文件
2. 在 `backend/schemas.py` 中定义数据模型
3. 在 `backend/main.py` 中注册路由

#### 数据库操作

使用SQLAlchemy ORM进行数据库操作：

```python
from sqlalchemy.orm import Session
from .database import get_db
from .models import Building

# 获取数据库会话
db: Session = next(get_db())

# 查询数据
buildings = db.query(Building).all()

# 创建数据
new_building = Building(name="应县木塔", dynasty="辽")
db.add(new_building)
db.commit()
```

### 前端开发

#### 添加新页面

1. 在 `frontend/src/pages/` 中创建页面组件
2. 在 `frontend/src/router/index.ts` 中添加路由
3. 在导航栏中添加链接

#### API调用

使用Axios调用后端API：

```typescript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export async function getBuildings() {
  const response = await axios.get(`${API_BASE_URL}/buildings/`);
  return response.data;
}
```

## 常见问题

### 1. 数据库连接失败

**问题**: `Access denied for user 'root'@'localhost'`

**解决方案**:
- 检查MySQL服务是否运行
- 确认用户名和密码正确
- 检查数据库是否已创建

### 2. 端口被占用

**问题**: `Address already in use`

**解决方案**:
```bash
# 查找占用端口的进程
netstat -ano | findstr :8000

# 结束进程
taskkill /PID <进程ID> /F
```

### 3. 前端依赖安装失败

**问题**: `npm install` 失败

**解决方案**:
```bash
# 清除缓存
npm cache clean --force

# 删除node_modules和package-lock.json
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

### 4. Python依赖安装失败

**问题**: `pip install` 失败

**解决方案**:
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 5. 数据导入失败

**问题**: CSV导入时出现错误

**解决方案**:
- 检查CSV文件编码是否为UTF-8
- 确认CSV文件路径正确
- 查看错误日志定位具体问题

## 部署说明

### 生产环境配置

1. **修改配置**:
   - 设置生产数据库连接
   - 配置CORS允许的域名
   - 关闭debug模式

2. **构建前端**:
```bash
cd frontend
npm run build
```

3. **部署后端**:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue
- 发送邮件
- 项目讨论区

## 致谢

感谢所有为本项目做出贡献的开发者和设计师！

---

**项目名称**: 溯光而行  
**项目描述**: 中国古代建筑成就数字展  
**技术支持**: FastAPI + Vue 3 + MySQL  
**最后更新**: 2024年