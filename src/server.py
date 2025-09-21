"""
Flowbite MCP Server - hlavný server súbor
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import BaseModel

from .config import get_config
from .models.component import ComponentType, ComponentVariant, ComponentSize
from .tools.generator import FlowbiteGenerator
from .tools.validator import FlowbiteValidator  
from .tools.suggestions import FlowbiteSuggestionEngine
from .resources.component_db import ComponentDatabase
from .resources.documentation import DocumentationManager

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

# Konfigurácia
config = get_config()

# Inicializácia modulov
generator = FlowbiteGenerator()
validator = FlowbiteValidator()
suggestion_engine = FlowbiteSuggestionEngine()
component_db = ComponentDatabase()
documentation_manager = DocumentationManager()

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
async def generate_component(
    component_type: str,
    variant: str = "default",
    size: str = "md",
    props: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Generuje Flowbite komponent
    
    Args:
        component_type: Typ komponentu (button, form, card, etc.)
        variant: Varianta komponentu
        size: Veľkosť komponentu  
        props: Dodatočné vlastnosti komponentu
        
    Returns:
        Vygenerovaný HTML kód s metadátami
    """
    try:
        logger.info(f"Generujem komponent: {component_type}, variant: {variant}")
        
        if props is None:
            props = {}
            
        # Použitie generátora
        result = await generator.generate_component(
            component_type=component_type,
            variant=variant,
            size=size,
            props=props
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Chyba pri generovaní komponentu: {e}")
        return {
            "error": str(e),
            "component_type": component_type,
            "variant": variant
        }


@app.tool()
async def suggest_components(
    context: str,
    page_type: str = "general",
    framework: str = "html",
    max_suggestions: int = 5
) -> Dict[str, Any]:
    """
    Navrhuje vhodné komponenty na základe kontextu
    
    Args:
        context: Popis potreby alebo kontextu
        page_type: Typ stránky (landing, dashboard, ecommerce, etc.)
        framework: Cieľový framework (html, react, vue, etc.)
        max_suggestions: Maximum počet návrhov
        
    Returns:
        Zoznam navrhnutých komponentov
    """
    try:
        logger.info(f"Generujem návrhy pre kontext: {context}")
        
        # Použitie suggestion engine
        suggestions = await suggestion_engine.suggest_components(
            context=context,
            page_type=page_type,
            framework=framework,
            max_suggestions=max_suggestions
        )
        
        return {
            "suggestions": [
                {
                    "component_type": s.component_type,
                    "name": s.name,
                    "description": s.description,
                    "confidence": s.confidence,
                    "props": s.props.dict() if s.props else {},
                    "reason": s.reason,
                    "use_case": s.use_case
                }
                for s in suggestions
            ]
        }
        
    except Exception as e:
        logger.error(f"Chyba pri generovaní návrhov: {e}")
        return {
            "suggestions": [],
            "error": str(e)
        }


@app.tool()
async def validate_component(
    html: str,
    component_type: str = None,
    strict: bool = False
) -> Dict[str, Any]:
    """
    Validuje Flowbite komponent
    
    Args:
        html: HTML kód na validáciu
        component_type: Očakávaný typ komponentu (voliteľné)
        strict: Prísna validácia
        
    Returns:
        Výsledok validácie s hodnotením a návrhmi
    """
    try:
        logger.info(f"Validujem komponent typu: {component_type}")
        
        # Použitie validátora
        result = await validator.validate_component(
            html=html,
            component_type=component_type,
            strict=strict
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Chyba pri validácii komponentu: {e}")
        return {
            "is_valid": False,
            "score": 0,
            "error": str(e)
        }


# MCP Resources
@app.resource("flowbite://components/{component_type}")
async def get_component_resource(component_type: str) -> str:
    """
    Poskytuje informácie o Flowbite komponente
    
    Args:
        component_type: Typ komponentu
        
    Returns:
        JSON s informáciami o komponente
    """
    try:
        logger.info(f"Získavam resource pre komponent: {component_type}")
        
        # Použitie component database
        component_data = await component_db.get_component(component_type)
        
        if not component_data:
            return json.dumps({
                "error": f"Komponent '{component_type}' nebol nájdený",
                "available_components": list(config.supported_components)
            }, ensure_ascii=False)
        
        return json.dumps(component_data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"Chyba pri získavaní resource: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@app.resource("flowbite://components/{component_type}/{variant}")
async def get_component_variant_resource(component_type: str, variant: str) -> str:
    """
    Poskytuje informácie o špecifickej variante komponentu
    
    Args:
        component_type: Typ komponentu
        variant: Varianta komponentu
        
    Returns:
        JSON s informáciami o variante
    """
    try:
        logger.info(f"Získavam resource pre: {component_type}/{variant}")
        
        # Použitie component database
        variant_data = await component_db.get_component(component_type, variant)
        
        if not variant_data:
            return json.dumps({
                "error": f"Varianta '{variant}' komponentu '{component_type}' nebola nájdená"
            }, ensure_ascii=False)
        
        return json.dumps(variant_data, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"Chyba pri získavaní variant resource: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@app.resource("flowbite://docs/{section}")
async def get_documentation_resource(section: str) -> str:
    """
    Poskytuje dokumentáciu pre danú sekciu
    
    Args:
        section: Názov sekcie dokumentácie
        
    Returns:
        Markdown obsah dokumentácie
    """
    try:
        logger.info(f"Získavam dokumentáciu: {section}")
        
        # Použitie documentation manager
        content = await documentation_manager.get_documentation(section)
        
        if not content:
            available_sections = await documentation_manager.list_sections()
            return f"""# Sekcia '{section}' nebola nájdená

## Dostupné sekcie:

{chr(10).join(f"- {s['id']}: {s['title']}" for s in available_sections)}
"""
        
        return content
        
    except Exception as e:
        logger.error(f"Chyba pri získavaní dokumentácie: {e}")
        return f"# Chyba\n\n{str(e)}"


# Inicializácia FastMCP aplikácie
app = FastMCP(config.name, version=config.version)


async def main():
    """Hlavná funkcia servera"""
    try:
        logger.info(f"Spúšťam {config.name} v{config.version}")
        logger.info(f"Podporované komponenty: {', '.join(config.supported_components)}")
        
        # Spustenie MCP servera
        await app.run()
        
    except KeyboardInterrupt:
        logger.info("Server ukončený používateľom")
    except Exception as e:
        logger.error(f"Kritická chyba servera: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())