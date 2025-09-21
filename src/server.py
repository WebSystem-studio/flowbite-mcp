"""
Flowbite MCP Server - Hlavný server súbor
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    from fastmcp import FastMCP
    from fastmcp.resources import Resource
    from fastmcp.tools import Tool
except ImportError:
    print("FastMCP nie je nainštalovaný. Nainštalujte ho pomocou: pip install fastmcp")
    exit(1)

from .config import get_config, validate_environment
from .models.component import (
    FlowbiteComponent,
    ComponentGenerationRequest,
    ComponentValidationResult,
    ComponentSuggestion,
    ComponentType,
    ComponentVariant,
    ComponentSize
)


# Konfigurácia loggingu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Načítanie konfigurácie
config = get_config()

# Inicializácia FastMCP servera
app = FastMCP(
    name=config.name,
    version=config.version,
    description=config.description
)


class FlowbiteServer:
    """Hlavná trieda MCP servera"""
    
    def __init__(self):
        self.config = config
        self.components_cache: Dict[str, List[FlowbiteComponent]] = {}
        self.templates_cache: Dict[str, str] = {}
        
    async def initialize(self):
        """Inicializácia servera"""
        logger.info("Inicializujem Flowbite MCP Server...")
        
        # Validácia environment
        if not validate_environment():
            raise RuntimeError("Chyba pri validácii environment")
        
        # Vytvorenie potrebných adresárov
        await self._ensure_directories()
        
        # Načítanie základných komponentov
        await self._load_default_components()
        
        logger.info("Server úspešne inicializovaný")
    
    async def _ensure_directories(self):
        """Zabezpečí existenciu potrebných adresárov"""
        for dir_path in [self.config.components_dir, self.config.examples_dir, self.config.schemas_dir]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    async def _load_default_components(self):
        """Načíta základné komponenty do cache"""
        for component_type in self.config.supported_components:
            await self._load_components_by_type(component_type)
    
    async def _load_components_by_type(self, component_type: str) -> List[FlowbiteComponent]:
        """Načíta komponenty daného typu"""
        if component_type in self.components_cache:
            return self.components_cache[component_type]
        
        component_path = self.config.get_component_path(component_type)
        components = []
        
        if component_path.exists():
            try:
                with open(component_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for comp_data in data.get(component_type, []):
                        components.append(FlowbiteComponent(**comp_data))
            except Exception as e:
                logger.error(f"Chyba pri načítavaní komponentov {component_type}: {e}")
        
        self.components_cache[component_type] = components
        return components


# Globálna inštancia servera
server = FlowbiteServer()


# MCP Tools
@app.tool()
async def generate_button(
    text: str = "Button",
    variant: str = "primary",
    size: str = "md",
    disabled: bool = False,
    icon: Optional[str] = None,
    href: Optional[str] = None,
    outline: bool = False
) -> str:
    """
    Generuje Flowbite button komponent
    
    Args:
        text: Text tlačidla
        variant: Variant tlačidla (primary, secondary, success, warning, danger)
        size: Veľkosť tlačidla (xs, sm, md, lg, xl)
        disabled: Či je tlačidlo vypnuté
        icon: CSS trieda pre ikonu (napr. 'fas fa-download')
        href: URL odkaz (ak je zadané, vytvorí sa <a> namiesto <button>)
        outline: Či má byť tlačidlo outline štýl
        
    Returns:
        HTML kód vygenerovaného tlačidla
    """
    try:
        # Validácia parametrov
        if variant not in [v.value for v in ComponentVariant]:
            variant = "primary"
        
        if size not in [s.value for s in ComponentSize]:
            size = "md"
        
        # Základné CSS triedy
        base_classes = "font-medium rounded-lg focus:outline-none focus:ring-4"
        
        # Variant specific classes
        variant_classes = {
            "primary": "text-white bg-blue-700 hover:bg-blue-800 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800",
            "secondary": "text-gray-900 bg-white border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:ring-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700",
            "success": "text-white bg-green-700 hover:bg-green-800 focus:ring-green-300 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800",
            "warning": "text-white bg-yellow-400 hover:bg-yellow-500 focus:ring-yellow-300",
            "danger": "text-white bg-red-700 hover:bg-red-800 focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900"
        }
        
        # Size specific classes
        size_classes = {
            "xs": "px-3 py-2 text-xs",
            "sm": "px-3 py-2 text-sm", 
            "md": "px-5 py-2.5 text-sm",
            "lg": "px-5 py-3 text-base",
            "xl": "px-6 py-3.5 text-base"
        }
        
        # Outline modifikácia
        if outline and variant in variant_classes:
            variant_classes[variant] = variant_classes[variant].replace("bg-", "border border-").replace("text-white", f"text-{variant}-700")
        
        # Kombinovanie tried
        classes = f"{base_classes} {variant_classes.get(variant, variant_classes['primary'])} {size_classes.get(size, size_classes['md'])}"
        
        # Generovanie HTML
        if href:
            # Link button
            html = f'<a href="{href}" class="{classes}"'
            if disabled:
                html += ' aria-disabled="true" tabindex="-1"'
            html += '>'
        else:
            # Regular button
            html = f'<button type="button" class="{classes}"'
            if disabled:
                html += ' disabled'
            html += '>'
        
        # Pridanie ikony a textu
        if icon:
            html += f'<i class="{icon}"></i> '
        html += text
        
        # Zatvorenie tagu
        html += '</a>' if href else '</button>'
        
        return html
        
    except Exception as e:
        logger.error(f"Chyba pri generovaní button: {e}")
        return f"<!-- Chyba pri generovaní button: {e} -->"


@app.tool()
async def generate_form(
    fields: List[Dict[str, Any]],
    submit_text: str = "Odoslať",
    method: str = "POST",
    action: Optional[str] = None,
    validation: bool = True,
    dark_mode: bool = False
) -> str:
    """
    Generuje Flowbite form komponent
    
    Args:
        fields: Zoznam polí formulára s vlastnosťami (name, type, label, placeholder, required)
        submit_text: Text submit tlačidla
        method: HTTP metóda (GET, POST)
        action: URL akcie formulára
        validation: Či zahrnúť validačné štýly
        dark_mode: Či použiť dark mode štýly
        
    Returns:
        HTML kód vygenerovaného formulára
    """
    try:
        # CSS triedy
        label_class = "block mb-2 text-sm font-medium text-gray-900"
        input_class = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
        
        if dark_mode:
            label_class += " dark:text-white"
            input_class += " dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        
        # Začiatok formulára
        form_html = '<form class="space-y-6"'
        if action:
            form_html += f' action="{action}"'
        form_html += f' method="{method}">\n'
        
        # Generovanie polí
        for field in fields:
            field_name = field.get("name", "")
            field_type = field.get("type", "text")
            field_label = field.get("label", field_name.capitalize())
            field_placeholder = field.get("placeholder", "")
            field_required = field.get("required", False)
            
            form_html += '  <div>\n'
            form_html += f'    <label for="{field_name}" class="{label_class}">{field_label}</label>\n'
            form_html += f'    <input type="{field_type}" id="{field_name}" name="{field_name}" class="{input_class}"'
            
            if field_placeholder:
                form_html += f' placeholder="{field_placeholder}"'
            if field_required:
                form_html += ' required'
            
            form_html += '>\n'
            form_html += '  </div>\n'
        
        # Submit tlačidlo
        submit_button = await generate_button(
            text=submit_text,
            variant="primary",
            size="md"
        )
        form_html += f'  {submit_button.replace("button", "submit")}\n'
        form_html += '</form>'
        
        return form_html
        
    except Exception as e:
        logger.error(f"Chyba pri generovaní form: {e}")
        return f"<!-- Chyba pri generovaní form: {e} -->"


@app.tool()
async def validate_component(
    html_code: str,
    component_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validuje Flowbite komponent kód
    
    Args:
        html_code: HTML kód na validáciu
        component_type: Typ komponentu (voliteľné)
        
    Returns:
        Výsledok validácie s chybami a návrhmi
    """
    try:
        result = ComponentValidationResult(
            valid=True,
            errors=[],
            warnings=[],
            suggestions=[],
            score=100.0
        )
        
        # Základná validácia HTML
        if not html_code or not html_code.strip():
            result.valid = False
            result.errors.append("Prázdny HTML kód")
            result.score = 0.0
            return result.dict()
        
        # Kontrola Flowbite tried
        flowbite_patterns = [
            "bg-blue-", "text-white", "rounded-lg", "focus:ring-",
            "hover:", "dark:", "border-gray-"
        ]
        
        found_patterns = sum(1 for pattern in flowbite_patterns if pattern in html_code)
        pattern_score = (found_patterns / len(flowbite_patterns)) * 100
        
        if pattern_score < 30:
            result.warnings.append("Malo Flowbite CSS tried - možno nie je to Flowbite komponent")
        
        # Accessibility kontroly
        if 'alt=' not in html_code and '<img' in html_code:
            result.warnings.append("Obrázok bez alt atribútu")
            result.accessibility_score -= 20
        
        if 'aria-' not in html_code and any(tag in html_code for tag in ['button', 'input', 'select']):
            result.suggestions.append("Zvážte pridanie ARIA atribútov pre lepšiu accessibility")
        
        # Performance kontroly
        if html_code.count('class=') > 10:
            result.suggestions.append("Veľa CSS tried - zvážte optimalizáciu")
        
        # Finálne skóre
        result.score = max(0, pattern_score - len(result.errors) * 20 - len(result.warnings) * 5)
        result.accessibility_score = max(0, 100 - len(result.warnings) * 10)
        result.performance_score = max(0, 100 - html_code.count('class=') * 2)
        result.best_practices_score = 100 if not result.errors else 80
        
        return result.dict()
        
    except Exception as e:
        logger.error(f"Chyba pri validácii: {e}")
        return {
            "valid": False,
            "errors": [f"Chyba pri validácii: {e}"],
            "warnings": [],
            "suggestions": [],
            "score": 0.0
        }


