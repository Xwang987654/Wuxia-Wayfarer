## ADDED Requirements

### Requirement: NPCs exist on map
NPC 按日程表出现在地图上的对应位置。

#### Scenario: NPC appears at scheduled location
- **WHEN** 当前时段与 NPC 日程匹配
- **THEN** NPC 出现在对应地点，玩家可见可交互

#### Scenario: NPC moves with time period
- **WHEN** 时段切换
- **THEN** NPC 根据日程表移动到下一个位置

### Requirement: Player can talk to NPC
玩家可与 NPC 对话，对话为选择式。

#### Scenario: Initiate dialogue
- **WHEN** 玩家点击 NPC
- **THEN** 弹出对话面板，显示 NPC 的当前对话内容和选项

#### Scenario: Dialogue choice affects affection
- **WHEN** 玩家选择对话选项
- **THEN** 根据选项内容，NPC 好感度可能增加或减少

#### Scenario: Dialogue conditions
- **WHEN** NPC 有好感度/声望条件的对话
- **THEN** 只有条件满足时才显示对应对话选项

### Requirement: NPCs have affection system
每个 NPC 有独立的好感度（-100 到 100）。

#### Scenario: Affection affects NPC attitude
- **WHEN** 好感度变化
- **THEN** NPC 的对话内容和态度相应变化

### Requirement: NPCs have daily schedule
NPC 有按时段变化的日程表。

#### Scenario: NPC follows schedule
- **WHEN** 清晨时段
- **THEN** 铁匠张大锤在家中休息，不在铁匠铺
