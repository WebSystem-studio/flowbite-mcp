"""
Validačné schémy pre Flowbite komponenty
"""

from typing import Dict, List, Optional, Any
import json


class ComponentSchema:
    """Schémy pre validáciu komponentov"""
    
    @staticmethod
    def get_button_schema() -> Dict[str, Any]:
        """Schéma pre button komponenty"""
        return {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["button", "submit", "reset"]
                },
                "variant": {
                    "type": "string",
                    "enum": ["primary", "secondary", "success", "warning", "danger", "info", "light", "dark", "outline"]
                },
                "size": {
                    "type": "string",
                    "enum": ["xs", "sm", "md", "lg", "xl"]
                },
                "disabled": {"type": "boolean"},
                "text": {"type": "string", "minLength": 1},
                "icon": {"type": "string"},
                "href": {"type": "string", "format": "uri"}
            },
            "required": ["text"],
            "additionalProperties": False
        }
    
    @staticmethod
    def get_form_schema() -> Dict[str, Any]:
        """Schéma pre form komponenty"""
        return {
            "type": "object",
            "properties": {
                "fields": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string", "enum": ["text", "email", "password", "number", "tel", "url"]},
                            "label": {"type": "string"},
                            "placeholder": {"type": "string"},
                            "required": {"type": "boolean"},
                            "validation": {"type": "object"}
                        },
                        "required": ["name", "type", "label"]
                    }
                },
                "submit_text": {"type": "string"},
                "method": {"type": "string", "enum": ["GET", "POST"]},
                "action": {"type": "string"}
            },
            "required": ["fields"],
            "additionalProperties": False
        }
    
    @staticmethod
    def get_navbar_schema() -> Dict[str, Any]:
        """Schéma pre navbar komponenty"""
        return {
            "type": "object",
            "properties": {
                "brand": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "logo": {"type": "string"},
                        "href": {"type": "string"}
                    }
                },
                "links": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "href": {"type": "string"},
                            "active": {"type": "boolean"}
                        },
                        "required": ["text", "href"]
                    }
                },
                "responsive": {"type": "boolean"},
                "dark_mode": {"type": "boolean"}
            },
            "required": ["brand", "links"],
            "additionalProperties": False
        }
    
    @staticmethod
    def get_card_schema() -> Dict[str, Any]:
        """Schéma pre card komponenty"""
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string"},
                "image": {
                    "type": "object",
                    "properties": {
                        "src": {"type": "string"},
                        "alt": {"type": "string"}
                    }
                },
                "actions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "href": {"type": "string"},
                            "variant": {"type": "string"}
                        }
                    }
                },
                "variant": {"type": "string", "enum": ["default", "bordered", "horizontal"]}
            },
            "required": ["title", "content"],
            "additionalProperties": False
        }
    
    @staticmethod
    def get_modal_schema() -> Dict[str, Any]:
        """Schéma pre modal komponenty"""
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string"},
                "size": {"type": "string", "enum": ["sm", "md", "lg", "xl"]},
                "closable": {"type": "boolean"},
                "backdrop": {"type": "boolean"},
                "actions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "variant": {"type": "string"},
                            "action": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["title", "content"],
            "additionalProperties": False
        }
    
    @staticmethod
    def get_component_schema(component_type: str) -> Optional[Dict[str, Any]]:
        """Vráti schému pre daný typ komponentu"""
        schemas = {
            "button": ComponentSchema.get_button_schema(),
            "form": ComponentSchema.get_form_schema(),
            "navbar": ComponentSchema.get_navbar_schema(),
            "card": ComponentSchema.get_card_schema(),
            "modal": ComponentSchema.get_modal_schema()
        }
        return schemas.get(component_type)


# CSS triedy pre rôzne komponenty
CSS_CLASSES = {
    "button": {
        "base": "font-medium rounded-lg text-sm px-5 py-2.5 focus:outline-none",
        "variants": {
            "primary": "text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800",
            "secondary": "text-gray-900 bg-white border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700",
            "success": "text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800",
            "warning": "text-white bg-yellow-400 hover:bg-yellow-500 focus:ring-4 focus:ring-yellow-300 dark:focus:ring-yellow-900",
            "danger": "text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900"
        },
        "sizes": {
            "xs": "px-3 py-2 text-xs",
            "sm": "px-3 py-2 text-sm",
            "md": "px-5 py-2.5 text-sm",
            "lg": "px-5 py-3 text-base",
            "xl": "px-6 py-3.5 text-base"
        }
    },
    "form": {
        "input": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
        "label": "block mb-2 text-sm font-medium text-gray-900 dark:text-white",
        "error": "mt-2 text-sm text-red-600 dark:text-red-500"
    },
    "navbar": {
        "nav": "bg-white border-gray-200 px-4 lg:px-6 py-2.5 dark:bg-gray-800 dark:border-gray-700",
        "brand": "flex items-center",
        "menu": "hidden justify-between items-center w-full lg:flex lg:w-auto lg:order-1",
        "link": "block py-2 pr-4 pl-3 text-gray-700 border-b border-gray-100 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-primary-700 lg:p-0 dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white lg:dark:hover:bg-transparent dark:border-gray-700"
    },
    "card": {
        "base": "max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700",
        "image": "rounded-t-lg",
        "content": "p-5",
        "title": "mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white",
        "text": "mb-3 font-normal text-gray-700 dark:text-gray-400"
    },
    "modal": {
        "backdrop": "fixed inset-0 z-40 bg-black bg-opacity-50",
        "container": "fixed inset-0 z-50 flex items-center justify-center p-4",
        "content": "relative bg-white rounded-lg shadow dark:bg-gray-700",
        "header": "flex items-start justify-between p-4 border-b rounded-t dark:border-gray-600",
        "body": "p-6 space-y-6",
        "footer": "flex items-center p-6 space-x-2 border-t border-gray-200 rounded-b dark:border-gray-600"
    }
}


