# Demo Acceptance

## 文档验收

- `data/docs/index.md` 的目录树与实际文件一致。
- `data/game-runtime/index.md` 的目录树与实际文件一致。
- demo 范围没有承诺门派、战斗、声望、复杂经营、大地图。
- 技术栈统一为 Godot 4.x + GDScript + JSON。
- 数据契约只指向 `data/game-runtime/`。

## 数据验收

- 每个 runtime JSON 文件只包含一个对象。
- 每个对象都有 `id`、`name`、`type`。
- 所有跨文件引用能找到目标对象。
- 没有聚合式 `items.json`、`npcs.json`。
- 初始状态、地图、NPC、对话、任务、物品可以组成完整任务闭环。

## 玩法验收

- 玩家从镇口开始。
- 玩家可以去林家药铺、清风客栈、溪边草坡。
- 玩家可以与药师林、周掌柜、赵守卫对话。
- 玩家可以接取并完成采草药任务。
- 完成后获得 20 文铜钱和 1 个馒头。
- 采集草药会推进至少 1 个时段。

