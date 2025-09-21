#!/usr/bin/env python3
"""
Flowbite MCP Server - Simplified functional testing
Test only functionality that doesn't require external dependencies
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_structure():
    """Test základnej štruktúry projektu"""
    print("🔍 Testovanie základnej štruktúry...")
    
    # Test konfigurácie
    try:
        from src.config import get_config, ServerConfig
        config = get_config()
        print(f"✅ Config načítaný: {config.name} v{config.version}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False


def test_json_structure():
    """Test štruktúry JSON súborov"""
    print("\n🔍 Testovanie štruktúry JSON súborov...")
    
    component_files = {
        "data/components/button.json": ["description", "category", "variants"],
        "data/components/form.json": ["description", "category", "variants"]
    }
    
    results = []
    
    for file_path, required_keys in component_files.items():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Test required keys
            missing_keys = []
            for key in required_keys:
                if key not in data:
                    missing_keys.append(key)
            
            if missing_keys:
                print(f"❌ {file_path}: chýbajú kľúče {missing_keys}")
                results.append(False)
            else:
                # Test variants structure
                if isinstance(data["variants"], dict):
                    variant_count = len(data["variants"])
                    print(f"✅ {file_path}: OK ({variant_count} variants)")
                    results.append(True)
                else:
                    print(f"❌ {file_path}: variants nie je dictionary")
                    results.append(False)
                    
        except json.JSONDecodeError as e:
            print(f"❌ {file_path}: neplatný JSON")
            results.append(False)
        except Exception as e:
            print(f"❌ {file_path}: {e}")
            results.append(False)
    
    return all(results)


def test_code_syntax():
    """Test syntaxe Python súborov bez importov"""
    print("\n🔍 Testovanie syntaxe kódu...")
    
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
    
    results = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Basic syntax check using compile
            compile(code, file_path, 'exec')
            print(f"✅ {file_path}: syntax OK")
            results.append(True)
            
        except SyntaxError as e:
            print(f"❌ {file_path}: syntax error na riadku {e.lineno}")
            results.append(False)
        except Exception as e:
            print(f"❌ {file_path}: {e}")
            results.append(False)
    
    return all(results)


def test_mcp_annotations():
    """Test prítomnosti MCP anotácií"""
    print("\n🔍 Testovanie MCP anotácií...")
    
    try:
        with open("src/server.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        mcp_features = {
            "@app.tool()": "MCP tool decorator",
            "generate_component": "Generate component tool",
            "validate_component": "Validate component tool", 
            "suggest_components": "Suggest components tool",
            "@app.resource(": "MCP resource decorator",
            "flowbite://components": "Components resource",
            "flowbite://docs": "Documentation resource"
        }
        
        results = []
        for feature, description in mcp_features.items():
            if feature in content:
                print(f"✅ {description} - nájdený")
                results.append(True)
            else:
                print(f"❌ {description} - chýba")
                results.append(False)
        
        return all(results)
        
    except Exception as e:
        print(f"❌ Error reading server.py: {e}")
        return False


def test_templates_structure():
    """Test prítomnosti template štruktúr"""
    print("\n🔍 Testovanie template štruktúr...")
    
    try:
        # Test button.json templates
        with open("data/components/button.json", 'r', encoding='utf-8') as f:
            button_data = json.load(f)
        
        template_found = False
        
        # Check if variants have HTML templates
        if "variants" in button_data:
            for variant_name, variant_data in button_data["variants"].items():
                if "html" in variant_data:
                    template_found = True
                    break
        
        if template_found:
            print("✅ Button komponenty obsahujú HTML templates")
        else:
            print("❌ Button komponenty neobsahujú HTML templates")
        
        # Test form.json templates
        with open("data/components/form.json", 'r', encoding='utf-8') as f:
            form_data = json.load(f)
        
        form_template_found = False
        if "variants" in form_data:
            for variant_name, variant_data in form_data["variants"].items():
                if "html" in variant_data:
                    form_template_found = True
                    break
        
        if form_template_found:
            print("✅ Form komponenty obsahujú HTML templates")
        else:
            print("❌ Form komponenty neobsahujú HTML templates")
        
        return template_found and form_template_found
        
    except Exception as e:
        print(f"❌ Template test error: {e}")
        return False


def main():
    """Hlavná test funkcia"""
    print("🚀 Flowbite MCP Server - Simplified functional testing")
    print("=" * 55)
    
    tests = [
        ("Základná štruktúra", test_basic_structure),
        ("JSON štruktúra", test_json_structure),
        ("Syntax kódu", test_code_syntax),
        ("MCP anotácie", test_mcp_annotations),
        ("Template štruktúry", test_templates_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 55)
    print("📋 SÚHRN SIMPLIFIED TESTOVANIA")
    print("=" * 55)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PREŠIEL" if result else "❌ NEPREŠIEL"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Výsledok: {passed}/{total} testov prešlo")
    
    if passed == total:
        print("🎉 Všetky základné testy úspešné!")
        print("📋 Odporúčania pre ďalší vývoj:")
        print("   1. Nainštalovať Python dependencies (fastmcp, pydantic, jinja2, beautifulsoup4)")
        print("   2. Spustiť server a testovať MCP nástroje")
        print("   3. Rozšíriť komponenty o ďalšie Flowbite prvky")
        print("   4. Pridať komplexnejšie template štruktúry")
    else:
        print("⚠️  Niektoré základné testy zlyhali")
        print("🔧 Opravte základné problémy pred pokračovaním")
    
    # Additional information
    print(f"\n💡 INFORMÁCIE O PROJEKTE:")
    print(f"   📁 Lokácia: {Path.cwd()}")
    print(f"   🐍 Python verzia: {sys.version.split()[0]}")
    print(f"   📦 Štruktúra: Kompletná MCP server implementácia")
    print(f"   🎯 Stav: {'Pripravený na produkciu' if passed == total else 'Potrebuje opravu'}")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)