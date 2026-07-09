---
title: Agent Coding System — 文档规范设计
description: 无人循环自主 Agent 编码系统的文档规范设计，定义文档体系的结构、规则和设计决策。
type: design
status: active
version: 2
created: 2026-06-26T00:00:00Z
---

> 本文档是规范本身的 Design Spec，描述文档体系的设计决策、约束和完整规则。
> 执行层实现见 [skills/devloop/](skills/devloop/)，模板见 `skills/devloop/assets/templates/`。

---

## 一、概述与目标

### 目标

设计一套**无人循环自主 Agent 编码系统**的文档规范，使 Agent 能够：

1. 从零接手项目时，通过文档完整了解上下文，无需人工持续 prompt
2. 在明确的权限边界内自主执行开发任务
3. 所有产出可追溯（计划→执行→报告→commit）
4. 意外中断后仅凭文件系统恢复状态，不依赖对话历史

### 适用范围

本文档定义的是**文档体系的结构和规则**。编码规范、Git 工作流等见 `skills/devloop/assets/templates/CONTRIBUTING.md`。

### 三层交付物

```
agent-coding-spec.md  ← 元设计（本文档）：描述"为什么这样设计"
skills/devloop/     ← 执行层（bootloader + 模板）：Agent 加载后知道如何操作系统
```

---

## 二、核心设计原则

### 2.1 渐进式披露

每层只描述**下一级**的内容，不越级展开细节。

```
skills/devloop/SKILL.md（bootloader：状态机 + 路由）
  └── AGENTS.md（项目入口地图：文档类型、目录结构）
        └── docs/README.md（当前状态）
              ├── vision.md（顶层愿景）
              ├── spec/（需求规格）
              ├── interface/（接口定义）
              ├── ac/（验收标准）
              ├── adr/（架构决策）
              └── plans/（执行容器）
```

模板格式只出现在模板文件自己所在的那一层，上层只做引用。

### 2.2 单一事实源

每类信息只有一个权威定义位置，其余文档只引用不复制。

| 信息类型 | 唯一定义位置 | 其余文档 |
|----------|-------------|----------|
| 业务目标、用户范围、长期愿景 | vision.md | 只引用，不复制 |
| 用户故事、模块划分、数据模型、非功能指标 | Spec | 只引用，不复制 |
| 接口定义（字段、错误码） | Interface | 只引用，不复制 |
| 验收标准（四场景） | AC | 只引用，不复制 |
| 技术选型、架构决策 | ADR | 只引用，不复制 |
| 编码规范、Git 规则 | CONTRIBUTING.md | 只引用，不复制 |
| 系统当前阶段 | docs/README.md | 只引用，不复制 |

### 2.3 阶段行为模型

Agent 无固定身份，行为由当前阶段决定。状态机中的每个阶段定义了该阶段允许和禁止的行为。Agent 读 `docs/README.md` 确认当前阶段后，对照 AGENTS.md 中的阶段行为边界表行动。

**阶段行为边界（概述）：**

| 阶段 | 允许 | 禁止 |
|------|------|------|
| INIT | 创建目录结构、标准文件、初始化 Git、填写 CONTRIBUTING.md | 编写 Vision/Spec/ADR/Plan、编写代码 |
| DESIGN | 编写 vision.md→Spec→AC→ADR→接口定义 | 编写代码、执行 Plan |
| TEST_INFRA | 搭建测试基建、创建执行容器、更新 CONTRIBUTING.md 测试段 | 编写业务测试用例、编写业务代码 |
| DEVELOP | 创建 Plan、执行 Plan（编码/测试）、更新 Plan/Report | 修改 Spec/ADR/AC 文档 |
| SYSTEM_TEST | 执行全量测试、修复集成问题 | 新增功能代码、修改 Spec/ADR |
| RELEASE | 部署到 staging/production、打 tag、整理 CHANGELOG、归档 | 修改任何代码 |

**状态变更由协调者执行。** 协调者可以是任何 Agent——它加载 skill，理解状态机，推进状态流转。协调者不固定身份，根据当前阶段切换行为模式。

### 2.4 Git 作为存储底座

Git 是整个项目（代码 + 文档）的**存储和版本控制器**。系统中所有状态流转和迭代都以 Git 动作作为切分边界：

- **一次迭代** = 隔离环境内完整执行任务 → 通过全部校验 → 原子合并入主分支。合并动作是项目进度的唯一有效变更点。
- **文档变更**必须独立 Commit，不与代码混合。
- **状态流转**伴随对应的 Git commit，commit 是状态变更的物理锚点。
- **容错**：任务异常中断 → 丢弃隔离环境，主分支零污染。误操作通过 Git 历史回退。

---

## 三、系统边界

以下 6 条边界是系统不可违反的硬性约束。每条边界内部有 Level 1 子边界（机制约束，不可违反）和 Level 2 实现模式（可变，按项目类型自适应）。

### 边界 1：契约与执行分离

在编写任何代码之前，契约必须冻结。这是并行化的唯一前提。

