
import json
import os
from pathlib import Path
from collections import Counter

# Folder projektow CapCut
capcut_path = (
    Path(os.environ["LOCALAPPDATA"])
    / "CapCut"
    / "User Data"
    / "Projects"
    / "com.lveditor.draft"
)

# Analizujemy kopie projektu
project_name = "Bullterrier - LONG-kopia"

project_file = next(
    (
        p for p in capcut_path.rglob("draft_content.json")
        if p.parent.name == project_name
    ),
    None
)

if project_file is None:
    print("Nie znaleziono projektu.")
    raise SystemExit

# Odczyt danych, bez ich modyfikacji
with project_file.open("r", encoding="utf-8-sig") as f:
    data = json.load(f)

tracks = data.get("tracks", [])

print("\n=== ASTRA VIDEO AGENT ===")
print(f"Projekt: {project_name}")
print(f"Liczba sciezek: {len(tracks)}")

track_types = Counter()

total_segments = 0

for track in tracks:
    track_type = track.get("type", "unknown")
    segments = track.get("segments", [])

    track_types[track_type] += 1
    total_segments += len(segments)

print(f"Liczba elementow osi czasu: {total_segments}")

print("\n=== RODZAJE SCIEZEK ===")

for track_type, count in track_types.items():
    print(f"{track_type}: {count}")

print("\n=== SZCZEGOLY SCIEZEK ===")

for i, track in enumerate(tracks, start=1):
    track_type = track.get("type", "unknown")
    segments = track.get("segments", [])

    print(
        f"Sciezka {i}: {track_type} "
        f"| Elementy: {len(segments)}"
    )

print("\nAnaliza zakonczona!")
