# 文档状态定义

每种文档类型有独立的状态集合，不同文档类型的状态语义不共享。

## Vision

```
draft → active → archived
```
- `draft`: 草稿（Designer 变更）
- `active`: 已定稿（Designer 变更）
- `archived`: 因重大业务转型被归档（Designer 变更）

## Design Spec

```
draft → active → archived
```
- `draft`: 编写中，尚未冻结（Designer 变更）
- `active`: 已冻结，当前唯一生效版本（Designer 变更）
- `archived`: 被新版本替代，原地保留（Designer 变更）
- 同时只有一个 active。冻结后不可修改。
- 归档: 旧 Spec 改为 archived，更新 design/README.md

## ADR

```
draft → accepted → superseded
  │                      │
  └──────────────────────┴──→ deprecated
```
- `draft`: 提案中（Designer 变更）
- `accepted`: 已采纳（Designer 变更）
- `superseded`: 被新 ADR 替代（Designer 变更）
- `deprecated`: 已废弃（Designer 变更）

## Plan

```
pending → in_progress → done
              │
              └──→ blocked → in_progress
```
- `pending`: 等待执行（Executor 变更）
- `in_progress`: 正在执行（Executor 变更）
- `blocked`: 遇到阻塞（Executor 变更）
- `done`: 已完成（Executor 变更）

## Report

```
draft → complete
```
- `draft`: 编写中（Executor 变更）
- `complete`: 已提交（Executor 变更）

## README.md / CHANGELOG.md

无 frontmatter 状态字段。