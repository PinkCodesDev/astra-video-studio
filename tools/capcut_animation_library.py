
import json
import os
from pathlib import Path
from collections import Counter

# ==========================================
# ASTRA VIDEO AGENT - ANIMATION LIBRARY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CAPCUT_DIR = (
    Path(os.environ["LOCALAPPDATA"])
    / "CapCut"
    / "User Data"
    / "Projects"
    / "com.lveditor.draft"
)

PROJECT_NAME = "Bullterrier - LONG-kopia"

OUTPUT = BASE_DIR / "memory" / "behave_animations.json"


# ==========================================
# 1. ODSZUKANIE PROJEKTU
# ==========================================

matches = [
    p for p in CAPCUT_DIR.rglob("draft_content.json")
    if p.parent.name == PROJECT_NAME
]

if len(matches) != 1:
    print("Liczba pasujacych projektow:", len(matches))
    print("Wymagany jest dokladnie jeden projekt.")
    raise SystemExit(1)

with matches[0].open("r", encoding="utf-8-sig") as f:
    project = json.load(f)


# ==========================================
# 2. ANALIZA KLATEK KLUCZOWYCH
# ==========================================

presets = []
motion_types = Counter()

for track_number, track in enumerate(
    project.get("tracks", []), start=1
):
    if track.get("type") != "video":
        continue

    for segment_number, segment in enumerate(
        track.get("segments", []), start=1
    ):
        groups = segment.get("common_keyframes") or []

        if not groups:
            continue

        properties = []
        active_motion = set()

        for group in groups:
            prop_type = group.get("property_type", "unknown")
            points = []

            for point in group.get("keyframe_list", []):
                raw_values = point.get("values") or []

                values = [
                    value for value in raw_values
                    if isinstance(value, (int, float))
                    and not isinstance(value, bool)
                ]

                points.append({
                    "time_offset_us": point.get("time_offset"),
                    "values": values,
                    "curve_type": point.get("curveType")
                })

            if not points:
                continue

            # Czy parametr rzeczywiscie zmienia wartosc?
            start_values = points[0]["values"]

            has_motion = any(
                p["values"] != start_values
                for p in points[1:]
            )

            if has_motion:
                active_motion.add(prop_type)

            properties.append({
                "property_type": prop_type,
                "has_motion": has_motion,
                "keyframes": points
            })

        if not properties:
            continue

        if "KFTypeScaleX" in active_motion:
            motion_types["zoom"] += 1

        if (
            "KFTypePositionX" in active_motion
            or "KFTypePositionY" in active_motion
        ):
            motion_types["pan"] += 1

        if not active_motion:
            motion_types["no_value_change"] += 1

        timerange = segment.get("target_timerange") or {}
        duration = timerange.get("duration", 0)

        presets.append({
            "source_track": track_number,
            "source_segment": segment_number,
            "duration_us": duration,
            "active_motion": sorted(active_motion),
            "properties": properties
        })


# ==========================================
# 3. ZAPIS BIBLIOTEKI
# ==========================================

library = {
    "brand": "Behave",
    "format": "LONG",
    "source_project": PROJECT_NAME,
    "time_unit": "microseconds",
    "description": (
        "Parametry klatek kluczowych odczytane "
        "z istniejacego projektu CapCut."
    ),
    "motion_summary": dict(motion_types),
    "presets": presets
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Nie nadpisujemy istniejacej biblioteki
if OUTPUT.exists():
    print("Biblioteka juz istnieje:", OUTPUT)
    print("Plik nie zostal nadpisany.")
    raise SystemExit(1)

with OUTPUT.open("w", encoding="utf-8") as f:
    json.dump(
        library,
        f,
        ensure_ascii=False,
        indent=2
    )


# ==========================================
# 4. RAPORT
# ==========================================

print("\n=== ASTRA ANIMATION LIBRARY ===")

print("Projekt:", PROJECT_NAME)
print("Zapisanych zestawow:", len(presets))

print("\nROZPOZNANE RUCHY:")

for name, count in motion_types.items():
    print(f"{name}: {count}")

print("\nBiblioteka zapisana:")
print(OUTPUT)

print("\nGotowe!")
