
# ASTRA VIDEO AGENT
## AI Video Editor & Content Production System

# 1. CEL PROJEKTU

Budujemy lokalnego agenta AI do automatycznego
montazu filmow dla marki Behave.

Docelowy model AI: GPT-6 Astra.

Agent ma analizowac poprzednie materialy,
uczyc sie preferencji montazowych uzytkownika,
tworzyc nowe filmy i oceniac ich jakosc.

Docelowym wynikiem jest edytowalny projekt CapCut.

Agent nie moze jedynie kopiowac starych filmow.
Ma rowniez identyfikowac mozliwosci ulepszen.

# 2. DWA TRYBY MONTAZU

## LONG FORM - YOUTUBE

Format:
- 16:9
- Dlugosc docelowa: 7-10 minut
- Narracja nagrana przez uzytkownika
- Glownie zdjecia i animacje
- Muzyka i efekty dzwiekowe
- Napisy i elementy graficzne

Workflow:

1. Przyjmij nagrany voice-over.
2. Wykonaj transkrypcje.
3. Podziel narracje na fragmenty tematyczne.
4. Przeanalizuj dostepne zdjecia.
5. Dobierz zdjecia do konkretnych fragmentow.
6. Ustal tempo montazu.
7. Dodaj zoom, pan i animacje.
8. Dopasuj muzyke i efekty dzwiekowe.
9. Dodaj napisy i elementy graficzne.
10. Wygeneruj edytowalny projekt CapCut.
11. Sprawdz jakosc gotowego materialu.
12. Zaproponuj ewentualne poprawki.

Pamiec stylu:
memory/behave_style.json

## SHORT FORM - SHORTS / TIKTOK / REELS

Format:
- 9:16
- Dlugosc dopasowana do narracji
- Dynamiczny montaz
- Mocny hook w pierwszych sekundach
- Materialy B-roll dostarczone przez uzytkownika
- Napisy zsynchronizowane z narracja
- Muzyka i efekty dzwiekowe

Workflow:

1. Przyjmij nagrany voice-over.
2. Wykonaj transkrypcje z timestampami.
3. Podziel narracje na fragmenty znaczeniowe.
4. Przeanalizuj dostarczone materialy B-roll.
5. Rozpoznaj sceny i zawartosc nagran.
6. Zidentyfikuj pasujace fragmenty wideo.
7. Dobierz B-roll do znaczenia narracji.
8. Wytnij odpowiednie fragmenty z nagran.
9. Zsynchronizuj je z voice-overem.
10. Dodaj napisy, animacje i przejscia.
11. Dodaj muzyke oraz efekty dzwiekowe.
12. Wygeneruj edytowalny projekt CapCut.
13. Przeprowadz kontrole jakosci.
14. Zaproponuj poprawki.

Pamiec stylu:
memory/behave_shorts_style.json

Ten plik pamieci Shorts powstanie w pozniejszym etapie.

# 3. INTELIGENTNY WYBOR B-ROLL

Najwazniejsza funkcja trybu SHORT.

Agent nie moze losowo wybierac fragmentow wideo.

Musi rozumiec:
- Co uzytkownik mowi.
- Co znajduje sie na dostarczonym nagraniu.
- Ktory fragment najlepiej pasuje do narracji.
- W ktorym momencie powinien nastapic montaz.

Przyklad:

Narracja:
"Malinois to pies o ogromnej ilosci energii."

Oczekiwany B-roll:
Dynamiczny fragment przedstawiajacy biegajacego
lub intensywnie trenujacego malinois.

Narracja:
"Ta rasa wykorzystywana jest przez policje."

Oczekiwany B-roll:
Fragment pokazujacy psa podczas szkolenia
policyjnego lub pracy sluzbowej.

## Zasady wyboru

- Dobieraj obraz na podstawie jego znaczenia.
- Nie uzywaj przypadkowych ujec.
- Unikaj pokazywania niewlasciwej rasy psa.
- Unikaj niepotrzebnego powtarzania ujec.
- Wybieraj czytelne i dobre jakosciowo fragmenty.
- Synchronizuj zmiany ujec z narracja.
- Uwzgledniaj tempo wypowiedzi.
- Zachowuj oryginalne materialy bez zmian.
- Nie korzystaj z materialow bez odpowiednich praw.
- Gdy brakuje pasujacego ujecia, zglos problem.

