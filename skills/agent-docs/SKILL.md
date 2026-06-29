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

**6 阶段概要：**

| 阶段 | 谁 | 做什么 |
|------|-----|--------|
| INIT | Designer | 搭建项目骨架（目录、标准文件、Git） |
| DESIGN | Designer | 冻结四类契约（业务/接口/质量/架构），拆解 Plan |
| DEVELOP | Executor | 4 条轨道并行：后端/前端/测试基建/数据库部署 |
| INTEGRATE | Executor | 全量测试。唯一串行关口——必须等所有轨道完成 |
| PRE_RELEASE | Designer | 预发布环境验证、版本号确认 |
| RELEASE | Designer | 版本归档、CHANGELOG 整理、迭代复盘 |

**DEVELOP 内部 4 条并行轨道：**

```
契约冻结后全部并行:
  ├─ 轨道 A: 后端开发     (独立 branch)
  ├─ 轨道 B: 前端开发     (独立 branch)
  ├─ 轨道 C: 测试基础设施  (独立 branch, 必须最先完成)
  └─ 轨道 D: 数据库/部署  (独立 branch)
```

**2 个角色：** Designer（设计决策、状态推进）与 Executor（执行实现）。你不固定属于哪一方。

## 第一步：确认当前状态

打开 `docs/README.md`，读「当前系统状态」段。那里告诉你当前阶段和允许/禁止的行为边界。

**禁止的事，即使你能做到，也不要做。**

## 第二步：按角色选择路径

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

## 硬性规则（永远记住）

1. 文档变更和代码变更永远分开 commit
2. 冻结的东西（status=active）不能原地改，必须走正式回退
3. 模板在 `assets/templates/`。复制后按项目实际情况填写
4. 关联用语义链（正文中引用 AC 编号和文件路径），不需要 frontmatter 的 related 字段