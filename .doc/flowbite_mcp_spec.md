# Flowbite MCP Server - Kompletná špecifikácia

## 📋 Prehľad projektu

**Cieľ:** Vytvoriť Model Context Protocol (MCP) server, ktorý umožní AI asistentom (Claude, Cursor, atď.) generovať, upravovať a navrhovať Flowbite komponenty pomocí štandardizovaného protokolu.

**Technológie:** Python, FastMCP, JSON-RPC 2.0, Tailwind CSS, Flowbite Library

## 🏗️ Architektúra systému

### Hlavné komponenty

```
┌─────────────────┐    JSON-RPC    ┌─────────────────┐    API    ┌─────────────────┐
│   Claude AI     │ ◄──────────────► │ Flowbite MCP    │ ◄─────────► │ Component       │
│   (Client)      │                 │ Server          │           │ Database        │
└─────────────────┘                 └─────────────────┘           └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ Template        │
                                    │ Generator       │
                                    └─────────────────┘
```

### Technická štruktúra

```
flowbite-mcp-server/
├── src/
│   ├── server.py                 # Hlavný MCP server
│   ├── config.py                # Konfigurácia servera
│   ├── models/
│   │   ├── __init__.py
│   │   ├── component.py         # Dátové modely komponentov
│   │   └── schema.py            # Validačné schémy
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── generator.py         # Generovanie komponentov
│   │   ├── validator.py         # Validácia kódu
│   │   └── suggestions.py       # Inteligentné návrhy
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── component_db.py      # Databáza komponentov
│   │   └── documentation.py     # Flowbite dokumentácia
│   ├── templates/
│   │   ├── __init__.py
│   │   └── component_templates.py # Šablóny komponentov
│   └── utils/
│       ├── __init__.py
│       ├── html_parser.py       # HTML parsing
│       └── css_utils.py         # CSS utility funkcie
├── data/
│   ├── components/
│   │   ├── buttons.json
│   │   ├── forms.json
│   │   ├── navigation.json
│   │   ├── cards.json
│   │   └── ...
│   ├── examples/
│   │   └── component_examples.json
│   └── schemas/
│       └── component_schema.json
├── tests/
│   ├── test_server.py
│   ├── test_tools.py
│   └── test_components.py
├── requirements.txt
├── pyproject.toml
├── README.md
└── .env.example
```

## 🛠️ Technická špecifikácia

### Závislosti (requirements.txt)

```txt
fastmcp>=0.2.0
pydantic>=2.5.0
jinja2>=3.1.0
beautifulsoup4>=4.12.0
pyyaml>=6.0.0
python-dotenv>=1.0.0
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
```

### Konfigurácia servera (config.py)

```python
from pydantic import BaseSettings
from typing import Optional

class ServerConfig(BaseSettings):
    # Server nastavenia
    name: str = "flowbite-mcp-server"
    version: str = "1.0.0"
    description: str = "MCP server pre Flowbite komponenty"
    
    # Databáza
    components_dir: str = "data/components"
    examples_dir: str = "data/examples"
    
    # Generovanie
    default_theme: str = "light"
    include_dark_mode: bool = True
    responsive_default: bool = True
    
    # Validácia
    strict_validation: bool = True
    auto_format: bool = True
    
    class Config:
        env_file = ".env"
```

## 📊 Dátové modely

### Komponent Model (models/component.py)

