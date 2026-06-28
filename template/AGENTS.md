
> Agent 启动前必须完整读取。本文档是项目的**入口地图**，读完你应该知道：这是什么项目、文档在哪、我能做什么、该按什么流程工作。

---

## 一、项目简介

<!-- 简要描述本项目：做什么、解决什么问题、技术栈 -->

---

## 二、文档导航

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

## 三、角色与权限

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

## 四、执行流程

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

## 五、故障处理

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
