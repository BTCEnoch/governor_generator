"""
Generate complete governor index by processing all governor files.
"""

import json
import os
from collections import defaultdict
from typing import Dict, List, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class GovernorData:
    """Structure for organizing governor data"""
    id: str
    title: str
    element: str
    aethyr: str
    role: str
    virtues: List[str]
    flaws: List[str]
    approaches: Dict[str, str]
    tones: Dict[str, str]
    motive: str
    role_archetype: str
    orientation: str
    polarity: str
    knowledge_base: List[str]
    correspondences: Dict[str, str]
    visual_aspects: Dict[str, Any]

class IndexGenerator:
    """Generates complete governor index"""
    
    def __init__(self, dossier_path: str, output_path: str):
        self.dossier_path = Path(dossier_path)
        self.output_path = Path(output_path)
        self.governors: Dict[str, GovernorData] = {}
        self.aethyr_map: Dict[str, List[str]] = defaultdict(list)
        self.element_map: Dict[str, List[str]] = defaultdict(list)
        self.correspondence_map: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        
    def load_governor_files(self):
        """Load all governor JSON files"""
        for file in self.dossier_path.glob("*.json"):
            if file.stem == "visual_aspects_generation_results":
                continue
            
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if "governor_id" not in data:
                continue
                
            # Get persona data which contains most attributes
            persona = data.get("persona", {})
            
            gov_id = data["governor_id"]
            self.governors[gov_id] = GovernorData(
                id=gov_id,
                title=persona.get("title", ""),
                element=persona.get("element", ""),
                aethyr=persona.get("aethyr", ""),
                role=persona.get("angelic_role", ""),
                virtues=persona.get("polar_traits", {}).get("virtues", []),
                flaws=persona.get("polar_traits", {}).get("flaws", []),
                approaches=persona.get("approaches", {}),
                tones=persona.get("tones", {}),
                motive=persona.get("polar_traits", {}).get("motive_alignment", ""),
                role_archetype=persona.get("polar_traits", {}).get("role_archetype", ""),
                orientation=persona.get("polar_traits", {}).get("orientation", ""),
                polarity=persona.get("polar_traits", {}).get("polarity", ""),
                knowledge_base=persona.get("knowledge_base", []),
                correspondences=persona.get("archetypal_correspondences", {}),
                visual_aspects=data.get("visual_aspects", {})
            )
            
            # Build mapping indexes
            self.aethyr_map[persona.get("aethyr", "")].append(gov_id)
            self.element_map[persona.get("element", "")].append(gov_id)
            
            # Map correspondences
            corr = persona.get("archetypal_correspondences", {})
            for k, v in corr.items():
                self.correspondence_map[k][v].append(gov_id)
    
    def generate_governor_section(self, gov: GovernorData) -> str:
        """Generate markdown for a single governor"""
        return f"""
### {gov.id}
**Title**: {gov.title}
**Element**: {gov.element}
**Aethyr**: {gov.aethyr}
**Role**: {gov.role}

#### Core Traits
- **Virtues**: {', '.join(gov.virtues)}
- **Flaws**: {', '.join(gov.flaws)}
- **Approach**: {gov.approaches.get('average', 'Unknown')} (Average), {gov.approaches.get('good', 'Unknown')} (Good)
- **Tone**: {gov.tones.get('average', 'Unknown')} (Average), {gov.tones.get('good', 'Unknown')} (Good)

#### Mystical Aspects
- **Motive**: {gov.motive}
- **Role**: {gov.role_archetype}
- **Orientation**: {gov.orientation}
- **Polarity**: {gov.polarity}

#### Knowledge Base
{chr(10).join(f'- {k}' for k in gov.knowledge_base)}

#### Correspondences
- **Tarot**: {gov.correspondences.get('tarot', 'Unknown')}
- **Sephirot**: {gov.correspondences.get('sephirot', 'Unknown')}
- **Zodiac**: {gov.correspondences.get('zodiac_sign', 'Unknown')}
- **Angel**: {gov.correspondences.get('zodiac_angel', 'Unknown')}
- **Number**: {gov.correspondences.get('numerology', 'Unknown')}
"""

    def generate_aethyr_section(self) -> str:
        """Generate markdown for Aethyric organization"""
        sections = []
        for aethyr in sorted(self.aethyr_map.keys()):
            if not aethyr:  # Skip empty aethyr
                continue
            governors = self.aethyr_map[aethyr]
            gov_list = [f"{gov} - {self.governors[gov].title.strip('\'"')}" 
                       for gov in governors if gov in self.governors]
            
            sections.append(f"""
### {aethyr}
**Governors**:
{chr(10).join(f'{i+1}. {g}' for i, g in enumerate(gov_list))}
""")
        return "\n".join(sections)

    def generate_element_section(self) -> str:
        """Generate markdown for element mappings"""
        sections = []
        for element in sorted(self.element_map.keys()):
            if not element:  # Skip empty element
                continue
            governors = self.element_map[element]
            gov_list = [f"{gov} ({self.governors[gov].aethyr}) - {self.governors[gov].title.strip('\'"')}"
                       for gov in governors if gov in self.governors]
            
            sections.append(f"""
### {element}
{chr(10).join(f'- {g}' for g in gov_list)}
""")
        return "\n".join(sections)

    def generate_correspondence_section(self) -> str:
        """Generate markdown for archetypal correspondences"""
        sections = []
        for corr_type, mappings in self.correspondence_map.items():
            section = [f"\n### {corr_type.replace('_', ' ').title()} Associations"]
            for value, governors in sorted(mappings.items()):
                if not value:  # Skip empty values
                    continue
                gov_list = [f"{gov}" for gov in governors if gov in self.governors]
                section.append(f"- **{value}**: {', '.join(gov_list)}")
            sections.append("\n".join(section))
        return "\n".join(sections)

    def generate_index(self):
        """Generate the complete index file"""
        self.load_governor_files()
        
        # Generate sections
        governor_section = "\n".join(self.generate_governor_section(gov) 
                                   for gov in self.governors.values())
        aethyr_section = self.generate_aethyr_section()
        element_section = self.generate_element_section()
        correspondence_section = self.generate_correspondence_section()
        
        # Combine into final document
        with open(self.output_path / "COMPLETE_GOVERNOR_INDEX.md", 'w', encoding='utf-8') as f:
            f.write(f"""# 📚 Complete Governor Index

## 🗂️ Table of Contents
1. [Visual Traits Reference](#visual-traits-reference)
2. [Governor Directory](#governor-directory)
3. [Aethyric Organization](#aethyric-organization)
4. [Element Mappings](#element-mappings)
5. [Archetypal Correspondences](#archetypal-correspondences)
6. [Manifestation Patterns](#manifestation-patterns)

## 📖 How to Use This Index
This document serves as the master index for all governor-related information. Each section provides different ways to access and understand governor data:

- Use Visual Traits Reference for understanding appearance and manifestation
- Use Governor Directory for individual governor details
- Use Aethyric Organization for hierarchical relationships
- Use Element Mappings for elemental associations
- Use Archetypal Correspondences for symbolic meanings
- Use Manifestation Patterns for ritual work

## 🎭 Visual Traits Reference
[See VISUAL_TRAIT_INDEX.md for complete details]

## 📑 Governor Directory
{governor_section}

## 🔮 Aethyric Organization
{aethyr_section}

## 🌟 Element Mappings
{element_section}

## 🎴 Archetypal Correspondences
{correspondence_section}

## ✨ Manifestation Patterns
[To be populated when governors define their visual aspects]

---

# 📝 Notes on Usage

1. **For Ritual Work**:
   - Check governor's element and Aethyr
   - Review manifestation patterns
   - Note correspondences
   - Consider polarity and orientation

2. **For Research**:
   - Start with Aethyric organization
   - Cross-reference with elements
   - Check archetypal correspondences
   - Review individual governor details

3. **For Practical Application**:
   - Begin with governor's approach and tone
   - Note virtues and flaws
   - Consider knowledge base
   - Review manifestation triggers

---

*This index is maintained as part of the Enochian Governor Generation project. Updates are made as new information is discovered or verified.*
""")

if __name__ == "__main__":
    generator = IndexGenerator(
        dossier_path="governor_dossier",
        output_path="data/governors/indexes"
    )
    generator.generate_index() 