Dla kazdego wybranego fragmentu zapisz:
- Nazwe pliku zrodlowego.
- Czas poczatku fragmentu.
- Czas konca fragmentu.
- Fragment narracji, do ktorego pasuje.
- Uzasadnienie wyboru.

Analiza wizualna B-roll musi byc rzeczywiscie
wykonana przez podlaczone narzedzia.
Nie wolno zgadywac zawartosci nagrania.

# 4. ANALIZA STARYCH PROJEKTOW CAPCUT

Agent powinien analizowac:
- Liczbe sciezek.
- Rodzaje materialow.
- Czasy wyswietlania zdjec.
- Dlugosc fragmentow wideo.
- Klatki kluczowe (keyframes).
- Zoom i przesuniecia.
- Animacje i przejscia.
- Elementy tekstowe.
- Muzyke i efekty dzwiekowe.
- Rozmieszczenie elementow na osi czasu.

Agent powinien tworzyc osobne profile montazu
dla LONG FORM i SHORT FORM.

## Aktualnie zebrane dane

Liczba wykrytych projektow CapCut: 429.

Projekt referencyjny:
Bullterrier - LONG-kopia

Dane:
- Liczba sciezek: 15
- Liczba elementow: 341
- Zdjecia: 179
- Wideo: 37
- Tekst: 25
- Audio: 100
- Mediana dlugosci zdjecia: 3.07 sekundy
- Elementy z wykrytymi keyframes: 56
- Czas projektu: okolo 7.86 minuty

Te dane opisuja jeden projekt.
Nie sa jeszcze uniwersalnymi zasadami montazu.

# 5. PAMIEC MONTAZOWA

Agent musi korzystac z zapisanej pamieci stylu.

Pamiec powinna zawierac:
- Preferowane tempo montazu.
- Typowe animacje.
- Schematy hookow.
- Sposob wykorzystania napisow.
- Preferencje muzyczne.
- Efekty dzwiekowe.
- Zasady wyboru zdjec i B-roll.
- Zasady kompozycji.
- Zaakceptowane poprawki uzytkownika.

Nie nalezy zakladac, ze zapisanie instrukcji
oznacza wytrenowanie modelu.

Pamiec ma byc aktualizowana na podstawie
rzeczywistych analiz i zatwierdzonych zmian.

# 6. KONTROLA JAKOSCI MONTAZU

Agent powinien oceniac gotowe materialy
i proponowac mozliwosci poprawy.

Analizuj:
- Jakosc pierwszych sekund filmu.
- Czy obraz pasuje do narracji.
- Tempo i rytm montazu.
- Dlugosc poszczegolnych ujec.
- Czytelnosc napisow.
- Jakosc animacji.
- Poziomy glosnosci.
- Synchronizacje efektow dzwiekowych.
- Powtarzajace sie ujecia.
- Potencjalnie nudne fragmenty.
- Bledy techniczne.

W raporcie podawaj:
1. Timestamp problemu.
2. Opis problemu.
3. Proponowana poprawke.
4. Uzasadnienie poprawki.
5. Priorytet poprawki.

Agent nie moze wymyslac bledow.

Ocena wizualna wymaga dostepu do rzeczywistego
obrazu z filmu, a ocena dzwieku do jego audio.

Nie wykonuj istotnych zmian kreatywnych
bez zatwierdzenia przez uzytkownika.

# 7. AUTOMATYCZNE TWORZENIE PROJEKTOW

Docelowe mozliwosci:

- Tworzenie nowych projektow CapCut.
- Dodawanie zdjec i materialow wideo.
- Przycinanie B-roll.
- Synchronizacja z voice-overem.
- Dodawanie napisow.
- Dodawanie animacji i keyframes.
- Dodawanie muzyki i efektow.
- Zapisywanie edytowalnych projektow.
- Aktualizowanie projektow po poprawkach.

