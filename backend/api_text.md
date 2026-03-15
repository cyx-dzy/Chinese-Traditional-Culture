## 后端接口测试说明（Postman）

本项目后端基于 **FastAPI**，默认运行在 `http://localhost:8000`。  
你可以使用 **Postman** 对每个接口进行调试和验证。

---

## 一、准备工作

- **确认环境**
  - 已安装 Python 及依赖：
    ```bash
    cd d:\desktop\笔记用的\计算机设计大赛\project\Chinese-Traditional-Culture
    pip install -r backend/requirements.txt
    ```
  - MySQL 已启动，且存在数据库：
    - 数据库名：`ancient_building`
    - 用户名：`root`
    - 密码：请运行时输入
    - 端口：`3306`
  - 四张表已按提供的 SQL 创建完成。
  - 四个 CSV 已放在项目根目录（与 `backend` 同级）：
    - `buildings.csv`
    - `building_details.csv`
    - `images.csv`
    - `faq.csv`

- **导入初始数据（可选但强烈推荐）**
  ```bash
  cd d:\desktop\笔记用的\计算机设计大赛\project\Chinese-Traditional-Culture
  python backend/sql/writh_sql.py
  ```

- **启动后端服务**
  ```bash
  uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
  ```

  看到控制台显示类似：
  - `Application startup complete`
  - `Uvicorn running on http://0.0.0.0:8000`

---

## 二、在 Postman 中创建基础环境

1. 打开 **Postman**。
2. 左侧点击 **Collections（集合）** → `New Collection`。
3. 集合命名为：`Chinese-Traditional-Culture API`（或任意名称）。
4. 在上方导航栏点击 **Environments**（齿轮图标）→ `Add` 新建环境：
   - 名称：`Local Backend`
   - 变量：
     - `base_url` → 初始值：`http://localhost:8000`
   - 保存环境，并在右上角环境下拉框中选中 `Local Backend`。

后续所有请求统一使用：
- `{{base_url}}` 作为服务器地址。

---

## 三、接口清单与 Postman 测试步骤

### 1. 健康检查接口（确认服务是否正常）

- **接口信息**
  - 方法：`GET`
  - 路径：`/health`
  - 完整 URL：`{{base_url}}/health`

- **Postman 操作步骤**
  1. 在集合 `Chinese-Traditional-Culture API` 上点右键 → `Add Request`。
  2. 请求命名为：`Health Check`。
  3. 在 URL 输入框中填写：`{{base_url}}/health`。
  4. 方法选择 `GET`。
  5. 点击 `Send`。
  6. 预期返回（Status 200）：
     ```json
     {
       "status": "ok"
     }
     ```

---

### 2. 首页数据接口 `/home/`

- **接口信息**
  - 方法：`GET`
  - 路径：`/home/`
  - 完整 URL：`{{base_url}}/home/`
  - 说明：用于首页展示高亮建筑、统计数据、FAQ 预览。

- **Postman 操作步骤**
  1. 在集合中新增请求：`Home Data`。
  2. 方法选择 `GET`。
  3. URL：`{{base_url}}/home/`。
  4. 无需填写参数或 Body。
  5. 点击 `Send`。
  6. 预期返回示例结构（字段可能根据数据有所不同）：
     ```json
     {
       "highlights": [
         {
           "id": 1,
           "name": "应县木塔",
           "name_en": "Yingxian Wooden Pagoda",
           "dynasty": "辽",
           "location": "山西应县",
           "category": "木结构",
           "summary": "世界最高的纯木塔……",
           "cover_image": "/images/yingxian/cover.jpg",
           "height": 67.31,
           "bay_count": "九间",
           "dougong_types": "54种",
           "earthquake_resistance": "经历40余次地震",
           "material": "木",
           "preservation_status": "完好"
         }
       ],
       "stats": {
         "total_buildings": 10,
         "by_category": {
           "木结构": 3,
           "砖石": 3,
           "园林": 2,
           "法式": 2
         },
         "by_dynasty": {
           "唐": 2,
           "宋": 3
         }
       },
       "faq_preview": [
         {
           "id": 1,
           "question": "为什么中国古建筑不用钉子？",
           "answer": "因为使用榫卯结构……"
         }
       ]
     }
     ```

