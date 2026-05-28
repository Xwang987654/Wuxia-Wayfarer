# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

武侠·自由人生 — 一款养生向武侠模拟经营游戏。2.5D斜俯视像素风，强调自由度、NPC互动与多路线人生体验。

**当前状态**：文档驱动开发阶段，尚无代码。

## 开发方式

本项目采用**文档驱动开发**。设计文档在 `docs/`，游戏内容在 `game-data/`。实现任何功能前，先阅读对应的设计文档和内容设定。

## 文档体系

### docs/ — 开发/设计文档

```
docs/
├── vision.md              # 愿景与目标
├── game-design.md         # 游戏设计总纲（GDD）
├── art-bible.md           # 美术圣经
├── technical-design.md    # 技术架构设计
├── data-model.md          # 数据模型（存档结构/模板定义）
│
├── systems/               # 系统设计文档
│   ├── time-system.md
│   ├── combat-system.md
│   ├── economy-system.md
│   ├── npc-system.md
│   ├── quest-system.md
│   └── reputation-system.md
│
└── milestones/
    └── mvp.md
```

### game-data/ — 游戏内容（世界观/角色/物品/事件）

```
game-data/
├── lore/                  # 世界观设定
│   ├── world-background.md
│   ├── martial-arts.md
│   ├── factions.md
│   └── qingfeng-town.md
├── world-map.md           # 地图设定
├── characters.md          # 角色/NPC设定
├── items.md               # 物品/道具
├── skills.md              # 武功/技能
├── events.md              # 事件/剧情
│
├── npcs/                  # NPC 数据（JSON，Godot 加载）
├── dialogues/             # 对话数据（JSON）
├── quests/                # 任务数据（JSON）
└── event-scripts/         # 事件脚本（JSON）
```

### 文档依赖关系

```
vision.md ──▶ game-design.md ──▶ systems/*.md
                   │                   │
                   ├──▶ art-bible.md   ├──▶ game-data/*.md
                   │         │         │
                   │         └─────────┴──▶ data-model.md
                   │                           │
                   └──▶ technical-design.md     │
                           │                   │
                           └───── milestones/mvp.md
```

- `docs/`：设计文档（怎么做、为什么做）
- `game-data/`：游戏内容（做什么、有什么）
- `data-model.md`：连接两者的桥梁，定义数据结构

## 数据模型关键决策

- **模板与实例分离**：物品/NPC/武功的定义（静态模板）与运行时状态（动态实例）分开存储
- **扁平结构**：不使用 ECS，直接访问 `player.hp`、`world.season`
- **背包**：格子展示，无容量限制
- **全局标记**：使用灵活的 `flags: Record<string, any>`
- **存档格式**：JSON 文件，支持版本号和数据迁移

## Core Design Decisions

- **画风**：像素风 2.5D 等距视角，AI（Gemini/GPT）生成美术素材
- **战斗**：回合+自动混合，MVP阶段仅文字结果输出
- **时间**：1天=10分钟，日夜5时段，四季每6天切换，随机天气
- **经营**：低买高卖 + 简化开店 + 轻量制造
- **路线**：散人/门派/衙门/商人，可自由选择和切换
- **范围**：先做清风镇（MVP），后续扩展

## OpenSpec Workflow

本项目使用 OpenSpec 管理变更流程。当前变更：`wuxia-life-game`。

常用命令：
- `/opsx:propose` — 创建新变更提案
- `/opsx:apply` — 实施变更任务
- `/opsx:explore` — 探索模式

## Tech Stack

待定。候选：Web (Phaser.js/PixiJS)、Godot。详见 `docs/technical-design.md`。
