---
title: plans/ 任务执行计划
description: 任务执行计划索引，列出所有 Plan 容器的状态、创建时间和关联 Design。
type: index
---

> 单次 Agent 执行任务的完整上下文容器。每个文件夹是一次独立执行，内部可包含多个子任务。
> 结构示例见 [0001-template/](0001-template/)。

---

## 任务列表

| 编号 | 标题 | 状态 | 创建时间 | 绑定 Design | 关联 ADR |
|------|------|------|----------|-------------|---|
| [0001](0001-template/) | Plan 模板（参考用） | template | — | — | - |

---

## 状态说明

| 状态 | 含义 |
|------|------|
| pending | 待执行 |
| in_progress | 执行中 |
| blocked | 阻塞（需注明原因） |
| done | 已完成 |

---

## 命名规范

- 文件夹：`xxxx-简短描述`（四位序号，按创建顺序递增）
- 内部子任务文件：`xx-plan-xxx.md` + `xx-report-xxx.md`（成对，一位序号）

---

## 规则

- Plan 可由人创建，Agent 也可基于 ADR 自行生成
- Agent 权限边界见 [AGENTS.md](../../AGENTS.md)
- 状态在 Plan 文件夹的 README.md 和本 README 中维护，Plan 文件夹原地保留
