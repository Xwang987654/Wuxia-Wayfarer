# 数据模型

> 定义游戏中所有数据的结构。分为静态数据（游戏配置）和动态数据（存档）。

## 设计原则

- **模板与实例分离**：物品/NPC/武功的定义（模板）与运行时状态（实例）分开存储
- **引用而非复制**：背包里存 `itemId` 引用模板，不复制物品属性
- **扁平结构**：不使用 ECS 组件化，直接访问 `player.hp`、`world.season`
- **灵活标记**：剧情/事件标记使用通用 `flags` 字段

## 数据分层

```
game-data/                  （静态，随游戏分发）
├── items.json              物品模板
├── npcs.json               NPC模板
├── skills.json             武功模板
├── quests.json             任务模板
├── maps.json               地图/地点定义
└── events.json             事件模板

save-data/                  （动态，玩家存档）
├── save-slot-1.json
├── save-slot-2.json
└── save-slot-3.json
```

---

## 存档结构（SaveData）

```typescript
interface SaveData {
  version: string              // 存档版本号（兼容性用）
  timestamp: number            // 存档时的现实时间戳
  playTime: number             // 总游玩时间（秒）

  player: Player
  world: WorldState
  npcs: NPCInstance[]
  questLog: QuestLog
  reputation: Reputation
  shops: ShopState[]
  flags: Record<string, any>   // 全局剧情/事件标记
}
```

---

## Player（玩家）

```typescript
interface Player {
  // 基础信息
  id: string
  name: string
  origin: "farmer" | "scholar" | "merchant" | "martial"
  portrait: string             // 头像资源ID

  // 生命/体力/内力
  hp: number                   // 当前生命
  hpMax: number                // 最大生命
  stamina: number              // 当前体力
  staminaMax: number           // 最大体力
  qi: number                   // 当前内力
  qiMax: number                // 最大内力

  // 战斗属性
  attack: number               // 基础攻击
  defense: number              // 基础防御
  agility: number              // 轻功

  // 社交属性
  eloquence: number            // 口才
  wisdom: number               // 悟性
  constitution: number         // 根骨

  // 经营属性
  craftsmanship: number        // 手艺
  perception: number           // 眼力

  // 位置
  map: string                  // 当前地图ID
  location: string             // 当前地点ID

  // 装备
  weapon: string | null        // 物品ID
  armor: string | null
  shoes: string | null

  // 背包（格子展示，无容量限制）
  inventory: InventorySlot[]

  // 武功
  learnedSkills: LearnedSkill[]
  equippedSkills: [string | null, string | null, string | null]  // 3个主动武功槽
  equippedInnerSkill: string | null  // 内功槽

  // 财产
  copper: number               // 铜钱
  silver: number               // 银两（1银两 = 1000铜钱）

  // 路线状态
  faction: string | null       // 所属门派ID
  factionRank: number          // 门派等级（0=未加入）
  job: string | null           // 职业ID
  jobRank: number              // 职业等级
}
```

### InventorySlot（背包格子）

```typescript
interface InventorySlot {
  itemId: string               // 物品模板ID
  quantity: number             // 数量
}
```

### LearnedSkill（已学武功）

```typescript
interface LearnedSkill {
  skillId: string              // 武功模板ID
  level: "chuxue" | "xiaocheng" | "dacheng" | "jingtong"
                               // 初学/小成/大成/精通
  useCount: number             // 使用次数（用于升级判定）
}
```

---

## WorldState（世界状态）

```typescript
interface WorldState {
  // 时间
  day: number                  // 第几天（从1开始）
  timeOfDay: number            // 当前时段（0=清晨, 1=上午, 2=午后, 3=傍晚, 4=夜晚）
  season: "spring" | "summer" | "autumn" | "winter"
  year: number                 // 第几年

  // 天气
  weather: "sunny" | "overcast" | "rain" | "heavy_rain" | "thunder"
           | "fog" | "wind" | "snow" | "heavy_snow" | "frost" | "scorching"
  weatherDuration: number      // 天气剩余持续天数

  // 事件状态
  activeEvents: string[]       // 当前激活的事件ID
  completedEvents: string[]    // 已完成的事件ID
  eventCooldowns: Record<string, number>  // 事件冷却（事件ID → 可再次触发的天数）

  // 全局标记
  flags: Record<string, any>
}
```

