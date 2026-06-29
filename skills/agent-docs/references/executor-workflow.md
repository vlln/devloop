# Executor 操作流程

你是 Executor。你负责执行任务、编码、测试、写 Report。

## 你的权责

- 你可以变更 Plan 和 Report 的 `status` 字段
- 你可以追加 CHANGELOG 的 `[Unreleased]` 段
- 你可以读取 Vision/Design/ADR，但**不可修改其内容或 status**
- 发现权威文档需修改时，在 Report 的「对权威文档的改动建议」中记录，由 Designer 决策
- 你可以是另一个 Agent，不一定是人

## 核心约束

**验证先于实现。** 测试基础设施（轨道 C）必须在编码开始前完成。低层测试（单元/接口）机器化，高层（E2E 语义）可由 Agent 判定。

**异常处理：**

| 异常 | 处理 |
|------|------|
| Agent 崩溃 | 丢弃 branch/worktree，任务重置为 pending |
| 步骤失败 | branch 内回退至步骤快照，内部重试 |
| 架构不可行 | 停止 DEVELOP，退回 DESIGN |
| 局部 bug | DEVELOP ↔ INTEGRATE 修复循环 |

**绝对禁止：**
- 修改 Vision、Design Spec、ADR 的内容或 status
- 修改全局契约
- 在没有 Plan 的情况下直接写代码
- 将文档修改与代码修改混入同一 commit

---

## 当前阶段 = DEVELOP

### 先确认你是哪个轨道

打开 `docs/plans/README.md`，找到你被分配的 Plan 文件夹。

**轨道 C（测试基础设施）必须最先完成。** A/B 开始编码前，测试武器必须就位。

### 轨道 C：测试基础设施

见 [testing/testing-infra.md](testing/testing-infra.md)。

### 轨道 A/B：后端/前端开发

```
1. 进入你的 Plan 文件夹
2. 创建或打开 01-plan-xxx.md，填写:
   - 目标
   - 前置条件
   - 依赖项
   - 分步计划
3. 创建独立 Git branch:
   git checkout -b plan/000x-任务名
4. 按 Plan 步骤编码
5. 每完成一步，运行对应测试层
6. 全部完成后，创建 01-report-xxx.md，填写:
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

### 轨道 D：数据库/部署

```
1. 基于数据模型编写 migration 脚本
2. 配置 CI/CD 脚本
3. 编写环境配置
4. 独立 commit
```

---

## 当前阶段 = INTEGRATE

### 这是唯一串行关口

必须等所有轨道 Plan done 才能进入。

```
1. 确认所有轨道 Plan 已 done
2. 按层级顺序执行全量测试（不可跳过）:
   npm run test:unit
   npm run test:integration
   npm run test:contract
   npm run test:orchestration
   npm run test:e2e
   npm run test:visual
3. 每层失败 → 停止，退回 DEVELOP 对应轨道修复
4. 全部通过 → 在 Report 中记录，报告给 Designer 推进到 PRE_RELEASE
```

### 修复循环规则

- 只修 bug，不新增功能
- 修复后重新从失败的那层开始执行
- 如果发现设计缺陷（不是 bug，是契约本身有问题）→ 退回 DESIGN:
  ```
  更新 docs/README.md 当前阶段为 DESIGN
  commit: docs(state): INTEGRATE → DESIGN (设计缺陷)
  ```

---

## 输出规范

**测试摘要**（不要输出完整日志）:

```markdown
## 测试摘要

| 测试层 | 通过/总数 | 失败用例 |
|--------|----------|----------|
| 单元测试 | 12/12 | — |
| E2E | 2/3 | AC-007 (选择器超时, 截图: tests/screenshots/AC-007-fail.png) |
```

**验收结果**:

```markdown
## 验收结果

| AC 编号 | 状态 | 说明 |
|---------|------|------|
| AC-001 | ✅ | 单元测试通过, commit abc123 |
| AC-005 | ✅ | Agent 判定: 渲染时间 1.2s |
| AC-007 | ❌ | 选择器超时，需修复 |
```