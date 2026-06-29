---
title: Agent Coding System — 文档规范设计
description: 无人循环自主 Agent 编码系统的文档规范设计，定义文档体系的结构、规则和设计决策。
type: design
status: active
version: 1
created: 2026-06-26T00:00:00Z
---

> 本文档是规范本身的 Design Spec，描述文档体系的设计决策、约束和完整规则。
> 模板实现见 [template/](template/)。

---

## 一、概述与目标

### 目标

设计一套**无人循环自主 Agent 编码系统**的文档规范，使 Agent 能够：

1. 从零接手项目时，通过文档完整了解上下文，无需人工持续 prompt
2. 在明确的权限边界内自主执行开发任务
3. 所有产出可追溯（计划→执行→报告→commit）

### 适用范围

本文档定义的是**文档体系的结构和规则**。编码规范、Git 工作流等见 [template/CONTRIBUTING.md](template/CONTRIBUTING.md)。

### 本文档与 template 的关系

```
agent-coding-spec.md  ← 元设计（本文档）：描述"为什么这样设计"
template/             ← 交付物：使用者拿到的完整模板
```

---

## 二、核心设计原则

### 2.1 渐进式披露

每层文档只描述**下一级**的内容，不越级展开细节。

```
AGENTS.md（项目入口地图）
  └── docs/README.md（子目录列表 + 当前系统状态）
        ├── design/README.md（Spec 版本索引）→ 001-spec.md（模板在此）
        ├── adr/README.md（决策索引）        → 0000-template.md（模板在此）
        └── plans/README.md（任务列表）      → 0001-template/README.md（模板在此）
```

模板格式只出现在模板文件自己所在的那一层，上层只做引用。

### 2.2 单一事实源

每类信息只有一个权威定义位置，其余文档只引用不复制。

| 信息类型 | 唯一定义位置 | 其余文档 |
|----------|-------------|----------|
| 业务需求、接口、数据模型、AC | Design Spec | 只引用，不复制 |
| 技术选型、架构折中 | ADR | 只引用，不复制 |
| 顶层愿景、硬性约束 | Vision | 只引用，不复制 |
| 编码规范、Git 规则 | CONTRIBUTING.md | 只引用，不复制 |
| 系统当前所处阶段 | docs/README.md | 只引用，不复制 |

### 2.3 角色与权责

系统中有两个角色，不绑定到"人"或"Agent"的具体身份：

```
Designer（设计者）   ← 负责规划、设计、决策
Executor（执行者）   ← 负责实现、执行
```

**第一推动力（固定）：**
系统的唯一固定起点是**Designer 提供的初始设计意图**。这是整个系统的第一推动力，不可被 Executor 僭越。

**协作光谱：**
除第一推动力外，所有工作都是 Designer 与 Executor 之间的协作。具体由谁执行取决于自动化程度：

| 自动化程度 | Designer | Executor | 典型场景 |
|-----------|----------|----------|----------|
| 高 | Agent | Agent | Agent 独立分析需求、编写 Design/ADR，人仅确认状态变更 |
| 中 | 人 + Agent 讨论 | Agent | 人描述需求，Agent 起草 Design/ADR，人确认后冻结 |
| 低 | 人 | Agent | 人编写完整 Design/ADR，Agent 读取后执行 Plan |

**核心规则：权责 = 状态变更权，而非内容编写权。**
- 谁有权变更文档的 `status` 字段，决定了该文档的权责归属
- 内容本身可以由任何角色协作编写
- 状态变更伴随 Git commit，commit 是状态变更的物理锚点

**状态变更权分配：**

| 文档类型 | 状态变更权 | 说明 |
|----------|-----------|------|
| Vision | Designer | Designer 定稿后冻结，重大转型才变更 |
| Design Spec | Designer | Designer 定稿后冻结，新版本由 Designer 创建 |
| ADR | Designer | Designer 决策采纳/替代/废弃 |
| Plan | Executor | Executor 在生命周期内管理状态流转 |
| Report | Executor | Executor 完成时提交 |
| CHANGELOG | Executor（追加 Unreleased）、Designer（整理发布） | — |
| 系统状态 | Designer（阶段推进）、Executor（DEVELOP↔INTEGRATE 内部循环） | 见第四节 |

**发现权威文档需修改时：**
Executor 不自行修改 Vision/Design/ADR，在 Report 中记录建议，由 Designer 决策。

### 2.4 Git 作为存储底座

Git 是整个项目（代码 + 文档）的**存储和版本控制器**。系统中所有状态流转和迭代都以 Git 动作作为切分边界：

- **一次迭代** = 隔离环境内完整执行任务 → 通过全部校验 → 原子合并入主分支。合并动作是项目进度的唯一有效变更点。
- **文档变更**必须独立 Commit，不与代码混合。Commit message 遵循 `docs(<scope>): <简述>` 格式。
- **状态流转**（如 Plan 从 `in_progress` → `done`，系统状态从 `DESIGN` → `DEVELOP`）伴随对应的 Git commit，commit 是状态变更的物理锚点。
- **容错**：任务异常中断 → 丢弃隔离环境，主分支零污染。误操作通过 Git 历史回退。

---

## 三、系统边界

