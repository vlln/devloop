# INTEGRATE 阶段

## 前置条件

全部轨道 Plan 已 done。这是唯一串行关口——必须等所有轨道完成。

## 执行全量测试

按层级顺序执行，不可跳过：

```
1. npm run test:unit
2. npm run test:integration
3. npm run test:contract        # 如果有 API
4. npm run test:orchestration   # 如果有多接口联动
5. npm run test:e2e             # 如果有 UI
6. npm run test:visual          # 如果是前端
```

每层通过后才进入下一层。

## 每层失败时

```
1. 停止，不继续下一层
2. 提取失败信息: 失败用例名、失败断言、截图路径
3. 退回 DEVELOP 对应轨道修复
4. 修复完成后，重新从失败的那层开始执行
```

## 全部通过时

```
1. 生成测试报告
2. 在 Report 中记录各层通过/总数和耗时
3. 推进到 PRE_RELEASE:
   更新 docs/README.md 当前阶段为 PRE_RELEASE
   commit: docs(state): INTEGRATE → PRE_RELEASE
```

## 修复循环规则

- 只修 bug，不新增功能
- 修复后重新从失败的那层开始
- 如果发现设计缺陷（不是 bug，是契约本身有问题）→ 退回 DESIGN:
  ```
  更新 docs/README.md 当前阶段为 DESIGN
  commit: docs(state): INTEGRATE → DESIGN (设计缺陷)
  ```

## 输出格式

**测试摘要**（不要输出完整日志）:

```markdown
| 测试层 | 通过/总数 | 失败用例 | 耗时 |
|--------|----------|----------|------|
| 单元测试 | 12/12 | — | 2.3s |
| E2E | 2/3 | AC-007 (选择器超时, 截图: tests/screenshots/AC-007-fail.png) | 15.8s |

结论: ❌ 未通过 / ✅ 全部通过
```