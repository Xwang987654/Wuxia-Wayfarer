# 内容模板

撰写内容时根据类型选择对应模板。所有字段名使用 snake_case，枚举值遵循 `refs/data-contract.md`。

---

## 模板 A：NPC 人设

```json
{
  "id": "npc_blacksmith_zhang",
  "name": "张大锤",
  "role": "blacksmith",
  "age": 45,
  "faction": "none",
  "location": "location_blacksmith_shop",
  "personality": "记仇、手巧、认死理",
  "schedule": {
    "morning": { "location": "location_blacksmith_shop", "action": "开炉生火" },
    "noon": { "location": "location_blacksmith_shop", "action": "打铁" },
    "afternoon": { "location": "location_blacksmith_shop", "action": "打铁" },
    "evening": { "location": "location_blacksmith_shop", "action": "收拾工具" },
    "night": { "location": "location_blacksmith_home", "action": "喝酒，早睡" }
  },
  "shop_inventory": ["item_iron_sword", "item_hundred_forged_blade", "item_copper_armguard"],
  "buy_preference": ["ore", "metal", "weapon"],
  "quest_ids": ["quest_better_ore"],
  "gameplay_role": "shop_weapon",
  "speaking_style": "话少，直来直去，讨价还价时说数字。例：'这把剑，二十两。'",
  "background": "张大锤祖上三代打铁。他爹在的时候，铁匠铺生意还行，后来老爷子走了，铺子就剩他一个人撑着。手艺不差，但脾气犟，跟同行处不来，也没什么徒弟愿意跟他学。",
  "secret": "三年前有个外地来的客商出高价让他打一批刀，他打了。后来才知道那批刀被青竹帮买去了。这事他谁都没说过。",
  "wish": "想收个肯吃苦的徒弟，把张家的手艺传下去。",
  "daily_quote": "要什么自己看，架子上的都能卖。",
  "player_value": "初期武器供应商，通过矿石任务引导玩家探索后山",
  "relationships": {
    "npc_doctor_li": "每隔几个月帮他打一套药碾子，关系还行",
    "npc_constable_chen": "给衙门打过兵器，陈捕头欠他一顿酒"
  },
  "design_note": "作为初期武器供应商，同时通过矿石任务引导玩家去后山探索"
}
```

**字段说明**：
- `faction`：`none` | `iron_palm` | `qingzhu_gang` | `government` | `merchant_guild`
- `gameplay_role`（authoring）：`shop_weapon` | `quest_giver` | `trainer` | `info_source` | `none`
- `schedule` key 使用 `morning/noon/afternoon/evening/night`
- `relationships`、`shop_inventory`、`quest_ids` 使用 id 引用
- `background` 不超过 200 字，写故事不写简历
- `personality` 用行为词，不用空泛形容词

---

## 模板 B：对话文本

```json
{
  "npc_id": "npc_blacksmith_zhang",
  "dialogues": [
    {
      "id": "dialogue_blacksmith_greeting",
      "conditions": {},
      "nodes": [
        {
          "id": "node_01",
          "speaker": "npc",
          "intent": "greeting",
          "text": "（头也不抬，继续打铁）要什么自己看，架子上的都能卖。",
          "choices": [
            {
              "text": "这把剑怎么卖？",
              "effects": {},
              "next": "node_02"
            },
            {
              "text": "你这有没有好一点的？",
              "effects": {},
              "next": "node_03"
            }
          ]
        },
        {
          "id": "node_02",
          "speaker": "npc",
          "intent": "shop",
          "text": "铁剑一把八百文。那几把百锻的，三两起。",
          "choices": [
            {
              "text": "我看看。",
              "effects": { "open_shop": true },
              "next": null
            },
            {
              "text": "太贵了，算了。",
              "effects": {},
              "next": "node_end"
            }
          ]
        },
        {
          "id": "node_03",
          "speaker": "npc",
          "intent": "quest_hint",
          "text": "好料子不好弄。后山那边倒是有好铁矿，就是路上不太平。",
          "choices": [
            {
              "text": "怎么个不太平？",
              "effects": { "flags_set": ["quest_better_ore_hint"] },
              "next": "node_04"
            }
          ]
        },
        {
          "id": "node_04",
          "speaker": "npc",
          "intent": "rumor",
          "text": "青竹帮的人有时候在那片晃荡。碰上了交点过路钱就没事，他们不随便伤人。",
          "choices": [
            {
              "text": "知道了。",
              "effects": {},
              "next": "node_end"
            }
          ]
        },
        {
          "id": "node_end",
          "speaker": "npc",
          "intent": "goodbye",
          "text": "（点了点头，继续打铁）",
          "choices": []
        }
      ]
    }
  ]
}
```

**intent 可选值**：
`greeting` | `quest_hint` | `open_quest` | `complete_quest` | `shop` | `rumor` | `lore` | `relationship` | `refuse` | `goodbye`

