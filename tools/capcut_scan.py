
from pathlib import Path
import os

# Lokalizacja projektów CapCut
capcut_path = (
    Path(os.environ["LOCALAPPDATA"])
    / "CapCut"
    / "User Data"
    / "Projects"
    / "com.lveditor.draft"
)

print("ASTRA VIDEO AGENT")
print("Szukanie projektów CapCut...\n")

if not capcut_path.exists():
    print("Nie znaleziono domyślnego folderu CapCut.")
    print(f"Sprawdzona lokalizacja: {capcut_path}")
else:
    projects = list(capcut_path.rglob("draft_content.json"))

    print(f"Znaleziono projektów: {len(projects)}")

    for project in projects[:10]:
        print(f"Projekt: {project.parent.name}")

    if len(projects) > 10:
        print(f"...i jeszcze {len(projects) - 10} projektów.")
