<div align="center">

# devloop

为 Agent 与人提供可安装的专业软件开发生命周期：有文档、有历史、可并行、可合作，从立项、验收到交付与多轮改进。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-spec-6e3af2)](https://agentskills.io/specification)

[English](<README.en.md>)

</div>

## 适合什么项目

需要跨会话持续推进、多人或多 Agent 合作、管理变化与验收交付的长期软件项目。devloop 不替模型选择每个编码步骤，也不以文档和审批数量衡量专业性。

## 提供什么

- **完整生命周期**：立项 → 需求与架构 → 工程准备 → 实现与集成 → 验收 → 交付、反馈与下一轮。
- **项目连续性**：项目、一次交付、工作单元分别跟踪；下一版本设计与当前版本验收可以并行。
- **需求变化管理**：新想法不自动变实现任务；插单要说明影响，明确改向后同步范围、计划与证据。
- **灵活而有边界的决定**：复用有效对话确认与条件授权，只问缺口；方案认可不等于生产操作许可。
- **可合作的文档**：当前规格连贯、重大历史可追溯；高层需求不被局部实现细节污染，共享文档有整合责任。
- **可接管的工作**：责任、依赖、工作位置、已验证成果与下一步持续保留，中断不默认丢弃工作树。
- **主动工程选择**：在动手、变更、集成和停止等节点提示判断，提供分支隔离、风险实验、回归与自检等默认策略，而不是等待用户逐项提醒。
- **真实交付依据**：验证实际消费者使用的产物，区分实现、测试、验收、交付与运行健康。

保留专业开发的阶段关口，按风险与项目事实裁剪工程方法；沿用既有工具和分支策略，不强制所有项目改用 Gitflow。

## 安装

### skit

```sh
brew install vlln/tap/skit
skit install vlln/devloop/skills/devloop
```

### npx skills

```sh
npx skills add vlln/devloop
```

### 手动

将[技能目录](<skills/devloop/>)复制到 Agent 的 skills 目录，按工具要求重启或重新加载。安装工具可选，技能本身不要求 skit 运行时。

远程安装获取的是已发布仓库内容，不代表本地未发布改动已同步；旧项目不会自动迁移。

## 开始使用

向 Agent 提供项目目标并要求“用 devloop 接入和推进这个项目”。已有项目会先扫描现有规范、在途工作和证据，增量接入，而不是覆盖布局或伪造历史决定。

也可以用于接手项目、评估本轮新需求、协调并行工作、整理规格或准备验收交付。无需先让用户手工填写整套模板。

## Skills

| Skill | 用途 |
|---|---|
| [devloop](<skills/devloop/SKILL.md>) | 专业开发生命周期、跨会话推进、并行协作、需求变化与多轮交付 |

## 开发与验证资料

- [设计说明](<docs/design.md>)：设计边界和机制理由。
- [重设计记录](<docs/redesign/README.md>)：候选设计及其到实现的过程。
- [隔离验证](<docs/redesign/validation/README.md>)：本地交付、跨会话变更和边界实验的证据与限制。
- [Backlog](<docs/backlog.md>)：本仓库的后续工作。

## 许可证

MIT
