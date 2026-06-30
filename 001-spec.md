
---
title: Design Spec 001 — vagent 插件
description: vagent Obsidian 插件的固化落地方案，定义业务需求、接口、数据模型、UI 约束和 AC 验收标准。
type: design
status: draft
version: 1
created: 2026-06-30T00:00:00Z
---

> vagent 规格文档。所有业务需求、接口、数据模型、AC 均在此定义。

---

## 一、项目概述

vagent 是 Obsidian 插件，基于 ACP（Agent Client Protocol）与外部 AI Agent 进程通信，在 Obsidian 内提供完整的 AI 对话体验。支持多 Agent（Claude Code、Codex、Gemini CLI、自定义 ACP Agent）、多会话管理、vault 上下文感知、流式消息渲染。

---

## 二、用户故事

| 编号 | 角色 | 需求 | 目的 | 优先级 |
|------|------|------|------|--------|
| US-001 | Obsidian 用户 | 在侧边栏与 AI Agent 对话 | 不离开 Obsidian 即可使用 AI 助手 | P0 |
| US-002 | Obsidian 用户 | Agent 自动感知当前活跃笔记 | 对话上下文自动包含当前工作内容 | P0 |
| US-003 | Obsidian 用户 | 管理多个会话（创建/恢复/删除） | 不同任务使用不同会话 | P0 |
| US-004 | Obsidian 用户 | 切换不同 Agent（Claude/Codex/Gemini） | 根据任务选择合适的 AI | P1 |
| US-005 | Obsidian 用户 | 导出对话为 Markdown 笔记 | 将对话保存为知识库的一部分 | P1 |
| US-006 | Obsidian 用户 | 浮动窗口模式 | 不占用侧边栏空间 | P1 |
| US-007 | Obsidian 用户 | @[[笔记]] 引用 | 手动指定特定笔记作为上下文 | P1 |

---

## 三、模块划分

| 模块 | 职责 | 优先级 |
|------|------|--------|
| ACP 通信层 | Agent 进程生命周期管理、JSON-RPC 通信、Session 管理 | P0 |
| 会话管理 | 会话创建/恢复/分叉/删除、会话文件 I/O | P0 |
| 消息处理 | 流式消息接收、类型转换、状态管理 | P0 |
| UI 聊天界面 | 侧边栏视图、消息列表、输入区域、工具栏 | P0 |
| Vault 集成 | 活跃笔记感知、@[[笔记]] 引用、笔记搜索 | P0 |
| 设置管理 | 插件配置、Agent 配置、API Key 管理 | P1 |
| 浮动窗口 | 浮动聊天窗口、拖拽/缩放 | P1 |
| 对话导出 | Markdown 导出、frontmatter 生成 | P1 |

---

## 四、接口定义

### ACP 通信层

#### `AcpClient` 类

```
class AcpClient {
  spawn(agentConfig): Promise<void>       // 启动 Agent 进程
  initialize(): Promise<void>             // 初始化 ACP 连接
  newSession(cwd?): Promise<void>         // 创建新会话
  sendPrompt(content): Promise<void>      // 发送用户消息
  cancel(): Promise<void>                 // 取消当前操作
  disconnect(): Promise<void>             // 断开连接，终止进程
  loadSession(sessionId): Promise<void>   // 加载历史会话
  resumeSession(sessionId): Promise<void> // 恢复会话
  forkSession(sessionId): Promise<void>   // 分叉会话
  onSessionUpdate: Set<Listener>          // 会话更新事件（单通道）
}
```

### 会话存储

#### `SessionStorage` 类

```
class SessionStorage {
  saveSession(info: SavedSessionInfo): Promise<void>
  getSavedSessions(agentId?, cwd?): SavedSessionInfo[]
  deleteSession(sessionId): Promise<void>
  saveSessionMessages(sessionId, agentId, messages): Promise<void>
  loadSessionMessages(sessionId): Promise<ChatMessage[] | null>
  deleteSessionMessages(sessionId): Promise<void>
}
```

### Vault 服务

#### `VaultService` 类

```
class VaultService {
  readNote(path: string): Promise<string>
  searchNotes(query: string): Promise<NoteMetadata[]>
  getActiveNote(): Promise<NoteMetadata | null>
  listNotes(): Promise<NoteMetadata[]>
}
```

---

## 五、数据模型

### ChatMessage

```typescript
interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: MessageContent[];
  timestamp: number;
  sessionId: string;
}

type MessageContent =
  | TextBlock
  | ToolCallBlock
  | ThinkingBlock
  | ImageBlock;
```

### ChatSession

```typescript
interface ChatSession {
  sessionId: string;
  agentId: string;
  cwd: string;
  title: string;
  createdAt: number;
  updatedAt: number;
  messageCount: number;
}
```

### SessionUpdate (12 种类型联合)

```typescript
type SessionUpdate =
  | AgentMessageChunk
  | AgentThoughtChunk
  | UserMessageChunk
  | ToolCall
  | ToolCallUpdate
  | Plan
  | AvailableCommandsUpdate
  | CurrentModeUpdate
  | SessionInfoUpdate
  | UsageUpdate
  | ConfigOptionUpdate
  | ProcessErrorUpdate;
```

### 会话文件格式 (JSONL)

```
{"type":"user","content":"请帮我分析这段代码","timestamp":1719000000000}
{"type":"assistant","content":"我来分析...","timestamp":1719000001000}
{"type":"tool_call","tool":"Read","input":{"file_path":"..."},"timestamp":1719000002000}
```

