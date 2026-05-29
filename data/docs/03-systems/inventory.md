# Inventory System

## 目标

背包只需要证明物品和铜钱变化能被看到。

## 规则

- 背包无容量限制。
- 物品按 `item_id` 叠加数量。
- 铜钱既可以作为 `currency.copper`，也可以有 `item_copper_coin` 作为物品定义用于展示说明；实际数值以 `currency.copper` 为准。
- demo 不做装备、品质、耐久、重量、制造。

## Demo 物品

- 铜钱：基础货币。
- 草药：任务采集物。
- 馒头：普通食物。

## Runtime 对应

物品数据见 `data/game-runtime/items/`，初始背包见 `data/game-runtime/player/initial_state.json`。