Nie zakladaj zgodnosci z formatem CapCut,
dopoki nie zostanie potwierdzona testami.

Kazda wygenerowana os czasu musi przejsc test:
- Czy projekt otwiera sie w CapCut?
- Czy media sa prawidlowo podlinkowane?
- Czy czasy ujec sa poprawne?
- Czy animacje dzialaja?
- Czy audio jest zsynchronizowane?
- Czy projekt mozna dalej edytowac?

# 8. STRUKTURA PROJEKTU

astra-video-agent/

agent.py
AGENTS.md

inputs/
    Nowe nagrania i materialy.

references/
    Poprzednie filmy i projekty CapCut.

outputs/
    Wygenerowane projekty.

memory/
    behave_style.json
    behave_shorts_style.json (planowany)

tools/
    capcut_scan.py
    capcut_analyze.py
    capcut_style_scan.py

# 9. ZASADY BEZPIECZENSTWA

- Nigdy nie modyfikuj oryginalnych projektow.
- Pracuj na kopiach.
- Nie usuwaj plikow bez zgody.
- Nie ujawniaj kluczy API.
- Nie wysylaj materialow bez zgody.
- Nie uruchamiaj platnych uslug bez zgody.
- Nie nadpisuj pamieci bez kopii zapasowej.
- Nie twierdz, ze film zostal przeanalizowany,
  jezeli odczytano jedynie jego metadane.
- W przypadku bledu przerwij niebezpieczna
  operacje i przedstaw diagnoze.

# 10. SPOSOB PRACY AGENTA

- Pracuj krok po kroku.
- Testuj kazda funkcje.
- Wyjasniaj zmiany prostym jezykiem.
- Nie wprowadzaj niepotrzebnych zaleznosci.
- Preferuj lokalne narzedzia open-source.
- Optymalizuj koszty API.
- Nie wysylaj niepotrzebnie calych filmow
  do modelu AI.
- Uzywaj transkrypcji i analizy wybranych klatek,
  kiedy jest to wystarczajace.
- Nie wykonuj kosztownych operacji bez zgody.
- Zapisuj wyniki testow.
- Informuj o ograniczeniach narzedzi.

# 11. AKTUALNY STAN PROJEKTU

Zrealizowane:
- Przygotowano Python 3.14.7.
- Zainstalowano biblioteke OpenAI.
- Utworzono strukture folderow.
- Wykryto 429 projektow CapCut.
- Przeanalizowano projekt Bullterrier LONG.
- Rozpoznano typy sciezek i materialow.
- Wykryto czesc klatek kluczowych.
- Utworzono pierwsza pamiec montazowa.
- Utworzono lokalny program agent.py.

Jeszcze niezrealizowane:
- Polaczenie z GPT-6 Astra.
- Analiza wizualna gotowych filmow.
- Analiza B-roll.
- Automatyczne dopasowywanie ujec.
- Pelna analiza animacji CapCut.
- Automatyczny montaz.
- Generowanie edytowalnych projektow.
- Automatyczny audyt jakosci.

# 12. NAJBLIZSZE ZADANIE

Zbadac strukture klatek kluczowych
w istniejacych projektach CapCut.

Nastepnie:
1. Zidentyfikowac parametry animacji.
2. Opracowac analize stylu SHORT.
3. Dodac pamiec dla Shorts.
4. Przygotowac indeksowanie B-roll.
5. Zbudowac pierwszy generator projektu.
6. Sprawdzic wynik na kopii projektu.

# CEL KONCOWY

Uzytkownik powinien moc wydac polecenie:

"Zmontuj mi nowy film o rottweilerze na
podstawie nagranego glosu, korzystajac
z mojego stylu i dostepnych materialow."

Agent powinien przeanalizowac materialy,
przygotowac montaz, wykonac kontrole jakosci
i zapisac edytowalny projekt CapCut.

Dla Shorts agent dodatkowo powinien
samodzielnie wybierac odpowiednie fragmenty
dostarczonych nagran B-roll.
