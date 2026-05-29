# Data Contract

本文件是 `data/game-runtime/` 中运行时 JSON 的唯一字段规范。Godot 加载器、内容生产和人工校验都以本文件为准。

## 通用规则

- 每个 JSON 文件只定义一个对象。
- 每个对象必须有 `id`、`name`、`type`。
- 字段名使用 snake_case。
- 跨文件引用只使用 `id`。
- 中文展示文本可以放在 runtime JSON 中。
- 规则说明放在 `data/docs/`，不要复制到 runtime JSON。
- demo 阶段不做复杂条件表达式、多语言、嵌套剧情脚本。
- runtime JSON 不允许出现本文件未定义的字段；如确需新增字段，必须先更新本文件。

## 类型

| type | 目录 | 用途 |
| --- | --- | --- |
| `map` | `maps/` | 地图、地点和连接 |
| `npc` | `npcs/` | NPC 基础信息 |
| `dialogue` | `dialogues/` | 对话节点 |
| `quest` | `quests/` | 任务目标和奖励 |
| `item` | `items/` | 物品定义 |
| `player_state` | `player/` | 初始玩家状态 |
| `rule` | `rules/` | 全局规则 |
| `asset_manifest` | `assets-manifest/` | 素材清单 |

## map

必需字段：

- `id`：地图 id。
- `name`：展示名称。
- `type`：固定为 `map`。
- `map_type`：地图类型，demo 当前使用 `town`。
- `description`：地图展示描述。
- `locations`：地点列表。
- `connections`：地点连接列表。
- `spawn_points`：出生点列表。

`locations[]` 必需字段：

- `id`：地点 id。
- `name`：地点展示名称。
- `kind`：地点类型，例如 `road`、`street`、`shop`、`inn`、`wilderness`。
- `description`：地点展示描述。

`connections[]` 必需字段：

- `from`：起点地点 id。
- `to`：终点地点 id。

`spawn_points[]` 必需字段：

- `id`：出生点 id。
- `location_id`：出生点所在地点 id。
- `description`：出生点说明。

示例：

```json
{
  "id": "map_qingfeng_town",
  "name": "清风镇",
  "type": "map",
  "map_type": "town",
  "description": "江南与中原交界的小镇，青石街贯穿南北。",
  "locations": [
    {
      "id": "loc_town_gate",
      "name": "镇口",
      "kind": "road",
      "description": "一块旧木牌立在路边，写着清风镇三个字。"
    }
  ],
  "connections": [
    { "from": "loc_town_gate", "to": "loc_main_street" }
  ],
  "spawn_points": [
    {
      "id": "spawn_player_start",
      "location_id": "loc_town_gate",
      "description": "玩家初始进入点"
    }
  ]
}
```

## npc

必需字段：

- `id`：NPC id。
- `name`：展示名称。
- `type`：固定为 `npc`。
- `role`：角色身份，例如 `herbalist`、`innkeeper`、`guard`。
- `location_id`：默认所在地点 id。
- `description`：NPC 简短描述。
- `dialogue_ids`：可触发的对话 id 列表。
- `quest_ids`：关联任务 id 列表；没有任务时使用空数组。

示例：

```json
{
  "id": "npc_herbalist_lin",
  "name": "药师林",
  "type": "npc",
  "role": "herbalist",
  "location_id": "loc_herb_shop",
  "description": "林家药铺的药师，说话慢，做事细。",
  "dialogue_ids": ["dlg_herbalist_intro"],
  "quest_ids": ["quest_collect_herbs"]
}
```

## dialogue

必需字段：

- `id`：对话 id。
- `name`：对话名称，供调试和编辑识别。
- `type`：固定为 `dialogue`。
- `speaker_id`：默认说话 NPC id。
- `nodes`：对话节点列表。

`nodes[]` 必需字段：

- `id`：节点 id。
- `speaker_id`：该节点说话者 id。
- `text`：展示文本。
- `choices`：玩家选项列表；没有后续选项时使用空数组。

`choices[]` 必需字段：

- `text`：选项展示文本。
- `next_node_id`：下一个节点 id；为 `null` 时结束对话。

`choices[]` 可选字段：

- `effects`：选项触发的最小效果对象。

demo 阶段唯一支持的 `effects` 字段：

- `quest_start`：开始指定任务，值为 quest id。

示例：

```json
{
  "id": "dlg_herbalist_intro",
  "name": "药师林初见",
  "type": "dialogue",
  "speaker_id": "npc_herbalist_lin",
  "nodes": [
    {
      "id": "start",
      "speaker_id": "npc_herbalist_lin",
      "text": "来得正好。溪边常见的草药快用完了。",
      "choices": [
        {
          "text": "我这就去。",
          "next_node_id": null,
          "effects": {
            "quest_start": "quest_collect_herbs"
          }
        }
      ]
    }
  ]
}
```

## quest

必需字段：

- `id`：任务 id。
- `name`：短名称。
- `type`：固定为 `quest`。
- `title`：任务面板标题。
- `giver_id`：发布者 NPC id。
- `status_default`：默认状态，demo 当前使用 `available`。
- `description`：任务说明。
- `steps`：任务步骤列表。
- `rewards`：奖励对象。
- `completion_text`：完成后展示文本。

