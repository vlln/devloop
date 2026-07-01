---
name: devpact
description: 契约驱动的项目开发系统。当 Agent 需要初始化项目、理解当前阶段能做什么、推进状态、创建和管理文档时使用。
---

# Project Pact

## 系统全貌

项目开发遵循 6 阶段状态机。每个阶段有明确的**证明命题**和**出口把关**——Agent 通过出口把关证明该阶段的命题成立，方可推进。

```
INIT ──→ DESIGN ──→ DEVELOP ──→ INTEGRATE ──→ PRE_RELEASE ──→ RELEASE
            ↑                       │  ↑
            │                       └──┘
            │                   (内部修复循环)
            │
            └──────────────────────────┘
               (架构变更回退)

RELEASE → DESIGN  (新一轮迭代)
```

### 阶段证明链

| 阶段 | 证明命题 | 出口把关（Agent 必须验证） |
|------|---------|--------------------------|
| **INIT** | 项目骨架就绪，可进入设计 | 目录结构存在、AGENTS.md/CONTRIBUTING.md/CHANGELOG.md 存在、Git 已初始化 |
| **DESIGN** | 契约已冻结，可进入编码 | vision.md 含业务目标+用户范围、Design Spec 含用户故事+模块划分+AC（内容级检查）、核心 ADR 全部 status=accepted（技术选型/存储/架构模式，验证段不为空）、Plan 已拆解且含执行边界 |
| **DEVELOP** | 各轨道独立功能正确，可进入集成验证 | 全部轨道 Plan done、各轨道 Report 中 AC 全部 ✅ |
| **INTEGRATE** | 跨轨道协作正确，可进入预发布 | 全部测试层通过（单元→集成→接口→E2E），无阻塞级缺陷 |
| **PRE_RELEASE** | 部署环境就绪，可发布 | CD 部署到 staging 成功、冒烟测试通过、环境配置验证通过、版本号和回滚方案确认 |
| **RELEASE** | 本轮迭代已闭环，可开始新迭代 | CD 部署到 production 成功、生产冒烟测试通过、版本 tag 已打、CHANGELOG 已整理、归档完成 |

**出口把关是不可跳过的硬性检查。** Agent 在每个阶段结束时必须逐项验证出口把关，全部通过方可推进。如果出口把关不通过，留在当前阶段修复，不得推进。

**DEVELOP 内部并行轨道：** 契约冻结后全部并行，每条轨道在独立 Git branch 中执行。轨道 A（测试基础设施）必须最先完成。轨道数量取决于项目类型（例如全栈项目 5 条，CLI 工具 2 条）。

**Agent 无状态。** 任何 Agent 可以随时被终止，下次启动时仅凭文件系统恢复状态。所有关键信息在文档中，不在对话历史中。

---

## 迭代模式

同一状态机骨架，三种迭代模式。Agent 进入 DESIGN 时根据已有文档状态自动判断：

### 首次设计（INIT → DESIGN）

所有文档全新创建。走完所有子阶段，不加跳过。

### 增量迭代（RELEASE → DESIGN）

已有文档已冻结。进入 DESIGN 后：
- vision.md 已 active → 跳过，不重写
- Design Spec 已 active → 在现有文档上追加，不重写
- 已有 ADR 已 accepted → 不修改，仅新增 ADR
- 已有 Plan 已 done → 新建 Plan，不重建

### 设计变更（DEVELOP → DESIGN，架构颠覆退回）

从 DEVELOP 因架构颠覆退回。进入 DESIGN 后走「设计变更」子阶段：
1. 定级：确认为架构颠覆（非轻微约束）
2. ADR 修订：旧 ADR 追加修订记录，或标记 superseded + 新建 ADR
3. 传导下游：同步更新受影响的 Design Spec、通知受影响轨道、更新 Plan
4. 恢复编码：以新 ADR 为依据重新推进到 DEVELOP

**注意：** 轻微约束（依赖能用但方式与预期不一致）在 DEVELOP 内解决，不退回 DESIGN。

---

## 安装系统

如果是全新项目，初始化项目骨架：

