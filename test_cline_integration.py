#!/usr/bin/env python3
"""
Quick test script pre Flowbite MCP Server
Simuluje Cline extension komunikáciu
"""

import json
import subprocess
import time

def test_mcp_server():
    """Test MCP server functionality"""
    
    print("🧪 Testing Flowbite MCP Server")
    print("="*50)
    
    # Test scenarios
    test_cases = [
        {
            "name": "Generate Primary Button",
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "button",
                    "variant": "primary",
                    "props": {"text": "Click Me!"}
                }
            }
        },
        {
            "name": "Generate Contact Form", 
            "method": "tools/call",
            "params": {
                "name": "generate_component",
                "arguments": {
                    "component_type": "form",
                    "variant": "contact"
                }
            }
        },
        {
            "name": "Validate Button HTML",
            "method": "tools/call", 
            "params": {
                "name": "validate_component",
                "arguments": {
                    "html": '<button type="button" class="bg-blue-500 text-white px-4 py-2 rounded">Test</button>',
                    "component_type": "button"
                }
            }
        },
        {
            "name": "Suggest E-shop Components",
            "method": "tools/call",
            "params": {
                "name": "suggest_components", 
                "arguments": {
                    "description": "product listing page with buy buttons",
                    "context": "e-shop"
                }
            }
        }
    ]
    
    # Start MCP server process
    print("🚀 Starting MCP server...")
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
            else:
                content = result["result"]["content"][0]["text"]
                # Truncate long output
                display_content = content[:200] + "..." if len(content) > 200 else content
                print(f"✅ Success: {display_content}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        # Cleanup
        process.terminate()
        process.wait()
        
    print(f"\n🎯 Testing completed!")
    print("Ready for Cline extension integration! 🚀")

if __name__ == "__main__":
    test_mcp_server()