```python
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
from enum import Enum

class ComponentType(str, Enum):
    BUTTON = "button"
    FORM = "form"
    INPUT = "input"
    NAVBAR = "navbar"
    CARD = "card"
    MODAL = "modal"
    DROPDOWN = "dropdown"
    ALERT = "alert"
    BREADCRUMB = "breadcrumb"
    PAGINATION = "pagination"
    TABLE = "table"
    CHART = "chart"

class ComponentVariant(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"

class ComponentSize(str, Enum):
    XS = "xs"
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"

class ComponentProps(BaseModel):
    variant: Optional[ComponentVariant] = ComponentVariant.PRIMARY
    size: Optional[ComponentSize] = ComponentSize.MD
    disabled: bool = False
    rounded: bool = True
    shadow: bool = False
    dark_mode: bool = True
    responsive: bool = True
    custom_classes: Optional[str] = None

class FlowbiteComponent(BaseModel):
    id: str = Field(..., description="Jedinečný identifikátor komponentu")
    type: ComponentType = Field(..., description="Typ komponentu")
    name: str = Field(..., description="Názov komponentu")
    description: str = Field(..., description="Popis komponentu")
    category: str = Field(..., description="Kategória komponentu")
    props: ComponentProps = Field(default_factory=ComponentProps)
    html_template: str = Field(..., description="HTML šablóna")
    css_classes: List[str] = Field(default_factory=list)
    javascript: Optional[str] = None
    examples: List[Dict] = Field(default_factory=list)
    documentation_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
```

## 🔧 MCP Tools implementácia

### 1. Generátor komponentov (tools/generator.py)

```python
from fastmcp import FastMCP
from typing import Dict, Any, Optional
import json

class FlowbiteGenerator:
    def __init__(self, components_db: ComponentDatabase):
        self.db = components_db
        self.template_engine = Jinja2()

    async def generate_component(
        self,
        component_type: str,
        props: Dict[str, Any],
        content: Optional[str] = None
    ) -> str:
        """
        Generuje Flowbite komponent na základe typu a vlastností
        
        Args:
            component_type: Typ komponentu (button, form, navbar...)
            props: Vlastnosti komponentu (variant, size, atď.)
            content: Obsah komponentu (text, deti...)
            
        Returns:
            Vygenerovaný HTML kód
        """
        # Implementácia generovania

@app.tool()
async def generate_button(
    text: str = "Button",
    variant: str = "primary",
    size: str = "md",
    disabled: bool = False,
    icon: Optional[str] = None,
    href: Optional[str] = None
) -> str:
    """Generuje Flowbite button komponent"""
    # Implementácia
    
@app.tool()
async def generate_form(
    fields: List[Dict[str, Any]],
    submit_text: str = "Submit",
    validation: bool = True,
    dark_mode: bool = False
) -> str:
    """Generuje Flowbite form s definovanými poľami"""
    # Implementácia

@app.tool()
async def generate_navbar(
    brand: str,
    links: List[Dict[str, str]],
    style: str = "default",
    responsive: bool = True,
    dark_mode: bool = False
) -> str:
    """Generuje Flowbite navigation bar"""
    # Implementácia

@app.tool()
async def generate_card(
    title: str,
    content: str,
    image_url: Optional[str] = None,
    actions: List[Dict[str, str]] = [],
    variant: str = "default"
) -> str:
    """Generuje Flowbite card komponent"""
    # Implementácia

@app.tool()
async def generate_modal(
    title: str,
    content: str,
    size: str = "md",
    closable: bool = True,
    actions: List[Dict[str, str]] = []
) -> str:
    """Generuje Flowbite modal komponent"""
    # Implementácia
```

### 2. Inteligentné návrhy (tools/suggestions.py)

```python
@app.tool()
async def suggest_components(
    context: str,
    page_type: str = "general",
    framework: str = "html"
) -> List[Dict[str, Any]]:
    """
    Navrhne vhodné Flowbite komponenty na základe kontextu
    
    Args:
        context: Popis toho, čo užívateľ potrebuje
        page_type: Typ stránky (landing, dashboard, ecommerce...)
        framework: Framework (html, react, vue...)
        
    Returns:
        Zoznam navrhnutých komponentov s popismi
    """
    # AI-powered suggestions implementácia

@app.tool()
async def analyze_layout(
    html_code: str
) -> Dict[str, Any]:
    """Analyzuje existujúci layout a navrhne vylepšenia"""
    # Implementácia analýzy

@app.tool()
async def optimize_components(
    html_code: str,
    target: str = "performance"
) -> str:
    """Optimalizuje existujúce Flowbite komponenty"""
    # Implementácia optimalizácie
```

