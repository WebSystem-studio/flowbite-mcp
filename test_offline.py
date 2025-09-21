#!/usr/bin/env python3
"""
Offline testovací script pre Flowbite MCP server
Testuje funkčnosť bez externájch závislostí
"""

import sys
import json
import os
from pathlib import Path

def test_project_structure():
    """Test projektovej štruktúry"""
    print("🔍 Testovanie projektovej štruktúry...")
    
    required_dirs = [
        "src",
        "src/models", 
        "src/tools",
        "src/resources",
        "data",
        "data/components",
        "tests"
    ]
    
    required_files = [
        "src/server.py",
        "src/config.py",
        "src/models/component.py",
        "src/tools/generator.py",
        "src/tools/validator.py", 
        "src/tools/suggestions.py",
        "src/resources/component_db.py",
        "src/resources/documentation.py",
        "requirements.txt",
        "README.md"
    ]
    
    errors = []
    
    # Test adresárov
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            errors.append(f"❌ Chýba adresár: {dir_path}")
        else:
            print(f"✅ Adresár OK: {dir_path}")
    
    # Test súborov
    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"❌ Chýba súbor: {file_path}")
        else:
            print(f"✅ Súbor OK: {file_path}")
    
    return errors


def test_config_file():
    """Test konfiguračného súboru"""
    print("\n🔍 Testovanie konfigurácie...")
    
    config_path = Path("src/config.py")
    if not config_path.exists():
        return ["❌ Config súbor neexistuje"]
    
    # Prečítanie a základná kontrola
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            "class ServerConfig",
            "name:",
            "version:",
            "description:",
            "data_dir:",
            "def get_config"
        ]
        
        errors = []
        for element in required_elements:
            if element not in content:
                errors.append(f"❌ Chýba v config: {element}")
            else:
                print(f"✅ Config obsahuje: {element}")
        
        return errors
        
    except Exception as e:
        return [f"❌ Chyba pri čítaní config: {e}"]


def test_component_data():
    """Test databázy komponentov"""
    print("\n🔍 Testovanie databázy komponentov...")
    
    component_files = [
        "data/components/button.json",
        "data/components/form.json"
    ]
    
    errors = []
    
    for file_path in component_files:
        if not Path(file_path).exists():
            errors.append(f"❌ Chýba component súbor: {file_path}")
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Základná validácia štruktúry
            required_keys = ["description", "category", "variants"]
            for key in required_keys:
                if key not in data:
                    errors.append(f"❌ Chýba kľúč '{key}' v {file_path}")
                else:
                    print(f"✅ {file_path} obsahuje: {key}")
            
            # Test variant
            if "variants" in data:
                variant_count = len(data["variants"])
                print(f"✅ {file_path} má {variant_count} variant")
                
                # Test prvej varianty
                if variant_count > 0:
                    first_variant = list(data["variants"].values())[0]
                    if "html" in first_variant:
                        print(f"✅ Varianty obsahujú HTML templates")
                    if "css_classes" in first_variant:
                        print(f"✅ Varianty obsahujú CSS classes")
            
        except json.JSONDecodeError as e:
            errors.append(f"❌ Neplatný JSON v {file_path}: {e}")
        except Exception as e:
            errors.append(f"❌ Chyba pri čítaní {file_path}: {e}")
    
    return errors