`steps[]` 必需字段：

- `id`：步骤 id。
- `objective_type`：目标类型，demo 当前使用 `collect`、`talk`。
- `target_id`：目标对象 id。
- `location_id`：目标地点 id。
- `required_count`：需要数量。
- `description`：任务面板中的步骤说明。

`rewards` 必需字段：

- `currency`：货币奖励对象。
- `items`：物品奖励列表；没有物品奖励时使用空数组。

`rewards.currency` 当前支持字段：

- `copper`：铜钱数量。

`rewards.items[]` 必需字段：

- `item_id`：奖励物品 id。
- `count`：奖励数量。

示例：

```json
{
  "id": "quest_collect_herbs",
  "name": "采回草药",
  "type": "quest",
  "title": "帮药师林采草药",
  "giver_id": "npc_herbalist_lin",
  "status_default": "available",
  "description": "药师林需要三份常见草药，溪边草坡可以采到。",
  "steps": [
    {
      "id": "step_collect_herbs",
      "objective_type": "collect",
      "target_id": "item_herb",
      "location_id": "loc_creek_grass_slope",
      "required_count": 3,
      "description": "在溪边草坡采集 3 份草药。"
    }
  ],
  "rewards": {
    "currency": {
      "copper": 20
    },
    "items": [
      {
        "item_id": "item_bun",
        "count": 1
      }
    ]
  },
  "completion_text": "药师林收下草药，递来二十文钱和一个馒头。"
}
```

## item

必需字段：

- `id`：物品 id。
- `name`：展示名称。
- `type`：固定为 `item`。
- `category`：物品分类，例如 `currency`、`quest_item`、`food`。
- `stackable`：是否可堆叠。
- `base_price`：基础价格，单位为文。
- `description`：物品描述。

示例：

```json
{
  "id": "item_bun",
  "name": "馒头",
  "type": "item",
  "category": "food",
  "stackable": true,
  "base_price": 2,
  "description": "清风客栈卖的白面馒头，顶饱。"
}
```

## player_state

必需字段：

- `id`：初始状态 id。
- `name`：展示名称。
- `type`：固定为 `player_state`。
- `location_id`：玩家初始地点 id。
- `time`：初始时间对象。
- `currency`：初始货币对象。
- `inventory`：初始背包列表。
- `quest_states`：任务状态表。
- `flags`：全局标记表。

`time` 必需字段：

- `day`：天数，从 1 开始。
- `time_of_day`：时段 id。

`currency` 当前支持字段：

- `copper`：铜钱数量。

`inventory[]` 必需字段：

- `item_id`：物品 id。
- `count`：数量。

`quest_states` 是对象，key 为 quest id，value 为任务状态。初始无任务状态时使用 `{}`。

`flags` 是对象，key 为 flag id，value 为布尔值或简单 JSON 值。初始无标记时使用 `{}`。

示例：

```json
{
  "id": "player_initial_state",
  "name": "玩家初始状态",
  "type": "player_state",
  "location_id": "loc_town_gate",
  "time": {
    "day": 1,
    "time_of_day": "morning"
  },
  "currency": {
    "copper": 10
  },
  "inventory": [],
  "quest_states": {},
  "flags": {}
}
```

## rule

必需字段：

- `id`：规则 id。
- `name`：规则名称。
- `type`：固定为 `rule`。
- `rule_type`：规则类型。

`rule_type: "time"` 支持字段：

- `time_periods`：时段列表，每项包含 `id`、`name`。
- `advance_actions`：推进时间的行动列表，每项包含 `action`、`location_id`、`advance_periods`。
- `default_time`：默认时间，包含 `day`、`time_of_day`。

`rule_type: "economy"` 支持字段：

- `currency`：货币定义，包含 `id`、`name`。
- `prices`：价格列表，每项包含 `item_id`、`buy_price`、`sell_price`。

示例：

```json
{
  "id": "rule_time",
  "name": "时间规则",
  "type": "rule",
  "rule_type": "time",
  "time_periods": [
    { "id": "morning", "name": "清晨" }
  ],
  "advance_actions": [
    {
      "action": "collect",
      "location_id": "loc_creek_grass_slope",
      "advance_periods": 1
    }
  ],
  "default_time": {
    "day": 1,
    "time_of_day": "morning"
  }
}
```

## asset_manifest

必需字段：

- `id`：素材清单 id。
- `name`：素材清单名称。
- `type`：固定为 `asset_manifest`。
- `assets`：素材需求列表。

`assets[]` 必需字段：

- `id`：素材 id。
- `kind`：素材类型。
- `description`：素材说明。

`assets` 可以先记录占位素材需求，不要求文件已经存在。

示例：

```json
{
  "id": "asset_manifest_demo",
  "name": "Demo 素材清单",
  "type": "asset_manifest",
  "assets": [
    {
      "id": "asset_player_placeholder",
      "kind": "character_sprite",
      "description": "玩家占位角色，等距像素风，站立和行走。"
    }
  ]
}
```