### 3. Validátor (tools/validator.py)

```python
@app.tool()
async def validate_component(
    html_code: str,
    component_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validuje Flowbite komponent kód
    
    Returns:
        {
            "valid": bool,
            "errors": List[str],
            "warnings": List[str],
            "suggestions": List[str]
        }
    """
    # Implementácia validácie

@app.tool()
async def fix_component(
    html_code: str,
    auto_fix: bool = True
) -> str:
    """Automaticky opraví chyby v Flowbite komponente"""
    # Implementácia auto-fix
```

## 📚 MCP Resources implementácia

### Databáza komponentov (resources/component_db.py)

```python
@app.resource("flowbite://components/{component_type}")
async def get_components_by_type(component_type: str) -> str:
    """Vráti všetky komponenty daného typu"""
    # Implementácia

@app.resource("flowbite://documentation/{topic}")
async def get_documentation(topic: str) -> str:
    """Vráti dokumentáciu pre dané téma"""
    # Implementácia

@app.resource("flowbite://examples/{component_id}")
async def get_component_examples(component_id: str) -> str:
    """Vráti príklady použitia komponentu"""
    # Implementácia
```

## 🗃️ Dátová štruktúra

### Databáza komponentov (data/components/buttons.json)

```json
{
  "buttons": [
    {
      "id": "btn-primary-md",
      "type": "button",
      "name": "Primary Button",
      "description": "Hlavné akčné tlačidlo s primary farbou",
      "category": "buttons",
      "props": {
        "variant": "primary",
        "size": "md",
        "rounded": true,
        "dark_mode": true
      },
      "html_template": "<button type=\"button\" class=\"text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800\">{{text}}</button>",
      "css_classes": [
        "text-white",
        "bg-blue-700",
        "hover:bg-blue-800",
        "focus:ring-4",
        "focus:ring-blue-300",
        "font-medium",
        "rounded-lg",
        "text-sm",
        "px-5",
        "py-2.5",
        "mr-2",
        "mb-2",
        "dark:bg-blue-600",
        "dark:hover:bg-blue-700",
        "focus:outline-none",
        "dark:focus:ring-blue-800"
      ],
      "examples": [
        {
          "name": "Basic usage",
          "code": "<button type=\"button\" class=\"text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:blue-700 focus:outline-none dark:focus:ring-blue-800\">Default</button>"
        }
      ],
      "documentation_url": "https://flowbite.com/docs/components/buttons/",
      "tags": ["button", "primary", "action", "form"]
    }
  ]
}
```

## 🚀 Implementačný plán

### Fáza 1: Základná štruktúra (Týždeň 1)

**Úlohy:**
- [ ] Vytvorenie projektovej štruktúry
- [ ] Nastavenie FastMCP servera
- [ ] Implementácia základných modelov
- [ ] Vytvorenie konfiguračného systému

**Výstupy:**
- Funkčný MCP server s basic ping/pong
- Dátové modely pre komponenty
- Základná konfigurácia

### Fáza 2: Základné komponenty (Týždeň 2)

**Úlohy:**
- [ ] Implementácia button generátora
- [ ] Implementácia form generátora
- [ ] Vytvorenie databázy základných komponentov
- [ ] Testovanie s Claude Desktop

**Výstupy:**
- Funkčné generovanie buttons a forms
- Testované pripojenie k Claude
- Dokumentácia API

### Fáza 3: Rozšírené komponenty (Týždeň 3-4)

**Úlohy:**
- [ ] Implementácia navigation komponentov
- [ ] Implementácia card, modal, dropdown
- [ ] Pridanie validačných nástrojov
- [ ] Implementácia inteligentných návrhov

**Výstupy:**
- Kompletná sada základných komponentov
- Validácia a auto-fix funkcie
- AI-powered suggestions

