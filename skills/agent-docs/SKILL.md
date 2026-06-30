---
name: agent-docs
description: 项目文档体系与生命周期管理。当 Agent 需要理解当前阶段能做什么、如何推进状态、如何创建和管理文档时使用。
---

# Agent Docs System

## 系统全貌

项目开发遵循 6 阶段状态机。Agent 的行为由当前阶段决定，不绑定固定角色。

```
INIT → DESIGN → DEVELOP → INTEGRATE → PRE_RELEASE → RELEASE
         ↑         │  ↑                    │
         │         │  └────────────────────┘
         │         │      (修复循环)
         └─────────┘
      (架构变更回退)

RELEASE → DESIGN  (新一轮迭代)
```

| 阶段 | 做什么 |
|------|--------|
| INIT | 搭建项目骨架（目录、标准文件、Git） |
| DESIGN | 冻结四类契约（业务/接口/质量/架构），拆解 Plan |
| DEVELOP | 多轨道并行：编码/测试基建/部署（轨道数取决于项目类型） |
| INTEGRATE | 全量测试。唯一串行关口——必须等所有轨道完成 |
| PRE_RELEASE | 预发布环境验证、版本号确认 |
| RELEASE | 版本归档、CHANGELOG 整理、迭代复盘 |

**DEVELOP 内部并行轨道：** 契约冻结后全部并行，每条轨道在独立 Git branch 中执行。测试基础设施必须最先完成。轨道数量取决于项目类型（例如全栈项目 4 条，CLI 工具 2 条）。

**Agent 无状态。** 任何 Agent 可以随时被终止，下次启动时仅凭文件系统恢复状态。所有关键信息在文档中，不在对话历史中。

---

## 安装系统

如果是全新项目，初始化项目骨架：

```
1. 复制 assets/templates/ 下的 AGENTS.md, CONTRIBUTING.md, CHANGELOG.md 到项目根目录
2. 复制 assets/templates/docs/ 下全部内容到项目 docs/ 目录
3. 在 docs/README.md 中设置当前阶段为 INIT
4. 提交（commit message 描述变更内容，格式见 CONTRIBUTING.md）
5. 推进: 更新 docs/README.md 当前阶段为 DESIGN，提交。约定 commit 前缀: `docs(state):`
```

系统已安装后，直接进入下一步。

---

## 导航系统

系统文档是自描述的。按以下顺序读取：

```
1. AGENTS.md           → 项目入口地图：文档类型、目录结构、系统边界、阶段行为
2. docs/README.md      → 当前系统状态 + 行为边界（首先读取！）
3. CONTRIBUTING.md     → 编码/Commit/文档/测试规范
4. 各级 README.md      → 子目录索引和状态
5. 具体文档             → Vision / Design Spec / ADR / Plan / Report
```

**系统规则和约定（文档类型、命名规范、frontmatter、Git 规则）在 AGENTS.md 和 CONTRIBUTING.md 中。** 本 skill 不重复这些内容。

---

## 按阶段选择路径

确认当前阶段后，按阶段选择操作流程：

| 当前阶段 | 去读 |
|----------|------|
| INIT / DESIGN | [references/phase-design.md](references/phase-design.md) |
| DEVELOP | [references/phase-develop.md](references/phase-develop.md) |
| INTEGRATE | [references/phase-integrate.md](references/phase-integrate.md) |
| PRE_RELEASE / RELEASE | [references/phase-release.md](references/phase-release.md) |

### DEVELOP 阶段的测试 Plan 创建

| 当需要创建 Plan 描述以下任务时 | 去读 |
|----------|------|
| 测试基础设施 | [references/testing/ref-testing-infra.md](references/testing/ref-testing-infra.md) |
| 编码自测 | [references/testing/ref-testing-dev.md](references/testing/ref-testing-dev.md) |
| 全量集成测试 | [references/testing/ref-testing-integrate.md](references/testing/ref-testing-integrate.md) |