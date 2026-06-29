> 项目文档体系入口。Executor 进入 docs/ 后首先读取本文件。

---

## 当前系统状态

<!-- 由调度层在状态变更时更新。Executor 启动时读取此段，确认当前阶段和行为边界 -->

| 字段 | 值 |
|------|-----|
| **当前阶段** | `INIT` |
| **阶段说明** | 见 [agent-coding-spec.md](../agent-coding-spec.md) 第三节「系统生命周期状态机」 |

### 当前阶段行为边界

<!-- 根据当前阶段，从 agent-coding-spec.md 第三节复制对应的允许/禁止列表 -->

**允许：**
- 创建目录结构
- 创建 AGENTS.md / CONTRIBUTING.md / CHANGELOG.md
- 初始化 Git
- 初始化 CI 配置

**禁止：**
- 编写 Vision / Design / ADR / Plan
- 编写业务代码（src/）

---

## 子目录

| 路径 | 用途 |
|------|------|
| [vision.md](vision.md) | 全局顶层愿景 |
| [design/](design/) | Design Spec 规格文档（唯一业务事实源） |
| [adr/](adr/) | 架构决策记录 |
| [plans/](plans/) | 任务执行计划 |

---