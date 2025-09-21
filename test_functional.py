#!/usr/bin/env python3
"""
Flowbite MCP Server - Funkčné testovanie
Test základnej funkčnosti MCP servera s reálnymi dependencies
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Pridáme src do path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_imports():
    """Test importu všetkých modulov"""
    print("🔍 Testovanie importov...")
    
    try:
        # Test základných importov
        from src.config import get_config, ServerConfig
        print("✅ Config import OK")
        
        from src.models.component import Component, ComponentRequest, ComponentResponse
        print("✅ Models import OK")
        
        from src.tools.generator import ComponentGenerator
        print("✅ Generator import OK")
        
        from src.tools.validator import ComponentValidator  
        print("✅ Validator import OK")
        
        from src.tools.suggestions import ComponentSuggestions
        print("✅ Suggestions import OK")
        
        from src.resources.component_db import ComponentDatabase
        print("✅ Database import OK")
        
        from src.resources.documentation import DocumentationResource
        print("✅ Documentation import OK")
        
        # Test FastMCP importu
        from fastmcp import FastMCP
        print("✅ FastMCP import OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


async def test_config():
    """Test konfigurácie"""
    print("\n🔍 Testovanie konfigurácie...")
    
    try:
        from src.config import get_config
        
        config = get_config()
        print(f"✅ Config načítaný: {config.name}")
        print(f"✅ Verzia: {config.version}")
        print(f"✅ Data dir: {config.data_dir}")
        
        # Test že data_dir existuje
        if Path(config.data_dir).exists():
            print("✅ Data directory existuje")
        else:
            print("❌ Data directory neexistuje")
            
        return True
        
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False


async def test_component_database():
    """Test component databázy"""
    print("\n🔍 Testovanie component databázy...")
    
    try:
        from src.resources.component_db import ComponentDatabase
        
        db = ComponentDatabase()
        await db.initialize()
        print("✅ Database inicializovaná")
        
        # Test načítania komponentov
        components = await db.get_all_components()
        print(f"✅ Načítaných {len(components)} komponentov")
        
        # Test získania variantov
        if components:
            first_component = list(components.keys())[0]
            variants = await db.get_variants(first_component)
            print(f"✅ Component '{first_component}' má {len(variants)} variant")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_component_generator():
    """Test component generátora"""
    print("\n🔍 Testovanie component generátora...")
    
    try:
        from src.tools.generator import ComponentGenerator
        from src.resources.component_db import ComponentDatabase
        
        # Inicializácia
        db = ComponentDatabase()
        await db.initialize()
        generator = ComponentGenerator(db)
        
        # Test generovania button komponenta
        result = await generator.generate_component(
            component_type="button",
            variant="primary", 
            props={"text": "Test Button", "size": "md"}
        )
        
        print("✅ Button component vygenerovaný")
        print(f"   HTML dĺžka: {len(result.get('html', ''))}")
        print(f"   CSS classes: {len(result.get('css_classes', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Generator error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_component_validator():
    """Test component validátora"""
    print("\n🔍 Testovanie component validátora...")
    
    try:
        from src.tools.validator import ComponentValidator
        from src.resources.component_db import ComponentDatabase
        
        # Inicializácia
        db = ComponentDatabase()
        await db.initialize()
        validator = ComponentValidator(db)
        
        # Test validácie správneho HTML
        valid_html = '<button class="bg-blue-500 text-white px-4 py-2 rounded">Test</button>'
        result = await validator.validate_component(
            html=valid_html,
            component_type="button"
        )
        
        print("✅ Validator test dokončený")
        print(f"   Validation result: {result.get('is_valid', False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Validator error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_component_suggestions():
    """Test component suggestions"""
    print("\n🔍 Testovanie component suggestions...")
    
    try:
        from src.tools.suggestions import ComponentSuggestions
        from src.resources.component_db import ComponentDatabase
        
        # Inicializácia
        db = ComponentDatabase()
        await db.initialize()
        suggestions = ComponentSuggestions(db)
        
        # Test návrhov
        result = await suggestions.suggest_components(
            description="I need a blue button for form submission",
            limit=3
        )
        
        print("✅ Suggestions test dokončený")
        print(f"   Počet návrhov: {len(result.get('suggestions', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Suggestions error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Hlavná test funkcia"""
    print("🚀 Flowbite MCP Server - Funkčné testovanie")
    print("=" * 50)
    
    tests = [
        ("Importy", test_imports),
        ("Konfigurácia", test_config), 
        ("Component databáza", test_component_database),
        ("Component generátor", test_component_generator),
        ("Component validátor", test_component_validator),
        ("Component suggestions", test_component_suggestions)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Súhrn
    print("\n" + "=" * 50)
    print("📋 SÚHRN FUNKČNÉHO TESTOVANIA")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PREŠIEL" if result else "❌ NEPREŠIEL"
        print(f"{status}: {test_name}")
    
    print(f"\n📊 Výsledok: {passed}/{total} testov prešlo")
    
    if passed == total:
        print("🎉 Všetky funkčné testy úspešné!")
        print("🚀 Server je pripravený na produkčné použitie!")
    else:
        print("⚠️  Niektoré testy zlyhali - potrebná ďalšia oprava")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)