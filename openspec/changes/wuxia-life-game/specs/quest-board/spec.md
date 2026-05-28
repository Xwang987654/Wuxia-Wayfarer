## ADDED Requirements

### Requirement: Bounty board displays available quests
集市中心有悬赏板，显示可接取的任务。

#### Scenario: View bounty board
- **WHEN** 玩家点击悬赏板
- **THEN** 显示当前可接取的悬赏任务列表（名称、描述、奖励）

#### Scenario: Daily refresh
- **WHEN** 新的一天开始
- **THEN** 悬赏板刷新部分任务

### Requirement: Player can accept quests
玩家可接取悬赏任务。

#### Scenario: Accept quest
- **WHEN** 玩家选择任务并点击"接取"
- **THEN** 任务添加到任务日志，显示任务目标

### Requirement: Player can complete quests
玩家完成任务目标后可提交任务。

#### Scenario: Complete quest
- **WHEN** 任务目标全部完成
- **THEN** 玩家可提交任务，获得奖励（铜钱、声望、物品）

### Requirement: Quest progress tracked
任务进度实时更新。

#### Scenario: Progress update on kill
- **WHEN** 玩家击败任务目标敌人
- **THEN** 任务日志中对应目标计数+1

#### Scenario: Progress update on collect
- **WHEN** 玩家获得任务所需物品
- **THEN** 任务日志中对应目标计数+1

### Requirement: Quest log accessible
玩家可随时查看任务日志。

#### Scenario: Open quest log
- **WHEN** 玩家打开任务面板
- **THEN** 显示所有进行中的任务及其进度
