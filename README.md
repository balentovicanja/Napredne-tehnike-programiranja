# Finance Tracker - Praćenje Osobnih Troškova

## Verzija Pythona

Aplikacija zahtjeva **Python 3.9 ili noviju verziju**.


## Opis Aplikacije

Finance Tracker je desktop aplikacija za praćenje osobnih prihoda i troškova. Aplikacija omogućava korisnicima da:

- **Dodavaju transakcije** - Evidentiranje novih prihoda i troškova sa iznosom, kategorijom, opisom i datumom
- **Pregledavaju transakcije** - Prikaz svih transakcija u tbalici sa mogućnošću sortiranja
- **Filtriraju transakcije** - Filtriranje po kategoriji i tipu (prihod/trošak)
- **Brišu transakcije** - Uklanjanje nepotrebnih zapisa
- **Prate statistiku** - Prikaz ukupnih prihoda, troškova, broja transakcija i detaljnog pregleda po kategorijama
- **Automatski čuvaju podatke** - Automatsko spremanje podataka u JSON datoteku

Aplikacija koristi grafičko sučelje (Tkinter) i podatke sprema u JSON datoteku u `data/expenses.json`.

### Predefinirane Kategorije

Aplikacija dolazi sa sljedećim kategorijama:
- Hrana
- Prijevoz
- Zabava
- Stanovanje
- Zdravstvo
- Obrazovanje
- Plaća
- Ostalo

## Način Pokretanja

### Postavljanje Okruženja
```bash
python -m venv venv
venv\Scripts\activate
```


### Instalacija Ovisnosti

Nakon aktiviranja virtuelnog okruženja, instalirajte sve potrebne pakete:
```bash
pip install -r requirements.txt
```

#### Ovisnosti

Aplikacija koristi sljedeće glavne pakete:

- **Tkinter** - Za grafički interfejs (uglavnom uključen sa Pythonom)
- **python-dateutil** - Za rad sa datumima
- **typing-extensions** - Za dodatne type hint funkcionalnosti
- **pytest** - Za testiranje
- **black, flake8, mypy** - Za kvalitetu koda

### Pokretanje Aplikacije

Aplikacija se može pokrenuti na dva načina:

#### 1. main.py - Osnovna verzija

```bash
python main.py
```

-osnovna verzija aplikacije gdje se podaci spremaju nakon svake akcije

#### 2. main_async.py - Konkurentna Verzija (Preporučena)

```bash
python main_async.py
```

Ovo je verzija sa konkurentnim izvršavanjem background zadataka:
- **Automatsko čuvanje** - automatsko spremanje podataka u pozadini svakih 30s
- **Realtime statistika** - ažuriranje statistike u pozadini svakih 5s

Preporučuje se korištenje `main_async.py` za bolji korisnički doživljaj, posebno tijekom rada sa većim količinama podataka.

### Pokretanje Testova

Za pokretanje testova:
```bash
python run_tests.py
```

## Arhitektura Projekta

```
Finance Tracker/
├── config.py                 # Konfiguracija aplikacije (putanje, kategorije)
├── main.py                   # Entry point osnovne verzije
├── main_async.py             # Entry point konkurentne verzije
├── requirements.txt          # Python ovisnosti
├── run_tests.py              # Script za pokretanje testova
├── data/                     
│   └── expenses.json         # Pohrana transakcija (JSON format)
├── src/
│   ├── models.py             # Podatkovni modeli (Transaction, TransactionStats, Category)
│   ├── business/             # Logika aplikacije
│   │   ├── manager.py        # ExpenseManager - upravljanje transakcijama
│   │   ├── filters.py        # Filtri za filtriranje transakcija
│   │   ├── decorators.py     # Dekoratori za validaciju i logiranje
│   │   └── concurrent.py     # Background radnik, autosave i statistički zadaci
│   ├── gui/                  # Grafički sučelje -> Tkinter
│   │   ├── main_window.py    # Glavni prozor aplikacije
│   │   ├── async_window.py   # Prozor sa konkurentnom podrškom
│   │   └── widgets.py        # GUI komponente
│   └── storage/              
│       ├── base.py           # Apstraktno sučelje za spremanja
│       └── json_storage.py   # JSON implementacija spremanja
└── tests/                    # Testovi     
```




