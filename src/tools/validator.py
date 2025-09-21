"""
Validátor Flowbite komponentov
"""

import re
import logging
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime
from bs4 import BeautifulSoup, Tag
import json

from ..config import get_config
from ..models.component import ComponentValidationResult, ComponentType
from ..models.schema import CSS_CLASSES, ComponentSchema

# Konfigurácia
config = get_config()
logger = logging.getLogger(__name__)


class FlowbiteValidator:
    """Hlavná trieda pre validáciu Flowbite komponentov"""
    
    def __init__(self):
        self.config = config
        self.flowbite_patterns = self._load_flowbite_patterns()
        self.accessibility_rules = self._load_accessibility_rules()
        self.performance_rules = self._load_performance_rules()
        
    def _load_flowbite_patterns(self) -> List[str]:
        """Načíta vzory CSS tried pre Flowbite"""
        return [
            r"bg-blue-\d+", r"text-white", r"rounded-lg", r"focus:ring-\d+",
            r"hover:bg-\w+-\d+", r"dark:", r"border-gray-\d+", r"px-\d+",
            r"py-\d+", r"text-\w+-\d+", r"font-medium", r"focus:outline-none",
            r"space-y-\d+", r"block", r"w-full", r"border", r"focus:border-\w+-\d+"
        ]
    
    def _load_accessibility_rules(self) -> Dict[str, Any]:
        """Načíta pravidlá pre accessibility"""
        return {
            "required_attributes": {
                "img": ["alt"],
                "input": ["id", "name"],
                "label": ["for"],
                "button": [],
                "a": ["href"]
            },
            "aria_attributes": [
                "aria-label", "aria-labelledby", "aria-describedby",
                "aria-expanded", "aria-hidden", "aria-current", "role"
            ],
            "interactive_elements": [
                "button", "a", "input", "select", "textarea"
            ],
            "heading_hierarchy": ["h1", "h2", "h3", "h4", "h5", "h6"]
        }
    
    def _load_performance_rules(self) -> Dict[str, Any]:
        """Načíta pravidlá pre performance"""
        return {
            "max_css_classes": 20,
            "max_nesting_depth": 8,
            "max_component_size": 10000,  # znakov
            "redundant_classes": [
                ("ml-2", "mr-2", "mx-2"),
                ("mt-2", "mb-2", "my-2"),
                ("pl-2", "pr-2", "px-2"),
                ("pt-2", "pb-2", "py-2")
            ]
        }
    
    async def validate_component(
        self,
        html_code: str,
        component_type: Optional[str] = None,
        strict: bool = None
    ) -> ComponentValidationResult:
        """
        Hlavná validačná funkcia
        
        Args:
            html_code: HTML kód komponentu
            component_type: Typ komponentu (ak je známy)
            strict: Prísna validácia
            
        Returns:
            Výsledok validácie
        """
        try:
            if strict is None:
                strict = self.config.strict_validation
            
            result = ComponentValidationResult(
                valid=True,
                errors=[],
                warnings=[],
                suggestions=[],
                score=100.0,
                accessibility_score=100.0,
                performance_score=100.0,
                best_practices_score=100.0,
                validated_at=datetime.now().isoformat(),
                validator_version=self.config.version
            )
            
            # Základná validácia
            await self._validate_basic_html(html_code, result)
            
            # Flowbite špecifická validácia
            await self._validate_flowbite_patterns(html_code, result)
            
            # Accessibility validácia
            await self._validate_accessibility(html_code, result)
            
            # Performance validácia
            await self._validate_performance(html_code, result)
            
            # Best practices validácia
            await self._validate_best_practices(html_code, result)
            
            # Typ-špecifická validácia
            if component_type:
                await self._validate_component_type(html_code, component_type, result)
            
            # Výpočet finálneho skóre
            self._calculate_final_score(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Chyba pri validácii: {e}")
            return ComponentValidationResult(
                valid=False,
                errors=[f"Chyba validátora: {str(e)}"],
                warnings=[],
                suggestions=[],
                score=0.0
            )
    
    async def _validate_basic_html(self, html_code: str, result: ComponentValidationResult):
        """Základná HTML validácia"""
        if not html_code or not html_code.strip():
            result.valid = False
            result.errors.append("Prázdny HTML kód")
            return
        
        # Parsovanie HTML
        try:
            soup = BeautifulSoup(html_code, 'html.parser')
        except Exception as e:
            result.valid = False
            result.errors.append(f"Neplatný HTML: {str(e)}")
            return
        
        # Kontrola párových tagov
        self._check_paired_tags(soup, result)
        
        # Kontrola povinných atribútov
        self._check_required_attributes(soup, result)
    
    async def _validate_flowbite_patterns(self, html_code: str, result: ComponentValidationResult):
        """Validácia Flowbite CSS vzory"""
        found_patterns = 0
        total_patterns = len(self.flowbite_patterns)
        
        for pattern in self.flowbite_patterns:
            if re.search(pattern, html_code):
                found_patterns += 1
        
        pattern_score = (found_patterns / total_patterns) * 100
        
        if pattern_score < 30:
            result.warnings.append("Málo Flowbite CSS tried - možno nie je to Flowbite komponent")
        elif pattern_score < 50:
            result.suggestions.append("Zvážte pridanie viacerých Flowbite CSS tried")
        
        # Kontrola dark mode podpory
        if "dark:" not in html_code:
            result.suggestions.append("Pridajte dark mode podporu pomocou 'dark:' prefix tried")
        
        # Kontrola responzívnych tried
        responsive_patterns = [r"sm:", r"md:", r"lg:", r"xl:"]
        responsive_found = any(re.search(pattern, html_code) for pattern in responsive_patterns)
        
        if not responsive_found:
            result.suggestions.append("Zvážte pridanie responzívnych CSS tried (sm:, md:, lg:, xl:)")
    
    async def _validate_accessibility(self, html_code: str, result: ComponentValidationResult):
        """Accessibility validácia"""
        soup = BeautifulSoup(html_code, 'html.parser')
        accessibility_issues = 0
        
        # Kontrola obrázkov bez alt atribútu
        images = soup.find_all('img')
        for img in images:
            if not img.get('alt'):
                result.warnings.append("Obrázok bez alt atribútu")
                accessibility_issues += 1
        
        # Kontrola labelov pre input elementy
        inputs = soup.find_all(['input', 'select', 'textarea'])
        for input_elem in inputs:
            input_id = input_elem.get('id')
            if input_id:
                label = soup.find('label', attrs={'for': input_id})
                if not label:
                    result.warnings.append(f"Input s ID '{input_id}' nemá príslušný label")
                    accessibility_issues += 1
            elif input_elem.get('type') not in ['hidden', 'submit', 'button']:
                result.warnings.append("Input element bez ID a label")
                accessibility_issues += 1
        
        # Kontrola ARIA atribútov
        interactive_elements = soup.find_all(['button', 'a', 'input', 'select', 'textarea'])
        aria_missing = 0
        
        for elem in interactive_elements:
            has_aria = any(attr.startswith('aria-') or attr == 'role' for attr in elem.attrs)
            if not has_aria and elem.name in ['button', 'a']:
                aria_missing += 1
        
        if aria_missing > 0:
            result.suggestions.append(f"Zvážte pridanie ARIA atribútov pre {aria_missing} interaktívnych elementov")
        
        # Kontrola fókusovateľnosti
        focusable_elements = soup.find_all(['button', 'a', 'input', 'select', 'textarea'])
        for elem in focusable_elements:
            if elem.get('tabindex') == '-1' and not elem.get('aria-hidden'):
                result.warnings.append("Element s tabindex='-1' môže byť problematický pre screen readery")
        
        # Výpočet accessibility skóre
        max_issues = len(images) + len(inputs) + len(interactive_elements)
        if max_issues > 0:
            result.accessibility_score = max(0, 100 - (accessibility_issues * 100 / max_issues))
        
    async def _validate_performance(self, html_code: str, result: ComponentValidationResult):
        """Performance validácia"""
        perf_rules = self.performance_rules
        performance_issues = 0
        
        # Kontrola veľkosti komponentu
        if len(html_code) > perf_rules["max_component_size"]:
            result.warnings.append(f"Komponent je príliš veľký ({len(html_code)} znakov)")
            performance_issues += 1
        
        # Kontrola počtu CSS tried
        css_classes = re.findall(r'class="([^"]*)"', html_code)
        total_classes = sum(len(classes.split()) for classes in css_classes)
        
        if total_classes > perf_rules["max_css_classes"]:
            result.suggestions.append(f"Veľa CSS tried ({total_classes}) - zvážte optimalizáciu")
            performance_issues += 1
        
        # Kontrola redundantných tried
        for classes_string in css_classes:
            classes = classes_string.split()
            for redundant_group in perf_rules["redundant_classes"]:
                found_redundant = [cls for cls in classes if any(cls.startswith(prefix) for prefix in redundant_group)]
                if len(found_redundant) > 1:
                    result.suggestions.append(f"Redundantné CSS triedy: {', '.join(found_redundant)}")
        
        # Kontrola vnorenia
        soup = BeautifulSoup(html_code, 'html.parser')
        max_depth = self._calculate_nesting_depth(soup)
        
        if max_depth > perf_rules["max_nesting_depth"]:
            result.warnings.append(f"Príliš hlboké vnorenie ({max_depth} úrovní)")
            performance_issues += 1
        
        # Výpočet performance skóre
        result.performance_score = max(0, 100 - (performance_issues * 25))
    
    async def _validate_best_practices(self, html_code: str, result: ComponentValidationResult):
        """Best practices validácia"""
        practices_issues = 0
        
        # Kontrola semantic HTML
        soup = BeautifulSoup(html_code, 'html.parser')
        
        # Použitie správnych HTML elementov
        if soup.find('div', attrs={'onclick': True}):
            result.suggestions.append("Používajte <button> namiesto <div> s onclick pre interaktívne elementy")
            practices_issues += 1
        
        # Kontrola inline štýlov
        if 'style=' in html_code:
            result.warnings.append("Vyhýbajte sa inline štýlom, používajte CSS triedy")
            practices_issues += 1
        
        # Kontrola JavaScript v HTML
        if any(attr in html_code for attr in ['onclick=', 'onchange=', 'onsubmit=']):
            result.suggestions.append("Vyhýbajte sa inline JavaScript, používajte event listenery")
        
        # Kontrola SEO friendly atribútov
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith('http') and not link.get('rel'):
                result.suggestions.append("Zvážte pridanie rel='noopener' pre externé odkazy")
        
        # Výpočet best practices skóre
        result.best_practices_score = max(0, 100 - (practices_issues * 20))
    
    async def _validate_component_type(self, html_code: str, component_type: str, result: ComponentValidationResult):
        """Validácia špecifická pre typ komponentu"""
        schema = ComponentSchema.get_component_schema(component_type)
        if not schema:
            return
        
        soup = BeautifulSoup(html_code, 'html.parser')
        
        if component_type == "button":
            await self._validate_button_specific(soup, result)
        elif component_type == "form":
            await self._validate_form_specific(soup, result)
        elif component_type == "navbar":
            await self._validate_navbar_specific(soup, result)
        elif component_type == "card":
            await self._validate_card_specific(soup, result)
    
    async def _validate_button_specific(self, soup: BeautifulSoup, result: ComponentValidationResult):
        """Button špecifická validácia"""
        buttons = soup.find_all(['button', 'a'])
        
        for button in buttons:
            # Kontrola type atribútu pre button elementy
            if button.name == 'button' and not button.get('type'):
                result.warnings.append("Button element bez type atribútu")
            
            # Kontrola textového obsahu
            if not button.get_text(strip=True) and not button.find(['img', 'svg', 'i']):
                result.errors.append("Button bez textového obsahu alebo ikony")
            
            # Kontrola disabled stavu
            if button.get('disabled') and 'opacity-50' not in button.get('class', []):
                result.suggestions.append("Pridajte vizuálnu indikáciu pre disabled button (opacity-50)")
    
    async def _validate_form_specific(self, soup: BeautifulSoup, result: ComponentValidationResult):
        """Form špecifická validácia"""
        forms = soup.find_all('form')
        
        for form in forms:
            # Kontrola method atribútu
            method = form.get('method', 'GET').upper()
            if method not in ['GET', 'POST']:
                result.warnings.append(f"Neštandardná HTTP metóda: {method}")
            
            # Kontrola submit tlačidla
            submit_buttons = form.find_all(['button', 'input'], attrs={'type': 'submit'})
            if not submit_buttons:
                result.warnings.append("Formulár bez submit tlačidla")
            
            # Kontrola required polí
            required_inputs = form.find_all(['input', 'select', 'textarea'], attrs={'required': True})
            for input_elem in required_inputs:
                if 'required' not in input_elem.get('class', []):
                    result.suggestions.append("Pridajte vizuálnu indikáciu pre povinné polia")
    
    async def _validate_navbar_specific(self, soup: BeautifulSoup, result: ComponentValidationResult):
        """Navbar špecifická validácia"""
        navs = soup.find_all('nav')
        
        for nav in navs:
            # Kontrola brand elementu
            brand = nav.find(['a', 'span'], class_=lambda x: x and 'brand' in ' '.join(x).lower())
            if not brand:
                result.suggestions.append("Zvážte pridanie brand elementu do navbar")
            
            # Kontrola responzívneho menu
            if 'lg:flex' in str(nav) and not nav.find(attrs={'id': lambda x: x and 'menu' in x}):
                result.suggestions.append("Responzívne menu potrebuje ID pre JavaScript funkcionalitu")
    
    async def _validate_card_specific(self, soup: BeautifulSoup, result: ComponentValidationResult):
        """Card špecifická validácia"""
        cards = soup.find_all(attrs={'class': lambda x: x and 'card' in ' '.join(x).lower()})
        
        for card in cards:
            # Kontrola štruktúry card
            if not card.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                result.suggestions.append("Card by mal obsahovať heading element")
            
            # Kontrola obrázka v card
            img = card.find('img')
            if img and not img.get('alt'):
                result.warnings.append("Obrázok v card bez alt atribútu")
    
    def _check_paired_tags(self, soup: BeautifulSoup, result: ComponentValidationResult):
        """Kontrola párových HTML tagov"""
        # BeautifulSoup automaticky opravuje nepárové tagy, takže kontrolujeme originál
        pass  # Implementácia by vyžadovala regex parsing
    
    def _check_required_attributes(self, soup: BeautifulSoup, result: ComponentValidationResult):
        """Kontrola povinných atribútov"""
        rules = self.accessibility_rules["required_attributes"]
        
        for tag_name, required_attrs in rules.items():
            elements = soup.find_all(tag_name)
            for elem in elements:
                for attr in required_attrs:
                    if not elem.get(attr):
                        result.warnings.append(f"{tag_name} element bez povinného {attr} atribútu")
    
    def _calculate_nesting_depth(self, soup: BeautifulSoup) -> int:
        """Vypočíta maximálnu hĺbku vnorenia"""
        def get_depth(element, current_depth=0):
            if not isinstance(element, Tag):
                return current_depth
            
            max_child_depth = current_depth
            for child in element.children:
                child_depth = get_depth(child, current_depth + 1)
                max_child_depth = max(max_child_depth, child_depth)
            
            return max_child_depth
        
        return max(get_depth(elem) for elem in soup.find_all())
    
    def _calculate_final_score(self, result: ComponentValidationResult):
        """Vypočíta finálne skóre validácie"""
        # Váhy pre rôzne aspekty
        weights = {
            "errors": -30,      # Chyby majú najväčší dopad
            "warnings": -10,    # Upozornenia majú stredný dopad
            "suggestions": -2,  # Návrhy majú malý dopad
            "accessibility": 0.3,
            "performance": 0.3,
            "best_practices": 0.2
        }
        
        # Základ skóre na základe problémov
        error_penalty = len(result.errors) * weights["errors"]
        warning_penalty = len(result.warnings) * weights["warnings"]
        suggestion_penalty = len(result.suggestions) * weights["suggestions"]
        
        base_score = 100 + error_penalty + warning_penalty + suggestion_penalty
        
        # Kombinované skóre z rôznych aspektov
        combined_score = (
            result.accessibility_score * weights["accessibility"] +
            result.performance_score * weights["performance"] +
            result.best_practices_score * weights["best_practices"] +
            base_score * 0.2
        )
        
        result.score = max(0, min(100, combined_score))
        
        # Označenie ako nevalidný ak má kritické chyby
        if result.errors or result.score < 30:
            result.valid = False
    
    async def fix_component(
        self,
        html_code: str,
        auto_fix: bool = True,
        component_type: Optional[str] = None
    ) -> str:
        """
        Automaticky opraví bežné chyby v komponente
        
        Args:
            html_code: Pôvodný HTML kód
            auto_fix: Či automaticky opraviť
            component_type: Typ komponentu
            
        Returns:
            Opravený HTML kód
        """
        try:
            if not auto_fix:
                return html_code
            
            soup = BeautifulSoup(html_code, 'html.parser')
            
            # Oprava základných HTML problémov
            self._fix_basic_html_issues(soup)
            
            # Oprava accessibility problémov
            self._fix_accessibility_issues(soup)
            
            # Oprava performance problémov
            self._fix_performance_issues(soup)
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Chyba pri oprave komponentu: {e}")
            return html_code
    
    def _fix_basic_html_issues(self, soup: BeautifulSoup):
        """Opraví základné HTML problémy"""
        # Pridanie type atribútu pre button elementy
        buttons = soup.find_all('button')
        for button in buttons:
            if not button.get('type'):
                button['type'] = 'button'
    
    def _fix_accessibility_issues(self, soup: BeautifulSoup):
        """Opraví accessibility problémy"""
        # Pridanie alt atribútov pre obrázky
        images = soup.find_all('img')
        for img in images:
            if not img.get('alt'):
                img['alt'] = ''
        
        # Pridanie ID pre input elementy bez ID
        inputs = soup.find_all(['input', 'select', 'textarea'])
        for i, input_elem in enumerate(inputs):
            if not input_elem.get('id') and input_elem.get('type') not in ['hidden', 'submit', 'button']:
                input_elem['id'] = f'input-{i+1}'
    
    def _fix_performance_issues(self, soup: BeautifulSoup):
        """Opraví performance problémy"""
        # Optimalizácia CSS tried (základná implementácia)
        elements = soup.find_all(attrs={'class': True})
        for elem in elements:
            classes = elem['class']
            if isinstance(classes, list):
                # Odstránenie duplicitných tried
                elem['class'] = list(dict.fromkeys(classes))


# Globálna inštancia validátora
validator = FlowbiteValidator()