# MCP Resources
@app.resource("flowbite://components/{component_type}")
async def get_components_by_type(component_type: str) -> str:
    """Vráti všetky komponenty daného typu"""
    try:
        components = await server._load_components_by_type(component_type)
        
        if not components:
            return f"Žiadne komponenty typu '{component_type}' nenájdené."
        
        result = {
            "type": component_type,
            "count": len(components),
            "components": [comp.dict() for comp in components]
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"Chyba pri načítavaní komponentov {component_type}: {e}")
        return f"Chyba pri načítavaní komponentov: {e}"


@app.resource("flowbite://documentation/getting-started")
async def get_getting_started() -> str:
    """Vráti dokumentáciu pre začiatočníkov"""
    return """
# Flowbite MCP Server - Začíname

## Podporované komponenty
- button: Tlačidlá rôznych variantov a veľkostí
- form: Formuláre s validáciou
- navbar: Navigačné lišty
- card: Karty pre obsah
- modal: Modálne okná

## Základné použitie

### Generovanie tlačidla
```
generate_button(text="Kliknite sem", variant="primary", size="lg")
```

### Generovanie formulára
```
generate_form(
    fields=[
        {"name": "email", "type": "email", "label": "E-mail", "required": true},
        {"name": "password", "type": "password", "label": "Heslo", "required": true}
    ],
    submit_text="Prihlásiť sa"
)
```

## Validácia komponentov
```
validate_component(html_code="<button class='bg-blue-500'>Test</button>")
```
"""


async def main():
    """Hlavná funkcia servera"""
    try:
        # Inicializácia servera
        await server.initialize()
        
        # Spustenie MCP servera
        logger.info(f"Spúšťam {config.name} v{config.version}")
        await app.run()
        
    except KeyboardInterrupt:
        logger.info("Server ukončený používateľom")
    except Exception as e:
        logger.error(f"Kritická chyba servera: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())