> Agent 启动后首先读取本文档。读完你应该知道：这是什么项目、文档在哪、当前处于什么状态。

---

## 一、项目简介

<!-- 简要描述本项目：做什么、解决什么问题、技术栈 -->

---

## 二、文档体系

### 文档类型

| 文档 | 用途 |
|------|------|
| 本文档（AGENTS.md） | 项目入口地图 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 编码/Commit/文档/测试规范 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录（Keep a Changelog） |
| [docs/arch/vision.md](docs/arch/vision.md) | 全局顶层愿景：业务目标、用户范围、顶层约束（有 frontmatter） |
| [docs/arch/design/](docs/arch/design/) | Design Spec：固化方案 + AC。唯一业务事实源 |
| [docs/arch/adr/](docs/arch/adr/) | 架构决策记录：技术选型、方案对比、取舍 |
| [docs/arch/plans/](docs/arch/plans/) | 单次执行容器：Plan + Report 成对 |
| [docs/arch/README.md](docs/arch/README.md) | 子目录索引 + **当前系统状态** |
| 各级 README.md | 该目录的索引和状态说明 |

### 目录结构

```
项目根目录
├── AGENTS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── docs/arch/
│   ├── README.md          # 索引 + 当前系统状态
│   ├── vision.md
│   ├── design/
│   │   ├── README.md
│   │   └── 001-template.md
│   ├── adr/
│   │   ├── README.md
│   │   └── 0001-xxx.md
│   └── plans/
│       ├── README.md
│       └── 0001-任务名/
│           ├── README.md
│           ├── 01-plan-xxx.md
│           ├── 01-report-xxx.md
│           └── artifacts/
├── src/
└── .github/workflows/
```

---

## 三、文档导航

| 要找什么 | 去哪里 |
|----------|--------|
| **当前系统状态 + 行为边界** | [docs/arch/README.md](docs/arch/README.md)（首先读取！） |
| 项目目标、架构约束、硬性规则 | [docs/arch/vision.md](docs/arch/vision.md) |
| 功能规格、接口、数据模型、AC 验收标准 | [docs/arch/design/](docs/arch/design/)（找 active 版本） |
| 技术选型理由、架构决策 | [docs/arch/adr/](docs/arch/adr/) |
| 当前任务进度 | [docs/arch/plans/README.md](docs/arch/plans/README.md) |
| Plan/Report 模板 | [docs/arch/plans/0001-template/](docs/arch/plans/0001-template/) |
| 编码规范、Git 规则、文档写作规范 | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 版本变更记录 | [CHANGELOG.md](CHANGELOG.md) |