def test_file_syntax():
    """Test syntaxe Python súborov"""
    print("\n🔍 Testovanie syntaxe Python súborov...")
    
    python_files = [
        "src/server.py",
        "src/config.py", 
        "src/models/component.py",
        "src/tools/generator.py",
        "src/tools/validator.py",
        "src/tools/suggestions.py",
        "src/resources/component_db.py",
        "src/resources/documentation.py"
    ]
    
    errors = []
    
    for file_path in python_files:
        if not Path(file_path).exists():
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Základná syntax kontrola
            compile(content, file_path, 'exec')
            print(f"✅ Syntax OK: {file_path}")
            
            # Kontrola imports
            if "from fastmcp import" in content:
                print(f"🔧 {file_path} používa FastMCP")
            if "from pydantic import" in content:
                print(f"🔧 {file_path} používa Pydantic")
            if "import jinja2" in content or "from jinja2 import" in content:
                print(f"🔧 {file_path} používa Jinja2")
                
        except SyntaxError as e:
            errors.append(f"❌ Syntax chyba v {file_path}: {e}")
        except Exception as e:
            errors.append(f"❌ Chyba pri čítaní {file_path}: {e}")
    
    return errors


def test_line_counts():
    """Test počtu riadkov kódu"""
    print("\n📊 Štatistiky kódu...")
    
    python_files = [
        "src/server.py",
        "src/config.py",
        "src/models/component.py", 
        "src/tools/generator.py",
        "src/tools/validator.py",
        "src/tools/suggestions.py",
        "src/resources/component_db.py",
        "src/resources/documentation.py"
    ]
    
    total_lines = 0
    
    for file_path in python_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                print(f"📄 {file_path}: {lines} riadkov")
                total_lines += lines
            except Exception:
                pass
    
    print(f"\n📊 Celkom: {total_lines} riadkov kódu")
    return []


def test_mcp_tools_definition():
    """Test definície MCP tools"""
    print("\n🔍 Testovanie MCP tools definícií...")
    
    server_path = Path("src/server.py")
    if not server_path.exists():
        return ["❌ Server súbor neexistuje"]
    
    try:
        with open(server_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        expected_tools = [
            "@app.tool()",
            "generate_component",
            "validate_component", 
            "suggest_components"
        ]
        
        errors = []
        for tool in expected_tools:
            if tool in content:
                print(f"✅ Nájdený MCP tool: {tool}")
            else:
                errors.append(f"❌ Chýba MCP tool: {tool}")
        
        # Test resources
        expected_resources = [
            "@app.resource(",
            "flowbite://components",
            "flowbite://docs"
        ]
        
        for resource in expected_resources:
            if resource in content:
                print(f"✅ Nájdený MCP resource: {resource}")
            else:
                errors.append(f"❌ Chýba MCP resource: {resource}")
        
        return errors
        
    except Exception as e:
        return [f"❌ Chyba pri čítaní server súboru: {e}"]


def main():
    """Hlavná testovacia funkcia"""
    print("🚀 Flowbite MCP Server - Offline testovanie")
    print("=" * 50)
    
    all_errors = []
    
    # Spustenie testov
    tests = [
        ("Projektová štruktúra", test_project_structure),
        ("Konfiguračný súbor", test_config_file),
        ("Databáza komponentov", test_component_data),
        ("Syntax Python súborov", test_file_syntax),
        ("MCP tools definície", test_mcp_tools_definition),
        ("Štatistiky kódu", test_line_counts)
    ]
    
    for test_name, test_func in tests:
        try:
            errors = test_func()
            all_errors.extend(errors)
        except Exception as e:
            error_msg = f"❌ Test '{test_name}' zlyhal: {e}"
            print(error_msg)
            all_errors.append(error_msg)
    
    # Súhrn
    print("\n" + "=" * 50)
    print("📋 SÚHRN TESTOVANIA")
    print("=" * 50)
    
    if not all_errors:
        print("🎉 Všetky testy prešli úspešne!")
        print("✅ Projekt je pripravený na testovanie s dependencies")
    else:
        print(f"⚠️  Nájdených {len(all_errors)} problémov:")
        for error in all_errors:
            print(f"   {error}")
    
    print("\n🔧 Pre úplné testovanie je potrebné nainštalovať:")
    print("   - fastmcp>=0.2.0")
    print("   - pydantic>=2.5.0") 
    print("   - jinja2>=3.1.0")
    print("   - beautifulsoup4>=4.12.0")
    
    return len(all_errors) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)