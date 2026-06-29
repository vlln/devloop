---
name: agent-docs
description: 项目文档体系与生命周期管理。当 Agent 需要理解自己在项目中的角色、当前阶段能做什么、如何创建和管理文档时使用。
---

# Agent Docs System

## 你的身份

首先确定你的角色：

- 如果你被分配了设计任务（定义需求、架构决策、冻结契约）→ 你是 **Designer**
- 如果你被分配了执行任务（编码、测试、写 Report）→ 你是 **Executor**

你不一定固定是哪一个——同一轮对话中可能切换。但每次操作前，先确认你当前是哪一方。

## 每一步开始前

不管你是什么角色，打开 `docs/README.md`，读「当前系统状态」段。那里告诉你：

- 项目当前处于哪个阶段（INIT / DESIGN / DEVELOP / INTEGRATE / PRE_RELEASE / RELEASE）
- 这个阶段允许做什么
- 这个阶段禁止做什么

**如果当前阶段禁止你做某件事，即使你技术上能做到，也不要做。** 这是硬性约束。如果你认为阶段应该改变，在 Report 中建议，由 Designer 处理。

## 如果你是 Designer

### 当前阶段 = INIT

你的任务：搭建项目骨架。

```
1. 创建 AGENTS.md（从 assets/templates/AGENTS.md 复制）
2. 创建 CONTRIBUTING.md（从 assets/templates/CONTRIBUTING.md 复制）
3. 创建 CHANGELOG.md（从 assets/templates/CHANGELOG.md 复制）
4. 创建 docs/ 目录结构（从 assets/templates/docs/ 复制全部）
5. 在 docs/README.md 中设置当前阶段为 INIT
6. 独立 commit: docs(init): 初始化项目文档骨架
7. 推进到 DESIGN: 更新 docs/README.md 当前阶段为 DESIGN，commit: docs(state): INIT → DESIGN
```

### 当前阶段 = DESIGN

你的任务：冻结四类契约。

按顺序做（有因果依赖，不能跳过）：

```
1. 编写 vision.md → 业务目标、用户范围、顶层约束
   冻结: status 改为 active，commit

2. 编写 Design Spec（001-spec.md）→ 接口 + 数据模型 + AC
   AC 尽量可量化。机器不可验证的 AC 标注"校验方式: 手动/Agent"
   冻结: status 改为 active，commit

3. 编写 ADR → 每个技术决策一个文件
   采纳: status 改为 accepted，commit

4. 定义 API 契约 → 接口详细定义（OpenAPI 或内嵌在 Design Spec 中）

5. 拆解 Plan → 在 docs/plans/ 下创建任务文件夹
   每个轨道一个文件夹:
   - 0001-后端开发
   - 0002-前端开发
   - 0003-测试基础设施
   - 0004-数据库部署

6. 测试用例设计 → 在 AC 定稿后可以与 ADR 并行
   参考 agent-testing skill

7. 全部完成后，推进到 DEVELOP:
   更新 docs/README.md 当前阶段为 DEVELOP
   commit: docs(state): DESIGN → DEVELOP
```

**如果你发现架构不可行**：不要推进到 DEVELOP。重新设计后再次 commit。

### 当前阶段 = PRE_RELEASE

```
1. 检查预发布环境配置
2. 确认版本号
3. 验证回滚方案
4. 全部通过后推进到 RELEASE: commit docs(state): PRE_RELEASE → RELEASE
```

### 当前阶段 = RELEASE

```
1. 整理 CHANGELOG.md（将 [Unreleased] 段整理为正式版本条目）
2. 迭代复盘：记录工期偏差、问题总结、改进点
3. 归档本轮迭代文档
4. 新一轮迭代: commit docs(state): RELEASE → DESIGN
```

## 如果你是 Executor

### 当前阶段 = DEVELOP

**先确认你是哪个轨道。** 打开 `docs/plans/README.md`，找到你被分配的 Plan 文件夹。

**轨道 C 的 Executor 优先执行**（测试基础设施必须在 A/B 开始编码前完成）。

```
1. 进入你的 Plan 文件夹
2. 创建或打开 01-plan-xxx.md，填写：
   - 目标
   - 前置条件
   - 依赖项
   - 分步计划
3. 在独立 Git branch 中执行：
   git checkout -b plan/000x-任务名
4. 按 Plan 步骤编码
5. 每完成一步，运行对应测试
6. 全部完成后，创建 01-report-xxx.md，填写：
   - 执行摘要
   - 关联 commit（hash 列表）
   - 产物清单
   - 测试摘要（各层通过/失败数）
   - 验收结果（逐条 AC ✅/❌）
   - 遗留问题
   - 对权威文档的改动建议（如果有）
7. Plan status 改为 done，commit
8. 更新 CHANGELOG.md 的 [Unreleased] 段
```

**绝对禁止：**
- 修改 Vision、Design Spec、ADR 的内容或 status
- 修改全局契约
- 在没有 Plan 的情况下直接写代码

**如果你发现 Design/ADR 有问题：**
- 不要自己修改
- 在 Report 的「对权威文档的改动建议」中记录
- 标记 Plan 为 blocked
- 等待 Designer 决策

### 当前阶段 = INTEGRATE

```
1. 确认所有轨道 Plan 已 done
2. 执行全量测试（按层级从内到外）：
   单元 → 集成 → 接口契约 → 接口编排 → E2E → 视觉回归
3. 全部通过 → 在 Report 中记录，报告给 Designer 推进到 PRE_RELEASE
4. 测试失败 → 退回 DEVELOP 对应轨道修复，修复后再次 INTEGRATE
   - 只修 bug，不新增功能
   - 如果发现设计缺陷，退回 DESIGN（由 Designer 处理）
```

## 通用规则

当你需要更详细的规则时，打开对应文件：

- 不确定是否越界 → `references/boundaries.md`
- 不确定状态流转 → `references/state-machine.md`
- 不确定谁有权做什么 → `references/roles.md`
- 不确定文档状态怎么改 → `references/document-status.md`

**硬性规则（永远记住）：**

1. 文档变更和代码变更永远分开 commit
2. 冻结的东西不能原地改，必须走正式回退
3. 关联用语义链（正文中引用 AC 编号和文件路径），不需要 frontmatter 的 related 字段
4. 模板是参考，可以根据项目复杂度简化或扩展，但四类契约（业务/接口/质量/架构）必须覆盖