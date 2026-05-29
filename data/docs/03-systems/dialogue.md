# Dialogue System

## 目标

对话系统只支持 demo 需要的最小能力：NPC 说一句或几句，玩家选择选项，选项可结束、跳转或触发任务相关动作。

## 节点规则

- 每个 dialogue 文件定义一个对话对象。
- 每个对话对象包含 `nodes`。
- 每个 node 包含 `id`、`speaker_id`、`text`、`choices`。
- 每个 choice 包含 `text`、`next_node_id`，可选 `effects`。
- `next_node_id` 为 `null` 表示结束对话。

## 限制

- 不做复杂条件表达式。
- 不做嵌套剧情脚本。
- 不做好感、声望、阵营检查。
- 单次对话最多 5 个节点。

