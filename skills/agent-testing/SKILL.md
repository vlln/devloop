---
name: agent-testing
description: 可伸缩的多层测试体系。当 Agent 需要搭建测试基础设施、编写测试用例、执行分层测试、或绑定 AC 到测试用例时使用。独立于 agent-docs，可单独安装。
---

# Agent Testing System

## 系统概览

测试从最内层向外逐层叠加。每层都是合并闸门，不可跳过。

**低层机器化**（单元/接口/契约测试 — 机器可执行）→ **高层智能化**（E2E 语义验证 — Agent 判定）。

## 第一步：确定你的任务

| 你的任务 | 去读 |
|----------|------|
| 搭建测试基础设施（DEVELOP 轨道 C） | [references/testing-infra.md](references/testing-infra.md) |
| 编码 + 自测（DEVELOP 轨道 A/B） | [references/testing-dev.md](references/testing-dev.md) |
| 全量集成测试（INTEGRATE 阶段） | [references/testing-integrate.md](references/testing-integrate.md) |

## 第二步：需要详细规则时

| 问题 | 去读 |
|------|------|
| 我的项目需要哪些测试层？ | [references/test-layers.md](references/test-layers.md) |
| 如何把 AC 变成测试用例？ | [references/ac-binding.md](references/ac-binding.md) |

## 关键规则

1. 测试基础设施先于编码完成（轨道 C 优先）
2. 每层都是闸门，从内向外逐层执行，不可跳过
3. AC 必须绑定测试用例（命名: AC-00X-xxx.test.ts）
4. 测试输出摘要化（只输出通过/失败数、失败用例名、失败断言）
5. 测试层级按项目类型伸缩（不是所有项目都需要全部 6 层）