# PRE_RELEASE / RELEASE 阶段

## PRE_RELEASE：部署验证

```
1. 执行 CD 脚本，部署到 staging 环境
   → 失败 → 修复 CD 脚本，重新部署，直到成功
2. 执行冒烟测试（核心流程快速验证）
3. 环境配置验证（数据库、密钥、依赖）
4. 确认版本号、tag、回滚方案
5. 灰度策略确认（如有）
6. 全部通过后推进:
   更新 docs/README.md 当前阶段为 RELEASE，追加最近事件，提交。约定前缀: `docs(state):`
```

## RELEASE：迭代闭环

```
1. 执行 CD 脚本，部署到 production 环境
2. 整理 CHANGELOG.md: 将 [Unreleased] 段整理为正式版本条目
3. 迭代复盘: 记录工期偏差、问题总结、改进点
4. 归档本轮迭代文档
5. 新一轮迭代:
   更新 docs/README.md 当前阶段为 DESIGN，追加最近事件，提交。约定前缀: `docs(state):`
```

## 回退规则

- 在 PRE_RELEASE 发现问题 → 修复后重新部署，直到通过
- 在 RELEASE 发现重大缺陷 → 退回 DESIGN:
  ```
  更新 docs/README.md 当前阶段为 DESIGN，追加最近事件，提交
  ```