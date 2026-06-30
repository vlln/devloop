# 测试基础设施 Plan（DEVELOP 轨道 C）

当你在 DEVELOP 阶段创建测试基础设施的 Plan 时，参考以下内容编写 Plan 文件。

## Plan 的「分步计划」应包含

### 1. 确定测试层级

根据项目类型确定需要的测试层：

| 项目类型 | 需要的测试层 |
|----------|-------------|
| 纯 CLI / 脚本 | 单元 → 集成 |
| 后端 API | 单元 → 集成 → 接口契约 → 接口编排 |
| 全栈 Web | 单元 → 集成 → 接口契约 → 接口编排 → E2E → 视觉回归 |
| 前端组件库 | 单元 → 组件测试 → 视觉回归 |

### 2. 搭建骨架

```bash
mkdir -p tests/unit tests/integration tests/e2e
```

### 3. 安装框架

| 项目类型 | 安装命令 |
|----------|----------|
| 任何项目 | `npm install -D vitest` |
| 前端/全栈 | `npm install -D vitest @playwright/test` |

### 4. 配置测试脚本

```json
{
  "scripts": {
    "test:unit": "vitest run tests/unit",
    "test:integration": "vitest run tests/integration",
    "test:e2e": "playwright test"
  }
}
```

### 5. 准备测试资源

- 测试账号和权限
- 测试数据（seed 脚本）
- 环境变量（`.env.test`）

### 6. 编写测试用例骨架

读取 active Design Spec，对每条机器可验证的 AC 创建骨架文件。命名: `AC-00X-简短描述.test.ts`。

对机器不可验证的 AC，在测试清单中标注"Agent 判定"。

### 7. 验证

```bash
npm run test:unit
```

## Plan 的「执行边界」应包含

```markdown
## 执行边界

**你必须做：**
- 搭建测试目录结构，安装测试框架
- 配置 package.json 测试脚本
- 为每条机器可验证的 AC 创建测试用例骨架
- 确认所有脚本可运行

**你必须不做：**
- 不编写业务代码
- 不修改 Design Spec 或 ADR
- 不推进系统状态
```