以下 6 条边界是系统不可违反的硬性约束。每条边界内部有 Level 1 子边界（机制约束，不可违反）和 Level 2 实现模式（可变，按项目类型自适应）。

### 边界 1：契约与执行分离

在编写任何代码之前，契约必须冻结。这是并行化的唯一前提。

**Level 1 — 最小契约类型集：**

系统不强制具体的文档名或模板，但以下四类契约信息必须存在，且在设计阶段完成冻结：

| 契约类型 | 必须回答的问题 | 冻结时机 |
|----------|--------------|----------|
| 业务契约 | 做什么、为谁做、为什么 | DESIGN 阶段最早冻结 |
| 接口契约 | 模块间如何通信、数据长什么样 | 业务契约冻结后 |
| 质量契约 | 什么算成功、什么算失败（AC） | 与业务契约同步冻结 |
| 架构契约 | 技术选型、约束、取舍 | 接口契约定义前冻结 |

**Level 1 — 冻结的硬性定义：**

- 冻结 = 对应文档的 `status` 字段从 `draft` 变为 `active`，伴随独立 Git commit
- 冻结后不可原地修改。要改必须走正式回退：退回 DESIGN → 新建版本 → 旧版本归档
- 复杂度等级决定契约密度（一个文件 vs 多个文件），不改变冻结的强制性

**Level 1 — 并行化的唯一前提：**

接口契约 + 质量契约已冻结。此时前后端可基于同一套 Mock 和 AC 分叉并行。

**Level 2 — 实现模式：**

- 小项目（CLI 工具）：业务契约 + 质量契约合并为一个文件，架构契约内嵌其中
- 中项目（后端 API）：Design Spec + ADR 分离
- 大项目（全栈）：四种契约各自独立文件 + API 契约文档（OpenAPI）

### 边界 2：验证先于实现

验证标准（AC、测试用例）必须在实现之前或独立于实现存在。测试不是"写完代码后跑一下"，而是"先定义什么算成功，再尝试到达成功"。

**Level 1 — 验证分层智能化：**

```
低层（近代码）→ 机器化
  单元测试、接口契约校验、类型检查
  → 无歧义、可复用、速度快

高层（近意图）→ 智能化（Agent）
  E2E 语义验证、UI 合理性判断、AC 中模糊标准的判定
  → 很多细节只有做了才知道，强行机器化破坏灵活性
```

**Level 1 — 最小验证系统：**

- AC 应尽可能可量化，但**不强制机器可验证**
- 机器能验证的尽量机器化（单元测试、契约测试）
- 机器做不到的交给 Agent 判断（语义理解、交互合理性），Agent 在 Report 中给出判定结论
- 测试系统可以是"机器 + Agent"的组合——例如独立的测试 Agent，读取 AC 和代码产物，执行机器测试 + 语义判断

**Level 1 — 验证与编码的时序：**

编码开始时，测试武器已就位。测试基础设施（轨道 C）必须在编码开始前完成。

**Level 1 — 验证层级按项目类型自底向上叠加：**

```
单元测试（必选，所有项目类型）
  → 集成测试（必选，所有项目类型）
    → 接口契约测试（API 类项目）
      → 接口编排测试（多接口联动场景）
        → E2E 测试（有 UI 的项目）
          → 视觉回归（前端项目）
```

每层都是合并闸门，不可跳过。从最内层向外逐层叠加，直到项目类型所需的最后一层。

**Level 2 — 实现模式：**

- 机器化测试：Jest/Vitest/Playwright 等框架
- Agent 化测试：独立的测试 Agent，读取 AC + 代码产物，执行语义判断和探索性验证

### 边界 3：状态变更 = 原子承诺

状态从 DESIGN 变为 DEVELOP 是一个承诺——"契约已冻结，现在开始基于此契约构建"。这个承诺不可半途撤销。

**Level 1 — 最小执行边界：**

- 每个 Plan 至少在一个**独立 Git branch** 中执行。branch 是底线，不可省略
- worktree 是**并行优化手段**（可选）。串行场景下不用 worktree，仅用 branch

**Level 1 — 变更锚点：**

| 锚点 | 含义 |
|------|------|
| commit | 状态变更的物理锚点。DESIGN→DEVELOP 的那次 commit 携带"契约已冻结"的语义 |
| merge | 迭代进度的原子单位。一次 merge = 一个完整的开发→集成→测试闭环 |
| 具体操作 | commit/merge/rebase/squash 由项目 Git 规范灵活决定，系统不强制特定操作 |

**Level 1 — 异常处理：**

| 异常 | 处理 |
|------|------|
| Agent 崩溃 | 丢弃 branch/worktree，任务重置为 `pending`，无半完成状态遗留 |
| 步骤失败 | branch 内回退至步骤快照，内部重试 |
| 架构不可行（DEVELOP 中发现） | 停止 DEVELOP，退回 DESIGN，不尝试在 DEVELOP 中修改契约 |
| 局部 bug（INTEGRATE 中发现） | DEVELOP ↔ INTEGRATE 修复循环，不触发全局回退 |

**Level 2 — 实现模式：**

- 串行项目：每个 Plan 一个 branch，顺序执行
- 并行项目：多个 Plan 在独立 worktree 中并行执行

