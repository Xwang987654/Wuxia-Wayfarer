# Time System

## 时段

demo 使用 4 个时段：

| id | 中文 | 说明 |
| --- | --- | --- |
| `morning` | 清晨 | 玩家初始时段 |
| `noon` | 午间 | 完成一次行动后可推进到这里 |
| `evening` | 傍晚 | demo 可选展示 |
| `night` | 夜晚 | demo 可选展示 |

## 推进规则

- 采集草药会推进 1 个时段。
- 普通移动和普通对话默认不推进时间。
- 交付任务默认不推进时间。
- 到 `night` 后是否换日，demo 阶段可以暂不实现。

## Runtime 对应

规则数据见 `data/game-runtime/rules/time.json`。

