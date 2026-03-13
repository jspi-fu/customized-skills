<p align="center">
  <img src="assets/claude-agent-skills.jpg" alt="Skills 架构图">
</p>

<p align="center">
  <img style="height: 50px;" src="https://readme-typing-svg.demolab.com?font=Noto+Sans+SC&weight=400&duration=3500&pause=2000&color=E78BE7&center=true&vCenter=true&random=false&width=200&lines=Customized+Skills+!" alt="Hello-vibe-typing-svg" />
</p>

<p align="center">
  <strong>作者精心开发与验证的 Agent Skills 集合，解决定制化需求</strong><br>
  <em>为 AI Agent 提供标准化、可复用的能力包</em>
</p>

---

## 什么是 Skills？

**Skills** 是可供重复使用的能力包。无论是"发送邮件"还是"文件上传"，这些成熟功能都可以封装成 Skill，让 Agent 和 MCP 像使用工具一样直接调用。

它通过固定的规则和标准化的能力，保证输出结果的稳定和一致。

### 使用场景示例

假设你要搭建一个网站，需要用户系统：

- 直接使用现成的「用户鉴权 Skill」接入登录验证
- 使用「手机验证码注册 Skill」搞定注册流程

这就是 Skills 带来的便利——**复用成熟方案，避免重复造轮子**。

---

## 项目包含的 Skills

- 🚀 [**edgeone-pages-best-practice**](Skills/edgeone-pages/SKILL.md)：指导 AI 生成符合 [EdgeOne Pages](https://edgeone.ai/zh) 平台规范的代码，避免部署报错。
- 📝 [**mkdocs-shadcn**](Skills/mkdocs-shadcn/SKILL.md)：mkdocs-shadcn 主题 Markdown 排版与项目编排，包括 YAML 配置、扩展语法（admonition、details、tab、数学公式等）、文本对齐规范等。


---

## 如何使用

1. **浏览 Skills**：查看 `Skills/` 目录下的技能定义
2. **阅读 SKILL.md**：每个 Skill 都有详细的触发条件和能力说明
3. **下载 Skills**：将需要的 Skill 完整技能包复制到你的项目中
4. **按需触发**：根据 Skill 描述中的触发场景，在对话中激活相应技能

---

## 贡献指南

欢迎贡献新的 Skills！请确保：

1. **经过充分调研**：本项目内的 Skills 应具有不可替代性和实用性，请先在 [skills.sh](https://skills.sh/) 平台或使用`find-skills`搜索是否已存在相似 Skill。
2. **包含完整文档**：提供清晰的触发条件和能力说明。
3. **附带参考资源**：如有需要，提供相关的参考文档。

---

<p align="center">
  <sub>如果本项目对你有帮助，欢迎 ⭐ Star 支持！</sub>
</p>