### 时间转换规则

```
totalGameMinutes = (day - 1) * 10 + timeOfDay * 2

day = floor(totalGameMinutes / 10) + 1
timeOfDay = floor((totalGameMinutes % 10) / 2)

season 计算：
seasonIndex = floor((day - 1) / 6) % 4
0 = spring, 1 = summer, 2 = autumn, 3 = winter

year 计算：
year = floor((day - 1) / 24) + 1
```

---

## NPCInstance（NPC实例）

```typescript
interface NPCInstance {
  npcId: string                // NPC模板ID（引用 npcs.json）
  affection: number            // 好感度（-100 ~ 100）
  isAlive: boolean
  currentLocation: string | null  // null = 按日程表走
  unlockedDialogues: string[]  // 已解锁的对话节点ID
  questStates: Record<string, "active" | "completed" | "failed">
  lastInteractionDay: number   // 最后互动的天数
  flags: Record<string, any>   // NPC个人标记
}
```

NPC模板（静态）包含：id、name、role、schedule、dialogue、inventory、buyPreference 等。详见 `game-data/characters.md`。

---

## QuestLog（任务日志）

```typescript
interface QuestLog {
  activeQuests: ActiveQuest[]
  completedQuests: string[]    // 已完成的任务ID
  failedQuests: string[]       // 已失败的任务ID
}

interface ActiveQuest {
  questId: string              // 任务模板ID
  progress: Record<string, number>  // 目标进度（目标ID → 当前数量）
  startDay: number             // 接取任务的天数
}
```

---

## Reputation（声望）

```typescript
interface Reputation {
  hero: number                 // 侠义值（-100 恶名 ~ +100 侠义）
  factions: Record<string, number>  // 门派声望（门派ID → 声望值）
  government: number           // 官府声望（0 ~ 100）
  commerce: number             // 商誉（0 ~ 100）
}
```

---

## ShopState（商铺状态）

```typescript
interface ShopState {
  id: string                   // 铺子实例ID
  type: "herb" | "blacksmith" | "tea" | "general"
  location: string             // 地点ID
  reputation: number           // 铺子声望（0 ~ 100）
  stock: ShopStockItem[]       // 货架上的物品
  pricing: Record<string, number>  // 物品定价（物品ID → 价格）
  dailyRevenue: number         // 今日收入（每日重置）
  totalRevenue: number         // 总收入
  rentDueDay: number           // 下次交租的天数
}

interface ShopStockItem {
  itemId: string
  quantity: number
}
```

---

## 静态数据模板

### ItemTemplate（物品模板）

```typescript
interface ItemTemplate {
  id: string
  name: string
  type: "weapon" | "armor" | "shoes" | "medicine" | "material"
        | "food" | "book" | "quest_item" | "special"
  quality: "normal" | "fine" | "rare" | "legendary"
  price: number                // 基础价格（铜钱）
  weight: number               // 重量（当前版本不影响背包）
  effects: {
    attack?: number
    defense?: number
    agility?: number
    hp?: number                // 恢复生命
    stamina?: number           // 恢复体力
    qi?: number                // 恢复内力
    tempAttack?: number        // 临时攻击加成
    tempWisdom?: number        // 临时悟性加成
  }
  description: string
  icon: string                 // 图标资源路径
}
```

### SkillTemplate（武功模板）