---

## 六、业务规则

| 规则编号 | 描述 | 触发条件 | 约束 |
|----------|------|----------|------|
| BR-001 | 每个 ChatView 有独立的 AcpClient 和 Session | 创建新视图 | 多视图互不干扰 |
| BR-002 | 会话消息流式更新通过 RAF 批处理 | 收到 Agent 消息块 | 每帧最多一次 UI 更新 |
| BR-003 | API Key 使用 Obsidian SecretStorage 存储 | 保存设置 | 不写入 data.json |
| BR-004 | 会话文件存储为 JSONL 格式 | 会话创建/更新 | 追加写入，不重写整个文件 |

---

## 七、UI 约束

### 页面结构

```
ChatView (侧边栏) / FloatingChatView (浮动窗口)
  └── ChatContextProvider (React Context)
        └── ChatPanel
              ├── ChatHeader (标题、Agent 选择器、操作按钮)
              ├── MessageList (虚拟滚动消息列表)
              │     └── MessageBubble (单条消息)
              │           ├── ToolCallBlock (工具调用渲染)
              │           ├── TerminalBlock (终端输出)
              │           └── MarkdownRenderer (Markdown 渲染)
              └── InputArea
                    ├── SuggestionPopup (@[[笔记]] 提示)
                    ├── AttachmentStrip (附件预览)
                    └── InputToolbar (模式/模型选择、发送按钮)
```

### 组件规范

- 使用 React 19 + TypeScript
- Hooks 层：`useAgent` 作为 facade，组合 `useAgentSession` + `useAgentMessages`
- Services 层：零 React 导入，纯业务逻辑
- 消息列表使用 `@tanstack/react-virtual` 虚拟滚动
- `MessageBubble`、`ToolCallBlock` 使用 `React.memo` 优化渲染

---

## 八、验收标准（AC）

### AC-001: 插件加载和基础 UI

- **前置条件**：Obsidian 已安装 vagent 插件
- **操作步骤**：
  1. 启用 vagent 插件
  2. 点击侧边栏图标或执行 "Open chat view" 命令
- **预期结果**：聊天视图出现在右侧面板，包含输入框和发送按钮
- **校验方式**：手动

### AC-002: Agent 连接和对话

- **前置条件**：已配置 Claude Code Agent 和 API Key
- **操作步骤**：
  1. 打开聊天视图
  2. 输入消息 "Hello"
  3. 点击发送
- **预期结果**：Agent 进程启动，返回响应消息，消息流式渲染
- **校验方式**：手动

### AC-003: 会话管理

- **前置条件**：已有至少一个会话历史
- **操作步骤**：
  1. 打开会话管理器
  2. 选择一个历史会话
  3. 点击恢复
- **预期结果**：历史消息加载并显示，可以继续对话
- **校验方式**：手动

### AC-004: Vault 上下文感知

- **前置条件**：vault 中有活跃笔记
- **操作步骤**：
  1. 打开一个笔记
  2. 打开聊天视图
  3. 发送消息
- **预期结果**：Agent 收到的消息中包含当前活跃笔记的引用
- **校验方式**：手动

### AC-005: @[[笔记]] 引用

- **前置条件**：vault 中有笔记
- **操作步骤**：
  1. 在输入框输入 `@`
  2. 输入笔记名称关键字
- **预期结果**：下拉菜单显示匹配的笔记，选择后插入 `@[[笔记名]]` 格式
- **校验方式**：手动

### AC-006: 对话导出

- **前置条件**：有一个已完成的对话
- **操作步骤**：
  1. 点击导出按钮
  2. 确认导出
- **预期结果**：对话以 Markdown 格式保存到 vault，包含 frontmatter
- **校验方式**：手动

### AC-007: 浮动窗口

- **前置条件**：已启用浮动窗口功能
- **操作步骤**：
  1. 执行 "Open floating chat view" 命令
- **预期结果**：浮动窗口出现，可拖拽移动，可正常对话
- **校验方式**：手动

---

## 九、非功能约束

> 继承自 [Vision](../vision.md)，此处仅补充本 Design 特有的约束。

| 维度 | 约束 |
|------|------|
| 性能 | 消息列表虚拟滚动，支持 1000+ 条消息不卡顿 |
| 安全 | API Key 仅存 SecretStorage，日志中不输出 |
| 国际化 | 至少支持 zh-CN 和 en，使用 Obsidian 语言设置 |

---

## 十、依赖项

| 依赖 | 版本 | 用途 |
|------|------|------|
| @agentclientprotocol/sdk | latest | ACP 协议 SDK |
| react | ^19.0.0 | UI 框架 |
| react-dom | ^19.0.0 | React DOM 渲染 |
| @tanstack/react-virtual | latest | 虚拟滚动 |
| obsidian | ^1.8.7 | Obsidian API |
| typescript | ^5.0.0 | 类型检查 |

---

## 十一、术语表

| 术语 | 定义 |
|------|------|
| ACP | Agent Client Protocol，AI Agent 与客户端通信的 JSON-RPC 标准协议 |
| Agent | 外部 AI 进程（如 Claude Code、Codex），通过 ACP 与插件通信 |
| Session | 一次对话会话，有独立的 sessionId 和消息历史 |
| Vault | Obsidian 的知识库，包含所有笔记和附件 |
| SecretStorage | Obsidian 提供的安全存储 API，用于存储 API Key 等敏感信息 |
| RAF | requestAnimationFrame，用于批处理流式更新 |