---

### 3. 建筑列表接口 `/buildings/`

用于「分类列表页」「首页搜索」「按朝代筛选」等场景。

- **接口信息**
  - 方法：`GET`
  - 路径：`/buildings/`
  - 完整 URL：`{{base_url}}/buildings/`

- **支持的查询参数（Query Params）**
  - `category`（可选）：建筑分类（`木结构` / `砖石` / `园林` / `法式`）。
  - `dynasty`（可选）：朝代，如 `唐`、`宋`、`明清` 等。
  - `keyword`（可选）：搜索关键字，匹配名称、英文名、简介。
  - `skip`（可选）：分页偏移，默认 `0`。
  - `limit`（可选）：每页数量，默认 `20`，最大 `100`。

- **Postman 操作步骤：基础请求（无筛选）**
  1. 新建请求命名：`List Buildings - All`。
  2. 方法：`GET`。
  3. URL：`{{base_url}}/buildings/`。
  4. 切换到 `Params` 标签页，暂时不填。
  5. 点击 `Send`。
  6. 返回示例（数组）：
     ```json
     [
       {
         "id": 1,
         "name": "应县木塔",
         "name_en": "Yingxian Wooden Pagoda",
         "dynasty": "辽",
         "location": "山西应县",
         "category": "木结构",
         "summary": "世界最高的纯木塔……",
         "cover_image": "/images/yingxian/cover.jpg",
         "height": 67.31,
         "bay_count": "九间",
         "dougong_types": "54种",
         "earthquake_resistance": "经历40余次地震",
         "material": "木",
         "preservation_status": "完好"
       }
     ]
     ```

- **测试 1：按分类筛选**
  1. 复制请求，重命名：`List Buildings - 木结构`。
  2. 在 `Params` 中增加：
     - Key：`category`，Value：`木结构`。
  3. 点击 `Send`。
  4. 检查返回的每条数据的 `category` 是否为 `木结构`。

- **测试 2：按朝代筛选**
  1. 新建/复制请求：`List Buildings - 唐代`。
  2. `Params`：
     - `dynasty` = `唐`。
  3. 点击 `Send`，检查 `dynasty` 字段。

- **测试 3：关键字搜索**
  1. 新建/复制请求：`List Buildings - Keyword`。
  2. `Params`：
     - `keyword` = `木塔`（或你数据中存在的名称片段）。
  3. `Send`，观察结果是否只包含匹配关键字的建筑。

- **测试 4：分页**
  1. `Params`：
     - `skip` = `0`
     - `limit` = `5`
  2. `Send` → 应返回最多 5 条。
  3. 修改为：
     - `skip` = `5`
     - `limit` = `5`
  4. 再次 `Send`，确认数据发生位移。

---

### 4. 建筑详情接口 `/buildings/{building_id}`

用于「建筑详情页」的数据加载。

- **接口信息**
  - 方法：`GET`
  - 路径：`/buildings/{building_id}`
  - 示例 URL：`{{base_url}}/buildings/1`

