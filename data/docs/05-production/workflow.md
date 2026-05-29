# Workflow

## 文档驱动流程

1. 先确认需求是否属于 `data/docs/00-project/demo-scope.md`。
2. 如果属于 demo，更新对应设计文档或系统文档。
3. 如果需要运行时内容，按 `data/docs/04-tech/data-contract.md` 写入 `data/game-runtime/`。
4. 实现 Godot 功能时只读取 `data/game-runtime/`。
5. 用 `data/docs/05-production/demo-acceptance.md` 验收。

## 变更规则

- 不新增第二套文档体系。
- 不在索引文件写设计正文。
- 不把旧 `docs/` 或 `game-data/` 恢复为事实源。
- 不引入超出 demo 范围的系统。
- 新 JSON 默认一对象一文件。

## 内容新增顺序

1. 先写或更新 docs 规则。
2. 再写 runtime JSON。
3. 运行 `python3 tools/validate.py` 校验通过。
4. 最后实现 Godot 读取和交互。

