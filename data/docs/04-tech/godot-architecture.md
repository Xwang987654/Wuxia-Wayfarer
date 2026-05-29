# Godot Architecture

## 技术栈

Godot 4.x + GDScript + JSON 数据驱动。

## 建议工程结构

```text
res://
├── scenes/                 # Godot 场景
├── scripts/                # GDScript
├── ui/                     # UI 场景和主题
├── assets/                 # 导入后的美术和音频资产
└── data/                   # 从仓库 data/game-runtime/ 同步或打包的数据
```

## 数据加载

- 开发期以 `data/game-runtime/` 为源。
- Godot 运行时可以把该目录复制到 `res://data/` 或打包为资源。
- 加载器按目录扫描 JSON，每个文件解析一个对象。
- 通过对象的 `id` 建立索引。

## 核心服务建议

- `DataRegistry`：加载并索引 runtime JSON。
- `GameState`：保存玩家位置、时间、背包、任务状态。
- `LocationController`：处理地点切换。
- `DialogueController`：处理对话节点。
- `QuestController`：处理任务状态和奖励。

## 约束

demo 阶段不引入 ECS、不引入数据库、不引入外部剧情脚本语言。