**Level 1 — 最小 DESIGN 文档集：**

| 文档类型 | 必须回答的问题 | 冻结时机 |
|----------|--------------|----------|
| vision.md | 做什么、为谁做 | DESIGN 阶段最早定稿 |
| Spec | 用户故事、模块划分、数据模型、非功能指标 | vision.md 后 |
| AC | 什么算成功、什么算失败（四场景） | 与 Spec 同步 |
| ADR | 技术选型、约束、取舍 | Spec 后 |
| Interface | 模块间如何通信、数据长什么样 | ADR 验证后 |
| 测试基建 ADR | 测试框架、Mock、CI 平台 | TEST_INFRA 阶段 |

**Level 1 — 冻结的硬性定义：**

- 冻结 = 对应文档的 `status` 字段从 `draft` 变为 `proposed`（设计师写完了），出口把关审查通过后 promote 为 `active`（或 `accepted`），伴随独立 Git commit
- 冻结后不可原地修改。要改必须走正式回退：退回 DESIGN → 修改后重新 promote 为 active。typo 修复、措辞澄清等非破坏性修改除外。Git 记录变更历史

**Level 2 — 实现模式：**

- 小项目（CLI 工具）：业务契约 + 质量契约合并为一个文件
- 中项目（后端 API）：Spec + ADR + Interface 分离
- 大项目（全栈）：四种契约各自独立文件 + API 契约文档

### 边界 2：验证先于实现

验证标准（AC、测试用例）必须在实现之前或独立于实现存在。

**Level 1 — 验证分层智能化：**

```
低层（近代码）→ 机器化
  单元测试、接口契约校验、类型检查

高层（近意图）→ 智能化（Agent）
  E2E 语义验证、AC 中模糊标准的判定
```

**Level 1 — 最小验证系统：**

- AC 应尽可能可量化，但**不强制机器可验证**
- 机器能验证的尽量机器化；机器做不到的由 Agent 在 Report 中给出判定结论
- 测试系统可以是"机器 + Agent"的组合

**Level 1 — 验证与编码的时序：**

编码开始时，测试基础设施必须已就位。

**Level 1 — 验证层级按项目类型自底向上叠加：**

```
单元测试（必选，所有项目）
  → 开发集成自测（必选，所有项目）
    → 契约测试（前后端/服务间）
      → 服务集成测试（所有项目，SYSTEM_TEST 阶段）
        → E2E 测试（有 UI 的项目）
          → 视觉回归（前端项目）
```

每层都是合并闸门，不可跳过。DEVELOP 执行前三层，SYSTEM_TEST 执行后三层。

**Level 2 — 实现模式：**

- 机器化测试：Jest/Vitest/Playwright 等框架
- Agent 化测试：独立的测试 Agent，读取 AC 和代码产物，执行语义判断

### 边界 3：状态变更 = 原子承诺

状态从 DESIGN 变为 DEVELOP 是一个承诺——"契约已冻结，现在开始基于此契约构建"。

**Level 1 — 分支模型（Gitflow）：**

- `main` 仅含 release 节点，始终可部署。`develop` 为持续集成分支，所有 Plan 分支合并到 `develop`。
- 分支类型与 commit type 一致：`feat/` `fix/` `ci/` `test/` `refactor/` `perf/` `build/` `chore/` `docs/`。系统特有类型 `spike/`（ADR 验证，保留不合并）。
- 一个执行容器 = 一个分支，从 `develop` 拉出，编号与执行容器对应。命名：`<type>/<编号>-<描述>`。
- `release/*` 和 `hotfix/*` 同时合并到 `main` 和 `develop`。
- 分支生命周期：创建 → 推送 → MR 门禁通过 → 合并到 `develop` → 删除。`release/*`/`hotfix/*` 额外合并到 `main`。
- 多个 Plan 并行执行时，必须使用 `git worktree`，保证隔离且共享同一个 repo。

**Level 1 — 变更锚点：**

| 锚点 | 含义 |
|------|------|
| commit | 状态变更的物理锚点 |
| merge | 迭代进度的原子单位 |
| 具体操作 | commit/merge/rebase/squash 由项目 Git 规范灵活决定 |

**Level 1 — 异常处理：**

| 异常 | 处理 |
|------|------|
| Agent 崩溃 | 丢弃 branch/worktree，任务重置为 pending |
| 步骤失败 | branch 内回退至步骤快照，内部重试 |
| 架构不可行（架构颠覆） | 停止 DEVELOP，退回 DESIGN |
| 基建缺陷 | SYSTEM_TEST 发现 → 退回 TEST_INFRA |
| 设计缺陷 | SYSTEM_TEST 发现 → 退回 DESIGN |
| 局部 bug | SYSTEM_TEST 内部修复循环 |

**Level 2 — 实现模式：**

- 串行项目：每个 Plan 一个 branch，顺序执行
- 并行项目：多个 Plan 在独立 worktree 中并行执行（Level 1 要求）

### 边界 4：可追溯性