### 边界 4：可追溯性

每一次变更都必须能追溯到：谁决定的（ADR/Design）→ 谁计划的（Plan）→ 谁执行的（Report）→ 哪次 commit。

**Level 1 — 语义链（底线）：**

追溯通过文档正文中的文本引用、命名约定、commit message 关联自然形成，不依赖 frontmatter 的 `related_*` 字段：

```
Design Spec AC-003
  → Plan 01-plan-order-api.md 步骤 2: "实现 AC-003 订单创建"
    → Commit message: "feat(order): 实现 AC-003 订单创建"
      → Report 01-report-order-api.md: "AC-003 ✅ 通过, commit abc123"
```

**Level 1 — 文档变更与代码变更分离：**

一次 commit 要么是文档，要么是代码，不混合。这是追溯粒度——你能精确知道"这个 spec 变更发生在哪个 commit"。

**Level 2 — Key 化（优化）：**

frontmatter 字段、结构化元数据。按需使用，便于程序/Agent 快速检索。断链 = 警告，不阻塞合并——过度强制追溯会产生虚假的合规。

**Level 2 — 准入判断（灵活）：**

- 程序化：简单场景，检查 `status` 字段
- Agent 化：复杂场景，语义理解、上下文判断
- 准入判断本身可以是程序也可以是 Agent，根据需要而定

### 边界 5：自描述入口

任何 Agent（无论有无上下文）进入系统后，仅凭文件系统就能理解：当前处于什么阶段、能做什么不能做什么、去哪里找下一步需要的信息。

**Level 1 — 入口路径：**

```
AGENTS.md → docs/README.md（当前状态）→ 各级 README（索引）→ 具体文档
```

这条路径必须始终完整，不可断裂。

**Level 1 — 当前状态单点可见：**

系统当前所处阶段 + 行为边界在 `docs/README.md` 中追踪，由调度层在状态变更时更新。

**Level 1 — 零上下文启动：**

系统不依赖外部记忆或对话历史。Agent 仅凭文件系统即可理解项目全貌。

### 边界 6：设计者意图为根

系统没有自主目标。所有顶层目标的唯一来源是 Designer 的设计意图。

**Level 1 — 目标来源：**

所有顶层目标来自 Designer 的设计意图。Executor 不可创造新的顶层目标。

**Level 1 — 决策权归属：**

架构变更、版本发布、需求调整由 Designer 决策。

**Level 1 — 角色边界固定：**

Executor 可分解、细化、执行，不可新增业务需求。此边界保护的是**职责分离**——Designer 的意图不被 Executor 在执行过程中僭越——而非特定身份。Designer 可以是另一个 Agent，人有时也可以是 Executor。

---

## 四、系统生命周期状态机

系统状态机是整个开发流程的核心控制骨架。它定义了项目从初始化到发布完成的完整生命周期，规定了每个阶段**能做什么、不能做什么、如何进入下一阶段**。

### 4.1 设计原则

- **外层串行，内层并行。** 状态机本身是串行骨架（关口），并行发生在状态内部。
- **契约是并行化的唯一前提。** 一旦接口契约 + 质量契约冻结，DEVELOP 内部各轨道可完全并行。
- **唯一串行关口：INTEGRATE。** 必须等所有并行模块联调完成才能进入。这是整个流程中唯一的强制串行点。

### 4.2 状态总览

```
INIT ──→ DESIGN ──→ DEVELOP ──→ INTEGRATE ──→ PRE_RELEASE ──→ RELEASE
            ↑          │  ↑                      │
            │          │  └──────────────────────┘
            │          │        (缺陷修复循环)
            │          │
            └──────────┘
         (架构变更回退)

RELEASE → DESIGN  (新一轮迭代)
```

6 个状态，1 个内部循环（`DEVELOP ↔ INTEGRATE` 修复循环）。

### 4.3 各状态定义

#### INIT — 项目初始化

| 维度 | 定义 |
|------|------|
| **含义** | 项目骨架搭建。纯串行，前置环节 |
| **允许** | 创建目录结构、AGENTS.md/CONTRIBUTING.md/CHANGELOG.md、初始化 Git、初始化 CI 配置 |
| **禁止** | 编写 Vision/Design/ADR/Plan、编写业务代码（src/） |
| **准入条件** | —（项目启动的起点） |
| **→ DESIGN 条件** | 目录结构就位、AGENTS.md/CONTRIBUTING.md/CHANGELOG.md 已创建、Git 仓库已初始化 |
| **触发者** | Designer |

#### DESIGN — 规划设计

| 维度 | 定义 |
|------|------|
| **含义** | 需求分析、架构设计、契约定义。**主体串行**（因果链），后期可有限并行 |
| **允许** | 编写 Vision → Design Spec → ADR → API 契约 → 拆解 Plan；讨论技术方案 |
| **禁止** | 编写业务代码（src/）、执行 Plan |
| **准入条件** | INIT 完成 |
| **→ DEVELOP 条件** | 四类契约已冻结（见边界 1）：业务契约 + 接口契约 + 质量契约 + 架构契约 status=active；Plan 任务板已拆解完成 |
| **回退** | 发现架构方案不可行 → 退回 DESIGN 自身（重新设计），不跳回 INIT |
| **触发者** | Designer |

