> Agent 启动前必须完整读取。本文档是项目的**入口地图**，读完你应该知道：这是什么项目、文档在哪、系统规则、我能做什么、该按什么流程工作。

---

## 一、项目简介

<!-- 简要描述本项目：做什么、解决什么问题、技术栈 -->

---

## 二、文档体系

### 文档类型

| 文档 | 用途 | 谁维护 |
|------|------|--------|
| 本文档（AGENTS.md） | 项目入口地图 | Designer |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 编码/Commit/文档/测试规范 | Designer |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录（Keep a Changelog） | Executor 追加 Unreleased，Designer 整理发布 |
| [docs/arch/vision.md](docs/arch/vision.md) | 全局顶层愿景：业务目标、用户范围、顶层约束 | Designer |
| [docs/arch/design/](docs/arch/design/) | Design Spec：固化方案 + AC。唯一业务事实源 | Designer |
| [docs/arch/adr/](docs/arch/adr/) | 架构决策记录：技术选型、方案对比、取舍 | Designer |
| [docs/arch/plans/](docs/arch/plans/) | 单次执行容器：Plan + Report 成对 | Executor |
| [docs/arch/README.md](docs/arch/README.md) | 子目录索引 + **当前系统状态** | Designer（状态更新） |
| 各级 README.md | 该目录的索引和状态说明 | Designer |

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
| 设计者意图为根 | 顶层目标来自 Designer。Executor 不可创造新目标 |

---

## 五、角色与权限

本项目采用 Designer/Executor 角色模型。你是 **Executor**（执行者），负责执行任务。

### 你的角色

- 你作为 Executor，可以**读写 Plan/Report**，自主管理 Plan 的生命周期状态
- 你作为 Executor，可以**读取 Vision/Design/ADR**，基于它们编写 Plan 和代码
- 你可以基于 Design 和 ADR 自行生成子 Plan
- 你可以追加 [CHANGELOG.md](CHANGELOG.md) 的 `[Unreleased]` 段

### 绝对禁止

- **禁止修改 Vision / Design / ADR 的内容** — 这些是 Designer（设计者）的决策域
- **禁止修改 Vision / Design / ADR 的 status 字段** — 状态变更权属于 Designer
- **禁止将文档修改与代码修改混入同一 Commit**
- 禁止删除 [docs/arch/vision.md](docs/arch/vision.md)、[docs/arch/design/](docs/arch/design/) 下的 active Spec
- 禁止在 Plan 内定义长期架构事实（接口/数据表/业务规则）

### 发现权威文档需修改时

- 不自行修改内容或状态，在 Report 的「对权威文档的改动建议」中记录，由 Designer 决策

---

## 六、执行流程

```
0. 读取 docs/arch/README.md → 确认当前系统状态，明确当前阶段能做什么/不能做什么
1. 读取本文档 → 了解项目全局
2. 读取 docs/arch/vision.md → 确认顶层约束
3. 读取 docs/arch/design/README.md → 确认当前生效 Design Spec
4. 读取 active Design Spec → 获取完整规格 + AC
5. 读取 docs/arch/adr/README.md → 了解相关技术决策
6. 读取 docs/arch/plans/README.md → 检查未完成 Plan（断点续跑）
7. 创建/恢复 Plan 文件夹（结构见模板）
8. 按 Plan 编码
9. 执行测试，校验 AC
10. 写入 Report，关联 commit
11. 更新状态
12. 更新 [CHANGELOG.md](CHANGELOG.md)（Unreleased 段）
```

> **重要：** 步骤 0 决定的「当前阶段行为边界」覆盖后续所有步骤。例如：若当前阶段为 `DESIGN`，则步骤 8 不可执行（禁止在 DESIGN 阶段编写代码）。

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