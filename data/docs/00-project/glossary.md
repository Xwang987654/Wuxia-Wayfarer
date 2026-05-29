# Glossary

## 项目术语

- demo：第一版最小可玩版本，只验证一个清风镇闭环。
- runtime data：Godot 运行时读取或打包的数据，位于 `data/game-runtime/`。
- design docs：设计与开发规范，位于 `data/docs/`。
- id：跨 JSON 文件引用用的稳定字符串。
- object-per-file：一对象一文件，不使用聚合式 `items.json` 或 `npcs.json`。

## 地点术语

- 清风镇：demo 唯一地图。
- 镇口：玩家初始进入点，也是守卫所在位置。
- 青石街：清风镇主街，连接各地点。
- 林家药铺：药师林所在地点，任务发布与交付点。
- 清风客栈：周掌柜所在地点，可闲聊、购买馒头。
- 溪边草坡：采集草药的地点，不写作“药田”，避免暗示已被人耕种。

## 数据类型

- map：地图与地点连接。
- npc：角色基础信息、默认地点、可用对话和任务。
- dialogue：对话节点与玩家选项。
- quest：任务步骤、目标和奖励。
- item：物品定义。
- player_state：玩家初始状态。
- rule：时间、经济等全局规则。
- asset_manifest：demo 素材清单。

