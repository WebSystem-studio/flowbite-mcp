"""
Generátor Flowbite komponentov
"""

import json
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from jinja2 import Template, Environment, BaseLoader

from ..config import get_config
from ..models.component import (
    FlowbiteComponent,
    ComponentType,
    ComponentVariant,
    ComponentSize,
    ComponentProps
)
from ..models.schema import CSS_CLASSES, HTML_TEMPLATES

# Konfigurácia
config = get_config()
logger = logging.getLogger(__name__)


class TemplateLoader(BaseLoader):
    """Custom template loader pre Jinja2"""
    
    def __init__(self, templates: Dict[str, Any]):
        self.templates = templates
    
    def get_source(self, environment, template):
        if template not in self.templates:
            raise FileNotFoundError(f"Template {template} not found")
        
        source = self.templates[template]
        return source, None, lambda: True


class FlowbiteGenerator:
    """Hlavná trieda pre generovanie Flowbite komponentov"""
    
    def __init__(self):
        self.config = config
        self.template_env = Environment(loader=TemplateLoader(HTML_TEMPLATES))
        self.css_classes = CSS_CLASSES
        self.components_cache: Dict[str, List[FlowbiteComponent]] = {}
        
    async def generate_component(
        self,
        component_type: str,
        props: Dict[str, Any],
        content: Optional[str] = None,
        template_variant: str = "basic"
    ) -> str:
        """
        Univerzálny generátor komponentov
        
        Args:
            component_type: Typ komponentu (button, form, navbar...)
            props: Vlastnosti komponentu
            content: Obsah komponentu
            template_variant: Variant šablóny
            
        Returns:
            Vygenerovaný HTML kód
        """
        try:
            # Validácia typu komponentu
            if not self.config.is_component_supported(component_type):
                raise ValueError(f"Nepodporovaný typ komponentu: {component_type}")
            
            # Načítanie šablóny
            template_key = f"{component_type}.{template_variant}"
            if template_key not in HTML_TEMPLATES.get(component_type, {}):
                template_key = f"{component_type}.basic"
            
            template_content = HTML_TEMPLATES.get(component_type, {}).get(template_variant)
            if not template_content:
                raise ValueError(f"Šablóna {template_key} nenájdená")
            
            # Príprava CSS tried
            css_classes = self._build_css_classes(component_type, props)
            
            # Príprava template variables
            template_vars = {
                **props,
                "classes": css_classes,
                "content": content or props.get("text", ""),
                **self._get_component_specific_vars(component_type, props)
            }
            
            # Renderovanie šablóny
            template = Template(template_content)
            html = template.render(**template_vars)
            
            return html.strip()
            
        except Exception as e:
            logger.error(f"Chyba pri generovaní komponentu {component_type}: {e}")
            raise
    
    def _build_css_classes(self, component_type: str, props: Dict[str, Any]) -> str:
        """Zostavuje CSS triedy pre komponent"""
        if component_type not in self.css_classes:
            return ""
        
        component_css = self.css_classes[component_type]
        classes = []
        
        # Základné triedy
        if "base" in component_css:
            classes.append(component_css["base"])
        
        # Variant specific classes
        variant = props.get("variant", "primary")
        if "variants" in component_css and variant in component_css["variants"]:
            classes.append(component_css["variants"][variant])
        
        # Size specific classes
        size = props.get("size", "md")
        if "sizes" in component_css and size in component_css["sizes"]:
            classes.append(component_css["sizes"][size])
        
        # Outline modifikácia
        if props.get("outline", False) and variant != "outline":
            outline_classes = self._get_outline_classes(variant)
            if outline_classes:
                classes = [cls for cls in classes if not any(
                    exclude in cls for exclude in ["bg-", "text-white"]
                )]
                classes.append(outline_classes)
        
        # Disabled state
        if props.get("disabled", False):
            classes.append("opacity-50 cursor-not-allowed")
        
        # Custom classes
        custom_classes = props.get("custom_classes")
        if custom_classes:
            classes.append(custom_classes)
        
        return " ".join(classes)
    
    def _get_outline_classes(self, variant: str) -> str:
        """Vráti outline CSS triedy pre daný variant"""
        outline_map = {
            "primary": "text-blue-700 border border-blue-700 hover:bg-blue-700 hover:text-white",
            "secondary": "text-gray-700 border border-gray-700 hover:bg-gray-700 hover:text-white",
            "success": "text-green-700 border border-green-700 hover:bg-green-700 hover:text-white",
            "warning": "text-yellow-700 border border-yellow-700 hover:bg-yellow-700 hover:text-white",
            "danger": "text-red-700 border border-red-700 hover:bg-red-700 hover:text-white"
        }
        return outline_map.get(variant, "")
    
    def _get_component_specific_vars(self, component_type: str, props: Dict[str, Any]) -> Dict[str, Any]:
        """Vráti špecifické premenné pre daný typ komponentu"""
        if component_type == "button":
            return self._get_button_vars(props)
        elif component_type == "form":
            return self._get_form_vars(props)
        elif component_type == "navbar":
            return self._get_navbar_vars(props)
        elif component_type == "card":
            return self._get_card_vars(props)
        else:
            return {}
    
    def _get_button_vars(self, props: Dict[str, Any]) -> Dict[str, Any]:
        """Špecifické premenné pre button"""
        return {
            "type": props.get("type", "button"),
            "disabled": props.get("disabled", False),
            "href": props.get("href"),
            "target": props.get("target"),
            "icon": props.get("icon")
        }
    
    def _get_form_vars(self, props: Dict[str, Any]) -> Dict[str, Any]:
        """Špecifické premenné pre form"""
        form_css = self.css_classes.get("form", {})
        
        return {
            "method": props.get("method", "POST"),
            "action": props.get("action"),
            "fields": props.get("fields", []),
            "submit_text": props.get("submit_text", "Submit"),
            "label_classes": form_css.get("label", ""),
            "input_classes": form_css.get("input", ""),
            "submit_classes": self._build_css_classes("button", {
                "variant": "primary",
                "size": "md"
            })
        }
    
    def _get_navbar_vars(self, props: Dict[str, Any]) -> Dict[str, Any]:
        """Špecifické premenné pre navbar"""
        navbar_css = self.css_classes.get("navbar", {})
        
        return {
            "brand": props.get("brand", {}),
            "links": props.get("links", []),
            "responsive": props.get("responsive", True),
            "nav_classes": navbar_css.get("nav", ""),
            "brand_classes": navbar_css.get("brand", ""),
            "menu_classes": navbar_css.get("menu", ""),
            "link_classes": navbar_css.get("link", "")
        }
    
    def _get_card_vars(self, props: Dict[str, Any]) -> Dict[str, Any]:
        """Špecifické premenné pre card"""
        card_css = self.css_classes.get("card", {})
        
        return {
            "title": props.get("title", ""),
            "content": props.get("content", ""),
            "image": props.get("image"),
            "actions": props.get("actions", []),
            "card_classes": card_css.get("base", ""),
            "image_classes": card_css.get("image", ""),
            "content_classes": card_css.get("content", ""),
            "title_classes": card_css.get("title", ""),
            "text_classes": card_css.get("text", "")
        }
    
    async def generate_button(
        self,
        text: str = "Button",
        variant: str = "primary",
        size: str = "md",
        disabled: bool = False,
        icon: Optional[str] = None,
        href: Optional[str] = None,
        outline: bool = False,
        **kwargs
    ) -> str:
        """Generuje Flowbite button komponent"""
        props = {
            "text": text,
            "variant": variant,
            "size": size,
            "disabled": disabled,
            "icon": icon,
            "href": href,
            "outline": outline,
            **kwargs
        }
        
        template_variant = "with_link" if href else "basic"
        return await self.generate_component("button", props, text, template_variant)
    
    async def generate_form(
        self,
        fields: List[Dict[str, Any]],
        submit_text: str = "Submit",
        method: str = "POST",
        action: Optional[str] = None,
        validation: bool = True,
        dark_mode: bool = False,
        **kwargs
    ) -> str:
        """Generuje Flowbite form komponent"""
        props = {
            "fields": fields,
            "submit_text": submit_text,
            "method": method,
            "action": action,
            "validation": validation,
            "dark_mode": dark_mode,
            **kwargs
        }
        
        return await self.generate_component("form", props, None, "basic")
    
    async def generate_navbar(
        self,
        brand: Union[str, Dict[str, str]],
        links: List[Dict[str, str]],
        style: str = "default",
        responsive: bool = True,
        dark_mode: bool = False,
        **kwargs
    ) -> str:
        """Generuje Flowbite navbar komponent"""
        # Normalizácia brand parametra
        if isinstance(brand, str):
            brand = {"text": brand, "href": "#"}
        
        props = {
            "brand": brand,
            "links": links,
            "style": style,
            "responsive": responsive,
            "dark_mode": dark_mode,
            **kwargs
        }
        
        return await self.generate_component("navbar", props, None, "basic")
    
    async def generate_card(
        self,
        title: str,
        content: str,
        image_url: Optional[str] = None,
        actions: List[Dict[str, str]] = None,
        variant: str = "default",
        **kwargs
    ) -> str:
        """Generuje Flowbite card komponent"""
        if actions is None:
            actions = []
        
        image = None
        if image_url:
            image = {"src": image_url, "alt": title}
        
        props = {
            "title": title,
            "content": content,
            "image": image,
            "actions": actions,
            "variant": variant,
            **kwargs
        }
        
        return await self.generate_component("card", props, None, "basic")
    
    async def generate_modal(
        self,
        title: str,
        content: str,
        size: str = "md",
        closable: bool = True,
        actions: List[Dict[str, str]] = None,
        **kwargs
    ) -> str:
        """Generuje Flowbite modal komponent"""
        if actions is None:
            actions = []
        
        # Generovanie unikátneho ID
        modal_id = kwargs.get("id", f"modal-{hash(title) % 10000}")
        
        props = {
            "id": modal_id,
            "title": title,
            "content": content,
            "size": size,
            "closable": closable,
            "actions": actions,
            **kwargs
        }
        
        return await self.generate_component("modal", props, None, "basic")
    
    async def get_component_variations(self, component_type: str) -> List[Dict[str, Any]]:
        """Vráti dostupné variácie pre daný typ komponentu"""
        try:
            component_path = self.config.get_component_path(component_type)
            if not component_path.exists():
                return []
            
            with open(component_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                components = data.get(component_type, [])
                
                variations = []
                for comp in components:
                    variations.append({
                        "id": comp.get("id"),
                        "name": comp.get("name"),
                        "description": comp.get("description"),
                        "props": comp.get("props", {})
                    })
                
                return variations
                
        except Exception as e:
            logger.error(f"Chyba pri načítavaní variácií pre {component_type}: {e}")
            return []


# Globálna inštancia generátora
generator = FlowbiteGenerator()