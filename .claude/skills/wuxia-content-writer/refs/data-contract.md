# 数据契约

本文件是项目数据字段、枚举、JSON 结构的唯一权威定义。所有 JSON 数据文件、skill 模板、data-model.md 必须与此一致。

---

## 字段命名规范

所有 JSON 数据文件的字段名使用 **snake_case**。

```
正确：shop_inventory, buy_preference, quest_ids, price, time_of_day
错误：shopInventory, buyPreference, questIds, priceCopper, timeOfDay
```

---

## 时间系统

### 时段（time_of_day）

使用字符串 key，不使用数字索引：

| key | 中文 | 大致对应 |
|-----|------|----------|
| `morning` | 清晨 | 卯时 |
| `noon` | 正午 | 午时 |
| `afternoon` | 午后 | 未时-申时 |
| `evening` | 黄昏 | 酉时-戌时 |
| `night` | 夜晚 | 亥时-寅时 |

### 季节（season）

`spring` | `summer` | `autumn` | `winter`

### 天气（weather）

`sunny` | `overcast` | `rain` | `heavy_rain` | `thunder` | `fog` | `wind` | `snow` | `heavy_snow` | `frost` | `scorching`

---

## 枚举值定义

### 物品类型（ItemTemplate.type）

`weapon` | `armor` | `shoes` | `medicine` | `material` | `food` | `book` | `quest_item` | `special`

### 物品品质（ItemTemplate.quality）

`normal` | `fine` | `rare` | `legendary`

### 技能类型（SkillTemplate.type）

`dao` | `jian` | `quantui` | `gun` | `neigong` | `qinggong`

| 值 | 中文 | 说明 |
|----|------|------|
| `dao` | 刀 | 刀法 |
| `jian` | 剑 | 剑法 |
| `quantui` | 拳腿 | 拳法、腿法、掌法等徒手功夫 |
| `gun` | 棍 | 棒法、杖法等长兵器 |
| `neigong` | 内功 | 内力修炼 |
| `qinggong` | 轻功 | 身法、步法 |

### 技能难度（SkillTemplate.tier）

`easy` | `normal` | `hard` | `expert` | `master`

| 值 | 中文 | 说明 |
|----|------|------|
| `easy` | 入门 | 基础武学，容易上手 |
| `normal` | 常规 | 标准武学 |
| `hard` | 难练 | 需要一定基础 |
| `expert` | 艰深 | 高阶武学 |
| `master` | 绝学 | 顶级武学 |

### 技能熟练度（LearnedSkill.level）

`chuxue` | `xiaocheng` | `dacheng` | `jingtong`

| 值 | 中文 | 说明 |
|----|------|------|
| `chuxue` | 初学 | 刚学会 |
| `xiaocheng` | 小成 | 基本掌握 |
| `dacheng` | 大成 | 熟练运用 |
| `jingtong` | 精通 | 融会贯通 |

### 地点类型（Location.type）

`shop` | `sect` | `residence` | `government` | `inn` | `market` | `road` | `wilderness` | `event`

| 值 | 中文 | 说明 |
|----|------|------|
| `shop` | 店铺 | 铁匠铺、药铺等 |
| `sect` | 门派 | 铁掌门等 |
| `residence` | 民居 | NPC 住宅 |
| `government` | 衙门 | 官署、衙门 |
| `inn` | 客栈 | 住宿/吃饭/喝酒/情报 |
| `market` | 集市 | 摆摊、悬赏板 |
| `road` | 道路 | 连接点、镇口 |
| `wilderness` | 野外 | 后山、竹林、矿洞 |
| `event` | 事件地点 | 临时/专用事件地点 |

### 地图类型（MapTemplate.type）

`town` | `wilderness` | `dungeon`

### 任务类型（QuestTemplate.type）

`bounty` | `faction` | `government` | `npc` | `random`

### 任务目标类型（QuestObjective.type）

`kill` | `collect` | `talk` | `go_to` | `deliver` | `craft`

### 事件类型（EventTemplate.type）

`timed` | `random` | `conditional` | `exploration`

### 玩家出身（Player.origin）

`farmer` | `scholar` | `merchant` | `martial`

### 商铺类型（ShopState.type）

