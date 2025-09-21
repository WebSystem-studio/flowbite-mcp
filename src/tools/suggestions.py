"""
Inteligentné návrhy pre Flowbite komponenty
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from ..config import get_config
from ..models.component import (
    ComponentSuggestion,
    ComponentType,
    ComponentVariant,
    ComponentSize,
    ComponentProps
)

# Konfigurácia
config = get_config()
logger = logging.getLogger(__name__)


class PageType(str, Enum):
    """Typy stránok"""
    LANDING = "landing"
    DASHBOARD = "dashboard"
    ECOMMERCE = "ecommerce"
    BLOG = "blog"
    PORTFOLIO = "portfolio"
    ADMIN = "admin"
    AUTH = "auth"
    DOCUMENTATION = "documentation"
    GENERAL = "general"


class Framework(str, Enum):
    """Podporované frameworky"""
    HTML = "html"
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"
    SVELTE = "svelte"


@dataclass
class ContextKeyword:
    """Kľúčové slovo pre analýzu kontextu"""
    keyword: str
    component_types: List[ComponentType]
    confidence_boost: float
    page_types: List[PageType]


class FlowbiteSuggestionEngine:
    """Engine pre generovanie inteligentných návrhov"""
    
    def __init__(self):
        self.config = config
        self.context_keywords = self._load_context_keywords()
        self.component_patterns = self._load_component_patterns()
        self.use_case_templates = self._load_use_case_templates()
        
    def _load_context_keywords(self) -> List[ContextKeyword]:
        """Načíta kľúčové slová pre analýzu kontextu"""
        return [
            # Navigation related
            ContextKeyword("navigation", [ComponentType.NAVBAR], 0.9, [PageType.GENERAL]),
            ContextKeyword("menu", [ComponentType.NAVBAR, ComponentType.DROPDOWN], 0.8, [PageType.GENERAL]),
            ContextKeyword("header", [ComponentType.NAVBAR], 0.8, [PageType.GENERAL]),
            
            # Form related
            ContextKeyword("login", [ComponentType.FORM, ComponentType.BUTTON], 0.9, [PageType.AUTH]),
            ContextKeyword("register", [ComponentType.FORM, ComponentType.BUTTON], 0.9, [PageType.AUTH]),
            ContextKeyword("contact", [ComponentType.FORM], 0.8, [PageType.GENERAL]),
            ContextKeyword("search", [ComponentType.INPUT, ComponentType.BUTTON], 0.8, [PageType.GENERAL]),
            ContextKeyword("form", [ComponentType.FORM, ComponentType.INPUT], 0.7, [PageType.GENERAL]),
            
            # Content related
            ContextKeyword("product", [ComponentType.CARD], 0.8, [PageType.ECOMMERCE]),
            ContextKeyword("article", [ComponentType.CARD], 0.7, [PageType.BLOG]),
            ContextKeyword("post", [ComponentType.CARD], 0.7, [PageType.BLOG]),
            ContextKeyword("gallery", [ComponentType.CARD, ComponentType.CAROUSEL], 0.7, [PageType.PORTFOLIO]),
            
            # Interactive
            ContextKeyword("button", [ComponentType.BUTTON], 0.9, [PageType.GENERAL]),
            ContextKeyword("click", [ComponentType.BUTTON], 0.6, [PageType.GENERAL]),
            ContextKeyword("submit", [ComponentType.BUTTON], 0.8, [PageType.GENERAL]),
            ContextKeyword("modal", [ComponentType.MODAL, ComponentType.BUTTON], 0.9, [PageType.GENERAL]),
            ContextKeyword("popup", [ComponentType.MODAL], 0.8, [PageType.GENERAL]),
            ContextKeyword("dialog", [ComponentType.MODAL], 0.8, [PageType.GENERAL]),
            
            # Notification
            ContextKeyword("alert", [ComponentType.ALERT], 0.9, [PageType.GENERAL]),
            ContextKeyword("notification", [ComponentType.TOAST, ComponentType.ALERT], 0.8, [PageType.GENERAL]),
            ContextKeyword("warning", [ComponentType.ALERT], 0.7, [PageType.GENERAL]),
            ContextKeyword("error", [ComponentType.ALERT], 0.7, [PageType.GENERAL]),
            
            # Data display
            ContextKeyword("table", [ComponentType.TABLE], 0.9, [PageType.DASHBOARD, PageType.ADMIN]),
            ContextKeyword("list", [ComponentType.LIST_GROUP], 0.7, [PageType.GENERAL]),
            ContextKeyword("chart", [ComponentType.CHART], 0.8, [PageType.DASHBOARD]),
            ContextKeyword("graph", [ComponentType.CHART], 0.8, [PageType.DASHBOARD]),
            
            # Layout
            ContextKeyword("sidebar", [ComponentType.SIDEBAR], 0.8, [PageType.DASHBOARD, PageType.ADMIN]),
            ContextKeyword("footer", [ComponentType.FOOTER], 0.7, [PageType.GENERAL]),
            ContextKeyword("breadcrumb", [ComponentType.BREADCRUMB], 0.7, [PageType.GENERAL]),
            
            # E-commerce specific
            ContextKeyword("cart", [ComponentType.BUTTON, ComponentType.BADGE], 0.8, [PageType.ECOMMERCE]),
            ContextKeyword("checkout", [ComponentType.FORM, ComponentType.BUTTON], 0.9, [PageType.ECOMMERCE]),
            ContextKeyword("price", [ComponentType.BADGE], 0.6, [PageType.ECOMMERCE]),
            ContextKeyword("rating", [ComponentType.RATING], 0.8, [PageType.ECOMMERCE]),
        ]
    
    def _load_component_patterns(self) -> Dict[ComponentType, Dict[str, Any]]:
        """Načíta vzory pre komponenty"""
        return {
            ComponentType.BUTTON: {
                "common_variants": [ComponentVariant.PRIMARY, ComponentVariant.SECONDARY],
                "common_sizes": [ComponentSize.MD, ComponentSize.LG],
                "common_use_cases": ["submit", "action", "navigation", "cancel"],
                "often_paired_with": [ComponentType.FORM, ComponentType.MODAL]
            },
            ComponentType.FORM: {
                "common_variants": [ComponentVariant.DEFAULT],
                "common_fields": ["email", "password", "name", "message"],
                "common_use_cases": ["login", "register", "contact", "search"],
                "often_paired_with": [ComponentType.BUTTON, ComponentType.INPUT]
            },
            ComponentType.CARD: {
                "common_variants": [ComponentVariant.DEFAULT, ComponentVariant.LIGHT],
                "common_use_cases": ["product", "article", "profile", "dashboard-widget"],
                "often_paired_with": [ComponentType.BUTTON, ComponentType.BADGE]
            },
            ComponentType.NAVBAR: {
                "common_variants": [ComponentVariant.DEFAULT, ComponentVariant.DARK],
                "common_use_cases": ["main-navigation", "top-bar"],
                "often_paired_with": [ComponentType.DROPDOWN, ComponentType.BUTTON]
            },
            ComponentType.MODAL: {
                "common_variants": [ComponentVariant.DEFAULT],
                "common_sizes": [ComponentSize.MD, ComponentSize.LG],
                "common_use_cases": ["confirmation", "form", "details", "image-view"],
                "often_paired_with": [ComponentType.BUTTON, ComponentType.FORM]
            }
        }
    
    def _load_use_case_templates(self) -> Dict[PageType, List[Dict[str, Any]]]:
        """Načíta šablóny pre rôzne typy stránok"""
        return {
            PageType.LANDING: [
                {
                    "name": "Hero Section",
                    "components": [ComponentType.NAVBAR, ComponentType.BUTTON, ComponentType.CARD],
                    "description": "Hlavná sekcia s navigáciou a call-to-action"
                },
                {
                    "name": "Features Section",
                    "components": [ComponentType.CARD],
                    "description": "Sekcia s charakteristikami produktu"
                },
                {
                    "name": "Contact Form",
                    "components": [ComponentType.FORM, ComponentType.BUTTON],
                    "description": "Kontaktný formulár"
                }
            ],
            PageType.DASHBOARD: [
                {
                    "name": "Sidebar Navigation",
                    "components": [ComponentType.SIDEBAR, ComponentType.NAVBAR],
                    "description": "Bočná navigácia pre dashboard"
                },
                {
                    "name": "Stats Cards",
                    "components": [ComponentType.CARD, ComponentType.CHART],
                    "description": "Karty so štatistikami"
                },
                {
                    "name": "Data Table",
                    "components": [ComponentType.TABLE, ComponentType.PAGINATION],
                    "description": "Tabuľka s dátami a stránkovaním"
                }
            ],
            PageType.ECOMMERCE: [
                {
                    "name": "Product Grid",
                    "components": [ComponentType.CARD, ComponentType.BUTTON, ComponentType.BADGE],
                    "description": "Mriežka produktov"
                },
                {
                    "name": "Shopping Cart",
                    "components": [ComponentType.BUTTON, ComponentType.BADGE, ComponentType.MODAL],
                    "description": "Nákupný košík"
                },
                {
                    "name": "Checkout Form",
                    "components": [ComponentType.FORM, ComponentType.BUTTON],
                    "description": "Formulár pre dokončenie objednávky"
                }
            ],
            PageType.AUTH: [
                {
                    "name": "Login Form",
                    "components": [ComponentType.FORM, ComponentType.BUTTON],
                    "description": "Prihlasovací formulár"
                },
                {
                    "name": "Registration Form",
                    "components": [ComponentType.FORM, ComponentType.BUTTON],
                    "description": "Registračný formulár"
                }
            ]
        }
    
    async def suggest_components(
        self,
        context: str,
        page_type: str = "general",
        framework: str = "html",
        max_suggestions: int = 5
    ) -> List[ComponentSuggestion]:
        """
        Navrhne komponenty na základe kontextu
        
        Args:
            context: Popis toho, čo užívateľ potrebuje
            page_type: Typ stránky
            framework: Framework
            max_suggestions: Maximum návrhov
            
        Returns:
            Zoznam navrhnutých komponentov
        """
        try:
            suggestions = []
            
            # Analýza kontextu
            context_analysis = self._analyze_context(context.lower())
            
            # Konverzia page_type
            try:
                page_enum = PageType(page_type.lower())
            except ValueError:
                page_enum = PageType.GENERAL
            
            # Generovanie návrhov na základe kľúčových slov
            keyword_suggestions = self._generate_keyword_suggestions(
                context_analysis, page_enum, max_suggestions
            )
            suggestions.extend(keyword_suggestions)
            
            # Generovanie návrhov na základe typu stránky
            page_suggestions = self._generate_page_type_suggestions(
                page_enum, context, max_suggestions - len(suggestions)
            )
            suggestions.extend(page_suggestions)
            
            # Generovanie návrhov na základe vzory
            pattern_suggestions = self._generate_pattern_suggestions(
                context, max_suggestions - len(suggestions)
            )
            suggestions.extend(pattern_suggestions)
            
            # Zoradenieie podľa confidence
            suggestions.sort(key=lambda x: x.confidence, reverse=True)
            
            return suggestions[:max_suggestions]
            
        except Exception as e:
            logger.error(f"Chyba pri generovaní návrhov: {e}")
            return []
    
    def _analyze_context(self, context: str) -> Dict[str, Any]:
        """Analyzuje kontext a extrahuje kľúčové informácie"""
        analysis = {
            "keywords": [],
            "intent": None,
            "complexity": "simple",
            "interactive": False,
            "data_heavy": False
        }
        
        # Hľadanie kľúčových slov
        for keyword_obj in self.context_keywords:
            if keyword_obj.keyword in context:
                analysis["keywords"].append(keyword_obj)
        
        # Určenie zámeru
        if any(word in context for word in ["create", "make", "build", "generate"]):
            analysis["intent"] = "create"
        elif any(word in context for word in ["show", "display", "list"]):
            analysis["intent"] = "display"
        elif any(word in context for word in ["form", "input", "submit"]):
            analysis["intent"] = "input"
        
        # Určenie komplexnosti
        if len(analysis["keywords"]) > 3:
            analysis["complexity"] = "complex"
        elif len(analysis["keywords"]) > 1:
            analysis["complexity"] = "medium"
        
        # Interaktivita
        interactive_words = ["click", "button", "form", "input", "submit", "modal"]
        analysis["interactive"] = any(word in context for word in interactive_words)
        
        # Data heavy
        data_words = ["table", "list", "chart", "graph", "data", "statistics"]
        analysis["data_heavy"] = any(word in context for word in data_words)
        
        return analysis
    
    def _generate_keyword_suggestions(
        self,
        context_analysis: Dict[str, Any],
        page_type: PageType,
        max_suggestions: int
    ) -> List[ComponentSuggestion]:
        """Generuje návrhy na základe kľúčových slov"""
        suggestions = []
        
        for keyword_obj in context_analysis["keywords"]:
            for component_type in keyword_obj.component_types:
                # Kontrola relevancie pre typ stránky
                relevance_boost = 0.1 if page_type in keyword_obj.page_types else 0
                confidence = min(0.95, keyword_obj.confidence_boost + relevance_boost)
                
                # Získanie vzory pre komponent
                pattern = self.component_patterns.get(component_type, {})
                
                suggestion = ComponentSuggestion(
                    component_type=component_type,
                    name=f"{component_type.value.title()} pre '{keyword_obj.keyword}'",
                    description=self._generate_component_description(
                        component_type, keyword_obj.keyword, pattern
                    ),
                    confidence=confidence,
                    props=self._generate_component_props(component_type, pattern),
                    reason=f"Detekované kľúčové slovo '{keyword_obj.keyword}' naznačuje potrebu {component_type.value}",
                    use_case=self._generate_use_case(component_type, keyword_obj.keyword)
                )
                
                suggestions.append(suggestion)
                
                if len(suggestions) >= max_suggestions:
                    break
            
            if len(suggestions) >= max_suggestions:
                break
        
        return suggestions
    
    def _generate_page_type_suggestions(
        self,
        page_type: PageType,
        context: str,
        max_suggestions: int
    ) -> List[ComponentSuggestion]:
        """Generuje návrhy na základe typu stránky"""
        suggestions = []
        
        templates = self.use_case_templates.get(page_type, [])
        
        for template in templates:
            if len(suggestions) >= max_suggestions:
                break
                
            # Kontrola relevancie template
            template_relevance = self._calculate_template_relevance(template, context)
            
            if template_relevance < 0.3:
                continue
            
            for component_type in template["components"]:
                if len(suggestions) >= max_suggestions:
                    break
                
                pattern = self.component_patterns.get(component_type, {})
                
                suggestion = ComponentSuggestion(
                    component_type=component_type,
                    name=f"{component_type.value.title()} pre {template['name']}",
                    description=f"{template['description']} - {component_type.value}",
                    confidence=min(0.9, 0.6 + template_relevance),
                    props=self._generate_component_props(component_type, pattern),
                    reason=f"Odporúčané pre {page_type.value} stránky: {template['name']}",
                    use_case=template["description"]
                )
                
                suggestions.append(suggestion)
        
        return suggestions
    
    def _generate_pattern_suggestions(
        self,
        context: str,
        max_suggestions: int
    ) -> List[ComponentSuggestion]:
        """Generuje návrhy na základe vzory"""
        suggestions = []
        
        # Základné vzory pre bežné use cases
        common_patterns = [
            {
                "keywords": ["website", "page", "site"],
                "components": [ComponentType.NAVBAR, ComponentType.BUTTON, ComponentType.FOOTER],
                "confidence": 0.5
            },
            {
                "keywords": ["admin", "management", "control"],
                "components": [ComponentType.SIDEBAR, ComponentType.TABLE, ComponentType.BUTTON],
                "confidence": 0.6
            },
            {
                "keywords": ["shop", "store", "buy", "sell"],
                "components": [ComponentType.CARD, ComponentType.BUTTON, ComponentType.BADGE],
                "confidence": 0.7
            }
        ]
        
        for pattern in common_patterns:
            if len(suggestions) >= max_suggestions:
                break
            
            # Kontrola či kontext zodpovedá vzoru
            pattern_match = any(keyword in context for keyword in pattern["keywords"])
            
            if pattern_match:
                for component_type in pattern["components"]:
                    if len(suggestions) >= max_suggestions:
                        break
                    
                    comp_pattern = self.component_patterns.get(component_type, {})
                    
                    suggestion = ComponentSuggestion(
                        component_type=component_type,
                        name=f"Základný {component_type.value}",
                        description=f"Štandardný {component_type.value} komponent",
                        confidence=pattern["confidence"],
                        props=self._generate_component_props(component_type, comp_pattern),
                        reason=f"Bežne používané pre tento typ aplikácie",
                        use_case="Všeobecné použitie"
                    )
                    
                    suggestions.append(suggestion)
        
        return suggestions
    
    def _calculate_template_relevance(self, template: Dict[str, Any], context: str) -> float:
        """Vypočíta relevanciu template pre daný kontext"""
        template_keywords = template["name"].lower().split() + template["description"].lower().split()
        context_words = context.lower().split()
        
        matches = sum(1 for word in template_keywords if word in context_words)
        return matches / len(template_keywords) if template_keywords else 0
    
    def _generate_component_description(
        self,
        component_type: ComponentType,
        keyword: str,
        pattern: Dict[str, Any]
    ) -> str:
        """Generuje popis komponentu"""
        descriptions = {
            ComponentType.BUTTON: f"Akčné tlačidlo pre {keyword} operácie",
            ComponentType.FORM: f"Formulár pre {keyword} funkcionalitu",
            ComponentType.CARD: f"Karta pre zobrazenie {keyword} obsahu",
            ComponentType.NAVBAR: f"Navigačná lišta s {keyword} menu",
            ComponentType.MODAL: f"Modálne okno pre {keyword} akcie",
            ComponentType.TABLE: f"Tabuľka pre {keyword} dáta",
            ComponentType.INPUT: f"Vstupné pole pre {keyword}",
            ComponentType.ALERT: f"Upozornenie pre {keyword} udalosti"
        }
        
        return descriptions.get(component_type, f"Komponent {component_type.value} pre {keyword}")
    
    def _generate_component_props(
        self,
        component_type: ComponentType,
        pattern: Dict[str, Any]
    ) -> ComponentProps:
        """Generuje vlastnosti komponentu"""
        props = ComponentProps()
        
        # Nastavenie variant na základe vzory
        common_variants = pattern.get("common_variants", [ComponentVariant.PRIMARY])
        if common_variants:
            props.variant = common_variants[0]
        
        # Nastavenie veľkosti
        common_sizes = pattern.get("common_sizes", [ComponentSize.MD])
        if common_sizes:
            props.size = common_sizes[0]
        
        # Špecifické nastavenia pre rôzne typy
        if component_type == ComponentType.BUTTON:
            props.rounded = True
            props.shadow = False
        elif component_type == ComponentType.CARD:
            props.shadow = True
            props.rounded = True
        elif component_type == ComponentType.FORM:
            props.variant = ComponentVariant.DEFAULT
        
        return props
    
    def _generate_use_case(self, component_type: ComponentType, keyword: str) -> str:
        """Generuje use case pre komponent"""
        use_cases = {
            ComponentType.BUTTON: f"Tlačidlo pre {keyword} akcie v aplikácii",
            ComponentType.FORM: f"Zber dát relacionovaných s {keyword}",
            ComponentType.CARD: f"Prezentácia {keyword} informácií v štruktúrovanom formáte",
            ComponentType.NAVBAR: f"Navigácia medzi {keyword} sekciami",
            ComponentType.MODAL: f"Zobrazenie {keyword} detailov alebo formulárov",
            ComponentType.TABLE: f"Organizácia a zobrazenie {keyword} dát",
            ComponentType.INPUT: f"Vstup {keyword} dát od používateľa"
        }
        
        return use_cases.get(component_type, f"Všeobecné použitie pre {keyword}")
    
    async def analyze_layout(self, html_code: str) -> Dict[str, Any]:
        """Analyzuje existujúci layout a navrhne vylepšenia"""
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html_code, 'html.parser')
            analysis = {
                "structure": {},
                "components_found": [],
                "missing_components": [],
                "improvements": [],
                "accessibility_issues": [],
                "performance_issues": []
            }
            
            # Analýza štruktúry
            analysis["structure"] = {
                "total_elements": len(soup.find_all()),
                "nesting_depth": self._calculate_max_depth(soup),
                "has_semantic_elements": bool(soup.find_all(['nav', 'header', 'main', 'footer', 'section', 'article'])),
                "interactive_elements": len(soup.find_all(['button', 'a', 'input', 'select', 'textarea']))
            }
            
            # Detekcia existujúcich komponentov
            analysis["components_found"] = self._detect_existing_components(soup)
            
            # Návrhy chýbajúcich komponentov
            analysis["missing_components"] = self._suggest_missing_components(soup)
            
            # Návrhy vylepšení
            analysis["improvements"] = self._suggest_layout_improvements(soup)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Chyba pri analýze layout: {e}")
            return {"error": str(e)}
    
    def _calculate_max_depth(self, soup) -> int:
        """Vypočíta maximálnu hĺbku vnorenia"""
        def get_depth(element, depth=0):
            if not hasattr(element, 'children'):
                return depth
            
            max_child_depth = depth
            for child in element.children:
                if hasattr(child, 'name') and child.name:
                    child_depth = get_depth(child, depth + 1)
                    max_child_depth = max(max_child_depth, child_depth)
            
            return max_child_depth
        
        return get_depth(soup)
    
    def _detect_existing_components(self, soup) -> List[str]:
        """Detekuje existujúce Flowbite komponenty"""
        components = []
        
        # Detekcia buttonov
        if soup.find('button') or soup.find('a', class_=re.compile(r'.*btn.*')):
            components.append("button")
        
        # Detekcia formov
        if soup.find('form'):
            components.append("form")
        
        # Detekcia navbar
        if soup.find('nav'):
            components.append("navbar")
        
        # Detekcia card
        if soup.find(attrs={'class': re.compile(r'.*card.*')}):
            components.append("card")
        
        # Detekcia modal
        if soup.find(attrs={'class': re.compile(r'.*modal.*')}):
            components.append("modal")
        
        # Detekcia table
        if soup.find('table'):
            components.append("table")
        
        return components
    
    def _suggest_missing_components(self, soup) -> List[str]:
        """Navrhne chýbajúce komponenty"""
        suggestions = []
        
        # Ak má formulár ale nemá submit button
        forms = soup.find_all('form')
        for form in forms:
            if not form.find(['button', 'input'], attrs={'type': 'submit'}):
                suggestions.append("submit button pre formulár")
        
        # Ak má interaktívne elementy ale žiadny modal
        interactive_elements = soup.find_all(['button', 'a'])
        if len(interactive_elements) > 3 and not soup.find(attrs={'class': re.compile(r'.*modal.*')}):
            suggestions.append("modal pre detailné zobrazenie")
        
        # Ak má veľa obsahu ale žiadne karty
        content_elements = soup.find_all(['div', 'section', 'article'])
        if len(content_elements) > 5 and not soup.find(attrs={'class': re.compile(r'.*card.*')}):
            suggestions.append("card komponenty pre lepšiu organizáciu obsahu")
        
        return suggestions
    
    def _suggest_layout_improvements(self, soup) -> List[str]:
        """Navrhne vylepšenia layoutu"""
        improvements = []
        
        # Kontrola responzívnosti
        responsive_classes = ['sm:', 'md:', 'lg:', 'xl:']
        html_content = str(soup)
        
        if not any(pattern in html_content for pattern in responsive_classes):
            improvements.append("Pridajte responzívne CSS triedy pre lepšie zobrazenie na mobilných zariadeniach")
        
        # Kontrola accessibility
        images = soup.find_all('img')
        if any(not img.get('alt') for img in images):
            improvements.append("Pridajte alt atribúty pre všetky obrázky")
        
        # Kontrola semantic HTML
        if not soup.find_all(['nav', 'header', 'main', 'footer']):
            improvements.append("Použite semantic HTML elementy (nav, header, main, footer)")
        
        # Kontrola dark mode
        if 'dark:' not in html_content:
            improvements.append("Pridajte dark mode podporu pomocou dark: tried")
        
        return improvements


# Globálna inštancia suggestion engine
suggestion_engine = FlowbiteSuggestionEngine()