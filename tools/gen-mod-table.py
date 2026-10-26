#!/usr/bin/env python3
"""Печатает сводную markdown-таблицу модов из mods/*/*/*/mod.yaml.

Использование:
    python3 tools/gen-mod-table.py          # таблица в stdout
    python3 tools/gen-mod-table.py --check  # сверка с README.md (exit 1 при рассинхроне)

Зависимость: PyYAML.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RISK = {"low": "низкий", "medium": "средний", "high": "высокий"}


def load_mods():
    mods = []
    for manifest in sorted(ROOT.glob("mods/*/*/*/mod.yaml")):
        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        rel = manifest.parent.relative_to(ROOT)
        mods.append((rel, data))
    return sorted(mods, key=lambda m: (m[1].get("book", ""), str(m[0])))


def render(mods):
    lines = [
        "| Мод | Книга | Этап | Где | Требования | Риск |",
        "|---|---|---|---|---|---|",
    ]
    for rel, m in mods:
        name = m["name"]
        lines.append(
            f"| [{name}]({rel}/) | {m.get('book','')} | {m.get('stage','')} "
            f"| {m.get('where','')} | {m.get('requires','')} "
            f"| {RISK.get(m.get('risk',''), m.get('risk',''))} |"
        )
    return "\n".join(lines)


def main():
    table = render(load_mods())
    if "--check" not in sys.argv:
        print(table)
        return
    if table in (ROOT / "README.md").read_text(encoding="utf-8"):
        print("таблица модов в README.md актуальна")
        return
    print("README.md: таблица модов устарела — обновите через gen-mod-table.py", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
