
import json
import os
from pathlib import Path
from openai import OpenAI


# ==========================================
# 1. KONFIGURACJA
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "memory"

MEMORY_DIR.mkdir(exist_ok=True)

MODEL = "gpt-6-astra"

CURRENT_MODE = "LONG"


# ==========================================
# 2. PROFILE MONTAZU
# ==========================================

MODES = {
    "LONG": {
        "name": "YouTube Long Form",
        "format": "16:9",
        "duration": "7-10 minut",
        "memory_file": "behave_style.json",
        "description": (
            "Montaz z nagranego glosu, zdjec, "
            "animacji, muzyki i efektow."
        )
    },

    "SHORT": {
        "name": "Shorts / TikTok / Reels",
        "format": "9:16",
        "duration": "Wedlug narracji",
        "memory_file": "behave_shorts_style.json",
        "description": (
            "Dynamiczny montaz z voice-overem "
            "i inteligentnym wyborem B-roll."
        )
    }
}


# ==========================================
# 3. WCZYTYWANIE PAMIECI STYLU
# ==========================================

def load_style(mode):
    filename = MODES[mode]["memory_file"]
    path = MEMORY_DIR / filename

    if not path.exists():
        return {
            "mode": mode,
            "status": "Brak przeanalizowanych projektow",
            "reference_projects": [],
            "style_learned": False
        }

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


# ==========================================
# 4. HISTORIA ROZMOW
# ==========================================

def history_path(mode):
    return MEMORY_DIR / f"chat_{mode.lower()}.json"


def load_history(mode):
    path = history_path(mode)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            history = json.load(file)

        if isinstance(history, list):
            return history

    except (OSError, json.JSONDecodeError):
        print("Nie udalo sie odczytac historii.")

    return []


def save_history(mode, history):
    path = history_path(mode)

    # Zachowujemy maksymalnie 40 wiadomosci
    history = history[-40:]

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            ensure_ascii=False,
            indent=2
        )


# ==========================================
# 5. INSTRUKCJE DLA ASTRY
# ==========================================

def build_instructions(mode):
    style = load_style(mode)
    profile = MODES[mode]

    common = """
    Jestes Astra Video Agent.

    Pracujesz dla marki Behave.

    Jestes specjalista od:
    - montazu filmow YouTube
    - montazu Shorts, Reels i TikTok
    - analizy narracji
    - animacji i synchronizacji audio
    - kontroli jakosci montazu

    Twoim celem jest tworzenie profesjonalnych
    edytowalnych projektow CapCut.

    Zasady:
    - Pracuj na kopiach projektow.
    - Nie zmieniaj oryginalnych plikow.
    - Nie wymyslaj wynikow analiz.
    - Nie udawaj, ze obejrzales film,
      jesli masz tylko jego metadane.
    - Nie twierdz, ze wykonales montaz,
      jesli narzedzia montazowe nie sa podlaczone.
    - Proponuj ulepszenia montazu.
    - Uwzgledniaj preferencje uzytkownika.
    - Nie korzystaj z materialow bez odpowiednich praw.
    - Przed istotnymi zmianami kreatywnymi
      uzyskaj akceptacje uzytkownika.
    """

    long_rules = """
    TRYB LONG FORM

    Format: 16:9
    Docelowa dlugosc: 7-10 minut

    Uzytkownik dostarcza nagrany glos.

    Docelowy proces:
    1. Analiza voice-over.
    2. Transkrypcja narracji.
    3. Podzial na sceny.
    4. Dobor zdjec do narracji.
    5. Planowanie zoom i pan.
    6. Dodawanie animacji.
    7. Synchronizacja muzyki i efektow.
    8. Tworzenie projektu CapCut.
    9. Kontrola jakosci filmu.

    Preferuj zdjecia i animacje.
    Korzystaj z pamieci stylu LONG.
    """

    short_rules = """
    TRYB SHORT FORM

    Format: 9:16
    Platformy: TikTok, Instagram Reels,
    YouTube Shorts.

    Uzytkownik dostarcza:
    - voice-over
    - materialy wideo B-roll

    Docelowy proces:
    1. Transkrypcja voice-over z timestampami.
    2. Analiza znaczenia wypowiedzi.
    3. Analiza scen w dostarczonych B-roll.
    4. Dobor scen do konkretnych wypowiedzi.
    5. Wycinanie pasujacych fragmentow.
    6. Synchronizacja z narracja.
    7. Dodanie napisow i animacji.
    8. Dodanie muzyki i efektow.
    9. Wygenerowanie projektu CapCut.
    10. Kontrola jakosci.

    ZASADY B-ROLL:
    - Nigdy nie wybieraj klipow losowo.
    - Dopasuj obraz do znaczenia wypowiedzi.
    - Unikaj niewlasciwych ras psow.
    - Nie powtarzaj niepotrzebnie ujec.
    - Zachowuj oryginalne nagrania.
    - Zapisuj zrodlo i timestampy fragmentow.
    - Gdy brak dobrego ujecia, zglos to.

    Stosuj mocne hooki i dynamiczny montaz.
    Korzystaj z osobnej pamieci Shorts.
    """

    selected_rules = (
        long_rules if mode == "LONG" else short_rules
    )

    return f"""
    {common}

    {selected_rules}

    AKTYWNY TRYB:
    {profile["name"]}

    PAMIEC STYLU:
    {json.dumps(style, ensure_ascii=False, indent=2)}

    Aktualnie masz dostep jedynie do danych
    tekstowych przekazanych w tej rozmowie.

    Narzedzia do rzeczywistej analizy wideo
    i modyfikacji CapCut zostana podlaczone
    w kolejnych etapach.
    """


