> 本文档遵循 GitHub 标准 Contributing Guide 结构。
> Agent 启动前必须完整读取，所有编码产出必须遵守本文件约束。

---

## 一、Code of Conduct

<!-- 项目行为准则，可引用 Contributor Covenant -->

---

## 二、Types of Contributions

- 代码贡献（feat / fix / refactor）
- 文档贡献（docs）
- 测试贡献（test）
- 问题反馈（Bug Report / Feature Request）

---

## 三、Before You Start

### Report Bugs

<!-- 使用 GitHub Issues，模板 -->

### Feature Requests

<!-- 先检查 docs/vision.md 和 docs/design/ 确认是否在规划内 -->

---

## 四、Setup Dev Environment

<!-- 克隆、安装依赖、启动开发服务器 -->

```bash
git clone <repo-url>
cd <project>
npm install
npm run dev
```

---

## 五、Pull Request Workflow

### 1. Fork & Branch

- `main`：生产分支，受保护
- `develop`：开发分支
- `feature/xxx`：功能分支
- `fix/xxx`：修复分支

### 2. Code Style & Lint

- 语言：TypeScript（严格模式）
- 格式化：Prettier（2 空格缩进，单引号，无分号）
- 命名：
  - 文件：kebab-case（`user-service.ts`）
  - 变量/函数：camelCase
  - 类/接口：PascalCase
  - 常量：UPPER_SNAKE_CASE

### 3. Commit Rules

```
<type>(<scope>): <简短描述>
```

| type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档变更（必须独立提交，不与代码混合） |
| refactor | 重构 |
| test | 测试相关 |
| chore | 构建/工具/依赖 |

### 4. Test

测试体系按项目类型可伸缩。提交前必须通过对应项目类型所要求的测试层。

**测试命令：**（根据项目实际配置修改）

| 命令 | 用途 |
|------|------|
| `npm run test:unit` | 单元测试 |
| `npm run test:integration` | 集成测试 |
| `npm run test:e2e` | E2E 测试 |

**检查清单：**
- [ ] 类型检查通过（`tsc --noEmit`）
- [ ] Lint 通过（`eslint`）
- [ ] 单元测试通过
- [ ] 无 console.log 残留

### 5. Open PR

<!-- PR 描述模板、Review 流程 -->

---

## 六、Docs Contribution

### 文档体系

项目文档遵循 AGENTS.md 中定义的结构。文档命名、frontmatter、status 等系统规则见 skill 的「系统规则」段。

### 文档 Commit

- 文档修改必须独立 Commit，不与代码混合
- 格式：`docs(<scope>): <简述>`

---

## 七、License & CLA

<!-- 项目许可证和贡献者协议 -->

---

## 八、Get Help

<!-- 联系方式、讨论渠道 -->