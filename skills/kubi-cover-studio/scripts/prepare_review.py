#!/usr/bin/env python3
"""Create review evidence; this script does not judge style or course meaning."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--reference", type=Path, nargs=3, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        from PIL import Image, ImageDraw, ImageOps
    except ImportError:
        parser.exit(2, "需要带 Pillow 的 Python 运行时；或用现有图像工具生成等效检查证据。\n")
    paths = [args.source.resolve(), *(p.resolve() for p in args.reference)]
    outputs = [args.out_dir / n for n in ("geometry.json", "thumbnail.png", "comparison.jpg")]
    if any(p.exists() for p in outputs):
        parser.exit(2, "目标证据已存在，请使用新的检查版本目录；未覆盖文件。\n")
    originals = []
    images = []
    transparency = []
    for path in paths:
        with Image.open(path) as raw:
            originals.append(raw.size)
            transparency.append(
                raw.convert("RGBA").getchannel("A").getextrema()[0] < 255)
            images.append(ImageOps.exif_transpose(raw).convert("RGB"))
    width, height = images[0].size
    ratio_pass = width > height and (
        abs(width - height * 16 / 9) <= 1 or abs(height - width * 9 / 16) <= 1)
    report = {
        "source": str(paths[0]), "source_sha256": hashlib.sha256(paths[0].read_bytes()).hexdigest(),
        "stored_size": list(originals[0]), "display_size": [width, height],
        "width": width, "height": height, "aspect_ratio": width / height,
        "has_transparent_pixels": transparency[0],
        "opaque_paper_background_result": "FAIL" if transparency[0] else "UNVERIFIED",
        "target": "16:9 landscape", "tolerance": "at most one pixel edge rounding",
        "aspect_ratio_result": "PASS" if ratio_pass else "FAIL",
        "references": [{"label": f"REFERENCE {i}", "path": str(p),
                        "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                       for i, p in enumerate(paths[1:], 1)],
        "visual_review": "UNVERIFIED: open original, thumbnail and comparison; write qa.md",
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    thumb_height = max(1, round(height * 320 / width))
    images[0].resize((320, thumb_height), Image.Resampling.LANCZOS).save(outputs[1])
    tile_w, tile_h, label_h, gap = 480, 270, 24, 12
    sheet = Image.new("RGB", (tile_w * 2 + gap * 3, (tile_h + label_h) * 2 + gap * 3), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    for i, img in enumerate(images):
        x = gap + (i % 2) * (tile_w + gap)
        y = gap + (i // 2) * (tile_h + label_h + gap)
        draw.text((x, y + 4), "CANDIDATE" if i == 0 else f"REFERENCE {i}", fill="#222222")
        tile = ImageOps.contain(img, (tile_w, tile_h), Image.Resampling.LANCZOS)
        sheet.paste(tile, (x + (tile_w - tile.width) // 2, y + label_h + (tile_h - tile.height) // 2))
    sheet.save(outputs[2], quality=94)
    outputs[0].write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"aspect_ratio_result": report["aspect_ratio_result"],
                      "evidence": [str(p.resolve()) for p in outputs],
                      "visual_review": "UNVERIFIED"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
