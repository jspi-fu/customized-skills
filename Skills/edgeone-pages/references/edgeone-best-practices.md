# EdgeOne Pages 最佳实践

## 目录
- [架构选择](#架构选择)
- [性能优化](#性能优化)
- [安全最佳实践](#安全最佳实践)
- [代码组织](#代码组织)
- [错误处理和日志](#错误处理和日志)
- [测试和部署](#测试和部署)
- [常见场景](#常见场景)

---

## 架构选择

### 渲染模式对比

| 模式 | 适用场景 | 优势 | 劣势 |
|------|----------|------|------|
| **SSG** | 营销页、博客、文档 | 最快加载、最佳 SEO、最低成本 | 内容静态 |
| **SSR** | 实时数据、个性化 | 最新数据、良好 SEO | 较高延迟、较高成本 |
| **ISR** | 新闻、产品目录 | 接近 SSG 性能、定期更新 | 配置复杂度 |
| **CSR** | 仪表盘、后台管理 | 最佳交互体验 | 不利于 SEO |

### 函数类型选择

**使用 Edge Functions：**
- 请求/响应拦截和修改
- A/B 测试、功能标志
- 地理位置路由、IP 过滤
- 简单的认证验证
- 请求转发、代理
- 响应缓存控制

**使用 Node Functions：**
- 复杂的数据库操作
- 文件系统操作
- 图像/视频处理
- 机器学习推理
- 长时间运行的任务

---

## 性能优化

### Edge Functions 优化

**1. 最小化代码体积**
```typescript
// ❌ 不好：导入整个库
import _ from 'lodash';

// ✅ 好：只导入需要的函数
import { debounce } from 'lodash';
```

**2. 使用标准 Web API**
```typescript
// ✅ 使用 fetch
const response = await fetch(url);

// ❌ 避免 axios（增加体积）
import axios from 'axios';
```

**3. 并行处理**
```typescript
// ✅ 并行请求
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);
```

**4. 简单缓存**
```typescript
const cache = new Map();

export default async function handler(request: Request) {
  const key = request.url;
  if (cache.has(key)) {
    return cache.get(key);
  }
  // ... 获取数据
  cache.set(key, response);
  return response;
}
```

### Node Functions 优化

**1. 数据库连接池**
```typescript
import { Pool } from 'pg';

// 全局连接池，不要每个请求创建新连接
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000
});
```

**2. 使用 Redis 缓存**
```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

export default async function handler(request: Request) {
  const cached = await redis.get('key');
  if (cached) {
    return new Response(cached);
  }
  // ... 获取数据
  await redis.setex('key', 3600, data);
}
```

**3. 查询优化**
- 使用索引
- 只查询需要的字段
- 使用分页

```typescript
// ✅ 分页查询
const page = parseInt(url.searchParams.get('page') || '1');
const limit = 20;
const offset = (page - 1) * limit;

const result = await pool.query(
  'SELECT id, name FROM users LIMIT $1 OFFSET $2',
  [limit, offset]
);
```

### 前端优化

**1. 代码分割**
```typescript
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Loading />
});
```

**2. 图片优化**
```typescript
import Image from 'next/image';

<Image
  src="/image.jpg"
  alt="Description"
  width={800}
  height={600}
  loading="lazy"
/>
```

---

## 安全最佳实践

### 1. 环境变量管理

```typescript
// ❌ 不要硬编码
const API_KEY = 'sk-1234567890abcdef';

// ✅ 使用环境变量
const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error('API_KEY is not configured');
}
```

### 2. 输入验证

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  age: z.number().min(18).max(120)
});

export default async function handler(request: Request) {
  const body = await request.json();

  try {
    const validated = UserSchema.parse(body);
    // 处理验证后的数据
  } catch (error) {
    return new Response(JSON.stringify({ error: 'Invalid input' }), {
      status: 400,
      headers: { 'content-type': 'application/json' }
    });
  }
}
```

### 3. SQL 注入防护

```typescript
// ❌ 不要拼接 SQL
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ 使用参数化查询
const query = 'SELECT * FROM users WHERE id = $1';
const result = await pool.query(query, [userId]);
```

### 4. CORS 配置

```typescript
export default async function handler(request: Request) {
  const allowedOrigins = ['https://example.com', 'https://app.example.com'];
  const origin = request.headers.get('origin');

  if (allowedOrigins.includes(origin || '')) {
    return new Response('...', {
      headers: {
        'Access-Control-Allow-Origin': origin || '',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      }
    });
  }

  return new Response('Unauthorized', { status: 403 });
}
```

### 5. 安全头设置

```typescript
export default async function handler(request: Request) {
  const response = new Response('...');

  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-XSS-Protection', '1; mode=block');
  response.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  response.headers.set('Content-Security-Policy', "default-src 'self'");

  return response;
}
```

### 6. JWT 认证

```typescript
import jwt from 'jsonwebtoken';

export default async function handler(request: Request) {
  const token = request.headers.get('Authorization')?.replace('Bearer ', '');

  if (!token) {
    return new Response('Unauthorized', { status: 401 });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET as string);

    if (!decoded.permissions?.includes('read_data')) {
      return new Response('Forbidden', { status: 403 });
    }

    return new Response('...');
  } catch (error) {
    return new Response('Invalid token', { status: 401 });
  }
}
```

---

## 代码组织

### 推荐目录结构

```
project-root/
├── src/                          # 前端源代码
│   ├── app/                      # Next.js App Router
│   │   ├── (marketing)/          # 营销页面组
│   │   ├── (auth)/               # 认证页面组
│   │   └── api/                  # 前端 API 路由
│   ├── components/               # 可复用组件
│   │   ├── ui/                   # 基础 UI 组件
│   │   └── features/             # 功能组件
│   ├── lib/                      # 工具库
│   └── types/                    # TypeScript 类型
├── edge-functions/               # Edge Functions
│   ├── middleware/               # 中间件
│   └── api/                      # API 端点
├── node-functions/               # Node Functions
│   ├── api/                      # API 端点
│   └── jobs/                     # 后台任务
├── public/                       # 静态资源
├── package.json
├── next.config.ts
└── .env.local
```

### 模块化原则

**1. 单一职责**
```typescript
// ✅ 每个函数只做一件事
// edge-functions/middleware/auth.ts - 只处理认证
// edge-functions/middleware/logging.ts - 只处理日志
```

**2. 共享逻辑提取**
```typescript
// lib/db.ts
import { Pool } from 'pg';
export const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// lib/auth.ts
export async function verifyToken(token: string) { /* ... */ }

// edge-functions/api/users.ts
import { pool } from '../../lib/db';
import { verifyToken } from '../../lib/auth';
```

---

## 错误处理和日志

### 统一错误处理

```typescript
class APIError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export default async function handler(request: Request) {
  try {
    const result = await processData();
    return new Response(JSON.stringify(result), {
      headers: { 'content-type': 'application/json' }
    });
  } catch (error) {
    if (error instanceof APIError) {
      return new Response(JSON.stringify({
        error: error.message,
        code: error.code
      }), {
        status: error.statusCode,
        headers: { 'content-type': 'application/json' }
      });
    }

    console.error('Unexpected error:', error);
    return new Response(JSON.stringify({
      error: 'Internal server error'
    }), {
      status: 500,
      headers: { 'content-type': 'application/json' }
    });
  }
}
```

### 结构化日志

```typescript
export function log(
  level: 'info' | 'warn' | 'error',
  message: string,
  data?: Record<string, any>
) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    ...data
  };
  console.log(JSON.stringify(entry));
}

// 使用
log('info', 'Request processed', { userId: '123', duration: 45 });
log('error', 'Database connection failed', { error: err.message });
```

---

## 测试和部署

### 本地开发

```bash
# 终端 1：前端开发服务器
npm run dev

# 终端 2：函数开发服务器
edgeone pages dev
```

### 部署检查清单

- [ ] 环境变量已配置
- [ ] 数据库连接已测试
- [ ] 所有依赖已添加到 package.json
- [ ] 函数路径正确
- [ ] CORS 配置正确
- [ ] 错误处理已实现
- [ ] 日志记录已添加
- [ ] 安全头已设置
- [ ] 本地测试通过

---

## 常见场景

### 场景 1：用户认证流程

```typescript
// edge-functions/api/auth/login.ts
export default async function handler(request: Request) {
  const { email, password } = await request.json();

  // 调用 Node Function 查询用户
  const userResponse = await fetch('/node-functions/api/users/login', {
    method: 'POST',
    body: JSON.stringify({ email })
  });

  const user = await userResponse.json();

  if (!user || !verifyPassword(password, user.password)) {
    return new Response('Invalid credentials', { status: 401 });
  }

  const token = generateJWT(user);
  return new Response(JSON.stringify({ token }), {
    headers: { 'content-type': 'application/json' }
  });
}
```

### 场景 2：A/B 测试

```typescript
// edge-functions/middleware/ab-testing.ts
export default async function handler(request: Request) {
  const variant = request.headers.get('Cookie')
    ?.match(/variant=([AB])/)?.[1]
    || (Math.random() > 0.5 ? 'A' : 'B');

  const modifiedRequest = new Request(request, {
    headers: {
      ...request.headers,
      'X-AB-Variant': variant
    }
  });

  return fetch(modifiedRequest);
}
```

### 场景 3：图片处理

```typescript
// node-functions/api/upload.ts
import sharp from 'sharp';
import formidable from 'formidable';

export default async function handler(request: Request) {
  const form = formidable({ uploadDir: '/tmp' });
  const [fields, files] = await form.parse(request);
  const image = files.image?.[0];

  if (!image) {
    return new Response('No image uploaded', { status: 400 });
  }

  const processed = await sharp(image.filepath)
    .resize(800, 600)
    .jpeg({ quality: 80 })
    .toBuffer();

  const url = await uploadToStorage(processed);

  return new Response(JSON.stringify({ url }), {
    headers: { 'content-type': 'application/json' }
  });
}
```

### 场景 4：地理位置路由

```typescript
// edge-functions/middleware/geo-routing.ts
export default async function handler(request: Request) {
  const country = request.headers.get('CF-IPCountry') || 'US';

  const regionalUrl = request.url.replace(
    '/content/',
    `/content/${country.toLowerCase()}/`
  );

  return fetch(regionalUrl);
}
```

### 场景 5：多层缓存

```typescript
// edge-functions/api/cached-data.ts
export default async function handler(request: Request) {
  const cacheKey = `data:${request.url}`;

  // 检查内存缓存
  if (cache.has(cacheKey)) {
    return new Response(cache.get(cacheKey), {
      headers: { 'X-Cache': 'HIT', 'Cache-Control': 'public, max-age=3600' }
    });
  }

  // 获取数据
  const data = await fetchData();
  const json = JSON.stringify(data);

  // 设置缓存
  cache.set(cacheKey, json);

  return new Response(json, {
    headers: { 'X-Cache': 'MISS', 'Cache-Control': 'public, max-age=3600' }
  });
}
```
