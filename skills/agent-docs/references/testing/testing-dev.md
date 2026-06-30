# 编码自测 Plan（DEVELOP 轨道 A/B）

当你在 DEVELOP 阶段创建后端或前端开发的 Plan 时，参考以下内容编写 Plan 文件。

## Plan 的「分步计划」应包含

### 工作流

```
1. 完成一个功能点
2. 运行对应测试层: npm run test:unit
3. 不通过 → 修复 → 重新运行，直到通过
4. 通过 → 提交代码
5. 在 Report 中记录测试结果
```

### 测试用例命名

`AC-00X-简短描述.test.ts`

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

### 机器不可验证的 AC

在 Plan 中标注哪些 AC 需要 Agent 判定。执行者完成功能后，基于 trace/截图给出判定，在 Report 中记录：
```
AC-005 ✅ Agent 判定: Playwright trace 显示首次渲染 1.2s, 帧率 55fps
```

## Plan 的「执行边界」应包含

```markdown
## 执行边界

**你必须做：**
- 实现 [具体模块] 的接口和逻辑，按 Design Spec 00x 第 x 节定义
- 编写单元测试覆盖 AC-00x 到 AC-00x
- 运行测试直到全部通过
- 完成后写入 Report，关联 commit hash

**你必须不做：**
- 不修改 Design Spec 或 ADR
- 不新增未在 AC 中定义的功能
- 不修改 docs/README.md 的系统状态字段
```

## Report 输出格式

执行者应在 Report 中按以下格式输出：

```markdown
## 测试摘要
| 测试层 | 通过/总数 | 失败用例 |
|--------|----------|----------|
| 单元测试 | 12/12 | — |

## 验收结果
| AC 编号 | 状态 | 说明 |
|---------|------|------|
| AC-001 | ✅ | 单元测试通过, commit abc123 |
| AC-005 | ✅ | Agent 判定: 渲染时间 1.2s |
```