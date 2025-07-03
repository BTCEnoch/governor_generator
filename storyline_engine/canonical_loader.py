#!/usr/bin/env python3
"""
Canonical Elements Loader - Simple pack file loader
Loads watchtowers, aethyrs, sigillum, and enochian alphabet data
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class CanonicalLoader:
    """Simple loader for canonical /pack/ files"""
    
    def __init__(self, base_path: Path = Path(".")):
        self.pack_path = Path(base_path) / "pack"
        self._cache = {}
        
        if not self.pack_path.exists():
            raise FileNotFoundError(f"Pack directory not found: {self.pack_path}")
    
    def load_watchtowers(self) -> Dict:
        """Load watchtowers.json"""
        if "watchtowers" not in self._cache:
            with open(self.pack_path / "watchtowers.json", 'r') as f:
                self._cache["watchtowers"] = json.load(f)
        return self._cache["watchtowers"]
    
    def load_aethyrs(self) -> Dict:
        """Load aethyrs.json"""
        if "aethyrs" not in self._cache:
            with open(self.pack_path / "aethyrs.json", 'r') as f:
                self._cache["aethyrs"] = json.load(f)
        return self._cache["aethyrs"]
    
    def load_enochian_alphabet(self) -> Dict:
        """Load enochian_alphabet.json"""
        if "alphabet" not in self._cache:
            with open(self.pack_path / "enochian_alphabet.json", 'r') as f:
                self._cache["alphabet"] = json.load(f)
        return self._cache["alphabet"]

def test_canonical_loader():
    """Simple test"""
    try:
        loader = CanonicalLoader()
        
        watchtowers = loader.load_watchtowers()
        aethyrs = loader.load_aethyrs()
        alphabet = loader.load_enochian_alphabet()
        
        print(f"✅ Loaded watchtowers: {len(watchtowers)} elements")
        print(f"✅ Loaded aethyrs: {len(aethyrs)} elements") 
        print(f"✅ Loaded alphabet: {len(alphabet)} elements")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_canonical_loader() 