每一次变更都必须能追溯到：谁决定的（ADR/Design）→ 谁计划的（Plan）→ 谁执行的（Report）→ 哪次 commit。

**Level 1 — 语义链（底线）：**

追溯通过文档正文中的文本引用、命名约定、commit message 关联自然形成，不依赖 frontmatter 的 `related_*` 字段：

```
AC 文档 AC-003
  → Plan 01-plan-order-api.md 步骤 2: "实现 AC-003 订单创建"
    → Commit: "feat(order): 实现 AC-003 订单创建"
      → Report 01-report-order-api.md: "AC-003 ✅, commit abc123"
```

**Level 1 — 文档变更与代码变更分离：**

一次 commit 要么是文档，要么是代码，不混合。

**Level 2 — Key 化（优化）：**

frontmatter 字段、结构化元数据。按需使用。断链 = 警告，不阻塞合并。

**Level 2 — 准入判断（灵活）：**

- 程序化：简单场景，检查 `status` 字段
- Agent 化：复杂场景，语义理解、上下文判断

### 边界 5：自描述入口

任何 Agent（无论有无上下文）进入系统后，仅凭文件系统就能理解：当前处于什么阶段、能做什么不能做什么、去哪里找下一步需要的信息。

**Level 1 — 入口路径：**

```
AGENTS.md → docs/README.md（当前状态）→ 各级 README（索引）→ 具体文档
```

**Level 1 — 当前状态单点可见：**

系统当前阶段 + 设计评估在 `docs/README.md` 中追踪。

**Level 1 — 零上下文启动：**

系统不依赖外部记忆或对话历史。Agent 仅凭文件系统即可理解项目全貌。

### 边界 6：设计者意图为根

系统没有自主目标。所有顶层目标的唯一来源是设计意图。

**Level 1 — 目标来源：**

所有顶层目标来自 DESIGN 阶段的设计意图。DEVELOP 阶段不可创造新的顶层目标。

**Level 1 — 决策权归属：**

架构变更、版本发布、需求调整由 DESIGN 阶段决策。

**Level 1 — 角色边界固定：**

此边界保护的是**职责分离**——设计意图不被执行过程僭越——而非特定身份。

---

## 四、系统生命周期状态机

系统状态机是整个开发流程的核心控制骨架。它定义了项目从初始化到发布完成的完整生命周期。

### 4.1 设计原则

- **外层串行，内层并行。** 状态机本身是串行骨架（关口），并行发生在状态内部。
- **契约是并行化的唯一前提。** 一旦 DESIGN 出口把关通过（Spec + ADR + 接口定义 + AC 全部冻结），TEST_INFRA 和 DEVELOP 内可并行。
- **唯一串行关口：SYSTEM_TEST。** 必须等所有 Plan done 才能进入。

### 4.2 三层模型

每个固定阶段内部有三层结构：

| 层次 | 含义 | 可变性 |
|------|------|--------|
| 固定阶段 | 状态机保证，所有项目必经 | 不可变 |
| 子阶段 | 按项目类型选择组合，每个标注必选/适用 | 可选组合 |
| 参考实现 | 示例，展示一种可行的覆盖方式 | 完全可变 |

### 4.3 状态总览

```
INIT → DESIGN → TEST_INFRA → DEVELOP → SYSTEM_TEST → RELEASE
        ↑         ↑        ↑            ↑
        │         │        │            │
        └─────────┴────────┴────────────┘
        (架构颠覆 / 基建缺陷 / 设计缺陷 回退)

RELEASE → DESIGN  (新一轮迭代 / 热修复)
```

6 个阶段，3 条回退路径，1 条热修复通道。

### 4.4 各状态定义

#### INIT — 项目初始化

| 维度 | 定义 |
|------|------|
| **含义** | 项目骨架搭建。将项目接入 devloop 系统。新项目安装模板，旧项目扫描合并 |
| **允许** | 创建目录结构、AGENTS.md/CONTRIBUTING.md/CHANGELOG.md、初始化 Git、填写 CONTRIBUTING.md 项目信息 |
| **禁止** | 编写 Vision/Spec/ADR/Plan、编写业务代码 |
| **准入条件** | —（项目启动的起点） |
| **→ DESIGN 条件** | 目录结构就位、标准文件已创建、Git 仓库已初始化、`main` + `develop` 分支已创建 |

#### DESIGN — 规划设计

| 维度 | 定义 |
|------|------|
| **含义** | 需求分析、架构设计、验收标准定义。主体串行（因果链），后期可有限并行 |
| **允许** | 编写 vision.md → Spec → AC 文档 → ADR → 验证 → 接口定义 |
| **禁止** | 编写业务代码 |
| **准入条件** | INIT 完成 |
| **→ TEST_INFRA 条件** | 全部文档 status=proposed，出口把关内容级审查通过，promote proposed→active/accepted |
| **回退** | vision.md 不可退回。其他文档发现设计缺陷 → 退回 DESIGN 自身 |

**DESIGN 子阶段：**