- **Postman 操作步骤**
  1. 确认在「建筑列表接口」中能看到至少一个建筑的 `id`（例如 `1`）。
  2. 新建请求：`Get Building Detail`。
  3. 方法：`GET`。
  4. URL：`{{base_url}}/buildings/1`（将 `1` 替换为实际存在的 `id`）。
  5. 点击 `Send`。
  6. 预期返回示例结构：
     ```json
     {
       "id": 1,
       "name": "应县木塔",
       "name_en": "Yingxian Wooden Pagoda",
       "dynasty": "辽",
       "location": "山西应县",
       "category": "木结构",
       "summary": "世界最高的纯木塔……",
       "cover_image": "/images/yingxian/cover.jpg",
       "height": 67.31,
       "bay_count": "九间",
       "dougong_types": "54种",
       "earthquake_resistance": "经历40余次地震",
       "material": "木",
       "preservation_status": "完好",
       "images": [
         {
           "id": 1,
           "image_path": "/images/yingxian/full_1.jpg",
           "image_type": "全景",
           "caption": "应县木塔全景"
         }
       ],
       "details": [
         {
           "id": 1,
           "section_type": "history",
           "title": "建造背景",
           "content": "应县木塔建于……"
         }
       ],
       "related_buildings": [
         {
           "id": 2,
           "name": "佛光寺东大殿",
           "name_en": "Foguang Temple East Hall",
           "dynasty": "唐",
           "location": "山西五台",
           "category": "木结构",
           "summary": "梁思成称其为“中国第一国宝”……",
           "cover_image": "/images/foguang/cover.jpg",
           "height": 20.00,
           "bay_count": "七间",
           "dougong_types": "七铺作",
           "earthquake_resistance": null,
           "material": "木",
           "preservation_status": "完好"
         }
       ]
     }
     ```

- **错误情况测试**
  - 将 URL 改为不存在的 ID，例如：`{{base_url}}/buildings/99999`
  - 点击 `Send`。
  - 预期返回状态码 `404`，Body：
    ```json
    {
      "detail": "建筑不存在"
    }
    ```

---

### 5. FAQ 接口 `/faq/`

用于「AI 问答页左侧常见问题列表」或首页预设问题区。

- **接口信息**
  - 方法：`GET`
  - 路径：`/faq/`
  - URL：`{{base_url}}/faq/`

- **Postman 操作步骤**
  1. 新建请求：`List FAQ`。
  2. 方法：`GET`。
  3. URL：`{{base_url}}/faq/`。
  4. 点击 `Send`。
  5. 预期返回示例：
     ```json
     [
       {
         "id": 1,
         "question": "为什么中国古建筑不用钉子？",
         "answer": "因为采用榫卯结构，利用木材的弹性和形状配合……"
       },
       {
         "id": 2,
         "question": "什么是斗拱？",
         "answer": "斗拱是中国古建筑中承重与装饰兼具的构件……"
       }
     ]
     ```

---

## 四、快速验证：使用内置文档（可选）

除了 Postman，也可以使用 FastAPI 自带文档做快速检查：

- 打开浏览器访问：
  - `http://localhost:8000/docs`（Swagger UI）
  - `http://localhost:8000/redoc`（ReDoc 文档）
- 在页面中可以：
  - 展开各个接口 → `Try it out` → 填写参数 → `Execute`。
  - 查看请求 URL、返回示例和实际返回值。

---

## 五、常见问题排查

- **1. Postman 返回 `500` 或连接失败**
  - 检查终端中 `uvicorn` 是否在运行。
  - 确认 MySQL 已启动，账号密码与 `backend/config.py` 中保持一致。
  - 如修改了数据库连接信息，可在项目根目录新建 `.env` 文件覆盖：
    ```env
    db_host=127.0.0.1
    db_port=3306
    db_user=root
    db_password=your_password
    db_name=ancient_building
    ```
  - 重启 `uvicorn`。

- **2. 返回数据为空数组 `[]`**
  - 检查是否已经成功执行 `python backend/sql/writh_sql.py`。
  - 在 MySQL 中确认对应表的记录是否存在（例如 `SELECT * FROM buildings;`）。

- **3. CORS 相关问题（前端开发调试时）**
  - 后端已在 `backend/main.py` 中启用了 CORS，默认允许所有来源。
  - 如果你修改了 CORS 配置，请确保前端域名在允许列表中。

---

按照以上步骤配置 Postman 后，你可以方便地对每个接口进行测试，也为前端联调提供清晰的参考。  
后续如果新增接口（例如 AI 聊天接口），建议在本文件中继续补充说明与测试方法。

