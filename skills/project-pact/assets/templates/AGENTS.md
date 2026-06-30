> Agent 启动前必须完整读取。本文档是项目的**入口地图**，读完你应该知道：这是什么项目、文档在哪、系统规则、我能做什么、该按什么流程工作。

---

## 一、项目简介

<!-- 简要描述本项目：做什么、解决什么问题、技术栈 -->

---

## 二、文档体系

### 文档类型

| 文档 | 用途 |
|------|------|
| 本文档（AGENTS.md） | 项目入口地图 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 编码/Commit/文档/测试规范 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录（Keep a Changelog） |
| [docs/arch/vision.md](docs/arch/vision.md) | 全局顶层愿景：业务目标、用户范围、顶层约束（有 frontmatter） |
| [docs/arch/design/](docs/arch/design/) | Design Spec：固化方案 + AC。唯一业务事实源 |
| [docs/arch/adr/](docs/arch/adr/) | 架构决策记录：技术选型、方案对比、取舍 |
| [docs/arch/plans/](docs/arch/plans/) | 单次执行容器：Plan + Report 成对 |
| [docs/arch/README.md](docs/arch/README.md) | 子目录索引 + **当前系统状态** |
| 各级 README.md | 该目录的索引和状态说明 |

### 目录结构

```
项目根目录
├── AGENTS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── docs/arch/
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

---

## 三、文档导航

| 要找什么 | 去哪里 |
|----------|--------|
| **当前系统状态 + 行为边界** | [docs/arch/README.md](docs/arch/README.md)（首先读取！） |
| 项目目标、架构约束、硬性规则 | [docs/arch/vision.md](docs/arch/vision.md) |
| 功能规格、接口、数据模型、AC 验收标准 | [docs/arch/design/](docs/arch/design/)（找 active 版本） |
| 技术选型理由、架构决策 | [docs/arch/adr/](docs/arch/adr/) |
| 当前任务进度 | [docs/arch/plans/README.md](docs/arch/plans/README.md) |
| Plan/Report 模板 | [docs/arch/plans/0001-template/](docs/arch/plans/0001-template/) |
| 编码规范、Git 规则、文档写作规范 | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 版本变更记录 | [CHANGELOG.md](CHANGELOG.md) |

---

## 四、系统边界

项目遵循 6 条不可违反的边界：

| 边界 | 约束 |
|------|------|
| 契约与执行分离 | 四类契约（业务/接口/质量/架构）冻结后，才能进入 DEVELOP 写代码 |
| 验证先于实现 | 测试基础设施先于编码完成。低层机器化，高层可由 Agent 判定 |
| 状态变更=原子承诺 | 每个 Plan 在独立 Git branch 中执行。状态流转不可跳跃或回跳 |
| 可追溯性 | AC 编号 → Plan 引用 → Commit → Report 记录。文档/代码 commit 分离 |
| 自描述入口 | 本文档 → docs/arch/README.md → 各级 README → 具体文档。Agent 零上下文启动即可理解项目 |
| 设计者意图为根 | 顶层目标来自 DESIGN 阶段。DEVELOP 阶段不可创造新目标 |

---

## 五、阶段行为边界

你的行为由当前阶段决定。打开 [docs/arch/README.md](docs/arch/README.md) 确认当前阶段后，对照下表：

### INIT

- **允许**: 创建目录结构、标准文件、初始化 Git/CI
- **禁止**: 编写 Vision/Design/ADR/Plan、编写代码

### DESIGN

- **允许**: 编写 Vision → Design Spec → ADR → API 契约 → 拆解 Plan
- **禁止**: 编写代码（src/）、执行 Plan
- **状态变更权**: 你可以推进状态（INIT→DESIGN→DEVELOP）

### DEVELOP

- **允许**: 创建 Plan、执行 Plan（编码/测试）、更新 Plan/Report 状态
- **禁止**: 修改 Vision/Design/ADR 的内容或 status、在没有 Plan 的情况下直接写代码
- **Plan 必须包含「执行边界」段**，明确指定执行者必须做和必须不做的事

### INTEGRATE

- **允许**: 执行全量测试、修复集成问题
- **禁止**: 新增功能代码、修改 Design/ADR
- 如果发现设计缺陷 → 退回 DESIGN

### PRE_RELEASE

- **允许**: 环境检查、版本号确认、回滚方案验证
- **禁止**: 修改代码和文档

### RELEASE

- **允许**: 版本归档、CHANGELOG 整理、迭代复盘
- **禁止**: 修改任何代码

---

## 六、执行流程

### 如果当前阶段是 INIT / DESIGN

```
0. 读取 docs/arch/README.md → 确认当前阶段
1. 读取本文档 → 了解文档体系、系统边界、阶段行为
2. 按阶段行为边界操作（见第五节）
3. 推进状态时: 更新 docs/arch/README.md，独立 commit
```

### 如果当前阶段是 DEVELOP

```
0. 读取 docs/arch/README.md → 确认当前阶段
1. 读取 docs/arch/plans/README.md → 找到你的 Plan 文件夹
2. 读取 Plan 文件 → 了解目标、分步计划、执行边界
3. 读取 active Design Spec → 获取完整规格 + AC
4. 读取 docs/arch/adr/README.md → 了解相关技术决策
5. 按 Plan 执行（编码/测试）
6. 写入 Report，关联 commit。在「变更摘要」段记录本次变更
7. 更新 Plan status
```

### 如果当前阶段是 INTEGRATE / PRE_RELEASE / RELEASE

```
0. 读取 docs/arch/README.md → 确认当前阶段
1. 按阶段行为边界操作（见第五节）
```

---

## 七、故障处理

### 编码自检失败

- 静态检查失败 → 自动修复
- 无法修复 → 记录阻塞点到 Plan，不继续下一步

### 任务中断恢复

- 读取 [docs/arch/plans/README.md](docs/arch/plans/README.md)，找到 `in_progress` 或 `blocked` 的 Plan
- 读取该 Plan 文件夹的 README.md，找到未完成的子任务
- 从断点继续

### 代码实现与 Design 冲突

- 暂停当前 Plan，在 Report 中记录冲突详情和改动建议
- 标记 Plan 状态为 `blocked`，等待 Designer 介入