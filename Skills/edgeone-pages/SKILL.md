---
name: edgeone-pages-best-practice
description: 指导 AI 生成符合 EdgeOne Pages 平台规范的代码，支持 SSG/SSR/ISR、Edge Functions 和 Node Functions。当用户需要创建或改造部署到 EdgeOne Pages 的 Web 项目、询问 EdgeOne 开发规范、或需要选择 Edge/Node Functions 时触发此技能。
---

# EdgeOne Pages 代码生成指南

## 核心职责

生成符合 EdgeOne Pages 平台规范的代码，包括：
- 智能判断功能应部署为 Edge Functions 或 Node Functions
- 遵循 EdgeOne 项目结构和代码规范
- 生成安全、高性能的代码

## 快速判断：Edge vs Node Functions

| 场景 | 选择 |
|------|------|
| 请求拦截、A/B测试、地理位置路由、简单认证 | **Edge Functions** |
| 数据库操作、文件处理、图像处理、复杂逻辑 | **Node Functions** |
| 静态页面展示、UI组件 | **前端代码** |

**关键词判断**：
- Edge: 拦截、路由、转发、缓存、验证、中间件
- Node: 数据库、文件、图像、支付、复杂处理

## 代码生成规范

### 1. 项目结构检测

**前端框架检测：**
- `src/app/` → Next.js App Router (src目录)
- `app/` (根级) → Next.js App Router
- `src/` (无app) → React/Vue SPA
- `pages/` → Next.js Pages Router
- `gatsby-config.js` → Gatsby
- `vite.config.ts` → Vite
- `nuxt.config.ts` → Nuxt

**函数类型检测：**
- `edge-functions/` → Edge Functions 项目
- `node-functions/` → Node Functions 项目
- `functions/` → Legacy Functions（默认 Edge）

### 2. 输出格式

始终使用独立代码块，标注完整文件路径：

````markdown
**文件：`edge-functions/api/hello.ts`**
```typescript
// 代码内容
```
````

### 3. 代码标准

- 默认使用 TypeScript
- 必须导入所有使用的方法
- Edge Functions 使用 ES 模块
- Node Functions 可用 CommonJS 或 ES 模块
- 使用环境变量存储密钥
- 包含错误处理

## 参考资源

| 资源 | 用途 | 何时读取 |
|------|------|----------|
| [quick-reference.md](references/quick-reference.md) | 快速查找常用代码片段和限制 | 需要快速参考时 |
| [edgeone-apis.md](references/edgeone-apis.md) | Edge/Node Functions API 详细列表 | 需要了解支持的 API 时 |
| [edgeone-best-practices.md](references/edgeone-best-practices.md) | 架构选择、性能优化、安全实践 | 需要深入最佳实践时 |

## 函数限制速查

**Edge Functions：**
- 代码大小：5 MB（压缩后）
- 请求体：1 MB
- CPU 时间：200ms/请求

**Node Functions：**
- 更高资源限制
- 完整 Node.js 环境
- 注意冷启动时间

## 示例

### 示例 1：用户注册 API

用户请求："创建用户注册功能"

分析：
- 关键词"注册"→ 需要 functions
- 涉及数据库 → Node Functions

输出：
- `node-functions/api/register.ts` - 处理注册逻辑
- `src/app/register/page.tsx` - 前端注册页面

### 示例 2：请求日志中间件

用户请求："添加请求日志功能"

分析：
- 请求拦截 → Edge Functions

输出：
- `edge-functions/middleware/logging.ts`

### 示例 3：产品展示页面

用户请求："创建产品展示页面"

分析：
- 纯展示 → 前端代码

输出：
- `src/app/products/page.tsx`
