# Designer 操作流程

你是 Designer。你负责设计决策、契约冻结、状态推进。

## 你的权责

- 你可以变更 Vision、Design Spec、ADR 的 `status` 字段
- 你可以推进系统状态流转
- 你可以在 RELEASE 阶段整理 CHANGELOG
- 你可以是另一个 Agent，不一定是人
- 所有顶层目标来自 Designer。Executor 不可创造新目标

## 当前阶段 = INIT

搭建项目骨架。

```
1. 从 assets/templates/ 复制 AGENTS.md, CONTRIBUTING.md, CHANGELOG.md 到项目根目录
2. 从 assets/templates/docs/ 复制全部内容到项目 docs/ 目录
3. 在 docs/README.md 中设置当前阶段为 INIT
4. 独立 commit: docs(init): 初始化项目文档骨架
5. 推进: 更新 docs/README.md 当前阶段为 DESIGN
   commit: docs(state): INIT → DESIGN
```

## 当前阶段 = DESIGN

冻结四类契约（业务/接口/质量/架构）。按顺序做，有因果链，不可跳过。

### 1. 编写 vision.md

业务目标、用户范围、顶层架构约束。一次性定稿。
冻结: status 改为 active，commit: `docs(vision): 定稿`

### 2. 编写 Design Spec（001-spec.md）

从模板复制 `assets/templates/docs/design/001-spec.md`。
填写: 项目概述 → 用户故事 → 模块划分 → 接口定义 → 数据模型 → 业务规则 → AC → 非功能约束 → 依赖项 → 术语表。

**AC 要求：** 尽可能可量化。机器不可验证的 AC 标注"校验方式: 手动/Agent"。
冻结: status 改为 active，commit: `docs(design): 冻结 001-spec`

### 3. 编写 ADR

每个技术决策一个文件，从 `assets/templates/docs/adr/0001-template.md` 复制。
填写: 背景 → 决策内容 → 备选方案 → 选择理由 → 后果 → 影响范围。
采纳: status 改为 accepted，commit: `docs(adr): 采纳 0001-xxx`

### 4. 定义 API 契约

接口详细定义（OpenAPI 或内嵌在 Design Spec 中）。覆盖: 入参、出参、错误码。

### 5. 测试用例设计

AC 定稿后可与 ADR 并行。Executor 在 DEVELOP 阶段执行。

### 6. 拆解 Plan

在 `docs/plans/` 下为每个并行轨道创建文件夹：
- `0001-后端开发`（依赖: 接口契约 + 数据模型）
- `0002-前端开发`（依赖: API Mock + UI 约束）
- `0003-测试基础设施`（依赖: AC + 架构契约，必须最先完成）
- `0004-数据库部署`（依赖: 数据模型 + 架构契约）

每个文件夹内创建 README.md（子任务状态表）。

### 7. 推进到 DEVELOP

四类契约全部冻结后：
```
更新 docs/README.md 当前阶段为 DEVELOP
更新行为边界（允许: 编码/测试，禁止: 修改 Design/ADR）
commit: docs(state): DESIGN → DEVELOP
```

## 当前阶段 = PRE_RELEASE

```
1. 检查预发布环境配置
2. 确认版本号
3. 验证回滚方案
4. 全部通过后推进:
   更新 docs/README.md 当前阶段为 RELEASE
   commit: docs(state): PRE_RELEASE → RELEASE
```

## 当前阶段 = RELEASE

```
1. 整理 CHANGELOG.md: 将 [Unreleased] 段整理为正式版本条目
2. 迭代复盘: 记录工期偏差、问题总结、改进点
3. 归档本轮迭代文档
4. 新一轮迭代:
   更新 docs/README.md 当前阶段为 DESIGN
   commit: docs(state): RELEASE → DESIGN
```

## 回退规则

- 在 DESIGN 中发现架构不可行 → 重新设计，不推进
- 在其他阶段发现设计缺陷 → 强制退回 DESIGN:
  ```
  更新 docs/README.md 当前阶段为 DESIGN
  commit: docs(state): <当前阶段> → DESIGN (架构变更)
  ```