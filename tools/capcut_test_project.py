
import os
import shutil
from pathlib import Path

# Folder naszego agenta
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder projektow CapCut
CAPCUT_DIR = (
    Path(os.environ["LOCALAPPDATA"])
    / "CapCut"
    / "User Data"
    / "Projects"
    / "com.lveditor.draft"
)

# Projekt referencyjny
PROJECT_NAME = "Bullterrier - LONG-kopia"

# Folder wyjsciowy
OUTPUT_DIR = (
    BASE_DIR
    / "outputs"
    / "Bullterrier_ASTRA_TEST"
)

print("\n=== ASTRA PROJECT CLONER ===")

# Znajdz dokladnie jeden projekt
matches = [
    p.parent
    for p in CAPCUT_DIR.rglob("draft_content.json")
    if p.parent.name == PROJECT_NAME
]

if len(matches) != 1:
    print("Nie znaleziono jednego projektu.")
    print("Liczba dopasowan:", len(matches))
    raise SystemExit(1)

source = matches[0]

# Nigdy nie nadpisujemy istniejacej kopii
if OUTPUT_DIR.exists():
    print("Folder testowy juz istnieje.")
    print(OUTPUT_DIR)
    raise SystemExit(1)

print("Projekt zrodlowy:", PROJECT_NAME)
print("Tworzenie kopii...")

# Kopiujemy caly folder projektu
shutil.copytree(source, OUTPUT_DIR)

# Sprawdzamy wynik
draft = OUTPUT_DIR / "draft_content.json"

if draft.is_file():
    print("\nSUKCES!")
    print("Utworzono kopie projektu:")
    print(OUTPUT_DIR)
    print("\nOryginalny projekt pozostal bez zmian.")
else:
    print("Brak draft_content.json w kopii.")
    raise SystemExit(1)
