## 一、项目简介

<!-- 由项目维护者更新。简要描述本项目：做什么、解决什么问题、技术栈 -->

---

## 二、项目形态档案

<!-- INIT 阶段填写，经用户确认。决定部署类门禁如何实例化，一经落盘，各阶段照档执行，不得临时裁量（见 devloop「门禁不可跳过，但可实例化」）。形态变化时在增量迭代的 DESIGN 中修订，经用户确认 -->

| 项 | 值 |
|----|----|
| 项目形态 | <!-- 服务型 / 发布型 / 本地型 --> |
| 部署类门禁实例化 | <!-- 按形态填写：服务型=全量；发布型=staging 为 dry-run/测试源发布、production 为正式 publish、冒烟为安装制品验证；本地型=豁免部署，RELEASE 退化为打 tag + CHANGELOG --> |
| 不可委托门禁豁免 | <!-- 默认「无」。如豁免（全自动发布场景），逐条列出并标注风险警告 --> |

---

## 三、文档体系

### 文档类型

| 文档 | 用途 |
|------|------|
| 本文档（AGENTS.md） | 项目入口地图 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 编码/Commit/文档/测试规范 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录（Keep a Changelog） |
| [docs/vision.md](docs/vision.md) | 全局顶层愿景：业务目标、用户范围、长期理想形态（有 frontmatter） |
| [docs/spec/](docs/spec/) | Spec：需求规格。用户故事、模块划分、数据模型、术语表 |
| [docs/interface/](docs/interface/) | 接口定义：入参/出参/错误码。适用有 API 时 |
| [docs/ac/](docs/ac/) | 验收标准（AC）：正常/边界/异常/失败四场景。测试唯一权威依据 |
| [docs/adr/](docs/adr/) | 架构决策记录：技术选型、方案对比、取舍 |
| [docs/plans/](docs/plans/) | 执行容器：对应一个 Git 分支，内含多个最小执行单元（Plan + Report 成对） |
| [docs/backlog.md](docs/backlog.md) | 工程需求池：DESIGN 迭代候选的唯一来源（无 frontmatter） |
| [docs/README.md](docs/README.md) | 子目录索引 + **当前系统状态** |
| 各级 README.md | 该目录的索引和状态说明 |

### 文档目录结构

```
项目根目录
├── AGENTS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── docs/
│   ├── README.md          # 索引 + 当前系统状态
│   ├── vision.md
│   ├── spec/
│   │   ├── README.md
│   │   └── 0001-template.md
│   ├── interface/
│   │   ├── README.md
│   │   └── 0001-template.md
│   ├── ac/
│   │   ├── README.md
│   │   └── 0001-xxx.md
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

