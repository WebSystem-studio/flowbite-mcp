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

    async def generate_component(self, component_type: str, variant: str = "primary", props: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate component HTML"""
        props = props or {}
        
        if component_type not in self.components_db:
            return {"error": f"Unknown component type: {component_type}"}
            
        component_variants = self.components_db[component_type]["variants"]
        if variant not in component_variants:
            available = list(component_variants.keys())
            return {"error": f"Unknown variant '{variant}' for {component_type}. Available: {available}"}
            
        template_data = component_variants[variant]
        html_template = template_data["html"]
        
        # Simple template replacement
        text = props.get("text", "Default Text")
        title = props.get("title", "Default Title")
        content = props.get("content", "Default content description.")
        
        html = html_template.replace("{{text}}", text)
        html = html.replace("{{title}}", title)
        html = html.replace("{{content}}", content)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Generated {component_type} component ({variant} variant):\n\n```html\n{html}\n```\n\nCSS Classes used: {', '.join(template_data['css_classes'][:10])}..."
                }
            ]
        }

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
        
        # Button suggestions
        if any(word in desc_lower for word in ["button", "click", "submit", "action", "cta"]):
            suggestions.append({
                "component": "button",
                "variants": ["primary", "secondary", "danger"],
                "reason": "Keywords suggest interactive element",
                "example": "Primary button for main actions, secondary for alternatives"
            })
            
        # Form suggestions  
        if any(word in desc_lower for word in ["form", "input", "contact", "register", "login", "submit"]):
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
            
        # Context-based suggestions
        if context == "e-shop":
            suggestions.append({
                "component": "button",
                "variants": ["primary", "danger"],
                "reason": "E-shop needs purchase and delete buttons",
                "example": "Buy now (primary), Remove from cart (danger)"
            })
            
        if not suggestions:
            suggestions.append({
                "component": "button", 
                "variants": ["primary"],
                "reason": "Default suggestion - buttons are universally useful",
                "example": "Start with a primary button for main actions"
            })
            
        result_text = f"Component Suggestions for: '{description}'\nContext: {context}\n\n"
        
        for i, suggestion in enumerate(suggestions, 1):
            result_text += f"{i}. **{suggestion['component'].title()}** Component\n"
            result_text += f"   Variants: {', '.join(suggestion['variants'])}\n"
            result_text += f"   Reason: {suggestion['reason']}\n"
            result_text += f"   Example: {suggestion['example']}\n\n"
            
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