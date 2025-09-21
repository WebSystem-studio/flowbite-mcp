"""
Dátové modely pre Flowbite komponenty
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
from enum import Enum


class ComponentType(str, Enum):
    """Typy Flowbite komponentov"""
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
    ACCORDION = "accordion"
    BADGE = "badge"
    BANNER = "banner"
    CAROUSEL = "carousel"
    DATEPICKER = "datepicker"
    DRAWER = "drawer"
    FOOTER = "footer"
    GALLERY = "gallery"
    INDICATOR = "indicator"
    JUMBOTRON = "jumbotron"
    LIST_GROUP = "list-group"
    MEGA_MENU = "mega-menu"
    POPOVER = "popover"
    PROGRESS = "progress"
    RATING = "rating"
    SIDEBAR = "sidebar"
    SPINNER = "spinner"
    STEPPER = "stepper"
    TAB = "tab"
    TIMELINE = "timeline"
    TOAST = "toast"
    TOOLTIP = "tooltip"


class ComponentVariant(str, Enum):
    """Varianty komponentov"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"
    DEFAULT = "default"
    ALTERNATIVE = "alternative"
    OUTLINE = "outline"
    GRADIENT = "gradient"


class ComponentSize(str, Enum):
    """Veľkosti komponentov"""
    XS = "xs"
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"
    XXL = "2xl"
    XXXL = "3xl"


class ComponentPosition(str, Enum):
    """Pozície pre komponenty ako tooltip, popover atď."""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"


class ComponentTheme(str, Enum):
    """Témy komponentov"""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


class ComponentProps(BaseModel):
    """Základné vlastnosti komponentu"""
    variant: Optional[ComponentVariant] = ComponentVariant.PRIMARY
    size: Optional[ComponentSize] = ComponentSize.MD
    disabled: bool = False
    rounded: bool = True
    shadow: bool = False
    dark_mode: bool = True
    responsive: bool = True
    theme: ComponentTheme = ComponentTheme.LIGHT
    custom_classes: Optional[str] = None
    position: Optional[ComponentPosition] = None
    
    # Špecifické vlastnosti
    outline: bool = False
    gradient: bool = False
    pill: bool = False
    loading: bool = False
    icon: Optional[str] = None
    href: Optional[str] = None
    target: Optional[str] = None
    
    # Form specific
    required: bool = False
    placeholder: Optional[str] = None
    value: Optional[str] = None
    
    # Interactive
    clickable: bool = False
    dismissible: bool = False
    collapsible: bool = False


class ComponentExample(BaseModel):
    """Príklad použitia komponentu"""
    name: str = Field(..., description="Názov príkladu")
    description: Optional[str] = Field(None, description="Popis príkladu")
    code: str = Field(..., description="HTML kód príkladu")
    preview_url: Optional[str] = Field(None, description="URL na náhľad")
    category: Optional[str] = Field(None, description="Kategória príkladu")


class ComponentVariation(BaseModel):
    """Variácia komponentu"""
    id: str = Field(..., description="ID variácie")
    name: str = Field(..., description="Názov variácie")
    description: Optional[str] = Field(None, description="Popis variácie")
    props: ComponentProps = Field(default_factory=ComponentProps)
    html_template: str = Field(..., description="HTML šablóna variácie")
    css_classes: List[str] = Field(default_factory=list)