`herb` | `blacksmith` | `tea` | `general`

---

## NPC 日程结构

```json
{
  "schedule": {
    "morning": { "location": "location_id", "action": "开炉生火" },
    "noon": { "location": "location_id", "action": "打铁" },
    "afternoon": { "location": "location_id", "action": "打铁" },
    "evening": { "location": "location_id", "action": "收拾工具" },
    "night": { "location": "location_id", "action": "喝酒，早睡" }
  }
}
```

---

## Effects 结构

effects 表示状态变化的差值（正数加，负数扣）。

```typescript
interface Effects {
  copper?: number                    // 铜钱差值
  hp?: number                        // 生命差值
  stamina?: number                   // 体力差值
  qi?: number                        // 内力差值
  reputation?: Record<string, number>  // 声望差值（维度 → 差值）
  affection?: Record<string, number>   // 好感差值（npc_id → 差值）
  flags_set?: string[]               // 设为 true 的 flag
  flags_unset?: string[]             // 取消的 flag
  items?: {
    add?: { id: string; count: number }[]     // 获得物品
    remove?: { id: string; count: number }[]  // 失去物品
  }
  skills?: {
    add?: string[]                   // 学会的技能 ID
    remove?: string[]                // 遗忘的技能 ID
  }
}
```

### 声望维度

| 维度 | 范围 | 说明 |
|------|------|------|
| `hero` | -100 ~ +100 | 侠义值（恶名 ↔ 侠义） |
| `factions.*` | 数值 | 门派声望（门派ID → 声望值） |
| `government` | 0 ~ 100 | 官府声望 |
| `commerce` | 0 ~ 100 | 商誉 |

---

## Conditions / Prerequisites 结构

```typescript
interface Prerequisites {
  flags?: string[]                   // 需要为 true 的 flag
  min_day?: number                   // 最早天数
  reputation?: Record<string, number>  // 声望要求
  affection?: Record<string, number>   // 好感要求（npc_id → 最低值）
  completed_quests?: string[]        // 需要已完成的任务 ID
  items?: { id: string; count: number }[]  // 需要持有的物品
  time?: string                      // 时段要求（morning/noon/...）
}
```

---

## Authoring 与 Runtime 字段分类

### NPC 模板

| 分类 | 字段 |
|------|------|
| **runtime** | id, name, role, age, faction, location, schedule, shop_inventory, buy_preference, quest_ids |
| **authoring** | gameplay_role, personality, speaking_style, background, secret, wish, daily_quote, player_value, relationships, design_note |

### 任务模板

| 分类 | 字段 |
|------|------|
| **runtime** | id, name, type, giver, location, description, prerequisites, objectives, rewards, time_limit |
| **authoring** | full_story, solution_paths, failure_result, effects_on_complete, related_npcs, related_locations, flavor_text, design_note |

### 事件模板

| 分类 | 字段 |
|------|------|
| **runtime** | id, name, type, trigger, description, choices, cooldown, repeatable, world_flags_required, world_flags_set, followup_event_ids |
| **authoring** | design_note |

### 地点模板

| 分类 | 字段 |
|------|------|
| **runtime** | id, name, region, type, description, interactables, npcs, shops, available_events, connected_locations, time_variants, flags |
| **authoring** | design_note |

### 物品模板

| 分类 | 字段 |
|------|------|
| **runtime** | id, name, type, quality, price, description, effects |
| **authoring** | flavor, related_npc, related_quest, design_note |

### 武学模板

| 分类 | 字段 |
|------|------|
| **runtime** | id, name, type, tier, source, description, unlock_condition, effects |
| **authoring** | flavor, related_npc, related_faction, design_note |

---

## 文件落点

每类内容最终写入的 JSON 文件路径：

| 内容类型 | 文件路径 |
|----------|----------|
| NPC | `game-data/npcs/*.json` |
| 对话 | `game-data/dialogues/*.json` |
| 任务 | `game-data/quests/*.json` |
| 事件 | `game-data/events/*.json` |
| 地点 | `game-data/maps/*.json` |
| 物品 | `game-data/items/*.json` |
| 武学 | `game-data/skills/*.json` |
| 传闻 | `game-data/rumors/*.json`（待建） |