```
1. 复制 assets/templates/ 下的 AGENTS.md, CONTRIBUTING.md, CHANGELOG.md 到项目根目录
2. 复制 assets/templates/docs/ 下全部内容到项目 docs/ 目录
3. 在 docs/README.md 中设置当前阶段为 INIT
4. 提交（commit message 描述变更内容，格式见 CONTRIBUTING.md）
5. 推进: 更新 docs/README.md 当前阶段为 DESIGN，追加最近事件，提交。约定前缀 `docs(state):`
```

系统已安装后，直接进入下一步。

---

## 导航系统

系统文档是自描述的。按以下顺序读取：

```
1. AGENTS.md           → 项目入口地图：文档类型、目录结构、系统边界、阶段行为
2. docs/README.md      → 当前系统状态 + 行为边界（首先读取！）
3. CONTRIBUTING.md     → 编码/测试/PR 规范（项目自定义）
4. 各级 README.md      → 子目录索引和状态
5. 具体文档             → Vision / Design Spec / ADR / Plan / Report
```

**系统规则和约定（文档类型、命名规范、frontmatter、Git 规则）在 AGENTS.md 和 CONTRIBUTING.md 中。** 本 skill 不重复这些内容。

---

## 系统规则

### 文档命名

| 文档 | 格式 | 示例 |
|------|------|------|
| Vision | `vision.md` | `vision.md` |
| Design Spec | `00x-xxxx.md` | `001-vagent.md` |
| ADR | `000x-xxxx.md` | `0001-db-choice.md` |
| Plan 文件夹 | `000x-简短描述` | `0001-订单模块` |
| Plan 子任务 | `0x-plan-xxx.md` | `01-plan-order-api.md` |
| Report | `0x-report-xxx.md` | `01-report-order-api.md` |

### Frontmatter

以下文档类型使用 YAML frontmatter（`---` 包裹），位于文件最顶部：

| 文档类型 | 必填字段 |
|----------|----------|
| Vision | `title`, `description`, `type: vision`, `status`, `created` |
| Design Spec | `title`, `description`, `type: design`, `status`, `version`, `created` |
| ADR | `title`, `description`, `type: adr`, `status`, `created` |
| Plan | `title`, `description`, `type: plan`, `status`, `created` |
| Report | `title`, `description`, `type: report`, `status`, `created` |

`created` 使用 ISO 8601 格式 (`YYYY-MM-DDTHH:MM:SSZ`)。`version` 仅 Design Spec 使用，整数递增。

以下文件**不使用** frontmatter：
- AGENTS.md、CONTRIBUTING.md、CHANGELOG.md
- 所有 README.md

### status 有效值

| 文档类型 | 状态值 | 流转 |
|----------|--------|------|
| Vision | `draft` / `active` / `archived` | draft→active→archived |
| Design Spec | `draft` / `active` / `archived` | draft→active→archived（同时只有一个 active） |
| ADR | `draft` / `accepted` / `superseded` / `deprecated` | draft→accepted→superseded/deprecated |
| Plan | `pending` / `in_progress` / `blocked` / `done` | pending→in_progress→done (可 blocked→in_progress) |
| Report | `draft` / `complete` | draft→complete |

**冻结定义：** status 从 `draft` 变为 `active`（或 `accepted`），伴随独立 commit。冻结后不可原地修改——要改必须退回 DESIGN、新建版本、旧版本归档。

### 语义链

关联通过文档正文中的文本引用和命名约定表达，不依赖 frontmatter 的 related 字段：

```
Design Spec AC-003
  → Plan 01-plan-order-api.md 步骤 2: "实现 AC-003 订单创建"
    → Commit: "feat(order): 实现 AC-003 订单创建"
      → Report 01-report-order-api.md: "AC-003 ✅, commit abc123"
```

### Git 规则

- 文档变更和代码变更永远分开 commit
- 状态变更伴随独立 commit，约定前缀 `docs(state):`
- 文档 commit 格式：`docs(<scope>): <简述>`
- Plan 执行在独立 branch 中

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