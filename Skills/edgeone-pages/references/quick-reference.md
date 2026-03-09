# EdgeOne Pages 快速参考

## 目录
- [函数类型选择](#函数类型选择)
- [函数限制](#函数限制)
- [路由规则](#路由规则)
- [代码模板](#代码模板)
- [常用 API](#常用-api)

---

## 函数类型选择

### 使用 Edge Functions 的场景
- 请求/响应拦截和修改
- A/B 测试、功能标志
- 地理位置路由、IP 过滤
- 简单的认证验证
- 请求转发、代理
- 响应缓存控制

### 使用 Node Functions 的场景
- 复杂的数据库操作
- 文件系统操作
- 图像/视频处理
- 机器学习推理
- 长时间运行的任务
- 需要完整 Node.js 生态

---

## 函数限制

| 限制项 | Edge Functions | Node Functions |
|--------|----------------|----------------|
| 代码大小 | 5 MB (压缩后) | 更高限制 |
| 请求体大小 | 1 MB | 更高限制 |
| CPU 执行时间 | 200ms/请求 | 更长 |
| 环境 | Web 标准 API | 完整 Node.js |

---

## 路由规则

函数使用文件路径作为 API 路径：

```
edge-functions/hello.ts           → /hello
edge-functions/api/users.ts       → /api/users
edge-functions/api/users/[id].ts  → /api/users/123 (动态路由)
node-functions/api/order.ts       → /api/order
```

---

## 代码模板

### Edge Function 基础模板

```typescript
// edge-functions/api/hello.ts
export default async function handler(request: Request) {
  const url = new URL(request.url);
  const name = url.searchParams.get('name') || 'World';

  return new Response(JSON.stringify({
    message: `Hello, ${name}!`
  }), {
    headers: { 'content-type': 'application/json' }
  });
}
```

### Edge Function - 带错误处理

```typescript
// edge-functions/api/hello.ts
export default async function handler(request: Request) {
  try {
    const body = await request.json();

    return new Response(JSON.stringify({ success: true, data: body }), {
      headers: { 'content-type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({
      error: 'Invalid request'
    }), {
      status: 400,
      headers: { 'content-type': 'application/json' }
    });
  }
}
```

### Node Function 基础模板

```typescript
// node-functions/api/users.ts
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

export default async function handler(request: Request) {
  try {
    const result = await pool.query('SELECT * FROM users LIMIT 10');

    return new Response(JSON.stringify(result.rows), {
      headers: { 'content-type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({
      error: error.message
    }), {
      status: 500,
      headers: { 'content-type': 'application/json' }
    });
  }
}
```

### 动态路由

```typescript
// edge-functions/api/users/[id].ts
export default async function handler(
  request: Request,
  { params }: { params: { id: string } }
) {
  const userId = params.id;

  return new Response(JSON.stringify({ userId }), {
    headers: { 'content-type': 'application/json' }
  });
}
```

### 中间件/拦截器

```typescript
// edge-functions/middleware/auth.ts
export default async function handler(request: Request) {
  const token = request.headers.get('Authorization');

  if (!token) {
    return new Response('Unauthorized', { status: 401 });
  }

  // 添加用户信息到请求头
  const modifiedRequest = new Request(request, {
    headers: {
      ...request.headers,
      'X-User-ID': 'user-123'
    }
  });

  return fetch(modifiedRequest);
}
```

---

## 常用 API

### Edge Functions 支持的 API

**Web 标准 API：**
- `fetch()`, `Request`, `Response`, `Headers`
- `URL`, `URLPattern`, `URLSearchParams`
- `ReadableStream`, `WritableStream`, `TransformStream`
- `crypto.subtle`, `crypto.getRandomValues()`
- `TextEncoder`, `TextDecoder`
- `console.log()`, `console.error()`
- `setTimeout()`, `setInterval()`
- `atob()`, `btoa()`
- `JSON.parse()`, `JSON.stringify()`

### Node Functions 支持的模块

**常用内置模块：**
- `fs` - 文件系统
- `path` - 路径处理
- `crypto` - 加密
- `http`, `https` - HTTP 服务器
- `stream` - 流处理
- `buffer` - Buffer 操作
- `os`, `util`, `querystring`, `url`, `zlib`

**常用 npm 包：**
- `express`, `koa`, `fastify` - Web 框架
- `pg`, `mysql2`, `mongodb`, `mongoose` - 数据库
- `redis` - 缓存
- `jsonwebtoken`, `bcrypt` - 认证
- `sharp` - 图像处理
- `axios`, `got` - HTTP 客户端

---

## 安全速查

### 环境变量
```typescript
// ✅ 正确
const API_KEY = process.env.API_KEY;

// ❌ 错误
const API_KEY = 'hardcoded-key';
```

### CORS 配置
```typescript
export default async function handler(request: Request) {
  const allowedOrigins = ['https://example.com'];
  const origin = request.headers.get('origin');

  if (allowedOrigins.includes(origin || '')) {
    return new Response('...', {
      headers: {
        'Access-Control-Allow-Origin': origin || '',
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      }
    });
  }
}
```

### 安全头
```typescript
const response = new Response('...');
response.headers.set('X-Content-Type-Options', 'nosniff');
response.headers.set('X-Frame-Options', 'DENY');
response.headers.set('Strict-Transport-Security', 'max-age=31536000');
return response;
```

---

## 性能优化速查

### Edge Functions
- 最小化代码体积，避免大型依赖
- 使用标准 Web API（fetch 而非 axios）
- 使用 `Promise.all()` 并行处理

### Node Functions
- 使用数据库连接池
- 实现缓存策略
- 优化数据库查询（索引、分页）

---

## 本地开发命令

```bash
# 前端开发服务器
npm run dev

# 函数开发服务器
edgeone pages dev
```
