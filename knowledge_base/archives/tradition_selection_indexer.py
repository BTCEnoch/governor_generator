#!/usr/bin/env python3
"""
Tradition Selection Indexer for Governor Knowledge Base Selection
================================================================

This script builds a comprehensive index of mystical traditions from governor_archives
and personality_seeds to help governors make informed knowledge base selections.

Part 1: Core tradition indexer structure and tradition loading
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure logging with UTF-8 encoding for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tradition_selection_indexer.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TraditionSummary:
    """Summary of a mystical tradition for governor selection"""
    tradition_name: str
    display_name: str
    overview: str
    core_wisdom: List[str]
    personality_influence: List[str]
    decision_frameworks: List[str]
    communication_styles: List[str]
    ideal_for_governors: List[str]
    key_concepts_count: int
    wisdom_teachings_count: int
    quality_rating: str

@dataclass
class TraditionSelectionIndex:
    """Comprehensive tradition selection index for governors"""
    version: str
    creation_timestamp: str
    total_traditions: int
    tradition_summaries: Dict[str, TraditionSummary]
    selection_recommendations: Dict[str, List[str]]

class TraditionSelectionIndexer:
    """Builds comprehensive tradition selection index from governor archives"""
    
    def __init__(self, archives_dir: str = "governor_archives", seeds_dir: str = "personality_seeds"):
        self.archives_dir = Path(archives_dir)
        self.seeds_dir = Path(seeds_dir)
        self.logger = logging.getLogger("TraditionSelectionIndexer")
        self.selection_index = None
        
        # Ensure directories exist
        if not self.archives_dir.exists():
            raise FileNotFoundError(f"Governor archives directory not found: {self.archives_dir}")
        if not self.seeds_dir.exists():
            raise FileNotFoundError(f"Personality seeds directory not found: {self.seeds_dir}")
        
        self.logger.info("Tradition Selection Indexer initialized")
        self.logger.info(f"Archives directory: {self.archives_dir.absolute()}")
        self.logger.info(f"Seeds directory: {self.seeds_dir.absolute()}")

    def load_tradition_archive(self, archive_file: Path) -> Optional[Dict[str, Any]]:
        """Load a tradition archive file"""
        try:
            with open(archive_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Loaded archive: {archive_file.name}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading {archive_file.name}: {e}")
            return None

    def load_personality_seed(self, seed_file: Path) -> Optional[Dict[str, Any]]:
        """Load a personality seed file"""
        try:
            with open(seed_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Loaded seed: {seed_file.name}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading {seed_file.name}: {e}")
            return None

    def get_tradition_files(self) -> Dict[str, Dict[str, Path]]:
        """Get matching tradition archive and seed files"""
        archive_files = list(self.archives_dir.glob("*_governor_archive.json"))
        seed_files = list(self.seeds_dir.glob("*_seed.json"))
        
        # Map tradition names to file paths
        traditions = {}
        
        for archive_file in archive_files:
            # Extract tradition name from filename
            tradition_name = archive_file.stem.replace("_governor_archive", "")
            
            # Find matching seed file
            seed_file = self.seeds_dir / f"{tradition_name}_seed.json"
            
            if seed_file.exists():
                traditions[tradition_name] = {
                    "archive": archive_file,
                    "seed": seed_file
                }
            else:
                self.logger.warning(f"No matching seed file for {tradition_name}")
        
        self.logger.info(f"Found {len(traditions)} complete tradition pairs")
        return traditions

    def extract_core_wisdom(self, archive_data: Dict[str, Any]) -> List[str]:
        """Extract core wisdom elements from tradition archive"""
        wisdom_elements = []
        
        # Extract from key concepts
        if "key_concepts" in archive_data:
            for concept in archive_data["key_concepts"][:3]:  # Top 3 concepts
                if isinstance(concept, dict) and "wisdom" in concept:
                    wisdom_elements.append(concept["wisdom"])
                elif isinstance(concept, dict) and "principle" in concept:
                    wisdom_elements.append(concept["principle"])
        
        # Extract from wisdom teachings
        if "wisdom_teachings" in archive_data:
            wisdom_elements.extend(archive_data["wisdom_teachings"][:2])  # Top 2 teachings
        
        return wisdom_elements[:5]  # Limit to 5 core wisdom elements

    def determine_ideal_governors(self, archive_data: Dict[str, Any], seed_data: Dict[str, Any]) -> List[str]:
        """Determine what types of governors this tradition is ideal for"""
        ideal_for = []
        
        # Check personality traits from seed
        if "traits" in seed_data:
            traits = seed_data["traits"]
            
            # Map traits to governor types
            trait_mappings = {
                "nature-connected": "Governors aligned with natural elements (Earth, Air)",
                "systematic": "Governors who value order and methodical approaches",
                "ethical": "Governors focused on justice and moral leadership", 
                "transformative": "Governors specializing in change and growth",
                "mystical": "Governors drawn to hidden knowledge and mysteries",
                "balanced": "Governors seeking harmony and equilibrium",
                "wisdom-focused": "Governors prioritizing knowledge and insight",
                "will-focused": "Governors emphasizing personal power and determination",
                "heart-centered": "Governors leading through love and compassion"
            }
            
            for trait in traits:
                if trait in trait_mappings:
                    ideal_for.append(trait_mappings[trait])
        
        # Check communication styles from archive
        if "communication_styles" in archive_data:
            comm_styles = archive_data["communication_styles"]
            if any("wisdom" in style.lower() for style in comm_styles):
                ideal_for.append("Governors who teach through wisdom")
            if any("heart" in style.lower() for style in comm_styles):
                ideal_for.append("Governors who lead through emotional connection")
        
        return ideal_for[:4]  # Limit to 4 recommendations

    def create_tradition_summary(self, tradition_name: str, archive_data: Dict[str, Any], seed_data: Dict[str, Any]) -> TraditionSummary:
        """Create comprehensive tradition summary for governor selection"""
        
        # Extract basic information
        display_name = archive_data.get("display_name", tradition_name.replace("_", " ").title())
        overview = archive_data.get("overview", "Mystical tradition providing wisdom for governance")
        
        # Extract core elements
        core_wisdom = self.extract_core_wisdom(archive_data)
        personality_influence = seed_data.get("traits", [])
        decision_frameworks = archive_data.get("decision_frameworks", [])[:3]  # Top 3
        communication_styles = archive_data.get("communication_styles", [])
        
        # Determine ideal governors
        ideal_for_governors = self.determine_ideal_governors(archive_data, seed_data)
        
        # Count key elements
        key_concepts_count = len(archive_data.get("key_concepts", []))
        wisdom_teachings_count = len(archive_data.get("wisdom_teachings", []))
        quality_rating = archive_data.get("quality_rating", "STANDARD")
        
        return TraditionSummary(
            tradition_name=tradition_name,
            display_name=display_name,
            overview=overview,
            core_wisdom=core_wisdom,
            personality_influence=personality_influence,
            decision_frameworks=decision_frameworks,
            communication_styles=communication_styles,
            ideal_for_governors=ideal_for_governors,
            key_concepts_count=key_concepts_count,
            wisdom_teachings_count=wisdom_teachings_count,
            quality_rating=quality_rating
        )

    def generate_selection_recommendations(self, tradition_summaries: Dict[str, TraditionSummary]) -> Dict[str, List[str]]:
        """Generate tradition selection recommendations by category"""
        recommendations = {
            "for_wisdom_seekers": [],
            "for_balanced_leaders": [],
            "for_mystical_governors": [],
            "for_practical_leaders": [],
            "for_spiritual_guides": [],
            "high_concept_count": [],
            "enhanced_quality": []
        }
        
        for name, summary in tradition_summaries.items():
            # Categorize by traits and characteristics
            if any("wisdom" in trait for trait in summary.personality_influence):
                recommendations["for_wisdom_seekers"].append(name)
            
            if "balanced" in summary.personality_influence:
                recommendations["for_balanced_leaders"].append(name)
            
            if any("mystical" in trait or "knowledge-focused" in trait for trait in summary.personality_influence):
                recommendations["for_mystical_governors"].append(name)
            
            if any("practical" in trait or "results-oriented" in trait for trait in summary.personality_influence):
                recommendations["for_practical_leaders"].append(name)
            
            if any("heart-centered" in trait or "devotional" in trait for trait in summary.personality_influence):
                recommendations["for_spiritual_guides"].append(name)
            
            # Categorize by quality metrics
            if summary.key_concepts_count >= 5:
                recommendations["high_concept_count"].append(name)
            
            if summary.quality_rating == "ENHANCED":
                recommendations["enhanced_quality"].append(name)
        
        return recommendations

    def build_selection_index(self) -> TraditionSelectionIndex:
        """Build comprehensive tradition selection index"""
        self.logger.info("Building tradition selection index...")
        
        tradition_files = self.get_tradition_files()
        tradition_summaries = {}
        
        # Process each tradition
        for tradition_name, files in tradition_files.items():
            archive_data = self.load_tradition_archive(files["archive"])
            seed_data = self.load_personality_seed(files["seed"])
            
            if archive_data and seed_data:
                summary = self.create_tradition_summary(tradition_name, archive_data, seed_data)
                tradition_summaries[tradition_name] = summary
                self.logger.info(f"Created summary for {summary.display_name}")
        
        # Generate recommendations
        recommendations = self.generate_selection_recommendations(tradition_summaries)
        
        # Create selection index
        selection_index = TraditionSelectionIndex(
            version="1.0.0",
            creation_timestamp=datetime.now().isoformat(),
            total_traditions=len(tradition_summaries),
            tradition_summaries=tradition_summaries,
            selection_recommendations=recommendations
        )
        
        self.selection_index = selection_index
        return selection_index

    def save_selection_index(self, output_file: str = "tradition_selection_index.json") -> bool:
        """Save the tradition selection index to JSON file"""
        if not self.selection_index:
            self.logger.error("No selection index to save. Build index first.")
            return False
        
        try:
            # Convert dataclass to dict for JSON serialization
            index_dict = asdict(self.selection_index)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(index_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Tradition selection index saved to {output_file}")
            self.logger.info(f"Total traditions: {self.selection_index.total_traditions}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving selection index: {e}")
            return False

def main():
    """Test the complete tradition selection indexer system"""
    print("Testing Complete Tradition Selection Indexer System...")
    
    try:
        print("Creating indexer...")
        indexer = TraditionSelectionIndexer()
        
        print("Getting tradition files...")
        # Get tradition files
        traditions = indexer.get_tradition_files()
        print(f"\nFound traditions: {len(traditions)}")
        
        if not traditions:
            print("No traditions found! Checking directories...")
            print(f"Archives dir exists: {indexer.archives_dir.exists()}")
            print(f"Seeds dir exists: {indexer.seeds_dir.exists()}")
            
            if indexer.archives_dir.exists():
                archive_files = list(indexer.archives_dir.glob("*.json"))
                print(f"Archive files found: {len(archive_files)}")
                for f in archive_files[:5]:  # Show first 5
                    print(f"  {f.name}")
            
            if indexer.seeds_dir.exists():
                seed_files = list(indexer.seeds_dir.glob("*.json"))
                print(f"Seed files found: {len(seed_files)}")
                for f in seed_files[:5]:  # Show first 5
                    print(f"  {f.name}")
            
            return False
         
        # Build complete selection index
        print("\nBuilding tradition selection index...")
        selection_index = indexer.build_selection_index()
        
        # Display summary
        print(f"\nTradition Selection Index Summary:")
        print(f"  Version: {selection_index.version}")
        print(f"  Total traditions: {selection_index.total_traditions}")
        
        # Show sample tradition summary
        if selection_index.tradition_summaries:
            sample_name = next(iter(selection_index.tradition_summaries.keys()))
            sample_summary = selection_index.tradition_summaries[sample_name]
            print(f"\n  Sample tradition: {sample_summary.display_name}")
            print(f"    Concepts: {sample_summary.key_concepts_count}")
            print(f"    Wisdom teachings: {sample_summary.wisdom_teachings_count}")
            print(f"    Quality: {sample_summary.quality_rating}")
            print(f"    Personality traits: {len(sample_summary.personality_influence)}")
        
        # Show recommendations summary
        print(f"\n  Selection Recommendations:")
        for category, traditions in selection_index.selection_recommendations.items():
            if traditions:
                print(f"    {category}: {len(traditions)} traditions")
        
        # Save selection index
        print(f"\nSaving tradition selection index...")
        success = indexer.save_selection_index()
        if success:
            print("Tradition selection index saved successfully!")
        
        print(f"\nTradition Selection Indexer system test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 