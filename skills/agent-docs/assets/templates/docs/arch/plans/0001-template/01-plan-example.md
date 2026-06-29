---
title: 01-plan-example
description: 子任务执行计划模板，定义目标、前置条件、分步计划、当前进度和阻塞点。
type: plan
# status: pending | in_progress | blocked | done
#   pending     → 已创建，等待执行（Executor 变更）
#   in_progress → 正在执行（Executor 变更）
#   blocked     → 遇到阻塞，等待外部条件（Executor 变更）
#   done        → 已完成，不再修改（Executor 变更）
status: template
created: YYYY-MM-DDTHH:MM:SSZ
---

# 01-plan: [子任务标题]

---

## 目标

<!-- 本次子任务要达成的具体目标，1-2 句话 -->

---

## 前置条件

<!-- 开始执行前必须满足的条件 -->

- [ ] 

---

## 依赖项

<!-- 本 Plan 依赖的其他 Plan、外部服务、环境 -->

| 依赖 | 类型 | 状态 |
|------|------|------|
| | Plan / 外部服务 / 环境 | 就绪 / 等待中 |

---

## 分步计划

- [ ] Step 1: 
- [ ] Step 2: 
- [ ] Step 3: 

---

## 当前进度

<!-- 当前执行到哪一步，遇到什么问题 -->

---

## 阻塞点

<!-- 若有阻塞，记录原因和依赖；无阻塞则写"无" -->

无