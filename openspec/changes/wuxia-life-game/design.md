# 技术设计：武侠·自由人生

## Context

武侠·自由人生是一款养生向武侠模拟经营游戏。项目已完成前期设计（世界观、系统、数据模型），即将进入开发阶段。

当前已有设计文档：
- `docs/` — 系统设计（时间、战斗、经济、NPC、任务、声望）
- `game-data/` — 游戏内容（世界观、角色、物品、武功）
- `docs/data-model.md` — 数据结构定义

技术栈已决定：**Godot 4.x + GDScript**。

## Goals / Non-Goals

### Goals

- 完成清风镇 MVP，验证核心玩法循环
- 建立可扩展的项目架构，后续可扩展到多城镇
- 数据驱动设计：游戏内容（NPC/物品/任务）通过 JSON 配置，不硬编码
- 存档/读档功能完整可用

### Non-Goals

- 不做战斗场景/动画（MVP 阶段仅文字结果）
- 不做多城镇（只做清风镇）
- 不做复杂经营系统（开店为 P2）
- 不做 PVP、联机、付费系统

## Decisions

### D1：使用 Godot 4.x + GDScript

**选择理由**：
- GDScript 语法接近 Python，学习成本低
- 内置 TileMap2D 支持等距地图
- 内置 Control 节点系统，UI 开发效率高
- 一键导出 Windows/Mac/Linux 桌面端
- 开源免费，无授权问题

**替代方案**：
- Web (Phaser.js)：中文文本渲染弱，UI 开发效率低
- Python + Pygame：基础设施全要自己造
- Java + LibGDX：对这个体量太重

### D2：数据驱动架构

游戏内容通过 JSON 配置文件定义，代码只负责逻辑和渲染。

```
game-data/              ← JSON 配置（设计师/策划编辑）
├── items.json
├── skills.json
├── npcs/*.json
├── dialogues/*.json
├── quests/*.json
└── event-scripts/*.json

res://                   ← Godot 资源（代码和美术）
├── scenes/              ← 场景文件
├── scripts/             ← GDScript 脚本
├── ui/                  ← UI 场景
└── assets/              ← 美术素材
```

**理由**：
- 修改游戏内容不需要改代码
- AI 生成的内容（NPC/对话）可以直接放到 JSON
- 后续多人协作时，策划和程序可以并行

### D3：场景架构

```
Main (主场景)
├── World (世界场景)
│   ├── TileMap (等距地图)
│   ├── NPCs (NPC 节点容器)
│   └── Player (玩家角色)
│
├── UI (UI 层，CanvasLayer)
│   ├── HUD (顶部状态栏：时间/天气/金钱)
│   ├── DialoguePanel (对话面板)
│   ├── InventoryPanel (背包面板)
│   ├── CharacterPanel (角色属性面板)
│   ├── QuestPanel (任务面板)
│   ├── ShopPanel (交易面板)
│   ├── BattleResultPanel (战斗结果面板)
│   └── MenuPanel (菜单/存档)
│
└── Systems (系统节点，不可见)
    ├── TimeSystem (时间管理)
    ├── QuestSystem (任务管理)
    ├── ReputationSystem (声望管理)
    ├── EventBus (全局事件总线)
    └── SaveManager (存档管理)
```

### D4：事件总线模式

各系统之间通过全局 EventBus 通信，避免直接引用：

```
TimeSystem --[time_tick]--> HUD (更新时间显示)
TimeSystem --[season_changed]--> NPCManager (更新 NPC 日程)
TimeSystem --[weather_changed]--> TileMap (更新天气效果)
QuestSystem --[quest_completed]--> ReputationSystem (更新声望)
Player --[entered_area]--> EventSystem (检查随机事件)
```

### D5：存档方案

- 使用 Godot 的 `FileAccess` 读写 JSON
- 存档路径：`user://save-slot-N.json`
- 3 个存档槽位
- 存档时序列化所有动态数据（Player/WorldState/NPCInstance/QuestLog/Reputation）
- 读档时反序列化并注入各系统

### D6：等距地图方案

- 使用 Godot TileMap2D 的 Isometric 模式
- Tile 大小：64x32（标准等距比例）
- 地图编辑在 Godot 编辑器中完成
- 碰撞通过 TileMap 的物理层实现

## Risks / Trade-offs

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| GDScript 学习曲线 | 开发速度 | 语法接近 Python，1-2 周可上手 |
| Godot 4.x 等距地图文档较少 | 开发效率 | 参考社区示例，必要时看源码 |
| JSON 数据量大后加载慢 | 游戏体验 | 按需加载，不一次性全部读取 |
| AI 生成美术素材风格不一致 | 视觉效果 | 统一调色板，后期手动微调 |
| 内容量大导致烂尾 | 项目完成度 | 严格控制 MVP 范围 |

## Open Questions

- [ ] Godot 项目目录结构的具体命名
- [ ] UI 主题/样式的具体方案（像素风 UI 在 Godot 中的实现方式）
- [ ] NPC 寻路方案（简单网格 vs NavigationServer）
