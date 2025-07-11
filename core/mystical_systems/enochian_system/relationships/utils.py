"""Utility functions for relationship calculations"""

import math
from typing import Dict, List, Any, Tuple
from .schemas import (
    GovernorConnection,
    ResonancePattern,
    RelationshipVisualizationCluster
)

def calculate_node_power(
    governor: str,
    connections: List[GovernorConnection],
    patterns: List[ResonancePattern],
    aethyrs: List[Any],
    entropy: str
) -> float:
    """Calculate power level for a visualization node"""
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
    
    # Power from Aethyrs
    aethyr_power = sum(
        1 for aethyr in aethyrs
        if governor in aethyr.governors
    ) / max(len(aethyrs), 1)
    
    # Entropy factor (0-1)
    entropy_factor = int(entropy[:8], 16) / (2**32)
    
    # Combine powers with weights
    power = (
        connection_power * 0.4 +
        pattern_power * 0.3 +
        aethyr_power * 0.2 +
        entropy_factor * 0.1
    )
    
    return min(1.0, power)

def calculate_coordinates(
    governors: List[str],
    edges: List[Dict[str, Any]],
    clusters: List[RelationshipVisualizationCluster],
    node_powers: Dict[str, float]
) -> Dict[str, Dict[str, float]]:
    """Calculate 3D coordinates for visualization nodes"""
    positions = {}
    
    # Calculate center of mass for each cluster
    cluster_centers = {}
    for i, cluster in enumerate(clusters):
        if not cluster.governors:
            continue
        
        # Average position of all governors in cluster
        x = sum(node_powers[gov] * math.cos(2 * math.pi * i / len(clusters)) for gov in cluster.governors)
        y = sum(node_powers[gov] * math.sin(2 * math.pi * i / len(clusters)) for gov in cluster.governors)
        z = sum(node_powers[gov] for gov in cluster.governors) / len(cluster.governors)
        
        cluster_centers[i] = {
            "x": x / len(cluster.governors),
            "y": y / len(cluster.governors),
            "z": z
        }
    
    # Calculate initial positions based on cluster membership
    for governor in governors:
        # Find which clusters contain this governor
        member_clusters = [
            i for i, cluster in enumerate(clusters)
            if governor in cluster.governors
        ]
        
        if member_clusters:
            # Average position from all containing clusters
            x = sum(cluster_centers[i]["x"] for i in member_clusters) / len(member_clusters)
            y = sum(cluster_centers[i]["y"] for i in member_clusters) / len(member_clusters)
            z = sum(cluster_centers[i]["z"] for i in member_clusters) / len(member_clusters)
        else:
            # Place unaffiliated nodes in a circle around the origin
            angle = 2 * math.pi * len(positions) / (len(governors) + 1)
            x = math.cos(angle)
            y = math.sin(angle)
            z = 0.0
        
        # Scale by node power
        power = node_powers[governor]
        positions[governor] = {
            "x": x * power,
            "y": y * power,
            "z": z * power
        }
    
    # Apply force-directed layout iterations
    iterations = 50
    k = 1.0  # Spring constant
    
    for _ in range(iterations):
        forces = {gov: {"x": 0.0, "y": 0.0, "z": 0.0} for gov in governors}
        
        # Repulsive forces between all nodes
        for i, gov1 in enumerate(governors):
            pos1 = positions[gov1]
            for gov2 in governors[i+1:]:
                pos2 = positions[gov2]
                
                dx = pos1["x"] - pos2["x"]
                dy = pos1["y"] - pos2["y"]
                dz = pos1["z"] - pos2["z"]
                
                distance = math.sqrt(dx*dx + dy*dy + dz*dz) + 0.1  # Avoid division by zero
                force = k / (distance * distance)
                
                # Apply force to both nodes
                forces[gov1]["x"] += force * dx / distance
                forces[gov1]["y"] += force * dy / distance
                forces[gov1]["z"] += force * dz / distance
                
                forces[gov2]["x"] -= force * dx / distance
                forces[gov2]["y"] -= force * dy / distance
                forces[gov2]["z"] -= force * dz / distance
        
        # Attractive forces along edges
        for edge in edges:
            source = edge["source"]
            target = edge["target"]
            weight = edge["weight"]
            
            pos1 = positions[source]
            pos2 = positions[target]
            
            dx = pos1["x"] - pos2["x"]
            dy = pos1["y"] - pos2["y"]
            dz = pos1["z"] - pos2["z"]
            
            distance = math.sqrt(dx*dx + dy*dy + dz*dz) + 0.1
            force = distance * weight * k
            
            # Apply force to both nodes
            forces[source]["x"] -= force * dx / distance
            forces[source]["y"] -= force * dy / distance
            forces[source]["z"] -= force * dz / distance
            
            forces[target]["x"] += force * dx / distance
            forces[target]["y"] += force * dy / distance
            forces[target]["z"] += force * dz / distance
        
        # Update positions
        for governor in governors:
            f = forces[governor]
            pos = positions[governor]
            
            # Apply forces with damping
            damping = 0.9
            pos["x"] += f["x"] * damping
            pos["y"] += f["y"] * damping
            pos["z"] += f["z"] * damping
            
            # Keep within reasonable bounds
            bound = 10.0
            pos["x"] = max(min(pos["x"], bound), -bound)
            pos["y"] = max(min(pos["y"], bound), -bound)
            pos["z"] = max(min(pos["z"], bound), -bound)
    
    return positions 