| 子阶段 | 适用 | 产出 | 退出条件 |
|--------|------|------|----------|
| vision.md | 必选 | 业务目标、用户范围、长期理想形态 | status=proposed |
| Spec | 必选 | 用户故事、模块划分、数据模型、非功能指标 | status=proposed |
| AC 文档 | 必选 | 四场景验收标准（正常/边界/异常/失败） | status=proposed |
| ADR | 必选 | 核心 ADR（技术栈/存储/架构模式） | status=proposed |
| 验证 | 必选 | ADR 验证段填写（含复现步骤 + 验证 branch） | 结论为「可行」，验证 branch 已记录 |
| 接口定义 | 适用 | 接口入参/出参/错误码 | status=proposed |

**出口把关：** 逐项审查，非全部退回。失败定位到具体文档，修复后重新检查该项。审查通过后 promote：proposed→active（ADR 为 accepted）。

**DESIGN 内部因果链：**

```
vision.md → Spec → AC 文档 + ADR 并行
                      ADR → 验证 → 接口定义
                      AC ──────────────→ 出口把关
                      接口定义 ─────────→ 出口把关
```

#### TEST_INFRA — 一次性基建

| 维度 | 定义 |
|------|------|
| **含义** | 设计并搭建测试基建——CI、测试框架、Mock、覆盖率、门禁、部署底座。为 DEVELOP 提供可验证的环境 |
| **允许** | 编写测试基建 ADR、创建执行容器、搭建基建、更新 CONTRIBUTING.md 测试段 |
| **禁止** | 编写业务测试用例、编写业务代码 |
| **准入条件** | DESIGN 完成（契约冻结） |
| **→ DEVELOP 条件** | 全部基建分支已合并到 `develop`、CI 可运行（自动化）、MR 门禁正确拦截（Agent 自证）、Mock 返回正确（Agent 自证）、覆盖率数据准确（Agent 自证）、E2E 框架可跑冒烟 `[适用]`、CONTRIBUTING.md 测试段已填写 |

**TEST_INFRA 子阶段：**

| 子阶段 | 适用 | 产出 | 退出条件 |
|--------|------|------|----------|
| 测试基建 ADR | 必选 | 框架选型、Mock 方案、CI 平台、部署策略等 | status=proposed |
| 一次性基建搭建 | 必选 | CI/测试框架/Mock/覆盖率/门禁/部署底座 | 自证通过 |

**设计理由：** 测试开发与业务开发分离。TEST_INFRA 阶段搭建武器工厂，DEVELOP 阶段制造武器。测试基建自证能正确判断对错（不仅能启动），而非在业务开发中边用边修。

#### DEVELOP — 编码开发（最高并行期）

| 维度 | 定义 |
|------|------|
| **含义** | 基于 TEST_INFRA 搭建的一次性基建，按 Spec 模块划分创建执行容器，TDD 左移开发 |
| **允许** | 创建 Plan、执行 Plan（编码/测试）、更新 Plan/Report |
| **禁止** | 修改 Spec/ADR/AC 文档、修改全局契约 |
| **准入条件** | TEST_INFRA 完成（一次性基建就绪） |
| **→ SYSTEM_TEST 条件** | 全部 feature 分支已合并到 `develop`、MR 门禁 + 提测门禁通过（自动化）、Report 中 AC 验收结果经 Agent 确认合理 |

**DEVELOP 子阶段：**

| 子阶段 | 适用 | 产出 |
|--------|------|------|
| 创建 Plan | 必选 | Spec 模块划分表 → 执行容器 |
| 编码 | 必选 | TDD 左移（单元测试 + 开发集成自测 + 契约测试 `[适用]`） |
| 打包部署 | 必选 | 部署配置 + 部署到测试环境 |
| 提测门禁 | 必选 | Report/AC/覆盖率检查 |

**Plan 与 Report 职责分离：**

| Plan（静态，创建后不改） | Report（动态，执行中持续更新） |
|--------------------------|------------------------------|
| Context（背景信息） | 执行摘要、关联 Commit |
| Request（要做什么） | 产物清单、测试摘要、验收结果 |
| Output Format（怎么交付） | 遗留问题 |
| Constraints（不能越界的） | |
| Checkpoint（终止条件） | |
| Steps（大致拆解） | |

**Constraints：** Plan 必须包含「Constraints」段，明确指定执行者不能假设的、不能越界的。执行者可能不加载 skill，仅凭 Plan 和系统文档工作，因此 Constraints 是执行者与协调者之间的契约。

**架构级依赖：** 独立服务/前后端可并行，共享库/基础包先做。代码级依赖 Agent 内部处理。

#### SYSTEM_TEST — 系统测试（在 develop 上验证）

