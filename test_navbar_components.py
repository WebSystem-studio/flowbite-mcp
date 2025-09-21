#!/usr/bin/env python3
"""
Test script pre navbar komponenty v MCP serveri
"""

import json
import subprocess
import time

def test_navbar_components():
    """Test navbar komponentov v MCP serveri"""
    
    print("🧪 Testing NAVBAR Components")
    print("="*50)
    
    # Test scenarios pre navbar komponenty
    test_cases = [
        {
            "name": "Generate Basic Navbar",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "navbar",
                    "variant": "basic",
                    "props": {
                        "brand": "My Website",
                        "nav_items": ["Home", "About", "Services", "Contact"]
                    }
                }
            }
        },
        {
            "name": "Generate Navbar with Dropdown",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "navbar",
                    "variant": "with-dropdown",
                    "props": {
                        "brand": "E-Commerce",
                        "dropdown_title": "Categories",
                        "dropdown_items": ["Electronics", "Clothing", "Books", "Sports"]
                    }
                }
            }
        },
        {
            "name": "Generate Dark Navbar",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "navbar",
                    "variant": "dark",
                    "props": {
                        "brand": "Dashboard",
                        "nav_items": ["Dashboard", "Analytics", "Reports", "Settings"]
                    }
                }
            }
        },
        {
            "name": "Generate Fixed Navbar with CTA",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "navbar",
                    "variant": "fixed",
                    "props": {
                        "brand": "SaaS Platform",
                        "nav_items": ["Features", "Pricing", "About"],
                        "cta_text": "Sign Up"
                    }
                }
            }
        },
        {
            "name": "Suggest Components for Landing Page",
            "method": "tools/call",
            "params": {
                "name": "suggest_components",
                "arguments": {
                    "description": "landing page with navigation and hero section",
                    "context": "landing"
                }
            }
        },
        {
            "name": "Suggest Components for E-shop",
            "method": "tools/call",
            "params": {
                "name": "suggest_components",
                "arguments": {
                    "description": "e-shop with product categories and shopping cart",
                    "context": "e-shop"
                }
            }
        },
        {
            "name": "Validate Navbar HTML",
            "method": "tools/call",
            "params": {
                "name": "validate_component",
                "arguments": {
                    "html": '<nav class="bg-white border-gray-200"><div class="max-w-screen-xl flex items-center justify-between mx-auto p-4"><span class="text-2xl font-semibold">Brand</span></div></nav>',
                    "component_type": "navbar"
                }
            }
        }
    ]
    
    # Start MCP server process
    print("🚀 Starting enhanced MCP server...")
    process = subprocess.Popen(
        ["python3", "mcp_server_simple.py", "--stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/mnt/raid1/www/flowbite-mcp"
    )
    
    time.sleep(1)  # Let server start
    
    # Initialize MCP
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    
    try:
        # Send init
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        init_result = json.loads(response)
        print(f"✅ Server initialized: {init_result['result']['serverInfo']['name']}")
        
        # Run test cases
        passed = 0
        failed = 0
        
        for i, test_case in enumerate(test_cases, 2):
            print(f"\n🧪 Test {i-1}: {test_case['name']}")
            
            request = {
                "jsonrpc": "2.0",
                "id": i,
                "method": test_case["method"],
                "params": test_case["params"]
            }
            
            # Send request
            process.stdin.write(json.dumps(request) + "\n")
            process.stdin.flush()
            
            # Read response
            response = process.stdout.readline()
            result = json.loads(response)
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
                failed += 1
            else:
                content = result["result"]["content"][0]["text"]
                # Show first line of content
                first_line = content.split('\n')[0]
                print(f"✅ Success: {first_line}")
                passed += 1
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        failed += 1
    finally:
        # Cleanup
        process.terminate()
        process.wait()
        
    print(f"\n🎯 Testing completed!")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success rate: {passed}/{passed+failed} ({100*passed/(passed+failed):.1f}%)")
    print("\n🚀 Navbar components ready for Cline testing!")

def show_navbar_examples():
    """Show navbar usage examples"""
    print("\n" + "="*50)
    print("🧭 NAVBAR COMPONENT EXAMPLES")
    print("="*50)
    
    examples = [
        {
            "type": "Basic Navbar",
            "command": "generate_component('navbar', 'basic', {'brand': 'My Site', 'nav_items': ['Home', 'About']})",
            "use_case": "Simple website navigation"
        },
        {
            "type": "Dropdown Navbar",
            "command": "generate_component('navbar', 'with-dropdown', {'brand': 'E-shop', 'dropdown_title': 'Categories'})",
            "use_case": "E-commerce site with product categories"
        },
        {
            "type": "Dark Navbar",
            "command": "generate_component('navbar', 'dark', {'brand': 'Dashboard'})",
            "use_case": "Admin dashboard or dark theme sites"
        },
        {
            "type": "Fixed Navbar",
            "command": "generate_component('navbar', 'fixed', {'brand': 'SaaS', 'cta_text': 'Sign Up'})",
            "use_case": "Landing page with sticky navigation and CTA"
        }
    ]
    
    for example in examples:
        print(f"\n🔧 {example['type']}:")
        print(f"   Command: {example['command']}")
        print(f"   Use Case: {example['use_case']}")

if __name__ == "__main__":
    test_navbar_components()
    show_navbar_examples()