class FlowbiteComponent(BaseModel):
    """Hlavný model pre Flowbite komponent"""
    id: str = Field(..., description="Jedinečný identifikátor komponentu")
    type: ComponentType = Field(..., description="Typ komponentu")
    name: str = Field(..., description="Názov komponentu")
    description: str = Field(..., description="Popis komponentu")
    category: str = Field(..., description="Kategória komponentu")
    
    # Základné vlastnosti
    props: ComponentProps = Field(default_factory=ComponentProps)
    html_template: str = Field(..., description="HTML šablóna komponentu")
    css_classes: List[str] = Field(default_factory=list, description="CSS triedy")
    javascript: Optional[str] = Field(None, description="JavaScript kód")
    
    # Variácie a príklady
    variations: List[ComponentVariation] = Field(default_factory=list)
    examples: List[ComponentExample] = Field(default_factory=list)
    
    # Metadáta
    documentation_url: Optional[str] = Field(None, description="URL dokumentácie")
    flowbite_version: Optional[str] = Field(None, description="Verzia Flowbite")
    tailwind_version: Optional[str] = Field(None, description="Verzia Tailwind CSS")
    tags: List[str] = Field(default_factory=list, description="Tagy komponentu")
    
    # Accessibility
    accessibility: Dict[str, Union[str, bool]] = Field(
        default_factory=dict, 
        description="Accessibility vlastnosti"
    )
    
    # Interaktivita
    interactive: bool = Field(False, description="Či je komponent interaktívny")
    requires_js: bool = Field(False, description="Či vyžaduje JavaScript")
    
    # Kompatibilita
    browser_support: List[str] = Field(
        default_factory=list, 
        description="Podporované prehliadače"
    )
    
    # Dependencie
    dependencies: List[str] = Field(
        default_factory=list,
        description="Požadované dependencie"
    )

    class Config:
        """Konfigurácia modelu"""
        json_encoders = {
            ComponentType: lambda v: v.value,
            ComponentVariant: lambda v: v.value,
            ComponentSize: lambda v: v.value,
        }
        
        schema_extra = {
            "example": {
                "id": "btn-primary-md",
                "type": "button",
                "name": "Primary Button",
                "description": "Hlavné akčné tlačidlo s primary farbou",
                "category": "buttons",
                "props": {
                    "variant": "primary",
                    "size": "md",
                    "rounded": True,
                    "dark_mode": True
                },
                "html_template": "<button type=\"button\" class=\"{{classes}}\">{{text}}</button>",
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
                    "py-2.5"
                ],
                "tags": ["button", "primary", "action", "form"]
            }
        }


class ComponentGenerationRequest(BaseModel):
    """Request pre generovanie komponentu"""
    component_type: ComponentType = Field(..., description="Typ komponentu na generovanie")
    props: ComponentProps = Field(default_factory=ComponentProps)
    content: Optional[str] = Field(None, description="Obsah komponentu")
    additional_classes: Optional[str] = Field(None, description="Dodatočné CSS triedy")
    custom_attributes: Dict[str, str] = Field(default_factory=dict)
    
    # Kontextové informácie
    context: Optional[str] = Field(None, description="Kontext použitia")
    target_framework: str = Field("html", description="Cieľový framework")
    include_javascript: bool = Field(False, description="Zahrnúť JavaScript")
    
    class Config:
        schema_extra = {
            "example": {
                "component_type": "button",
                "props": {
                    "variant": "primary",
                    "size": "lg",
                    "rounded": True
                },
                "content": "Kliknite sem",
                "context": "login form submit button"
            }
        }


class ComponentValidationResult(BaseModel):
    """Výsledok validácie komponentu"""
    valid: bool = Field(..., description="Či je komponent validný")
    errors: List[str] = Field(default_factory=list, description="Chyby")
    warnings: List[str] = Field(default_factory=list, description="Upozornenia")
    suggestions: List[str] = Field(default_factory=list, description="Návrhy na zlepšenie")
    score: float = Field(0.0, description="Skóre kvality (0-100)")
    
    # Detailná analýza
    accessibility_score: float = Field(0.0, description="Accessibility skóre")
    performance_score: float = Field(0.0, description="Performance skóre")
    best_practices_score: float = Field(0.0, description="Best practices skóre")
    
    # Metadata
    validated_at: Optional[str] = Field(None, description="Čas validácie")
    validator_version: Optional[str] = Field(None, description="Verzia validátora")


class ComponentSuggestion(BaseModel):
    """Návrh komponentu"""
    component_type: ComponentType = Field(..., description="Navrhovaný typ komponentu")
    name: str = Field(..., description="Názov návrhu")
    description: str = Field(..., description="Popis návrhu")
    confidence: float = Field(..., description="Istota návrhu (0-1)")
    props: ComponentProps = Field(default_factory=ComponentProps)
    reason: str = Field(..., description="Dôvod návrhu")
    use_case: str = Field(..., description="Prípad použitia")
    
    class Config:
        schema_extra = {
            "example": {
                "component_type": "card",
                "name": "Product Card",
                "description": "Karta pre zobrazenie produktu s obrázkom a popisom",
                "confidence": 0.95,
                "reason": "Kontext naznačuje potrebu zobraziť produkty v grid layoute",
                "use_case": "E-commerce product listing"
            }
        }