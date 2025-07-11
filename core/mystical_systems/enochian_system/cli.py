"""
Command-line interface for the Enochian system
"""

import asyncio
import json
from typing import List, Optional, Dict, Any
from pathlib import Path

from core.utils.custom_logging import setup_logger
from .enochian_system import EnochianSystem
from .schemas import EnochianSystemConfig
from .ritual_mechanics import RitualEngine
from .ritual_mechanics.schemas import RitualPoint
from .relationships import RelationshipEngine

try:
    import click
except ImportError:
    raise ImportError(
        "click package is required. Install it with: pip install click"
    )

logger = setup_logger("enochian_cli")

@click.group()
def cli():
    """Enochian Magic System CLI"""
    pass

@cli.command()
@click.option('--config', type=click.Path(exists=True), help='Path to config file')
@click.option('--output', type=click.Path(), help='Output path for results')
@click.argument('governors', nargs=-1)
def analyze_relationships(config: Optional[str], output: Optional[str], governors: List[str]):
    """Analyze relationships between specified Governors"""
    async def _analyze():
        try:
            # Load config
            if config:
                with open(config) as f:
                    config_data = json.load(f)
            else:
                config_data = {}
            
            # Initialize system
            system_config = EnochianSystemConfig(**config_data)
            system = EnochianSystem(config=system_config.model_dump())
            relationship_engine = RelationshipEngine(system_config)
            
            # Get Aethyrs data
            aethyrs = await system.get_all_aethyrs()
            
            # Generate relationship profile
            profile = await relationship_engine.generate_relationship_profile(
                list(governors),
                aethyrs
            )
            
            # Format output
            result = {
                "governors": governors,
                "connections": [conn.model_dump() for conn in profile.connections],
                "patterns": [pat.model_dump() for pat in profile.resonance_patterns],
                "rules": [rule.model_dump() for rule in profile.interaction_rules],
                "visualization": profile.visualization.model_dump(),
                "timestamp": profile.timestamp.isoformat(),
                "bitcoin_verification": profile.bitcoin_block_hash
            }
            
            # Save or print results
            if output:
                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w') as f:
                    json.dump(result, f, indent=2)
                click.echo(f"Results saved to {output}")
            else:
                click.echo(json.dumps(result, indent=2))
                
        except Exception as e:
            logger.error(f"Error analyzing relationships: {str(e)}")
            raise click.ClickException(str(e))
    
    asyncio.run(_analyze())

@cli.command()
@click.option('--config', type=click.Path(exists=True), help='Path to config file')
@click.option('--output', type=click.Path(), help='Output path for results')
@click.argument('ritual_points', type=click.Path(exists=True))
def validate_ritual(config: Optional[str], output: Optional[str], ritual_points: str):
    """Validate ritual points and calculate resonance"""
    async def _validate():
        try:
            # Load config
            if config:
                with open(config) as f:
                    config_data = json.load(f)
            else:
                config_data = {}
            
            # Load ritual points
            with open(ritual_points) as f:
                points_data = json.load(f)
            
            # Initialize system
            system_config = EnochianSystemConfig(**config_data)
            system = EnochianSystem(config=system_config.model_dump())
            ritual_engine = RitualEngine(system_config.model_dump())
            
            # Validate points
            validation = await ritual_engine.validate_ritual_points(
                points_data["points"]
            )
            
            if not validation.is_valid:
                raise click.ClickException(
                    f"Invalid ritual points: {validation.errors}"
                )
            
            # Match ritual pattern
            # Convert points to RitualPoint objects
            ritual_point_objects = [RitualPoint(**point) for point in points_data["points"]]
            pattern = await ritual_engine.match_ritual_pattern(ritual_point_objects)
            
            # Calculate resonance if Aethyr specified
            resonance = None
            if "aethyr" in points_data:
                aethyr = await system.get_aethyr(points_data["aethyr"])
                if aethyr:
                    # For now, use a simple resonance calculation
                    resonance = {
                        "aethyr": aethyr.name,
                        "strength": sum(p.energy_level for p in ritual_point_objects) / len(ritual_point_objects),
                        "compatibility": True
                    }
            
            # Format results
            result = {
                "validation": validation.model_dump(),
                "pattern": pattern.model_dump() if pattern else None,
                "resonance": resonance
            }
            
            # Save or print results
            if output:
                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w') as f:
                    json.dump(result, f, indent=2)
                click.echo(f"Results saved to {output}")
            else:
                click.echo(json.dumps(result, indent=2))
                
        except Exception as e:
            logger.error(f"Error validating ritual: {str(e)}")
            raise click.ClickException(str(e))
    
    asyncio.run(_validate())

@cli.command()
@click.option('--config', type=click.Path(exists=True), help='Path to config file')
@click.option('--output', type=click.Path(), help='Output path for art')
@click.argument('profile_path', type=click.Path(exists=True))
def generate_art(config: Optional[str], output: Optional[str], profile_path: str):
    """Generate visual art for a relationship profile"""
    async def _generate():
        try:
            # Load config
            if config:
                with open(config) as f:
                    config_data = json.load(f)
            else:
                config_data = {}
            
            # Load profile
            with open(profile_path) as f:
                profile_data = json.load(f)
            
            # Initialize system
            system_config = EnochianSystemConfig(**config_data)
            system = EnochianSystem(config=system_config.model_dump())
            
            # Generate art
            art_path = await system.generate_ritual_art(
                profile_data,
                output or "governor_art.json"
            )
            
            click.echo(f"Art generated at {art_path}")
            
        except Exception as e:
            logger.error(f"Error generating art: {str(e)}")
            raise click.ClickException(str(e))
    
    asyncio.run(_generate())

def main():
    """Main entry point for the CLI"""
    cli()

if __name__ == '__main__':
    main() 