| 维度 | 定义 |
|------|------|
| **含义** | 在 `develop` 分支上执行系统级验证——集成测试、系统测试、专项测试。单元测试和开发集成自测已在 DEVELOP 完成 |
| **允许** | 执行全量测试、在 `fix/*` 分支修复 bug 后合并回 `develop`、生成测试报告 |
| **禁止** | 新增功能代码、修改 Spec/ADR |
| **准入条件** | 全部 feature Plan 分支已合并到 `develop` |
| **→ RELEASE 条件** | `develop` 全部测试层通过，无阻塞级缺陷 |
| **回退** | 基建缺陷 → TEST_INFRA，设计缺陷 → DESIGN |

**SYSTEM_TEST 子阶段：**

| 子阶段 | 适用 | 产出 |
|--------|------|------|
| 集成测试 | 必选 | 服务集成/契约/编排 |
| 系统测试 | 必选 | E2E/视觉回归 |
| 专项测试 | 适用 | 性能/安全/兼容性 |

**修复循环：** 修复在 SYSTEM_TEST 内部完成。局部 bug 内部修复；基建缺陷 → TEST_INFRA；设计缺陷 → DESIGN。

#### RELEASE — 迭代闭环

| 维度 | 定义 |
|------|------|
| **含义** | 从 `develop` 拉出 `release/*` 分支，staging 验证 → production 发布 → 合并到 `main` + `develop` |
| **允许** | CD 部署、冒烟测试、打 tag、整理 CHANGELOG、归档 |
| **禁止** | 修改任何代码 |
| **准入条件** | SYSTEM_TEST 全部测试通过 |
| **→ DESIGN 条件** | `release/*` 已合并到 `main` + `develop`，tag 已打 |

**RELEASE 子阶段：** staging 验证（部署 + 冒烟 + 环境检查）→ production 发布（发布策略确认 + 监控 + 回滚方案 + 打 tag + 归档于 `main`）。

**staging 失败分类：** CD/环境失败 → 在 `release/*` 内修复；业务 bug → 在 `develop` 修复后重新拉 `release/*`。

**热修复：** 从 `main` 拉 `hotfix/*`，合并到 `main` + `develop`（RELEASE → DESIGN 轻量 → TEST_INFRA 增量 → DEVELOP 最小修复 → SYSTEM_TEST 回归 → RELEASE 补丁 tag）。

### 4.5 流转刚性规则

| 规则 | 说明 |
|------|------|
| 禁止跳跃 | 不允许跨状态流转（如 INIT → DEVELOP） |
| 架构颠覆 | DEVELOP → DESIGN |
| 基建缺陷 | SYSTEM_TEST → TEST_INFRA |
| 设计缺陷 | SYSTEM_TEST → DESIGN |
| 热修复 | RELEASE → DESIGN（轻量，跳过 full Spec/AC） |
| 新一轮迭代 | RELEASE → DESIGN（增量模式） |
| 准入灵活 | 准入判断可以是程序（检查 status 字段）也可以是 Agent（语义理解） |

### 4.6 双层可见性

| 层面 | 使用者 | 用途 |
|------|--------|------|
| **外部调度层** | 协调 Agent（加载 skill） | 读取状态机，执行状态流转、准入检查、Plan 分配、异常上浮 |
| **项目文档层** | 执行 Agent（不加载 skill） | 读取 `docs/README.md` 确认当前阶段，AGENTS.md 确认行为边界，Plan 文件确认执行任务 |

**当前状态追踪：** 系统当前阶段、设计评估记录在 `docs/README.md` 中。状态变更时更新。Agent 中断恢复时通过 `git log --oneline --grep="docs(state):\|docs(plan):"` 重建上下文。

---

## 五、文档体系

### 5.1 Vision（docs/vision.md）

| 维度 | 定义 |
|------|------|
| **定位** | 全局唯一顶层愿景：业务目标、用户范围、长期理想形态 |
| **创建时机** | DESIGN 阶段 |
| **变更规则** | 一次性定稿，不可退回。仅重大业务转型才修订。旧版本由 Git 历史追溯，不原地保留 |

| **生命周期** | draft → proposed → active |

**设计理由：** vision.md 只回答"为什么要做这个项目"。架构约束、非功能指标、硬性规则分别属于 ADR、Spec。不混入 vision。

### 5.2 Spec（docs/spec/000x-xxxx.md）

| 维度 | 定义 |
|------|------|
| **定位** | 需求规格：用户故事、模块划分、数据模型、非功能指标。所有业务需求的唯一事实源 |
| **创建时机** | DESIGN 阶段 |
| **变更规则** | 冻结后不可原地修改。增量迭代追加内容，设计变更（架构颠覆）退回 DESIGN 修改。typo 修复、措辞澄清等非破坏性修改除外。Git 记录变更历史，不原地保留旧版本 |

| **生命周期** | draft → proposed → active。同时只有一个 active |

### 5.3 Interface（docs/interface/000x-xxxx.md）

| 维度 | 定义 |
|------|------|
| **定位** | 接口定义：入参/出参/错误码。业务字段来自 Spec，传输格式由 ADR 决定 |
| **创建时机** | DESIGN 阶段，ADR 验证后 |
| **变更规则** | 同 Spec |
| **生命周期** | draft → proposed → active |

