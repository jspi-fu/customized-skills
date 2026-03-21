---
name: mkdocs-shadcn
description: mkdocs-shadcn 主题 Markdown 排版与项目编排。当用户需要编写或修改 mkdocs-shadcn 主题的文档、配置 mkdocs.yml、或询问排版语法时，必须使用此技能。
---

# mkdocs-shadcn 主题排版技能

## 工作流程（每次运行技能时必须运行该工作流程中的所有步骤）
---
### 1. 检查项目配置

运行配置检查脚本：

```bash
python <mkdocs-shadcn-path>/scripts/check_config.py <项目目录> [--apply]
```

脚本会自动检查并补充：

- `theme.name` 是否为 `shadcn`
- `plugins` 是否包含必要插件
- `markdown_extensions` 是否包含推荐的扩展
- `nav` 导航配置
- `site_name` 站点名称

如需自动应用修复，添加 `--apply` 参数。

---

### 2. 智能排版内容

根据内容特征选择合适语法，进行排版：

| 内容特征 | 选择语法 | 参考文档 |
|----------|----------|----------|
| 内容较长，非必需阅读 | `/// details` | [syntax-guide.md](references/syntax-guide.md) |
| 问答形式的 FAQ | `/// details \| ❓ 问题` | [syntax-guide.md](references/syntax-guide.md) |
| 多平台/互斥选项 | `/// tab` | [syntax-guide.md](references/syntax-guide.md) |
| 技巧、建议 | `!!! tip` | [syntax-guide.md](references/syntax-guide.md) |
| 警告、风险 | `!!! warning/danger` | [syntax-guide.md](references/syntax-guide.md) |
| 补充说明 | `!!! note/info` | [syntax-guide.md](references/syntax-guide.md) |

详细语法和示例参考 [syntax-guide.md](references/syntax-guide.md) 和 [examples.md](references/examples.md)。

---

### 3. 格式化文档

排版内容完成后，必须运行格式化脚本：

```bash
python <mkdocs-shadcn-path>/scripts/format.py <文件或目录路径>
```

脚本自动处理：

- 标题分割线（H2 下方 `---`，H3 上方 `---`，H2 后第一个 H3 除外）
- 图片居中（统一转为 `<p align="center">
  <img ...>
</p>`）

- 资源路径（`assets/` 路径转为 `/assets` 绝对路径）
- 列表间距（统一空行规范）

## 页面模板
---
新建页面时，使用终端命令复制 [assets/page-template.md](assets/page-template.md) 作为起点。

项目初始化时，参考 [assets/mkdocs-template.yml](assets/mkdocs-template.yml) 创建配置文件。

## 决策流程
---
```
内容是否需要折叠？
├── 是 → /// details
│   └── FAQ 形式？→ 标题用 ❓ 开头
│
内容是否有多个互斥选项？
├── 是 → /// tab
│   └── 按平台/方式/工具分类
│
内容是否需要突出强调？
├── 是 → !!! tip/note/warning/danger
│
└── 默认 → 直接展示
```
