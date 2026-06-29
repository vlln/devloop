---
name: agent-docs
description: 项目文档体系与生命周期管理。当 Agent 需要理解自己在项目中的角色、当前阶段能做什么、如何创建和管理文档时使用。
---

# Agent Docs System

## 系统全貌

项目开发遵循 6 阶段状态机：

```
INIT → DESIGN → DEVELOP → INTEGRATE → PRE_RELEASE → RELEASE
         ↑         │  ↑                    │
         │         │  └────────────────────┘
         │         │      (修复循环)
         └─────────┘
      (架构变更回退)

RELEASE → DESIGN  (新一轮迭代)
```

| 阶段 | 谁 | 做什么 |
|------|-----|--------|
| INIT | Designer | 搭建项目骨架（目录、标准文件、Git） |
| DESIGN | Designer | 冻结四类契约（业务/接口/质量/架构），拆解 Plan |
| DEVELOP | Executor | 4 条轨道并行：后端/前端/测试基建/数据库部署 |
| INTEGRATE | Executor | 全量测试。唯一串行关口——必须等所有轨道完成 |
| PRE_RELEASE | Designer | 预发布环境验证、版本号确认 |
| RELEASE | Designer | 版本归档、CHANGELOG 整理、迭代复盘 |

**DEVELOP 内部 4 条并行轨道：** 契约冻结后全部并行，每条轨道在独立 Git branch 中执行。轨道 C（测试基础设施）必须最先完成。

**2 个角色：** Designer（设计决策、状态推进）与 Executor（执行实现）。你不固定属于哪一方。

---

## 安装系统

如果是全新项目，初始化项目骨架：

```
1. 复制 assets/templates/ 下的 AGENTS.md, CONTRIBUTING.md, CHANGELOG.md 到项目根目录
2. 复制 assets/templates/docs/ 下全部内容到项目 docs/ 目录
3. 在 docs/README.md 中设置当前阶段为 INIT
4. 独立 commit: docs(init): 初始化项目文档骨架
5. 推进: 更新 docs/README.md 当前阶段为 DESIGN
   commit: docs(state): INIT → DESIGN
```

系统已安装后，直接进入下一步。

---

## 导航系统

系统文档是自描述的。按以下顺序读取：

```
1. AGENTS.md           → 项目入口地图：文档类型、目录结构、系统边界、角色权限
2. docs/README.md      → 当前系统状态 + 行为边界（首先读取！）
3. CONTRIBUTING.md     → 编码/Commit/文档/测试规范
4. 各级 README.md      → 子目录索引和状态
5. 具体文档             → Vision / Design Spec / ADR / Plan / Report
```

**系统规则和约定（文档类型、命名规范、frontmatter、Git 规则）在 AGENTS.md 和 CONTRIBUTING.md 中。** 本 skill 不重复这些内容。

---

## 按角色选择路径

确认当前阶段后，按角色选择操作流程：

| 你的角色 | 当前阶段 | 去读 |
|----------|---------|------|
| Designer | INIT / DESIGN / PRE_RELEASE / RELEASE | [references/designer-workflow.md](references/designer-workflow.md) |
| Executor | DEVELOP / INTEGRATE | [references/executor-workflow.md](references/executor-workflow.md) |

### Executor 的测试任务

| 你的任务 | 去读 |
|----------|------|
| 搭建测试基础设施（DEVELOP 轨道 C） | [references/testing/testing-infra.md](references/testing/testing-infra.md) |
| 编码 + 自测（DEVELOP 轨道 A/B） | [references/testing/testing-dev.md](references/testing/testing-dev.md) |
| 全量集成测试（INTEGRATE 阶段） | [references/testing/testing-integrate.md](references/testing/testing-integrate.md) |