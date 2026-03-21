# mkdocs-shadcn 项目配置参考

## 完整 mkdocs.yml 配置
---
```yaml
site_name: "项目名称"
site_url: https://your-site.github.io/
repo_url: https://github.com/username/repo.git
repo_name: username/repo

theme:
  name: shadcn
  show_title: true          # 显示站点标题
  show_stargazers: true     # 显示 GitHub Star 数
  pygments_style:
    light: shadcn-light     # 亮色代码主题
    dark: github-dark       # 暗色代码主题
  icon: assets/logo.svg     # 站点图标
  topbar_sections: false    # 顶部导航栏显示章节
  show_datetime: false      # 是否显示文档日期

plugins:

  - search                  # 搜索插件
  - mkdocstrings:           # API 文档生成
      handlers:
        python:
          options:
            show_root_heading: true

extra_javascript:

  - assets/custom-favicon.js

markdown_extensions:

  - admonition              # 提示框
  - codehilite              # 代码高亮
  - fenced_code             # 围栏代码块
  - footnotes               # 脚注
  - pymdownx.blocks.details # 可折叠详情块
  - pymdownx.blocks.tab     # 标签页
  - pymdownx.progressbar    # 进度条
  - pymdownx.tabbed         # 选项卡
  - pymdownx.arithmatex:    # 数学公式
      generic: true

  - attr_list               # 属性列表

nav:

  - 首页: index.md
  - 章节一: 01_章节.md
  - 章节二:
    - 子章节1: 02_章节/01_子章节.md
    - 子章节2: 02_章节/02_子章节.md
```

## 主题配置详解
---
### show_title

控制是否显示站点标题。

```yaml
theme:
  show_title: true   # 显示
  show_title: false  # 隐藏
```

---

### show_stargazers

控制是否显示 GitHub Star 数（需要配置 repo_url）。

```yaml
theme:
  show_stargazers: true   # 显示
  show_stargazers: false  # 隐藏
```

---

### pygments_style

配置代码高亮主题。

```yaml
theme:
  pygments_style:
    light: shadcn-light   # 亮色主题
    dark: github-dark     # 暗色主题
```

可用主题：

- `shadcn-light` / `shadcn-dark`
- `github-light` / `github-dark`
- `monokai`
- `dracula`

---

### topbar_sections

控制是否在顶部导航栏显示章节。

```yaml
theme:
  topbar_sections: true   # 顶部显示章节导航
  topbar_sections: false  # 仅在侧边栏显示
```

**建议**：对于深层嵌套的文档（d>2），建议开启此选项。

---

### show_datetime

控制是否显示文档日期。

```yaml
theme:
  show_datetime: true   # 显示
  show_datetime: false  # 隐藏
```

也可以在单页面覆盖：

```markdown
show_datetime: false
```

## 页面元数据
---
每个 Markdown 文件顶部可配置 YAML Front Matter：

```markdown
title: 页面标题              # 显示在浏览器标签和页面顶部
summary: 页面摘要            # 用于搜索和预览
description: 详细描述        # SEO 描述
keywords: 关键词1, 关键词2   # SEO 关键词
order: 2                   # 侧边栏排序（数字越小越靠前）
sidebar_title: 导航标题      # 侧边栏显示名称
show_datetime: false       # 是否显示日期
```

### order 排序规则

`order` 控制页面在侧边栏中的排序：

1. 未设置 `order` 的页面按字母顺序排列
2. 设置 `order` 的页面按数字排序
3. 数字越小越靠前

示例：

```
| a.md ; order 未设置
| b.md ; order: 42
| c.md ; order: 0
| d.md ; order 未设置
```

排序结果：`c.md` (0) → `a.md` (默认0) → `d.md` (默认1) → `b.md` (42)

## 导航配置
---
### 基础导航

```yaml
nav:

  - 首页: index.md
  - 简介: introduction.md
  - 指南: guide.md
```

---

### 嵌套导航

```yaml
nav:

  - 首页: index.md
  - 基础入门:
    - 概念: basics/concepts.md
    - 安装: basics/installation.md
  - 高级主题:
    - 配置: advanced/config.md
    - 部署: advanced/deploy.md
```

---

### 使用数字前缀控制排序

文件系统使用数字前缀：

```
docs/
├── 00_介绍.md
├── 01_基础/
│   ├── 00_概念.md
│   └── 01_安装.md
└── 02_进阶.md
```

mkdocs.yml 中无需数字前缀：

```yaml
nav:

  - 介绍: 00_介绍.md
  - 基础:
    - 概念: 01_基础/00_概念.md
    - 安装: 01_基础/01_安装.md
  - 进阶: 02_进阶.md
```

## 插件配置
---
### search 搜索插件

```yaml
plugins:

  - search
```

---

### mkdocstrings API 文档

```yaml
plugins:

  - mkdocstrings:
      handlers:
        python:
          options:
            show_root_heading: true
```

安装依赖：

```bash
pip install 'mkdocstrings[python]'
```

## Markdown 扩展配置
---
### 基础扩展

```yaml
markdown_extensions:

  - admonition        # 提示框 !!!
  - codehilite        # 代码高亮
  - fenced_code       # 围栏代码块 ```
  - footnotes         # 脚注 [^1]
  - attr_list         # 属性列表 {: }
```

---

### pymdownx 扩展

```yaml
markdown_extensions:

  - pymdownx.blocks.details    # 可折叠块 /// details
  - pymdownx.blocks.tab        # 标签页 /// tab
  - pymdownx.progressbar       # 进度条 [==50%]
  - pymdownx.tabbed            # 选项卡 ===
  - pymdownx.arithmatex:       # 数学公式 $
      generic: true
```

安装依赖：

```bash
pip install pymdown-extensions
```

## 静态资源
---
### 自定义 JavaScript

```yaml
extra_javascript:

  - assets/custom-favicon.js
  - assets/analytics.js
```

---

### 自定义 CSS

```yaml
extra_css:

  - css/custom-style.css
```

---

### 图标配置

```yaml
theme:
  icon: assets/logo.svg
```

## 目录结构建议
---
```
project/
├── mkdocs.yml          # 配置文件
├── docs/               # 文档目录
│   ├── index.md        # 首页
│   ├── 01_章节.md      # 第一章
│   ├── 02_章节/        # 第二章目录
│   │   ├── 00_小节.md
│   │   └── 01_小节.md
│   └── assets/         # 文档资源
│       ├── logo.svg
│       └── images/
└── excalidraw/         # Excalidraw 插件目录（如使用）
```

## 部署配置
---
### GitHub Pages

```yaml
# mkdocs.yml
site_url: https://username.github.io/repo-name/
```

```bash
# 部署命令
mkdocs gh-deploy
```

---

### 本地预览

```bash
mkdocs serve
```

---

### 构建站点

```bash
mkdocs build
```

## 完整依赖安装
---
```bash
pip install mkdocs-shadcn pymdown-extensions mkdocstrings
```

或使用：

```bash
pip install mkdocs-shadcn
pip install pymdown-extensions
pip install 'mkdocstrings[python]'
```