**设计理由：** 接口定义独立于 Spec。Spec 定义模块和业务规则，Interface 定义模块间通信契约。分离后接口变更不影响 Spec，且前后端可基于 Interface 并行开发。

### 5.4 AC（docs/ac/000x-xxxx.md）

| 维度 | 定义 |
|------|------|
| **定位** | 验收标准：测试的唯一权威依据。每条 AC 必须覆盖四场景（正常/边界/异常/失败） |
| **创建时机** | DESIGN 阶段 |
| **变更规则** | 同 Spec |
| **生命周期** | draft → proposed → active |

**设计理由：** AC 独立于 Spec。AC 是 Spec、开发、测试三方共享的契约。只写正常流程的 AC 属于无效 AC。四场景全覆盖确保测试不遗漏。

### 5.5 ADR（docs/adr/000x-xxxx.md）

| 维度 | 定义 |
|------|------|
| **定位** | 架构决策记录：技术选型、方案折中、风险取舍。覆盖业务架构 + 测试基建架构 |
| **创建时机** | DESIGN 阶段（业务 ADR）+ TEST_INFRA 阶段（测试基建 ADR） |
| **变更规则** | 持续新增，不删除。修订时旧 ADR 标记 superseded + 新建 ADR。验证 branch 保留不合并，供后续阶段参考 |
| **生命周期** | draft → proposed → accepted → superseded/deprecated |

### 5.6 Plan + Report（docs/plans/000x-任务名/）

| 维度 | 定义 |
|------|------|
| **定位** | 执行容器。任何需要执行的任务都通过创建执行容器来组织。一个执行容器对应一个 Git 分支，内含多个最小执行单元（Plan + Report 成对） |
| **创建时机** | 各阶段自行创建（TEST_INFRA 创建基建 Plan，DEVELOP 创建业务 Plan） |
| **变更规则** | Plan 创建后不改；Report 执行中持续更新，完成后标记 complete |
| **生命周期** | pending → done。执行失败也标记 done，另写新 Plan 继续。原地保留不删除 |

**内部结构：**

```
000x-任务名/
├── README.md              # 最小执行单元状态表 + 依赖 + AC 覆盖 + commit 映射
├── 01-plan-xxx.md         # Plan 文件（静态）
├── 01-report-xxx.md       # Report 文件（动态，一一对应）
```

**Plan 段（静态）：** Context（背景信息）、Request（要做什么）、Output Format（怎么交付）、Constraints（不能越界的）、Checkpoint（终止条件）、Steps（大致拆解）。

**Report 段（动态）：** 执行摘要、关联 Commit、产物清单、测试摘要、验收结果、遗留问题。

**Plan/Report 成对规则：** 一一对应。一个 Plan 可对应多个 commit。

**Constraints：** Plan 必须包含「Constraints」段，明确指定执行者不能假设的、不能越界的。执行者可能不加载 skill，仅凭 Plan 和系统文档工作。

### 5.7 CHANGELOG.md（项目根目录）

