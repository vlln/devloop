# PRE_RELEASE / RELEASE 阶段

## PRE_RELEASE：预发布验证

```
1. 检查预发布环境配置
2. 确认版本号
3. 验证回滚方案
4. 全部通过后推进:
   更新 docs/README.md 当前阶段为 RELEASE，追加最近事件，提交。约定前缀: `docs(state):`
```

## RELEASE：迭代闭环

```
1. 整理 CHANGELOG.md: 将 [Unreleased] 段整理为正式版本条目
2. 迭代复盘: 记录工期偏差、问题总结、改进点
3. 归档本轮迭代文档
4. 新一轮迭代:
   更新 docs/README.md 当前阶段为 DESIGN，追加最近事件，提交。约定前缀: `docs(state):`
```

## 回退规则

- 在 PRE_RELEASE 发现问题 → 退回 INTEGRATE 修复
- 在 RELEASE 发现重大缺陷 → 退回 DESIGN:
  ```
  更新 docs/README.md 当前阶段为 DESIGN，追加最近事件，提交
  ```