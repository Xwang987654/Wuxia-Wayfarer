## ADDED Requirements

### Requirement: Combat triggers during exploration
玩家在镇外探索时可能遭遇敌对 NPC。

#### Scenario: Random encounter
- **WHEN** 玩家在探索区域移动
- **THEN** 有概率触发战斗遭遇，显示遭遇提示

### Requirement: Player can choose combat response
遭遇时玩家可选择应对方式。

#### Scenario: Choose to fight
- **WHEN** 玩家选择"战斗"
- **THEN** 系统自动计算战斗结果，显示战斗过程文字描述

#### Scenario: Choose to flee
- **WHEN** 玩家选择"逃跑"
- **THEN** 根据轻功值计算逃跑成功率，成功则无事发生，失败则进入战斗

### Requirement: Battle result displayed as text
战斗结果以文字形式展示，包含过程描述和奖励。

#### Scenario: Victory
- **WHEN** 战斗胜利
- **THEN** 显示战斗过程文字、获得的战利品（物品/铜钱）、消耗的状态

#### Scenario: Defeat
- **WHEN** 战斗失败
- **THEN** 显示失败描述，损失部分金钱，回到客栈恢复

### Requirement: Combat formula uses attributes
战斗结果基于玩家属性、装备、武功和随机因素计算。

#### Scenario: Damage calculation
- **WHEN** 战斗计算
- **THEN** 伤害 = 攻击力 × 武功倍率 - 防御力 × 护甲系数 + 随机浮动
