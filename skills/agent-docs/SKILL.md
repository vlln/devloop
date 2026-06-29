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

## 文档体系

### 文档类型

| 文档 | 用途 | 谁维护 | 有 frontmatter？ |
|------|------|--------|-----------------|
| `AGENTS.md` | 项目入口地图，Agent 启动时首先读取 | Designer | 否 |
| `CONTRIBUTING.md` | 编码/Commit/文档/测试规范 | Designer | 否 |
| `CHANGELOG.md` | 版本变更记录（Keep a Changelog 格式） | Executor 追加 Unreleased，Designer 整理发布 | 否 |
| `docs/vision.md` | 全局顶层愿景：业务目标、用户范围、顶层约束 | Designer | 否 |
| `docs/design/00x-xxxx.md` | Design Spec：固化方案 + AC。唯一业务事实源 | Designer | 是 |
| `docs/adr/000x-xxxx.md` | 架构决策记录：技术选型、方案对比、取舍 | Designer | 是 |
| `docs/plans/000x-任务名/` | 单次执行容器：Plan + Report 成对 | Executor | Plan/Report 是 |
| `docs/README.md` | 子目录索引 + 当前系统状态 | Designer（状态更新） | 否 |
| 各级 `README.md` | 该目录的索引和状态说明 | Designer | 否 |

### 目录结构

```
项目根目录
├── AGENTS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── docs/
│   ├── README.md          # 索引 + 当前系统状态
│   ├── vision.md
│   ├── design/
│   │   ├── README.md
│   │   └── 001-spec.md
│   ├── adr/
│   │   ├── README.md
│   │   └── 0001-xxx.md
│   └── plans/
│       ├── README.md
│       └── 0001-任务名/
│           ├── README.md
│           ├── 01-plan-xxx.md
│           ├── 01-report-xxx.md
│           └── artifacts/
├── src/
└── .github/workflows/
```

### 命名规范

| 文档 | 格式 | 示例 |
|------|------|------|
| Vision | `vision.md` | `vision.md` |
| Design Spec | `00x-xxxx.md` | `001-spec.md` |
| ADR | `000x-xxxx.md` | `0001-db-choice.md` |
| Plan 文件夹 | `000x-简短描述` | `0001-订单模块` |
| Plan 子任务 | `0x-plan-xxx.md` | `01-plan-order-api.md` |
| Report | `0x-report-xxx.md` | `01-report-order-api.md` |

---

## Frontmatter 规范

以下文档类型使用 YAML frontmatter（`---` 包裹），位于文件最顶部：

| 文档类型 | 必填字段 |
|----------|----------|
| Design Spec | `title`, `description`, `type: design`, `status`, `version`, `created` |
| ADR | `title`, `description`, `type: adr`, `status`, `created` |
| Plan | `title`, `description`, `type: plan`, `status`, `created` |
| Report | `title`, `description`, `type: report`, `status`, `created` |

**字段说明：** `title` 文档标题 / `description` 一句话摘要 / `type` 固定值 / `status` 见下方 / `created` ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`) / `version` 仅 Design Spec，整数递增。

**以下文件不使用 frontmatter：** AGENTS.md、CONTRIBUTING.md、CHANGELOG.md、所有 README.md、vision.md。

**status 有效值：**

| 文档类型 | 状态值 | 流转 |
|----------|--------|------|
| Vision | `draft` / `active` / `archived` | draft→active→archived |
| Design Spec | `draft` / `active` / `archived` | draft→active→archived（同时只有一个 active） |
| ADR | `draft` / `accepted` / `superseded` / `deprecated` | draft→accepted→superseded/deprecated |
| Plan | `pending` / `in_progress` / `blocked` / `done` | pending→in_progress→done (可 blocked→in_progress) |
| Report | `draft` / `complete` | draft→complete |

**冻结定义：** status 从 `draft` 变为 `active`（或 `accepted`），伴随独立 commit。冻结后不可原地修改——要改必须退回 DESIGN、新建版本、旧版本归档。

---

## 6 条系统边界

| 边界 | 共享约束 |
|------|---------|
| 契约与执行分离 | 四类契约（业务/接口/质量/架构）冻结后，才能进入 DEVELOP 写代码。冻结 = status→active + 独立 commit |
| 验证先于实现 | 测试基础设施（轨道 C）先于编码完成。低层机器化，高层可由 Agent 判定 |
| 状态变更=原子承诺 | 每个 Plan 至少在一个独立 Git branch 中执行。状态流转不可跳跃或回跳（除修复循环和 DESIGN 回退） |
| 可追溯性 | 语义链：AC 编号 → Plan 引用 → Commit message → Report 记录。文档/代码 commit 分离 |
| 自描述入口 | 入口路径 `AGENTS.md → docs/README.md → 各级 README → 具体文档` 必须完整。Agent 零上下文启动仅凭文件系统即可理解项目 |
| 设计者意图为根 | 顶层目标来自 Designer。Executor 不可创造新目标。边界保护职责分离，不绑定特定身份 |

---

## Git 规则

- **文档变更与代码变更永远分开 commit。** 一次 commit 只含文档或只含代码
- Commit 格式：`<type>(<scope>): <简述>`。文档 commit 用 `docs(<scope>):`，代码 commit 用 `feat/fix/refactor/test/chore`
- Plan 执行在独立 branch 中：`git checkout -b plan/000x-任务名`
- 状态变更伴随独立 commit：`docs(state): DESIGN → DEVELOP`
- 关联用语义链（正文中引用文件路径和 AC 编号），不依赖 frontmatter 的 related 字段

---

## 模板使用

模板在 `assets/templates/` 中。使用时复制到项目对应位置，按实际情况填写内容。

- 初始化项目：复制 `assets/templates/` 根目录下的 AGENTS.md、CONTRIBUTING.md、CHANGELOG.md 以及 `docs/` 全部内容
- 创建 Design Spec：复制 `assets/templates/docs/design/001-spec.md`
- 创建 ADR：复制 `assets/templates/docs/adr/0001-template.md`
- 创建 Plan/Report：复制 `assets/templates/docs/plans/0001-template/` 下对应文件

模板是参考实现，可根据项目复杂度简化或扩展，但四类契约必须覆盖。

---

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