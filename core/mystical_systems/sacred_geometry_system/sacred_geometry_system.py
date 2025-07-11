"""
Sacred Geometry System Implementation with Bitcoin Integration
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple, cast, Any
from pydantic import ValidationError

from core.utils.mystical.base import (
    BitcoinMysticalSystem,
    MysticalAttribute,
    ValidationResult
)
from core.utils.mystical.bitcoin_integration import BitcoinIntegration
from core.utils.bitcoin.art_generation import BitcoinArtGenerator
from core.utils.custom_logging import setup_logger
from .schemas import (
    GeometricForm,
    GeometryPattern,
    SacredGeometryProfile,
    SacredGeometrySystemConfig,
    SacredProportion
)
from .data.geometry_database import get_form_data, get_proportion_data
import time

logger = setup_logger("sacred_geometry_system")

class SacredGeometrySystem(BitcoinMysticalSystem):
    """Bitcoin-integrated Sacred Geometry system implementation"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the Sacred Geometry system with Bitcoin integration"""
        if config is None:
            config = SacredGeometrySystemConfig(
                min_complexity=1,
                max_complexity=10,
                resonance_threshold=0.7,
                power_scale=1,  # Changed to int
                ritual_points_required=3
            ).model_dump()
        validated_config = SacredGeometrySystemConfig(**config)
        super().__init__(
            system_id="sacred_geometry",
            config=validated_config.model_dump()
        )
        
        self.bitcoin = BitcoinIntegration(config.get("bitcoin_integration"))
        self.art_generator = BitcoinArtGenerator()
        self.logger = logger
        self.logger.info("Initialized Bitcoin-integrated SacredGeometrySystem")

    def get_system_info(self) -> Dict[str, Any]:
        """Get information about the sacred geometry system"""
        return {
            "name": "Sacred Geometry System",
            "version": "1.0.0",
            "description": (
                "A Bitcoin-integrated sacred geometry system for generating "
                "mystical patterns and readings based on geometric forms and "
                "divine proportions."
            ),
            "capabilities": [
                "Geometric pattern generation",
                "Sacred proportion calculations",
                "Ritual point validation",
                "Bitcoin-based art generation",
                "Governor resonance analysis"
            ],
            "requirements": [
                "Bitcoin integration for entropy",
                "Art generation capabilities",
                "3D geometry support"
            ],
            "author": "Enochian Cyphers",
            "documentation_url": "https://docs.enochiancyphers.com/sacred_geometry"
        }

    def validate_input(self, input_data: Dict[str, Any]) -> ValidationResult:
        """Validate input data for sacred geometry operations"""
        try:
            validation_data = {"input": input_data}
            
            if "complexity" in input_data:
                complexity = input_data["complexity"]
                if not isinstance(complexity, int) or complexity < 1 or complexity > 10:
                    return ValidationResult(
                        data=validation_data,
                        is_valid=False,
                        errors=["Complexity must be an integer between 1 and 10"]
                    )
            
            if "form" in input_data:
                form = input_data["form"]
                if not isinstance(form, str) or form not in [f.value for f in GeometricForm]:
                    return ValidationResult(
                        data=validation_data,
                        is_valid=False,
                        errors=["Invalid geometric form specified"]
                    )
            
            return ValidationResult(data=validation_data, is_valid=True, errors=[])
            
        except Exception as e:
            return ValidationResult(
                data={"error": str(e)},
                is_valid=False,
                errors=[f"Validation error: {str(e)}"]
            )

    def format_output(self, output_data: Dict[str, Any] | SacredGeometryProfile) -> Dict[str, Any]:
        """Format sacred geometry output data"""
        try:
            if isinstance(output_data, SacredGeometryProfile):
                output_data = output_data.model_dump()
            
            # Add form descriptions
            if "primary_form" in output_data:
                form_data = get_form_data(output_data["primary_form"])
                output_data["primary_form_data"] = form_data
            
            if "secondary_forms" in output_data:
                secondary_data = []
                for form in output_data["secondary_forms"]:
                    form_data = get_form_data(form)
                    secondary_data.append(form_data)
                output_data["secondary_forms_data"] = secondary_data
            
            # Add proportion descriptions
            if "dominant_proportion" in output_data:
                prop_data = get_proportion_data(output_data["dominant_proportion"])
                output_data["dominant_proportion_data"] = prop_data
            
            return output_data
            
        except Exception as e:
            self.logger.error(f"Error formatting output: {str(e)}")
            return output_data if isinstance(output_data, dict) else {}

    def calculate_correspondences(self, profile: Dict[str, Any]) -> List[MysticalAttribute]:
        """Calculate mystical correspondences for a sacred geometry profile"""
        correspondences = []
        
        try:
            # Add form-based correspondences
            if "primary_form" in profile:
                form_data = get_form_data(profile["primary_form"])
                
                # Add elemental correspondences
                for element in form_data.get("elements", []):
                    correspondences.append(
                        MysticalAttribute(
                            name=f"element_{element.lower()}",
                            value=1.0,
                            description=f"Elemental correspondence: {element}"
                        )
                    )
                
                # Add symbolic correspondences
                for aspect in form_data.get("governor_aspects", []):
                    correspondences.append(
                        MysticalAttribute(
                            name=f"aspect_{aspect.lower().replace(' ', '_')}",
                            value=0.8,
                            description=f"Governor aspect: {aspect}"
                        )
                    )
            
            # Add proportion-based correspondences
            if "dominant_proportion" in profile:
                prop_data = get_proportion_data(profile["dominant_proportion"])
                
                for aspect in prop_data.get("governor_aspects", []):
                    correspondences.append(
                        MysticalAttribute(
                            name=f"proportion_{aspect.lower().replace(' ', '_')}",
                            value=0.9,
                            description=f"Sacred proportion aspect: {aspect}"
                        )
                    )
            
            # Add resonance-based correspondences
            if "resonance_score" in profile:
                correspondences.append(
                    MysticalAttribute(
                        name="geometric_resonance",
                        value=float(profile["resonance_score"]),
                        description="Overall geometric resonance score"
                    )
                )
            
            return correspondences
            
        except Exception as e:
            self.logger.error(f"Error calculating correspondences: {str(e)}")
            return []

    def _calculate_resonance(self, form: GeometricForm, block_hash: str) -> float:
        """Calculate resonance between geometric form and Bitcoin block hash"""
        # Use golden ratio (phi) based calculations for resonance
        phi = 1.618033988749895
        
        # Convert block hash to numerical value
        hash_value = int(block_hash, 16)
        
        # Calculate base resonance using phi-based modulo
        base_resonance = (hash_value % int(phi * 1e6)) / (phi * 1e6)
        
        # Adjust resonance based on form complexity
        form_complexity = {
            GeometricForm.POINT: 1,
            GeometricForm.LINE: 2,
            GeometricForm.TRIANGLE: 3,
            GeometricForm.SQUARE: 4,
            GeometricForm.PENTAGON: 5,
            GeometricForm.HEXAGON: 6,
            GeometricForm.CIRCLE: 7,
            GeometricForm.VESICA_PISCIS: 8,
            GeometricForm.SEED_OF_LIFE: 9,
            GeometricForm.FLOWER_OF_LIFE: 10,
            GeometricForm.METATRONS_CUBE: 11,
            GeometricForm.TETRAHEDRON: 12,
            GeometricForm.CUBE: 13,
            GeometricForm.OCTAHEDRON: 14,
            GeometricForm.DODECAHEDRON: 15,
            GeometricForm.ICOSAHEDRON: 16
        }
        
        complexity_factor = form_complexity[form] / 16
        resonance = (base_resonance + complexity_factor) / 2
        
        return min(1.0, max(0.0, resonance))

    def _generate_ritual_points(
        self, 
        form: GeometricForm,
        complexity: int,
        seed: str
    ) -> List[Dict[str, float]]:
        """Generate ritual interaction points for a geometric form"""
        points = []
        num_points = min(complexity * 2, 12)  # Max 12 points
        
        # Use Bitcoin entropy for point generation
        for i in range(num_points):
            x = self.bitcoin.generate_number(
                seed=f"{seed}_x_{i}",
                min_val=-100,
                max_val=100
            ) / 100.0
            
            y = self.bitcoin.generate_number(
                seed=f"{seed}_y_{i}",
                min_val=-100,
                max_val=100
            ) / 100.0
            
            z = self.bitcoin.generate_number(
                seed=f"{seed}_z_{i}",
                min_val=-100,
                max_val=100
            ) / 100.0 if complexity > 5 else 0.0
            
            points.append({"x": x, "y": y, "z": z})
        
        return points

    def _generate_pattern(
        self,
        form: GeometricForm,
        block_hash: str,
        complexity: int
    ) -> GeometryPattern:
        """Generate a sacred geometry pattern"""
        # Calculate resonance
        resonance = self._calculate_resonance(form, block_hash)
        
        # Determine dimensions based on form
        dimensions = 2 if form in [
            GeometricForm.POINT,
            GeometricForm.LINE,
            GeometricForm.TRIANGLE,
            GeometricForm.SQUARE,
            GeometricForm.PENTAGON,
            GeometricForm.HEXAGON,
            GeometricForm.CIRCLE,
            GeometricForm.VESICA_PISCIS,
            GeometricForm.SEED_OF_LIFE,
            GeometricForm.FLOWER_OF_LIFE,
            GeometricForm.METATRONS_CUBE
        ] else 3
        
        # Generate ritual points
        ritual_points = self._generate_ritual_points(
            form,
            complexity,
            block_hash
        )
        
        # Calculate power level based on complexity and resonance
        power_level = int(((complexity / 10) + resonance) * 50)
        
        # Determine symmetry order based on form
        symmetry_order = {
            GeometricForm.POINT: 1,
            GeometricForm.LINE: 2,
            GeometricForm.TRIANGLE: 3,
            GeometricForm.SQUARE: 4,
            GeometricForm.PENTAGON: 5,
            GeometricForm.HEXAGON: 6,
            GeometricForm.CIRCLE: 1,
            GeometricForm.VESICA_PISCIS: 2,
            GeometricForm.SEED_OF_LIFE: 6,
            GeometricForm.FLOWER_OF_LIFE: 6,
            GeometricForm.METATRONS_CUBE: 12,
            GeometricForm.TETRAHEDRON: 4,
            GeometricForm.CUBE: 4,
            GeometricForm.OCTAHEDRON: 8,
            GeometricForm.DODECAHEDRON: 12,
            GeometricForm.ICOSAHEDRON: 20
        }[form]
        
        # Select proportions based on form and complexity
        proportions = [SacredProportion.PHI]  # Always include phi
        if complexity > 3:
            proportions.append(SacredProportion.PI)
        if complexity > 5:
            proportions.append(SacredProportion.SQRT2)
        if complexity > 7:
            proportions.append(SacredProportion.SQRT3)
        if complexity > 9:
            proportions.append(SacredProportion.SQRT5)
            
        return GeometryPattern(
            form=form,
            proportions=proportions,
            complexity=complexity,
            dimensions=dimensions,
            symmetry_order=symmetry_order,
            ritual_points=ritual_points,
            power_level=power_level,
            resonance=resonance
        )

    async def generate_profile(
        self,
        txid: Optional[str] = None,
        complexity: Optional[int] = None
    ) -> SacredGeometryProfile:
        """Generate a complete sacred geometry profile"""
        # Get Bitcoin block hash from txid entropy
        block_hash = self.bitcoin.derive_randomness(txid if txid else str(time.time())).hex()
        
        # Use validated complexity or config default
        validated_complexity = min(
            max(
                complexity or self.config["min_complexity"],
                self.config["min_complexity"]
            ),
            self.config["max_complexity"]
        )
        
        # Select primary form using Bitcoin entropy
        primary_idx = self.bitcoin.generate_number(
            seed=f"{block_hash}_primary",
            min_val=0,
            max_val=len(GeometricForm) - 1
        )
        primary_form = list(GeometricForm)[primary_idx]
        
        # Generate 2-3 secondary forms
        num_secondary = validated_complexity // 4 + 2  # 2-3 based on complexity
        secondary_forms = []
        for i in range(num_secondary):
            idx = self.bitcoin.generate_number(
                seed=f"{block_hash}_secondary_{i}",
                min_val=0,
                max_val=len(GeometricForm) - 1
            )
            form = list(GeometricForm)[idx]
            if form != primary_form and form not in secondary_forms:
                secondary_forms.append(form)
        
        # Generate patterns for primary and secondary forms
        patterns = [
            self._generate_pattern(
                primary_form,
                block_hash,
                validated_complexity
            )
        ]
        for form in secondary_forms:
            patterns.append(
                self._generate_pattern(
                    form,
                    block_hash,
                    max(1, validated_complexity - 2)
                )
            )
        
        # Calculate overall resonance score
        resonance_score = sum(p.resonance for p in patterns) / len(patterns)
        
        # Select dominant proportion based on resonance
        proportion_idx = self.bitcoin.generate_number(
            seed=f"{block_hash}_proportion",
            min_val=0,
            max_val=len(SacredProportion) - 1
        )
        dominant_proportion = list(SacredProportion)[proportion_idx]
        
        # Generate power centers (1-3 based on complexity)
        num_centers = validated_complexity // 4 + 1
        power_centers = self._generate_ritual_points(
            primary_form,
            num_centers,
            f"{block_hash}_power"
        )
        
        # Calculate governor alignment
        governor_alignment = resonance_score * (validated_complexity / 10)
        
        return SacredGeometryProfile(
            primary_form=primary_form,
            secondary_forms=secondary_forms,
            patterns=patterns,
            dominant_proportion=dominant_proportion,
            power_centers=power_centers,
            resonance_score=resonance_score,
            ritual_complexity=validated_complexity,
            governor_alignment=governor_alignment,
            timestamp=datetime.utcnow().isoformat(),
            bitcoin_block_hash=block_hash
        )

    async def generate_art(
        self,
        profile: SacredGeometryProfile,
        output_path: str
    ) -> str:
        """Generate visual art representation of the sacred geometry profile"""
        try:
            # Extract points and energy levels from the profile
            points = [(p["x"], p["y"]) for p in profile.patterns[0].ritual_points]
            energy_levels = [p.get("energy", 0.5) for p in profile.patterns[0].ritual_points]
            
            return await self.art_generator.generate_ritual_art(
                points=points,
                energy_levels=energy_levels,
                pattern_type=profile.primary_form.lower(),
                output_path=output_path,
                entropy=profile.bitcoin_block_hash
            )
        except Exception as e:
            self.logger.error(f"Art generation failed: {e}")
            return ""

    def validate_ritual_pattern(
        self,
        points: List[Dict[str, float]],
        target_pattern: GeometryPattern
    ) -> bool:
        """Validate if given points match the required ritual pattern"""
        if len(points) != len(target_pattern.ritual_points):
            return False
            
        # Calculate tolerance based on complexity
        tolerance = 0.1 * (11 - target_pattern.complexity)
        
        # Check each point is within tolerance of a target point
        matched_targets = set()
        for point in points:
            found_match = False
            for i, target in enumerate(target_pattern.ritual_points):
                if i in matched_targets:
                    continue
                    
                # Calculate distance
                dist = sum(
                    (point.get(k, 0) - target.get(k, 0)) ** 2 
                    for k in ['x', 'y', 'z']
                ) ** 0.5
                
                if dist <= tolerance:
                    matched_targets.add(i)
                    found_match = True
                    break
                    
            if not found_match:
                return False
                
        return True 