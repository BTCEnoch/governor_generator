"""
Enochian Governor relationship engine implementation
"""

from typing import Dict, List, Optional, Any, Tuple, Iterable
from datetime import datetime
import math
import json
import os
import hashlib
import shutil
import time
import itertools

from core.utils.mystical.bitcoin_integration import BitcoinIntegration
from core.utils.custom_logging import setup_logger

from ..schemas import EnochianSystemConfig, AethyrProfile
from .schemas import (
    ConnectionType,
    ResonanceType,
    InteractionType,
    GovernorConnection,
    ResonancePattern,
    InteractionRule,
    RelationshipVisualization,
    RelationshipProfile,
    RelationshipVisualizationNode,
    RelationshipVisualizationCluster,
    ValidationResult,
    VisualProperties,
    ColorRGB,
    GlowEffect,
    BorderStyle,
    ShapeProperties
)
from .utils import calculate_node_power, calculate_coordinates

logger = setup_logger("relationship_engine")

class RelationshipEngine:
    """Engine for processing Enochian Governor relationships"""
    
    def __init__(
        self,
        config: EnochianSystemConfig,
        bitcoin_integration: Optional[BitcoinIntegration] = None
    ):
        """Initialize the relationship engine"""
        self.config = config
        self.bitcoin_integration = bitcoin_integration or BitcoinIntegration()
        self.logger = logger
        
        # Create cache directory if it doesn't exist
        os.makedirs(os.path.join(config.output_dir, "visualization_cache"), exist_ok=True)
        
        self.logger.info("Initialized RelationshipEngine with config: %s", config)
    
    def validate_connection(
        self,
        connection: GovernorConnection
    ) -> ValidationResult:
        """Validate a Governor connection"""
        try:
            validation_data = {"connection": connection}
            errors = []
            
            # Check that governors are different
            if connection.source_governor == connection.target_governor:
                errors.append("Source and target governors must be different")
            
            # Validate strength range
            if not 0 <= connection.strength <= 1:
                errors.append("Connection strength must be between 0 and 1")
            
            # Validate shared attributes
            if len(connection.shared_attributes) == 0:
                errors.append("Must have at least one shared attribute")
            
            return ValidationResult(
                data=validation_data,
                is_valid=len(errors) == 0,
                errors=errors if errors else []
            )
            
        except Exception as e:
            self.logger.error("Connection validation error: %s", str(e))
            return ValidationResult(
                data={"error": str(e)},
                is_valid=False,
                errors=[f"Validation error: {str(e)}"]
            )
    
    def validate_resonance_pattern(
        self,
        pattern: ResonancePattern
    ) -> ValidationResult:
        """Validate a resonance pattern"""
        try:
            validation_data = {"pattern": pattern}
            errors = []
            
            # Check minimum governors
            if len(pattern.governors) < 2:
                errors.append("Pattern must involve at least 2 governors")
            
            # Check for duplicate governors
            if len(set(pattern.governors)) != len(pattern.governors):
                errors.append("Pattern contains duplicate governors")
            
            # Validate intensity range
            if not 0 <= pattern.intensity <= 1:
                errors.append("Pattern intensity must be between 0 and 1")
            
            return ValidationResult(
                data=validation_data,
                is_valid=len(errors) == 0,
                errors=errors if errors else []
            )
            
        except Exception as e:
            self.logger.error("Pattern validation error: %s", str(e))
            return ValidationResult(
                data={"error": str(e)},
                is_valid=False,
                errors=[f"Validation error: {str(e)}"]
            )

    def validate_resonance_combinations(
        self,
        patterns: List[ResonancePattern]
    ) -> ValidationResult:
        """Validate resonance pattern combinations for conflicts and balance"""
        try:
            validation_data = {"patterns": patterns}
            
            # Count pattern types
            type_counts = {
                ResonanceType.HARMONIC: 0,
                ResonanceType.AMPLIFYING: 0,
                ResonanceType.NEUTRAL: 0,
                ResonanceType.DAMPENING: 0,
                ResonanceType.DISSONANT: 0
            }
            
            # Track governor participation
            governor_patterns = {}
            
            for pattern in patterns:
                # Count pattern types
                type_counts[pattern.pattern_type] += 1
                
                # Track patterns per governor
                for governor in pattern.governors:
                    if governor not in governor_patterns:
                        governor_patterns[governor] = []
                    governor_patterns[governor].append(pattern)
            
            # Check pattern type balance
            total_patterns = len(patterns)
            if total_patterns > 0:
                # No single type should dominate (max 40%)
                for count in type_counts.values():
                    if count / total_patterns > 0.4:
                        return ValidationResult(
                            data=validation_data,
                            is_valid=False,
                            errors=["One resonance type is too dominant (>40%)"]
                        )
                
                # Should have some neutral patterns (10-30%)
                neutral_ratio = type_counts[ResonanceType.NEUTRAL] / total_patterns
                if not (0.1 <= neutral_ratio <= 0.3):
                    return ValidationResult(
                        data=validation_data,
                        is_valid=False,
                        errors=["Neutral pattern ratio outside acceptable range (10-30%)"]
                    )
            
            # Check governor pattern conflicts
            for governor, gov_patterns in governor_patterns.items():
                # Check for too many patterns per governor (max 5)
                if len(gov_patterns) > 5:
                    return ValidationResult(
                        data=validation_data,
                        is_valid=False,
                        errors=[f"Governor {governor} involved in too many patterns (>5)"]
                    )
                
                # Check for conflicting pattern types
                harmonic_patterns = [p for p in gov_patterns if p.pattern_type == ResonanceType.HARMONIC]
                dissonant_patterns = [p for p in gov_patterns if p.pattern_type == ResonanceType.DISSONANT]
                
                # Can't have both strong harmonic and dissonant patterns
                if harmonic_patterns and dissonant_patterns:
                    strong_harmonic = any(p.intensity > 0.7 for p in harmonic_patterns)
                    strong_dissonant = any(p.intensity > 0.7 for p in dissonant_patterns)
                    if strong_harmonic and strong_dissonant:
                        return ValidationResult(
                            data=validation_data,
                            is_valid=False,
                            errors=[f"Governor {governor} has conflicting strong harmonic and dissonant patterns"]
                        )
            
            return ValidationResult(
                data=validation_data,
                is_valid=True,
                errors=[]
            )
            
        except Exception as e:
            self.logger.error("Error validating resonance combinations: %s", str(e))
            return ValidationResult(
                data={"error": str(e)},
                is_valid=False,
                errors=[f"Error validating resonance combinations: {str(e)}"]
            )

    def validate_rule_conflicts(
        self,
        rules: List[InteractionRule]
    ) -> ValidationResult:
        """Validate interaction rules for conflicts and consistency"""
        try:
            validation_data = {"rules": rules}
            
            # Group rules by type
            rules_by_type = {}
            for rule in rules:
                if rule.rule_type not in rules_by_type:
                    rules_by_type[rule.rule_type] = []
                rules_by_type[rule.rule_type].append(rule)
            
            # Check priority distribution
            all_priorities = [rule.priority for rule in rules]
            if len(set(all_priorities)) != len(all_priorities):
                return ValidationResult(
                    data=validation_data,
                    is_valid=False,
                    errors=["Duplicate priorities found"]
                )
            
            # Check rule type balance
            total_rules = len(rules)
            if total_rules > 0:
                for rule_type, type_rules in rules_by_type.items():
                    # No single type should dominate (max 40%)
                    if len(type_rules) / total_rules > 0.4:
                        return ValidationResult(
                            data=validation_data,
                            is_valid=False,
                            errors=[f"Rule type {rule_type} is too dominant (>40%)"]
                        )
            
            # Check for conflicting effects
            for rule_type, type_rules in rules_by_type.items():
                for i, rule1 in enumerate(type_rules):
                    for rule2 in type_rules[i+1:]:
                        # Check for overlapping conditions but different effects
                        shared_conditions = set(rule1.conditions.keys()) & set(rule2.conditions.keys())
                        shared_effects = set(rule1.effects.keys()) & set(rule2.effects.keys())
                        
                        if shared_conditions and shared_effects:
                            # Check for significantly different effect values
                            for effect in shared_effects:
                                if abs(rule1.effects[effect] - rule2.effects[effect]) > 0.5:
                                    return ValidationResult(
                                        data=validation_data,
                                        is_valid=False,
                                        errors=[f"Conflicting effects found in {rule_type} rules"]
                                    )
            
            # Check for logical conflicts between rule types
            if (InteractionType.TEACHING in rules_by_type and
                InteractionType.OPPOSITION in rules_by_type):
                # Teaching and Opposition rules should not target same conditions
                teaching_rules = rules_by_type[InteractionType.TEACHING]
                opposition_rules = rules_by_type[InteractionType.OPPOSITION]
                
                for t_rule in teaching_rules:
                    for o_rule in opposition_rules:
                        shared_conditions = set(t_rule.conditions.keys()) & set(o_rule.conditions.keys())
                        if shared_conditions:
                            return ValidationResult(
                                data=validation_data,
                                is_valid=False,
                                errors=["Teaching and Opposition rules have conflicting conditions"]
                            )
            
            return ValidationResult(
                data=validation_data,
                is_valid=True,
                errors=[]
            )
            
        except Exception as e:
            self.logger.error("Error validating rule conflicts: %s", str(e))
            return ValidationResult(
                data={"error": str(e)},
                is_valid=False,
                errors=[f"Error validating rule conflicts: {str(e)}"]
            )

    def validate_visualization_constraints(
        self,
        visualization: RelationshipVisualization
    ) -> ValidationResult:
        """Validate visualization constraints for proper spacing and balance"""
        try:
            # Helper function to calculate distance between nodes
            def calculate_distance(node1: RelationshipVisualizationNode, node2: RelationshipVisualizationNode) -> float:
                return math.sqrt(
                    (node1.x - node2.x) ** 2 +
                    (node1.y - node2.y) ** 2 +
                    (node1.z - node2.z) ** 2
                )
            
            # Check node spacing
            min_distance = 0.1  # Minimum distance between nodes
            for i, node1 in enumerate(visualization.nodes):
                for node2 in visualization.nodes[i+1:]:
                    distance = calculate_distance(node1, node2)
                    if distance < min_distance:
                        return ValidationResult(
                            is_valid=False,
                            message=f"Nodes {node1.governor} and {node2.governor} are too close (distance: {distance:.2f})"
                        )
            
            # Check node power distribution
            powers = [node.power for node in visualization.nodes]
            avg_power = sum(powers) / len(powers)
            power_variance = sum((p - avg_power) ** 2 for p in powers) / len(powers)
            
            if power_variance > 0.25:  # Max allowed variance
                return ValidationResult(
                    is_valid=False,
                    message="Node power distribution is too uneven"
                )
            
            # Check edge weight distribution
            if visualization.edges:
                weights = [edge["weight"] for edge in visualization.edges]
                avg_weight = sum(weights) / len(weights)
                weight_variance = sum((w - avg_weight) ** 2 for w in weights) / len(weights)
                
                if weight_variance > 0.25:  # Max allowed variance
                    return ValidationResult(
                        is_valid=False,
                        message="Edge weight distribution is too uneven"
                    )
            
            # Check cluster overlap
            if visualization.clusters:
                for i, cluster1 in enumerate(visualization.clusters):
                    for cluster2 in visualization.clusters[i+1:]:
                        # Check for overlapping governors
                        overlap = set(cluster1.governors) & set(cluster2.governors)
                        if len(overlap) > len(cluster1.governors) * 0.5:  # Max 50% overlap
                            return ValidationResult(
                                is_valid=False,
                                message=f"Clusters have too much overlap ({len(overlap)} governors)"
                            )
                        
                        # Check intensity balance for overlapping clusters
                        if overlap and abs(cluster1.intensity - cluster2.intensity) > 0.5:
                            return ValidationResult(
                                is_valid=False,
                                message="Overlapping clusters have too different intensities"
                            )
            
            # Check spatial balance
            x_coords = [node.x for node in visualization.nodes]
            y_coords = [node.y for node in visualization.nodes]
            z_coords = [node.z for node in visualization.nodes]
            
            # Calculate center of mass
            center_x = sum(x_coords) / len(x_coords)
            center_y = sum(y_coords) / len(y_coords)
            center_z = sum(z_coords) / len(z_coords)
            
            # Check if center of mass is close to origin
            if abs(center_x) > 0.1 or abs(center_y) > 0.1 or abs(center_z) > 0.1:
                return ValidationResult(
                    is_valid=False,
                    message="Visualization is not well-centered"
                )
            
            # Check spatial distribution
            x_variance = sum((x - center_x) ** 2 for x in x_coords) / len(x_coords)
            y_variance = sum((y - center_y) ** 2 for y in y_coords) / len(y_coords)
            z_variance = sum((z - center_z) ** 2 for z in z_coords) / len(z_coords)
            
            # Variances should be similar for balanced distribution
            max_variance_ratio = max(x_variance, y_variance, z_variance) / min(x_variance, y_variance, z_variance)
            if max_variance_ratio > 2:  # Max allowed ratio
                return ValidationResult(
                    is_valid=False,
                    message="Spatial distribution is too uneven"
                )
            
            return ValidationResult(
                is_valid=True,
                message="Visualization constraints are valid"
            )
            
        except Exception as e:
            self.logger.error("Error validating visualization constraints: %s", str(e))
            return ValidationResult(
                is_valid=False,
                message=f"Error validating visualization constraints: {str(e)}"
            )

    def validate_visualization_aesthetics(
        self,
        visualization: RelationshipVisualization,
        clusters: List[RelationshipVisualizationCluster]
    ) -> ValidationResult:
        """Validate visualization aesthetics and color harmony"""
        try:
            validation_data = {
                "visualization": visualization,
                "clusters": clusters
            }
            errors = []
            
            # Helper function to calculate color distance
            def color_distance(c1: ColorRGB, c2: ColorRGB) -> float:
                return math.sqrt(
                    (c1.r - c2.r) ** 2 +
                    (c1.g - c2.g) ** 2 +
                    (c1.b - c2.b) ** 2
                )
            
            # Helper function to calculate color harmony
            def check_color_harmony(colors: List[ColorRGB]) -> bool:
                if not colors:
                    return True
                
                # Calculate average distance between colors
                distances = []
                for i, c1 in enumerate(colors[:-1]):
                    for c2 in colors[i+1:]:
                        distances.append(color_distance(c1, c2))
                
                if not distances:
                    return True
                
                avg_distance = sum(distances) / len(distances)
                return avg_distance >= 50  # Min distance for good contrast
            
            # Check node distribution
            node_positions = [(node.x, node.y, node.z) for node in visualization.nodes]
            if node_positions:
                # Calculate average distance between nodes
                distances = []
                for i, pos1 in enumerate(node_positions[:-1]):
                    for pos2 in node_positions[i+1:]:
                        dist = math.sqrt(
                            (pos1[0] - pos2[0]) ** 2 +
                            (pos1[1] - pos2[1]) ** 2 +
                            (pos1[2] - pos2[2]) ** 2
                        )
                        distances.append(dist)
                
                if distances:
                    avg_distance = sum(distances) / len(distances)
                    min_distance = min(distances)
                    
                    if min_distance < 0.1:
                        errors.append("Nodes too close together")
                    if avg_distance < 0.3:
                        errors.append("Poor node distribution")
            
            # Check edge weight distribution
            edge_weights = [edge["weight"] for edge in visualization.edges]
            if edge_weights:
                weight_range = max(edge_weights) - min(edge_weights)
                if weight_range < 0.3:
                    errors.append("Insufficient edge weight variation")
            
            # Check cluster colors
            cluster_colors = []
            for cluster in clusters:
                if cluster.visuals and cluster.visuals.color:
                    cluster_colors.append(cluster.visuals.color)
            
            if not check_color_harmony(cluster_colors):
                errors.append("Poor color harmony between clusters")
            
            # Check cluster overlap
            for i, c1 in enumerate(clusters[:-1]):
                for j, c2 in enumerate(clusters[i+1:], i+1):
                    shared_governors = set(c1.governors) & set(c2.governors)
                    if shared_governors:
                        # Check visual distinction
                        if (
                            c1.visuals and c2.visuals and
                            c1.visuals.color and c2.visuals.color
                        ):
                            color_dist = color_distance(
                                c1.visuals.color,
                                c2.visuals.color
                            )
                            if color_dist < 30:  # Min distance for overlapping clusters
                                errors.append(
                                    f"Insufficient visual distinction between overlapping clusters {i} and {j}"
                                )
            
            # Check glow effects
            glow_intensities = []
            for cluster in clusters:
                if cluster.visuals and cluster.visuals.glow:
                    glow_intensities.append(cluster.visuals.glow.intensity)
            
            if glow_intensities:
                intensity_range = max(glow_intensities) - min(glow_intensities)
                if intensity_range < 0.2:
                    errors.append("Insufficient glow intensity variation")
            
            # Check border styles
            border_widths = []
            for cluster in clusters:
                if cluster.visuals and cluster.visuals.border:
                    border_widths.append(cluster.visuals.border.width)
            
            if border_widths:
                width_range = max(border_widths) - min(border_widths)
                if width_range < 0.5:
                    errors.append("Insufficient border width variation")
            
            # Check shape distribution
            shape_counts = {}
            for cluster in clusters:
                if cluster.visuals and cluster.visuals.shape:
                    shape_type = cluster.visuals.shape.type
                    shape_counts[shape_type] = shape_counts.get(shape_type, 0) + 1
            
            if shape_counts:
                max_shape_ratio = max(shape_counts.values()) / len(clusters)
                if max_shape_ratio > 0.7:  # Max 70% same shape
                    errors.append("Excessive use of same cluster shape")
            
            is_valid = len(errors) == 0
            self.logger.info(
                "Visualization aesthetics validation %s: %d errors",
                "passed" if is_valid else "failed",
                len(errors)
            )
            
            return ValidationResult(
                data=validation_data,
                is_valid=is_valid,
                errors=errors
            )
            
        except Exception as e:
            self.logger.error("Error validating visualization aesthetics: %s", str(e))
            return ValidationResult(
                data={"error": str(e)},
                is_valid=False,
                errors=[f"Validation error: {str(e)}"]
            )

    async def generate_connection(
        self,
        source_governor: str,
        target_governor: str,
        shared_attributes: List[str]
    ) -> GovernorConnection:
        """Generate a connection between two Governors"""
        try:
            # Get Bitcoin entropy for connection
            entropy = await self.bitcoin_integration.get_entropy(
                f"{source_governor}_{target_governor}"
            )
            
            # Determine connection type based on shared attributes
            if any(attr.startswith("aethyr_") for attr in shared_attributes):
                conn_type = ConnectionType.AETHYRIC
            elif any(attr.startswith("element_") for attr in shared_attributes):
                conn_type = ConnectionType.ELEMENTAL
            elif any(attr.startswith("resonance_") for attr in shared_attributes):
                conn_type = ConnectionType.RESONANT
            elif any(attr.startswith("complement_") for attr in shared_attributes):
                conn_type = ConnectionType.COMPLEMENTARY
            else:
                conn_type = ConnectionType.DIRECT
            
            # Calculate connection strength
            base_strength = len(shared_attributes) / 10  # 10 is max expected attributes
            entropy_factor = int(entropy[:8], 16) / (2**32)  # Convert first 8 hex chars to 0-1
            strength = min(1.0, (base_strength + entropy_factor) / 2)
            
            connection = GovernorConnection(
                source_governor=source_governor,
                target_governor=target_governor,
                connection_type=conn_type,
                strength=strength,
                shared_attributes=shared_attributes,
                bitcoin_verification=entropy
            )
            
            # Validate the connection
            validation = self.validate_connection(connection)
            if not validation.is_valid:
                raise ValueError(f"Invalid connection: {validation.errors}")
            
            return connection
            
        except Exception as e:
            self.logger.error(
                "Error generating connection between %s and %s: %s",
                source_governor, target_governor, str(e)
            )
            raise

    async def calculate_resonance(
        self,
        governors: List[str],
        aethyrs: List[AethyrProfile]
    ) -> ResonancePattern:
        """Calculate resonance pattern between Governors"""
        try:
            # Get Bitcoin entropy for resonance calculation
            entropy = await self.bitcoin_integration.get_entropy(
                "_".join(sorted(governors))  # Sort for consistency
            )
            
            # Convert entropy to float factors (0-1)
            entropy_bytes = bytes.fromhex(entropy)
            pattern_factor = int(entropy_bytes[:4].hex(), 16) / (2**32)
            intensity_factor = int(entropy_bytes[4:8].hex(), 16) / (2**32)
            type_factor = int(entropy_bytes[8:12].hex(), 16) / (2**32)
            
            # Calculate base intensity from shared Aethyrs
            shared_aethyrs = [
                aethyr for aethyr in aethyrs
                if all(gov in aethyr.governors for gov in governors)
            ]
            
            base_intensity = len(shared_aethyrs) / len(aethyrs) if aethyrs else 0
            
            # Calculate ritual alignment
            ritual_matches = 0
            total_rituals = 0
            for aethyr in shared_aethyrs:
                total_rituals += len(aethyr.ritual_requirements)
                for ritual in aethyr.ritual_requirements:
                    # Check if all governors can perform the ritual
                    if all(
                        any(ritual in a.ritual_requirements for a in aethyrs if gov in a.governors)
                        for gov in governors
                    ):
                        ritual_matches += 1
            
            ritual_alignment = ritual_matches / max(total_rituals, 1)
            
            # Calculate resonance type based on ritual alignment and entropy
            type_threshold = type_factor * ritual_alignment
            if type_threshold > 0.8:
                pattern_type = ResonanceType.HARMONIC
            elif type_threshold > 0.6:
                pattern_type = ResonanceType.AMPLIFYING
            elif type_threshold > 0.4:
                pattern_type = ResonanceType.NEUTRAL
            elif type_threshold > 0.2:
                pattern_type = ResonanceType.DAMPENING
            else:
                pattern_type = ResonanceType.DISSONANT
            
            # Calculate final intensity with entropy factors
            intensity = min(1.0, (
                base_intensity * 0.4 +  # Base from shared Aethyrs
                ritual_alignment * 0.3 +  # Ritual compatibility
                pattern_factor * 0.2 +  # Random factor from Bitcoin
                intensity_factor * 0.1  # Additional entropy influence
            ))
            
            # Create the pattern
            pattern = ResonancePattern(
                governors=governors,
                pattern_type=pattern_type,
                intensity=intensity,
                bitcoin_entropy=entropy
            )
            
            # Validate the pattern
            validation = self.validate_resonance_pattern(pattern)
            if not validation.is_valid:
                raise ValueError(f"Invalid resonance pattern: {validation.errors}")
            
            self.logger.info(
                "Calculated resonance pattern: type=%s, intensity=%.2f, governors=%s",
                pattern_type, intensity, governors
            )
            
            return pattern
            
        except Exception as e:
            self.logger.error("Error calculating resonance: %s", str(e))
            raise

    def create_interaction_rule(
        self,
        rule_type: InteractionType,
        conditions: Dict[str, float],
        effects: Dict[str, float],
        priority: int,
        description: str
    ) -> InteractionRule:
        """Create an interaction rule between Governors"""
        try:
            # Validate rule type
            if rule_type not in InteractionType.__members__.values():
                raise ValueError(f"Invalid interaction type: {rule_type}")
            
            # Validate priority range
            if not 1 <= priority <= 10:
                raise ValueError("Priority must be between 1 and 10")
            
            # Validate conditions
            required_conditions = {
                InteractionType.TEACHING: ["reputation", "knowledge_level"],
                InteractionType.EMPOWERMENT: ["energy_level", "resonance"],
                InteractionType.TRANSFORMATION: ["connection_strength", "pattern_intensity"],
                InteractionType.OPPOSITION: ["dissonance", "conflict_level"],
                InteractionType.SYNTHESIS: ["harmony", "synchronization"]
            }
            
            missing_conditions = set(required_conditions[rule_type]) - set(conditions.keys())
            if missing_conditions:
                raise ValueError(f"Missing required conditions for {rule_type}: {missing_conditions}")
            
            # Validate effects
            required_effects = {
                InteractionType.TEACHING: ["knowledge_gain", "reputation_change"],
                InteractionType.EMPOWERMENT: ["energy_boost", "power_increase"],
                InteractionType.TRANSFORMATION: ["mutation_factor", "evolution_rate"],
                InteractionType.OPPOSITION: ["challenge_level", "breakthrough_chance"],
                InteractionType.SYNTHESIS: ["synergy_level", "pattern_stability"]
            }
            
            missing_effects = set(required_effects[rule_type]) - set(effects.keys())
            if missing_effects:
                raise ValueError(f"Missing required effects for {rule_type}: {missing_effects}")
            
            # Validate value ranges
            for value in conditions.values():
                if not 0 <= value <= 1:
                    raise ValueError("Condition values must be between 0 and 1")
            
            for value in effects.values():
                if not 0 <= value <= 1:
                    raise ValueError("Effect values must be between 0 and 1")
            
            # Create the rule
            rule = InteractionRule(
                rule_type=rule_type,
                conditions=conditions,
                effects=effects,
                priority=priority,
                description=description
            )
            
            self.logger.info(
                "Created interaction rule: %s (priority %d)",
                rule_type, priority
            )
            
            return rule
            
        except Exception as e:
            self.logger.error("Error creating interaction rule: %s", str(e))
            raise

    def apply_interaction_rules(
        self,
        connections: List[GovernorConnection],
        patterns: List[ResonancePattern]
    ) -> List[InteractionRule]:
        """Apply interaction rules to connections and patterns"""
        try:
            active_rules = []
            
            # Helper function to check if conditions are met
            def check_conditions(rule: InteractionRule, conn: GovernorConnection, pattern: Optional[ResonancePattern]) -> bool:
                # Check connection-based conditions
                if "connection_strength" in rule.conditions:
                    if conn.strength < rule.conditions["connection_strength"]:
                        return False
                
                # Check pattern-based conditions
                if pattern and "pattern_intensity" in rule.conditions:
                    if pattern.intensity < rule.conditions["pattern_intensity"]:
                        return False
                
                # Check resonance conditions
                if pattern and "resonance" in rule.conditions:
                    if pattern.pattern_type == ResonanceType.HARMONIC:
                        resonance = 1.0
                    elif pattern.pattern_type == ResonanceType.AMPLIFYING:
                        resonance = 0.8
                    elif pattern.pattern_type == ResonanceType.NEUTRAL:
                        resonance = 0.5
                    elif pattern.pattern_type == ResonanceType.DAMPENING:
                        resonance = 0.3
                    else:  # DISSONANT
                        resonance = 0.1
                        
                    if resonance < rule.conditions["resonance"]:
                        return False
                
                # Check dissonance conditions
                if pattern and "dissonance" in rule.conditions:
                    if pattern.pattern_type == ResonanceType.DISSONANT:
                        dissonance = 1.0
                    elif pattern.pattern_type == ResonanceType.DAMPENING:
                        dissonance = 0.7
                    elif pattern.pattern_type == ResonanceType.NEUTRAL:
                        dissonance = 0.5
                    elif pattern.pattern_type == ResonanceType.AMPLIFYING:
                        dissonance = 0.2
                    else:  # HARMONIC
                        dissonance = 0.0
                        
                    if dissonance < rule.conditions["dissonance"]:
                        return False
                
                return True
            
            # Helper function to resolve rule conflicts
            def resolve_conflicts(rules: List[InteractionRule]) -> List[InteractionRule]:
                # Sort by priority (higher first)
                sorted_rules = sorted(rules, key=lambda r: r.priority, reverse=True)
                
                # Group by rule type
                rule_groups: Dict[InteractionType, List[InteractionRule]] = {}
                for rule in sorted_rules:
                    if rule.rule_type not in rule_groups:
                        rule_groups[rule.rule_type] = []
                    rule_groups[rule.rule_type].append(rule)
                
                # Keep only the highest priority rule of each type
                resolved_rules = []
                for rules_of_type in rule_groups.values():
                    resolved_rules.append(rules_of_type[0])  # First rule has highest priority
                
                return resolved_rules
            
            # Process each connection
            for conn in connections:
                # Find matching pattern for this connection
                matching_pattern = next(
                    (p for p in patterns if conn.source_governor in p.governors and conn.target_governor in p.governors),
                    None
                )
                
                # Create teaching rules for strong connections
                if conn.strength >= 0.8:
                    teaching_rule = self.create_interaction_rule(
                        rule_type=InteractionType.TEACHING,
                        conditions={
                            "reputation": 0.6,
                            "knowledge_level": 0.4
                        },
                        effects={
                            "knowledge_gain": conn.strength,
                            "reputation_change": 0.1
                        },
                        priority=8,
                        description=f"Teaching interaction between {conn.source_governor} and {conn.target_governor}"
                    )
                    active_rules.append(teaching_rule)
                
                # Create empowerment rules for resonant patterns
                if matching_pattern and matching_pattern.pattern_type in [ResonanceType.HARMONIC, ResonanceType.AMPLIFYING]:
                    empowerment_rule = self.create_interaction_rule(
                        rule_type=InteractionType.EMPOWERMENT,
                        conditions={
                            "energy_level": 0.5,
                            "resonance": 0.7
                        },
                        effects={
                            "energy_boost": matching_pattern.intensity,
                            "power_increase": 0.2
                        },
                        priority=7,
                        description=f"Empowerment through {matching_pattern.pattern_type} resonance"
                    )
                    active_rules.append(empowerment_rule)
                
                # Create transformation rules for strong dissonant patterns
                if matching_pattern and matching_pattern.pattern_type == ResonanceType.DISSONANT and matching_pattern.intensity >= 0.7:
                    transformation_rule = self.create_interaction_rule(
                        rule_type=InteractionType.TRANSFORMATION,
                        conditions={
                            "connection_strength": 0.6,
                            "pattern_intensity": 0.7
                        },
                        effects={
                            "mutation_factor": matching_pattern.intensity,
                            "evolution_rate": 0.3
                        },
                        priority=6,
                        description=f"Transformation through strong dissonance"
                    )
                    active_rules.append(transformation_rule)
                
                # Create opposition rules for dampening patterns
                if matching_pattern and matching_pattern.pattern_type == ResonanceType.DAMPENING:
                    opposition_rule = self.create_interaction_rule(
                        rule_type=InteractionType.OPPOSITION,
                        conditions={
                            "dissonance": 0.5,
                            "conflict_level": 0.6
                        },
                        effects={
                            "challenge_level": matching_pattern.intensity,
                            "breakthrough_chance": 0.4
                        },
                        priority=5,
                        description=f"Opposition through dampening resonance"
                    )
                    active_rules.append(opposition_rule)
                
                # Create synthesis rules for neutral patterns
                if matching_pattern and matching_pattern.pattern_type == ResonanceType.NEUTRAL:
                    synthesis_rule = self.create_interaction_rule(
                        rule_type=InteractionType.SYNTHESIS,
                        conditions={
                            "harmony": 0.5,
                            "synchronization": 0.5
                        },
                        effects={
                            "synergy_level": matching_pattern.intensity,
                            "pattern_stability": 0.6
                        },
                        priority=4,
                        description=f"Synthesis through neutral resonance"
                    )
                    active_rules.append(synthesis_rule)
            
            # Filter rules by conditions
            active_rules = [
                rule for rule in active_rules
                if any(
                    check_conditions(rule, conn, next(
                        (p for p in patterns if conn.source_governor in p.governors and conn.target_governor in p.governors),
                        None
                    ))
                    for conn in connections
                )
            ]
            
            # Resolve conflicts
            final_rules = resolve_conflicts(active_rules)
            
            self.logger.info(
                "Applied %d interaction rules (resolved from %d active rules)",
                len(final_rules), len(active_rules)
            )
            
            return final_rules
            
        except Exception as e:
            self.logger.error("Error applying interaction rules: %s", str(e))
            raise

    async def generate_visualization(
        self,
        connections: List[GovernorConnection],
        patterns: List[ResonancePattern],
        aethyrs: List[AethyrProfile]
    ) -> Tuple[RelationshipVisualization, List[RelationshipVisualizationCluster]]:
        """Generate a visualization of the relationship network"""
        try:
            # Get Bitcoin entropy for visualization
            bitcoin_entropy = await self.bitcoin_integration.get_entropy(
                "_".join(sorted([
                    conn.source_governor + conn.target_governor
                    for conn in connections
                ]) or ["default"])
            )
            
            # Get all unique governors
            governors = set()
            for conn in connections:
                governors.add(conn.source_governor)
                governors.add(conn.target_governor)
            for pattern in patterns:
                governors.update(pattern.governors)
            governors = sorted(list(governors))
            
            # Calculate node powers
            node_powers = {}
            for governor in governors:
                node_powers[governor] = await self.calculate_node_power(
                    governor,
                    connections,
                    patterns,
                    aethyrs,
                    bitcoin_entropy
                )
            
            # Calculate edge weights
            edges = []
            for conn in connections:
                weight = self.calculate_edge_weight(
                    conn,
                    patterns,
                    node_powers,
                    bitcoin_entropy
                )
                edges.append({
                    "source": conn.source_governor,
                    "target": conn.target_governor,
                    "weight": weight,
                    "type": conn.connection_type.value
                })
            
            # Form clusters
            clusters = self.form_clusters(
                patterns,
                node_powers,
                bitcoin_entropy
            )
            
            # Calculate node positions
            node_positions = calculate_coordinates(
                governors,
                edges,
                clusters,
                node_powers
            )
            
            # Create visualization nodes
            nodes = []
            for governor in governors:
                nodes.append(RelationshipVisualizationNode(
                    governor=governor,
                    power=node_powers[governor],
                    x=node_positions[governor]["x"],
                    y=node_positions[governor]["y"],
                    z=node_positions[governor]["z"]
                ))
            
            # Calculate cluster visuals
            for cluster in clusters:
                cluster.visuals = self.calculate_cluster_visuals(
                    cluster,
                    node_powers,
                    bitcoin_entropy
                )
            
            # Create visualization
            visualization = RelationshipVisualization(
                nodes=nodes,
                edges=edges,
                clusters=clusters,
                entropy=bitcoin_entropy
            )
            
            # Validate visualization
            validation = self.validate_visualization_constraints(visualization)
            if not validation.is_valid:
                self.logger.warning(
                    "Visualization constraints validation failed: %s",
                    validation.errors
                )
            
            validation = self.validate_visualization_aesthetics(visualization, clusters)
            if not validation.is_valid:
                self.logger.warning(
                    "Visualization aesthetics validation failed: %s",
                    validation.errors
                )
            
            # Cache visualization
            cache_key = self.get_cache_key(connections, patterns)
            self.cache_visualization(visualization, clusters, cache_key)
            
            return visualization, clusters
            
        except Exception as e:
            self.logger.error("Error generating visualization: %s", str(e))
            raise

    async def generate_relationship_profile(
        self,
        governors: List[str],
        aethyrs: List[AethyrProfile]
    ) -> RelationshipProfile:
        """Generate a complete relationship profile for a set of Governors"""
        try:
            # Get Bitcoin block hash
            block_hash = await self.bitcoin_integration.get_entropy("relationship_profile")
            
            # Generate all possible connections
            connections = []
            for i, gov1 in enumerate(governors[:-1]):
                for gov2 in governors[i+1:]:
                    # Find shared attributes from aethyrs
                    shared_attributes = []
                    for aethyr in aethyrs:
                        if gov1 in aethyr.governors and gov2 in aethyr.governors:
                            shared_attributes.append(aethyr.correspondence)
                    
                    connection = await self.generate_connection(
                        gov1,
                        gov2,
                        shared_attributes
                    )
                    connections.append(connection)
            
            # Generate resonance patterns
            patterns = []
            for i in range(3, len(governors) + 1):  # Patterns of 3 or more governors
                for group in itertools.combinations(governors, i):
                    pattern = await self.calculate_resonance(
                        list(group),
                        aethyrs
                    )
                    patterns.append(pattern)
            
            # Apply interaction rules
            rules = self.apply_interaction_rules(connections, patterns)
            
            # Generate visualization
            visualization, _ = await self.generate_visualization(
                connections,
                patterns,
                aethyrs
            )
            
            # Create profile
            profile = RelationshipProfile(
                connections=connections,
                resonance_patterns=patterns,
                interaction_rules=rules,
                visualization=visualization,
                bitcoin_block_hash=block_hash
            )
            
            # Validate profile
            if not await self.verify_block_hash(block_hash, profile):
                self.logger.warning("Profile verification failed")
            
            return profile
            
        except Exception as e:
            self.logger.error("Error generating relationship profile: %s", str(e))
            raise

    async def update_relationship_profile(
        self,
        profile: RelationshipProfile,
        transaction_id: str,
        update_type: str,
        update_data: Dict[str, Any]
    ) -> RelationshipProfile:
        """Update an existing relationship profile"""
        try:
            # Get transaction entropy
            tx_entropy = await self.bitcoin_integration.get_entropy(transaction_id)
            
            # Update based on type
            if update_type == "add_governor":
                governor = update_data["governor"]
                aethyrs = update_data.get("aethyrs", [])
                
                # Get existing governors from connections
                existing_governors = set()
                for conn in profile.connections:
                    existing_governors.add(conn.source_governor)
                    existing_governors.add(conn.target_governor)
                
                # Generate new connections if governor doesn't exist
                if governor not in existing_governors:
                    for existing_gov in existing_governors:
                        shared_attributes = []
                        for aethyr in aethyrs:
                            if governor in aethyr.governors and existing_gov in aethyr.governors:
                                shared_attributes.append(aethyr.correspondence)
                        
                        connection = await self.generate_connection(
                            governor,
                            existing_gov,
                            shared_attributes
                        )
                        profile.connections.append(connection)
                
                # Update resonance patterns
                all_governors = list(existing_governors) + [governor]
                new_patterns = []
                for i in range(3, len(all_governors) + 1):
                    for group in itertools.combinations(all_governors, i):
                        if governor in group:
                            pattern = await self.calculate_resonance(
                                list(group),
                                aethyrs
                            )
                            new_patterns.append(pattern)
                profile.resonance_patterns.extend(new_patterns)
                
                # Update interaction rules
                profile.interaction_rules = self.apply_interaction_rules(
                    profile.connections,
                    profile.resonance_patterns
                )
                
                # Update visualization
                visualization, _ = await self.generate_visualization(
                    profile.connections,
                    profile.resonance_patterns,
                    aethyrs
                )
                profile.visualization = visualization
            
            # Update block hash
            profile.bitcoin_block_hash = await self.bitcoin_integration.get_entropy("relationship_profile")
            
            # Validate updated profile
            if not await self.verify_block_hash(profile.bitcoin_block_hash, profile):
                self.logger.warning("Updated profile verification failed")
            
            return profile
            
        except Exception as e:
            self.logger.error("Error updating relationship profile: %s", str(e))
            raise

    def calculate_edge_weight(
        self,
        connection: GovernorConnection,
        patterns: List[ResonancePattern],
        node_powers: Dict[str, float],
        bitcoin_entropy: str
    ) -> float:
        """Calculate weight for a visualization edge"""
        try:
            # Base weight from connection strength
            weight = connection.strength
            
            # Adjust based on node powers
            source_power = node_powers[connection.source_governor]
            target_power = node_powers[connection.target_governor]
            power_factor = (source_power + target_power) / 2
            weight *= power_factor
            
            # Adjust based on resonance patterns
            pattern_influence = 0.0
            pattern_count = 0
            for pattern in patterns:
                if (connection.source_governor in pattern.governors and
                    connection.target_governor in pattern.governors):
                    pattern_influence += pattern.intensity
                    pattern_count += 1
            
            if pattern_count > 0:
                pattern_factor = pattern_influence / pattern_count
                weight = (weight + pattern_factor) / 2
            
            # Add entropy-based variation
            entropy_hash = int(bitcoin_entropy[:8], 16)
            variation = (entropy_hash & 0xFF) / 255.0 * 0.2 - 0.1  # -0.1 to +0.1
            weight = max(0.1, min(1.0, weight + variation))
            
            return weight
            
        except Exception as e:
            self.logger.error("Error calculating edge weight: %s", str(e))
            return 0.5  # Default weight

    def form_clusters(
        self,
        patterns: List[ResonancePattern],
        node_powers: Dict[str, float],
        bitcoin_entropy: str
    ) -> List[RelationshipVisualizationCluster]:
        """Form visualization clusters from resonance patterns"""
        try:
            # Helper function to check if patterns can be merged
            def can_merge_patterns(p1: ResonancePattern, p2: ResonancePattern) -> bool:
                # Must be same type
                if p1.pattern_type != p2.pattern_type:
                    return False
                
                # Must have overlapping governors
                overlap = set(p1.governors) & set(p2.governors)
                if not overlap:
                    return False
                
                # Must have similar intensities
                intensity_diff = abs(p1.intensity - p2.intensity)
                if intensity_diff > 0.3:  # Max 30% difference
                    return False
                
                return True
            
            # Helper function to merge patterns into a cluster
            def merge_patterns(patterns_to_merge: List[ResonancePattern]) -> RelationshipVisualizationCluster:
                # Get all governors
                all_governors = set()
                for pattern in patterns_to_merge:
                    all_governors.update(pattern.governors)
                
                # Calculate average intensity
                avg_intensity = sum(p.intensity for p in patterns_to_merge) / len(patterns_to_merge)
                
                return RelationshipVisualizationCluster(
                    governors=sorted(list(all_governors)),
                    type=patterns_to_merge[0].pattern_type.value,
                    intensity=avg_intensity
                )
            
            # Sort patterns by intensity (descending)
            sorted_patterns = sorted(
                patterns,
                key=lambda p: p.intensity,
                reverse=True
            )
            
            # Group patterns by type
            pattern_groups = {}
            for pattern in sorted_patterns:
                if pattern.pattern_type not in pattern_groups:
                    pattern_groups[pattern.pattern_type] = []
                pattern_groups[pattern.pattern_type].append(pattern)
            
            # Form clusters for each type
            clusters = []
            for pattern_type, type_patterns in pattern_groups.items():
                # Start with each pattern as its own cluster
                current_clusters = [[p] for p in type_patterns]
                
                # Keep merging until no more merges possible
                while True:
                    merged = False
                    for i in range(len(current_clusters)):
                        if merged:
                            break
                        for j in range(i + 1, len(current_clusters)):
                            # Check if any pattern in cluster i can merge with any in cluster j
                            can_merge = any(
                                can_merge_patterns(p1, p2)
                                for p1 in current_clusters[i]
                                for p2 in current_clusters[j]
                            )
                            
                            if can_merge:
                                # Merge clusters
                                current_clusters[i].extend(current_clusters[j])
                                del current_clusters[j]
                                merged = True
                                break
                    
                    if not merged:
                        break
                
                # Convert merged pattern groups to clusters
                for pattern_group in current_clusters:
                    clusters.append(merge_patterns(pattern_group))
            
            # Sort clusters by size and intensity
            clusters.sort(
                key=lambda c: (len(c.governors), c.intensity),
                reverse=True
            )
            
            # Use entropy to adjust cluster order
            entropy_hash = int(bitcoin_entropy[:8], 16)
            if entropy_hash & 1:  # 50% chance to reverse order
                clusters.reverse()
            
            return clusters
            
        except Exception as e:
            self.logger.error("Error forming clusters: %s", str(e))
            return []

    def calculate_cluster_visuals(
        self,
        cluster: RelationshipVisualizationCluster,
        node_powers: Dict[str, float],
        bitcoin_entropy: str
    ) -> VisualProperties:
        """Calculate visual properties for a cluster"""
        try:
            # Use entropy for consistent randomization
            entropy_hash = int(bitcoin_entropy[:8], 16)
            
            # Calculate base color from node powers
            avg_power = sum(node_powers[gov] for gov in cluster.governors) / len(cluster.governors)
            
            # Generate color based on power and entropy
            hue = (entropy_hash & 0xFF) / 255.0  # 0-1 range
            saturation = 0.5 + avg_power * 0.5   # 0.5-1 range
            value = 0.7 + avg_power * 0.3        # 0.7-1 range
            
            # Convert HSV to RGB
            h = hue * 6
            c = value * saturation
            x = c * (1 - abs(h % 2 - 1))
            m = value - c
            
            if h < 1:
                r, g, b = c, x, 0
            elif h < 2:
                r, g, b = x, c, 0
            elif h < 3:
                r, g, b = 0, c, x
            elif h < 4:
                r, g, b = 0, x, c
            elif h < 5:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
            
            color = ColorRGB(
                r=int((r + m) * 255),
                g=int((g + m) * 255),
                b=int((b + m) * 255)
            )
            
            # Calculate opacity based on power
            opacity = 0.4 + avg_power * 0.6  # 0.4-1 range
            
            # Generate glow effect
            glow = GlowEffect(
                radius=5 + avg_power * 15,  # 5-20 range
                color=color,
                intensity=avg_power
            )
            
            # Generate border style
            border = BorderStyle(
                width=1 + avg_power * 4,  # 1-5 range
                style="solid",
                color=color
            )
            
            # Generate shape properties
            shape_types = ["circle", "hexagon", "octagon", "decagon"]
            shape_idx = int(entropy_hash >> 8) % len(shape_types)
            rotation = (entropy_hash >> 16) % 360
            
            shape = ShapeProperties(
                type=shape_types[shape_idx],
                sides=6 + shape_idx * 2,  # 6-12 sides
                rotation=float(rotation)
            )
            
            return VisualProperties(
                color=color,
                opacity=opacity,
                glow=glow,
                border=border,
                shape=shape
            )
            
        except Exception as e:
            self.logger.error("Error calculating cluster visuals: %s", str(e))
            # Return default visuals
            color = ColorRGB(r=128, g=128, b=128)
            return VisualProperties(
                color=color,
                opacity=0.7,
                glow=GlowEffect(radius=10, color=color, intensity=0.5),
                border=BorderStyle(width=2, style="solid", color=color),
                shape=ShapeProperties(type="circle", sides=6, rotation=0)
            )

    def validate_cluster_formation(
        self,
        clusters: List[RelationshipVisualizationCluster],
        patterns: List[ResonancePattern],
        node_powers: Dict[str, float]
    ) -> ValidationResult:
        """Validate cluster formation and merging rules"""
        try:
            errors = []
            
            # Check for empty clusters
            empty_clusters = [
                i for i, cluster in enumerate(clusters)
                if not cluster.governors
            ]
            if empty_clusters:
                errors.append(f"Empty clusters found at indices: {empty_clusters}")
            
            # Check for oversized clusters
            oversized_clusters = [
                i for i, cluster in enumerate(clusters)
                if len(cluster.governors) > 7  # Max reasonable size for visualization
            ]
            if oversized_clusters:
                errors.append(f"Oversized clusters found at indices: {oversized_clusters}")
            
            # Check for duplicate governors in clusters
            for i, cluster in enumerate(clusters):
                if len(set(cluster.governors)) != len(cluster.governors):
                    errors.append(f"Duplicate governors in cluster {i}")
            
            # Check for overlapping clusters of same type
            for i, c1 in enumerate(clusters[:-1]):
                for j, c2 in enumerate(clusters[i+1:], i+1):
                    if c1.type == c2.type:
                        overlap = set(c1.governors) & set(c2.governors)
                        if len(overlap) > len(c1.governors) * 0.7 or len(overlap) > len(c2.governors) * 0.7:
                            errors.append(f"Excessive overlap between clusters {i} and {j}")
            
            # Check intensity distribution
            intensities = [cluster.intensity for cluster in clusters]
            if intensities:
                avg_intensity = sum(intensities) / len(intensities)
                outliers = [
                    i for i, intensity in enumerate(intensities)
                    if abs(intensity - avg_intensity) > 0.5  # Max 50% deviation
                ]
                if outliers:
                    errors.append(f"Intensity outliers found in clusters: {outliers}")
            
            # Check pattern coverage
            covered_patterns = set()
            for cluster in clusters:
                cluster_governors = set(cluster.governors)
                for pattern in patterns:
                    if set(pattern.governors).issubset(cluster_governors):
                        covered_patterns.add(pattern)
            
            uncovered = len(patterns) - len(covered_patterns)
            if uncovered > len(patterns) * 0.2:  # Max 20% uncovered
                errors.append(f"Too many uncovered patterns: {uncovered}/{len(patterns)}")
            
            # Check power balance
            for i, cluster in enumerate(clusters):
                cluster_powers = [node_powers[gov] for gov in cluster.governors]
                if cluster_powers:
                    avg_power = sum(cluster_powers) / len(cluster_powers)
                    power_spread = max(cluster_powers) - min(cluster_powers)
                    if power_spread > 0.6:  # Max 60% power difference
                        errors.append(f"Excessive power spread in cluster {i}: {power_spread:.2f}")
            
            # Check cluster density
            for i, cluster in enumerate(clusters):
                if len(cluster.governors) >= 3:
                    # Calculate density as ratio of actual connections to possible connections
                    possible_connections = (len(cluster.governors) * (len(cluster.governors) - 1)) / 2
                    actual_connections = sum(
                        1 for pattern in patterns
                        if len(set(pattern.governors) & set(cluster.governors)) >= 2
                    )
                    density = actual_connections / possible_connections
                    if density < 0.3:  # Min 30% density
                        errors.append(f"Low connection density in cluster {i}: {density:.2f}")
            
            # Check cluster isolation
            for i, cluster in enumerate(clusters):
                external_connections = 0
                internal_connections = 0
                cluster_governors = set(cluster.governors)
                
                for pattern in patterns:
                    pattern_governors = set(pattern.governors)
                    if pattern_governors.issubset(cluster_governors):
                        internal_connections += 1
                    elif pattern_governors & cluster_governors:
                        external_connections += 1
                
                if internal_connections > 0 and external_connections / internal_connections > 2:
                    errors.append(f"Cluster {i} has too many external connections")
            
            is_valid = len(errors) == 0
            self.logger.info(
                "Cluster validation %s: %d errors",
                "passed" if is_valid else "failed",
                len(errors)
            )
            
            return ValidationResult(
                is_valid=is_valid,
                errors=errors
            )
            
        except Exception as e:
            self.logger.error("Error validating clusters: %s", str(e))
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"]
            ) 

    def export_visualization(
        self,
        visualization: RelationshipVisualization,
        clusters: List[RelationshipVisualizationCluster],
        file_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Export visualization data to JSON format"""
        try:
            # Convert nodes to JSON format
            nodes_json = []
            for node in visualization.nodes:
                nodes_json.append({
                    "id": node.governor,
                    "position": {
                        "x": float(node.x),
                        "y": float(node.y),
                        "z": float(node.z)
                    },
                    "power": float(node.power)
                })
            
            # Convert edges to JSON format
            edges_json = []
            for edge in visualization.edges:
                edges_json.append({
                    "source": edge["source"],
                    "target": edge["target"],
                    "weight": float(edge["weight"])
                })
            
            # Convert clusters to JSON format
            clusters_json = []
            for cluster in clusters:
                cluster_data = {
                    "governors": cluster.governors,
                    "type": cluster.type,
                    "intensity": float(cluster.intensity)
                }
                
                # Add visual properties if available
                if hasattr(cluster, "visuals") and cluster.visuals:
                    visuals = cluster.visuals
                    cluster_data["visuals"] = {
                        "color": {
                            "r": int(visuals.color.r),
                            "g": int(visuals.color.g),
                            "b": int(visuals.color.b)
                        },
                        "opacity": float(visuals.opacity)
                    }
                    
                    # Add optional glow properties
                    if visuals.glow:
                        cluster_data["visuals"]["glow"] = {
                            "radius": float(visuals.glow.radius),
                            "color": {
                                "r": int(visuals.glow.color.r),
                                "g": int(visuals.glow.color.g),
                                "b": int(visuals.glow.color.b)
                            },
                            "intensity": float(visuals.glow.intensity)
                        }
                    
                    # Add optional border properties
                    if visuals.border:
                        cluster_data["visuals"]["border"] = {
                            "width": float(visuals.border.width),
                            "style": visuals.border.style,
                            "color": {
                                "r": int(visuals.border.color.r),
                                "g": int(visuals.border.color.g),
                                "b": int(visuals.border.color.b)
                            }
                        }
                    
                    # Add optional shape properties
                    if visuals.shape:
                        cluster_data["visuals"]["shape"] = {
                            "type": visuals.shape.type,
                            "sides": int(visuals.shape.sides),
                            "rotation": float(visuals.shape.rotation)
                        }
                
                clusters_json.append(cluster_data)
            
            # Create complete visualization data
            visualization_data = {
                "metadata": {
                    "dimensions": visualization.dimensions,
                    "entropy": visualization.entropy,
                    "timestamp": datetime.utcnow().isoformat(),
                    "version": "1.0"
                },
                "nodes": nodes_json,
                "edges": edges_json,
                "clusters": clusters_json
            }
            
            # Save to file if path provided
            if file_path:
                try:
                    with open(file_path, "w") as f:
                        json.dump(visualization_data, f, indent=2)
                    self.logger.info("Visualization exported to %s", file_path)
                except Exception as e:
                    self.logger.error("Error saving visualization to file: %s", str(e))
            
            return visualization_data
            
        except Exception as e:
            self.logger.error("Error exporting visualization: %s", str(e))
            raise 

    def import_visualization(
        self,
        file_path: str
    ) -> Tuple[RelationshipVisualization, List[RelationshipVisualizationCluster]]:
        """Import visualization data from JSON format"""
        try:
            # Read JSON data
            with open(file_path, "r") as f:
                data = json.load(f)
            
            # Validate version
            version = data.get("metadata", {}).get("version", "1.0")
            if version != "1.0":
                self.logger.warning(
                    "Importing visualization with different version: %s",
                    version
                )
            
            # Create nodes
            nodes = []
            for node_data in data["nodes"]:
                nodes.append(
                    RelationshipVisualizationNode(
                        governor=node_data["id"],
                        x=float(node_data["position"]["x"]),
                        y=float(node_data["position"]["y"]),
                        z=float(node_data["position"]["z"]),
                        power=float(node_data["power"])
                    )
                )
            
            # Create edges
            edges = []
            for edge_data in data["edges"]:
                edges.append({
                    "source": edge_data["source"],
                    "target": edge_data["target"],
                    "weight": float(edge_data["weight"])
                })
            
            # Create clusters
            clusters = []
            for cluster_data in data["clusters"]:
                cluster = RelationshipVisualizationCluster(
                    governors=cluster_data["governors"],
                    type=cluster_data["type"],
                    intensity=float(cluster_data["intensity"])
                )
                
                # Add visual properties if available
                if "visuals" in cluster_data:
                    visuals = cluster_data["visuals"]
                    
                    # Create VisualProperties object
                    color = ColorRGB(
                        r=int(visuals["color"]["r"]),
                        g=int(visuals["color"]["g"]),
                        b=int(visuals["color"]["b"])
                    )
                    
                    glow = None
                    if "glow" in visuals:
                        glow_color = ColorRGB(
                            r=int(visuals["glow"]["color"]["r"]),
                            g=int(visuals["glow"]["color"]["g"]),
                            b=int(visuals["glow"]["color"]["b"])
                        )
                        glow = GlowEffect(
                            radius=float(visuals["glow"]["radius"]),
                            color=glow_color,
                            intensity=float(visuals["glow"]["intensity"])
                        )
                    
                    border = None
                    if "border" in visuals:
                        border_color = ColorRGB(
                            r=int(visuals["border"]["color"]["r"]),
                            g=int(visuals["border"]["color"]["g"]),
                            b=int(visuals["border"]["color"]["b"])
                        )
                        border = BorderStyle(
                            width=float(visuals["border"]["width"]),
                            style=visuals["border"]["style"],
                            color=border_color
                        )
                    
                    shape = None
                    if "shape" in visuals:
                        shape = ShapeProperties(
                            type=visuals["shape"]["type"],
                            sides=int(visuals["shape"]["sides"]),
                            rotation=float(visuals["shape"]["rotation"])
                        )
                    
                    cluster.visuals = VisualProperties(
                        color=color,
                        opacity=float(visuals["opacity"]),
                        glow=glow,
                        border=border,
                        shape=shape
                    )
                
                clusters.append(cluster)
            
            # Create visualization
            visualization = RelationshipVisualization(
                nodes=nodes,
                edges=edges,
                clusters=clusters,
                dimensions=data["metadata"]["dimensions"],
                entropy=data["metadata"]["entropy"]
            )
            
            # Validate imported data
            aesthetics_validation = self.validate_visualization_aesthetics(
                visualization=visualization,
                clusters=clusters
            )
            if not aesthetics_validation.is_valid:
                self.logger.warning(
                    "Imported visualization has aesthetic issues: %s",
                    ", ".join(aesthetics_validation.errors or [])
                )
            
            self.logger.info(
                "Imported visualization from %s with %d nodes, %d edges, %d clusters",
                file_path, len(nodes), len(edges), len(clusters)
            )
            
            return visualization, clusters
            
        except Exception as e:
            self.logger.error("Error importing visualization: %s", str(e))
            raise

    def get_cache_key(
        self,
        connections: List[GovernorConnection],
        patterns: List[ResonancePattern]
    ) -> str:
        """Generate a cache key from connections and patterns"""
        try:
            # Sort connections by governor names
            sorted_connections = sorted([
                f"{conn.source_governor}_{conn.target_governor}_{conn.connection_type.value}_{conn.strength:.3f}"
                for conn in connections
            ])
            
            # Sort patterns by governors
            sorted_patterns = sorted([
                f"{','.join(sorted(pattern.governors))}_{pattern.pattern_type.value}_{pattern.intensity:.3f}"
                for pattern in patterns
            ])
            
            # Combine and hash
            combined = "_".join(sorted_connections + sorted_patterns)
            return hashlib.sha256(combined.encode()).hexdigest()
            
        except Exception as e:
            self.logger.error("Error generating cache key: %s", str(e))
            # Fall back to timestamp-based key
            return f"fallback_{int(time.time())}"
    
    def get_cache_path(self, cache_key: str) -> str:
        """Get file path for cached visualization data"""
        cache_dir = os.path.join(self.config.output_dir, "visualization_cache")
        os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, f"{cache_key}.json")
    
    def cache_visualization(
        self,
        visualization: RelationshipVisualization,
        clusters: List[RelationshipVisualizationCluster],
        cache_key: str
    ) -> bool:
        """Cache visualization data to file"""
        try:
            cache_path = self.get_cache_path(cache_key)
            
            # Export visualization to cache file
            self.export_visualization(
                visualization=visualization,
                clusters=clusters,
                file_path=cache_path
            )
            
            self.logger.info("Cached visualization to %s", cache_path)
            return True
            
        except Exception as e:
            self.logger.error("Error caching visualization: %s", str(e))
            return False
    
    def get_cached_visualization(
        self,
        cache_key: str
    ) -> Optional[Tuple[RelationshipVisualization, List[RelationshipVisualizationCluster]]]:
        """Retrieve cached visualization data"""
        try:
            cache_path = self.get_cache_path(cache_key)
            
            # Check if cache exists
            if not os.path.exists(cache_path):
                return None
            
            # Check cache age
            cache_age = time.time() - os.path.getmtime(cache_path)
            if cache_age > self.config.visualization_cache_ttl:
                self.logger.info(
                    "Cache expired for key %s (age: %.2f hours)",
                    cache_key, cache_age / 3600
                )
                return None
            
            # Import visualization from cache
            visualization, clusters = self.import_visualization(cache_path)
            
            self.logger.info("Retrieved visualization from cache: %s", cache_path)
            return visualization, clusters
            
        except Exception as e:
            self.logger.error("Error retrieving cached visualization: %s", str(e))
            return None
    
    def clear_visualization_cache(self) -> bool:
        """Clear all cached visualization data"""
        try:
            cache_dir = os.path.join(self.config.output_dir, "visualization_cache")
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                os.makedirs(cache_dir)
                self.logger.info("Cleared visualization cache")
                return True
            return False
            
        except Exception as e:
            self.logger.error("Error clearing visualization cache: %s", str(e))
            return False

    async def verify_block_hash(
        self,
        block_hash: str,
        profile: RelationshipProfile
    ) -> bool:
        """Verify that a relationship profile matches its block hash"""
        try:
            # Get current block hash
            current_hash = await self.bitcoin_integration.get_entropy("relationship_profile")
            
            # Compare hashes
            if block_hash != current_hash:
                self.logger.warning(
                    "Block hash mismatch: stored=%s, current=%s",
                    block_hash, current_hash
                )
                return False
            
            # Verify individual components
            for conn in profile.connections:
                if not self.bitcoin_integration.verify_hash(conn.bitcoin_verification):
                    self.logger.warning(
                        "Connection verification failed: %s -> %s",
                        conn.source_governor, conn.target_governor
                    )
                    return False
            
            for pattern in profile.resonance_patterns:
                if not self.bitcoin_integration.verify_hash(pattern.bitcoin_entropy):
                    self.logger.warning(
                        "Pattern verification failed: %s",
                        pattern.governors
                    )
                    return False
            
            if profile.visualization and not self.bitcoin_integration.verify_hash(profile.visualization.entropy):
                self.logger.warning("Visualization verification failed")
                return False
            
            self.logger.info("Block hash verification successful")
            return True
            
        except Exception as e:
            self.logger.error("Error verifying block hash: %s", str(e))
            return False

    async def calculate_node_power(
        self,
        governor: str,
        connections: List[GovernorConnection],
        patterns: List[ResonancePattern],
        aethyrs: List[AethyrProfile],
        bitcoin_entropy: str
    ) -> float:
        """Calculate power level for a visualization node"""
        try:
            # Base power from connections
            connection_power = sum(
                conn.strength
                for conn in connections
                if governor in (conn.source_governor, conn.target_governor)
            ) / max(len(connections), 1)
            
            # Power from resonance patterns
            pattern_power = sum(
                pattern.intensity
                for pattern in patterns
                if governor in pattern.governors
            ) / max(len(patterns), 1)
            
            # Power from aethyric influence
            aethyr_power = sum(
                aethyr.influence
                for aethyr in aethyrs
                if governor in aethyr.governors
            ) / max(len(aethyrs), 1)
            
            # Combine powers with entropy-based weighting
            entropy_hash = int(bitcoin_entropy[:8], 16)
            weights = [
                (entropy_hash >> 6) & 0x3,  # Connection weight
                (entropy_hash >> 4) & 0x3,  # Pattern weight
                (entropy_hash >> 2) & 0x3   # Aethyr weight
            ]
            total_weight = sum(weights) or 1
            
            power = (
                weights[0] * connection_power +
                weights[1] * pattern_power +
                weights[2] * aethyr_power
            ) / total_weight
            
            return min(max(power, 0.1), 1.0)  # Clamp between 0.1 and 1.0
            
        except Exception as e:
            self.logger.error("Error calculating node power: %s", str(e))
            return 0.5  # Default power level