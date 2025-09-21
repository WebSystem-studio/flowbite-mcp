"""
Konfigurácia pre Flowbite MCP Server
"""

import os
from typing import Optional, List
from pathlib import Path


class ServerConfig:
    """Hlavná konfigurácia servera"""
    
    def __init__(self):
        # Základné nastavenia servera
        self.name: str = os.getenv("MCP_SERVER_NAME", "flowbite-mcp-server")
        self.version: str = os.getenv("MCP_SERVER_VERSION", "0.1.0")
        self.description: str = os.getenv(
            "MCP_SERVER_DESCRIPTION", 
            "MCP server pre Flowbite komponenty"
        )
        
        # Cesty k dátam
        self.base_dir = Path(__file__).parent.parent
        self.components_dir: str = os.getenv(
            "COMPONENTS_DIR", 
            str(self.base_dir / "data" / "components")
        )
        self.examples_dir: str = os.getenv(
            "EXAMPLES_DIR", 
            str(self.base_dir / "data" / "examples")
        )
        self.schemas_dir: str = os.getenv(
            "SCHEMAS_DIR",
            str(self.base_dir / "data" / "schemas")
        )
        
        # Generovanie komponentov
        self.default_theme: str = os.getenv("DEFAULT_THEME", "light")
        self.include_dark_mode: bool = os.getenv("INCLUDE_DARK_MODE", "true").lower() == "true"
        self.responsive_default: bool = os.getenv("RESPONSIVE_DEFAULT", "true").lower() == "true"
        
        # Validácia
        self.strict_validation: bool = os.getenv("STRICT_VALIDATION", "true").lower() == "true"
        self.auto_format: bool = os.getenv("AUTO_FORMAT", "true").lower() == "true"
        
        # Development nastavenia
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Flowbite špecifické nastavenia
        self.flowbite_version: str = "2.0.0"
        self.tailwind_version: str = "3.3.0"
        
        # Podporované komponenty
        self.supported_components: List[str] = [
            "button", "form", "input", "navbar", "card", "modal", 
            "dropdown", "alert", "breadcrumb", "pagination", "table",
            "accordion", "badge", "banner", "carousel", "datepicker"
        ]
        
        # CSS framework nastavenia
        self.css_framework: str = "tailwind"
        self.include_flowbite_js: bool = True
        self.include_flowbite_css: bool = True
        
        # Template engine
        self.template_engine: str = "jinja2"
        self.template_cache: bool = True
        
        # Performance nastavenia
        self.cache_components: bool = True
        self.cache_ttl: int = 3600  # 1 hodina
        
        # Accessibility
        self.enforce_accessibility: bool = True
        self.accessibility_level: str = "AA"  # WCAG level
        
        # Bezpečnosť
        self.sanitize_html: bool = True
        self.allowed_html_tags: List[str] = [
            "div", "span", "p", "h1", "h2", "h3", "h4", "h5", "h6",
            "button", "a", "img", "ul", "ol", "li", "form", "input",
            "label", "select", "option", "textarea", "nav", "header",
            "footer", "section", "article", "aside", "main"
        ]
        
        # Limits
        self.max_component_size: int = 100000  # 100KB
        self.max_components_per_request: int = 10
        self.rate_limit_per_minute: int = 100
        
        # Lokalizácia
        self.default_language: str = "sk"
        self.supported_languages: List[str] = ["sk", "en", "cs"]
        
    def get_component_path(self, component_type: str) -> Path:
        """Vráti cestu k súboru s komponentmi daného typu"""
        return Path(self.components_dir) / f"{component_type}.json"
    
    def get_examples_path(self, component_type: str) -> Path:
        """Vráti cestu k príkladom daného typu komponentu"""
        return Path(self.examples_dir) / f"{component_type}_examples.json"
    
    def get_schema_path(self, schema_name: str) -> Path:
        """Vráti cestu k validačnej schéme"""
        return Path(self.schemas_dir) / f"{schema_name}_schema.json"
    
    def is_component_supported(self, component_type: str) -> bool:
        """Kontroluje či je typ komponentu podporovaný"""
        return component_type.lower() in self.supported_components
    
    def get_cdn_urls(self) -> dict:
        """Vráti CDN URLs pre Flowbite a Tailwind"""
        return {
            "tailwind_css": f"https://cdn.tailwindcss.com/{self.tailwind_version}",
            "flowbite_css": f"https://cdnjs.cloudflare.com/ajax/libs/flowbite/{self.flowbite_version}/flowbite.min.css",
            "flowbite_js": f"https://cdnjs.cloudflare.com/ajax/libs/flowbite/{self.flowbite_version}/flowbite.min.js"
        }
    
    def get_tailwind_config(self) -> dict:
        """Vráti základnú Tailwind konfiguráciu pre Flowbite"""
        return {
            "content": [
                "./src/**/*.{html,js,ts,jsx,tsx}",
                "./node_modules/flowbite/**/*.js"
            ],
            "theme": {
                "extend": {
                    "colors": {
                        "primary": {
                            "50": "#eff6ff",
                            "100": "#dbeafe", 
                            "200": "#bfdbfe",
                            "300": "#93c5fd",
                            "400": "#60a5fa",
                            "500": "#3b82f6",
                            "600": "#2563eb",
                            "700": "#1d4ed8",
                            "800": "#1e40af",
                            "900": "#1e3a8a"
                        }
                    }
                }
            },
            "plugins": ["flowbite/plugin"]
        }
    
    def validate_config(self) -> List[str]:
        """Validuje konfiguráciu a vráti zoznam chýb"""
        errors = []
        
        # Kontrola existencie adresárov
        for dir_path in [self.components_dir, self.examples_dir, self.schemas_dir]:
            if not Path(dir_path).exists():
                errors.append(f"Adresár neexistuje: {dir_path}")
        
        # Kontrola podporovaných hodnôt
        if self.default_theme not in ["light", "dark", "auto"]:
            errors.append(f"Nepodporovaná téma: {self.default_theme}")
        
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            errors.append(f"Nepodporovaný log level: {self.log_level}")
        
        if self.accessibility_level not in ["A", "AA", "AAA"]:
            errors.append(f"Nepodporovaný accessibility level: {self.accessibility_level}")
        
        return errors


# Globálna inštancia konfigurácie
config = ServerConfig()


# Pomocné funkcie
def load_env_file(env_path: Optional[str] = None) -> None:
    """Načíta environment variables z .env súboru"""
    if env_path is None:
        env_path = Path(__file__).parent.parent / ".env"
    
    if Path(env_path).exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
        except ImportError:
            print("python-dotenv nie je nainštalovaný, preskakujem načítanie .env súboru")


def get_config() -> ServerConfig:
    """Vráti globálnu konfiguráciu"""
    return config


def reload_config() -> ServerConfig:
    """Znovu načíta konfiguráciu"""
    global config
    config = ServerConfig()
    return config


def validate_environment() -> bool:
    """Validuje environment a konfiguráciu"""
    errors = config.validate_config()
    
    if errors:
        print("Chyby v konfigurácii:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True


# Načítanie .env súboru pri importe
load_env_file()