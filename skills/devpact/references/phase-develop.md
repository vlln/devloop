# DEVELOP 阶段

## 固定阶段

DEVELOP 是基于冻结契约的多轨道并行编码阶段。每条轨道在独立 Git branch 中执行。**Plan 是协调者与执行者之间的契约。** 执行者可能不加载本 skill，仅凭 Plan 文件和系统文档工作。因此 Plan 必须自包含「执行边界」段。

## 子阶段

### 创建 Plan（必选，所有轨道）

每个轨道一个 Plan 文件夹。在 `docs/plans/000x-任务名/` 下创建 `01-plan-xxx.md`。

Plan 必须包含以下段：
1. 关联文档 — 执行者需要读取的 Design Spec 和 ADR 路径
2. 目标 — 1-2 句话
3. 前置条件 — 开始执行前必须满足的条件
4. 依赖项 — 依赖的其他 Plan、外部服务、环境
5. 分步计划 — 具体步骤，可勾选
6. **执行边界** — 必须做和必须不做（见下方）

**执行边界示例：**

```markdown
## 执行边界

**你必须做：**
- 实现 [具体功能]，按 Design Spec 00x 第 x 节定义
- 编写单元测试覆盖本次修改的代码
- 运行单元测试直到全部通过（具体命令见 CONTRIBUTING.md）
- 完成后更新 Plan status 为 done，写入 Report

**你必须不做：**
- 不修改 Design Spec 或 ADR 的任何内容
- 不新增未在 AC 中定义的功能
- 不修改 docs/arch/README.md 的系统状态字段
- 不修改其他轨道的 Plan 文件
```

### 执行 Plan（必选，所有轨道）

Plan 创建后，可以由任何 Agent 执行。执行方式灵活：
- 同一个 Agent 继续执行
- 发起 subagent，指定 Plan 路径
- 多个独立 Agent 会话并行执行不同轨道

执行者只需：读 Plan 文件 → 读 Design Spec（了解 AC）→ 执行。

### 检查 Report（必选，所有轨道）

Plan 执行完成后，检查 `01-report-xxx.md`：
- 执行摘要是否完整
- 关联 commit 是否列出
- 测试摘要是否填写（各层通过/失败数）
- 验收结果是否逐条 AC 标注 ✅/❌
- 变更摘要是否填写
- 是否有对权威文档的改动建议

检查通过后，更新容器 README 状态表（Plan 状态 + AC 覆盖状态），追加最近事件到 `docs/README.md`。

### 测试基础设施（适用：需要自动化测试的项目）

测试基础设施（轨道 A）必须在其他轨道开始编码前完成。职责是搭建框架和 E2E 脚手架，不编写具体测试用例。参考 [testing/ref-testing-infra.md](testing/ref-testing-infra.md)。

## 推进到 INTEGRATE

全部轨道 Plan done 后，验证出口把关（见 SKILL.md 阶段证明链），全部通过后：更新 `docs/README.md` 当前阶段为 INTEGRATE，追加最近事件，提交。约定前缀 `docs(state):`。

## 异常处理

| 异常 | 处理 |
|------|------|
| 执行者崩溃 | 丢弃 branch/worktree，任务重置为 pending |
| 步骤失败 | branch 内回退至步骤快照，内部重试 |
| 架构不可行 — 轻微约束 | 依赖能用但方式与预期不一致。更新 ADR 追加修订记录，在 DEVELOP 内调整，不退回 DESIGN |
| 架构不可行 — 架构颠覆 | 技术路线走不通，必须更换方案。停止 DEVELOP，退回 DESIGN 执行正式变更流程（见 phase-design.md「设计变更」子阶段） |

## 参考实现

### 全栈 Web 项目

4 条轨道并行：
- 轨道 A：测试基础设施（参考 [testing/ref-testing-infra.md](testing/ref-testing-infra.md)，必须最先完成）
- 轨道 B：后端开发（编码自测参考 [testing/ref-testing-dev.md](testing/ref-testing-dev.md)）
- 轨道 C：前端开发（编码自测参考 [testing/ref-testing-dev.md](testing/ref-testing-dev.md)）
- 轨道 D：数据库/部署脚本
- 轨道 E：系统级测试用例（基于 AC 编写集成/E2E 用例，在 A 就位后、INTEGRATE 之前完成）

### CLI 工具项目

2 条轨道：
- 轨道 A：测试基础设施（参考 [testing/ref-testing-infra.md](testing/ref-testing-infra.md)，必须最先完成）
- 轨道 B：核心功能（编码自测参考 [testing/ref-testing-dev.md](testing/ref-testing-dev.md)）