# Save Format

## 存档目标

demo 存档只保存运行中会变化的状态，不复制静态 runtime 数据。

## 建议路径

Godot 使用：

```text
user://saves/demo_slot_1.json
```

## 结构

```json
{
  "version": 1,
  "player": {
    "location_id": "loc_town_gate",
    "time": {
      "day": 1,
      "time_of_day": "morning"
    },
    "currency": {
      "copper": 30
    },
    "inventory": [
      { "item_id": "item_bun", "count": 1 }
    ],
    "quest_states": {}
  },
  "flags": {}
}
```

## 约束

- 存档不保存 NPC 模板、地图模板、物品模板。
- 存档不做复杂迁移；版本号先保留。
- demo 阶段只需要一个存档槽。

