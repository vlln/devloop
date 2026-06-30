# DEVELOP 阶段

## 你的职责

在 DEVELOP 阶段，你的职责是**创建 Plan 并推进执行**。你不一定亲自编码——你可以创建 Plan 文件，然后由任何 Agent（包括你自己）执行。

**Plan 是协调者与执行者之间的契约。** 执行者可能不加载本 skill，仅凭 Plan 文件和系统文档工作。因此 Plan 必须自包含执行边界。

## 创建 Plan

每个轨道一个 Plan 文件夹。在 `docs/plans/000x-任务名/` 下创建 `01-plan-xxx.md`。

**Plan 必须包含以下段：**

1. 目标 — 1-2 句话
2. 前置条件 — 开始执行前必须满足的条件
3. 依赖项 — 依赖的其他 Plan、外部服务、环境
4. 分步计划 — 具体步骤，可勾选
5. **执行边界** — 必须做和必须不做（见下方）
6. 当前进度 — 执行中更新
7. 阻塞点 — 遇到阻塞时记录

**执行边界示例：**

```markdown
## 执行边界

**你必须做：**
- 实现 POST /api/orders 接口，按 Design Spec 001 第四节定义
- 编写单元测试覆盖 AC-001 到 AC-005
- 运行单元测试直到全部通过（具体命令见 CONTRIBUTING.md）
- 完成后更新 Plan status 为 done，写入 Report

**你必须不做：**
- 不修改 Design Spec 或 ADR 的任何内容
- 不新增未在 AC 中定义的功能
- 不修改 docs/README.md 的系统状态字段
- 不修改其他轨道的 Plan 文件
```

**测试相关 Plan 的创建参考：**
- 轨道 C（测试基础设施）→ [testing/testing-infra.md](testing/testing-infra.md)
- 轨道 A/B（编码自测）→ [testing/testing-dev.md](testing/testing-dev.md)
- 全量集成测试 → [testing/testing-integrate.md](testing/testing-integrate.md)

## 执行 Plan

Plan 创建后，可以由任何 Agent 执行。执行方式灵活：

- 同一个 Agent 继续执行
- 发起 subagent，指定 Plan 路径
- 多个独立 Agent 会话并行执行不同轨道

执行者只需：读 Plan 文件 → 读 Design Spec（了解 AC）→ 执行。

## 检查 Report

Plan 执行完成后，检查 `01-report-xxx.md`：

- 执行摘要是否完整
- 关联 commit 是否列出
- 测试摘要是否填写（各层通过/失败数）
- 验收结果是否逐条 AC 标注 ✅/❌
- 是否有对权威文档的改动建议

## 推进到 INTEGRATE

全部轨道 Plan done 后：
```
更新 docs/README.md 当前阶段为 INTEGRATE
更新行为边界（允许: 全量测试，禁止: 新增功能代码）
commit: docs(state): DEVELOP → INTEGRATE
```

## 异常处理

| 异常 | 处理 |
|------|------|
| 执行者崩溃 | 丢弃 branch/worktree，任务重置为 pending |
| 步骤失败 | branch 内回退至步骤快照，内部重试 |
| 架构不可行 | 停止 DEVELOP，退回 DESIGN |
| 局部 bug | 在 DEVELOP ↔ INTEGRATE 修复循环内解决 |