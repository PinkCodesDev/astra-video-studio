
import json
import os
from pathlib import Path
from datetime import datetime

# ==========================================
# ASTRA - BROLL LIBRARY SCANNER
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT = BASE_DIR / "memory" / "broll_inventory.json"

VIDEO_EXTENSIONS = {
    ".mp4", ".mov", ".mkv",
    ".avi", ".webm", ".m4v"
}

print("\n=== ASTRA B-ROLL SCANNER ===")

print("\nPodaj sciezke do folderu")
print("z wszystkimi rasami psow.\n")

user_path = input("Folder B-roll: ").strip().strip('"').strip("'")

root = Path(
    os.path.expandvars(user_path)
).expanduser()

if not root.is_dir():
    print("\nBLAD: Folder nie istnieje.")
    raise SystemExit(1)

root = root.resolve()

# ==========================================
# 1. SZUKAMY FOLDEROW RAS
# ==========================================

breed_folders = sorted(
    [p for p in root.iterdir() if p.is_dir()],
    key=lambda p: p.name.lower()
)

inventory = {
    "library_root": str(root),
    "created_at": datetime.now().isoformat(),
    "breeds": {}
}

total_videos = 0

# ==========================================
# 2. SKANUJEMY PLIKI WIDEO
# ==========================================

for folder in breed_folders:

    video_files = sorted(
        [
            p for p in folder.rglob("*")
            if p.is_file()
            and p.suffix.lower() in VIDEO_EXTENSIONS
        ]
    )

    files = []

    for video in video_files:
        files.append({
            "filename": video.name,
            "relative_path": str(video.relative_to(root)),
            "size_mb": round(
                video.stat().st_size / (1024 * 1024), 2
            ),
            "analyzed": False,
            "scenes": []
        })

    inventory["breeds"][folder.name] = {
        "video_count": len(files),
        "files": files
    }

    total_videos += len(files)

# ==========================================
# 3. ZAPISUJEMY INDEKS
# ==========================================

inventory["total_breeds"] = len(breed_folders)
inventory["total_videos"] = total_videos

OUTPUT.parent.mkdir(exist_ok=True, parents=True)

with OUTPUT.open("w", encoding="utf-8") as f:
    json.dump(
        inventory,
        f,
        ensure_ascii=False,
        indent=2
    )

# ==========================================
# 4. RAPORT
# ==========================================

print("\n=== WYNIKI SKANOWANIA ===")

print("Folderow ras:", len(breed_folders))
print("Wszystkich filmow:", total_videos)

print("\nPIERWSZE 15 RAS:")

for breed, info in list(
    inventory["breeds"].items()
)[:15]:
    print(
        f"{breed}: {info['video_count']} filmow"
    )

print("\nIndeks zapisany:")
print(OUTPUT)

print("\nSkanowanie zakonczone!")
