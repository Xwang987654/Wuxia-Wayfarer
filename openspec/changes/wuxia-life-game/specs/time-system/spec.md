## ADDED Requirements

### Requirement: Time flows in game
游戏内时间以 10 分钟（现实）= 1 天（游戏内）的速度流逝。

#### Scenario: Time advances during gameplay
- **WHEN** 游戏运行中
- **THEN** 游戏内时间持续流逝，HUD 显示当前时段和天数

### Requirement: Day has five time periods
一天分为五个时段：清晨、上午、午后、傍晚、夜晚。

#### Scenario: Time period changes
- **WHEN** 当前时段结束（每段 2 分钟现实时间）
- **THEN** 切换到下一个时段，画面色调相应变化

### Requirement: Four seasons cycle
四季循环，每 6 天（游戏内）切换一次季节。

#### Scenario: Season transitions
- **WHEN** 第 7 天到来
- **THEN** 季节从春切换到夏，后续依次秋→冬→春循环

### Requirement: Weather system
每个季节有对应的天气类型，随机触发。

#### Scenario: Weather changes randomly
- **WHEN** 新的一天开始
- **THEN** 有概率触发特殊天气（雨/雪/雾等），天气影响 NPC 行为和游戏机制

### Requirement: Time can be fast-forwarded
玩家可跳过当前时段。

#### Scenario: Skip time period
- **WHEN** 玩家选择"等待"操作
- **THEN** 时间快进到下一个时段，触发期间应发生的事件
