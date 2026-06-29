---
name: agent-testing
description: 可伸缩的多层测试体系。当 Agent 需要搭建测试基础设施、编写测试用例、执行分层测试、或绑定 AC 到测试用例时使用。独立于 agent-docs，可单独安装。
---

# Agent Testing System

## 你的身份

你是 Executor。你的任务是确保代码在合并前通过所有必需的测试。如果你被分配的是 DEVELOP 轨道 C（测试基础设施），你的任务优先级最高——必须在其他轨道开始编码前完成。

## 第一步：确定你要做什么

### 如果你是轨道 C（测试基础设施）

你必须在轨道 A/B 开始编码前完成。你的产出是**测试武器**，不是业务代码。

```
1. 读取 active Design Spec，提取所有 AC
2. 对照 references/test-layers.md，确定项目类型需要的测试层级
3. 搭建测试骨架：
   mkdir -p tests/unit tests/integration tests/e2e
   npm install -D vitest playwright  # 根据项目类型选择
4. 配置 package.json 测试脚本（每个测试层一个命令）
5. 准备测试数据、测试账号、环境变量
6. 为每条机器可验证的 AC 编写测试用例骨架（命名: AC-00X-xxx.test.ts）
7. 对机器不可验证的 AC，在测试清单中标注"Agent 判定"
8. 确认所有脚本可运行: npm run test:unit
9. 独立 commit: test(infra): 搭建测试基础设施
```

### 如果你是轨道 A/B（后端/前端）

你写代码时，测试基础设施应该已经就位。你的自测流程：

```
1. 完成一个功能点后，立即运行对应测试层
2. 单元测试不通过 → 不提交
3. 在 Report 的「测试摘要」段记录各层结果
```

### 如果你在 INTEGRATE 阶段

```
1. 确认所有轨道 Plan 已 done
2. 按层级顺序执行全量测试（不可跳过）:
   npm run test:unit
   npm run test:integration
   npm run test:contract     # 如果有
   npm run test:orchestration # 如果有
   npm run test:e2e          # 如果有
   npm run test:visual       # 如果有
3. 每层失败 → 停止，退回 DEVELOP 修复，修复后重新从该层开始
4. 全部通过 → 在 Report 中记录，报告给 Designer 推进到 PRE_RELEASE
```

## 写测试用例

### 机器可验证的 AC

打开 `references/ac-binding.md` 看命名约定和模板。

简短版：
```
1. 找到 Design Spec 中一条 AC，例如 AC-003
2. 创建 tests/unit/AC-003-xxx.test.ts
3. 测试用例必须覆盖 AC 的前置条件、操作步骤、预期结果
4. 写好一个，跑一个: npx vitest run tests/unit/AC-003-xxx.test.ts
```

### 机器不可验证的 AC

例如"页面加载流畅"、"交互体验良好"——这些你无法自动化判定。

```
1. 在测试清单中标注"Agent 判定"
2. 功能实现后，执行 E2E 测试获取 trace/截图
3. 基于 trace 数据给出判定
4. 在 Report 中记录:
   AC-005 ✅ Agent 判定: Playwright trace 显示首次渲染 1.2s, 帧率 55fps
```

## 输出测试结果

**不要输出完整日志。** 上下文是有限的。只输出摘要：

```markdown
## 测试摘要

| 测试层 | 通过/总数 | 失败用例 |
|--------|----------|----------|
| 单元测试 | 12/12 | — |
| 集成测试 | 5/5 | — |
| E2E | 2/3 | AC-007-订单取消 (选择器超时, 截图: tests/screenshots/AC-007-fail.png) |

## 验收结果

| AC 编号 | 状态 | 说明 |
|---------|------|------|
| AC-001 | ✅ | 单元测试通过 |
| AC-002 | ✅ | 接口测试通过 |
| AC-007 | ❌ | 选择器超时，需修复 |
| AC-010 | ✅ | Agent 判定: 渲染时间 1.2s |
```

## 关键规则

1. **测试基础设施先于编码完成。** 轨道 C 的 Executor 优先执行
2. **每层都是闸门。** 从内向外逐层执行，不可跳过。上一层不通过，不进入下一层
3. **低层机器化，高层智能化。** 单元/接口测试必须机器可执行；E2E 语义验证可由 Agent 判定
4. **AC 必须绑定测试用例。** 命名: AC-00X-xxx.test.ts
5. **输出摘要化。** 不输出完整日志，只输出通过/失败数、失败用例名、失败断言
6. **测试层级按项目类型伸缩。** 打开 `references/test-layers.md` 确定你的项目需要哪些层

需要详细定义时，打开：
- `references/test-layers.md` — 各层测试对象、校验目标、执行方式
- `references/ac-binding.md` — AC 命名约定、测试用例模板、Agent 判定示例