```typescript
interface SkillTemplate {
  id: string
  name: string
  type: "fist" | "palm" | "sword" | "dao" | "hidden_weapon"
        | "lightness" | "inner"
  damageMultiplier: number     // 伤害倍率
  qiCost: number               // 内力消耗
  critRate: number             // 暴击率
  special: string | null       // 特殊效果描述
  learnCondition: {
    faction?: string           // 需要所属门派
    rank?: number              // 需要门派等级
    affection?: { npcId: string, value: number }  // 需要NPC好感
    prerequisite?: string      // 前置武功ID
  } | null
  upgradeThresholds: {
    xiaocheng: number          // 达到小成的使用次数
    dacheng: number
    jingtong: number
  }
  description: string
}
```

### NPCTemplate（NPC模板）

```typescript
interface NPCTemplate {
  id: string
  name: string
  role: string                 // 角色身份
  age: number
  personality: string          // 性格描述（影响对话风格）
  location: string             // 默认所在地
  schedule: Record<number, {   // 日程（时段 → 行为）
    location: string
    action: string
  }>
  dialogues: DialogueNode[]    // 对话树
  shopInventory: string[] | null  // 可出售的物品ID列表
  buyPreference: string[] | null  // 偏好收购的物品类型
  questIds: string[]           // 可提供的任务ID
}
```

### QuestTemplate（任务模板）

```typescript
interface QuestTemplate {
  id: string
  name: string
  type: "bounty" | "faction" | "government" | "npc" | "random"
  giver: string                // 发布者（NPC ID 或 "notice_board"）
  description: string
  objectives: QuestObjective[]
  rewards: {
    copper?: number
    silver?: number
    items?: { itemId: string, quantity: number }[]
    reputation?: Partial<Reputation>
    skillId?: string           // 奖励武功
  }
  prerequisites: {
    minDay?: number            // 最早触发天数
    reputation?: Partial<Reputation>
    completedQuests?: string[]
    affection?: { npcId: string, value: number }
    flags?: Record<string, any>
  }
  timeLimit: number | null     // 限时天数（null=不限时）
}

interface QuestObjective {
  id: string                   // 目标ID（用于进度追踪）
  type: "kill" | "collect" | "talk" | "go_to" | "craft"
  target: string               // 目标ID（怪物/物品/NPC/地点）
  count: number                // 需要数量
}
```

### MapTemplate（地图模板）

```typescript
interface MapTemplate {
  id: string
  name: string
  type: "town" | "wilderness" | "dungeon"
  locations: Location[]
  connections: {               // 可到达的其他地图
    targetMap: string
    travelTime: number         // 路程天数
    requirements: Record<string, any> | null  // 进入条件
  }[]
}

interface Location {
  id: string
  name: string
  type: "shop" | "guild" | "government" | "inn" | "explore" | "event"
  npcIds: string[]             // 此地点可能出现的NPC
  availableActions: string[]   // 可执行的操作
  description: string
}
```

### EventTemplate（事件模板）

```typescript
interface EventTemplate {
  id: string
  name: string
  type: "timed" | "random" | "conditional" | "exploration"
  trigger: {
    season?: string            // 季节限定
    weather?: string           // 天气限定
    timeOfDay?: number         // 时段限定
    location?: string          // 地点限定
    probability?: number       // 触发概率（0-1）
    minDay?: number            // 最早天数
    conditions?: Record<string, any>  // 其他条件（flags等）
  }
  description: string
  choices: EventChoice[]
  cooldown: number             // 冷却天数
}

interface EventChoice {
  text: string
  conditions?: Record<string, any>  // 显示此选项的条件
  effects: {
    copper?: number
    hp?: number
    stamina?: number
    affection?: { npcId: string, value: number }
    reputation?: Partial<Reputation>
    items?: { itemId: string, quantity: number }[]
    flags?: Record<string, any>
    skillId?: string
  }
}
```

---

## 存档读写流程

```
存档：
Player + WorldState + NPCInstances + QuestLog + Reputation + Shops + Flags
    │
    ▼
JSON.stringify()
    │
    ▼
写入 save-slot-N.json

读档：
读取 save-slot-N.json
    │
    ▼
JSON.parse()
    │
    ▼
版本检查（version字段）
    │
    ▼
数据迁移（如版本不匹配）
    │
    ▼
注入到游戏各系统
```
