"""
Bitcoin-based art generation
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from core.utils.custom_logging import setup_logger

logger = setup_logger("core.utils.bitcoin.art_generation")

class BitcoinArtGenerator:
    """Generates art using Bitcoin-derived entropy"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize art generator with optional configuration"""
        self.config = config or {}
        self.logger = logger
        
    def generate_color_scheme(self, entropy: str) -> List[str]:
        """Generate a color scheme from entropy"""
        colors = []
        for i in range(0, len(entropy), 6):
            if i + 6 <= len(entropy):
                colors.append(f"#{entropy[i:i+6]}")
        return colors[:5]  # Return up to 5 colors
        
    def generate_pattern(self, entropy: str, width: int, height: int) -> List[Dict[str, Any]]:
        """Generate a pattern from entropy"""
        pattern = []
        for i in range(0, len(entropy), 8):
            if i + 8 <= len(entropy):
                value = int(entropy[i:i+8], 16)
                pattern.append({
                    "x": value % width,
                    "y": (value >> 16) % height,
                    "size": (value >> 24) % 50 + 10,
                    "rotation": value % 360
                })
        return pattern

    async def generate_ritual_art(
        self,
        points: List[Tuple[float, float]],
        energy_levels: List[float],
        pattern_type: str = "relationship",
        entropy: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> str:
        """Generate ritual art based on points and energy levels"""
        try:
            # Generate entropy if not provided
            entropy_value = entropy if entropy is not None else hashlib.sha256(str(datetime.now()).encode()).hexdigest()
            
            # Generate art data
            art_data = {
                "metadata": {
                    "type": "ritual_art",
                    "pattern_type": pattern_type,
                    "timestamp": datetime.utcnow().isoformat(),
                    "entropy": entropy_value
                },
                "width": 1024,
                "height": 1024,
                "colors": self.generate_color_scheme(entropy_value),
                "pattern": self.generate_pattern(entropy_value, 1024, 1024),
                "ritual_elements": []
            }
            
            # Add ritual elements
            for (x, y), energy in zip(points, energy_levels):
                art_data["ritual_elements"].append({
                    "type": "energy_point",
                    "x": int(x * 1024),
                    "y": int(y * 1024),
                    "size": int(energy * 100),
                    "intensity": energy
                })
            
            # Save art data
            if output_path:
                # Create output directory if it doesn't exist
                output_dir = os.path.dirname(output_path)
                os.makedirs(output_dir, exist_ok=True)
                
                # Generate unique filename
                art_path = os.path.join(
                    output_dir,
                    f"ritual_{pattern_type}_{hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8]}.json"
                )
                
                with open(art_path, "w") as f:
                    json.dump(art_data, f, indent=2)
                return art_path
            else:
                return json.dumps(art_data, indent=2)
                
        except Exception as e:
            logger.error(f"Error generating ritual art: {str(e)}")
            raise
    
    def _generate_triangle(self, points: List[Tuple[int, int]]) -> List[Dict[str, Any]]:
        """Generate triangle pattern elements"""
        if len(points) < 3:
            return []
            
        elements = []
        
        # Add vertices
        for x, y in points[:3]:
            elements.append({
                "type": "vertex",
                "x": x,
                "y": y,
                "size": 10
            })
        
        # Add edges
        for i in range(3):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % 3]
            elements.append({
                "type": "edge",
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })
        
        return elements
    
    def _generate_square(self, points: List[Tuple[int, int]]) -> List[Dict[str, Any]]:
        """Generate square pattern elements"""
        if len(points) < 4:
            return []
            
        elements = []
        
        # Add vertices
        for x, y in points[:4]:
            elements.append({
                "type": "vertex",
                "x": x,
                "y": y,
                "size": 10
            })
        
        # Add edges
        for i in range(4):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % 4]
            elements.append({
                "type": "edge",
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })
        
        return elements
    
    def _generate_pentagram(self, points: List[Tuple[int, int]]) -> List[Dict[str, Any]]:
        """Generate pentagram pattern elements"""
        if len(points) < 5:
            return []
            
        elements = []
        
        # Add vertices
        for x, y in points[:5]:
            elements.append({
                "type": "vertex",
                "x": x,
                "y": y,
                "size": 10
            })
        
        # Add pentagram edges (connect every second point)
        for i in range(5):
            x1, y1 = points[i]
            x2, y2 = points[(i + 2) % 5]
            elements.append({
                "type": "edge",
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })
        
        return elements
    
    def _generate_hexagram(self, points: List[Tuple[int, int]]) -> List[Dict[str, Any]]:
        """Generate hexagram pattern elements"""
        if len(points) < 6:
            return []
            
        elements = []
        
        # Add vertices
        for x, y in points[:6]:
            elements.append({
                "type": "vertex",
                "x": x,
                "y": y,
                "size": 10
            })
        
        # Add first triangle
        for i in range(3):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % 3]
            elements.append({
                "type": "edge",
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })
        
        # Add second triangle
        for i in range(3):
            x1, y1 = points[i + 3]
            x2, y2 = points[(i + 1) % 3 + 3]
            elements.append({
                "type": "edge",
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })
        
        return elements 