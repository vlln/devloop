# 隔离验证证据索引

记录类型分开：结构检查、Agent 实际项目执行、边界答复实验、独立复核。前三者不能互相代替；条文存在不证明行为正确，模拟回复也不证明生产操作已执行。

## 产品与环境

- [初始快照摘要](<snapshot-initial.json>)：首轮实验的 33 个技能文件 SHA-256。
- [首轮最终快照摘要](<snapshot-final.json>)：首轮补齐安装后独立评审义务后的 33 文件摘要；与初始只有常驻简规模板一处不同。后续[工程选择补充](<../engineering-choices.md>)另有快照，不能用本摘要校验当前工作树。
- [环境与范围](<environment.json>)：会话模型标识、环境与整体摘要；子执行者使用当前配置默认模型，没有跨模型对照。
- [静态结果](<static-results.json>)：6 项结构测试、9 份 YAML、隔离目录安装与 skit 链接兼容性说明。

## 原始执行记录

以下 `.txt` 是从隔离项目原样保存的 Markdown 文本。内部相对链接保留其**原项目上下文**，不是仓库导航；应从会话实验目录定位，不能把复制后的链接当作仓库文件引用。JSON 中的绝对位置同样属于本次实验，不是公开可用路径。这里未归档嵌套 Git 仓库或二进制产物；摘要和日志用于追溯，完整演练可按[固定输入](<../../../tests/fixtures/README.md>)重建。

| 记录 | 性质与范围 |
|---|---|
| [首轮新项目观察](<new-project-round1-observation.txt>) | 新安装、实现、验证、受托验收、同字节本地 zipapp 交付的执行者记录 |
| [候选制品检查](<new-project-round1-acceptance.json>) | 27 项独立目录实际候选检查，包含对象摘要和各项输出 |
| [实际交付检查](<new-project-round1-delivery.json>) | 接受候选与本地交付摘要对应、三条现场消费结果 |
| [已有项目接入观察](<legacy-onboarding-observation.txt>) | 保留原生资料和 main，增量接入完成；原业务交付仍待验收，不补造历史 |
| [边界答复](<boundary-outcomes.txt>) | 六组模拟输入下的实际答复与拟记录；没有真实数据库、并行任务或生产恢复 |
| [已决范围变更](<legacy-scope-change.txt>) | 新会话处理优惠券本轮决定，维护承诺与选择性证据，不改业务 |
| [累计候选建议](<legacy-scope-proposals.txt>) | 再次新会话识别未决会员/礼品卡，保留本轮优惠券，不把推荐冒充用户采纳 |
| [新项目第二轮观察](<new-project-round2-observation.txt>) | 全新会话只凭项目资料完成 --column 增量及本地交付，首轮22文件保留 |
| [二轮实际候选](<new-project-round2-acceptance.json>) / [交付](<new-project-round2-delivery.json>) | 49 项实际制品检查与同字节交付 |
| [首轮历史保留](<new-project-round1-preservation.json>) | 对接管时基线和 Git 对象逐字节核对受保护文件 |
| [主会话二轮独立消费](<round2-independent.json>) | 复制实际包到独立目录，默认 amount 与 --column net 路径实跑，输入不改，首轮摘要不变 |
| [仅讨论问题](<new-project-question.txt>) | 又一新会话讨论远程汇率，仅写观察；已交付状态与包字节未改，未启动下一轮 |
| [最终重新安排与交接](<legacy-final-handoff.txt>) | 用户采纳会员/礼品卡留后续，执行者更新决定效力并交接；优惠券仍本轮，业务仍未交付 |

后续轮次与最终评估见[实现与验证记录](<../implementation.md>)。尚未结束的轮次不在本索引提前记通过。

## 后续工程选择定向验证

[工程选择补充](<../engineering-choices.md>)另存新快照与四夹具结果：[快照](<engineering-choices/manifest.json>)、[干净/已有分支核验](<engineering-choices/independent-feature-existing.json>)、[脏目录/主干例外核验](<engineering-choices/independent-dirty-mainline.json>)。原始观察分别为[新工作](<engineering-choices/feature-observation.txt>)、[已有分支](<engineering-choices/existing-observation.txt>)、[脏目录](<engineering-choices/dirty-observation.txt>)、[主干策略](<engineering-choices/mainline-observation.txt>)。它们不覆盖或改写首轮快照与结果。

## 解释边界

实验输入含明确授权与范围约束，部分场景直接指出不得重复确认或不得实现；因此结果证明的是该条件下执行行为，不证明只有本技能才能做到，也不能从中推导对无约束自然输入的独立因果收益。本轮没有无技能基线 A/B、弱文档模型或长期大型多团队实战；这些属于后续评估。

有限的新会话接手可检验项目资料是否足以继续，不等于在真实进程崩溃、跨宿主任务恢复或并发竞争中完成了故障注入测试。
