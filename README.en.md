<div align="center">

# devloop

An installable professional software lifecycle for agents and people: documented, traceable, parallel and collaborative work, from project inception to acceptance, delivery and repeated improvement.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-spec-6e3af2)](https://agentskills.io/specification)

[中文](<README.md>)

</div>

## Who it is for

Long-running software projects that need continuity across sessions, collaboration, change management and credible acceptance and delivery. devloop does not prescribe every coding step or measure professionalism by document or approval counts.

## What it provides

- **A complete lifecycle**: inception → requirements and architecture → engineering readiness → implementation and integration → acceptance → delivery, feedback and further iterations.
- **Project continuity**: track projects, deliveries and work units separately; design for the next version can coexist with acceptance of the current one.
- **Change management**: questions do not automatically become implementation commitments; explain the impact of additions and update scope, plans and evidence after a clear direction change.
- **Flexible, bounded decisions**: reuse valid conversational decisions and conditional permissions, asking only about gaps; endorsing a design does not authorize production operations.
- **Collaborative documentation**: coherent current specifications with traceable history, appropriate abstraction and explicit integration responsibility for shared documents.
- **Recoverable work**: preserve ownership, dependencies, workspace, verified results and next actions; interruption does not automatically discard a worktree.
- **Proactive engineering choices**: activate judgment at work, change, integration and stopping boundaries, with defaults for isolation, risk experiments, regression evidence and self-checks instead of waiting for itemized user reminders.
- **Delivery evidence**: validate what consumers actually use, distinguishing implementation, tests, acceptance, delivery and operational health.

Keep professional lifecycle gates while tailoring methods to risk and project facts. Existing tools and branch strategies take precedence; Gitflow is not mandatory.

## Installation

### skit

```sh
brew install vlln/tap/skit
skit install vlln/devloop/skills/devloop
```

### npx skills

```sh
npx skills add vlln/devloop
```

### Manual

Copy the [skill directory](<skills/devloop/>) into your agent's skills directory and reload as required by the host. Installation tools are optional; skit is not a runtime dependency.

Remote installation fetches published repository content, not unpublished local changes. Existing projects are not migrated automatically.

## Getting started

Give the agent your project goal and ask it to adopt devloop and advance the project. For an existing project, it first inspects established rules, ongoing work and evidence, then integrates incrementally instead of overwriting the layout or inventing historical decisions.

Use it to take over work, assess new requests, coordinate parallel work, maintain specifications or prepare acceptance and delivery. Users do not need to fill out a complete template set in advance.

## Skills

| Skill | Purpose |
|---|---|
| [devloop](<skills/devloop/SKILL.md>) | Professional software lifecycle, cross-session continuity, collaboration, changing requirements and repeated delivery |

## Development and validation

- [Design](<docs/design.md>): boundaries and rationale.
- [Redesign records](<docs/redesign/README.md>): candidate design and implementation history.
- [Isolated validation](<docs/redesign/validation/README.md>): evidence and limits of local delivery, cross-session changes and boundary experiments.
- [Backlog](<docs/backlog.md>): follow-up work for this repository.

## License

MIT
