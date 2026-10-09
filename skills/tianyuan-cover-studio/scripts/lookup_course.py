#!/usr/bin/env python3
"""Return exact lesson text from this portable skill's scoped outline."""
import argparse
import json
import re
from pathlib import Path


def read_courses(path):
    courses = []
    categories = {}
    active = None
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^(#{2,5})\s+(.+)$", line)
        if heading:
            level, title = len(heading[1]), heading[2]
            if active is not None:
                courses.append(active)
                active = None
            if level < 5:
                categories = {k: v for k, v in categories.items() if k < level}
                categories[level] = title
            else:
                match = re.match(r"(\d+)\s+(.+)$", title)
                if match:
                    active = {"id": int(match[1]), "name": match[2].strip(),
                              "category": list(categories.values()), "lines": [line]}
        elif active is not None:
            if not line.startswith("<a ") and line.strip() != "---":
                active["lines"].append(line)
    if active is not None:
        courses.append(active)
    for item in courses:
        item["original_text"] = "\n".join(item.pop("lines")).strip()
    return courses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", type=int)
    group.add_argument("--name")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "references/course-outline.md"
    courses = read_courses(source)
    matches = [c for c in courses if c["id"] == args.id] if args.id is not None else [
        c for c in courses if c["name"] == args.name.strip()]
    if len(matches) != 1:
        print(json.dumps({"error": "未找到唯一匹配，请核对编号、准确课名及所属风格。",
                          "matches": [{"id": c["id"], "name": c["name"]} for c in matches]},
                         ensure_ascii=False, indent=2))
        return 2
    print(json.dumps({"source": str(source), **matches[0]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