**DESIGN 内部因果链：**

```
Vision → Design Spec → ADR → API 契约定义 → Plan 拆解
  │                    │
  │                    └──→ 测试用例设计（AC 定稿后可并行）
  │
  └── 一次性定稿，几乎不修改
```

- Vision 固定后，Design Spec 基于 Vision 编写
- Design Spec 的 AC 定稿后，测试用例设计可与 ADR/API 契约并行
- API 契约需要 Design Spec（接口定义）+ ADR（技术选型）同时就位
- Plan 拆解是所有前序产出的汇总，最后完成

#### DEVELOP — 编码开发（最高并行期）

| 维度 | 定义 |
|------|------|
| **含义** | 基于冻结契约，多轨道并行执行。Executor 在隔离环境中完成编码和自测 |
| **允许** | 领取任务、编写代码、单元测试、集成测试、更新 Plan/Report 状态 |
| **禁止** | 修改 Vision/Design/ADR、修改全局契约 |
| **准入条件** | DESIGN 完成（四类契约已冻结，Plan 拆解完成） |
| **→ INTEGRATE 条件** | 全部并行轨道 Plan done |
| **触发者** | Executor（通过调度层），状态变更伴随 Plan done 的 commit |

**DEVELOP 内部并行轨道：**

DESIGN 冻结的契约是并行化的唯一前提。以下轨道在接口契约 + 质量契约就位后**完全独立，互不等待**：

```
DESIGN（契约冻结）
  │
  ├─ 轨道 A: 后端开发
  │   依赖: 接口契约 + 数据模型
  │   隔离: 独立 Git branch（并行场景使用 worktree 优化）
  │   产出: 接口实现、服务逻辑、单元测试
  │
  ├─ 轨道 B: 前端开发
  │   依赖: API Mock + UI 约束
  │   隔离: 独立 Git branch（并行场景使用 worktree 优化）
  │   产出: 页面交互、组件、组件自测
  │
  ├─ 轨道 C: 测试基础设施
  │   依赖: 质量契约（AC）+ 架构契约
  │   隔离: 独立 Git branch（不依赖 A/B 的代码）
  │   产出: 测试环境、测试数据、自动化脚本、E2E 脚手架
  │   时机: **先于 A/B 完成**，确保 Executor 写代码时测试武器已就位
  │
  └─ 轨道 D: 数据库 / 部署脚本
      依赖: 数据模型 + 架构契约
      隔离: 独立 Git branch（并行场景使用 worktree 优化）
      产出: migration 脚本、CI/CD 配置、环境配置
```

**并行规则：**
- 每个轨道 = 一个独立的 Plan 文件夹（`docs/plans/000x-xxx/`）
- 每个轨道在独立的 Git branch 中执行，互不污染
- 轨道 C（测试基础设施）应**最先完成**，作为 A/B 执行时的质量闸门
- 轨道 A 和 B 可以同时 `in_progress`，由不同 Executor 或同一 Executor 串行领取
- 无依赖、无公共资源竞争的轨道自动并行；共享资源（如数据表结构）的轨道设置软锁

#### INTEGRATE — 集成校验（唯一串行关口）

| 维度 | 定义 |
|------|------|
| **含义** | 整体模块联调完成，打包部署到测试环境，正式提测。**整个流程中唯一必须等所有模块完成的阶段** |
| **允许** | 执行全量测试、修复集成问题、生成测试报告 |
| **禁止** | 新增功能代码、修改 Design/ADR |
| **准入条件** | DEVELOP 全部轨道 Plan done |
| **→ PRE_RELEASE 条件** | 全部测试层通过（见边界 2 验证层级） |
| **触发者** | Executor（通过调度层），以测试全部通过为硬性闸门 |

**INTEGRATE 内部修复循环：**

```
INTEGRATE（执行全量测试）
  │
  ├─ 全部通过 → PRE_RELEASE
  │
  └─ 测试失败 → 退回 DEVELOP 对应轨道修复 → 再测 → INTEGRATE
       │
       └─ 多层测试（自底向上）：
           单元测试 → 集成测试 → 接口契约 → 接口编排 → E2E → 视觉回归
           （每层都是闸门，不可跳过）
```

- 修复循环是 `DEVELOP ↔ INTEGRATE` 之间的局部循环，不触发全局状态回退
- 仅局部 bug 在此循环内修复；若发现设计缺陷 → 退回 `DESIGN`（见边界 3 异常处理）
- 测试分层执行：先单模块，再跨模块集成，最后全流程 E2E
- 低层机器化测试，高层可引入 Agent 化测试（见边界 2）

#### PRE_RELEASE — 预发布验证

| 维度 | 定义 |
|------|------|
| **含义** | 预发布环境验证、版本号确认、回滚方案检查 |
| **允许** | 环境配置检查、版本号确认、回滚脚本验证、部署清单检查 |
| **禁止** | 修改代码、修改文档 |
| **准入条件** | INTEGRATE 全部测试通过 |
| **→ RELEASE 条件** | 预发布验证通过，版本号、回滚方案确认无误 |
| **触发者** | Designer |

#### RELEASE — 迭代闭环

