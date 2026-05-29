#!/usr/bin/env python3
"""校验 data/game-runtime/ 下所有 JSON 文件是否符合 data-contract.md。"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_DIR = PROJECT_ROOT / "data" / "game-runtime"
DOCS_DIR = PROJECT_ROOT / "data" / "docs"

VALID_TYPES = {
    "map", "npc", "dialogue", "quest", "item",
    "player_state", "rule", "asset_manifest",
}

VALID_OBJECTIVE_TYPES = {"collect", "talk"}

VALID_DIALOGUE_EFFECTS = {"quest_start"}

# 每种 type 的必需顶层字段（不含 id/name/type，它们在 COMMON_REQUIRED 中）
TYPE_REQUIRED_FIELDS: dict[str, list[tuple[str, str]]] = {
    # (field_name, expected_type_or_None)
    "map": [
        ("locations", "list"),
        ("connections", "list"),
        ("spawn_points", "list"),
    ],
    "npc": [
        ("role", "str"),
        ("location_id", "str"),
        ("dialogue_ids", "list"),
        ("quest_ids", "list"),
    ],
    "dialogue": [
        ("speaker_id", "str"),
        ("nodes", "list"),
    ],
    "quest": [
        ("title", "str"),
        ("giver_id", "str"),
        ("steps", "list"),
        ("rewards", "dict"),
    ],
    "item": [
        ("category", "str"),
        ("stackable", "bool"),
        ("base_price", "int"),
        ("description", "str"),
    ],
    "player_state": [
        ("location_id", "str"),
        ("time", "dict"),
        ("currency", "dict"),
        ("inventory", "list"),
        ("quest_states", "dict"),
    ],
    "rule": [
        ("rule_type", "str"),
    ],
    "asset_manifest": [
        ("assets", "list"),
    ],
}

COMMON_REQUIRED = [("id", "str"), ("name", "str"), ("type", "str")]

# 需要检查引用完整性的字段 -> 引用目标的类型目录
REFERENCE_FIELDS = {
    "location_id": "maps",       # 出现在 npc, player_state, quest.step, map.spawn_point
    "speaker_id": "npcs",        # 出现在 dialogue, dialogue.node
    "giver_id": "npcs",          # 出现在 quest
    "target_id": None,           # 可以是 npc 或 item，运行时确定
    "item_id": "items",          # 出现在 rewards, inventory, prices
    "quest_id": "quests",        # 出现在 npc
    "next_node_id": None,        # 对话节点内部引用，特殊处理
    "quest_start": "quests",     # dialogue effect
}


# ---------------------------------------------------------------------------
# 错误收集
# ---------------------------------------------------------------------------

class Errors:
    def __init__(self):
        self._list: list[str] = []

    def add(self, file_label: str, msg: str):
        self._list.append(f"  {file_label}: {msg}")

    @property
    def count(self) -> int:
        return len(self._list)

    def print_all(self):
        for e in self._list:
            print(e)


# ---------------------------------------------------------------------------
# 辅助
# ---------------------------------------------------------------------------

def load_json(path: Path):
    """尝试解析 JSON，返回 (data, error_msg)。"""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data, None
    except json.JSONDecodeError as exc:
        return None, f"JSON 解析失败: {exc}"


def check_type(value, expected: str, field_name: str) -> str | None:
    """检查字段类型，返回错误消息或 None。"""
    if expected == "str":
        if not isinstance(value, str):
            return f"字段 {field_name} 应为 string，实际为 {type(value).__name__}"
    elif expected == "int":
        if not isinstance(value, int) or isinstance(value, bool):
            return f"字段 {field_name} 应为 int，实际为 {type(value).__name__}"
    elif expected == "bool":
        if not isinstance(value, bool):
            return f"字段 {field_name} 应为 bool，实际为 {type(value).__name__}"
    elif expected == "list":
        if not isinstance(value, list):
            return f"字段 {field_name} 应为 list，实际为 {type(value).__name__}"
    elif expected == "dict":
        if not isinstance(value, dict):
            return f"字段 {field_name} 应为 dict，实际为 {type(value).__name__}"
    return None


def extract_all_ids(runtime_dir: Path, errors: Errors) -> dict[str, str]:
    """扫描所有 JSON，返回 {id: file_name} 映射。包含顶层 id 和 map 内的 location id。同时检查 id 唯一性。"""
    ids: dict[str, str] = {}
    for json_file in sorted(runtime_dir.rglob("*.json")):
        data, err = load_json(json_file)
        if err or not isinstance(data, dict):
            continue
        rel = str(json_file.relative_to(runtime_dir))
        obj_id = data.get("id")
        if obj_id and isinstance(obj_id, str):
            if obj_id in ids:
                errors.add(rel, f"id 重复: {obj_id}（首次出现于 {ids[obj_id]}）")
            else:
                ids[obj_id] = rel
        # 从 map 的 locations 中收集地点 id
        if data.get("type") == "map":
            for loc in data.get("locations", []):
                if isinstance(loc, dict):
                    loc_id = loc.get("id")
                    if loc_id and isinstance(loc_id, str):
                        loc_label = f"{rel}#{loc_id}"
                        if loc_id in ids:
                            errors.add(rel, f"location id 重复: {loc_id}（首次出现于 {ids[loc_id]}）")
                        else:
                            ids[loc_id] = loc_label
    return ids


def collect_refs_in_value(value, ref_field_name: str) -> list[tuple[str, str]]:
    """从值中提取引用，返回 [(ref_id, context), ...]。"""
    refs = []
    if isinstance(value, str) and value:
        refs.append((value, ref_field_name))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            if isinstance(item, str):
                refs.append((item, f"{ref_field_name}[{i}]"))
            elif isinstance(item, dict):
                # list of dicts, e.g. rewards.items[].item_id
                for k, v in item.items():
                    if k.endswith("_id") or k in REFERENCE_FIELDS:
                        refs.extend(collect_refs_in_value(v, f"{ref_field_name}[{i}].{k}"))
    elif isinstance(value, dict):
        for k, v in value.items():
            if k.endswith("_id") or k in REFERENCE_FIELDS:
                refs.extend(collect_refs_in_value(v, f"{ref_field_name}.{k}"))
    return refs


# ---------------------------------------------------------------------------
# 各 type 的详细校验
# ---------------------------------------------------------------------------

def validate_locations(locations: list, label: str, all_ids: dict, errors: Errors):
    loc_ids = set()
    for i, loc in enumerate(locations):
        loc_label = f"{label}.locations[{i}]"
        if not isinstance(loc, dict):
            errors.add(loc_label, "应为 object")
            continue
        for field in ("id", "name", "description"):
            v = loc.get(field)
            if not v or not isinstance(v, str):
                errors.add(loc_label, f"缺少或为空的字段 {field}")
        loc_id = loc.get("id")
        if loc_id:
            if loc_id in loc_ids:
                errors.add(loc_label, f"location id 重复: {loc_id}")
            loc_ids.add(loc_id)


def validate_connections(connections: list, loc_ids: set, label: str, errors: Errors):
    for i, conn in enumerate(connections):
        conn_label = f"{label}.connections[{i}]"
        if not isinstance(conn, dict):
            errors.add(conn_label, "应为 object")
            continue
        for direction in ("from", "to"):
            v = conn.get(direction)
            if not v or not isinstance(v, str):
                errors.add(conn_label, f"缺少或为空的字段 {direction}")
            elif v not in loc_ids:
                errors.add(conn_label, f"{direction} 引用了不存在的 location id: {v}")


def validate_spawn_points(spawns: list, loc_ids: set, label: str, errors: Errors):
    for i, sp in enumerate(spawns):
        sp_label = f"{label}.spawn_points[{i}]"
        if not isinstance(sp, dict):
            errors.add(sp_label, "应为 object")
            continue
        loc_id = sp.get("location_id")
        if not loc_id or not isinstance(loc_id, str):
            errors.add(sp_label, "缺少或为空的字段 location_id")
        elif loc_id not in loc_ids:
            errors.add(sp_label, f"location_id 引用了不存在的地点: {loc_id}")


def validate_dialogue_nodes(nodes: list, label: str, all_ids: dict, errors: Errors):
    node_ids = set()
    for i, node in enumerate(nodes):
        node_label = f"{label}.nodes[{i}]"
        if not isinstance(node, dict):
            errors.add(node_label, "应为 object")
            continue
        node_id = node.get("id")
        if not node_id or not isinstance(node_id, str):
            errors.add(node_label, "缺少或为空的字段 id")
        elif node_id in node_ids:
            errors.add(node_label, f"node id 重复: {node_id}")
        else:
            node_ids.add(node_id)

        speaker = node.get("speaker_id")
        if not speaker or not isinstance(speaker, str):
            errors.add(node_label, "缺少或为空的字段 speaker_id")

        text = node.get("text")
        if not text or not isinstance(text, str):
            errors.add(node_label, "缺少或为空的字段 text")

        choices = node.get("choices")
        if not isinstance(choices, list):
            errors.add(node_label, "字段 choices 应为 list")
            continue

        for j, choice in enumerate(choices):
            choice_label = f"{node_label}.choices[{j}]"
            if not isinstance(choice, dict):
                errors.add(choice_label, "应为 object")
                continue
            choice_text = choice.get("text")
            if not choice_text or not isinstance(choice_text, str):
                errors.add(choice_label, "缺少或为空的字段 text")

            # next_node_id 可以为 null
            next_id = choice.get("next_node_id")
            if next_id is not None and next_id not in node_ids:
                # 可能是前向引用，先记为警告；这里我们延迟校验
                pass

            effects = choice.get("effects")
            if effects is not None:
                if not isinstance(effects, dict):
                    errors.add(choice_label, "effects 应为 object")
                else:
                    for eff_key, eff_val in effects.items():
                        if eff_key not in VALID_DIALOGUE_EFFECTS:
                            errors.add(choice_label, f"未知的 dialogue effect: {eff_key}")
                        elif eff_key == "quest_start":
                            if not isinstance(eff_val, str):
                                errors.add(choice_label, f"quest_start 值应为 string")
                            elif eff_val not in all_ids:
                                errors.add(choice_label, f"quest_start 引用了不存在的 quest id: {eff_val}")

    # 校验 next_node_id 引用（延迟校验）
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            continue
        choices = node.get("choices", [])
        for j, choice in enumerate(choices):
            if not isinstance(choice, dict):
                continue
            next_id = choice.get("next_node_id")
            if next_id is not None and next_id not in node_ids:
                errors.add(
                    f"{label}.nodes[{i}].choices[{j}]",
                    f"next_node_id 引用了不存在的 node id: {next_id}",
                )


def validate_quest_steps(steps: list, label: str, all_ids: dict, errors: Errors):
    for i, step in enumerate(steps):
        step_label = f"{label}.steps[{i}]"
        if not isinstance(step, dict):
            errors.add(step_label, "应为 object")
            continue
        for field in ("id", "objective_type", "target_id", "required_count", "description"):
            if field not in step:
                errors.add(step_label, f"缺少必需字段 {field}")

        obj_type = step.get("objective_type")
        if obj_type and obj_type not in VALID_OBJECTIVE_TYPES:
            errors.add(step_label, f"未知的 objective_type: {obj_type}")

        target_id = step.get("target_id")
        if target_id and isinstance(target_id, str) and target_id not in all_ids:
            errors.add(step_label, f"target_id 引用了不存在的 id: {target_id}")

        count = step.get("required_count")
        if count is not None and (not isinstance(count, int) or count < 1):
            errors.add(step_label, f"required_count 应为正整数，实际为 {count}")


def validate_rewards(rewards: dict, label: str, all_ids: dict, errors: Errors):
    if not isinstance(rewards, dict):
        errors.add(label, "rewards 应为 object")
        return
    items = rewards.get("items", [])
    if not isinstance(items, list):
        errors.add(f"{label}.rewards", "items 应为 list")
        return
    for i, item in enumerate(items):
        item_label = f"{label}.rewards.items[{i}]"
        if not isinstance(item, dict):
            errors.add(item_label, "应为 object")
            continue
        item_id = item.get("item_id")
        if not item_id or not isinstance(item_id, str):
            errors.add(item_label, "缺少或为空的字段 item_id")
        elif item_id not in all_ids:
            errors.add(item_label, f"item_id 引用了不存在的物品: {item_id}")


def validate_prices(prices: list, label: str, all_ids: dict, errors: Errors):
    for i, price in enumerate(prices):
        price_label = f"{label}.prices[{i}]"
        if not isinstance(price, dict):
            errors.add(price_label, "应为 object")
            continue
        item_id = price.get("item_id")
        if not item_id or not isinstance(item_id, str):
            errors.add(price_label, "缺少或为空的字段 item_id")
        elif item_id not in all_ids:
            errors.add(price_label, f"item_id 引用了不存在的物品: {item_id}")


# ---------------------------------------------------------------------------
# 单文件校验
# ---------------------------------------------------------------------------

def validate_file(json_file: Path, all_ids: dict, errors: Errors):
    rel = json_file.relative_to(RUNTIME_DIR)
    label = str(rel)

    data, err = load_json(json_file)
    if err:
        errors.add(label, err)
        return

    if not isinstance(data, dict):
        errors.add(label, "顶层应为 object，不是 array 或其他类型")
        return

    # 通用必需字段
    for field, expected_type in COMMON_REQUIRED:
        val = data.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            errors.add(label, f"缺少或为空的字段 {field}")
        else:
            type_err = check_type(val, expected_type, field)
            if type_err:
                errors.add(label, type_err)

    obj_type = data.get("type")
    if obj_type and obj_type not in VALID_TYPES:
        errors.add(label, f"未知的 type: {obj_type}")
        return

    if not obj_type:
        return

    # type 专属字段
    type_fields = TYPE_REQUIRED_FIELDS.get(obj_type, [])
    for field, expected_type in type_fields:
        val = data.get(field)
        if val is None:
            errors.add(label, f"缺少必需字段 {field}")
        elif expected_type:
            type_err = check_type(val, expected_type, field)
            if type_err:
                errors.add(label, type_err)

    # ---- type 深入校验 ----

    if obj_type == "map":
        locations = data.get("locations", [])
        if isinstance(locations, list):
            validate_locations(locations, label, all_ids, errors)
            loc_ids = {loc["id"] for loc in locations if isinstance(loc, dict) and loc.get("id")}
            connections = data.get("connections", [])
            if isinstance(connections, list):
                validate_connections(connections, loc_ids, label, errors)
            spawn_points = data.get("spawn_points", [])
            if isinstance(spawn_points, list):
                validate_spawn_points(spawn_points, loc_ids, label, errors)

    elif obj_type == "npc":
        # location_id 引用检查
        loc_id = data.get("location_id")
        if loc_id and isinstance(loc_id, str) and loc_id not in all_ids:
            errors.add(label, f"location_id 引用了不存在的地点: {loc_id}")

        # dialogue_ids 引用检查
        for i, dlg_id in enumerate(data.get("dialogue_ids", [])):
            if not isinstance(dlg_id, str):
                errors.add(label, f"dialogue_ids[{i}] 应为 string")
            elif dlg_id not in all_ids:
                errors.add(label, f"dialogue_ids[{i}] 引用了不存在的对话: {dlg_id}")

        # quest_ids 引用检查
        for i, qid in enumerate(data.get("quest_ids", [])):
            if not isinstance(qid, str):
                errors.add(label, f"quest_ids[{i}] 应为 string")
            elif qid not in all_ids:
                errors.add(label, f"quest_ids[{i}] 引用了不存在的任务: {qid}")

    elif obj_type == "dialogue":
        speaker_id = data.get("speaker_id")
        if speaker_id and isinstance(speaker_id, str) and speaker_id not in all_ids:
            errors.add(label, f"speaker_id 引用了不存在的 NPC: {speaker_id}")
        nodes = data.get("nodes", [])
        if isinstance(nodes, list):
            validate_dialogue_nodes(nodes, label, all_ids, errors)

    elif obj_type == "quest":
        giver_id = data.get("giver_id")
        if giver_id and isinstance(giver_id, str) and giver_id not in all_ids:
            errors.add(label, f"giver_id 引用了不存在的 NPC: {giver_id}")
        steps = data.get("steps", [])
        if isinstance(steps, list):
            validate_quest_steps(steps, label, all_ids, errors)
        rewards = data.get("rewards")
        if rewards:
            validate_rewards(rewards, label, all_ids, errors)

    elif obj_type == "rule":
        rule_type = data.get("rule_type")
        if rule_type == "economy":
            prices = data.get("prices", [])
            if isinstance(prices, list):
                validate_prices(prices, label, all_ids, errors)


# ---------------------------------------------------------------------------
# index.md 一致性检查
# ---------------------------------------------------------------------------

def check_index_consistency(index_path: Path, runtime_dir: Path, errors: Errors):
    """检查 index.md 中列出的文件是否与实际文件一致。"""
    if not index_path.exists():
        errors.add(str(index_path.relative_to(PROJECT_ROOT)), "index.md 不存在")
        return

    text = index_path.read_text(encoding="utf-8")

    # 从 index.md 中提取提到的 .json 和 .md 文件名
    mentioned_files: set[str] = set()
    for match in re.finditer(r'[\w\-]+\.(?:json|md)', text):
        mentioned_files.add(match.group())

    # 实际文件（排除 index.md 自身）
    actual_files: set[str] = set()
    for f in runtime_dir.rglob("*"):
        if f.is_file() and f.name != "index.md":
            actual_files.add(f.name)

    # index 中有但实际不存在的
    phantom = mentioned_files - actual_files - {"index.md"}
    for f in sorted(phantom):
        errors.add("index.md", f"列出了不存在的文件: {f}")

    # 实际存在但 index 中没提到的
    unlisted = actual_files - mentioned_files
    for f in sorted(unlisted):
        errors.add("index.md", f"实际存在但未列出的文件: {f}")


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    errors = Errors()

    if not RUNTIME_DIR.exists():
        print(f"错误: 找不到 {RUNTIME_DIR}")
        sys.exit(1)

    # 收集所有 id（同时检查唯一性）
    all_ids = extract_all_ids(RUNTIME_DIR, errors)

    # 校验每个 JSON 文件
    json_files = sorted(RUNTIME_DIR.rglob("*.json"))
    print(f"扫描 {len(json_files)} 个 JSON 文件...\n")

    for json_file in json_files:
        validate_file(json_file, all_ids, errors)

    # index.md 一致性
    index_path = RUNTIME_DIR / "index.md"
    check_index_consistency(index_path, RUNTIME_DIR, errors)

    # 输出结果
    if errors.count == 0:
        print("全部通过，未发现问题。")
        sys.exit(0)
    else:
        errors.print_all()
        print(f"\n共发现 {errors.count} 个问题。")
        sys.exit(1)


if __name__ == "__main__":
    main()
