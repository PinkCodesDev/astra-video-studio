
import json
import os
from pathlib import Path
from collections import Counter
from statistics import median

# ==========================================
# ASTRA - SHORTS STYLE ANALYZER
# ==========================================

ROOT = (
    Path(os.environ["LOCALAPPDATA"])
    / "CapCut"
    / "User Data"
    / "Projects"
    / "com.lveditor.draft"
)

PROJECT_NAME = "3 lagodne"

# 1. Szukamy projektu
matches = [
    p for p in ROOT.rglob("draft_content.json")
    if p.parent.name == PROJECT_NAME
]

if len(matches) != 1:
    print("Liczba znalezionych projektow:", len(matches))
    print("Potrzebujemy dokladnie jednego.")
    raise SystemExit(1)

with matches[0].open("r", encoding="utf-8-sig") as f:
    data = json.load(f)

tracks = data.get("tracks", [])
materials = data.get("materials", {})

# 2. Indeks materialow
media = {}

for group in ("videos", "photos", "images"):
    for item in materials.get(group, []):
        if isinstance(item, dict) and item.get("id"):
            media[item["id"]] = item

track_counts = Counter()
visual_types = Counter()

photo_durations = []
video_durations = []

video_samples = []
animated_segments = 0
max_end = 0
total_segments = 0

# 3. Analiza osi czasu
for track in tracks:
    track_type = track.get("type", "unknown")
    track_counts[track_type] += 1

    for segment in track.get("segments", []):
        total_segments += 1

        timerange = segment.get("target_timerange") or {}

        start = timerange.get("start", 0)
        duration = timerange.get("duration", 0)

        if not isinstance(start, (int, float)):
            continue

        if not isinstance(duration, (int, float)):
            continue

        if duration <= 0:
            continue

        max_end = max(max_end, start + duration)

        if track_type != "video":
            continue

        seconds = duration / 1_000_000

        material = media.get(
            segment.get("material_id"), {}
        )

        kind = str(
            material.get("type")
            or material.get("material_type")
            or "unknown"
        ).lower()

        visual_types[kind] += 1

        if kind in ("photo", "image", "picture"):
            photo_durations.append(seconds)

        elif kind == "video":
            video_durations.append(seconds)

            if len(video_samples) < 8:
                source = (
                    segment.get("source_timerange") or {}
                )

                video_samples.append({
                    "timeline_start_s": round(
                        start / 1_000_000, 2
                    ),
                    "duration_s": round(seconds, 2),
                    "source_start_s": round(
                        source.get("start", 0) / 1_000_000, 2
                    )
                })

        if segment.get("common_keyframes"):
            animated_segments += 1

# 4. Raport
print("\n=== ASTRA SHORTS ANALYZER ===")
print("Projekt:", PROJECT_NAME)

print("\n--- INFORMACJE OGOLNE ---")
print("Czas osi czasu:", round(max_end / 1_000_000, 2), "s")
print("Liczba sciezek:", len(tracks))
print("Liczba elementow:", total_segments)

print("\n--- SCIEZKI ---")
for name, count in track_counts.items():
    print(f"{name}: {count}")

print("\n--- MATERIALY WIZUALNE ---")
for kind, count in visual_types.items():
    print(f"{kind}: {count}")

if video_durations:
    print("\n--- B-ROLL ---")
    print("Liczba fragmentow:", len(video_durations))
    print(
        "Mediana dlugosci:",
        round(median(video_durations), 2), "s"
    )
    print(
        "Najkrotszy fragment:",
        round(min(video_durations), 2), "s"
    )
    print(
        "Najdluzszy fragment:",
        round(max(video_durations), 2), "s"
    )

if photo_durations:
    print("\n--- ZDJECIA ---")
    print("Liczba:", len(photo_durations))
    print(
        "Mediana dlugosci:",
        round(median(photo_durations), 2), "s"
    )

print("\n--- ANIMACJE ---")
print("Elementy z keyframes:", animated_segments)

print("\n--- PRZYKLADOWE CIECIA B-ROLL ---")

for sample in video_samples:
    print(sample)

print("\nAnaliza zakonczona.")
