# mkdocs-shadcn 排版示例

## 示例 1：书籍序言页面

```markdown
---
title: 序言
summary: 本书序言，阐述AI编程教程的写作初衷与背景
new: false
show_datetime: false
---

> 送给即将与AI同行的人们

在此，我将我的一切所学倾囊相授...

## 你能从这本书中获得什么
---

- **理解AI编程的概念并快速上手**
- **亲手为自己定制一份实用工具**
- **学习AI编程的高阶技巧**

## 赠语
---

编程的本质从未改变...

<p align="center"><strong>亲爱的同志们，不要成为我，要超越我。</strong></p>
```

## 示例 2：技术教程页面

```markdown
---
title: 快速上手
summary: 5分钟快速上手AI编程，完成环境配置与第一个程序
new: false
show_datetime: false
---

# 快速上手

本文将带你5分钟快速上手AI编程。

## 环境准备
---

### 安装依赖

/// tab | pip
```bash
pip install openai
```
///

/// tab | uv
```bash
uv add openai
```
///

/// tab | poetry
```bash
poetry add openai
```
///

### 配置API密钥

!!! warning "安全提示"
    请勿将API密钥硬编码在代码中，建议使用环境变量。

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

## 第一个程序
---

!!! tip "提示"
    保持提示词简洁明了，描述你想要的结果即可。

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "写一个Python函数，计算斐波那契数列"}
    ]
)
print(response.choices[0].message.content)
```

## 常见问题
---

/// details | API密钥无效怎么办？
1. 检查密钥是否正确复制
2. 确认环境变量已设置
3. 检查账户余额是否充足
///

/// details | 如何降低API成本？
- 使用更便宜的模型（如gpt-3.5-turbo）
- 限制输出token数量
- 使用缓存避免重复请求
///
```

## 示例 3：API文档页面

```markdown
---
title: API参考
summary: 完整的API接口文档，包含认证、接口列表与错误码说明
new: false
show_datetime: false
---

# API参考

## 认证
---

所有API请求需要在Header中携带认证信息：

```
Authorization: Bearer YOUR_API_KEY
```

!!! danger "重要"
    API密钥具有完全访问权限，请妥善保管，不要在客户端暴露。

## 接口列表
---

### 获取用户信息

```http
GET /api/v1/user
```

**响应示例**：

```json
{
  "id": 123,
  "name": "张三",
  "email": "zhangsan@example.com"
}
```

### 更新用户信息

```http
POST /api/v1/user
Content-Type: application/json

{
  "name": "李四"
}
```

## 错误码
---

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查请求参数格式 |
| 401 | 未授权 | 检查API密钥 |
| 404 | 资源不存在 | 检查资源ID |
| 500 | 服务器错误 | 稍后重试 |
```

## 示例 4：多步骤教程

```markdown
---
title: 项目实战
summary: 从零开始构建一个完整的待办事项应用，学习AI编程实战技巧
new: false
show_datetime: false
---

# 项目实战

本教程将带你从零开始构建一个待办事项应用。

## 第一阶段：需求分析
---

[==25%]

### 目标

构建一个支持以下功能的待办应用：

- [x] 添加任务
- [x] 标记完成
- [ ] 设置提醒
- [ ] 数据同步

### 技术选型

/// details | 前端技术栈
- React 18
- Tailwind CSS
- shadcn/ui组件库
///

/// details | 后端技术栈
- Python FastAPI
- PostgreSQL
- Redis缓存
///

## 第二阶段：项目搭建
---

[==50%]

!!! tip "最佳实践"
    使用虚拟环境隔离项目依赖。

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## 第三阶段：核心功能
---

[==75%]

待补充...

## 第四阶段：部署上线
---

[==100%]

!!! success "完成"
    恭喜你完成了整个项目！
```

## 示例 5：数学公式展示

```markdown
---
title: 算法原理
summary: 核心算法的数学原理
description: 详解算法背后的数学公式
keywords: 算法, 数学, 原理
order: 3
---

# 算法原理

## 线性回归
---

线性回归模型的目标是最小化损失函数：

$$
J(\theta) = \frac{1}{2m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})^2
$$

其中：
- $m$ 是样本数量
- $h_\theta(x)$ 是假设函数
- $y$ 是真实值

## 梯度下降
---

参数更新公式：

$$
\theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta)
$$

学习率 $\alpha$ 的选择很重要：

- 太大：可能无法收敛
- 太小：收敛速度太慢

!!! note "公式说明"
    上述公式中的 $:=$ 表示赋值操作。
```

## 示例 6：对比表格

```markdown
---
title: 方案对比
summary: 不同方案的优缺点对比
description: 详细对比各方案的优劣
keywords: 对比, 方案, 选择
order: 4
---

# 方案对比

## 技术方案对比
---

| 方案 | 优点 | 缺点 | 适用场景 |
|:-----|:-----|:-----|:---------|
| 方案A | 简单易用 | 功能有限 | 小型项目 |
| 方案B | 功能丰富 | 学习曲线陡 | 大型项目 |
| 方案C | 性能优秀 | 社区较小 | 高性能需求 |

## 成本对比
---

!!! info "说明"
    以下成本估算基于月均使用量。

| 项目 | 方案A | 方案B | 方案C |
|:-----|------:|------:|------:|
| 服务器 | ¥200 | ¥500 | ¥300 |
| 存储 | ¥50 | ¥100 | ¥80 |
| 总计 | ¥250 | ¥600 | ¥380 |

## 推荐方案
---

!!! tip "建议"
    对于初创团队，建议选择**方案A**快速验证想法，后期再迁移到方案B。
```

## 示例 7：常见误区（使用 Details 折叠）

```markdown
## 常见误区
---

/// details | 误区一：把用户群体当用户个体
"年轻人"不是用户，"25岁在上海工作的产品经理小王"才是用户。

群体是统计概念，个体才能指导设计。
///

/// details | 误区二：描述人口属性而非使用场景
"28岁女性"不如"每天通勤1小时、想利用这段时间学点东西的上班族"有用。

年龄性别只是标签，使用场景才能指导功能。
///

/// details | 误区三：用户≠付费者
做给老板看的数据报告，用户是老板，不是你自己。

搞清楚谁真正在用，才能做出他们真正需要的东西。
///
```

**效果说明**：常见误区类内容适合用 `/// details` 逐个折叠，读者可以根据兴趣展开查看，不会让主要内容显得冗长。

## 排版决策参考

| 场景 | 推荐语法 | 示例 |
|------|----------|------|
| 重要语句/赠语 | 居中加粗 | `<p align="center"><strong>文字</strong></p>` |
| 章节分隔 | 标题+分割线 | `## 标题` + `---` |
| 补充说明 | Note提示框 | `!!! note` |
| 警告信息 | Warning提示框 | `!!! warning` |
| 危险操作 | Danger提示框 | `!!! danger` |
| 技巧建议 | Tip提示框 | `!!! tip` |
| 常见误区 | Details折叠 | `/// details \| 误区X：...` |
| 可选阅读 | Details折叠 | `/// details` |
| 多平台说明 | Tab标签页 | `/// tab` |
| 进度展示 | 进度条 | `[==50%]` |
| 数学公式 | Katex | `$公式$` 或 `$$公式$$` |
