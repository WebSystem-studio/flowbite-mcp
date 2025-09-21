#!/usr/bin/env python3
"""
Flowbite MCP Server - Simplified version pre Cline testing
Funguje bez external dependencies (FastMCP, Pydantic, atď.)
"""

import json
import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional

class SimpleMCPServer:
    """Simplified MCP server implementation"""
    
    def __init__(self):
        self.tools = {
            "generate_component": {
                "name": "generate_component",
                "description": "Generate Flowbite component HTML",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "component_type": {"type": "string", "description": "Type of component (button, form, card, etc.)"},
                        "variant": {"type": "string", "description": "Component variant (primary, secondary, etc.)"},
                        "props": {"type": "object", "description": "Component properties"}
                    },
                    "required": ["component_type"]
                }
            },
            "validate_component": {
                "name": "validate_component", 
                "description": "Validate Flowbite component HTML",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "html": {"type": "string", "description": "HTML code to validate"},
                        "component_type": {"type": "string", "description": "Expected component type"}
                    },
                    "required": ["html"]
                }
            },
            "suggest_components": {
                "name": "suggest_components",
                "description": "Suggest appropriate Flowbite components",
                "inputSchema": {
                    "type": "object", 
                    "properties": {
                        "description": {"type": "string", "description": "Description of what you need"},
                        "context": {"type": "string", "description": "Context (e-shop, dashboard, landing, etc.)"}
                    },
                    "required": ["description"]
                }
            }
        }
        
        self.components_db = {
            "button": {
                "variants": {
                    "primary": {
                        "html": '<button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">{{text}}</button>',
                        "css_classes": ["text-white", "bg-blue-700", "hover:bg-blue-800", "focus:ring-4", "focus:ring-blue-300", "font-medium", "rounded-lg", "text-sm", "px-5", "py-2.5", "mr-2", "mb-2"]
                    },
                    "secondary": {
                        "html": '<button type="button" class="py-2.5 px-5 mr-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">{{text}}</button>',
                        "css_classes": ["py-2.5", "px-5", "mr-2", "mb-2", "text-sm", "font-medium", "text-gray-900", "focus:outline-none", "bg-white", "rounded-lg", "border", "border-gray-200"]
                    },
                    "danger": {
                        "html": '<button type="button" class="text-white bg-red-700 hover:bg-red-800 focus:outline-none focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900">{{text}}</button>',
                        "css_classes": ["text-white", "bg-red-700", "hover:bg-red-800", "focus:outline-none", "focus:ring-4", "focus:ring-red-300", "font-medium", "rounded-lg", "text-sm", "px-5", "py-2.5"]
                    }
                }
            },
            "form": {
                "variants": {
                    "contact": {
                        "html": '<form class="max-w-md mx-auto"><div class="mb-5"><label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your email</label><input type="email" id="email" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="name@flowbite.com" required /></div><div class="mb-5"><label for="message" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your message</label><textarea id="message" rows="4" class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Leave a comment..."></textarea></div><button type="submit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button></form>',
                        "css_classes": ["max-w-md", "mx-auto", "mb-5", "block", "mb-2", "text-sm", "font-medium", "text-gray-900", "bg-gray-50", "border", "border-gray-300", "rounded-lg"]
                    }
                }
            },
            "card": {
                "variants": {
                    "basic": {
                        "html": '<div class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"><a href="#"><h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{{title}}</h5></a><p class="mb-3 font-normal text-gray-700 dark:text-gray-400">{{content}}</p><a href="#" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Read more<svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/></svg></a></div>',
                        "css_classes": ["max-w-sm", "p-6", "bg-white", "border", "border-gray-200", "rounded-lg", "shadow", "dark:bg-gray-800", "dark:border-gray-700"]
                    }
                }
            },
            "input": {
                "variants": {
                    "text": {
                        "html": '<div class="mb-5"><label for="{{id}}" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{label}}</label><input type="text" id="{{id}}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="{{placeholder}}" {{required}} /></div>',
                        "css_classes": ["mb-5", "block", "mb-2", "text-sm", "font-medium", "text-gray-900", "bg-gray-50", "border", "border-gray-300", "rounded-lg", "focus:ring-blue-500", "focus:border-blue-500", "w-full", "p-2.5"]
                    },
                    "email": {
                        "html": '<div class="mb-5"><label for="{{id}}" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{label}}</label><input type="email" id="{{id}}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="{{placeholder}}" {{required}} /></div>',
                        "css_classes": ["mb-5", "block", "mb-2", "text-sm", "font-medium", "text-gray-900", "bg-gray-50", "border", "border-gray-300", "rounded-lg", "focus:ring-blue-500", "focus:border-blue-500", "w-full", "p-2.5"]
                    },
                    "password": {
                        "html": '<div class="mb-5"><label for="{{id}}" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{label}}</label><input type="password" id="{{id}}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="{{placeholder}}" {{required}} /></div>',
                        "css_classes": ["mb-5", "block", "mb-2", "text-sm", "font-medium", "text-gray-900", "bg-gray-50", "border", "border-gray-300", "rounded-lg", "focus:ring-blue-500", "focus:border-blue-500", "w-full", "p-2.5"]
                    },
                    "search": {
                        "html": '<div class="mb-5"><label for="{{id}}" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{label}}</label><div class="relative"><div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none"><svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/></svg></div><input type="search" id="{{id}}" class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="{{placeholder}}" {{required}} /></div></div>',
                        "css_classes": ["mb-5", "relative", "w-4", "h-4", "text-gray-500", "ps-3", "pointer-events-none", "block", "w-full", "p-4", "ps-10", "text-sm", "text-gray-900", "border", "border-gray-300", "rounded-lg", "bg-gray-50"]
                    },
                    "number": {
                        "html": '<div class="mb-5"><label for="{{id}}" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{label}}</label><input type="number" id="{{id}}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="{{placeholder}}" {{required}} {{min}} {{max}} {{step}} /></div>',
                        "css_classes": ["mb-5", "block", "mb-2", "text-sm", "font-medium", "text-gray-900", "bg-gray-50", "border", "border-gray-300", "rounded-lg", "focus:ring-blue-500", "focus:border-blue-500", "w-full", "p-2.5"]
                    },
                    "tel": {
                        "html": '<div class="mb-5"><label for="{{id}}" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{label}}</label><input type="tel" id="{{id}}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="{{placeholder}}" {{required}} /></div>',
                        "css_classes": ["mb-5", "block", "mb-2", "text-sm", "font-medium", "text-gray-900", "bg-gray-50", "border", "border-gray-300", "rounded-lg", "focus:ring-blue-500", "focus:border-blue-500", "w-full", "p-2.5"]
                    },
                    "url": {
                        "html": '<div class="mb-5"><label for="{{id}}" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{label}}</label><input type="url" id="{{id}}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="{{placeholder}}" {{required}} /></div>',
                        "css_classes": ["mb-5", "block", "mb-2", "text-sm", "font-medium", "text-gray-900", "bg-gray-50", "border", "border-gray-300", "rounded-lg", "focus:ring-blue-500", "focus:border-blue-500", "w-full", "p-2.5"]
                    }
                }
            },
            "textarea": {
                "variants": {
                    "basic": {
                        "html": '<div class="mb-5"><label for="{{id}}" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{label}}</label><textarea id="{{id}}" rows="{{rows}}" class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="{{placeholder}}" {{required}}></textarea></div>',
                        "css_classes": ["mb-5", "block", "mb-2", "text-sm", "font-medium", "text-gray-900", "p-2.5", "w-full", "bg-gray-50", "rounded-lg", "border", "border-gray-300", "focus:ring-blue-500", "focus:border-blue-500"]
                    },
                    "resizable": {
                        "html": '<div class="mb-5"><label for="{{id}}" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{label}}</label><textarea id="{{id}}" rows="{{rows}}" class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 resize-y" placeholder="{{placeholder}}" {{required}}></textarea></div>',
                        "css_classes": ["mb-5", "block", "mb-2", "text-sm", "font-medium", "text-gray-900", "p-2.5", "w-full", "bg-gray-50", "rounded-lg", "border", "border-gray-300", "focus:ring-blue-500", "focus:border-blue-500", "resize-y"]
                    }
                }
            },
            "alert": {
                "variants": {
                    "info": {
                        "html": '<div class="flex items-center p-4 mb-4 text-sm text-blue-800 rounded-lg bg-blue-50 dark:bg-gray-800 dark:text-blue-400" role="alert"><svg class="flex-shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/></svg><span class="sr-only">Info</span><div><span class="font-medium">{{title}}</span> {{message}}</div></div>',
                        "css_classes": ["flex", "items-center", "p-4", "mb-4", "text-sm", "text-blue-800", "rounded-lg", "bg-blue-50", "dark:bg-gray-800", "dark:text-blue-400"]
                    },
                    "success": {
                        "html": '<div class="flex items-center p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400" role="alert"><svg class="flex-shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/></svg><span class="sr-only">Success</span><div><span class="font-medium">{{title}}</span> {{message}}</div></div>',
                        "css_classes": ["flex", "items-center", "p-4", "mb-4", "text-sm", "text-green-800", "rounded-lg", "bg-green-50", "dark:bg-gray-800", "dark:text-green-400"]
                    },
                    "warning": {
                        "html": '<div class="flex items-center p-4 mb-4 text-sm text-yellow-800 rounded-lg bg-yellow-50 dark:bg-gray-800 dark:text-yellow-300" role="alert"><svg class="flex-shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm0-4a1 1 0 0 1-1-1V6a1 1 0 0 1 2 0v4a1 1 0 0 1-1 1Z"/></svg><span class="sr-only">Warning</span><div><span class="font-medium">{{title}}</span> {{message}}</div></div>',
                        "css_classes": ["flex", "items-center", "p-4", "mb-4", "text-sm", "text-yellow-800", "rounded-lg", "bg-yellow-50", "dark:bg-gray-800", "dark:text-yellow-300"]
                    },
                    "error": {
                        "html": '<div class="flex items-center p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert"><svg class="flex-shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/></svg><span class="sr-only">Error</span><div><span class="font-medium">{{title}}</span> {{message}}</div></div>',
                        "css_classes": ["flex", "items-center", "p-4", "mb-4", "text-sm", "text-red-800", "rounded-lg", "bg-red-50", "dark:bg-gray-800", "dark:text-red-400"]
                    },
                    "dismissible": {
                        "html": '<div class="flex items-center p-4 mb-4 text-sm text-blue-800 rounded-lg bg-blue-50 dark:bg-gray-800 dark:text-blue-400" role="alert"><svg class="flex-shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/></svg><span class="sr-only">Info</span><div><span class="font-medium">{{title}}</span> {{message}}</div><button type="button" class="ms-auto -mx-1.5 -my-1.5 bg-blue-50 text-blue-500 rounded-lg focus:ring-2 focus:ring-blue-400 p-1.5 hover:bg-blue-200 inline-flex items-center justify-center h-8 w-8 dark:bg-gray-800 dark:text-blue-400 dark:hover:bg-gray-700" data-dismiss-target="#alert-1" aria-label="Close"><span class="sr-only">Close</span><svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/></svg></button></div>',
                        "css_classes": ["flex", "items-center", "p-4", "mb-4", "text-sm", "text-blue-800", "rounded-lg", "bg-blue-50", "ms-auto", "-mx-1.5", "-my-1.5", "focus:ring-2", "focus:ring-blue-400", "p-1.5", "hover:bg-blue-200", "inline-flex", "justify-center", "h-8", "w-8"]
                    }
                }
            },
            "navbar": {
                "variants": {
                    "basic": {
                        "html": '<nav class="bg-white border-gray-200 dark:bg-gray-900"><div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4"><a href="#" class="flex items-center space-x-3 rtl:space-x-reverse"><span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">{{brand}}</span></a><button data-collapse-toggle="navbar-default" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-default" aria-expanded="false"><span class="sr-only">Open main menu</span><svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/></svg></button><div class="hidden w-full md:block md:w-auto" id="navbar-default"><ul class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700"><li><a href="#" class="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500" aria-current="page">{{nav_items}}</a></li></ul></div></div></nav>',
                        "css_classes": ["bg-white", "border-gray-200", "dark:bg-gray-900", "max-w-screen-xl", "flex", "flex-wrap", "items-center", "justify-between", "mx-auto", "p-4", "text-2xl", "font-semibold", "whitespace-nowrap"]
                    },
                    "with-dropdown": {
                        "html": '<nav class="bg-white border-gray-200 dark:bg-gray-900"><div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4"><a href="#" class="flex items-center space-x-3 rtl:space-x-reverse"><span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">{{brand}}</span></a><button data-collapse-toggle="navbar-dropdown" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"><span class="sr-only">Open main menu</span><svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/></svg></button><div class="hidden w-full md:block md:w-auto" id="navbar-dropdown"><ul class="flex flex-col font-medium p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700"><li><button id="dropdownNavbarLink" data-dropdown-toggle="dropdownNavbar" class="flex items-center justify-between w-full py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 md:w-auto dark:text-white md:dark:hover:text-blue-500 dark:focus:text-white dark:border-gray-700 dark:hover:bg-gray-700 md:dark:hover:bg-transparent">{{dropdown_title}} <svg class="w-2.5 h-2.5 ms-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/></svg></button><div id="dropdownNavbar" class="z-10 hidden font-normal bg-white divide-y divide-gray-100 rounded-lg shadow w-44 dark:bg-gray-700 dark:divide-gray-600"><ul class="py-2 text-sm text-gray-700 dark:text-gray-400"><li><a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">{{dropdown_items}}</a></li></ul></div></li></ul></div></div></nav>',
                        "css_classes": ["bg-white", "border-gray-200", "dark:bg-gray-900", "max-w-screen-xl", "flex", "flex-wrap", "items-center", "justify-between", "mx-auto", "p-4", "text-2xl", "font-semibold", "hidden", "w-full", "md:block", "md:w-auto"]
                    },
                    "dark": {
                        "html": '<nav class="bg-gray-900 border-gray-700"><div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4"><a href="#" class="flex items-center space-x-3 rtl:space-x-reverse"><span class="self-center text-2xl font-semibold whitespace-nowrap text-white">{{brand}}</span></a><button data-collapse-toggle="navbar-default" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-400 rounded-lg md:hidden hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-600"><span class="sr-only">Open main menu</span><svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/></svg></button><div class="hidden w-full md:block md:w-auto" id="navbar-default"><ul class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-700 rounded-lg bg-gray-800 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-gray-900"><li><a href="#" class="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-500 md:p-0" aria-current="page">{{nav_items}}</a></li></ul></div></div></nav>',
                        "css_classes": ["bg-gray-900", "border-gray-700", "max-w-screen-xl", "flex", "flex-wrap", "items-center", "justify-between", "mx-auto", "p-4", "text-2xl", "font-semibold", "whitespace-nowrap", "text-white"]
                    },
                    "fixed": {
                        "html": '<nav class="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600"><div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4"><a href="#" class="flex items-center space-x-3 rtl:space-x-reverse"><span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">{{brand}}</span></a><div class="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse"><button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">{{cta_text}}</button><button data-collapse-toggle="navbar-sticky" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"><span class="sr-only">Open main menu</span><svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/></svg></button></div><div class="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-sticky"><ul class="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700"><li><a href="#" class="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500" aria-current="page">{{nav_items}}</a></li></ul></div></div></nav>',
                        "css_classes": ["bg-white", "dark:bg-gray-900", "fixed", "w-full", "z-20", "top-0", "start-0", "border-b", "border-gray-200", "dark:border-gray-600", "max-w-screen-xl", "flex", "flex-wrap", "items-center", "justify-between", "mx-auto", "p-4"]
                    }
                }
            },
            "modal": {
                "variants": {
                    "basic": {
                        "html": '<div id="{{id}}" tabindex="-1" aria-hidden="true" class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"><div class="relative p-4 w-full max-w-2xl max-h-full"><div class="relative bg-white rounded-lg shadow dark:bg-gray-700"><div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600"><h3 class="text-xl font-semibold text-gray-900 dark:text-white">{{title}}</h3><button type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="{{id}}"><svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/></svg><span class="sr-only">Close modal</span></button></div><div class="p-4 md:p-5 space-y-4"><p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">{{content}}</p></div><div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600"><button data-modal-hide="{{id}}" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">{{primary_button}}</button><button data-modal-hide="{{id}}" type="button" class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">{{secondary_button}}</button></div></div></div></div>',
                        "css_classes": ["hidden", "overflow-y-auto", "overflow-x-hidden", "fixed", "top-0", "right-0", "left-0", "z-50", "justify-center", "items-center", "w-full", "md:inset-0", "h-[calc(100%-1rem)]", "max-h-full", "relative", "p-4", "max-w-2xl", "bg-white", "rounded-lg", "shadow", "dark:bg-gray-700"]
                    },
                    "confirmation": {
                        "html": '<div id="{{id}}" tabindex="-1" class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"><div class="relative p-4 w-full max-w-md max-h-full"><div class="relative bg-white rounded-lg shadow dark:bg-gray-700"><button type="button" class="absolute top-3 end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="{{id}}"><svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/></svg><span class="sr-only">Close modal</span></button><div class="p-6 text-center"><svg class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/></svg><h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">{{message}}</h3><button data-modal-hide="{{id}}" type="button" class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center">{{confirm_button}}</button><button data-modal-hide="{{id}}" type="button" class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">{{cancel_button}}</button></div></div></div></div>',
                        "css_classes": ["hidden", "overflow-y-auto", "overflow-x-hidden", "fixed", "top-0", "right-0", "left-0", "z-50", "justify-center", "items-center", "w-full", "md:inset-0", "relative", "p-4", "max-w-md", "max-h-full", "bg-white", "rounded-lg", "shadow", "dark:bg-gray-700", "text-center"]
                    },
                    "form": {
                        "html": '<div id="{{id}}" tabindex="-1" aria-hidden="true" class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"><div class="relative p-4 w-full max-w-md max-h-full"><div class="relative bg-white rounded-lg shadow dark:bg-gray-700"><div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600"><h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{title}}</h3><button type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="{{id}}"><svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/></svg><span class="sr-only">Close modal</span></button></div><form class="p-4 md:p-5"><div class="grid gap-4 mb-4 grid-cols-2"><div class="col-span-2"><label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{{form_fields}}</label><input type="text" name="name" id="name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Type here" required=""></div></div><button type="submit" class="text-white inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"><svg class="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"></path></svg>{{submit_button}}</button></form></div></div></div>',
                        "css_classes": ["hidden", "overflow-y-auto", "overflow-x-hidden", "fixed", "top-0", "right-0", "left-0", "z-50", "justify-center", "items-center", "w-full", "md:inset-0", "relative", "p-4", "max-w-md", "max-h-full", "bg-white", "rounded-lg", "shadow", "dark:bg-gray-700"]
                    },
                    "timeline": {
                        "html": '<div id="{{id}}" tabindex="-1" aria-hidden="true" class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"><div class="relative p-4 w-full max-w-4xl max-h-full"><div class="relative bg-white rounded-lg shadow dark:bg-gray-700"><div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600"><h3 class="text-xl font-semibold text-gray-900 dark:text-white">{{title}}</h3><button type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="{{id}}"><svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/></svg><span class="sr-only">Close modal</span></button></div><div class="p-4 md:p-5"><ol class="relative border-s border-gray-200 dark:border-gray-700"><li class="mb-10 ms-6"><span class="absolute flex items-center justify-center w-6 h-6 bg-blue-100 rounded-full -start-3 ring-8 ring-white dark:ring-gray-900 dark:bg-blue-900"><svg class="w-2.5 h-2.5 text-blue-800 dark:text-blue-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M20 4a2 2 0 0 0-2-2h-2V1a1 1 0 0 0-2 0v1h-3V1a1 1 0 0 0-2 0v1H6V1a1 1 0 0 0-2 0v1H2a2 2 0 0 0-2 2v2h20V4ZM0 18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8H0v10Zm5-8h10a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Z"/></svg></span><h3 class="flex items-center mb-1 text-lg font-semibold text-gray-900 dark:text-white">{{timeline_item}}</h3><time class="block mb-2 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">{{timeline_date}}</time><p class="mb-4 text-base font-normal text-gray-500 dark:text-gray-400">{{timeline_description}}</p></li></ol></div><div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600"><button data-modal-hide="{{id}}" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Close</button></div></div></div></div>',
                        "css_classes": ["hidden", "overflow-y-auto", "overflow-x-hidden", "fixed", "top-0", "right-0", "left-0", "z-50", "justify-center", "items-center", "w-full", "md:inset-0", "relative", "p-4", "max-w-4xl", "max-h-full", "bg-white", "rounded-lg", "shadow", "dark:bg-gray-700", "border-s", "border-gray-200", "dark:border-gray-700"]
                    }
                }
            }
        }

    async def handle_rpc_call(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP RPC calls"""
        
        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": "flowbite-mcp-server",
                    "version": "1.0.0"
                }
            }
            
        elif method == "tools/list":
            return {"tools": list(self.tools.values())}
            
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "generate_component":
                return await self.generate_component(**arguments)
            elif tool_name == "validate_component":
                return await self.validate_component(**arguments)
            elif tool_name == "suggest_components":
                return await self.suggest_components(**arguments)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
                
        else:
            return {"error": f"Unknown method: {method}"}

    async def generate_component(self, component_type: str, variant: str = None, props: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate component HTML"""
        props = props or {}
        
        if component_type not in self.components_db:
            available_types = list(self.components_db.keys())
            return {"error": f"Unknown component type: {component_type}. Available: {available_types}"}
            
        component_variants = self.components_db[component_type]["variants"]
        
        # Auto-select default variant if not specified
        if variant is None:
            if component_type == "button":
                variant = "primary"
            elif component_type == "input":
                variant = "text"
            elif component_type == "textarea":
                variant = "basic"
            elif component_type == "alert":
                variant = "info"
            elif component_type == "navbar":
                variant = "basic"
            elif component_type == "modal":
                variant = "basic"
            else:
                variant = list(component_variants.keys())[0]
        
        if variant not in component_variants:
            available = list(component_variants.keys())
            return {"error": f"Unknown variant '{variant}' for {component_type}. Available: {available}"}
            
        template_data = component_variants[variant]
        html_template = template_data["html"]
        
        # Enhanced template replacement system
        replacements = self._get_template_replacements(component_type, variant, props)
        
        html = html_template
        for placeholder, value in replacements.items():
            html = html.replace(f"{{{{{placeholder}}}}}", str(value))
        
        # Component-specific information
        component_info = self._get_component_info(component_type, variant, props)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Generated **{component_type}** component ({variant} variant):\n\n```html\n{html}\n```\n\n{component_info}\n\nCSS Classes: {', '.join(template_data['css_classes'][:8])}..."
                }
            ]
        }
    
    def _get_template_replacements(self, component_type: str, variant: str, props: Dict[str, Any]) -> Dict[str, str]:
        """Get template placeholder replacements based on component type"""
        
        # Common replacements
        replacements = {
            "text": props.get("text", "Click Me"),
            "title": props.get("title", "Default Title"),
            "content": props.get("content", "Default content description."),
            "message": props.get("message", "This is a default message."),
        }
        
        # Input-specific replacements
        if component_type in ["input", "textarea"]:
            replacements.update({
                "id": props.get("id", f"{component_type}_{variant}"),
                "label": props.get("label", f"{variant.title()} Input"),
                "placeholder": props.get("placeholder", f"Enter your {variant}..."),
                "required": "required" if props.get("required", False) else "",
                "rows": props.get("rows", "4"),
                "min": f'min="{props["min"]}"' if "min" in props else "",
                "max": f'max="{props["max"]}"' if "max" in props else "",
                "step": f'step="{props["step"]}"' if "step" in props else "",
            })
        
        # Alert-specific replacements
        elif component_type == "alert":
            replacements.update({
                "title": props.get("title", f"{variant.title()}!"),
                "message": props.get("message", f"This is a {variant} alert message."),
            })
            
        # Navbar-specific replacements
        elif component_type == "navbar":
            nav_items = props.get("nav_items", "Home")
            if isinstance(nav_items, list):
                nav_items = "</a></li><li><a href='#' class='block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:text-white dark:border-gray-700 dark:hover:bg-gray-700 md:dark:hover:bg-transparent'>".join(nav_items)
            
            dropdown_items = props.get("dropdown_items", "Item 1")
            if isinstance(dropdown_items, list):
                dropdown_items = "</a></li><li><a href='#' class='block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white'>".join(dropdown_items)
            
            replacements.update({
                "brand": props.get("brand", "Flowbite"),
                "nav_items": nav_items,
                "dropdown_title": props.get("dropdown_title", "Services"),
                "dropdown_items": dropdown_items,
                "cta_text": props.get("cta_text", "Get started"),
            })
            
        # Modal-specific replacements
        elif component_type == "modal":
            replacements.update({
                "id": props.get("id", f"modal-{variant}"),
                "title": props.get("title", f"{variant.title()} Modal"),
                "content": props.get("content", "This is the modal content area."),
                "primary_button": props.get("primary_button", "Confirm"),
                "secondary_button": props.get("secondary_button", "Cancel"),
                "confirm_button": props.get("confirm_button", "Yes, I'm sure"),
                "cancel_button": props.get("cancel_button", "No, cancel"),
                "submit_button": props.get("submit_button", "Add new item"),
                "form_fields": props.get("form_fields", "Name"),
                "timeline_item": props.get("timeline_item", "Project Milestone"),
                "timeline_date": props.get("timeline_date", "February 2022"),
                "timeline_description": props.get("timeline_description", "Important project milestone achieved."),
            })
            
        return replacements
    
    def _get_component_info(self, component_type: str, variant: str, props: Dict[str, Any]) -> str:
        """Get additional component information"""
        
        info_map = {
            "input": {
                "text": "📝 Text input field for general text entry",
                "email": "📧 Email input with built-in validation",
                "password": "🔒 Password input with hidden text",
                "search": "🔍 Search input with search icon",
                "number": "🔢 Number input with validation",
                "tel": "📞 Telephone number input",
                "url": "🌐 URL input with validation"
            },
            "textarea": {
                "basic": "📄 Multi-line text input for longer content",
                "resizable": "📏 Resizable textarea for flexible content"
            },
            "alert": {
                "info": "ℹ️ Information alert for general notifications",
                "success": "✅ Success alert for positive feedback",
                "warning": "⚠️ Warning alert for cautionary messages",
                "error": "❌ Error alert for error messages",
                "dismissible": "❌ Dismissible alert with close button"
            },
            "button": {
                "primary": "🔵 Primary action button",
                "secondary": "⚪ Secondary action button", 
                "danger": "🔴 Destructive action button"
            },
            "card": {
                "basic": "🃏 Basic content card with title and description"
            },
            "form": {
                "contact": "📬 Contact form with email and message"
            },
            "navbar": {
                "basic": "🧭 Basic navigation bar with responsive design",
                "with-dropdown": "📋 Navigation bar with dropdown menu",
                "dark": "🌙 Dark theme navigation bar",
                "fixed": "📌 Fixed navigation bar with CTA button"
            },
            "modal": {
                "basic": "💬 Basic modal dialog with header, content, and buttons",
                "confirmation": "❓ Confirmation modal for user decisions",
                "form": "📝 Form modal for data entry",
                "timeline": "📅 Timeline modal for displaying chronological events"
            }
        }
        
        return info_map.get(component_type, {}).get(variant, f"📦 {component_type} component")

    async def validate_component(self, html: str, component_type: str = None) -> Dict[str, Any]:
        """Validate component HTML"""
        errors = []
        warnings = []
        suggestions = []
        
        # Basic validation
        if not html.strip():
            errors.append("HTML cannot be empty")
            
        if not html.strip().startswith('<'):
            errors.append("HTML must start with a valid tag")
            
        # Check for required elements based on component type
        if component_type:
            if component_type == "button" and "<button" not in html.lower():
                errors.append("Button component must contain <button> tag")
            elif component_type == "form" and "<form" not in html.lower():
                errors.append("Form component must contain <form> tag")
                
        # Check for Tailwind classes
        if "class=" not in html:
            warnings.append("No CSS classes found - consider adding Tailwind classes")
        elif "bg-" not in html:
            suggestions.append("Consider adding background color classes (bg-blue-500, bg-gray-100, etc.)")
            
        # Calculate score
        score = 100
        score -= len(errors) * 25
        score -= len(warnings) * 10
        score = max(0, score)
        
        status = "valid" if len(errors) == 0 else "invalid"
        
        return {
            "content": [
                {
                    "type": "text", 
                    "text": f"Validation Result: {status.upper()}\n\nScore: {score}/100\n\n" +
                           (f"❌ Errors ({len(errors)}):\n" + "\n".join(f"  • {e}" for e in errors) + "\n\n" if errors else "") +
                           (f"⚠️ Warnings ({len(warnings)}):\n" + "\n".join(f"  • {w}" for w in warnings) + "\n\n" if warnings else "") +
                           (f"💡 Suggestions ({len(suggestions)}):\n" + "\n".join(f"  • {s}" for s in suggestions) if suggestions else "")
                }
            ]
        }

    async def suggest_components(self, description: str, context: str = "general") -> Dict[str, Any]:
        """Suggest appropriate components"""
        
        # Simple keyword matching
        desc_lower = description.lower()
        suggestions = []
        
        # Input/Form suggestions (High priority)
        if any(word in desc_lower for word in ["input", "field", "enter", "type", "fill"]):
            suggestions.append({
                "component": "input",
                "variants": ["text", "email", "password", "search", "number"],
                "reason": "Keywords suggest user input collection",
                "example": "Text input for user data entry"
            })
            
        if any(word in desc_lower for word in ["textarea", "message", "comment", "description", "multi-line"]):
            suggestions.append({
                "component": "textarea", 
                "variants": ["basic", "resizable"],
                "reason": "Keywords suggest multi-line text input",
                "example": "Textarea for longer text content"
            })
        
        # Alert/Notification suggestions
        if any(word in desc_lower for word in ["alert", "notification", "message", "warning", "error", "success", "info"]):
            suggestions.append({
                "component": "alert",
                "variants": ["info", "success", "warning", "error", "dismissible"],
                "reason": "Keywords suggest user feedback messages",
                "example": "Alert for user notifications and feedback"
            })
        
        # Navigation suggestions
        if any(word in desc_lower for word in ["navbar", "navigation", "menu", "nav", "header", "top"]):
            suggestions.append({
                "component": "navbar",
                "variants": ["basic", "with-dropdown", "dark", "fixed"],
                "reason": "Keywords suggest navigation component",
                "example": "Navigation bar for site navigation and branding"
            })
        
        # Button suggestions
        if any(word in desc_lower for word in ["button", "click", "submit", "action", "cta"]):
            suggestions.append({
                "component": "button",
                "variants": ["primary", "secondary", "danger"],
                "reason": "Keywords suggest interactive element",
                "example": "Primary button for main actions, secondary for alternatives"
            })
            
        # Form suggestions  
        if any(word in desc_lower for word in ["form", "contact", "register", "login", "submit"]):
            suggestions.append({
                "component": "form",
                "variants": ["contact"],
                "reason": "Keywords suggest user input collection",
                "example": "Contact form for user inquiries"
            })
            
        # Card suggestions
        if any(word in desc_lower for word in ["card", "content", "article", "product", "display", "show"]):
            suggestions.append({
                "component": "card",
                "variants": ["basic"],
                "reason": "Keywords suggest content presentation", 
                "example": "Basic card for displaying content with title and description"
            })
            
        # Modal suggestions
        if any(word in desc_lower for word in ["modal", "dialog", "popup", "overlay", "confirm", "form modal"]):
            suggestions.append({
                "component": "modal",
                "variants": ["basic", "confirmation", "form", "timeline"],
                "reason": "Keywords suggest dialog or overlay interaction",
                "example": "Modal for confirmations, forms, or detailed content"
            })
            
        # Context-based suggestions
        if context == "e-shop":
            if not any(s["component"] == "button" for s in suggestions):
                suggestions.append({
                    "component": "button",
                    "variants": ["primary", "danger"],
                    "reason": "E-shop needs purchase and delete buttons",
                    "example": "Buy now (primary), Remove from cart (danger)"
                })
            if not any(s["component"] == "input" for s in suggestions):
                suggestions.append({
                    "component": "input",
                    "variants": ["search", "number", "email"],
                    "reason": "E-shop needs search, quantity, and contact inputs",
                    "example": "Product search, quantity selection, email for checkout"
                })
            if not any(s["component"] == "navbar" for s in suggestions):
                suggestions.append({
                    "component": "navbar",
                    "variants": ["basic", "with-dropdown"],
                    "reason": "E-shop needs navigation with product categories",
                    "example": "Navigation with shopping cart and user account access"
                })
            if not any(s["component"] == "modal" for s in suggestions):
                suggestions.append({
                    "component": "modal",
                    "variants": ["confirmation", "form"],
                    "reason": "E-shop needs confirmation dialogs and checkout forms",
                    "example": "Delete confirmation, checkout forms, product details"
                })
                
        elif context == "dashboard":
            if not any(s["component"] == "alert" for s in suggestions):
                suggestions.append({
                    "component": "alert",
                    "variants": ["info", "success", "warning", "error"],
                    "reason": "Dashboard needs status and notification alerts",
                    "example": "System status alerts and user notifications"
                })
            if not any(s["component"] == "navbar" for s in suggestions):
                suggestions.append({
                    "component": "navbar",
                    "variants": ["dark", "fixed"],
                    "reason": "Dashboard needs consistent navigation",
                    "example": "Fixed navigation for admin panel access"
                })
            if not any(s["component"] == "modal" for s in suggestions):
                suggestions.append({
                    "component": "modal",
                    "variants": ["confirmation", "form", "timeline"],
                    "reason": "Dashboard needs dialogs for admin actions and data entry",
                    "example": "Confirmation dialogs, add user forms, project timelines"
                })
                
        elif context == "landing" or context == "website":
            if not any(s["component"] == "navbar" for s in suggestions):
                suggestions.append({
                    "component": "navbar",
                    "variants": ["basic", "fixed"],
                    "reason": "Landing pages need prominent navigation",
                    "example": "Hero navigation with CTA button"
                })
                
        elif context == "form" or context == "contact":
            if not any(s["component"] == "input" for s in suggestions):
                suggestions.append({
                    "component": "input",
                    "variants": ["text", "email", "tel"],
                    "reason": "Contact forms need basic input fields",
                    "example": "Name, email, and phone inputs for contact"
                })
            if not any(s["component"] == "textarea" for s in suggestions):
                suggestions.append({
                    "component": "textarea",
                    "variants": ["basic"],
                    "reason": "Contact forms need message field",
                    "example": "Message textarea for detailed inquiries"
                })
            
        if not suggestions:
            suggestions.append({
                "component": "button", 
                "variants": ["primary"],
                "reason": "Default suggestion - buttons are universally useful",
                "example": "Start with a primary button for main actions"
            })
            
        result_text = f"🎯 Component Suggestions for: **'{description}'**\n📍 Context: {context}\n\n"
        
        for i, suggestion in enumerate(suggestions, 1):
            icon_map = {
                "input": "📝", "textarea": "📄", "alert": "🚨", 
                "button": "🔘", "form": "📋", "card": "🃏", "navbar": "🧭", "modal": "💬"
            }
            icon = icon_map.get(suggestion['component'], "📦")
            
            result_text += f"{i}. {icon} **{suggestion['component'].title()}** Component\n"
            result_text += f"   📋 Variants: {', '.join(suggestion['variants'])}\n"
            result_text += f"   💡 Reason: {suggestion['reason']}\n"
            result_text += f"   🔧 Example: {suggestion['example']}\n\n"
            
        result_text += "💡 **Try generating**: `generate_component('input', 'email', {'label': 'Email Address', 'required': True})`"
            
        return {
            "content": [
                {
                    "type": "text",
                    "text": result_text
                }
            ]
        }

    def run_stdio(self):
        """Run MCP server in stdio mode for Cline"""
        import sys
        
        print("Flowbite MCP Server starting in stdio mode...", file=sys.stderr)
        
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                    
                # Parse JSON-RPC request
                try:
                    request = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue
                    
                # Handle request
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")
                
                # Run async handler
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    result = loop.run_until_complete(self.handle_rpc_call(method, params))
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0", 
                        "id": request_id,
                        "error": {
                            "code": -32603,
                            "message": str(e)
                        }
                    }
                finally:
                    loop.close()
                
                # Send response
                print(json.dumps(response), flush=True)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    server = SimpleMCPServer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        server.run_stdio()
    else:
        print("🚀 Flowbite MCP Server (Simplified)")
        print("="*50)
        print("Usage:")
        print("  python mcp_server_simple.py --stdio  # For Cline integration")
        print("\nAvailable tools:")
        for tool_name, tool_info in server.tools.items():
            print(f"  • {tool_name}: {tool_info['description']}")
        print("\nReady for MCP testing! 🎯")