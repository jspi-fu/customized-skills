---
name: mkdocs-shadcn
description: mkdocs-shadcn 主题 Markdown 排版与项目编排。用于创建和编辑使用 mkdocs-shadcn 主题的文档，包括 YAML 配置、扩展语法（admonition、details、tab、数学公式等）、文本对齐、项目结构规划等。当用户需要编写或修改 mkdocs-shadcn 主题的 Markdown 文件、配置 mkdocs.yml、询问排版语法、或需要决策何时使用 details/tab/admonition 等语法时触发此技能。
---

# mkdocs-shadcn 主题排版技能

## 快速开始

### 1. 基础配置检查

编辑 Markdown 文件前，确认项目已配置：

```yaml
# mkdocs.yml
markdown_extensions:
  - admonition
  - codehilite
  - pymdownx.blocks.details
  - pymdownx.blocks.tab
  - pymdownx.tabbed
  - pymdownx.arithmatex:
      generic: true
  - attr_list
```

### 2. 页面元数据模板

每个 Markdown 文件开头使用：

```markdown
---
title: 页面标题
summary: 页面摘要，概括核心内容（不应是 title 的简单扩写）
new: false
show_datetime: false
---
```

**字段说明：**
- `title`: 页面标题
- `summary`: 页面摘要，用于搜索和预览。**注意：不应是 title 的简单扩写，而应概括页面核心内容**
- `new`: 是否标记为新内容，默认 `false`
- `show_datetime`: 是否显示日期时间，默认 `false`

## 核心语法速查

### 文本对齐

```markdown
<!-- 居中 -->
<p align="center">居中文字</p>
<p align="center"><strong>居中加粗</strong></p>

<!-- 居右 -->
<div align="right">
作者<br>
日期
</div>
```

### 标题分割线

