#!/usr/bin/env python3
"""
Test script pre nové Flowbite komponenty v MCP serveri
"""

import json
import subprocess
import time

def test_new_components():
    """Test nových komponentov v MCP serveri"""
    
    print("🧪 Testing NEW Flowbite Components")
    print("="*50)
    
    # Test scenarios pre nové komponenty
    test_cases = [
        {
            "name": "Generate Email Input",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "input",
                    "variant": "email",
                    "props": {
                        "label": "Email Address",
                        "placeholder": "Enter your email",
                        "required": True,
                        "id": "user_email"
                    }
                }
            }
        },
        {
            "name": "Generate Search Input",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "input",
                    "variant": "search",
                    "props": {
                        "label": "Search Products",
                        "placeholder": "Search for products...",
                        "id": "product_search"
                    }
                }
            }
        },
        {
            "name": "Generate Number Input",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "input",
                    "variant": "number",
                    "props": {
                        "label": "Quantity",
                        "placeholder": "Enter quantity",
                        "min": "1",
                        "max": "99",
                        "step": "1",
                        "required": True
                    }
                }
            }
        },
        {
            "name": "Generate Resizable Textarea",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "textarea",
                    "variant": "resizable",
                    "props": {
                        "label": "Your Message",
                        "placeholder": "Tell us about your project...",
                        "rows": "6",
                        "required": True
                    }
                }
            }
        },
        {
            "name": "Generate Success Alert",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "alert",
                    "variant": "success",
                    "props": {
                        "title": "Success!",
                        "message": "Your order has been successfully placed."
                    }
                }
            }
        },
        {
            "name": "Generate Warning Alert",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "alert",
                    "variant": "warning",
                    "props": {
                        "title": "Warning:",
                        "message": "Your session will expire in 5 minutes."
                    }
                }
            }
        },
        {
            "name": "Generate Dismissible Alert",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "alert",
                    "variant": "dismissible",
                    "props": {
                        "title": "Info:",
                        "message": "Check out our new features in the dashboard."
                    }
                }
            }
        },
        {
            "name": "Suggest Components for Registration Form",
            "method": "tools/call",
            "params": {
                "name": "suggest_components",
                "arguments": {
                    "description": "user registration form with name, email, password fields",
                    "context": "form"
                }
            }
        },
        {
            "name": "Suggest Components for E-shop Product Page",
            "method": "tools/call",
            "params": {
                "name": "suggest_components",
                "arguments": {
                    "description": "product page with search, quantity input, and buy button",
                    "context": "e-shop"
                }
            }
        },
        {
            "name": "Validate Alert HTML",
            "method": "tools/call",
            "params": {
                "name": "validate_component",
                "arguments": {
                    "html": '<div class="flex items-center p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50" role="alert">Success message</div>',
                    "component_type": "alert"
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
    print("\n🚀 Enhanced MCP server ready for Cline testing!")

def test_component_generation():
    """Quick component generation test"""
    print("\n" + "="*50)
    print("🎨 QUICK COMPONENT SHOWCASE")
    print("="*50)
    
    components_to_showcase = [
        ("input", "email", {"label": "Email", "required": True}),
        ("input", "password", {"label": "Password", "required": True}),
        ("textarea", "basic", {"label": "Message", "rows": "4"}),
        ("alert", "success", {"title": "Success!", "message": "Data saved."}),
        ("alert", "error", {"title": "Error!", "message": "Please fix the issues."}),
    ]
    
    for comp_type, variant, props in components_to_showcase:
        print(f"\n🔧 {comp_type} ({variant}):")
        print(f"   Props: {props}")
        print(f"   Usage: generate_component('{comp_type}', '{variant}', {props})")

if __name__ == "__main__":
    test_new_components()
    test_component_generation()