| 维度 | 定义 |
|------|------|
| **定位** | 项目版本变更记录，遵循 [Keep a Changelog](https://keepachangelog.com/) |
| **创建时机** | INIT 阶段创建 |
| **变更规则** | RELEASE 阶段整理为正式版本条目 |
| **生命周期** | 持续更新，不删除 |

### 5.8 README.md（目录索引 + 系统状态）

| 目录 | README 内容 |
|------|------------|
| `docs/` | 子目录列表、**当前阶段** |
| `docs/spec/` | Spec 版本列表（文件、状态） |
| `docs/interface/` | 接口定义列表 |
| `docs/ac/` | AC 文档列表 |
| `docs/adr/` | 决策列表（编号、标题、状态） |
| `docs/plans/` | 任务列表（编号、标题、状态、创建时间） |
| 执行容器内 | 最小执行单元状态表（编号、Plan、Report、覆盖 AC、状态、Commits） |

**docs/README.md 关键字段：**

- **当前阶段**：INIT/DESIGN/TEST_INFRA/DEVELOP/SYSTEM_TEST/RELEASE

---

## 六、文档状态定义

每种文档类型有各自独立的状态集合和流转规则。

### 6.1 Vision

```
draft ──→ proposed ──→ active
```

| 状态 | 含义 |
|------|------|
| `draft` | 编写中 |
| `proposed` | 编写完成，待出口把关审查 |
| `active` | 审查通过，当前生效 |

**设计理由：** proposed 是"设计师写完"和"系统采纳"之间的中间态。设计师标记 proposed 表示"我写完了"，出口把关审查通过后 promote 为 active。这防止未审查的内容直接生效。旧版本由 Git 历史追溯，不原地保留。

### 6.2 Spec / Interface / AC

```
draft ──→ proposed ──→ active
```

| 状态 | 含义 |
|------|------|
| `draft` | 编写中，尚未冻结 |
| `proposed` | 编写完成，待出口把关审查 |
| `active` | 审查通过，当前唯一生效版本 |

- 同时只有一个 active。冻结后不可原地修改。typo 修复、措辞澄清等非破坏性修改除外。旧版本由 Git 历史追溯，不原地保留。

### 6.3 ADR

```
draft ──→ proposed ──→ accepted ──→ superseded
  │                      │
  └──────────────────────┴──→ deprecated
```

| 状态 | 含义 |
|------|------|
| `draft` | 提案中，尚未采纳 |
| `proposed` | 编写完成，待出口把关审查 |
| `accepted` | 审查通过，当前生效 |
| `superseded` | 被新 ADR 替代 |
| `deprecated` | 已废弃 |

### 6.4 Plan

```
pending ──→ done
```

| 状态 | 含义 |
|------|------|
| `pending` | 未执行 |
| `done` | 已执行（无论成功/失败）。失败时另写新 Plan 继续 |

### 6.5 Report

```
draft ──→ complete
```

| 状态 | 含义 |
|------|------|
| `draft` | 编写中，伴随 Plan 执行同步更新 |
| `complete` | 已提交 |

### 6.6 README.md / CHANGELOG.md

无 frontmatter 状态字段。

---

## 七、文档格式约定

### 7.1 Frontmatter

以下文档类型使用 YAML frontmatter：

| 文档类型 | 必填字段 |
|----------|----------|
| Vision | `title`, `description`, `type: vision`, `status`, `created` |
| Spec | `title`, `description`, `type: spec`, `status`, `version`, `created` |
| Interface | `title`, `description`, `type: interface`, `status`, `created` |
| AC | `title`, `description`, `type: ac`, `status`, `created` |
| ADR | `title`, `description`, `type: adr`, `status`, `created` |
| Plan | `title`, `description`, `type: plan`, `status`, `created` |
| Report | `title`, `description`, `type: report`, `status`, `created` |

以下文件**不使用** frontmatter：
- AGENTS.md、CONTRIBUTING.md、CHANGELOG.md（标准文件）
- 所有 README.md（目录索引）

字段说明：
- `title`：文档标题
- `description`：一句话摘要
- `type`：`vision` | `spec` | `interface` | `ac` | `adr` | `plan` | `report`
- `status`：见 [六、文档状态定义](#六文档状态定义)
- `created`：ISO 8601 格式
- `version`：仅 Spec，整数递增

### 7.2 路径引用

所有跨文档引用使用相对路径 Markdown 链接。禁止使用反引号包裹的纯文本路径。

### 7.3 命名规范

| 文档 | 命名 | 示例 |
|------|------|------|
| Vision | `vision.md` | `vision.md` |
| Spec | `000x-xxxx.md` | `0001-vagent.md` |
| Interface | `000x-xxxx.md` | `0001-order-api.md` |
| AC | `000x-xxxx.md` | `0001-order-ac.md` |
| ADR | `000x-xxxx.md` | `0001-db-choice.md` |
| 执行容器 | `000x-简短描述` | `0001-订单模块` |
| Plan 文件 | `0x-plan-xxx.md` | `01-plan-order-api.md` |
| Report | `0x-report-xxx.md` | `01-report-order-api.md` |

---

## 八、目录结构

```
项目根目录
├── CHANGELOG.md
├── CONTRIBUTING.md
├── AGENTS.md
├── docs/
│   ├── README.md          # 索引 + 当前阶段
│   ├── vision.md
│   ├── spec/
│   │   ├── README.md
│   │   └── 0001-template.md
│   ├── interface/
│   │   ├── README.md
│   │   └── 0001-template.md
│   ├── ac/
│   │   ├── README.md
│   │   └── 0001-xxx.md
│   ├── adr/
│   │   ├── README.md
│   │   └── 0001-xxx.md
│   └── plans/
│       ├── README.md
│       └── 0001-任务名/
│           ├── README.md
│           ├── 01-plan-xxx.md
│           └── 01-report-xxx.md
├── src/
```

---

## 九、联动规则

当修改权威文档时，需遵循以下规则：

### 修改 Spec

1. 更新 `docs/spec/README.md` 中的版本状态
2. 检查 `docs/adr/README.md` 中所有引用该 Spec 的 ADR，更新状态
3. 若 AC 变更，同步更新 AC 文档
4. 独立 Commit

### 新增/修改 ADR

1. 更新 `docs/adr/README.md`
2. 若替代旧 ADR，旧 ADR 状态改为 `superseded`，新 ADR 正文中引用旧 ADR 路径

---

## 十、测试体系（可伸缩）

### 10.1 核心原则

- 测试基础设施（CI/Mock/E2E/覆盖率/门禁）由 TEST_INFRA 阶段一次性搭建，自证正确性
- 业务测试用例由 DEVELOP 阶段各 Plan 自行编写
- 低层机器化（单元/集成/契约），高层智能化（Agent 语义判定）
- 测试作为合并闸门：全部测试通过方可提交合并

### 10.2 测试层级

| 测试层 | 适用条件 | 执行阶段 |
|--------|---------|---------|
| 单元测试 | 所有项目 | DEVELOP |
| 开发集成自测 | 所有项目 | DEVELOP |
| 契约测试 | 前后端/服务间 | DEVELOP |
| 服务集成测试 | 所有项目 | SYSTEM_TEST |
| E2E 测试 | 有 UI 的项目 | SYSTEM_TEST |
| 视觉回归 | 前端项目 | SYSTEM_TEST |
| 专项测试 | 有性能/安全要求的项目 | SYSTEM_TEST |

### 10.3 在文档体系中的分布

| 内容 | 位置 |
|------|------|
| 验收标准 | AC 文档 |
| 测试基建 ADR | docs/adr/（TEST_INFRA 阶段创建） |
| 测试命令 | CONTRIBUTING.md（TEST_INFRA 阶段填写） |
| 测试目录 | CONTRIBUTING.md（TEST_INFRA 阶段填写） |

---

## 十一、架构分层

### 11.1 Skills 层（bootloader）

`skills/devloop/` 是执行层入口。Agent 加载 skill 后获得：
- 状态机全貌和路由
- 系统安装指令
- 按阶段的操作流程（references/）

Skill 不包含项目规则（文档类型、命名规范、frontmatter 等）——这些在系统文档中。

### 11.2 项目文档层（模板交付物）

安装到项目中的文档。包含 AGENTS.md、CONTRIBUTING.md、CHANGELOG.md 和 docs/ 子目录。模板位于 `skills/devloop/assets/templates/`。项目内 Agent 读取此层即可工作，无需加载 skill。

### 11.3 调度/协调层（外部基础设施）

由更高层级的调度 Agent 执行。职责：读取状态机，执行状态流转、准入检查、任务分配、隔离环境创建与回收、异常上浮。项目内 Agent 不可见此层。

### 11.4 三层交互

```
调度/协调层（外部）
  │ 加载 skill → 获取状态机定义
  │ 读取 docs/README.md → 获取当前状态
  │ 执行准入检查 → 推进状态 → 更新 docs/README.md
  │ 创建隔离环境，分配执行 Agent
  ▼
Skills 层（bootloader）
  │ 提供系统安装、导航、路由
  │ 按阶段提供操作流程
  ▼
项目文档层
  │ Agent 读取 AGENTS.md → 阶段行为边界
  │ Agent 读取 docs/README.md → 当前阶段
  │ Agent 读取 Plan → Constraints/Checkpoint → 执行
  │ 产出通过 Git commit 反馈
```

---

## 十二、关键设计决策

| 决策 | 理由 |
|------|------|
| 6 条系统边界为不可违反的硬性约束 | Level 1 约束机制，Level 2 允许自适应 |
| 契约与执行分离 | 并行化的唯一前提。冻结后不可原地修改（typo 修复、措辞澄清除外） |
| 验证先于实现 | 低层机器化，高层智能化。测试基建在编码前就位 |
| 状态变更 = 原子承诺 | branch 为最小执行边界 |
| 语义链为底线 | 准入判断灵活：程序或 Agent 均可 |
| 设计者意图为根 | 保护职责分离，非特定身份 |
| 6 阶段状态机 | INIT→DESIGN→TEST_INFRA→DEVELOP→SYSTEM_TEST→RELEASE。以 Gitflow 为分支容器，把关分两层：自动化（CI/门禁/部署）+ Agent 判断（文档语义/自证/失败分类/发布决策） |
| 固定阶段 → 子阶段 → 参考实现三层模型 | 固定约束 + 可选组合 + 自由实现 |
| proposed 状态 | 设计师写完→待审查→审查通过才冻结。防止未审查内容直接生效 |
| 出口把关 = 内容级检查 | 非形式检查，逐项审查。失败定位到具体文档 |
| 一次性基建（TEST_INFRA） | 测试基建独立搭建，自证正确性，DEVELOP 直接使用 |
| 系统测试（SYSTEM_TEST） | 集成+系统+专项统一阶段，PRE_RELEASE 作为 RELEASE 内部步骤 |
| 执行容器 | 各阶段创建自己的执行容器，不替下游创建 |
| 通用优先 | 不绑定项目类型、技术栈。E2E/契约标注 `[适用]`，示例标记清楚 |
| 阶段行为模型取代角色模型 | Agent 无固定身份，行为由当前阶段决定 |
| Plan 静态 / Report 动态 | 计划创建后不改，执行信息在 Report 中持续更新 |
| Constraints | Plan 通过 Constraints + Checkpoint 明确执行约束 |
| Git 作为存储底座 | 状态流转以 commit 为切分边界。Agent 中断恢复时通过 git log 重建上下文 |
| 热修复通道 | 阻断性故障走快速通道，不完整走全量 DESIGN |
| 接口定义独立 | 接口变更不影响 Spec，前后端可基于接口定义并行开发 |
| AC 独立 | AC 是三方共享契约，独立于 Spec 确保测试权威性 |
| 占位符规范 | 模板使用 `<!-- -->` 注释占位，非硬编码示例 |