# HTML šablóny pre komponenty
HTML_TEMPLATES = {
    "button": {
        "basic": """<button type="{{ type | default('button') }}" 
                    class="{{ classes }}"
                    {% if disabled %}disabled{% endif %}
                    {% if href %}onclick="window.location.href='{{ href }}'"{% endif %}>
                    {% if icon %}<i class="{{ icon }}"></i> {% endif %}{{ text }}
                   </button>""",
        
        "with_link": """<a href="{{ href }}" 
                       class="inline-flex items-center {{ classes }}"
                       {% if target %}target="{{ target }}"{% endif %}>
                       {% if icon %}<i class="{{ icon }}"></i> {% endif %}{{ text }}
                      </a>"""
    },
    
    "form": {
        "basic": """<form class="space-y-6" {% if action %}action="{{ action }}"{% endif %} method="{{ method | default('POST') }}">
                    {% for field in fields %}
                    <div>
                        <label for="{{ field.name }}" class="{{ label_classes }}">{{ field.label }}</label>
                        <input type="{{ field.type }}" 
                               id="{{ field.name }}" 
                               name="{{ field.name }}"
                               class="{{ input_classes }}"
                               {% if field.placeholder %}placeholder="{{ field.placeholder }}"{% endif %}
                               {% if field.required %}required{% endif %}>
                    </div>
                    {% endfor %}
                    <button type="submit" class="{{ submit_classes }}">{{ submit_text | default('Submit') }}</button>
                   </form>"""
    },
    
    "navbar": {
        "basic": """<nav class="{{ nav_classes }}">
                    <div class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
                        <a href="{{ brand.href | default('#') }}" class="{{ brand_classes }}">
                            {% if brand.logo %}<img src="{{ brand.logo }}" class="mr-3 h-6 sm:h-9" alt="{{ brand.text }} Logo">{% endif %}
                            <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">{{ brand.text }}</span>
                        </a>
                        <div class="{{ menu_classes }}" id="mobile-menu-2">
                            <ul class="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-8 lg:mt-0">
                                {% for link in links %}
                                <li>
                                    <a href="{{ link.href }}" 
                                       class="{{ link_classes }} {% if link.active %}text-primary-700{% endif %}"
                                       {% if link.active %}aria-current="page"{% endif %}>{{ link.text }}</a>
                                </li>
                                {% endfor %}
                            </ul>
                        </div>
                    </div>
                   </nav>"""
    },
    
    "card": {
        "basic": """<div class="{{ card_classes }}">
                    {% if image %}
                    <a href="#">
                        <img class="{{ image_classes }}" src="{{ image.src }}" alt="{{ image.alt | default('') }}" />
                    </a>
                    {% endif %}
                    <div class="{{ content_classes }}">
                        <a href="#">
                            <h5 class="{{ title_classes }}">{{ title }}</h5>
                        </a>
                        <p class="{{ text_classes }}">{{ content }}</p>
                        {% if actions %}
                        <div class="flex space-x-2">
                            {% for action in actions %}
                            <a href="{{ action.href }}" class="{{ action.classes }}">{{ action.text }}</a>
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                   </div>"""
    },
    
    "modal": {
        "basic": """<!-- Modal backdrop -->
                   <div id="{{ id }}-backdrop" class="{{ backdrop_classes }}" style="display: none;"></div>
                   <!-- Modal -->
                   <div id="{{ id }}" class="{{ container_classes }}" style="display: none;">
                       <div class="{{ content_classes }} w-full max-w-{{ size | default('md') }}">
                           <!-- Modal header -->
                           <div class="{{ header_classes }}">
                               <h3 class="text-xl font-semibold text-gray-900 dark:text-white">{{ title }}</h3>
                               {% if closable %}
                               <button type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white" onclick="closeModal('{{ id }}')">
                                   <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                       <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                                   </svg>
                               </button>
                               {% endif %}
                           </div>
                           <!-- Modal body -->
                           <div class="{{ body_classes }}">
                               {{ content }}
                           </div>
                           <!-- Modal footer -->
                           {% if actions %}
                           <div class="{{ footer_classes }}">
                               {% for action in actions %}
                               <button type="button" class="{{ action.classes }}" onclick="{{ action.action | default('') }}">{{ action.text }}</button>
                               {% endfor %}
                           </div>
                           {% endif %}
                       </div>
                   </div>"""
    }
}