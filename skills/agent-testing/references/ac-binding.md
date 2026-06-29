# AC 绑定测试用例

## 原则

- 每条 Design Spec 的 AC 必须有对应的测试用例
- 机器可验证的 AC 尽量机器化；机器不可验证的由 Agent 判定
- 测试用例与 AC 通过命名约定建立语义链，不依赖 frontmatter 字段

## 命名约定

```
测试用例文件: {AC编号}-{简短描述}.test.ts
示例: AC-001-用户注册成功.test.ts
```

## AC 分类

### 机器可验证的 AC（编写自动化测试）

```markdown
### AC-001: 用户注册成功
- 前置条件: 数据库无此用户
- 操作步骤: POST /api/register { username, password }
- 预期结果: 返回 201, 数据库新增一条用户记录
- 校验方式: 自动化
```

→ 对应测试用例: `AC-001-用户注册成功.test.ts`（接口测试）

### Agent 化判定的 AC（在 Report 中给出结论）

```markdown
### AC-005: 订单列表加载流畅
- 前置条件: 数据库存在 1000 条订单
- 操作步骤: 打开订单列表页面
- 预期结果: 页面在 2 秒内完成渲染，滚动不卡顿
- 校验方式: 手动
```

→ 在 Report 中记录: "AC-005 ✅ Agent 判定: Playwright trace 显示首次渲染 1.2s，滚动帧率 55fps，满足条件"

## 测试用例模板

```typescript
// tests/unit/AC-001-用户注册校验.test.ts
import { describe, it, expect } from 'vitest'

describe('AC-001: 用户注册校验', () => {
  it('空用户名应返回错误', () => {
    // 对应 AC-001 的前置条件和操作步骤
    const result = validateRegistration({ username: '', password: '123456' })
    expect(result.error).toBe('用户名不能为空')
  })
})
```

## 在 Report 中记录

```markdown
## 验收结果

| AC 编号 | 状态 | 说明 |
|---------|------|------|
| AC-001 | ✅ | 单元测试通过, commit abc123 |
| AC-002 | ✅ | 接口测试通过, commit abc124 |
| AC-005 | ✅ | Agent 判定: 渲染时间 1.2s, 帧率 55fps |