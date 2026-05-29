# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

「武侠·自由人生」当前重构为一个低武侠、养生向的小镇生活 demo。目标是先做出清风镇最小可玩闭环，而不是维护完整大世界设计。

## Single Source Of Truth

`data/` 是项目唯一事实源。

- `data/docs/`：项目目标、设计规范、系统规则、技术契约和验收标准。
- `data/game-runtime/`：Godot 运行时需要读取或打包的世界观文本、JSON 数据和素材清单。

旧的 `docs/`、`game-data/` 和 OpenSpec 变更稿不再作为当前规范使用。新增或修改内容前，先阅读 `data/docs/index.md`。

`.claude/skills/` 中的旧内容写作 skill 本轮暂不迁移。迁移前，如 skill 内容与 `data/` 冲突，一律以 `data/` 为准。

## Current Demo

第一版 demo 只做：

- 清风镇单地图。
- 3 个 NPC。
- 1 个采草药任务。
- 3 个基础物品。
- 最小时段推进。
- 背包和铜钱反馈。

明确不做：门派、战斗、声望、复杂经营、隐藏武功、大地图旅行、深度季节天气、多结局。

## Data Rules

- 运行时 JSON 遵守 `data/docs/04-tech/data-contract.md`。
- demo 范围以 `data/docs/00-project/demo-scope.md` 为准。
- 验收以 `data/docs/05-production/demo-acceptance.md` 为准。
- 所有运行时 JSON 一对象一文件，用稳定 `id` 互相引用。
- 不通过旧 OpenSpec 变更稿定义当前项目范围。

## Tech Stack

Godot 4.x + GDScript + JSON 数据驱动。

## 文件同步

本文件与 `AGENTS.md` 内容保持一致。修改本文件时，必须同步更新 `AGENTS.md` 的对应部分；反之亦然。两者的 Project Overview、Single Source Of Truth、Current Demo、Data Rules、Tech Stack 段落应始终相同。
