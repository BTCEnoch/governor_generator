"""
Ritual mechanics engine implementation
"""

from typing import List, Dict, Optional, Any
from pydantic import ValidationError

from core.utils.custom_logging import setup_logger
from core.utils.mystical.bitcoin_integration import BitcoinIntegration
from .schemas import (
    RitualPoint,
    RitualPattern,
    ValidationResult,
    Direction
)

logger = setup_logger("ritual_engine")

class RitualEngine:
    """Engine for ritual mechanics"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the ritual engine"""
        self.config = config
        self.logger = setup_logger("ritual_engine")
        self.bitcoin = BitcoinIntegration()
        
        # Log initialization
        self.logger.info(
            f"Initialized RitualEngine with config: "
            f"min_power={config['min_power']} "
            f"max_power={config['max_power']} "
            f"resonance_threshold={config['resonance_threshold']} "
            f"governor_influence={config['governor_influence']} "
            f"ritual_points_required={config['ritual_points_required']}"
        )
    
    async def validate_ritual_points(
        self,
        points: List[Dict[str, Any]]
    ) -> ValidationResult:
        """Validate ritual points"""
        try:
            # Convert points to RitualPoint objects
            ritual_points = []
            for point in points:
                ritual_points.append(RitualPoint(**point))
            
            # Basic validation
            if len(ritual_points) < self.config["ritual_points_required"]:
                return ValidationResult(
                    is_valid=False,
                    data={"points": ritual_points},
                    errors=[f"Need at least {self.config['ritual_points_required']} points"]
                )
            
            # Check energy levels
            total_energy = sum(p.energy_level for p in ritual_points)
            if total_energy < self.config["min_power"]:
                return ValidationResult(
                    is_valid=False,
                    data={"points": ritual_points},
                    errors=[f"Total energy {total_energy} below minimum {self.config['min_power']}"]
                )
            
            # Check element balance
            elements = [p.element for p in ritual_points]
            if len(set(elements)) < 2:
                return ValidationResult(
                    is_valid=False,
                    data={"points": ritual_points},
                    errors=["Need at least 2 different elements"]
                )
            
            # Check governor influence
            governors = [p.governor_influence for p in ritual_points if p.governor_influence]
            if not governors:
                return ValidationResult(
                    is_valid=False,
                    data={"points": ritual_points},
                    errors=["Need at least one Governor influence"]
                )
            
            # Check Aethyr resonance
            aethyrs = set(p.aethyr_resonance for p in ritual_points)
            if len(aethyrs) > 1:
                return ValidationResult(
                    is_valid=False,
                    data={"points": ritual_points},
                    errors=["All points must resonate with the same Aethyr"]
                )
            
            # Success
            return ValidationResult(
                is_valid=True,
                data={"points": ritual_points},
                errors=[]
            )
            
        except ValidationError as e:
            self.logger.error(f"Point validation error: {str(e)}")
            return ValidationResult(
                is_valid=False,
                data={},
                errors=[f"Validation error: {str(e)}"]
            )
        except Exception as e:
            self.logger.error(f"Error validating ritual points: {str(e)}")
            return ValidationResult(
                is_valid=False,
                data={},
                errors=[f"Error: {str(e)}"]
            )
    
    async def match_ritual_pattern(
        self,
        points: List[RitualPoint]
    ) -> Optional[RitualPattern]:
        """Match ritual points to a pattern"""
        try:
            # Get Bitcoin entropy for pattern matching
            entropy = await self.bitcoin.get_entropy("pattern_matching")
            
            # Extract pattern data
            elements = [p.element for p in points]
            governors = [p.governor_influence for p in points if p.governor_influence]
            aethyrs = list(set(p.aethyr_resonance for p in points))
            total_energy = sum(p.energy_level for p in points)
            
            # Determine pattern type based on point arrangement
            if len(points) == 3:
                pattern_type = "triangle"
            elif len(points) == 4:
                pattern_type = "square"
            elif len(points) == 5:
                pattern_type = "pentagram"
            else:
                pattern_type = "complex"
            
            return RitualPattern(
                points=points,
                pattern_type=pattern_type,
                total_energy=total_energy,
                elements=elements,
                governors=governors,
                aethyrs=aethyrs,
                bitcoin_entropy=entropy
            )
            
        except Exception as e:
            self.logger.error(f"Error matching ritual pattern: {str(e)}")
            return None
    
    def get_ritual_direction(self, point: RitualPoint) -> Direction:
        """Get ritual direction from point coordinates"""
        x, y = point.x, point.y
        
        # Convert to polar coordinates
        angle = (y - 0.5) / (x - 0.5) if x != 0.5 else float('inf')
        
        # Map angle to direction
        if angle > 2.414:  # tan(67.5°)
            return Direction.NORTH if y > 0.5 else Direction.SOUTH
        elif angle > 0.414:  # tan(22.5°)
            return Direction.NORTHEAST if y > 0.5 else Direction.SOUTHWEST
        elif angle > -0.414:  # tan(-22.5°)
            return Direction.EAST if x > 0.5 else Direction.WEST
        elif angle > -2.414:  # tan(-67.5°)
            return Direction.SOUTHEAST if y < 0.5 else Direction.NORTHWEST
        else:
            return Direction.NORTH if y > 0.5 else Direction.SOUTH 