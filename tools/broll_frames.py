
import json
import hashlib
import subprocess
from pathlib import Path

# ==========================================
# ASTRA - B-ROLL FRAME EXTRACTOR
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

INVENTORY_FILE = (
    BASE_DIR / "memory" / "broll_inventory.json"
)

BREED = "Basenji"

# 1. Wczytaj biblioteke
with INVENTORY_FILE.open("r", encoding="utf-8") as f:
    inventory = json.load(f)

root = Path(inventory["library_root"]).resolve()

breed_data = inventory["breeds"].get(BREED)

if not breed_data or not breed_data["files"]:
    print("Brak filmow dla rasy:", BREED)
    raise SystemExit(1)

# 2. Wybierz pierwszy istniejacy film
video = None

for item in breed_data["files"]:
    candidate = (
        root / item["relative_path"]
    ).resolve()

    if (
        candidate.is_relative_to(root)
        and candidate.is_file()
    ):
        video = candidate
        break

if video is None:
    print("Nie znaleziono dostepnego filmu.")
    raise SystemExit(1)

print("\n=== ASTRA B-ROLL ANALYZER ===")
print("Rasa:", BREED)
print("Plik:", video.name)

# 3. Sprawdz dlugosc nagrania
probe = subprocess.run(
    [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        str(video)
    ],
    capture_output=True,
    text=True,
    check=True
)

probe_data = json.loads(probe.stdout)

duration = float(
    probe_data["format"]["duration"]
)

print("Dlugosc:", round(duration, 2), "sekund")

# 4. Przygotuj folder na klatki
file_hash = hashlib.sha256(
    str(video).encode("utf-8")
).hexdigest()[:10]

output_dir = (
    BASE_DIR
    / "outputs"
    / "broll_previews"
    / BREED
    / f"{video.stem}_{file_hash}"
)

output_dir.mkdir(parents=True, exist_ok=True)

# 5. Pobierz 6 klatek z roznych momentow
positions = [0.10, 0.25, 0.40, 0.55, 0.70, 0.85]

frames = []

for index, fraction in enumerate(positions, 1):

    timestamp = duration * fraction

    output_file = (
        output_dir / f"frame_{index:02d}.jpg"
    )

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-ss", f"{timestamp:.3f}",
        "-i", str(video),
        "-frames:v", "1",
        "-vf", "scale=640:-2",
        "-y",
        str(output_file)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Blad FFmpeg:", result.stderr[-500:])
        continue

    if not output_file.exists():
        continue

    frames.append({
        "time_seconds": round(timestamp, 3),
        "image_path": str(output_file)
    })

    print(
        f"Klatka {index}: "
        f"{timestamp:.2f} s"
    )

# 6. Zapisz manifest klatek
manifest = {
    "breed": BREED,
    "source_video": str(video),
    "duration_seconds": duration,
    "frames": frames
}

manifest_file = output_dir / "frames.json"

with manifest_file.open("w", encoding="utf-8") as f:
    json.dump(
        manifest,
        f,
        ensure_ascii=False,
        indent=2
    )

print("\n=== WYNIK ===")
print("Zapisanych klatek:", len(frames))
print("Folder:", output_dir)
print("Manifest:", manifest_file)
print("\nAnaliza lokalna zakonczona!")