**要点**：
- 一段对话不超过 5 个节点
- 每个节点有 intent，明确功能
- 选项不写"善/恶/中立"，写玩家会说的话
- effects 使用 data-contract 标准结构（flags_set/flags_unset 等）

---

## 模板 C：任务剧情

```json
{
  "id": "quest_better_ore",
  "name": "好铁难求",
  "type": "npc",
  "giver": "npc_blacksmith_zhang",
  "location": "location_blacksmith_shop",
  "description": "后山近日不太平，有商旅被劫。能料理的来衙门找陈捕头。赏银五十两。",
  "prerequisites": {
    "flags": ["quest_better_ore_hint"],
    "min_day": null,
    "reputation": {},
    "affection": {},
    "completed_quests": [],
    "items": [],
    "time": null
  },
  "objectives": [
    {
      "id": "obj_01",
      "type": "go_to",
      "target": "location_back_mountain_mine",
      "count": 1,
      "description": "去后山矿洞"
    },
    {
      "id": "obj_02",
      "type": "collect",
      "target": "item_iron_ore_quality",
      "count": 5,
      "description": "采集五块上好铁矿石"
    }
  ],
  "rewards": {
    "copper": 500,
    "items": [],
    "reputation": { "iron_palm": 5 }
  },
  "time_limit": null,
  "full_story": "张大锤最近接了个大单，需要好铁矿。但后山矿洞附近有青竹帮的人出没，他自己不方便去。如果玩家能帮忙弄到矿石，他愿意低价卖一把好武器。",
  "solution_paths": [
    { "path": "fight", "description": "打退青竹帮的人，直接进矿洞" },
    { "path": "pay", "description": "给青竹帮200文过路钱" },
    { "path": "talk", "description": "如果之前帮过青竹帮的忙，可以免费通过" }
  ],
  "failure_result": "矿石没带回来，张大锤叹了口气。",
  "effects_on_complete": {
    "flags_set": ["blacksmith_shop_upgraded"],
    "affection": { "npc_blacksmith_zhang": 10 }
  },
  "related_npcs": ["npc_blacksmith_zhang", "npc_qingzhu_scout"],
  "related_locations": ["location_back_mountain_mine", "location_blacksmith_shop"],
  "flavor_text": "张大锤看了看矿石，难得笑了一下。'成色不错。下回还有这种料子，直接送过来。'",
  "design_note": "引导玩家探索后山，接触青竹帮。提供多种解法让不同玩法的玩家都能完成"
}
```

**字段说明**：
- `type`：`bounty` | `faction` | `government` | `npc` | `random`
- `objectives.type`：`kill` | `collect` | `talk` | `go_to` | `deliver` | `craft`
- `prerequisites` 使用统一结构，见 data-contract.md
- `rewards.reputation` 使用声望维度：`hero`/`factions.*`/`government`/`commerce`
- authoring 字段：`full_story`、`solution_paths`、`failure_result`、`effects_on_complete`、`related_npcs`、`related_locations`、`flavor_text`、`design_note`
- 任务必须支持至少一种非战斗解法，除非用户明确要求纯战斗任务

---

## 模板 D：随机事件

```json
{
  "id": "event_beggar_meal",
  "name": "一碗面",
  "type": "random",
  "trigger": {
    "location": "location_marketplace",
    "time": "noon",
    "season": null,
    "weather": null,
    "probability": 0.15
  },
  "description": "集市口的面摊边上，一个老乞丐蹲在墙角，盯着锅里冒热气的面条。没伸手要，就那么看着。",
  "choices": [
    {
      "id": "choice_01",
      "text": "叫一碗面给他",
      "conditions": { "copper_min": 8 },
      "effects": {
        "copper": -8,
        "flags_set": ["beggar_helped"],
        "reputation": { "hero": 2 }
      },
      "result_text": "老乞丐接过碗，呼噜呼噜吃完，抹了抹嘴。'后生，你是个好人。改天要是去后山，小心青竹帮那个长脸汉子，他专门盯面生的。'"
    },
    {
      "id": "choice_02",
      "text": "装作没看见",
      "conditions": {},
      "effects": {},
      "result_text": "你走过去了。老乞丐还是蹲在那里，好像从来没有人经过一样。"
    },
    {
      "id": "choice_03",
      "text": "蹲下来，问他叫什么",
      "conditions": {},
      "effects": { "flags_set": ["beggar_name_learned"] },
      "result_text": "'我叫什么？'老乞丐愣了一下，好像很久没人问过这个问题。'大伙都叫我老孙头。以前的事，不提了。'他摆摆手，但看你的眼神和之前不一样了。"
    }
  ],
  "cooldown": 7,
  "repeatable": false,
  "world_flags_required": [],
  "world_flags_set": ["beggar_encountered"],
  "followup_event_ids": ["event_beggar_tip"],
  "design_note": "温和的初见事件。三个选项分别导向：获得情报、无事发生、开启后续关系线"
}
```

