# Designer/Executor 角色与权责

两个角色不绑定到"人"或"Agent"的具体身份。

## Designer（设计者）

- 负责规划、设计、决策
- 可变更: Vision、Design Spec、ADR 的 status 字段
- 可推进系统状态流转（INIT→DESIGN→DEVELOP→...）
- 可管理 CHANGELOG 正式版本条目（RELEASE 阶段）
- 可以是人，也可以是另一个 Agent

## Executor（执行者）

- 负责实现、执行
- 可变更: Plan、Report 的 status 字段
- 可追加 CHANGELOG 的 `[Unreleased]` 段
- 可读写 Plan/Report，可读取 Vision/Design/ADR
- 不可修改 Vision/Design/ADR 的内容或 status
- 发现权威文档需修改时，在 Report 中记录建议，由 Designer 决策

## 第一推动力

系统的唯一固定起点是 Designer 提供的初始设计意图。不可被 Executor 僭越。

## 协作光谱

| 自动化程度 | Designer | Executor | 典型场景 |
|-----------|----------|----------|----------|
| 高 | Agent | Agent | Agent 独立分析需求、编写 Design/ADR，人仅确认 |
| 中 | 人 + Agent 讨论 | Agent | 人描述需求，Agent 起草，人确认后冻结 |
| 低 | 人 | Agent | 人编写完整 Design/ADR，Agent 执行 Plan |

## 状态变更权分配

| 文档类型 | 状态变更权 |
|----------|-----------|
| Vision | Designer |
| Design Spec | Designer |
| ADR | Designer |
| Plan | Executor |
| Report | Executor |
| CHANGELOG | Executor（追加 Unreleased）、Designer（整理发布） |
| 系统状态 | Designer（阶段推进）、Executor（DEVELOP↔INTEGRATE 循环） |