**规范：**
1. **二级标题 (##)**: 下一行必须添加 `---` 分隔符。
2. **三级标题 (###)**: 上一行必须添加 `---` 分隔符并换行。
    - **特例**：二级标题后的第一个三级标题前 **不加** 分隔符。
3. **清理**: 除上述场景外，删除文档中其他所有的 `---`（YAML frontmatter 中的除外）。

```markdown
## 章节标题
---

### 第一个小节标题  <-- 二级标题后的第一个，前不加 ---

内容...

---

### 第二个小节标题  <-- 非第一个，前加 ---
```

### 图片与 GIF

**规范：** 所有图片和 GIF 必须居中放置，且不加标题。

```markdown
<p align="center">![](image_url)</p>
```

### 提示框

```markdown
!!! note "标题"
    提示内容（缩进4空格）

!!! tip/warning/danger/info
```

### 可折叠块

```markdown
/// details | 标题
折叠内容
///
```

### 标签页

```markdown
/// tab | 标签A
内容A
///

/// tab | 标签B
内容B
///
```

### 数学公式

```markdown
行内: $E = mc^2$

块级:
$$
\frac{a}{b} = c
$$
```

## 详细参考

- **完整语法手册**: 参见 [references/syntax-guide.md](references/syntax-guide.md)
- **项目配置参考**: 参见 [references/configuration.md](references/configuration.md)
- **排版示例**: 参见 [references/examples.md](references/examples.md)

## 模板文件

- **页面模板**: [assets/page-template.md](assets/page-template.md)
- **mkdocs.yml 模板**: [assets/mkdocs-template.yml](assets/mkdocs-template.yml)

## 工作流程

### 编辑/创建页面的两阶段流程

编辑或创建 Markdown 文件时，必须按照以下**两阶段**执行：

#### 第一阶段：智能排版决策（AI 完成）

此阶段由 AI 分析内容并做出排版决策：

1. **分析内容结构**：阅读并理解用户提供的原始内容
2. **应用智能排版决策**：
   - 根据内容特征决定是否使用 `/// details` 可折叠块
   - 根据互斥选项决定是否使用 `/// tab` 标签页
   - 根据信息重要性决定是否使用 `!!! tip/note/warning` 提示框
   - 参考下方的「智能排版决策指南」做出判断
3. **编写内容**：使用选定的语法编写 Markdown 内容

**注意**：此阶段**不处理**标题分割线、图片居中、列表间距等格式问题——这些留给第二阶段脚本处理

#### 第二阶段：自动格式规范化（脚本执行）

内容编写完成后，**必须**执行格式化脚本：

```powershell
python .trae/skills/mkdocs-shadcn/scripts/format.py <文件路径>
```

脚本会处理以下**确定性格式**（AI 不应手动处理）：
- **标题分割线**：按规范添加 H2/H3 标题的分隔符
- **图片居中**：所有图片转换为居中 HTML 格式
- **资源路径**：包含 `assets/` 的路径自动转换为以 `/assets` 开头的绝对路径
- **列表间距**：修复列表项之间的空行，确保符合规范

**⚠️ 重要规则**：
- 脚本执行是**强制性的**，在第一阶段完成后必须执行
- AI **不允许**手动修改标题分割线、图片居中格式或列表间距
- 如果格式化多个文件，可以一次性执行：`python .trae/skills/mkdocs-shadcn/scripts/format.py <目录路径>`

### 完整示例流程

```
用户要求：帮我整理这篇 Python 教程文档

步骤 1（AI 智能决策）：
- 分析内容：教程包含安装步骤、基础用法、进阶技巧
- 做出决策：
  - 安装步骤用 /// tab 区分 Windows/macOS/Linux
  - 进阶技巧用 /// details 折叠（可选阅读）
  - 重要提示用 !!! tip 突出
- 编写内容（此时不处理标题分割线、图片格式等）

步骤 2（脚本执行）：
- 执行：python .trae/skills/mkdocs-shadcn/scripts/format.py tutorial.md
- 脚本自动添加 --- 分割线、居中图片、修复列表间距
```

### 配置项目

1. 参考 [assets/mkdocs-template.yml](assets/mkdocs-template.yml)
2. 根据 [references/configuration.md](references/configuration.md) 调整配置

### 智能排版决策指南

#### 何时使用 Details（可折叠块）

| 场景特征 | 示例 | 决策 |
|----------|------|------|
| 内容较长，但不是所有人都需要看 | 详细解释、背景知识、实现原理 | ✅ 使用 `/// details` |
| 问答形式的 FAQ | "什么是 XXX？"、"为什么要...？" | ✅ 使用 `/// details \| ❓ 问题标题` |
| 常见误区/反模式 | "误区一：..."、"误区二：..." | ✅ 使用 `/// details` 逐个折叠 |
| 可选阅读内容 | 进阶用法、额外配置、参考资料 | ✅ 使用 `/// details` |
| 代码示例过多 | 多种实现方式的代码展示 | ✅ 使用 `/// details` 折叠 |
| 内容简短且重要 | 核心概念、关键步骤 | ❌ 直接展示，不要折叠 |
| 需要连续阅读 | 教程步骤、流程说明 | ❌ 直接展示，不要折叠 |

**Details 标题命名建议：**
- FAQ 问题：`/// details | ❓ 为什么要使用 UV？`
- 详细说明：`/// details | 📖 点击查看详细配置`
- 代码示例：`/// details | 💻 完整代码示例`

#### 何时使用 Tab（标签页）

| 场景特征 | 示例 | 决策 |
|----------|------|------|
| 互斥的选项/方式 | 不同操作系统、不同工具、不同方法 | ✅ 使用 `/// tab` |
| 并行对比内容 | 工具对比、方案对比、版本对比 | ✅ 使用 `/// tab` |
| 分类整理的速查表 | 环境管理/包管理/项目管理 | ✅ 使用 `/// tab` |
| 内容有依赖关系 | 步骤1 → 步骤2 → 步骤3 | ❌ 使用顺序列表，不要 Tab |
| 内容需要同时参考 | 多个相关概念的解释 | ❌ 直接展示，不要 Tab |

**Tab 标签命名建议：**
- 按平台：`/// tab | Windows`、`/// tab | macOS`、`/// tab | Linux`
- 按方式：`/// tab | 方式一：原生管理`、`/// tab | 方式二：兼容模式`
- 按工具：`/// tab | UV vs pip`、`/// tab | UV vs Conda`
- 加 emoji：`/// tab | 🖥️ 环境管理`、`/// tab | 📦 包管理`

#### 何时使用 Admonition（提示框）

| 类型 | 使用场景 | 示例 |
|------|----------|------|
| `!!! tip` | 技巧、建议、最佳实践、优化方案 | "使用 `uv run` 无需手动激活虚拟环境" |
| `!!! note` | 补充说明、额外信息、注意事项 | "UV 支持 Python 3.8+ 版本" |
| `!!! warning` | 警告、需要注意的问题、潜在风险 | "不要把 API 密钥提交到 Git" |
| `!!! danger` | 危险操作、会导致严重后果的行为 | "删除操作不可恢复" |
| `!!! info` | 一般性信息、参考链接、相关资源 | "更多信息请参考官方文档" |

#### 排版决策流程图

```
内容是否需要折叠？
├── 是 → 使用 /// details
│   └── 是 FAQ 形式？→ 标题用 ❓ 开头
│
内容是否有多个互斥选项？
├── 是 → 使用 /// tab
│   └── 按什么分类？→ 平台/方式/工具/类别
│
内容是否需要突出强调？
├── 是 → 使用 !!! tip/note/warning/danger
│   └── 重要程度？
│       ├── 技巧建议 → tip
│       ├── 补充说明 → note
│       ├── 需要注意 → warning
│       └── 严重后果 → danger
│
└── 默认 → 直接展示
```

### 快速参考表

| 场景 | 推荐语法 |
|------|----------|
| 重要语句/赠语 | `<p align="center"><strong>文字</strong></p>` |
| 章节分隔 | `## 标题` + `---` |
| FAQ 问答 | `/// details \| ❓ 问题标题` |
| 可选阅读内容 | `/// details \| 📖 标题` |
| 多平台/多方式说明 | `/// tab \| 标签名` |
| 工具/方案对比 | `/// tab \| 对比项A` + `/// tab \| 对比项B` |
| 技巧建议 | `!!! tip "标题"` |
| 补充说明 | `!!! note "标题"` |
| 警告提示 | `!!! warning/danger "标题"` |
