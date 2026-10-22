
import os
import json
import base64
import sys
from pathlib import Path
from openai import OpenAI

BASE = Path(__file__).resolve().parent.parent

FRAMES_ROOT = (
    BASE / "outputs" / "broll_previews" / "Basenji"
)

MODEL = "gpt-6-astra"


def main():
    manifests = list(FRAMES_ROOT.rglob("frames.json"))

    if not manifests:
        print("Nie znaleziono klatek Basenji.")
        return

    manifest_file = max(
        manifests,
        key=lambda p: p.stat().st_mtime
    )

    with manifest_file.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    frames = manifest["frames"]

    print("\n=== ASTRA B-ROLL VISION ===")
    print("Model:", MODEL)
    print("Film:", Path(manifest["source_video"]).name)
    print("Liczba klatek:", len(frames))

    for frame in frames:
        image_path = Path(frame["image_path"])

        if not image_path.is_file():
            print("Brak pliku:", image_path)
            return

        print("Klatka:", frame["time_seconds"], "s")

    # Domyslnie tylko test lokalny
    if "--analyze" not in sys.argv:
        print("\nKlatki sa gotowe do analizy AI.")
        print("Nie wykonano platnego zapytania.")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\nBrak OPENAI_API_KEY.")
        print("Nie wykonano platnego zapytania.")
        return

    output_file = manifest_file.parent / "vision_analysis.json"

    if output_file.exists():
        print("\nAnaliza juz istnieje:")
        print(output_file)
        print("Nie wysylam kolejnego zapytania.")
        return

    content = [{
        "type": "input_text",
        "text": (
            "Przeanalizuj kolejne klatki filmu o psie. "
            "Dla kazdej klatki opisz widoczne zachowanie, "
            "np. bieg, odpoczynek, szczekanie sugerowane "
            "postawa, zabawa lub odsloniete zeby. "
            "Nie diagnozuj agresji na podstawie samego "
            "obrazu. Nie zakladaj, ze slyszysz dzwiek. "
            "Zapisz opis sceny i do jakiej narracji "
            "ujecie moze pasowac. Odpowiadaj po polsku."
        )
    }]

    for frame in frames:
        path = Path(frame["image_path"])

        encoded = base64.b64encode(
            path.read_bytes()
        ).decode("ascii")

        content.append({
            "type": "input_text",
            "text": f"Klatka: {frame['time_seconds']} s"
        })

        content.append({
            "type": "input_image",
            "image_url": (
                f"data:image/jpeg;base64,{encoded}"
            ),
            "detail": "low"
        })

    print("\nWysylam 6 klatek do analizy...")

    client = OpenAI(max_retries=0)

    try:
        response = client.responses.create(
            model=MODEL,
            reasoning={"effort": "low"},
            max_output_tokens=2500,
            input=[{
                "role": "user",
                "content": content
            }]
        )

    except Exception as error:
        print("\nBlad API:", error)
        return

    answer = response.output_text

    print("\n=== ANALIZA ASTRA ===")
    print(answer or "Brak odpowiedzi tekstowej.")

    if answer:
        result = {
            "model": MODEL,
            "source_video": manifest["source_video"],
            "frames": frames,
            "analysis": answer
        }

        with output_file.open(
            "w", encoding="utf-8"
        ) as f:
            json.dump(
                result, f,
                ensure_ascii=False, indent=2
            )

        print("\nZapisano:", output_file)

    if response.usage:
        print("\nTokeny wejscia:",
              response.usage.input_tokens)
        print("Tokeny wyjscia:",
              response.usage.output_tokens)


if __name__ == "__main__":
    main()