**字段说明**：
- `type`：`timed` | `random` | `conditional` | `exploration`
- `trigger.time` 使用字符串（morning/noon/afternoon/evening/night）
- effects 使用 data-contract 标准结构：`copper`（差值）、`flags_set`/`flags_unset`、`reputation`（声望维度）
- description 三五句话，有画面感但不铺陈
- 选择必须有不同后果，result_text 交代结果

---

## 模板 E：地点设定

```json
{
  "id": "location_blacksmith_shop",
  "name": "张记铁匠铺",
  "region": "qingfeng_town",
  "type": "shop",
  "description": "临街一间矮砖房，门口挂着几把打好的镰刀和菜刀。屋里一个大火炉，墙上挂满了铁器，地上一层黑灰。",
  "interactables": [
    { "type": "npc", "id": "npc_blacksmith_zhang" },
    { "type": "shop", "id": "shop_blacksmith" },
    { "type": "container", "id": "weapon_rack", "description": "架子上的成品武器" }
  ],
  "npcs": ["npc_blacksmith_zhang"],
  "shops": ["shop_blacksmith"],
  "available_events": ["event_beggar_meal"],
  "connected_locations": ["location_marketplace", "location_inn"],
  "time_variants": {
    "night": { "description": "铁匠铺关了门，门口的铁器都收了进去。只从门缝里透出一点火光。" }
  },
  "flags": {},
  "design_note": "初期武器商店，连接集市和客栈，是玩家日常必经之地"
}
```

**字段说明**：
- `type`：`shop` | `sect` | `residence` | `government` | `inn` | `market` | `road` | `wilderness` | `event`
- 描述不超过 80 字，只写玩家能看见、能互动的东西
- 每个地点至少承载一种玩法功能
- `time_variants` 写不同时段的差异

---

## 模板 F：传闻

```json
{
  "id": "rumor_iron_palm_recruiting",
  "source": "npc_innkeeper_wang",
  "content": "听说了没？铁掌门最近在招新弟子。赵老爷子亲自教头三个月。",
  "truth_level": "true",
  "related_quest": "quest_join_iron_palm",
  "related_event": null,
  "unlock_condition": { "flags": [] },
  "expires_after_days": 14,
  "effects": {
    "flags_set": ["rumor_iron_palm_recruiting_heard"]
  },
  "design_note": "引导玩家了解铁掌门加入途径。即使过期也可以直接去铁掌门触发"
}
```

**字段说明**：
- `source`：来源 NPC id 或 `notice_board` 或 `overheard`
- `truth_level`：`true`（完全真实）| `half_true`（部分真实）| `false`（谣言）
- 传闻要像人说出来的话，不像公告
- 应尽量引导任务、地点、人物关系或世界变化

---

## 模板 G：物品文案

```json
{
  "id": "item_iron_sword",
  "name": "铁剑",
  "type": "weapon",
  "quality": "normal",
  "description": "一把普通的铁剑，剑身有些锻打痕迹，但开了刃，能用。",
  "flavor": "剑柄上刻了个小小的'张'字。",
  "effects": {
    "attack": 5
  },
  "price": 800,
  "related_npc": "npc_blacksmith_zhang",
  "related_quest": null,
  "design_note": "初期基础武器，价格定位让新手需要攒几天钱"
}
```

**字段说明**：
- `type`：`weapon` | `armor` | `shoes` | `medicine` | `material` | `food` | `book` | `quest_item` | `special`
- `quality`：`normal` | `fine` | `rare` | `legendary`
- `price` 单位为铜钱（不用 `price_copper`）
- `description` 短，一两句话；`flavor` 可以有点味道但不抒情过度
- authoring 字段：`flavor`、`related_npc`、`related_quest`、`design_note`

---

## 模板 H：武学文案

```json
{
  "id": "skill_iron_palm_three_strikes",
  "name": "铁掌三式",
  "type": "quantui",
  "tier": "easy",
  "source": "铁掌门入门武学",
  "description": "铁掌门基础掌法，三招直来直去的劈、推、拍，看着笨，练熟了力道不小。",
  "flavor": "赵铁山教第一式的时候说：'这一掌，不是让你打死人，是让你站得住。'",
  "unlock_condition": {
    "flags": ["player_joined_iron_palm"],
    "min_attribute": { "strength": 10 }
  },
  "effects": {
    "attack": 8,
    "skill_multiplier": 1.2
  },
  "related_npc": "npc_zhao_tieshan",
  "related_faction": "iron_palm",
  "design_note": "铁掌门入门武学，定位 tier:easy。作为玩家可能学到的第一个门派技能"
}
```

**字段说明**：
- `type`：`dao` | `jian` | `quantui` | `gun` | `neigong` | `qinggong`
- `tier`：`easy`（入门）| `normal`（常规）| `hard`（难练）| `expert`（艰深）| `master`（绝学）
- 清风镇阶段只写 `easy` 到 `hard`，最多 `expert`（赵铁山的看家本领）
- `flavor` 引用教武学的人说的话，比抽象描述生动
- authoring 字段：`flavor`、`related_npc`、`related_faction`、`design_note`
