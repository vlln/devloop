---
title: plans/ 任务执行计划
description: 任务执行计划索引，列出所有 Plan 容器的状态、创建时间和关联 Spec。
type: index
---

## 任务列表

| 编号 | 标题 | 状态 | 创建时间 | 绑定 Spec | 关联 ADR |
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

- Plan 由各阶段根据 Spec 模块划分自行创建
- Agent 权限边界见 [AGENTS.md](../../AGENTS.md)
- 状态在 Plan 文件夹的 README.md 和本 README 中维护，Plan 文件夹原地保留
