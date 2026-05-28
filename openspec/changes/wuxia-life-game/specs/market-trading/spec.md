## ADDED Requirements

### Requirement: Player can buy items from NPC shops
玩家可在 NPC 商铺购买物品。

#### Scenario: Open shop interface
- **WHEN** 玩家与商人 NPC 对话选择"交易"
- **THEN** 打开交易界面，左侧显示 NPC 商品，右侧显示玩家背包

#### Scenario: Purchase item
- **WHEN** 玩家选择商品并确认购买
- **THEN** 扣除铜钱，物品添加到背包，铜钱不足时购买按钮禁用

### Requirement: Player can sell items to NPC shops
玩家可将背包中的物品出售给 NPC。

#### Scenario: Sell item
- **WHEN** 玩家选择背包中的物品并确认出售
- **THEN** 物品从背包移除，获得铜钱（按物品基础价格的一定比例）

### Requirement: Prices fluctuate daily
物品价格每日浮动。

#### Scenario: Prices change each day
- **WHEN** 新的一天开始
- **THEN** 各 NPC 商铺的商品价格根据供需、季节、天气因素重新计算

### Requirement: Different NPCs have different prices
不同 NPC 对同一物品的收购价不同。

#### Scenario: NPC buy preference affects price
- **WHEN** 玩家向 NPC 出售物品
- **THEN** 如果物品属于 NPC 偏好类型，收购价更高
