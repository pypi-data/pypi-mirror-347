# coBoarding

coBoarding to kompleksowy, kontenerowy system do automatycznego wypełniania formularzy rekrutacyjnych, kładący nacisk na prywatność, elastyczność oraz wsparcie wielojęzyczne.

## Główne cechy
- Architektura oparta na Docker (moduły: browser-service, llm-orchestrator, novnc, web-interface)
- 100% lokalne przetwarzanie danych (prywatność)
- Wykrywanie sprzętu (GPU/CPU, RAM) i automatyczny dobór modelu LLM
- Wielojęzyczność (PL, DE, EN) z automatyczną detekcją
- Nowoczesny web UI z HTTPS i sterowaniem głosowym
- Automatyczna generacja pipelines dla portali pracy
- Wizualizacja procesu przez noVNC
- Integracja z menedżerami haseł (Bitwarden, PassBolt)
- Kompletne środowisko testowe

## 📚 Spis treści / Menu
- [Szybki start](#szybki-start)
- [Instalacja środowiska (Python 3.11+ / 3.12 na Ubuntu 24.10+)](#instalacja-środowiska-python-311--312-na-ubuntu-2410)
- [Struktura kontenerów](#struktura-kontenerów)
- [Weryfikacja wdrożenia](#weryfikacja-wdrożenia)
- [Scenariusze testowe](#scenariusze-testowe)
- [FAQ](#faq)
- [Kontakt i wsparcie](#kontakt-i-wsparcie)

## Szybki start

```bash
git clone https://github.com/coboarding/coboarding.git
cd coBoarding
bash install.sh  # automatyczna instalacja zależności i Docker Compose v2
bash run.sh      # lub ./run.ps1 na Windows
```

Pierwsze uruchomienie automatycznie skonfiguruje środowisko (venv, zależności, kontenery, Docker Compose v2).

> **WAŻNE:** Projekt wymaga Docker Compose v2 (polecenie `docker compose`). Skrypt `install.sh` instaluje go automatycznie jako plugin CLI.

## Instalacja środowiska (Python 3.11+ / 3.12 na Ubuntu 24.10+)

Aby uniknąć problemów z kompatybilnością (np. PyAudio vs Python 3.12), zalecane jest użycie Pythona 3.11. **Na Ubuntu 24.10+ dostępny jest tylko Python 3.12 – patrz uwaga poniżej!**

```bash
# (Linux/Ubuntu) Instalacja wymaganych pakietów
sudo apt-get update && sudo apt-get install python3.11 python3.11-venv python3.11-dev
# Na Ubuntu 24.10+:
sudo apt-get install python3.12 python3.12-venv python3.12-dev

# Utworzenie i aktywacja środowiska wirtualnego
python3.11 -m venv venv-py311   # lub
python3.12 -m venv venv-py312   # na Ubuntu 24.10+
source venv-py311/bin/activate  # lub
source venv-py312/bin/activate

# Instalacja zależności
pip install --upgrade pip
pip install -r requirements.txt
```

Możesz także użyć skryptu:
```bash
bash install.sh  # automatyczna instalacja Docker Compose v2 (plugin CLI)
```

Po instalacji Compose v2 dostępne będzie jako polecenie:
```bash
docker compose version
```

> **Uwaga dot. PyAudio i Python 3.12:**
> PyAudio nie jest kompatybilne z Python 3.12 (błąd: `pkgutil.ImpImporter`).
> - Jeśli nie potrzebujesz funkcji audio, możesz usunąć PyAudio z `requirements.txt`.
> - Jeśli potrzebujesz PyAudio, spróbuj zainstalować [nieoficjalny wheel z https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) (tylko Windows), lub rozważ alternatywę np. `sounddevice`.
> - Możesz też użyć środowiska z Pythonem 3.11 (np. Docker, starsze Ubuntu).

## Struktura kontenerów
- **browser-service**: Selenium, Chrome/Firefox
- **llm-orchestrator**: API do analizy formularzy, wykrywanie sprzętu, zarządzanie modelami LLM (torch, transformers, langchain)
- **novnc**: Podgląd przeglądarki
- **web-interface**: React, HTTPS, Web Speech API

## Weryfikacja wdrożenia
- Czy docker-compose.yml zawiera wszystkie kontenery i wolumeny?
- Czy skrypty inicjalizacyjne wykrywają sprzęt?
- Czy web-interface jest dostępny przez HTTPS?
- Czy API llm-orchestrator działa?
- Czy testy przechodzą dla przykładowych formularzy?

## Scenariusze testowe
- Wypełnianie prostego i złożonego formularza
- Test wielojęzyczności
- Test podglądu przez noVNC
- Test integracji z menedżerem haseł

## Dokumentacja
Szczegółowe prompty i pytania weryfikacyjne znajdziesz w pliku `TODO.txt`.

## Kontakt i wsparcie
Projekt open-source. Wszelkie zgłoszenia błędów i propozycje zmian prosimy kierować przez Issues na GitHub.


# coBoarding

System do automatycznego wypełniania formularzy internetowych wykorzystujący lokalne modele językowe (LLM) w trzech językach (polski, niemiecki, angielski) bazujący na danych z CV.

![coBoarding Logo](https://via.placeholder.com/800x200/3498db/ffffff?text=coBoarding)

## Funkcjonalności

- **Automatyczne wykrywanie formularzy** na stronach internetowych
- **Inteligentne dopasowywanie danych z CV** do pól formularza
- **Obsługa trzech języków**: polski, niemiecki, angielski - automatyczne wykrywanie języka formularza
- **Lokalna analiza językowa** z wykorzystaniem modeli LLM (bez wysyłania danych do zewnętrznych API)
- **Wsparcie dla różnych formatów CV**: HTML, PDF, DOCX
- **Pełna automatyzacja** procesu wypełniania formularzy rekrutacyjnych
- **Zrzuty ekranu** wypełnionych formularzy do weryfikacji

## Wymagania systemowe

- Docker i Docker Compose
- Minimum 8GB RAM (zalecane 16GB)
- Minimum 10GB wolnego miejsca na dysku
- Połączenie z internetem (tylko do pobierania modeli LLM przy pierwszym uruchomieniu)

## Szybki start

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/coboarding/coboarding.git
cd coBoarding
```

### 2. Przygotuj CV

Umieść swoje CV w katalogu `cv/` w jednym z obsługiwanych formatów (HTML, PDF, DOCX).

### 3. Utwórz plik z adresami URL

Utwórz plik `urls.txt` z adresami stron zawierających formularze rekrutacyjne:

```
https://example.com/job-application1
https://example.com/job-application2
```

### 4. Uruchom skrypt startowy

```bash
chmod +x run.sh
./run.sh
```

Skrypt przeprowadzi Cię przez proces uruchomienia systemu.

## Szczegółowa konfiguracja

Możesz dostosować działanie systemu edytując plik `config.ini`:

```ini
[CV]
path = /app/cv/cv_tom_sapletta_2025_de.html

[LLM]
model_path = /app/models/mistral.gguf
model_type = llama
device = cpu

[Browser]
type = chrome
headless = true

[Output]
directory = /app/output
```

### Dostępne modele LLM

System domyślnie używa modelu Mistral, ale możesz użyć jednego z następujących modeli:

- `mistral.gguf` - Mistral 7B (domyślny, dobry kompromis między jakością a wymaganiami)
- `llama-2-7b.gguf` - Llama 2 7B (alternatywa)
- `falcon-7b.gguf` - Falcon 7B (alternatywa)

Większe modele (13B, 70B) zapewniają lepszą jakość, ale wymagają więcej zasobów.

## Tryby działania

System można uruchomić w trzech trybach:

1. **Tryb wsadowy** - przetwarzanie wszystkich adresów URL z pliku:
   ```bash
   python main.py --config config.ini --urls-file urls.txt
   ```

2. **Tryb pojedynczego URL** - przetwarzanie pojedynczego adresu:
   ```bash
   python main.py --config config.ini --url https://example.com/job-application
   ```

3. **Tryb interaktywny** - do debugowania (tylko w Dockerze):
   ```bash
   # W docker-compose.yml zmień command: sleep infinity
   docker-compose up -d
   docker exec -it coBoarding bash
   ```

## Obsługa błędów

### Typowe problemy

1. **Problem:** Kontener Docker kończy działanie z błędem
   **Rozwiązanie:** Sprawdź logi: `docker-compose logs`

2. **Problem:** Formularze nie są poprawnie wykrywane
   **Rozwiązanie:** Niektóre strony używają niestandardowego JavaScript. Spróbuj uruchomić w trybie nieheadless.

3. **Problem:** Model LLM nie jest pobierany automatycznie
   **Rozwiązanie:** Pobierz model ręcznie i umieść go w katalogu `models/`

## Szczegółowe logowanie i debugowanie

W plikach Dockerfile, `install.sh` oraz `run.sh` zostały dodane szczegółowe komunikaty [DEBUG] oraz [INFO].

- Każdy kluczowy etap instalacji, budowy obrazu i uruchamiania usług jest logowany.
- Logi pomagają szybko zlokalizować miejsce, gdzie wystąpił problem.
- W terminalu zobaczysz wyraźne komunikaty o postępie i ewentualnych błędach.

**Wskazówka:**
Jeśli coś pójdzie nie tak, sprawdź logi [DEBUG] w konsoli — wskażą, na którym etapie pojawił się problem.

## Jak to działa

1. System analizuje CV użytkownika, parsując kluczowe informacje (doświadczenie, umiejętności, wykształcenie).
2. Dla każdego URL, system uruchamia zautomatyzowaną przeglądarkę i wykrywa formularze na stronie.
3. Lokalny model LLM analizuje strukturę formularza i jego pola.
4. System inteligentnie dopasowuje dane z CV do pól formularza, tłumacząc je na odpowiedni język.
5. Formularz jest automatycznie wypełniany, a zrzut ekranu jest zapisywany do weryfikacji.

## Bezpieczeństwo

- Wszystkie dane są przetwarzane lokalnie
- Żadne informacje nie są wysyłane do zewnętrznych API
- Lokalne modele LLM zapewniają prywatność danych
- System nie wysyła automatycznie formularzy - tylko je wypełnia

## Licencja

Ten projekt jest udostępniany na licencji MIT. Szczegółowe informacje można znaleźć w pliku LICENSE.

## Autor

Tom Sapletta

## Współpraca

Chętnie przyjmujemy Pull Requesty! Aby przyczynić się do rozwoju projektu:

1. Sforkuj repozytorium
2. Utwórz branch z nową funkcjonalnością (`git checkout -b feature/amazing-feature`)
3. Zatwierdź zmiany (`git commit -m 'Add amazing feature'`)
4. Wypchnij branch (`git push origin feature/amazing-feature`)
5. Otwórz Pull Request



# Struktura projektu coBoarding

```
coBoarding/
├── cv/                                 # Katalog na pliki CV
│   └── cv_tom_sapletta_2025_de.html    # Twoje CV w formacie HTML
│
├── models/                             # Katalog na modele LLM
│   └── mistral.gguf                    # Pobrany automatycznie przy pierwszym uruchomieniu
│
├── output/                             # Katalog na dane wyjściowe (zrzuty ekranu)
│
├── Dockerfile                          # Definicja obrazu Docker
├── docker-compose.yml                  # Konfiguracja Docker Compose
├── config.ini                          # Konfiguracja aplikacji
├── requirements.txt                    # Zależności Pythona
├── main.py                             # Główny skrypt aplikacji
├── run.sh                              # Skrypt do łatwego uruchamiania
├── urls.txt                            # Lista adresów URL do przetworzenia
└── README.md                           # Dokumentacja projektu
```

## Opis plików

### Główne pliki aplikacji

- **main.py**: Główny skrypt aplikacji zawierający całą logikę wypełniania formularzy.
- **config.ini**: Plik konfiguracyjny aplikacji.
- **requirements.txt**: Lista zależności Pythona potrzebnych do działania aplikacji.
- **urls.txt**: Plik z listą adresów URL stron z formularzami do wypełnienia.
- **run.sh**: Skrypt ułatwiający uruchamianie aplikacji.

### Pliki Docker

- **Dockerfile**: Definicja obrazu Docker z potrzebnymi zależnościami.
- **docker-compose.yml**: Konfiguracja Docker Compose do łatwego uruchamiania aplikacji.

### Katalogi danych

- **cv/**: Katalog zawierający pliki CV, z których aplikacja będzie czerpać dane do wypełniania formularzy.
- **models/**: Katalog zawierający modele LLM używane do analizy formularzy i generowania odpowiedzi.
- **output/**: Katalog przechowujący zrzuty ekranu wypełnionych formularzy.

## Kluczowe funkcjonalności

Aplikacja działa w następujący sposób:

1. Parsuje CV użytkownika, aby wydobyć kluczowe informacje.
2. Otwiera stronę internetową z formularzem w zautomatyzowanej przeglądarce.
3. Analizuje formularz za pomocą lokalnego modelu językowego (LLM).
4. Dopasowuje dane z CV do pól formularza, automatycznie tłumacząc je na odpowiedni język (polski, niemiecki, angielski).
5. Wypełnia formularz i wykonuje zrzut ekranu.

Całość działa w kontenerze Docker, co zapewnia łatwą instalację i uruchomienie na różnych systemach operacyjnych.