| 维度 | 定义 |
|------|------|
| **含义** | 版本归档、迭代记录更新，本轮迭代结束 |
| **允许** | 版本归档、CHANGELOG 整理、迭代复盘、文档索引更新 |
| **禁止** | 修改任何代码 |
| **准入条件** | PRE_RELEASE 验证通过 |
| **→ DESIGN 条件** | 新一轮迭代启动（Designer 发起） |
| **触发者** | Designer |

### 4.4 流转刚性规则

| 规则 | 说明 |
|------|------|
| 禁止跳跃 | 不允许跨状态流转（如 INIT → DEVELOP） |
| 禁止回跳 | 除 `DEVELOP ↔ INTEGRATE` 修复循环和 `DESIGN` 回退外，不允许逆向流转 |
| 架构变更强制回退 | 架构方案发生颠覆性变更 → 强制退回 `DESIGN`，不允许在 DEVELOP 阶段直接修改契约 |
| 局部 bug 内部循环 | 仅局部 bug、代码实现问题 → 在 `DEVELOP ↔ INTEGRATE` 修复循环内解决，不触发全局回退 |
| 准入灵活 | 进入下一状态必须通过前置准入检查。准入判断可以是程序（检查 status 字段）也可以是 Agent（语义理解），根据需要而定 |

### 4.5 双层可见性

系统状态机定义在本文档中，但运行在两个层面：

| 层面 | 使用者 | 用途 |
|------|--------|------|
| **外部调度层** | 调度/协调 Agent | 读取状态机定义，执行状态流转、准入检查、并行轨道分配、隔离环境创建与回收、异常上浮。**主动推进状态变更** |
| **项目文档层** | 项目内 Executor | 读取 `docs/README.md` 中的当前状态字段，**自我约束**：判断当前阶段能做什么、不能做什么、自己属于哪个并行轨道 |

**当前状态追踪：**
系统当前所处阶段记录在 `docs/README.md` 的「当前系统状态」段中，由调度层在状态变更时更新。项目内 Executor 启动时读取该字段，确认自己处于哪个阶段以及行为边界。

---

## 五、文档体系

### 5.1 Vision（docs/vision.md）

| 维度 | 定义 |
|------|------|
| **定位** | 全局唯一顶层愿景：业务目标、用户范围、顶层架构约束、非功能指标、硬性规则 |
| **创建时机** | 项目启动时（DESIGN 阶段），由 Designer 编写 |
| **变更规则** | 仅重大业务转型才修订，每次变更独立 Git Commit |
| **生命周期** | 长期不变，几乎不修改 |
| **不定义** | 实现细节、技术选型、接口定义 |

### 5.2 Design Spec（docs/design/00x-xxxx.md）

| 维度 | 定义 |
|------|------|
| **定位** | 固化落地方案 + AC 验收标准。覆盖业务契约和接口契约。所有业务需求的**唯一事实源** |
| **创建时机** | DESIGN 阶段，由 Designer 编写 |
| **变更规则** | 定稿后固化。日常迭代不修改。重大重构时归档旧版，新建编号（001→002） |
| **生命周期** | 同时只有一个 active 版本，旧版标记 archived |
| **不定义** | 技术选型理由（那是 ADR）、顶层愿景（那是 Vision） |
| **AC 验收标准** | 每条尽可能可量化。机器可验证的 AC 尽量机器化；机器不可验证的 AC 由 Agent 在 Report 中给出判定结论（见边界 2） |

### 5.3 ADR（docs/adr/000x-xxxx.md）

| 维度 | 定义 |
|------|------|
| **定位** | 架构决策记录：技术选型、方案折中、风险取舍。覆盖架构契约。覆盖测试架构、部署架构、数据架构 |
| **创建时机** | DESIGN 阶段或任何需要技术决策时，由 Designer 编写 |
| **变更规则** | 持续新增，不删除。状态流转：draft → accepted → superseded/deprecated |
| **生命周期** | 长期留存，永久追溯 |
| **不定义** | 业务需求（那是 Design）、编码规范（那是 CONTRIBUTING.md） |

### 5.4 Plan + Report（docs/plans/000x-任务名/）

| 维度 | 定义 |
|------|------|
| **定位** | 单次执行容器。每个文件夹是一次独立任务，对应 DEVELOP 中的一个并行轨道 |
| **创建时机** | DESIGN 阶段由 Designer 创建，或 DEVELOP 阶段由 Executor 自行生成 |
| **变更规则** | 执行中持续更新进度，完成后不改 |
| **生命周期** | 短期，任务完成即完结。原地保留不删除，README 状态字段区分 |
| **不定义** | 长期架构事实（接口/数据表/业务规则） |

**内部结构：**

```
000x-任务名/
├── README.md              # 子任务状态表 + commit 映射
├── 01-plan-xxx.md         # 子任务计划
├── 01-report-xxx.md       # 子任务报告（一一对应）
├── 02-plan-yyy.md
├── 02-report-yyy.md
└── artifacts/             # 执行产出
```

**Plan/Report 成对规则：**
- 每个 Plan 对应一个 Report，一一对应
- 一个 Plan 可对应多个 commit，在 README.md 状态表中记录
- 若同一 Plan 需要多次执行，续写/重整同一个 Report
- Report 中记录：执行摘要、关联 commit、产物清单、AC 验收结果、测试摘要、遗留问题、对权威文档的改动建议

