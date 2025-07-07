"""
Builds and compiles governor interactions for on-chain storage.
This system works with the AI during development to generate and store all possible
governor interactions and responses that will be needed during gameplay.
"""

import json
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Any
from pathlib import Path

@dataclass
class InteractionPattern:
    """Defines a specific way a governor can interact"""
    pattern_id: str
    trigger_conditions: List[str]
    response_templates: List[str]
    trait_requirements: List[str]
    knowledge_references: List[str]

@dataclass
class KnowledgeFragment:
    """A piece of knowledge the governor can reference"""
    fragment_id: str
    content: str
    tags: List[str]
    related_fragments: List[str]
    source_tradition: str

class OnchainInteractionBuilder:
    """Builds complete interaction libraries for governors to be stored on-chain"""
    
    def __init__(self, trait_interpreter, output_dir: Path):
        self.logger = logging.getLogger(__name__)
        self.trait_interpreter = trait_interpreter
        self.output_dir = output_dir
        self.patterns: Dict[str, InteractionPattern] = {}
        self.knowledge: Dict[str, KnowledgeFragment] = {}
        
    def build_interaction_library(self, governor_name: str, binary_traits: bytes) -> Dict:
        """Build complete interaction library for a governor
        
        This is run during development to create the full set of possible
        interactions that will be stored on-chain.
        
        Args:
            governor_name: Name of the governor
            binary_traits: Binary trait data
            
        Returns:
            Dictionary containing all interaction patterns and knowledge
        """
        self.logger.info(f"Building interaction library for {governor_name}")
        
        # Get trait understanding
        traits = self.trait_interpreter.interpret_binary_traits(binary_traits)
        
        # Build basic interaction patterns
        self._build_basic_patterns(traits)
        
        # Build knowledge fragments
        self._build_knowledge_fragments(traits)
        
        # Generate response templates
        self._generate_response_templates(traits)
        
        # Build final library
        library = {
            "governor": governor_name,
            "traits": self._encode_traits_for_chain(binary_traits),
            "patterns": self._compile_patterns(),
            "knowledge": self._compile_knowledge(),
            "index": self._build_search_index()
        }
        
        # Save to file
        self._save_library(governor_name, library)
        
        return library
        
    def _build_basic_patterns(self, traits: List[Any]) -> None:
        """Build basic interaction patterns based on traits"""
        for trait in traits:
            # Create greeting pattern
            self.patterns[f"greet_{trait.name}"] = InteractionPattern(
                pattern_id=f"greet_{trait.name}",
                trigger_conditions=["first_interaction", "returning_after_break"],
                response_templates=[
                    f"Greets with {trait.name.lower()} energy",
                    f"Welcomes showing {trait.definition.lower()}"
                ],
                trait_requirements=[trait.name],
                knowledge_references=[]
            )
            
            # Create teaching pattern
            self.patterns[f"teach_{trait.name}"] = InteractionPattern(
                pattern_id=f"teach_{trait.name}",
                trigger_conditions=["asked_about_trait", "showing_interest"],
                response_templates=[
                    f"Explains the nature of {trait.name.lower()}",
                    f"Demonstrates {trait.definition.lower()} through example"
                ],
                trait_requirements=[trait.name],
                knowledge_references=[f"nature_of_{trait.name.lower()}"]
            )
            
    def _build_knowledge_fragments(self, traits: List[Any]) -> None:
        """Build knowledge fragments based on traits"""
        for trait in traits:
            # Create basic trait knowledge
            self.knowledge[f"nature_of_{trait.name.lower()}"] = KnowledgeFragment(
                fragment_id=f"nature_of_{trait.name.lower()}",
                content=trait.definition,
                tags=[trait.category, "basic_knowledge"],
                related_fragments=[],
                source_tradition=trait.mystical_correspondences.get("tradition", "unknown")
                if trait.mystical_correspondences else "unknown"
            )
            
            # Create usage knowledge
            self.knowledge[f"using_{trait.name.lower()}"] = KnowledgeFragment(
                fragment_id=f"using_{trait.name.lower()}",
                content=trait.usage_context,
                tags=[trait.category, "practical_application"],
                related_fragments=[f"nature_of_{trait.name.lower()}"],
                source_tradition=trait.mystical_correspondences.get("tradition", "unknown")
                if trait.mystical_correspondences else "unknown"
            )
            
    def _generate_response_templates(self, traits: List[Any]) -> None:
        """Generate response templates for different situations"""
        # Add response patterns based on trait combinations
        for i, trait1 in enumerate(traits):
            for trait2 in traits[i+1:]:
                pattern_id = f"combine_{trait1.name}_{trait2.name}"
                self.patterns[pattern_id] = InteractionPattern(
                    pattern_id=pattern_id,
                    trigger_conditions=["multiple_traits_relevant"],
                    response_templates=[
                        f"Shows how {trait1.name} and {trait2.name} work together",
                        f"Demonstrates the harmony between {trait1.definition} and {trait2.definition}"
                    ],
                    trait_requirements=[trait1.name, trait2.name],
                    knowledge_references=[
                        f"nature_of_{trait1.name.lower()}", 
                        f"nature_of_{trait2.name.lower()}"
                    ]
                )
                
    def _encode_traits_for_chain(self, binary_traits: bytes) -> str:
        """Encode binary traits for on-chain storage"""
        return binary_traits.hex()
        
    def _compile_patterns(self) -> Dict:
        """Compile all interaction patterns for on-chain storage"""
        return {
            pattern_id: {
                "triggers": pattern.trigger_conditions,
                "responses": pattern.response_templates,
                "requires": pattern.trait_requirements,
                "refs": pattern.knowledge_references
            }
            for pattern_id, pattern in self.patterns.items()
        }
        
    def _compile_knowledge(self) -> Dict:
        """Compile all knowledge fragments for on-chain storage"""
        return {
            fragment_id: {
                "content": fragment.content,
                "tags": fragment.tags,
                "related": fragment.related_fragments,
                "source": fragment.source_tradition
            }
            for fragment_id, fragment in self.knowledge.items()
        }
        
    def _build_search_index(self) -> Dict:
        """Build search index for finding relevant patterns and knowledge"""
        index = {
            "by_trait": {},
            "by_tag": {},
            "by_tradition": {}
        }
        
        # Index patterns by trait
        for pattern in self.patterns.values():
            for trait in pattern.trait_requirements:
                if trait not in index["by_trait"]:
                    index["by_trait"][trait] = {"patterns": [], "knowledge": []}
                index["by_trait"][trait]["patterns"].append(pattern.pattern_id)
                
        # Index knowledge by tags and traditions
        for fragment in self.knowledge.values():
            # By tag
            for tag in fragment.tags:
                if tag not in index["by_tag"]:
                    index["by_tag"][tag] = []
                index["by_tag"][tag].append(fragment.fragment_id)
                
            # By tradition
            if fragment.source_tradition not in index["by_tradition"]:
                index["by_tradition"][fragment.source_tradition] = []
            index["by_tradition"][fragment.source_tradition].append(fragment.fragment_id)
            
            # Add to trait index
            for trait, trait_index in index["by_trait"].items():
                if trait.lower() in fragment.content.lower():
                    trait_index["knowledge"].append(fragment.fragment_id)
                    
        return index
        
    def _save_library(self, governor_name: str, library: Dict) -> None:
        """Save interaction library to file"""
        output_file = self.output_dir / f"{governor_name}_interactions.json"
        
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with output_file.open('w', encoding='utf-8') as f:
                json.dump(library, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved interaction library to {output_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving library: {e}")
            raise 