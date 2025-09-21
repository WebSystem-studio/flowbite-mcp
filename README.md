# Flowbite MCP Server

Model Context Protocol (MCP) server pre generovanie a správu Flowbite komponentov. Umožňuje AI asistentom (Claude, Cursor, atď.) vytvárať, upravovať a navrhovať Flowbite komponenty pomocou štandardizovaného protokolu.

## 🚀 Funkcie

- **Generovanie komponentov**: Automatické vytváranie Flowbite komponentov
- **Validácia kódu**: Kontrola správnosti a kvality komponentov
- **Inteligentné návrhy**: AI-powered odporúčania pre komponenty
- **Dark mode podpora**: Automatická podpora tmavého režimu
- **Responsive design**: Generovanie responzívnych komponentov
- **Accessibility**: Dodržiavanie WCAG štandardov

## 📦 Podporované komponenty

### Aktuálne implementované
- ✅ **Button**: Tlačidlá všetkých variantov (primary, secondary, success, danger, warning)
- ✅ **Form**: Prihlasovací, registračný a kontaktný formulár
- 🔄 **Input**: Vstupné polia (v príprave)
- 🔄 **Navbar**: Navigačné lišty (v príprave)

### Plánované
- 📋 Card: Karty pre obsah
- 📋 Modal: Modálne okná
- 📋 Dropdown: Rozbaľovacie menu
- 📋 Alert: Upozornenia
- 📋 Breadcrumb: Navigačná cesta
- 📋 Pagination: Stránkovanie

## 🛠️ Inštalácia

### Predpoklady
- Python 3.8+
- pip package manager

### Kroky inštalácie

1. **Klónovanie repozitára**
```bash
git clone https://github.com/flowbite/flowbite-mcp-server.git
cd flowbite-mcp-server
```

2. **Vytvorenie virtuálneho prostredia**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# alebo
venv\\Scripts\\activate  # Windows
```

3. **Inštalácia závislostí**
```bash
pip install -r requirements.txt
```

4. **Konfigurácia**
```bash
cp .env.example .env
# Upravte .env súbor podľa potreby
```

5. **Spustenie servera**
```bash
python -m src.server
```

## ⚙️ Konfigurácia pre Claude Desktop

Pridajte do vašej Claude Desktop konfigurácie:

```json
{
  "mcpServers": {
    "flowbite": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/flowbite-mcp-server",
      "env": {
        "PYTHONPATH": "/path/to/flowbite-mcp-server"
      }
    }
  }
}
```

## 🎯 Použitie

### Generovanie tlačidla
```
Vytvor mi primary button s textom 'Odoslať'
```

### Generovanie formulára
```
Vygeneruj login form s email a password políčkami
```

### Validácia komponentu
```
Skontroluj tento Flowbite kód: [vložený kód]
```

### Inteligentné návrhy
```
Aké komponenty potrebujem pre dashboard aplikáciu?
```

## 🛠️ API

### Tools (Nástroje)

#### `generate_button`
Generuje Flowbite button komponent.

**Parametre:**
- `text` (string): Text tlačidla
- `variant` (string): Variant (primary, secondary, success, warning, danger)
- `size` (string): Veľkosť (xs, sm, md, lg, xl)
- `disabled` (bool): Či je tlačidlo vypnuté
- `icon` (string): CSS trieda pre ikonu
- `href` (string): URL odkaz
- `outline` (bool): Outline štýl

#### `generate_form`
Generuje Flowbite form komponent.

**Parametre:**
- `fields` (array): Zoznam polí formulára
- `submit_text` (string): Text submit tlačidla
- `method` (string): HTTP metóda
- `action` (string): URL akcie
- `validation` (bool): Zahrnúť validačné štýly
- `dark_mode` (bool): Dark mode štýly

#### `validate_component`
Validuje Flowbite komponent kód.

**Parametre:**
- `html_code` (string): HTML kód na validáciu
- `component_type` (string): Typ komponentu

### Resources (Zdroje)

#### `flowbite://components/{component_type}`
Vráti všetky komponenty daného typu.

#### `flowbite://documentation/getting-started`
Dokumentácia pre začiatočníkov.

## 🏗️ Štruktúra projektu

```
flowbite-mcp-server/
├── src/
│   ├── server.py              # Hlavný MCP server
│   ├── config.py             # Konfigurácia
│   ├── models/
│   │   ├── component.py      # Dátové modely
│   │   └── schema.py         # Validačné schémy
│   ├── tools/               # MCP nástroje
│   ├── resources/           # MCP zdroje
│   ├── templates/           # Šablóny komponentov
│   └── utils/               # Utility funkcie
├── data/
│   ├── components/          # Databáza komponentov
│   ├── examples/            # Príklady použitia
│   └── schemas/             # JSON schémy
├── tests/                   # Unit testy
├── requirements.txt         # Python závislosti
├── pyproject.toml          # Projekt konfigurácia
└── README.md               # Dokumentácia
```

## 🧪 Testovanie

```bash
# Spustenie všetkých testov
pytest

# Spustenie s pokrytím
pytest --cov=src

# Spustenie konkrétneho testu
pytest tests/test_components.py
```

## 📚 Dokumentácia

- [Kompletná špecifikácia](.doc/flowbite_mcp_spec.md)
- [Pokrok vo vývoji](PROGRESS.md)
- [Flowbite dokumentácia](https://flowbite.com/docs/)
- [MCP špecifikácia](https://spec.modelcontextprotocol.io/)

## 🤝 Prispievanie

1. Fork repozitár
2. Vytvorte feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit zmeny (`git commit -m 'Add AmazingFeature'`)
4. Push do branch (`git push origin feature/AmazingFeature`)
5. Otvorte Pull Request

## 📝 Licencia

Tento projekt je licencovaný pod MIT licenciou. Pozrite si [LICENSE](LICENSE) súbor pre detaily.

## 🔗 Odkazy

- [Flowbite](https://flowbite.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop)

## 📊 Stav projektu

**Verzia:** 0.1.0-dev  
**Stav:** Alpha (aktívny vývoj)  
**Pokrok:** 15% dokončené

Pozrite si [PROGRESS.md](PROGRESS.md) pre aktuálny stav vývoja.

---

Vytvorené s ❤️ pre Flowbite komunitu