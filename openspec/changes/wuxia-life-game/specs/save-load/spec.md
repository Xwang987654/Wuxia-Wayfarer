## ADDED Requirements

### Requirement: Player can save game
玩家可将当前游戏状态保存到存档文件。

#### Scenario: Save to slot
- **WHEN** 玩家在菜单中选择"存档"并选择槽位
- **THEN** 当前游戏状态序列化为 JSON 写入 `user://save-slot-N.json`

#### Scenario: Save contains all game state
- **WHEN** 存档完成
- **THEN** 存档包含：玩家状态、世界状态、NPC 实例、任务日志、声望、全局标记

### Requirement: Player can load game
玩家可从存档文件恢复游戏状态。

#### Scenario: Load from slot
- **WHEN** 玩家在菜单中选择"读档"并选择槽位
- **THEN** 从 JSON 文件反序列化，恢复所有游戏状态

#### Scenario: Load validates version
- **WHEN** 读取存档
- **THEN** 检查存档版本号，版本不匹配时提示并尝试迁移

### Requirement: Save slots
游戏支持 3 个存档槽位。

#### Scenario: Display save slots
- **WHEN** 玩家打开存档/读档界面
- **THEN** 显示 3 个槽位，每个槽位显示：存档时间、游玩时长、当前天数

#### Scenario: Empty slot
- **WHEN** 槽位无存档
- **THEN** 显示"空"
