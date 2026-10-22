
import json
import os
from pathlib import Path
from collections import Counter

# =====================================
# ASTRA - KEYFRAME DETAILS
# =====================================

ROOT = (
    Path(os.environ["LOCALAPPDATA"])
    / "CapCut"
    / "User Data"
    / "Projects"
    / "com.lveditor.draft"
)

PROJECT_NAME = "Bullterrier - LONG-kopia"

matches = [
    path for path in ROOT.rglob("draft_content.json")
    if path.parent.name == PROJECT_NAME
]

if not matches:
    print("Nie znaleziono projektu.")
    raise SystemExit

if len(matches) > 1:
    print("Znaleziono kilka projektow o tej nazwie.")
    print("Liczba:", len(matches))
    raise SystemExit

with matches[0].open("r", encoding="utf-8-sig") as f:
    data = json.load(f)

property_counts = Counter()
examples = []
animated_segments = 0

for track_index, track in enumerate(data.get("tracks", []), 1):

    if track.get("type") != "video":
        continue

    for segment_index, segment in enumerate(
        track.get("segments", []), 1
    ):

        groups = segment.get("common_keyframes") or []

        if not groups:
            continue

        animated_segments += 1
        properties = []

        for group in groups:
            prop_type = str(
                group.get("property_type", "unknown")
            )

            property_counts[prop_type] += 1

            points = []

            for point in group.get("keyframe_list", []):

                # Tylko parametry liczbowe.
                # Nie pokazujemy identyfikatorow ani sciezek.
                raw_values = point.get("values") or []

                values = [
                    v for v in raw_values
                    if isinstance(v, (int, float))
                    and not isinstance(v, bool)
                ]

                points.append({
                    "time_offset": point.get("time_offset"),
                    "values": values
                })

            properties.append({
                "property_type": prop_type,
                "keyframes": points[:5]
            })

        if len(examples) < 5:
            clip = segment.get("clip") or {}

            examples.append({
                "track": track_index,
                "segment": segment_index,
                "clip_scale": clip.get("scale"),
                "clip_transform": clip.get("transform"),
                "clip_rotation": clip.get("rotation"),
                "properties": properties[:10]
            })

print("\n=== ASTRA ANIMATION DETAILS ===")

print("Projekt:", PROJECT_NAME)
print("Segmenty z keyframes:", animated_segments)

print("\n=== RODZAJE ANIMOWANYCH PARAMETROW ===")

for prop, count in property_counts.most_common():
    print(f"{prop}: {count}")

print("\n=== PRZYKLADY ANIMACJI ===")

for example in examples:
    print(json.dumps(
        example,
        indent=2,
        ensure_ascii=False
    ))

print("\nAnaliza zakonczona.")
