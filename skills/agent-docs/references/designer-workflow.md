# Designer 操作流程

你是 Designer。你负责设计决策、契约冻结、状态推进。

## 你的权责

- 你可以变更 Vision、Design Spec、ADR 的 `status` 字段
- 你可以推进系统状态流转（INIT→DESIGN→DEVELOP→...）
- 你可以在 RELEASE 阶段整理 CHANGELOG
- 你可以是另一个 Agent，不一定是人

## 核心约束

**契约与执行分离。** 在四类契约冻结之前，任何代码都不能写。冻结 = status 从 `draft` 变为 `active`，伴随独立 commit。冻结后不可原地修改——要改必须退回 DESIGN、新建版本、旧版本归档。

**设计者意图为根。** 所有顶层目标来自 Designer。Executor 不可创造新目标。架构变更、版本发布、需求调整由你决策。

**四类最小契约：**

| 契约类型 | 必须回答 | 冻结时机 |
|----------|---------|----------|
| 业务契约 | 做什么、为谁做、为什么 | DESIGN 最早 |
| 接口契约 | 模块间如何通信、数据长什么样 | 业务契约冻结后 |
| 质量契约 | 什么算成功、什么算失败（AC） | 与业务契约同步 |
| 架构契约 | 技术选型、约束、取舍 | 接口契约定义前 |

**文档状态规则：**

| 文档 | 状态流转 | 谁可变更 |
|------|---------|----------|
| Vision | `draft → active → archived` | Designer |
| Design Spec | `draft → active → archived`（同时只有一个 active） | Designer |
| ADR | `draft → accepted → superseded/deprecated` | Designer |

---

## 当前阶段 = INIT

搭建项目骨架。

```
1. 复制 assets/templates/ 下的 AGENTS.md, CONTRIBUTING.md, CHANGELOG.md 到项目根目录
2. 复制 assets/templates/docs/ 下全部内容到项目 docs/ 目录
3. 在 docs/README.md 中设置当前阶段为 INIT
4. 独立 commit: docs(init): 初始化项目文档骨架
5. 推进: 更新 docs/README.md 当前阶段为 DESIGN
   commit: docs(state): INIT → DESIGN
```

## 当前阶段 = DESIGN

冻结四类契约。按顺序做（有因果链，不可跳过）：

### 1. 编写 vision.md

业务目标、用户范围、顶层架构约束。一次性定稿，几乎不修改。
冻结: status 改为 active，commit: `docs(vision): 定稿`

### 2. 编写 Design Spec（001-spec.md）

从 `assets/templates/docs/design/001-spec.md` 复制模板。
填写: 项目概述 → 用户故事 → 模块划分 → 接口定义 → 数据模型 → 业务规则 → AC → 非功能约束 → 依赖项 → 术语表。

**AC 要求：** 尽可能可量化。机器不可验证的 AC 标注"校验方式: 手动/Agent"。
冻结: status 改为 active，commit: `docs(design): 冻结 001-spec`

### 3. 编写 ADR

每个技术决策一个文件，从 `assets/templates/docs/adr/0001-template.md` 复制。
填写: 背景 → 决策内容 → 备选方案 → 选择理由 → 后果 → 影响范围。
采纳: status 改为 accepted，commit: `docs(adr): 采纳 0001-xxx`

### 4. 定义 API 契约

接口详细定义（OpenAPI 或内嵌在 Design Spec 中）。必须覆盖：入参、出参、错误码。

### 5. 测试用例设计

AC 定稿后可与 ADR 并行。Executor 会在 DEVELOP 阶段执行。

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
- 禁止跳跃（如 INIT → DEVELOP）。禁止回跳（除 DESIGN 回退和 DEVELOP↔INTEGRATE 修复循环）