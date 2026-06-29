> 本文档遵循 GitHub 标准 Contributing Guide 结构。
> Agent 启动前必须完整读取，所有编码产出必须遵守本文件约束。

---

## 一、Code of Conduct

<!-- 项目行为准则，可引用 Contributor Covenant -->

---

## 二、Types of Contributions

- 代码贡献（feat / fix / refactor）
- 文档贡献（docs）
- 测试贡献（test）
- 问题反馈（Bug Report / Feature Request）

---

## 三、Before You Start

### Report Bugs

<!-- 使用 GitHub Issues，模板 -->

### Feature Requests

<!-- 先检查 docs/vision.md 和 docs/design/ 确认是否在规划内 -->

---

## 四、Setup Dev Environment

<!-- 克隆、安装依赖、启动开发服务器 -->

```bash
git clone <repo-url>
cd <project>
npm install
npm run dev
```

---

## 五、Pull Request Workflow

### 1. Fork & Branch

- `main`：生产分支，受保护
- `develop`：开发分支
- `feature/xxx`：功能分支
- `fix/xxx`：修复分支

### 2. Code Style & Lint

- 语言：TypeScript（严格模式）
- 格式化：Prettier（2 空格缩进，单引号，无分号）
- 命名：
  - 文件：kebab-case（`user-service.ts`）
  - 变量/函数：camelCase
  - 类/接口：PascalCase
  - 常量：UPPER_SNAKE_CASE

### 3. Commit Rules

```
<type>(<scope>): <简短描述>
```

| type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档变更（必须独立提交，不与代码混合） |
| refactor | 重构 |
| test | 测试相关 |
| chore | 构建/工具/依赖 |

### 4. Test

测试体系按项目类型可伸缩，详见 [agent-coding-spec.md](agent-coding-spec.md) 第八节。提交前必须通过对应项目类型所要求的测试层。

**检查清单：**
- [ ] 类型检查通过（`tsc --noEmit`）
- [ ] Lint 通过（`eslint`）
- [ ] 单元测试通过
- [ ] 无 console.log 残留

### 5. Open PR

<!-- PR 描述模板、Review 流程 -->

---

## 六、Docs Contribution

### 文档体系

项目文档遵循 [agent-coding-spec.md](agent-coding-spec.md) 定义的结构。新增或修改文档前，先阅读该规范。

### Frontmatter 规范

以下文档类型使用 YAML frontmatter（`---` 包裹），位于文件最顶部：

| 文档类型 | 必填字段 |
|----------|----------|
| Design Spec | `title`, `description`, `type`, `status`, `version`, `created` |
| ADR | `title`, `description`, `type`, `status`, `created` |
| Plan | `title`, `description`, `type`, `status`, `created` |
| Report | `title`, `description`, `type`, `status`, `created` |

`status` 字段的有效值由文档类型决定，详见 [agent-coding-spec.md](agent-coding-spec.md) 第四节「文档状态定义」。

以下文件**不使用** frontmatter：
- AGENTS.md、CONTRIBUTING.md、CHANGELOG.md（标准文件）
- 所有 README.md（目录索引）
- vision.md（全局愿景）

```yaml
---
title: 文档标题
description: 一句话摘要，Agent 无需读正文即可了解文档用途
type: design | adr | plan | report
status: 见 agent-coding-spec.md 第四节
created: YYYY-MM-DDTHH:MM:SSZ
---
```

### 路径引用

- 所有跨文档引用使用相对路径 Markdown 链接：`[text](relative/path.md)`
- 禁止使用反引号包裹的纯文本路径

### 文档 Commit

- 文档修改必须独立 Commit，不与代码混合
- 格式：`docs(<scope>): <简述>`

---

## 七、License & CLA

<!-- 项目许可证和贡献者协议 -->

---

## 八、Get Help

<!-- 联系方式、讨论渠道 -->