# ==========================================
# 6. STATUS AGENTA
# ==========================================

def show_status(mode):
    profile = MODES[mode]
    style = load_style(mode)
    history = load_history(mode)

    print("\n=== STATUS AGENTA ===")
    print("Model:", MODEL)
    print("Tryb:", mode)
    print("Format:", profile["format"])
    print("Dlugosc:", profile["duration"])
    print("Wiadomosci w historii:", len(history))

    references = style.get("reference_projects", [])
    print("Projekty w pamieci:", len(references))

    if os.getenv("OPENAI_API_KEY"):
        print("API: Klucz ustawiony")
    else:
        print("API: Niepodlaczone")

    print("Montaz CapCut: Jeszcze niepodlaczony")
    print("Analiza B-roll: Jeszcze niepodlaczona")


# ==========================================
# 7. ROZMOWA Z ASTRA
# ==========================================

def ask_astra(mode, message):
    if not os.getenv("OPENAI_API_KEY"):
        print("\nBrak klucza OPENAI_API_KEY.")
        print("Mozesz korzystac z komend lokalnych.")
        print("Rozmowa AI wymaga podlaczenia API.")
        return

    history = load_history(mode)

    # Ograniczamy kontekst, aby kontrolowac koszty
    recent_history = history[-12:]

    messages = recent_history + [
        {
            "role": "user",
            "content": message
        }
    ]

    try:
        client = OpenAI(max_retries=0)

        response = client.responses.create(
            model=MODEL,
            instructions=build_instructions(mode),
            input=messages,
            max_output_tokens=4000
        )

        answer = response.output_text

        if not answer:
            print("\nModel nie zwrocil odpowiedzi tekstowej.")
            return

        print("\nASTRA:")
        print(answer)

        history.append({
            "role": "user",
            "content": message
        })

        history.append({
            "role": "assistant",
            "content": answer
        })

        save_history(mode, history)

        if response.usage:
            print(
                "\nTokeny:",
                response.usage.input_tokens,
                "wejscie /",
                response.usage.output_tokens,
                "wyjscie"
            )

    except Exception as error:
        print("\nBlad komunikacji z API:")
        print(error)


# ==========================================
# 8. GLOWNY PROGRAM
# ==========================================

def main():
    mode = CURRENT_MODE

    print("\n================================")
    print("       ASTRA VIDEO AGENT")
    print("================================")

    print("Model:", MODEL)
    print("Marka: Behave")
    print("Dostepne tryby: LONG / SHORT")

    print("\nKomendy:")
    print("/long   - Montaz dlugich filmow")
    print("/short  - Montaz Shorts")
    print("/status - Status agenta")
    print("/help   - Lista komend")
    print("/exit   - Zakoncz program")

    show_status(mode)

    while True:
        message = input(f"\n[{mode}] Ty: ").strip()

        if not message:
            continue

        command = message.lower()

        if command == "/exit":
            print("\nAstra Video Agent zakonczyl prace.")
            break

        elif command == "/long":
            mode = "LONG"
            print("\nPrzelaczono na LONG FORM.")

        elif command == "/short":
            mode = "SHORT"
            print("\nPrzelaczono na SHORT FORM.")

        elif command == "/status":
            show_status(mode)

        elif command == "/help":
            print("\n/long - Tryb LONG")
            print("/short - Tryb SHORT")
            print("/status - Status")
            print("/exit - Wyjscie")

        else:
            ask_astra(mode, message)


# ==========================================
# 9. START
# ==========================================

if __name__ == "__main__":
    main()
