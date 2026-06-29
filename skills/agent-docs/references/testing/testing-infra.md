# 测试基础设施搭建（DEVELOP 轨道 C）

你是轨道 C 的 Executor。你的产出是测试武器，必须在轨道 A/B 开始编码前完成。

## 1. 确定测试层级

读取 active Design Spec，提取所有 AC。然后打开 [test-layers.md](test-layers.md)，确定项目类型需要的测试层级。

## 2. 搭建骨架

```bash
mkdir -p tests/unit tests/integration tests/e2e
```

## 3. 安装框架

根据项目类型选择：

| 项目类型 | 安装命令 |
|----------|----------|
| 任何项目 | `npm install -D vitest` |
| API 项目 | `npm install -D vitest` |
| 前端/全栈 | `npm install -D vitest @playwright/test` |

## 4. 配置测试脚本

在 `package.json` 中添加粒度化命令（每个测试层一个）：

```json
{
  "scripts": {
    "test:unit": "vitest run tests/unit",
    "test:integration": "vitest run tests/integration",
    "test:contract": "vitest run tests/contract",
    "test:orchestration": "vitest run tests/orchestration",
    "test:e2e": "playwright test",
    "test:e2e:feature:login": "playwright test tests/e2e/login.spec.js",
    "test:visual": "playwright test tests/visual"
  }
}
```

## 5. 准备测试资源

```
- 测试账号和权限
- 测试数据（seed 脚本）
- 环境变量（.env.test）
- Mock 服务配置（如果需要）
```

## 6. 编写测试用例骨架

对每条机器可验证的 AC，创建骨架文件：

```
tests/unit/AC-001-xxx.test.ts
tests/integration/AC-005-xxx.test.ts
tests/e2e/AC-010-xxx.spec.js
```

命名规则见 [ac-binding.md](ac-binding.md)。

对机器不可验证的 AC，在测试清单中标注"Agent 判定"。

## 7. 验证

```bash
npm run test:unit
```

确认所有脚本可运行（即使测试用例为空，框架能正常启动即可）。

## 8. 提交

```bash
git add tests/
git commit -m "test(infra): 搭建测试基础设施"
```

## 输出

- 测试目录结构
- 测试框架已安装
- package.json 测试脚本已配置
- 测试用例骨架文件
- 测试资源就绪（账号、数据、环境变量）