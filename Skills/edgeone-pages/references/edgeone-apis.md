# EdgeOne Functions API 参考

## 目录
- [概览](#概览)
- [Edge Functions API](#edge-functions-api)
- [Node Functions API](#node-functions-api)
- [函数配置和路由](#函数配置和路由)
- [函数限制](#函数限制)
- [代码示例](#代码示例)

---

## 概览

EdgeOne Pages 提供两种计算系统：

| 特性 | Edge Functions | Node Functions |
|------|----------------|----------------|
| 运行环境 | Web 标准 API | 完整 Node.js |
| 延迟 | 极低 | 可能有冷启动 |
| 资源限制 | 较低 | 较高 |
| 适用场景 | 简单逻辑、拦截 | 复杂处理、数据库 |

---

## Edge Functions API

基于 Web 标准 API，类似浏览器环境。

### 标准 Web API

| API | 用途 |
|-----|------|
| `fetch()` | HTTP 请求 |
| `Request` / `Response` | HTTP 请求/响应对象 |
| `Headers` | HTTP 头操作 |
| `URL` / `URLSearchParams` | URL 解析和查询参数 |
| `URLPattern` | URL 路由匹配 |
| `ReadableStream` / `WritableStream` | 流处理 |
| `crypto.subtle` | 加密操作 |
| `TextEncoder` / `TextDecoder` | 文本编解码 |
| `console.log/error/warn` | 日志输出 |
| `setTimeout` / `setInterval` | 定时器 |
| `atob` / `btoa` | Base64 编解码 |

### Request 对象

```typescript
interface Request {
  method: string;           // HTTP 方法
  url: string;              // 请求 URL
  headers: Headers;         // 请求头
  body: ReadableStream;     // 请求体
  json(): Promise<any>;     // 解析 JSON
  text(): Promise<string>;  // 解析文本
  arrayBuffer(): Promise<ArrayBuffer>;
  blob(): Promise<Blob>;
}
```

### Response 构造

```typescript
// 基础响应
new Response(body, init)

// JSON 响应
new Response(JSON.stringify(data), {
  headers: { 'content-type': 'application/json' }
})

// 重定向
Response.redirect(url, status)
```

---

## Node Functions API

提供完整的 Node.js 环境，支持所有内置模块和 npm 生态。

### 内置模块

| 模块 | 用途 |
|------|------|
| `fs` | 文件系统操作 |
| `path` | 路径处理 |
| `crypto` | 加密功能 |
| `http` / `https` | HTTP 服务器/客户端 |
| `stream` | 流处理 |
| `events` | 事件发射器 |
| `buffer` | Buffer 操作 |
| `os` | 操作系统信息 |
| `util` | 实用工具 |
| `querystring` | 查询字符串解析 |
| `url` | URL 解析 |
| `zlib` | 压缩/解压缩 |
| `child_process` | 子进程 |
| `worker_threads` | 工作线程 |

### 常用 npm 包

**数据库：**
- `mysql` / `mysql2` - MySQL
- `pg` - PostgreSQL
- `mongodb` / `mongoose` - MongoDB
- `redis` - Redis
- `sqlite3` - SQLite

**认证：**
- `jsonwebtoken` - JWT
- `bcrypt` / `bcryptjs` - 密码哈希
- `passport` - 认证中间件

**HTTP 客户端：**
- `axios` - HTTP 客户端
- `got` - 轻量级 HTTP 客户端

**图像处理：**
- `sharp` - 高性能图像处理
- `jimp` - 纯 JavaScript 图像处理

**Web 框架：**
- `express` - Express.js
- `koa` - Koa
- `fastify` - Fastify
- `nestjs` - NestJS

---

## 函数配置和路由

### 路由规则

函数文件路径决定 API 路径：

```
文件路径                              API 路径
─────────────────────────────────────────────────────────
edge-functions/hello.ts               /hello
edge-functions/hello/index.ts         /hello
edge-functions/hello/world.ts         /hello/world
edge-functions/api/users/[id].ts      /api/users/123
edge-functions/[...catchAll].ts       /* (捕获所有)
```

### 动态路由

使用方括号 `[param]` 定义动态参数：

```typescript
// edge-functions/api/users/[id].ts
export default async function handler(
  request: Request,
  { params }: { params: { id: string } }
) {
  const userId = params.id;
  // userId = "123" 当访问 /api/users/123
}
```

### 通配路由

```typescript
// edge-functions/api/[...path].ts
export default async function handler(
  request: Request,
  { params }: { params: { path: string[] } }
) {
  // 访问 /api/a/b/c
  // params.path = ['a', 'b', 'c']
}
```

---

## 函数限制

### Edge Functions 限制

| 限制项 | 值 |
|--------|-----|
| 代码大小 | 5 MB（压缩后）|
| 请求体大小 | 1 MB |
| CPU 执行时间 | 200ms/请求（不含等待时间）|
| 不支持 | 原生 Node 模块、文件系统 |

### Node Functions 限制

| 限制项 | 说明 |
|--------|------|
| 代码大小 | 更高限制 |
| 执行时间 | 更长 |
| 环境 | 完整 Node.js |
| 注意 | 冷启动时间 |

---

## 代码示例

### Edge Function - 基础

```typescript
export default async function handler(request: Request) {
  return new Response('Hello from Edge!', {
    headers: { 'content-type': 'text/plain' }
  });
}
```

### Edge Function - JSON API

```typescript
export default async function handler(request: Request) {
  const data = {
    message: 'Hello',
    timestamp: new Date().toISOString()
  };

  return new Response(JSON.stringify(data), {
    headers: { 'content-type': 'application/json' }
  });
}
```

### Edge Function - 请求处理

```typescript
export default async function handler(request: Request) {
  const url = new URL(request.url);
  const method = request.method;

  if (method === 'GET') {
    const id = url.searchParams.get('id');
    return new Response(JSON.stringify({ id }), {
      headers: { 'content-type': 'application/json' }
    });
  }

  if (method === 'POST') {
    const body = await request.json();
    return new Response(JSON.stringify({ received: body }), {
      headers: { 'content-type': 'application/json' }
    });
  }

  return new Response('Method not allowed', { status: 405 });
}
```

### Edge Function - 加密操作

```typescript
export default async function handler(request: Request) {
  // 生成随机值
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);

  // HMAC 签名
  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode('secret'),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );

  const signature = await crypto.subtle.sign(
    'HMAC',
    key,
    new TextEncoder().encode('data')
  );

  return new Response(JSON.stringify({
    random: Array.from(array),
    signature: Array.from(new Uint8Array(signature))
  }), {
    headers: { 'content-type': 'application/json' }
  });
}
```

### Edge Function - 流处理

```typescript
export default async function handler(request: Request) {
  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(new TextEncoder().encode('Hello '));
      controller.enqueue(new TextEncoder().encode('World!'));
      controller.close();
    }
  });

  return new Response(stream, {
    headers: { 'content-type': 'text/plain' }
  });
}
```

### Edge Function - 地理位置

```typescript
export default async function handler(request: Request) {
  // Cloudflare 提供的地理位置头
  const country = request.headers.get('CF-IPCountry');
  const city = request.headers.get('CF-IPCity');

  return new Response(JSON.stringify({
    country,
    city,
    message: country === 'CN' ? '欢迎！' : 'Welcome!'
  }), {
    headers: { 'content-type': 'application/json' }
  });
}
```

### Node Function - 数据库查询

```typescript
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

export default async function handler(request: Request) {
  const { searchParams } = new URL(request.url);
  const userId = searchParams.get('userId');

  try {
    const result = await pool.query(
      'SELECT * FROM users WHERE id = $1',
      [userId]
    );

    if (result.rows.length === 0) {
      return new Response('User not found', { status: 404 });
    }

    return new Response(JSON.stringify(result.rows[0]), {
      headers: { 'content-type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'content-type': 'application/json' }
    });
  }
}
```

### Node Function - 使用 Express

```typescript
import express from 'express';

const app = express();
app.use(express.json());

app.get('/api/users', async (req, res) => {
  // 处理 GET 请求
  res.json({ users: [] });
});

app.post('/api/users', async (req, res) => {
  // 处理 POST 请求
  const user = req.body;
  res.status(201).json(user);
});

export default app;
```
