# 系统生命周期状态机

6 个状态，1 个内部循环（`DEVELOP ↔ INTEGRATE` 修复循环）。

```
INIT ──→ DESIGN ──→ DEVELOP ──→ INTEGRATE ──→ PRE_RELEASE ──→ RELEASE
            ↑          │  ↑                      │
            │          │  └──────────────────────┘
            │          │        (缺陷修复循环)
            │          │
            └──────────┘
         (架构变更回退)

RELEASE → DESIGN  (新一轮迭代)
```

## 流转刚性规则

- 禁止跳跃（如 INIT → DEVELOP）
- 禁止回跳（除 DEVELOP↔INTEGRATE 修复循环和 DESIGN 回退）
- 架构变更强制退回 DESIGN
- 局部 bug 在 DEVELOP↔INTEGRATE 修复循环内解决

---

## INIT — 项目初始化

- **允许**: 创建目录结构、标准文件、初始化 Git/CI
- **禁止**: 编写 Vision/Design/ADR/Plan、编写代码
- **→ DESIGN**: 目录结构就位、标准文件已创建、Git 已初始化

## DESIGN — 规划设计

- **允许**: 编写 Vision→Design Spec→ADR→API 契约→拆解 Plan
- **禁止**: 编写代码、执行 Plan
- **→ DEVELOP**: 四类契约已冻结（status=active）、Plan 已拆解完成
- **回退**: 架构不可行 → 退回 DESIGN 自身

### DESIGN 内部因果链

```
Vision → Design Spec → ADR → API 契约定义 → Plan 拆解
  │                    │
  │                    └──→ 测试用例设计（AC 定稿后可并行）
  │
  └── 一次性定稿，几乎不修改
```

## DEVELOP — 编码开发（最高并行期）

- **允许**: 领取任务、编写代码、单元测试、更新 Plan/Report
- **禁止**: 修改 Vision/Design/ADR、修改全局契约
- **→ INTEGRATE**: 全部并行轨道 Plan done

### DEVELOP 内部 4 条并行轨道

```
DESIGN（契约冻结）
  ├─ 轨道 A: 后端开发     (依赖: 接口契约 + 数据模型)
  ├─ 轨道 B: 前端开发     (依赖: API Mock + UI 约束)
  ├─ 轨道 C: 测试基础设施  (依赖: AC + 架构契约, 先于 A/B 完成)
  └─ 轨道 D: 数据库/部署  (依赖: 数据模型 + 架构契约)
```

- 每条轨道 = 独立 Plan 文件夹 + 独立 Git branch
- 轨道 C 最先完成，作为 A/B 的质量闸门
- 隔离: 独立 Git branch（并行场景使用 worktree 优化）

## INTEGRATE — 集成校验（唯一串行关口）

- **允许**: 执行全量测试、修复集成问题
- **禁止**: 新增功能代码、修改 Design/ADR
- **→ PRE_RELEASE**: 全部测试层通过

### 修复循环

```
INTEGRATE（全量测试）
  ├─ 全部通过 → PRE_RELEASE
  └─ 失败 → 退回 DEVELOP 对应轨道修复 → 再测 → INTEGRATE
```
局部 bug 在循环内修复；设计缺陷 → 退回 DESIGN。

## PRE_RELEASE — 预发布验证

- **允许**: 环境检查、版本号确认、回滚方案验证
- **禁止**: 修改代码和文档
- **→ RELEASE**: 预发布验证通过

## RELEASE — 迭代闭环

- **允许**: 版本归档、CHANGELOG 整理、复盘
- **禁止**: 修改任何代码
- **→ DESIGN**: 新一轮迭代启动