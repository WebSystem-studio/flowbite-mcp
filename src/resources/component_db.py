"""
Správa databázy komponentov pre MCP resources
"""

import json
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from dataclasses import asdict

from ..config import get_config
from ..models.component import FlowbiteComponent, ComponentType, ComponentVariant

# Konfigurácia
config = get_config()
logger = logging.getLogger(__name__)


class ComponentDatabase:
    """Správca databázy Flowbite komponentov"""
    
    def __init__(self):
        self.config = config
        self.components_dir = config.data_dir / "components"
        self._cache = {}
        self._index = {}
        self._initialize_index()
    
    def _initialize_index(self):
        """Inicializuje index komponentov"""
        try:
            index_file = self.components_dir / "index.json"
            
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    self._index = json.load(f)
            else:
                self._build_index()
                
        except Exception as e:
            logger.error(f"Chyba pri inicializácii indexu: {e}")
            self._index = {}
    
    def _build_index(self):
        """Zostaví index komponentov zo súborov"""
        try:
            self._index = {
                "components": {},
                "categories": {},
                "variants": {},
                "last_updated": None
            }
            
            # Prechádza všetky JSON súbory v components directory
            for json_file in self.components_dir.glob("*.json"):
                if json_file.name == "index.json":
                    continue
                
                try:
                    component_type = json_file.stem
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Registrácia komponentu
                    self._index["components"][component_type] = {
                        "file": json_file.name,
                        "variants": list(data.get("variants", {}).keys()),
                        "count": len(data.get("variants", {})),
                        "category": data.get("category", "general")
                    }
                    
                    # Indexovanie variant
                    for variant_name in data.get("variants", {}):
                        variant_key = f"{component_type}_{variant_name}"
                        self._index["variants"][variant_key] = {
                            "component_type": component_type,
                            "variant": variant_name,
                            "file": json_file.name
                        }
                    
                    # Indexovanie kategórií
                    category = data.get("category", "general")
                    if category not in self._index["categories"]:
                        self._index["categories"][category] = []
                    self._index["categories"][category].append(component_type)
                    
                except Exception as e:
                    logger.error(f"Chyba pri spracovaní {json_file}: {e}")
            
            # Uloženie indexu
            self._save_index()
            
        except Exception as e:
            logger.error(f"Chyba pri budovaní indexu: {e}")
    
    def _save_index(self):
        """Uloží index do súboru"""
        try:
            index_file = self.components_dir / "index.json"
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(self._index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Chyba pri ukladaní indexu: {e}")
    
    async def get_component(
        self,
        component_type: str,
        variant: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Načíta komponent z databázy
        
        Args:
            component_type: Typ komponentu
            variant: Konkrétna varianta
            
        Returns:
            Data komponentu alebo None
        """
        try:
            # Kontrola cache
            cache_key = f"{component_type}_{variant or 'all'}"
            if cache_key in self._cache:
                return self._cache[cache_key]
            
            # Načítanie zo súboru
            component_info = self._index["components"].get(component_type)
            if not component_info:
                return None
            
            file_path = self.components_dir / component_info["file"]
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Ak je špecifikovaná varianta
            if variant:
                variant_data = data.get("variants", {}).get(variant)
                if variant_data:
                    result = {
                        "type": component_type,
                        "variant": variant,
                        "category": data.get("category"),
                        "description": data.get("description"),
                        **variant_data
                    }
                else:
                    result = None
            else:
                result = data
            
            # Uloženie do cache
            self._cache[cache_key] = result
            return result
            
        except Exception as e:
            logger.error(f"Chyba pri načítaní komponentu {component_type}: {e}")
            return None
    
    async def list_components(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Zoznam dostupných komponentov
        
        Args:
            category: Filtrovanie podľa kategórie
            search: Vyhľadávací výraz
            
        Returns:
            Zoznam komponentov
        """
        try:
            components = []
            
            # Filtrovanie podľa kategórie
            if category:
                component_types = self._index["categories"].get(category, [])
            else:
                component_types = list(self._index["components"].keys())
            
            # Spracovanie každého komponentu
            for component_type in component_types:
                component_info = self._index["components"][component_type]
                
                # Aplikovanie vyhľadávania
                if search:
                    search_lower = search.lower()
                    if (search_lower not in component_type.lower() and
                        search_lower not in component_info.get("category", "").lower()):
                        continue
                
                components.append({
                    "type": component_type,
                    "category": component_info.get("category"),
                    "variants_count": component_info.get("count", 0),
                    "variants": component_info.get("variants", [])
                })
            
            return components
            
        except Exception as e:
            logger.error(f"Chyba pri listovaní komponentov: {e}")
            return []
    
    async def search_components(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Vyhľadá komponenty podľa query
        
        Args:
            query: Vyhľadávací výraz
            max_results: Maximum výsledkov
            
        Returns:
            Zoznam vyhovujúcich komponentov
        """
        try:
            results = []
            query_lower = query.lower()
            
            # Vyhľadávanie v názvoch komponentov
            for component_type, component_info in self._index["components"].items():
                score = 0
                
                # Skóre pre názov komponentu
                if query_lower == component_type.lower():
                    score += 100  # Presná zhoda
                elif query_lower in component_type.lower():
                    score += 50   # Čiastočná zhoda v názve
                
                # Skóre pre kategóriu
                category = component_info.get("category", "")
                if query_lower in category.lower():
                    score += 25
                
                # Skóre pre varianty
                for variant in component_info.get("variants", []):
                    if query_lower in variant.lower():
                        score += 15
                
                if score > 0:
                    results.append({
                        "type": component_type,
                        "category": category,
                        "variants": component_info.get("variants", []),
                        "score": score
                    })
            
            # Vyhľadávanie v obsahu súborov
            for component_type in self._index["components"].keys():
                if len(results) >= max_results * 2:  # Obmedzenie pre výkon
                    break
                
                component_data = await self.get_component(component_type)
                if component_data:
                    content_score = self._search_in_content(component_data, query_lower)
                    if content_score > 0:
                        # Kontrola či už nie je v rezultátoch
                        existing = next((r for r in results if r["type"] == component_type), None)
                        if existing:
                            existing["score"] += content_score
                        else:
                            results.append({
                                "type": component_type,
                                "category": component_data.get("category", ""),
                                "variants": list(component_data.get("variants", {}).keys()),
                                "score": content_score
                            })
            
            # Zoradenie podľa skóre
            results.sort(key=lambda x: x["score"], reverse=True)
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Chyba pri vyhľadávaní: {e}")
            return []
    
    def _search_in_content(self, content: Dict[str, Any], query: str) -> int:
        """Vyhľadá v obsahu komponentu"""
        score = 0
        
        # Vyhľadávanie v popise
        description = content.get("description", "")
        if query in description.lower():
            score += 20
        
        # Vyhľadávanie vo variantoch
        variants = content.get("variants", {})
        for variant_name, variant_data in variants.items():
            if query in variant_name.lower():
                score += 15
            
            # Vyhľadávanie v HTML kóde
            html = variant_data.get("html", "")
            if query in html.lower():
                score += 10
            
            # Vyhľadávanie v CSS triedach
            css_classes = variant_data.get("css_classes", [])
            for css_class in css_classes:
                if query in css_class.lower():
                    score += 5
        
        return score
    
    async def get_categories(self) -> Dict[str, List[str]]:
        """
        Vráti všetky kategórie s komponentmi
        
        Returns:
            Dictionary kategórií
        """
        return self._index.get("categories", {})
    
    async def get_variants(self, component_type: str) -> List[str]:
        """
        Vráti všetky varianty pre komponent
        
        Args:
            component_type: Typ komponentu
            
        Returns:
            Zoznam variant
        """
        component_info = self._index["components"].get(component_type)
        if component_info:
            return component_info.get("variants", [])
        return []
    
    async def add_component(
        self,
        component_type: str,
        component_data: Dict[str, Any]
    ) -> bool:
        """
        Pridá nový komponent do databázy
        
        Args:
            component_type: Typ komponentu
            component_data: Dáta komponentu
            
        Returns:
            True ak úspešne pridané
        """
        try:
            file_path = self.components_dir / f"{component_type}.json"
            
            # Validácia dát
            if not self._validate_component_data(component_data):
                return False
            
            # Uloženie súboru
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(component_data, f, indent=2, ensure_ascii=False)
            
            # Aktualizácia indexu
            self._build_index()
            
            # Vyčistenie cache
            self._cache.clear()
            
            logger.info(f"Komponent {component_type} úspešne pridaný")
            return True
            
        except Exception as e:
            logger.error(f"Chyba pri pridávaní komponentu {component_type}: {e}")
            return False
    
    def _validate_component_data(self, data: Dict[str, Any]) -> bool:
        """Validuje dáta komponentu"""
        required_fields = ["description", "category", "variants"]
        
        for field in required_fields:
            if field not in data:
                logger.error(f"Chýba povinné pole: {field}")
                return False
        
        # Validácia variant
        variants = data.get("variants", {})
        if not isinstance(variants, dict) or not variants:
            logger.error("Variants musí byť neprázdny dictionary")
            return False
        
        for variant_name, variant_data in variants.items():
            if not isinstance(variant_data, dict):
                logger.error(f"Neplatná varianta: {variant_name}")
                return False
            
            if "html" not in variant_data:
                logger.error(f"Chýba HTML v variante: {variant_name}")
                return False
        
        return True
    
    async def update_component(
        self,
        component_type: str,
        component_data: Dict[str, Any]
    ) -> bool:
        """
        Aktualizuje existujúci komponent
        
        Args:
            component_type: Typ komponentu
            component_data: Nové dáta
            
        Returns:
            True ak úspešne aktualizované
        """
        try:
            # Kontrola existencie
            existing = await self.get_component(component_type)
            if not existing:
                logger.error(f"Komponent {component_type} neexistuje")
                return False
            
            # Aktualizácia
            return await self.add_component(component_type, component_data)
            
        except Exception as e:
            logger.error(f"Chyba pri aktualizácii komponentu {component_type}: {e}")
            return False
    
    async def delete_component(self, component_type: str) -> bool:
        """
        Zmaže komponent z databázy
        
        Args:
            component_type: Typ komponentu
            
        Returns:
            True ak úspešne zmazané
        """
        try:
            file_path = self.components_dir / f"{component_type}.json"
            
            if file_path.exists():
                file_path.unlink()
                
                # Aktualizácia indexu
                self._build_index()
                
                # Vyčistenie cache
                self._cache.clear()
                
                logger.info(f"Komponent {component_type} úspešne zmazaný")
                return True
            else:
                logger.warning(f"Komponent {component_type} neexistuje")
                return False
                
        except Exception as e:
            logger.error(f"Chyba pri mazaní komponentu {component_type}: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Vráti štatistiky databázy
        
        Returns:
            Štatistiky databázy
        """
        try:
            total_components = len(self._index["components"])
            total_variants = len(self._index["variants"])
            categories = self._index["categories"]
            
            category_stats = {}
            for category, components in categories.items():
                category_stats[category] = {
                    "count": len(components),
                    "components": components
                }
            
            return {
                "total_components": total_components,
                "total_variants": total_variants,
                "categories": category_stats,
                "most_variants": max(
                    self._index["components"].items(),
                    key=lambda x: x[1].get("count", 0),
                    default=("none", {"count": 0})
                )[0] if total_components > 0 else None
            }
            
        except Exception as e:
            logger.error(f"Chyba pri získavaní štatistík: {e}")
            return {"error": str(e)}
    
    def clear_cache(self):
        """Vyčistí cache"""
        self._cache.clear()
        logger.info("Cache vyčistená")
    
    def rebuild_index(self):
        """Znovu zostaví index"""
        self._cache.clear()
        self._build_index()
        logger.info("Index znovu zostavený")


# Globálna inštancia databázy
component_db = ComponentDatabase()