### Fáza 4: Pokročilé funkcie (Týždeň 5)

**Úlohy:**
- [ ] Dark mode podpora
- [ ] Responsive design generovanie
- [ ] Template engine optimalizácia
- [ ] Performance optimalizácie

**Výstupy:**
- Kompletne funkčný server
- Optimalizované výkony
- Advanced features

### Fáza 5: Dokumentácia a distribúcia (Týždeň 6)

**Úlohy:**
- [ ] Kompletná dokumentácia
- [ ] Unit testy a integration testy
- [ ] PyPI package príprava
- [ ] GitHub repository setup

**Výstupy:**
- Publikovaný package
- Kompletná dokumentácia
- Open source repository

## 🧪 Testovacia stratégia

### Unit testy

```python
# tests/test_generator.py
import pytest
from src.tools.generator import FlowbiteGenerator

class TestFlowbiteGenerator:
    def test_generate_button_basic(self):
        generator = FlowbiteGenerator()
        result = generator.generate_button("Click me", "primary", "md")
        assert "bg-blue-700" in result
        assert "Click me" in result
        
    def test_generate_button_with_icon(self):
        # Test implementácia
        pass
        
    def test_generate_form_validation(self):
        # Test implementácia  
        pass
```

### Integration testy

```python
# tests/test_mcp_integration.py
import pytest
from fastmcp.testing import MCPClient

@pytest.mark.asyncio
async def test_mcp_server_connection():
    client = MCPClient("flowbite-mcp-server")
    await client.connect()
    
    # Test tools listing
    tools = await client.list_tools()
    assert "generate_button" in [tool.name for tool in tools]
    
    # Test component generation
    result = await client.call_tool("generate_button", {
        "text": "Test Button",
        "variant": "primary"
    })
    assert result.success
    assert "bg-blue-700" in result.content
```

## 📖 Používateľská dokumentácia

### Inštalácia

```bash
# Klónovanie repozitára
git clone https://github.com/username/flowbite-mcp-server.git
cd flowbite-mcp-server

# Inštalácia závislostí
pip install -e .

# Spustenie servera
python -m src.server
```

### Konfigurácia pre Claude Desktop

```json
{
  "mcpServers": {
    "flowbite": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/flowbite-mcp-server"
    }
  }
}
```

### Použitie v Claude

```
# Generovanie komponentov
"Vytvor mi primary button s textom 'Odoslať'"
"Vygeneruj login form s email a password políčkami"
"Navrhni mi navbar pre e-commerce stránku"

# Validácia a opravy
"Skontroluj tento Flowbite kód: [vložený kód]"
"Oprav chyby v tomto komponente: [kód]"

# Inteligentné návrhy
"Aké komponenty potrebujem pre dashboard aplikáciu?"
"Optimalizuj tento layout pre mobilné zariadenia"
```

## 🔮 Budúce rozšírenia

### Verzia 2.0
- Flowbite Blocks podpora
- Template generovanie
- Multi-framework podpora (React, Vue, Angular)
- Advanced theming

### Verzia 3.0
- AI-powered design suggestions
- Automatické A/B testing návrhov
- Integration s Figma
- Real-time preview

## 📄 Licencia a distribúcia

**Licencia:** MIT License
**Distribúcia:** PyPI package
**Repository:** GitHub (open source)
**Dokumentácia:** GitHub Pages

## 🎯 Úspešnosť metriky

- [ ] Funkčné generovanie všetkých základných Flowbite komponentov
- [ ] Úspešné pripojenie k Claude Desktop
- [ ] Pozitivný feedback od beta testerov
- [ ] Adopcia v komunite (GitHub stars, PyPI downloads)
- [ ] Príspevky od komunity (pull requests)

---

**Tento dokument slúži ako komplexná špecifikácia pre vývoj Flowbite MCP servera. Priebežne aktualizuj podľa postupu implementácie.**