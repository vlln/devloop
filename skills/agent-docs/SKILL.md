---
name: agent-docs
description: 项目文档体系与生命周期管理。当 Agent 需要初始化项目文档结构、创建 Design/ADR/Plan/Report、管理文档状态、遵循系统边界、或判断当前阶段能做什么时使用。
---

# Agent Docs System

## When To Use

- 初始化新项目的文档骨架（目录结构 + 标准文件）
- 创建或修改 Design Spec、ADR、Plan、Report
- 管理文档状态流转（draft→active→archived 等）
- 判断当前系统阶段允许/禁止什么操作
- 需要理解 Designer/Executor 权责边界

## Workflow

### 初始化项目

```
1. 创建项目根目录文件: AGENTS.md, CONTRIBUTING.md, CHANGELOG.md
   模板见 assets/templates/ 对应文件
2. 创建 docs/ 目录结构:
   docs/README.md → docs/vision.md
   docs/design/README.md → docs/design/001-spec.md
   docs/adr/README.md → docs/adr/0001-template.md
   docs/plans/README.md → docs/plans/0001-template/
3. 在 docs/README.md 中设置当前系统状态为 INIT
4. 独立 Git commit: docs(init): 初始化项目文档骨架
```

### 创建 Design Spec

```
1. 复制 assets/templates/docs/design/001-spec.md 为 docs/design/001-spec.md
2. 填写: 项目概述 → 用户故事 → 模块划分 → 接口定义 → 数据模型 → 业务规则 → AC
3. status 保持 draft 直到 Designer 确认冻结
4. 冻结时将 status 改为 active，独立 commit
5. 更新 docs/design/README.md 版本列表
```

### 创建 ADR

```
1. 复制 assets/templates/docs/adr/0001-template.md 为 docs/adr/0001-xxx.md
2. 填写: 背景 → 决策内容 → 备选方案 → 选择理由 → 后果 → 影响范围
3. status 保持 draft 直到 Designer 采纳
4. 采纳时将 status 改为 accepted，独立 commit
5. 更新 docs/adr/README.md
```

### 创建 Plan/Report

```
1. 在 docs/plans/ 下创建 000x-任务名/ 文件夹
2. 创建 README.md（子任务状态表）
3. 创建 01-plan-xxx.md（目标 → 前置条件 → 依赖项 → 分步计划）
4. Plan 执行完成后创建 01-report-xxx.md（执行摘要 → commit → 产物 → 测试摘要 → AC 结果）
5. Plan/Report 一一对应
```

### 状态流转

```
系统状态变更时更新 docs/README.md 的「当前系统状态」段:
- 更新当前阶段字段
- 更新行为边界（允许/禁止列表）
- 独立 commit: docs(state): DESIGN → DEVELOP
```

## Rules

- **6 条系统边界不可违反。** 每次操作前对照 references/boundaries.md 检查是否越界
- **状态机是唯一流转路径。** 禁止跳跃或回跳（除 DEVELOP↔INTEGRATE 修复循环），见 references/state-machine.md
- **文档变更独立 commit。** 一次 commit 只含文档或只含代码，不混合
- **Designer 管状态，Executor 管执行。** 见 references/roles.md。发现权威文档需修改时在 Report 中建议，不自行修改
- **每种文档有独立的状态定义。** 见 references/document-status.md。status 字段不可跨类型混用
- **冻结即不可原地修改。** 要改 Design/ADR 必须走正式回退路径
- **关联用语义链。** 正文中引用文档路径和 AC 编号，不依赖 frontmatter 的 related 字段
- **模板是参考实现。** 可根据项目复杂度自适应简化或扩展，但必须覆盖四类契约（业务/接口/质量/架构）

## Output

- 符合规范的文档文件（含正确 frontmatter 和 status）
- 状态变更记录在 docs/README.md 中
- 每次文档变更独立 commit，commit message 格式: `docs(<scope>): <简述>`
- Plan/Report 成对出现，Report 关联 commit hash