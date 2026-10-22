
import json
import os
from pathlib import Path
from collections import Counter

# =====================================
# ASTRA - KEYFRAME ANALYZER
# =====================================

ROOT = (
    Path(os.environ["LOCALAPPDATA"])
    / "CapCut"
    / "User Data"
    / "Projects"
    / "com.lveditor.draft"
)

PROJECT_NAME = "Bullterrier - LONG-kopia"

# Znajdz projekt
matches = [
    p for p in ROOT.rglob("draft_content.json")
    if p.parent.name == PROJECT_NAME
]

if not matches:
    print("Nie znaleziono projektu.")
    raise SystemExit

with matches[0].open("r", encoding="utf-8-sig") as f:
    data = json.load(f)


# Pokazujemy strukture danych bez ujawniania
# sciezek do plikow oraz identyfikatorow.
def inspect_structure(value, depth=0):

    if depth >= 5:
        return "..."

    if isinstance(value, dict):
        return {
            key: inspect_structure(val, depth + 1)
            for key, val in list(value.items())[:10]
        }

    if isinstance(value, list):
        return {
            "type": "list",
            "length": len(value),
            "first_item": (
                inspect_structure(value[0], depth + 1)
                if value else None
            )
        }

    if isinstance(value, bool):
        return "<boolean>"

    if isinstance(value, (int, float)):
        return "<number>"

    if isinstance(value, str):
        return "<text>"

    return str(type(value).__name__)


total_video_segments = 0
segments_with_keyframes = 0
field_counts = Counter()
examples = []

for track_index, track in enumerate(data.get("tracks", []), 1):

    if track.get("type") != "video":
        continue

    for segment_index, segment in enumerate(
        track.get("segments", []), 1
    ):

        total_video_segments += 1

        common = segment.get("common_keyframes")
        refs = segment.get("keyframe_refs")

        if common or refs:
            segments_with_keyframes += 1

            if common:
                field_counts["common_keyframes"] += 1

            if refs:
                field_counts["keyframe_refs"] += 1

            if len(examples) < 3:
                examples.append({
                    "track": track_index,
                    "segment": segment_index,
                    "common_keyframes": inspect_structure(common),
                    "keyframe_refs": inspect_structure(refs),
                    "clip": inspect_structure(
                        segment.get("clip", {})
                    )
                })


print("\n=== ASTRA KEYFRAME ANALYZER ===")

print("Projekt:", PROJECT_NAME)
print("Elementy wizualne:", total_video_segments)
print("Elementy z keyframes:", segments_with_keyframes)

print("\n=== RODZAJE DANYCH ===")

for field, count in field_counts.items():
    print(f"{field}: {count}")

print("\n=== PRZYKLADOWE STRUKTURY ===")

for example in examples:
    print(
        json.dumps(
            example,
            indent=2,
            ensure_ascii=False
        )
    )

print("\nAnaliza zakonczona.")
