
import json
import os
from pathlib import Path
from collections import Counter
from statistics import median

# 1. Lokalizacja projektow
root = (
    Path(os.environ["LOCALAPPDATA"])
    / "CapCut" / "User Data"
    / "Projects" / "com.lveditor.draft"
)

project_name = "Bullterrier - LONG-kopia"

matches = [
    p for p in root.rglob("draft_content.json")
    if p.parent.name == project_name
]

if not matches:
    print("Nie znaleziono projektu.")
    raise SystemExit

# 2. Odczyt projektu
with matches[0].open("r", encoding="utf-8-sig") as f:
    data = json.load(f)

tracks = data.get("tracks", [])
materials = data.get("materials", {})

# 3. Indeks materialow
media = {}

for group in ("videos", "photos", "images"):
    for item in materials.get(group, []):
        if isinstance(item, dict) and item.get("id"):
            media[item["id"]] = item

animation_ids = {
    item["id"]
    for item in materials.get("animations", [])
    if isinstance(item, dict) and item.get("id")
}

durations = []
photo_durations = []
media_types = Counter()

max_end = 0
keyframe_segments = 0
animation_segments = 0
sample_segment = None

# 4. Analiza osi czasu
for track in tracks:
    if track.get("type") != "video":
        continue

    for segment in track.get("segments", []):
        if sample_segment is None:
            sample_segment = segment

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

        # CapCut zwykle zapisuje czas w mikrosekundach
        seconds = duration / 1_000_000
        durations.append(seconds)

        material = media.get(segment.get("material_id"), {})
        kind = str(
            material.get("type")
            or material.get("material_type")
            or "unknown"
        ).lower()

        media_types[kind] += 1

        if kind in ("photo", "image", "picture"):
            photo_durations.append(seconds)

        # Sprawdzamy obecne pola klatek kluczowych
        if (
            segment.get("common_keyframes")
            or segment.get("keyframe_refs")
        ):
            keyframe_segments += 1

        # Sprawdzamy odwolania do animacji
        refs = segment.get("extra_material_refs") or []

        if not isinstance(refs, list):
            refs = []

        if (
            any(ref in animation_ids for ref in refs)
            or segment.get("animation_id")
            or segment.get("animations")
        ):
            animation_segments += 1

# 5. Raport
print("\n=== ASTRA STYLE ANALYZER ===")
print("Projekt:", project_name)

print("\n--- CZAS ---")
print(f"Najpozniejszy koniec elementu: {max_end / 60_000_000:.2f} min")

if durations:
    print(f"Mediana dlugosci elementu: {median(durations):.2f} s")
    print(f"Najkrotszy element: {min(durations):.2f} s")
    print(f"Najdluzszy element: {max(durations):.2f} s")

if photo_durations:
    print(f"Mediana zdjecia: {median(photo_durations):.2f} s")

print("\n--- RODZAJE MATERIALOW ---")
for kind, count in media_types.items():
    print(f"{kind}: {count}")

print("\n--- ANIMACJE ---")
print(f"Elementy z wykrytymi keyframes: {keyframe_segments}")
print(f"Elementy z wykrytymi animacjami: {animation_segments}")
print(f"Animacje w bibliotece projektu: {len(animation_ids)}")

# 6. Diagnostyka struktury
if sample_segment:
    print("\n--- POLA SEGMENTU ---")
    print(", ".join(sorted(sample_segment.keys())))

    clip = sample_segment.get("clip")
    if isinstance(clip, dict):
        print("\n--- POLA CLIP ---")
        print(", ".join(sorted(clip.keys())))

print("\nAnaliza zakonczona.")