### 5.5 CHANGELOG.md（项目根目录）

| 维度 | 定义 |
|------|------|
| **定位** | 项目版本变更记录，遵循 [Keep a Changelog](https://keepachangelog.com/) |
| **创建时机** | INIT 阶段创建 |
| **变更规则** | Executor 每次完成任务后追加 `[Unreleased]` 段；RELEASE 阶段由 Designer 整理为正式版本条目 |
| **生命周期** | 持续更新，不删除 |
| **不定义** | 任务状态（那是 Plan）、技术决策（那是 ADR） |

### 5.6 README.md（目录索引 + 系统状态）

每个子目录有独立的 README.md，作为该目录的索引和状态说明。

| 目录 | README 内容 |
|------|------------|
| `docs/` | 子目录列表、**当前系统状态**（见第四节）、当前生效版本 |
| `docs/design/` | Spec 版本列表（文件、状态）、命名规范 |
| `docs/adr/` | 决策列表（编号、标题、状态）、命名规范 |
| `docs/plans/` | 任务列表（编号、标题、状态、创建时间、并行轨道标记）、命名规范 |
| Plan 容器内 | 子任务状态表（编号、子任务、Plan、Report、状态、Commits） |

---

## 六、文档状态定义

每种文档类型有各自独立的状态集合和流转规则。不同文档类型的状态语义不共享。

### 6.1 Vision

```
draft ──→ active ──→ archived
```

| 状态 | 含义 | 状态变更权 |
|------|------|-----------|
| `draft` | 草稿，尚未定稿 | Designer |
| `active` | 已定稿，当前生效 | Designer |
| `archived` | 因重大业务转型被归档 | Designer |

- `draft → active`：定稿发布，伴随独立 Git commit
- `active → archived`：发生重大业务转型，旧 Vision 归档，新建 Vision 文件

### 6.2 Design Spec

```
draft ──→ active ──→ archived
```

| 状态 | 含义 | 状态变更权 |
|------|------|-----------|
| `draft` | 编写中，尚未冻结 | Designer |
| `active` | 已冻结，当前唯一生效版本 | Designer |
| `archived` | 被新版本替代，原地保留供追溯 | Designer |

- `draft → active`：定稿冻结，伴随独立 Git commit。冻结后不可修改。
- `active → archived`：新版本 Design Spec 创建并冻结后，旧版本归档。同时只有一个 `active`。
- 归档操作：旧 Spec 状态改为 `archived`，更新 `docs/design/README.md`。

### 6.3 ADR

```
draft ──→ accepted ──→ superseded
  │                      │
  └──────────────────────┴──→ deprecated
```

| 状态 | 含义 | 状态变更权 |
|------|------|-----------|
| `draft` | 提案中，尚未采纳 | Designer |
| `accepted` | 已采纳，当前生效 | Designer |
| `superseded` | 被新 ADR 替代，保留供追溯 | Designer |
| `deprecated` | 已废弃（无替代方案），保留供追溯 | Designer |

- `draft → accepted`：决策被采纳，伴随独立 Git commit
- `accepted → superseded`：新 ADR 替代此决策，旧 ADR 在正文中引用新 ADR 路径
- `accepted → deprecated` 或 `draft → deprecated`：决策直接废弃，无需替代

### 6.4 Plan

```
pending ──→ in_progress ──→ done
              │
              └──→ blocked ──→ in_progress
```

| 状态 | 含义 | 状态变更权 |
|------|------|-----------|
| `pending` | 已创建，等待执行 | Executor |
| `in_progress` | 正在执行 | Executor |
| `blocked` | 遇到阻塞，等待外部条件满足 | Executor |
| `done` | 已完成，不再修改 | Executor |

- `pending → in_progress`：Executor 开始执行，伴随 Plan 文件更新
- `in_progress → done`：全部步骤完成且 AC 全部通过，伴随 Report 提交和 Git commit
- `in_progress → blocked`：遇到无法自动解决的阻塞，在 Report 中记录阻塞原因
- `blocked → in_progress`：阻塞解除，恢复执行

### 6.5 Report

```
draft ──→ complete
```

| 状态 | 含义 | 状态变更权 |
|------|------|-----------|
| `draft` | 编写中，伴随 Plan 执行同步更新 | Executor |
| `complete` | 已提交，内容不再修改 | Executor |

- `draft → complete`：Plan 执行完毕，所有 AC 验收结果已填入，伴随 Git commit

### 6.6 README.md

README.md 无 frontmatter 状态字段。其内容由对应目录的文档状态自然反映。

### 6.7 CHANGELOG.md

CHANGELOG.md 无 frontmatter。其 `[Unreleased]` 段由 Executor 追加，正式版本条目由 Designer 在 RELEASE 阶段整理发布。

---

## 七、文档格式约定

### 7.1 Frontmatter

以下文档类型使用 YAML frontmatter（`---` 包裹），位于文件最顶部：

| 文档类型 | 必填字段 |
|----------|----------|
| Design Spec | `title`, `description`, `type`, `status`, `version`, `created` |
| ADR | `title`, `description`, `type`, `status`, `created` |
| Plan | `title`, `description`, `type`, `status`, `created` |
| Report | `title`, `description`, `type`, `status`, `created` |

以下文件**不使用** frontmatter：
- AGENTS.md、CONTRIBUTING.md、CHANGELOG.md（标准文件）
- 所有 README.md（目录索引）
- vision.md（全局愿景）

字段说明：
- `title`：文档标题
- `description`：一句话摘要，Agent 无需读正文即可了解文档用途
- `type`：`design` | `adr` | `plan` | `report`
- `status`：见 [六、文档状态定义](#六文档状态定义)
- `created`：ISO 8601 格式，`YYYY-MM-DDTHH:MM:SSZ`
- `version`：仅 Design Spec 使用，整数递增

### 7.2 路径引用

所有跨文档引用使用相对路径 Markdown 链接：`[text](relative/path.md)`。禁止使用反引号包裹的纯文本路径。

### 7.3 命名规范

| 文档 | 命名 | 示例 |
|------|------|------|
| Vision | `vision.md` | `vision.md` |
| Design Spec | `00x-xxxx.md` | `001-spec.md` |
| ADR | `000x-xxxx.md` | `0001-db-choice.md` |
| Plan 文件夹 | `000x-简短描述` | `0001-订单模块` |
| Plan 子任务 | `0x-plan-xxx.md` | `01-plan-order-api.md` |
| Report | `0x-report-xxx.md` | `01-report-order-api.md` |

---

## 八、目录结构

```
项目根目录
├── CHANGELOG.md
├── CONTRIBUTING.md
├── AGENTS.md
├── docs/
│   ├── README.md          # 子目录索引 + 当前系统状态
│   ├── vision.md
│   ├── design/
│   │   ├── README.md
│   │   └── 001-spec.md
│   ├── adr/
│   │   ├── README.md
│   │   └── 0001-xxx.md
│   └── plans/
│       ├── README.md
│       └── 0001-订单模块/
│           ├── README.md
│           ├── 01-plan-xxx.md
│           ├── 01-report-xxx.md
│           └── artifacts/
├── src/
└── .github/workflows/
```

---

## 九、联动规则

当 Designer 修改权威文档时，需遵循以下规则：

### 修改 Design Spec

1. 更新 `docs/design/README.md` 中的版本状态
2. 检查 `docs/adr/README.md` 中所有引用该 Spec 的 ADR，更新状态
3. 若 AC 变更，生成对应 Plan 更新测试
4. 独立 Commit，格式：`docs(design): <简述>`

### 新增/修改 ADR

1. 更新 `docs/adr/README.md`
2. 若替代旧 ADR，旧 ADR 状态改为 `superseded`，新 ADR 正文中引用旧 ADR 路径

### 归档旧 Design

1. 旧 Spec 状态标记为 `archived`（原地保留，不移动）
2. 更新 `docs/design/README.md`
3. 更新 `docs/adr/README.md` 中所有引用

---

## 十、测试体系（可伸缩）

测试不集中在单一文档，也不强制固定层数。根据项目类型，从最内层向外逐层按需搭建。

### 10.1 核心原则

- 测试从**单元测试**（最内层）开始，向外逐层按需叠加
- 每层的测试用例必须绑定 Design Spec 的 AC
- 测试输出做摘要化处理（只返回通过/失败数、失败用例名、失败断言），避免占用 Agent 上下文
- 测试作为合并闸门：全部测试通过方可提交合并
- 低层机器化，高层智能化（见边界 2）

### 10.2 按项目类型伸缩

| 项目类型 | 测试层（从内到外） | 说明 |
|----------|-------------------|------|
| 纯 CLI / 脚本工具 | ① 单元测试 → ② 集成测试 | 集成测试使用退出码、stdout、文件断言替代界面测试 |
| 后端 API 服务 | ① 单元 → ② 集成 → ③ 接口契约 → ④ 接口编排 | 接口编排测试覆盖多接口时序联动 |
| 全栈 Web 应用 | ① 单元 → ② 集成 → ③ 接口契约 → ④ 接口编排 → ⑤ E2E → ⑥ 视觉回归 | 最完整分层，E2E 使用 Playwright/Cypress |
| 前端组件库 | ① 单元 → ② 组件测试 → ③ 视觉回归 | 组件测试验证渲染、属性变化、事件触发 |

### 10.3 各层定位

| 层级 | 测试对象 | 校验目标 | 执行方式 |
|------|----------|----------|----------|
| 单元测试 | 纯函数、工具、状态计算、校验规则、hooks | 给定入参→固定结果 | 机器化 |
| 集成测试 | 多单元组合的内部流程链路 | 局部流程验收 | 机器化 |
| 组件测试 | 组件渲染、属性变化、事件触发 | 介于单元和 E2E 之间 | 机器化 |
| 接口契约测试 | 单个接口的格式、参数、返回结构 | 单个接口本身合法 | 机器化 |
| 接口编排测试 | 多接口调用时序与状态联动 | 串行流程 | 机器化 |
| E2E 测试 | 完整用户交互流程 | 跨接口、跨页面、状态流转 | 机器化 + Agent 化 |
| 视觉回归测试 | 像素差异比对 | 布局、样式、弹窗位置 | 机器化 |

### 10.4 在文档体系中的分布

| 层级 | 内容 | 位置 |
|------|------|------|
| 验收标准 | 每条功能的可量化判定条件 | Design Spec AC |
| 测试架构 | 框架选型、分层策略、覆盖率标准、Mock 方案 | ADR |
| PR 检查 | 提交前必须通过测试 | CONTRIBUTING.md PR Workflow |
| 前端约束 | 组件规范、视觉回归 | Design Spec UI 约束（前端项目） |

---

## 十一、架构分层

本文档规范定义的是**项目文档层**。系统运行依赖一个外部**调度/协调层**，两者是上下层关系，不混合。

### 11.1 项目文档层（template/ 交付物）

- 项目内 Executor 可见、可读
- 包含 Vision、Design、ADR、Plan、Report、CHANGELOG、AGENTS.md、CONTRIBUTING.md
- 遵循本文档定义的所有规范
- **系统状态机定义在本文档中，当前状态追踪在 `docs/README.md`**

### 11.2 调度/协调层（外部基础设施）

- 由更高层级的调度/协调 Agent 执行
- 职责：读取状态机定义和系统边界，执行状态流转、准入检查、任务板管理、Agent 调度、隔离环境（Git worktree/branch）创建与回收、异常上浮与决策推送
- 状态以文件记录，但不属于项目文档体系
- 项目内 Executor **不可见**此层

### 11.3 两层交互

```
调度/协调层（外部）
  │ 读取 agent-coding-spec.md → 获取状态机定义 + 系统边界
  │ 读取 docs/README.md → 获取当前系统状态
  │ 执行准入检查 → 推进状态流转 → 更新 docs/README.md 状态字段
  │ 创建隔离环境（branch/worktree），分配 Executor 执行任务
  │ 校验产出，执行合并
  ▼
项目文档层（template/）
  │ Executor 启动时读取 docs/README.md → 确认当前阶段 + 行为边界
  │ Executor 读写 Plan/Report
  │ Executor 读取 Vision/Design/ADR（发现需修改时在 Report 中建议）
  │ 产出通过 Git commit 反馈到调度层
```

---

## 十二、关键设计决策

| 决策 | 理由 |
|------|------|
| 6 条系统边界为不可违反的硬性约束 | 定义系统骨架，Level 1 约束机制，Level 2 允许自适应 |
| 契约与执行分离 | 并行化的唯一前提。冻结后不可原地修改 |
| 验证先于实现 | 低层机器化，高层智能化。测试武器在编码前就位 |
| 状态变更 = 原子承诺 | branch 为最小执行边界，worktree 为并行优化 |
| 语义链为底线，Key 化为优化 | 准入判断灵活：程序或 Agent 均可 |
| 设计者意图为根 | 顶层目标来源为 Designer，Executor 不可僭越。保护职责分离，非特定身份 |
| 系统状态机为核心控制骨架 | 6 状态 + 内部并行轨道 + DEVELOP↔INTEGRATE 修复循环 |
| AGENTS.md = 项目入口地图 | Agent 读完知道项目全貌、文档在哪、权限边界 |
| CONTRIBUTING.md = GitHub 标准 8 段结构 | 编码/Commit/文档/测试规范统一入口，符合社区惯例 |
| Designer/Executor 角色分离 | 权责 = 状态变更权，不绑定具体身份，支持协作光谱 |
| Executor 可自行生成 Plan | 基于 Design 和 ADR，Executor 有能力拆解执行步骤 |
| Plan/Report 成对 | 每次修改有计划→执行→报告闭环，可追溯 |
| Report 挂钩 commit | 最小执行单元 = 一个 Plan，可能对应多个 commit |
| 测试分层不集中 | AC 在 Design，架构在 ADR，PR 流程在 CONTRIBUTING |
| 测试按项目类型可伸缩 | 不同项目类型需要不同测试层，不强制固定四层 |
| 每种文档有独立的状态集合和流转规则 | 不同类型文档的生命周期语义不同，不能共用同一套状态 |
| 无全局 Index.md | 各目录 README.md 自治，渐进式披露，Agent 按需读取不浪费 token |
| Plan 不移动归档 | README 状态字段区分，原地保留，方便追溯 |
| 模板在示例文件中 | 上层只引用，不展开细节 |
| 统一 YAML frontmatter | 元信息结构化，Agent 可解析无需读全文 |
| 标准文件/README 无 frontmatter | 标准文件和索引文件有固定格式，无需 frontmatter 元信息 |
| 不设计 tag/related 字段 | 关联关系通过文档正文中的相对路径链接表达，不依赖 frontmatter 元数据字段 |
| 相对路径链接 | 所有跨文档引用使用 `[text](path.md)`，可点击、可追溯 |
| 元设计与交付物分离 | agent-coding-spec.md 不在 template/ 内，使用者只拿 template/ |
| 调度层与文档层分离 | 任务板/状态机/调度逻辑属于外部基础设施，项目内 Agent 不可见 |
| 系统状态追踪在 docs/README.md | 单点追踪，Executor 启动时读取以自我约束 |
| Git 作为存储底座 | 所有状态流转以 Git 动作（commit/merge）为切分边界，迭代以原子合并为进度节点 |