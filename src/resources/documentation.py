"""
Správa dokumentácie pre MCP resources
"""

import json
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import re
from datetime import datetime

from ..config import get_config

# Konfigurácia
config = get_config()
logger = logging.getLogger(__name__)


class DocumentationManager:
    """Správca dokumentácie Flowbite komponentov"""
    
    def __init__(self):
        self.config = config
        self.docs_dir = config.data_dir / "docs"
        self.templates_dir = config.templates_dir
        self._cache = {}
        self._index = {}
        self._initialize()
    
    def _initialize(self):
        """Inicializuje dokumentačný systém"""
        try:
            # Vytvorenie adresárov ak neexistujú
            self.docs_dir.mkdir(parents=True, exist_ok=True)
            
            # Načítanie indexu
            self._load_documentation_index()
            
            # Generovanie základnej dokumentácie ak neexistuje
            if not self._index:
                self._generate_initial_documentation()
                
        except Exception as e:
            logger.error(f"Chyba pri inicializácii dokumentácie: {e}")
    
    def _load_documentation_index(self):
        """Načíta index dokumentácie"""
        try:
            index_file = self.docs_dir / "index.json"
            
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    self._index = json.load(f)
            else:
                self._index = {
                    "sections": {},
                    "guides": {},
                    "examples": {},
                    "api": {},
                    "last_updated": None
                }
                
        except Exception as e:
            logger.error(f"Chyba pri načítaní indexu dokumentácie: {e}")
            self._index = {}
    
    def _save_documentation_index(self):
        """Uloží index dokumentácie"""
        try:
            index_file = self.docs_dir / "index.json"
            self._index["last_updated"] = datetime.now().isoformat()
            
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(self._index, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Chyba pri ukladaní indexu dokumentácie: {e}")
    
    def _generate_initial_documentation(self):
        """Generuje základnú dokumentáciu"""
        try:
            # Základné sekcie
            sections = {
                "introduction": {
                    "title": "Úvod do Flowbite MCP",
                    "description": "Základné informácie o Flowbite MCP serveri",
                    "order": 1
                },
                "installation": {
                    "title": "Inštalácia a nastavenie",
                    "description": "Ako nainštalovať a nakonfigurovať server",
                    "order": 2
                },
                "components": {
                    "title": "Komponenty",
                    "description": "Dostupné Flowbite komponenty",
                    "order": 3
                },
                "tools": {
                    "title": "Nástroje",
                    "description": "MCP nástroje a ich použitie",
                    "order": 4
                },
                "examples": {
                    "title": "Príklady použitia",
                    "description": "Praktické príklady a use cases",
                    "order": 5
                },
                "api": {
                    "title": "API referencia",
                    "description": "Kompletná API dokumentácia",
                    "order": 6
                }
            }
            
            self._index["sections"] = sections
            
            # Generovanie obsahov sekcií
            for section_id, section_info in sections.items():
                self._generate_section_content(section_id, section_info)
            
            self._save_documentation_index()
            
        except Exception as e:
            logger.error(f"Chyba pri generovaní dokumentácie: {e}")
    
    def _generate_section_content(self, section_id: str, section_info: Dict[str, Any]):
        """Generuje obsah sekcie"""
        try:
            file_path = self.docs_dir / f"{section_id}.md"
            
            if file_path.exists():
                return  # Neprepisovať existujúcu dokumentáciu
            
            content = self._get_section_template(section_id, section_info)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            logger.error(f"Chyba pri generovaní sekcie {section_id}: {e}")
    
    def _get_section_template(self, section_id: str, section_info: Dict[str, Any]) -> str:
        """Vráti template pre sekciu"""
        templates = {
            "introduction": self._get_introduction_template(),
            "installation": self._get_installation_template(),
            "components": self._get_components_template(),
            "tools": self._get_tools_template(),
            "examples": self._get_examples_template(),
            "api": self._get_api_template()
        }
        
        return templates.get(section_id, self._get_default_template(section_info))
    
    def _get_introduction_template(self) -> str:
        """Template pre úvodnú sekciu"""
        return """# Úvod do Flowbite MCP

Flowbite MCP (Model Context Protocol) server je nástroj pre generovanie a správu Flowbite komponentov.

## Čo je Flowbite MCP?

Flowbite MCP server poskytuje:

- **Generovanie komponentov**: Automatické vytvorenie HTML komponentov s Tailwind CSS
- **Validácia**: Kontrola správnosti a dostupnosti komponentov
- **Návrhy**: Inteligentné odporúčania komponentov na základe kontextu
- **Dokumentácia**: Kompletná dokumentácia všetkých komponentov

## Kľúčové vlastnosti

### 🚀 Jednoduché použitie
Generujte komponenty pomocou jednoduchých MCP nástrojov.

### 🎨 Plná podpora Tailwind CSS
Všetky komponenty využívajú najnovšie Tailwind CSS triedy.

### 📱 Responzívny dizajn
Komponenty sú optimalizované pre všetky zariadenia.

### ♿ Accessibility
Všetky komponenty dodržiavajú WCAG 2.1 štandardy.

### 🌙 Dark mode
Plná podpora pre svetlý a tmavý režim.

## Podporované komponenty

- Buttons (tlačidlá)
- Forms (formuláre)
- Cards (karty)
- Navigation (navigácia)
- Modals (modálne okná)
- Tables (tabuľky)
- Alerts (upozornenia)
- A mnoho ďalších...

## Začíname

Pokračujte v sekcii [Inštalácia](installation.md) pre nastavenie servera.
"""
    
    def _get_installation_template(self) -> str:
        """Template pre inštalačnú sekciu"""
        return """# Inštalácia a nastavenie

## Požiadavky

- Python 3.8+
- pip alebo poetry
- Node.js (voliteľné, pre development)

## Inštalácia

### 1. Klónovanie repozitára

```bash
git clone https://github.com/your-repo/flowbite-mcp.git
cd flowbite-mcp
```

### 2. Vytvorenie virtuálneho prostredia

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# alebo
venv\\Scripts\\activate  # Windows
```

### 3. Inštalácia závislostí

```bash
pip install -r requirements.txt
```

### 4. Konfigurácia

Vytvorte `.env` súbor:

```env
# Server nastavenia
SERVER_HOST=localhost
SERVER_PORT=8000
DEBUG=true

# Cesty
DATA_DIR=./data
TEMPLATES_DIR=./templates

# Supported komponenty
SUPPORTED_COMPONENTS=button,form,card,navbar,modal,table,alert
```

## Spustenie servera

```bash
python -m src.server
```

Server bude dostupný na `http://localhost:8000`

## Konfiguračné možnosti

### Environment premenné

| Premenná | Popis | Predvolená hodnota |
|----------|-------|-------------------|
| `SERVER_HOST` | Host servera | `localhost` |
| `SERVER_PORT` | Port servera | `8000` |
| `DEBUG` | Debug režim | `false` |
| `DATA_DIR` | Adresár s dátami | `./data` |
| `TEMPLATES_DIR` | Adresár s template | `./templates` |

### Pokročilé nastavenia

Pre pokročilé konfigurácie upravte `src/config.py`.

## Overenie inštalácie

Otestujte server pomocou:

```bash
curl http://localhost:8000/health
```

Očakávaný výstup:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "components_loaded": 8
}
```

## Problémy a riešenia

### Port už používaný
Zmeňte port v `.env` súbore alebo použite:
```bash
SERVER_PORT=8001 python -m src.server
```

### Chýbajúce závislosti
Reinstalujte závislosti:
```bash
pip install -r requirements.txt --force-reinstall
```

## Ďalšie kroky

- [Komponenty](components.md) - Zoznam dostupných komponentov
- [Nástroje](tools.md) - Ako použiť MCP nástroje
- [Príklady](examples.md) - Praktické príklady
"""
    
    def _get_components_template(self) -> str:
        """Template pre komponenty sekciu"""
        return """# Komponenty

Flowbite MCP podporuje široký výber komponentov pre moderné webové aplikácie.

## Dostupné komponenty

### Základné komponenty

#### Button (Tlačidlo)
Interaktívne tlačidlá s rôznymi štýlmi a veľkosťami.

**Varianty:**
- `primary` - Hlavné tlačidlo
- `secondary` - Sekundárne tlačidlo  
- `success` - Úspešná akcia
- `danger` - Nebezpečná akcia
- `warning` - Varovanie
- `info` - Informácia
- `light` - Svetlé tlačidlo
- `dark` - Tmavé tlačidlo

**Veľkosti:**
- `xs` - Extra malé
- `sm` - Malé
- `md` - Stredné (predvolené)
- `lg` - Veľké
- `xl` - Extra veľké

#### Form (Formulár)
Kompletné formuláre s validáciou.

**Typy:**
- `contact` - Kontaktný formulár
- `login` - Prihlasovací formulár
- `register` - Registračný formulár

### Layout komponenty

#### Card (Karta)
Kontajnery pre organizáciu obsahu.

**Varianty:**
- `default` - Základná karta
- `interactive` - Interaktívna karta
- `testimonial` - Testimonial karta

#### Navbar (Navigácia)
Hlavné navigačné menu.

**Varianty:**
- `default` - Základná navigácia
- `dark` - Tmavá navigácia
- `fixed` - Fixná navigácia

### Overlay komponenty

#### Modal (Modálne okno)
Prekryvné okná pre dialógy.

**Veľkosti:**
- `sm` - Malé modálne okno
- `md` - Stredné modálne okno
- `lg` - Veľké modálne okno
- `xl` - Extra veľké modálne okno

### Data komponenty

#### Table (Tabuľka)
Zobrazenie dát v tabuľkovom formáte.

**Varianty:**
- `simple` - Jednoduchá tabuľka
- `striped` - Pruhovaná tabuľka
- `hover` - S hover efektom

#### Alert (Upozornenie)
Informačné a varovné správy.

**Typy:**
- `info` - Informácia
- `success` - Úspech
- `warning` - Varovanie
- `error` - Chyba

## Použitie komponentov

### Cez MCP nástroje

```python
# Generovanie tlačidla
result = await generate_component(
    component_type="button",
    variant="primary",
    size="lg",
    props={
        "text": "Kliknite sem",
        "rounded": true
    }
)
```

### Priame použitie

```python
from src.tools.generator import FlowbiteGenerator

generator = FlowbiteGenerator()
html = await generator.generate_component(
    component_type="card",
    variant="default",
    props={"title": "Moja karta"}
)
```

## Prispôsobenie komponentov

### Custom CSS triedy

Pridajte vlastné CSS triedy:

```python
props = {
    "custom_classes": ["my-custom-class", "another-class"]
}
```

### Template customizácia

Upravte template súbory v `templates/` adresári.

## Najlepšie praktiky

1. **Konzistentnosť**: Používajte rovnaké varianty v celej aplikácii
2. **Accessibility**: Vždy pridajte `aria-label` a `alt` atribúty
3. **Performance**: Načítavajte iba potrebné komponenty
4. **Responzívnosť**: Testujte na rôznych zariadeniach

## Príklady

Pozrite si [Príklady použitia](examples.md) pre praktické ukážky.
"""
    
    def _get_tools_template(self) -> str:
        """Template pre nástroje sekciu"""
        return """# MCP nástroje

Flowbite MCP server poskytuje sadu nástrojov pre prácu s komponentmi.

## Dostupné nástroje

### generate_component

Generuje HTML kód pre špecifikovaný komponent.

**Parametre:**
- `component_type` (string): Typ komponentu
- `variant` (string, voliteľný): Varianta komponentu  
- `size` (string, voliteľný): Veľkosť komponentu
- `props` (object, voliteľný): Dodatočné vlastnosti

**Príklad použitia:**
```json
{
  "component_type": "button",
  "variant": "primary", 
  "size": "lg",
  "props": {
    "text": "Kliknite sem",
    "rounded": true,
    "shadow": false
  }
}
```

**Odpoveď:**
```json
{
  "html": "<button class=\"bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded\">Kliknite sem</button>",
  "css_classes": ["bg-blue-500", "hover:bg-blue-700", "text-white", "font-bold", "py-2", "px-4", "rounded"],
  "component_type": "button",
  "variant": "primary"
}
```

### validate_component

Validuje HTML kód komponentu.

**Parametre:**
- `html` (string): HTML kód na validáciu
- `component_type` (string, voliteľný): Očakávaný typ komponentu
- `strict` (boolean, voliteľný): Prísna validácia

**Príklad použitia:**
```json
{
  "html": "<button class=\"btn btn-primary\">Test</button>",
  "component_type": "button",
  "strict": true
}
```

**Odpoveď:**
```json
{
  "is_valid": true,
  "score": 85,
  "issues": [],
  "suggestions": ["Pridajte aria-label pre lepšiu accessibility"],
  "auto_fix_available": true
}
```

### suggest_components

Navrhuje komponenty na základe kontextu.

**Parametre:**
- `context` (string): Popis potreby
- `page_type` (string, voliteľný): Typ stránky
- `framework` (string, voliteľný): Framework
- `max_suggestions` (number, voliteľný): Maximum návrhov

**Príklad použitia:**
```json
{
  "context": "Potrebujem vytvoriť kontaktný formulár s tlačidlom na odoslanie",
  "page_type": "general",
  "max_suggestions": 3
}
```

**Odpoveď:**
```json
{
  "suggestions": [
    {
      "component_type": "form",
      "name": "Kontaktný formulár",
      "description": "Formulár pre kontaktné informácie",
      "confidence": 0.95,
      "props": {
        "variant": "contact"
      },
      "reason": "Detekované kľúčové slovo 'kontaktný formulár'",
      "use_case": "Zber kontaktných informácií od používateľov"
    }
  ]
}
```

## MCP Resources

### flowbite://components/{type}

Prístup k definícii komponentu.

**Príklad:**
```
flowbite://components/button
```

### flowbite://components/{type}/{variant}

Prístup k špecifickej variante komponentu.

**Príklad:**
```
flowbite://components/button/primary
```

## Integrácia s MCP klientmi

### Claude Desktop

Pridajte do `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flowbite": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/flowbite-mcp"
    }
  }
}
```

### VS Code s MCP rozšírením

1. Nainštalujte MCP rozšírenie
2. Pridajte server konfiguráciu
3. Reštartujte VS Code

## Chybové hlásenia

### Častí chyby

**"Component type not supported"**
- Skontrolujte názov komponentu
- Pozrite zoznam podporovaných komponentov

**"Invalid variant"**
- Skontrolujte dostupné varianty
- Použite `list_components` pre zoznam

**"Validation failed"**
- Skontrolujte HTML syntax
- Použite `validate_component` pre detaily

## Rozšírenie

### Pridanie nového komponentu

1. Vytvorte JSON súbor v `data/components/`
2. Definujte varianty a template
3. Reštartujte server

### Custom nástroje

Rozšírte `src/tools/` s vlastnými nástrojmi.

## Debugging

Zapnite debug režim v `.env`:
```env
DEBUG=true
```

Pozrite logy pre detailné informácie o chybách.
"""
    
    def _get_examples_template(self) -> str:
        """Template pre príklady sekciu"""
        return """# Príklady použitia

Praktické príklady použitia Flowbite MCP servera.

## Základné príklady

### 1. Vytvorenie tlačidla

```json
{
  "tool": "generate_component",
  "parameters": {
    "component_type": "button",
    "variant": "primary",
    "size": "md",
    "props": {
      "text": "Kliknite sem",
      "rounded": true
    }
  }
}
```

**Výsledok:**
```html
<button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
  Kliknite sem
</button>
```

### 2. Kontaktný formulár

```json
{
  "tool": "generate_component",
  "parameters": {
    "component_type": "form",
    "variant": "contact",
    "props": {
      "title": "Kontaktujte nás",
      "submit_text": "Odoslať správu"
    }
  }
}
```

**Výsledok:**
```html
<form class="max-w-md mx-auto">
  <div class="mb-5">
    <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Meno</label>
    <input type="text" id="name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required />
  </div>
  <!-- viac polí -->
  <button type="submit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
    Odoslať správu
  </button>
</form>
```

## Pokročilé príklady

### 3. Dashboard s kartami

```python
# Generovanie viacerých komponentov pre dashboard
components = []

# Sidebar navigácia
sidebar = await generate_component(
    component_type="sidebar",
    variant="default",
    props={
        "items": [
            {"text": "Dashboard", "icon": "dashboard", "active": True},
            {"text": "Používatelia", "icon": "users"},
            {"text": "Nastavenia", "icon": "settings"}
        ]
    }
)
components.append(sidebar)

# Štatistické karty
stats_cards = []
for stat in [
    {"title": "Celkom používateľov", "value": "1,234", "change": "+12%"},
    {"title": "Mesačný rast", "value": "23%", "change": "+5%"},
    {"title": "Aktívni dnes", "value": "890", "change": "-2%"}
]:
    card = await generate_component(
        component_type="card",
        variant="stats",
        props=stat
    )
    stats_cards.append(card)

components.extend(stats_cards)
```

### 4. E-commerce produktová stránka

```python
# Produktová karta
product_card = await generate_component(
    component_type="card",
    variant="product",
    props={
        "title": "MacBook Pro 16",
        "price": "€2,499",
        "image": "macbook-pro.jpg",
        "rating": 4.8,
        "reviews": 234,
        "description": "Najvýkonnejší MacBook s M2 Pro čipom.",
        "in_stock": True
    }
)

# Tlačidlá pre akcie
add_to_cart = await generate_component(
    component_type="button",
    variant="primary",
    size="lg",
    props={
        "text": "Pridať do košíka",
        "icon": "shopping-cart"
    }
)

buy_now = await generate_component(
    component_type="button", 
    variant="success",
    size="lg",
    props={
        "text": "Kúpiť teraz",
        "icon": "credit-card"
    }
)
```

### 5. Autentifikácia

```python
# Prihlasovací formulár
login_form = await generate_component(
    component_type="form",
    variant="login",
    props={
        "title": "Prihlásenie",
        "forgot_password": True,
        "social_login": ["google", "github"],
        "remember_me": True
    }
)

# Registračný formulár
register_form = await generate_component(
    component_type="form",
    variant="register", 
    props={
        "title": "Registrácia",
        "terms_agreement": True,
        "social_login": ["google", "github"],
        "password_strength": True
    }
)
```

## Use case scenáre

### Scenár 1: Landing page

```python
async def create_landing_page():
    components = []
    
    # Hero sekcia
    hero_navbar = await generate_component("navbar", "landing")
    hero_content = await generate_component("hero", "default", props={
        "title": "Naša úžasná aplikácia",
        "subtitle": "Riešenie všetkých vašich problémov",
        "cta_text": "Začať zadarmo"
    })
    
    # Features sekcia
    feature_cards = []
    features = [
        {"title": "Rýchle", "description": "Optimalizované pre výkon"},
        {"title": "Bezpečné", "description": "Enterprise-grade bezpečnosť"},
        {"title": "Škálovateľné", "description": "Rastie s vašou firmou"}
    ]
    
    for feature in features:
        card = await generate_component("card", "feature", props=feature)
        feature_cards.append(card)
    
    # Contact formulár
    contact_form = await generate_component("form", "contact", props={
        "title": "Kontaktujte nás",
        "fields": ["name", "email", "company", "message"]
    })
    
    return {
        "navbar": hero_navbar,
        "hero": hero_content,
        "features": feature_cards,
        "contact": contact_form
    }
```

### Scenár 2: Admin panel

```python
async def create_admin_panel():
    # Layout komponenty
    sidebar = await generate_component("sidebar", "admin", props={
        "logo": "AdminPanel",
        "user": {"name": "Admin", "role": "Administrator"},
        "menu_items": [
            {"text": "Dashboard", "icon": "dashboard", "active": True},
            {"text": "Používatelia", "icon": "users", "badge": "12"},
            {"text": "Objednávky", "icon": "orders", "badge": "5"},
            {"text": "Produkty", "icon": "products"},
            {"text": "Nastavenia", "icon": "settings"}
        ]
    })
    
    # Data tabuľka
    users_table = await generate_component("table", "users", props={
        "title": "Zoznam používateľov",
        "searchable": True,
        "sortable": True,
        "pagination": True,
        "actions": ["edit", "delete", "view"]
    })
    
    # Štatistiky
    stats = await generate_component("stats", "dashboard", props={
        "cards": [
            {"title": "Celkom používateľov", "value": "1,234", "trend": "up"},
            {"title": "Nové objednávky", "value": "56", "trend": "up"},
            {"title": "Príjmy", "value": "€23,456", "trend": "down"},
            {"title": "Konverzia", "value": "3.2%", "trend": "stable"}
        ]
    })
    
    return {
        "sidebar": sidebar,
        "table": users_table,
        "stats": stats
    }
```

## Validácia a debugging

### Validácia komponentov

```python
# Validácia vygenerovaného HTML
result = await validate_component(
    html=generated_html,
    component_type="button",
    strict=True
)

if not result["is_valid"]:
    print("Problémy:", result["issues"])
    print("Návrhy:", result["suggestions"])
    
    # Auto-fix ak je dostupný
    if result["auto_fix_available"]:
        fixed_html = await auto_fix_component(generated_html)
```

### Debugging generácie

```python
# Debug informácie
debug_info = await generate_component(
    component_type="card",
    variant="product",
    props={"debug": True}
)

print("Template used:", debug_info["template"])
print("CSS classes:", debug_info["css_classes"])
print("Processing time:", debug_info["processing_time"])
```

## Integrácia s frameworkmi

### React komponent

```javascript
// Generovanie React komponentu
const generateReactButton = async (text, variant = 'primary') => {
  const result = await mcpClient.callTool('generate_component', {
    component_type: 'button',
    variant,
    framework: 'react',
    props: { text }
  });
  
  return result.jsx;
};
```

### Vue komponent

```javascript
// Vue integrácia
export default {
  async mounted() {
    const cardHtml = await this.$mcp.generate({
      component_type: 'card',
      variant: 'default',
      props: {
        title: this.title,
        content: this.content
      }
    });
    
    this.$refs.cardContainer.innerHTML = cardHtml;
  }
}
```

## Najlepšie praktiky

1. **Cacheovanie**: Cachujte vygenerované komponenty
2. **Validácia**: Vždy validujte pred produkčným použitím
3. **Testing**: Testujte komponenty na rôznych zariadeniach
4. **Performance**: Optimalizujte veľké stránky
5. **Accessibility**: Kontrolujte accessibility score

## Ďalšie príklady

Pre viac príkladov pozrite:
- [GitHub repozitár](https://github.com/your-repo/flowbite-mcp/examples)
- [Demo aplikácia](https://demo.flowbite-mcp.com)
- [Community príklady](https://community.flowbite-mcp.com)
"""
    
    def _get_api_template(self) -> str:
        """Template pre API sekciu"""
        return """# API Referencia

Kompletná dokumentácia Flowbite MCP API.

## MCP Tools

### generate_component

Generuje HTML kód pre Flowbite komponent.

**Syntax:**
```json
{
  "tool": "generate_component",
  "parameters": {
    "component_type": "string",
    "variant": "string?",
    "size": "string?",
    "props": "object?"
  }
}
```

**Parametre:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `component_type` | string | ✅ | Typ komponentu (button, form, card, ...) |
| `variant` | string | ❌ | Varianta komponentu |
| `size` | string | ❌ | Veľkosť komponentu |
| `props` | object | ❌ | Dodatočné vlastnosti |

**Návratová hodnota:**
```typescript
{
  html: string;           // Vygenerovaný HTML
  css_classes: string[];  // Použité CSS triedy
  component_type: string; // Typ komponentu
  variant: string;        // Použitá varianta
  size?: string;          // Použitá veľkosť
  props: object;          // Aplikované vlastnosti
}
```

**Príklady:**

Základné tlačidlo:
```json
{
  "tool": "generate_component",
  "parameters": {
    "component_type": "button",
    "variant": "primary",
    "props": {
      "text": "Kliknite sem"
    }
  }
}
```

Komplexný formulár:
```json
{
  "tool": "generate_component", 
  "parameters": {
    "component_type": "form",
    "variant": "contact",
    "props": {
      "title": "Kontaktujte nás",
      "fields": [
        {"name": "name", "type": "text", "required": true},
        {"name": "email", "type": "email", "required": true},
        {"name": "message", "type": "textarea", "required": true}
      ],
      "submit_text": "Odoslať"
    }
  }
}
```

### validate_component

Validuje HTML kód komponentu a poskytuje hodnotenie kvality.

**Syntax:**
```json
{
  "tool": "validate_component",
  "parameters": {
    "html": "string",
    "component_type": "string?",
    "strict": "boolean?"
  }
}
```

**Parametre:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `html` | string | ✅ | HTML kód na validáciu |
| `component_type` | string | ❌ | Očakávaný typ komponentu |
| `strict` | boolean | ❌ | Prísna validácia (default: false) |

**Návratová hodnota:**
```typescript
{
  is_valid: boolean;           // Či je komponent platný
  score: number;               // Skóre kvality (0-100)
  issues: ValidationIssue[];   // Zoznam problémov
  suggestions: string[];       // Návrhy na vylepšenie
  auto_fix_available: boolean; // Či je možný auto-fix
  accessibility_score: number; // Accessibility skóre
  performance_score: number;   // Performance skóre
}
```

**ValidationIssue:**
```typescript
{
  type: "error" | "warning" | "info";
  category: string;  // "html", "css", "accessibility", "performance"
  message: string;
  line?: number;
  suggestions?: string[];
}
```

### suggest_components

Navrhuje vhodné komponenty na základe kontextu.

**Syntax:**
```json
{
  "tool": "suggest_components",
  "parameters": {
    "context": "string",
    "page_type": "string?",
    "framework": "string?",
    "max_suggestions": "number?"
  }
}
```

**Parametre:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `context` | string | ✅ | Popis potreby alebo kontextu |
| `page_type` | string | ❌ | Typ stránky (landing, dashboard, ecommerce, ...) |
| `framework` | string | ❌ | Cieľový framework (html, react, vue, ...) |
| `max_suggestions` | number | ❌ | Maximum návrhov (default: 5) |

**Návratová hodnota:**
```typescript
{
  suggestions: ComponentSuggestion[];
}
```

**ComponentSuggestion:**
```typescript
{
  component_type: string;  // Typ komponentu
  name: string;           // Názov návrhu
  description: string;    // Popis
  confidence: number;     // Istota návrhu (0-1)
  props: object;          // Odporúčané vlastnosti
  reason: string;         // Dôvod návrhu
  use_case: string;       // Use case
}
```

## MCP Resources

### flowbite://components/{type}

Poskytuje kompletné informácie o type komponentu.

**Syntax:**
```
flowbite://components/button
```

**Návratová hodnota:**
```typescript
{
  type: string;                    // Typ komponentu
  description: string;             // Popis
  category: string;                // Kategória
  variants: {[key: string]: ComponentVariant}; // Dostupné varianty
  examples: ComponentExample[];    // Príklady použitia
}
```

### flowbite://components/{type}/{variant}

Poskytuje informácie o špecifickej variante komponentu.

**Syntax:**
```
flowbite://components/button/primary
```

**Návratová hodnota:**
```typescript
{
  type: string;           // Typ komponentu
  variant: string;        // Názov varianty
  description: string;    // Popis varianty
  html: string;          // HTML template
  css_classes: string[]; // CSS triedy
  props: object;         // Podporované vlastnosti
  example: string;       // Príklad použitia
}
```

## Podporované komponenty

### Button

**Typ:** `button`

**Varianty:**
- `primary` - Hlavné tlačidlo (modré)
- `secondary` - Sekundárne tlačidlo (sivé) 
- `success` - Úspešná akcia (zelené)
- `danger` - Nebezpečná akcia (červené)
- `warning` - Varovanie (žlté)
- `info` - Informácia (svetlo modré)
- `light` - Svetlé tlačidlo
- `dark` - Tmavé tlačidlo

**Veľkosti:** `xs`, `sm`, `md`, `lg`, `xl`

**Props:**
```typescript
{
  text: string;           // Text tlačidla
  icon?: string;          // Názov ikony
  rounded?: boolean;      // Zaoblené rohy
  shadow?: boolean;       // Tieň
  disabled?: boolean;     // Zakázané
  loading?: boolean;      // Loading stav
  href?: string;          // Link URL
  target?: string;        // Link target
  onclick?: string;       // JavaScript handler
}
```

### Form

**Typ:** `form`

**Varianty:**
- `contact` - Kontaktný formulár
- `login` - Prihlasovací formulár
- `register` - Registračný formulár

**Props:**
```typescript
{
  title?: string;         // Titulok formulára
  subtitle?: string;      // Podtitulok
  fields?: FormField[];   // Polia formulára
  submit_text?: string;   // Text submit tlačidla
  cancel_text?: string;   // Text cancel tlačidla
  method?: string;        // HTTP metóda
  action?: string;        // Action URL
}
```

**FormField:**
```typescript
{
  name: string;           // Názov poľa
  type: string;           // Typ input (text, email, password, ...)
  label?: string;         // Label textu
  placeholder?: string;   // Placeholder text
  required?: boolean;     // Povinné pole
  validation?: string;    // Validačné pravidlá
}
```

### Card

**Typ:** `card`

**Varianty:**
- `default` - Základná karta
- `interactive` - Interaktívna karta s hover efektmi
- `testimonial` - Testimonial karta
- `product` - Produktová karta
- `stats` - Štatistická karta

**Props:**
```typescript
{
  title?: string;         // Titulok karty
  subtitle?: string;      // Podtitulok
  content?: string;       // Obsah karty
  image?: string;         // URL obrázka
  actions?: CardAction[]; // Akčné tlačidlá
  footer?: string;        // Footer obsah
  header?: string;        // Header obsah
}
```

### Navbar

**Typ:** `navbar`

**Varianty:**
- `default` - Základná navigácia
- `dark` - Tmavá navigácia
- `fixed` - Fixná navigácia
- `transparent` - Transparentná navigácia

**Props:**
```typescript
{
  brand?: string;         // Názov značky/logo
  logo?: string;          // URL loga
  items?: NavItem[];      // Menu položky
  search?: boolean;       // Vyhľadávanie
  user_menu?: boolean;    // Používateľské menu
  mobile_menu?: boolean;  // Mobilné menu
}
```

## Error kódy

| Kód | Popis | Riešenie |
|-----|-------|----------|
| `COMPONENT_NOT_FOUND` | Komponent neexistuje | Skontrolujte názov komponentu |
| `VARIANT_NOT_FOUND` | Varianta neexistuje | Skontrolujte dostupné varianty |
| `INVALID_PROPS` | Neplatné vlastnosti | Skontrolujte Props dokumentáciu |
| `VALIDATION_FAILED` | Validácia zlyhala | Skontrolujte HTML syntax |
| `TEMPLATE_ERROR` | Chyba v template | Kontaktujte support |

## Rate limiting

- **Tools:** 100 požiadaviek/minútu
- **Resources:** 200 požiadaviek/minútu
- **Bulk operácie:** 10 požiadaviek/minútu

## Verzie

### v1.0.0 (aktuálna)
- Základné komponenty (button, form, card, navbar)
- MCP tools a resources
- Validácia a návrhy

### Plánované v1.1.0
- Pokročilé komponenty (charts, calendar)
- Template customizácia
- Performance optimalizácie

### Plánované v1.2.0
- React/Vue komponenty
- Advanced validácia
- Theming systém

## Podpora

- **Dokumentácia:** [docs.flowbite-mcp.com](https://docs.flowbite-mcp.com)
- **GitHub:** [github.com/flowbite-mcp](https://github.com/flowbite-mcp)
- **Discord:** [discord.gg/flowbite-mcp](https://discord.gg/flowbite-mcp)
- **Email:** support@flowbite-mcp.com
"""

    def _get_default_template(self, section_info: Dict[str, Any]) -> str:
        """Predvolený template"""
        return f"""# {section_info['title']}

{section_info['description']}

## Obsah sekcie

Táto sekcia je v štádiu vývoja.

## Ďalšie informácie

Pre viac informácií navštívte [hlavnú dokumentáciu](introduction.md).
"""
    
    async def get_documentation(
        self,
        section: str,
        format: str = "markdown"
    ) -> Optional[str]:
        """
        Načíta dokumentáciu pre sekciu
        
        Args:
            section: Názov sekcie
            format: Formát výstupu (markdown, html, json)
            
        Returns:
            Obsah dokumentácie
        """
        try:
            # Kontrola cache
            cache_key = f"{section}_{format}"
            if cache_key in self._cache:
                return self._cache[cache_key]
            
            # Načítanie zo súboru
            file_path = self.docs_dir / f"{section}.md"
            
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Formátovanie ak potrebné
            if format == "html":
                content = self._markdown_to_html(content)
            elif format == "json":
                content = self._markdown_to_json(content)
            
            # Uloženie do cache
            self._cache[cache_key] = content
            return content
            
        except Exception as e:
            logger.error(f"Chyba pri načítaní dokumentácie {section}: {e}")
            return None
    
    def _markdown_to_html(self, markdown_content: str) -> str:
        """Konvertuje markdown na HTML"""
        try:
            # Základná konverzia (zjednodušená)
            html = markdown_content
            
            # Headers
            html = re.sub(r'^### (.*)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
            html = re.sub(r'^## (.*)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
            html = re.sub(r'^# (.*)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
            
            # Code blocks
            html = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code class="\1">\2</code></pre>', html, flags=re.DOTALL)
            
            # Inline code
            html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
            
            # Bold
            html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
            
            # Italic
            html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
            
            # Links
            html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
            
            # Paragraphs
            html = re.sub(r'\n\n', '</p><p>', html)
            html = '<p>' + html + '</p>'
            
            return html
            
        except Exception as e:
            logger.error(f"Chyba pri konverzii markdown: {e}")
            return markdown_content
    
    def _markdown_to_json(self, markdown_content: str) -> str:
        """Konvertuje markdown na JSON štruktúru"""
        try:
            # Parsovanie štruktúry
            lines = markdown_content.split('\n')
            structure = {
                "title": "",
                "sections": [],
                "content": markdown_content
            }
            
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                if line.startswith('# '):
                    structure["title"] = line[2:]
                elif line.startswith('## '):
                    if current_section:
                        structure["sections"].append(current_section)
                    current_section = {
                        "title": line[3:],
                        "content": "",
                        "subsections": []
                    }
                elif line.startswith('### '):
                    if current_section:
                        current_section["subsections"].append({
                            "title": line[4:],
                            "content": ""
                        })
                elif current_section:
                    current_section["content"] += line + "\n"
            
            if current_section:
                structure["sections"].append(current_section)
            
            return json.dumps(structure, ensure_ascii=False, indent=2)
            
        except Exception as e:
            logger.error(f"Chyba pri konverzii JSON: {e}")
            return json.dumps({"error": str(e), "content": markdown_content})
    
    async def list_sections(self) -> List[Dict[str, Any]]:
        """
        Vráti zoznam všetkých sekcií
        
        Returns:
            Zoznam sekcií s metadátami
        """
        try:
            sections = []
            
            for section_id, section_info in self._index.get("sections", {}).items():
                file_path = self.docs_dir / f"{section_id}.md"
                
                section_data = {
                    "id": section_id,
                    "title": section_info.get("title", section_id.title()),
                    "description": section_info.get("description", ""),
                    "order": section_info.get("order", 999),
                    "exists": file_path.exists(),
                    "size": file_path.stat().st_size if file_path.exists() else 0
                }
                
                sections.append(section_data)
            
            # Zoradenie podľa poradia
            sections.sort(key=lambda x: x["order"])
            return sections
            
        except Exception as e:
            logger.error(f"Chyba pri listovaní sekcií: {e}")
            return []
    
    async def search_documentation(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Vyhľadá v dokumentácii
        
        Args:
            query: Vyhľadávací výraz
            max_results: Maximum výsledkov
            
        Returns:
            Zoznam výsledkov
        """
        try:
            results = []
            query_lower = query.lower()
            
            # Vyhľadávanie v sekciách
            for section_id, section_info in self._index.get("sections", {}).items():
                score = 0
                
                # Skóre pre názov sekcie
                title = section_info.get("title", "")
                if query_lower in title.lower():
                    score += 50
                
                # Skóre pre popis
                description = section_info.get("description", "")
                if query_lower in description.lower():
                    score += 25
                
                # Skóre pre obsah
                content = await self.get_documentation(section_id)
                if content and query_lower in content.lower():
                    score += 10
                    
                    # Nájdenie kontextu
                    context = self._extract_context(content, query_lower)
                    
                    if score > 0:
                        results.append({
                            "section": section_id,
                            "title": title,
                            "description": description,
                            "context": context,
                            "score": score
                        })
            
            # Zoradenie podľa skóre
            results.sort(key=lambda x: x["score"], reverse=True)
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Chyba pri vyhľadávaní: {e}")
            return []
    
    def _extract_context(self, content: str, query: str, context_length: int = 200) -> str:
        """Extrahuje kontext okolo nájdeného výrazu"""
        try:
            lines = content.split('\n')
            query_lower = query.lower()
            
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    # Extrakt kontextu
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    context_lines = lines[start:end]
                    
                    context = '\n'.join(context_lines)
                    if len(context) > context_length:
                        context = context[:context_length] + "..."
                    
                    return context
            
            return ""
            
        except Exception as e:
            logger.error(f"Chyba pri extrakcii kontextu: {e}")
            return ""
    
    async def update_documentation(
        self,
        section: str,
        content: str
    ) -> bool:
        """
        Aktualizuje dokumentáciu
        
        Args:
            section: Názov sekcie
            content: Nový obsah
            
        Returns:
            True ak úspešne aktualizované
        """
        try:
            file_path = self.docs_dir / f"{section}.md"
            
            # Uloženie súboru
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Vyčistenie cache
            cache_keys = [k for k in self._cache.keys() if k.startswith(f"{section}_")]
            for key in cache_keys:
                del self._cache[key]
            
            logger.info(f"Dokumentácia {section} úspešne aktualizovaná")
            return True
            
        except Exception as e:
            logger.error(f"Chyba pri aktualizácii dokumentácie {section}: {e}")
            return False
    
    def clear_cache(self):
        """Vyčistí cache"""
        self._cache.clear()
        logger.info("Dokumentačná cache vyčistená")


# Globálna inštancia documentation managera
documentation_manager = DocumentationManager()