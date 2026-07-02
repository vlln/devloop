# devpact

契约驱动的项目开发系统 — 基于 6 阶段状态机的 Agent 自主编码框架。

This repository stores skills under `skills/`. Each skill follows the
[Agent Skills specification](https://agentskills.io/specification) and can be
used by skills-compatible agents.

## Skills

| Skill | Description |
|-------|-------------|
| [`devpact`](skills/devpact) | 契约驱动的项目开发系统。当 Agent 需要初始化项目、理解当前阶段能做什么、推进状态、创建和管理文档时使用。 |

## Quick Start

Paste this into your AI agent (Claude Code, Cursor, OpenAI Assistants, etc.):

```text
Install the Agent Skills from https://raw.githubusercontent.com/vlln/devpact/main/README.md
```

## Installation

Recommended: install these skills with
`skit`. It fetches skills from the published repository, records them in a local
manifest, and activates them for local agents.

### skit

Install `skit` with Homebrew:

```sh
brew install vlln/tap/skit
```

For other platforms, see the `skit` installation instructions.

Install one skill:

```sh
skit install vlln/devpact/skills/devpact
```

Install all skills in this repository:

```sh
skit install vlln/devpact --all
```

### npx skills

```sh
npx skills add vlln/devpact
```

### Manual

Copy the desired skill directory from `skills/<skill-name>` into your agent's
skills directory, then restart the agent if required.

Common locations:

- Codex CLI: `~/.codex/skills`
- Claude Code: `.claude/skills` in the project, or the configured user skills directory
- OpenCode: `~/.opencode/skills/<repo-name>`

## Requirements

- `skit` CLI for install and validation workflows.

## License

MIT