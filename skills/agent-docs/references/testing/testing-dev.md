# 编码自测（DEVELOP 轨道 A/B）

你是轨道 A（后端）或 B（前端）的 Executor。你在写代码，测试基础设施应该已经就位。

## 工作流

```
1. 完成一个功能点
2. 运行对应测试层:
   npm run test:unit
3. 不通过 → 修复 → 重新运行，直到通过
4. 通过 → 提交代码
5. 在 Report 中记录测试结果
```

## 写测试用例

找到 Design Spec 中的 AC，按以下约定创建测试文件：

**命名:** `AC-00X-简短描述.test.ts`

```typescript
// tests/unit/AC-001-用户注册校验.test.ts
import { describe, it, expect } from 'vitest'

describe('AC-001: 用户注册校验', () => {
  it('空用户名应返回错误', () => {
    const result = validateRegistration({ username: '', password: '123456' })
    expect(result.error).toBe('用户名不能为空')
  })
})
```

测试必须覆盖 AC 的前置条件、操作步骤、预期结果。写好一个，跑一个：`npx vitest run tests/unit/AC-003-xxx.test.ts`

## 机器不可验证的 AC

例如"页面加载流畅"、"交互体验良好"——你无法自动化判定。

```
1. 在测试清单中标注"Agent 判定"
2. 功能实现后，执行 E2E 测试获取 trace/截图
3. 基于 trace 数据给出判定
4. 在 Report 中记录:
   AC-005 ✅ Agent 判定: Playwright trace 显示首次渲染 1.2s, 帧率 55fps
```

## 在 Report 中记录

```markdown
## 测试摘要

| 测试层 | 通过/总数 | 失败用例 |
|--------|----------|----------|
| 单元测试 | 12/12 | — |
| 集成测试 | 5/5 | — |

## 验收结果

| AC 编号 | 状态 | 说明 |
|---------|------|------|
| AC-001 | ✅ | 单元测试通过 |
| AC-002 | ✅ | 接口测试通过 |
| AC-005 | ✅ | Agent 判定: 渲染时间 1.2s |
```

## 注意

- 不要输出完整测试日志。只输出摘要
- 单元测试不通过 → 不提交
- 你的 Report 必须关联 commit hash 列表