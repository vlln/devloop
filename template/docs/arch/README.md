> 项目文档体系入口。Agent 启动后首先读取本文件，确认当前阶段和行为边界。

---

## 当前系统状态

<!-- 状态变更时更新以下字段和行为边界 -->

| 字段 | 值 |
|------|-----|
| **当前阶段** | `INIT` |
| **设计评估** | — |

### 当前阶段行为边界

<!-- 根据当前阶段，替换为对应阶段的行为边界。各阶段模板见下方。 -->

**允许：**
- 创建目录结构
- 创建 AGENTS.md / CONTRIBUTING.md / CHANGELOG.md
- 初始化 Git
- 初始化 CI 配置

**禁止：**
- 编写 Vision / Design / ADR / Plan
- 编写业务代码（src/）

---

## 设计评估

<!-- 仅在 DESIGN 阶段填写。评估设计是否完备到可以进入 DEVELOP。 -->

**设计评估** 字段取值：
- `完备` — 四类契约全部冻结，AC 覆盖所有已知场景，可进入 DEVELOP
- `基本完备` — 核心 AC 已冻结，部分边缘场景标注为"Agent 判定"，可进入 DEVELOP 但需在 Report 中关注
- `不完备` — 关键 AC 缺失或模糊，需继续完善 DESIGN

---

## 各阶段行为边界模板

<!-- 状态变更时，将对应模板复制到上方「当前阶段行为边界」段 -->

### INIT

**允许：** 创建目录结构、标准文件、初始化 Git/CI
**禁止：** 编写 Vision/Design/ADR/Plan、编写代码

### DESIGN

**允许：** 编写 Vision → Design Spec → ADR → API 契约 → 拆解 Plan
**禁止：** 编写代码（src/）、执行 Plan

### DEVELOP

**允许：** 创建 Plan、执行 Plan（编码/测试）、更新 Plan/Report 状态
**禁止：** 修改 Vision/Design/ADR 的内容或 status、在没有 Plan 的情况下直接写代码

### INTEGRATE

**允许：** 执行全量测试、修复集成问题
**禁止：** 新增功能代码、修改 Design/ADR

### PRE_RELEASE

**允许：** 环境检查、版本号确认、回滚方案验证
**禁止：** 修改代码和文档

### RELEASE

**允许：** 版本归档、CHANGELOG 整理、迭代复盘
**禁止：** 修改任何代码

---

## 子目录

| 路径 | 用途 |
|------|------|
| [vision.md](vision.md) | 全局顶层愿景 |
| [design/](design/) | Design Spec 规格文档（唯一业务事实源） |
| [adr/](adr/) | 架构决策记录 |
| [plans/](plans/) | 任务执行计划 |