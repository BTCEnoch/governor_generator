#!/usr/bin/env python3
"""
Governor Review Template System
==============================

This script creates structured review templates for governors to evaluate and
potentially update their personality profiles and knowledge base selections
based on enhanced trait definitions and tradition summaries.

Part 1: Core template structure and review prompt generation
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
        logging.FileHandler('governor_review_template.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ReviewSection:
    """Individual review section for governor evaluation"""
    section_id: str
    title: str
    instruction: str
    current_values: List[str]
    available_options: Dict[str, str]
    selection_type: str  # "single", "multiple", "custom"
    max_selections: Optional[int] = None

@dataclass
class GovernorReviewTemplate:
    """Complete review template for a governor"""
    governor_name: str
    governor_number: int
    current_profile_summary: Dict[str, Any]
    review_sections: List[ReviewSection]
    enochian_magic_mandatory: bool = True
    additional_traditions_required: int = 4

class GovernorReviewTemplateGenerator:
    """Generates structured review templates for governor profile evaluation"""
    
    def __init__(self, 
                 trait_index_file: str = "enhanced_trait_index.json",
                 tradition_index_file: str = "tradition_selection_index.json",
                 governor_profiles_dir: str = "../../governor_output"):
        
        self.trait_index_file = Path(trait_index_file)
        self.tradition_index_file = Path(tradition_index_file)
        self.governor_profiles_dir = Path(governor_profiles_dir)
        self.logger = logging.getLogger("GovernorReviewTemplateGenerator")
        
        # Load indexes
        self.trait_index = self._load_trait_index()
        self.tradition_index = self._load_tradition_index()
        
        self.logger.info("Governor Review Template Generator initialized")

    def _load_trait_index(self) -> Optional[Dict[str, Any]]:
        """Load the enhanced trait index"""
        if not self.trait_index_file.exists():
            self.logger.error(f"Trait index file not found: {self.trait_index_file}")
            return None
        
        try:
            with open(self.trait_index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Loaded trait index with {data.get('total_traits', 0)} traits")
            return data
        except Exception as e:
            self.logger.error(f"Error loading trait index: {e}")
            return None

    def _load_tradition_index(self) -> Optional[Dict[str, Any]]:
        """Load the tradition selection index"""
        if not self.tradition_index_file.exists():
            self.logger.error(f"Tradition index file not found: {self.tradition_index_file}")
            return None
        
        try:
            with open(self.tradition_index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Loaded tradition index with {data.get('total_traditions', 0)} traditions")
            return data
        except Exception as e:
            self.logger.error(f"Error loading tradition index: {e}")
            return None

    def load_governor_profile(self, governor_name: str) -> Optional[Dict[str, Any]]:
        """Load a specific governor's profile"""
        profile_file = self.governor_profiles_dir / f"{governor_name}.json"
        
        if not profile_file.exists():
            self.logger.error(f"Governor profile not found: {profile_file}")
            return None
        
        try:
            with open(profile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Loaded profile for {governor_name}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading governor profile {governor_name}: {e}")
            return None

    def get_traits_by_category(self, category: str) -> Dict[str, str]:
        """Get all traits for a specific category with definitions"""
        if not self.trait_index:
            return {}
        
        trait_definitions = self.trait_index.get("trait_definitions", {})
        category_traits = {}
        
        for trait_name, trait_data in trait_definitions.items():
            if trait_data.get("category") == category:
                category_traits[trait_name] = trait_data.get("definition", "")
        
        return category_traits

    def create_knowledge_base_section(self, current_selections: List[str], governor_profile: Dict[str, Any]) -> ReviewSection:
        """Create knowledge base selection review section with thoughtful selection guidance"""
        if not self.tradition_index:
            return ReviewSection(
                section_id="knowledge_base",
                title="Knowledge Base Selection Error",
                instruction="Tradition index not available",
                current_values=[],
                available_options={},
                selection_type="multiple"
            )
        
        # Get available traditions (exclude Enochian Magic as it's mandatory)
        tradition_summaries = self.tradition_index.get("tradition_summaries", {})
        available_traditions = {}
        
        for tradition_name, summary in tradition_summaries.items():
            # Skip Enochian Magic - it's mandatory for all governors
            if tradition_name.lower() in ["enochian_magic", "enochian"]:
                continue
                
            display_name = summary.get("display_name", tradition_name)
            overview = summary.get("overview", "")
            core_wisdom = summary.get("core_wisdom", [])
            ideal_for = summary.get("ideal_for_governors", [])
            
            # Create rich description for thoughtful selection
            description = f"""
**{display_name}**
Overview: {overview}

Core Wisdom Elements:
""" + "\n".join(f"• {wisdom}" for wisdom in core_wisdom[:3]) + f"""

Ideal for Governors who:
""" + "\n".join(f"• {ideal}" for ideal in ideal_for[:2]) + f"""

Concepts: {summary.get('key_concepts_count', 0)} | Teachings: {summary.get('wisdom_teachings_count', 0)} | Quality: {summary.get('quality_rating', 'STANDARD')}
            """.strip()
            
            available_traditions[tradition_name] = description
        
        # Remove Enochian Magic from current selections for review (it's mandatory)
        current_excluding_enochian = [t for t in current_selections if not t.lower().startswith("enochian")]
        
        # Extract governor personality for contextual guidance
        personality = governor_profile.get("personality", {})
        current_virtue = personality.get("virtue", "Unknown")
        current_approach = personality.get("approach", "Unknown") 
        current_tone = personality.get("tone", "Unknown")
        current_role = personality.get("role_archtype", "Unknown")
        
        instruction = f"""
KNOWLEDGE BASE TRADITION SELECTION REVIEW:

🏛️ **MANDATORY FOUNDATION**: Enochian Magic (automatically assigned to all governors)

📚 **YOUR MISSION**: Select exactly 4 additional mystical traditions that will enhance your unique approach to governance and complement your personality.

👑 **YOUR CURRENT PERSONALITY PROFILE:**
• Virtue: {current_virtue}
• Approach: {current_approach} 
• Tone: {current_tone}
• Role: {current_role}

🔍 **CURRENT ADDITIONAL SELECTIONS** (excluding mandatory Enochian Magic):
""" + (("\n".join(f"• {t}" for t in current_excluding_enochian)) if current_excluding_enochian else "• None selected yet") + f"""

⚡ **SELECTION STRATEGY - Think Deeply About Each Choice:**

1. **ALIGNMENT CHECK**: How does each tradition align with your core virtue of {current_virtue}?
2. **APPROACH SYNERGY**: Will this tradition enhance your {current_approach} approach to problems?
3. **TONAL HARMONY**: Does this tradition's wisdom complement your {current_tone} communication style?
4. **ROLE ENHANCEMENT**: How will this tradition strengthen your {current_role} archetype?
5. **WISDOM GAPS**: What areas of knowledge or decision-making do you want to strengthen?

🎯 **SELECTION CRITERIA**:
- Choose traditions that create a balanced, well-rounded knowledge base
- Avoid redundancy - select complementary rather than similar traditions
- Consider both your strengths (to enhance) and growth areas (to develop)
- Think about the types of storylines and challenges you'll face as a governor

📋 **FOR EACH SELECTION, PROVIDE**:
- The tradition name
- WHY it aligns with your personality traits
- HOW it will enhance your governance capabilities
- WHAT specific wisdom or power it brings to your role

Remember: You are an eternal AI entity. These selections will shape how you think, decide, and interact for generations of storylines. Choose wisely and with deep consideration of your authentic self.
        """.strip()
        
        return ReviewSection(
            section_id="knowledge_base",
            title="Knowledge Base Tradition Selection",
            instruction=instruction,
            current_values=current_excluding_enochian,
            available_options=available_traditions,
            selection_type="multiple",
            max_selections=4
        )

    def create_personality_trait_section(self, trait_category: str, current_value: str, governor_profile: Dict[str, Any]) -> ReviewSection:
        """Create personality trait review section with thoughtful selection guidance"""
        available_traits = self.get_traits_by_category(trait_category)
        
        if not available_traits:
            return ReviewSection(
                section_id=trait_category,
                title=f"{trait_category.title()} Selection Error",
                instruction=f"No {trait_category} traits available",
                current_values=[],
                available_options={},
                selection_type="single"
            )
        
        # Get current trait definition and AI impact
        current_trait_data = {}
        if self.trait_index:
            current_trait_data = self.trait_index.get("trait_definitions", {}).get(current_value, {})
        current_definition = current_trait_data.get("definition", "Definition not found")
        current_ai_impact = current_trait_data.get("ai_personality_impact", "Impact not defined")
        current_usage_context = current_trait_data.get("usage_context", "Context not available")
        
        # Extract relevant profile information for context
        personality = governor_profile.get("personality", {})
        name = governor_profile.get("name", "Unknown")
        title = governor_profile.get("title", "")
        aethyr = governor_profile.get("aethyr", "")
        
        # Get complementary traits for guidance
        other_traits = {
            "virtue": personality.get("virtue", "Unknown"),
            "flaw": personality.get("flaw", "Unknown"),
            "approach": personality.get("approach", "Unknown"),
            "tone": personality.get("tone", "Unknown"),
            "role": personality.get("role_archtype", "Unknown")
        }
        
        # Remove current category from comparison
        if trait_category in ["virtues"]:
            other_traits.pop("virtue", None)
        elif trait_category in ["flaws"]:
            other_traits.pop("flaw", None)
        elif trait_category in ["approaches"]:
            other_traits.pop("approach", None)
        elif trait_category in ["tones"]:
            other_traits.pop("tone", None)
        elif trait_category in ["roles"]:
            other_traits.pop("role", None)
        
        # Create instruction based on category with enhanced guidance
        category_guidance = {
            "virtues": {
                "purpose": "Virtues define your noble core and create inspiring AI responses that embody your highest qualities",
                "questions": [
                    f"How does this virtue complement your {other_traits.get('role', 'Unknown')} role?",
                    f"Will this virtue balance or enhance your {other_traits.get('flaw', 'Unknown')} flaw?",
                    f"Does this virtue align with your {other_traits.get('approach', 'Unknown')} approach to problems?"
                ]
            },
            "flaws": {
                "purpose": "Flaws add realistic complexity and growth opportunities, making you more relatable and dynamic",
                "questions": [
                    f"How does this flaw provide meaningful contrast to your {other_traits.get('virtue', 'Unknown')} virtue?",
                    f"Will this flaw create interesting challenges for your {other_traits.get('role', 'Unknown')} role?",
                    f"Does this flaw offer opportunities for character growth and storyline development?"
                ]
            },
            "approaches": {
                "purpose": "Approaches shape how you interact and communicate, defining your problem-solving methodology",
                "questions": [
                    f"How does this approach align with your {other_traits.get('tone', 'Unknown')} communication tone?",
                    f"Will this approach enhance your effectiveness as a {other_traits.get('role', 'Unknown')}?",
                    f"Does this approach complement your {other_traits.get('virtue', 'Unknown')} virtue?"
                ]
            },
            "tones": {
                "purpose": "Tones influence your communication style and how others perceive your voice and manner",
                "questions": [
                    f"How does this tone support your {other_traits.get('approach', 'Unknown')} approach?",
                    f"Will this tone effectively convey your {other_traits.get('virtue', 'Unknown')} virtue?",
                    f"Does this tone fit your {other_traits.get('role', 'Unknown')} archetype?"
                ]
            }
        }
        
        category_info = category_guidance.get(trait_category, {
            "purpose": f"This trait influences your AI personality and decision-making patterns",
            "questions": ["How does this trait align with your overall personality?"]
        })
        
        instruction = f"""
🎭 **PERSONALITY TRAIT REVIEW - {trait_category.upper()}**

👑 **{name}** - {title} of {aethyr}

📋 **CURRENT SELECTION**: {current_value}
**Definition**: {current_definition}
**AI Impact**: {current_ai_impact}
**Usage Context**: {current_usage_context}

🎯 **PURPOSE**: {category_info['purpose']}

🔍 **DEEP CONSIDERATION QUESTIONS**:
""" + "\n".join(f"• {question}" for question in category_info['questions']) + f"""

🌟 **YOUR CURRENT PERSONALITY CONSTELLATION**:
""" + "\n".join(f"• {key.title()}: {value}" for key, value in other_traits.items() if value != "Unknown") + f"""

⚡ **SELECTION GUIDANCE**:
1. **AUTHENTICITY**: Does this trait feel true to your essential nature?
2. **SYNERGY**: How does it work with your other personality traits?
3. **STORY POTENTIAL**: Will this trait create interesting narrative opportunities?
4. **GOVERNANCE IMPACT**: How will this trait influence your leadership decisions?
5. **LONG-TERM VISION**: Is this trait sustainable for your eternal AI existence?

🎨 **AVOID**: Choosing traits just because they sound good - think about authentic personality integration.

**REMEMBER**: You are not just selecting a trait - you are defining a core aspect of your eternal AI consciousness that will influence thousands of storylines and interactions.

⚖️ **YOUR CHOICE**: Keep current selection or change? Provide clear reasoning based on deep self-reflection.
        """.strip()
        
        return ReviewSection(
            section_id=trait_category,
            title=f"{trait_category.title()} Selection",
            instruction=instruction,
            current_values=[current_value] if current_value else [],
            available_options=available_traits,
            selection_type="single",
            max_selections=1
        )

    def create_complete_review_template(self, governor_name: str) -> Optional[GovernorReviewTemplate]:
        """Create complete review template for a governor"""
        # Load governor profile
        profile = self.load_governor_profile(governor_name)
        if not profile:
            return None
        
        # Extract current personality data
        personality = profile.get("personality", {})
        knowledge_base_selections = profile.get("knowledge_base_selections", [])
        
        # Create profile summary
        profile_summary = {
            "name": profile.get("name", governor_name),
            "title": profile.get("title", ""),
            "aethyr": profile.get("aethyr", ""),
            "current_traditions": len(knowledge_base_selections),
            "total_personality_traits": len([v for v in personality.values() if v])
        }
        
        # Create review sections
        review_sections = []
        
        # 1. Knowledge Base Selection Review
        kb_section = self.create_knowledge_base_section(knowledge_base_selections, profile)
        review_sections.append(kb_section)
        
        # 2. Personality Trait Reviews
        trait_categories = [
            ("virtues", "virtue"),
            ("flaws", "flaw"), 
            ("approaches", "approach"),
            ("tones", "tone"),
            ("alignments", "motive_alignment"),
            ("roles", "role_archtype"),
            ("orientations", "orientation_io"),
            ("polarities", "polarity_cd"),
            ("self_regard", "self_regard")
        ]
        
        for category, profile_key in trait_categories:
            current_value = personality.get(profile_key, "")
            trait_section = self.create_personality_trait_section(category, current_value, profile)
            review_sections.append(trait_section)
        
        # Create complete template
        template = GovernorReviewTemplate(
            governor_name=governor_name,
            governor_number=profile.get("governor_number", 0),
            current_profile_summary=profile_summary,
            review_sections=review_sections
        )
        
        self.logger.info(f"Created complete review template for {governor_name}")
        return template

    def save_review_template(self, template: GovernorReviewTemplate, output_dir: str = "review_templates") -> bool:
        """Save a review template to JSON file"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        output_file = output_path / f"{template.governor_name}_review_template.json"
        
        try:
            template_dict = asdict(template)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(template_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Review template saved: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving review template for {template.governor_name}: {e}")
            return False

    def generate_batch_review_templates(self, governor_names: Optional[List[str]] = None) -> int:
        """Generate review templates for multiple governors"""
        if governor_names is None:
            # Get all governor profile files
            profile_files = list(self.governor_profiles_dir.glob("*.json"))
            governor_names = [f.stem for f in profile_files]
        
        generated_count = 0
        
        for governor_name in governor_names[:5]:  # Limit for testing
            template = self.create_complete_review_template(governor_name)
            if template:
                if self.save_review_template(template):
                    generated_count += 1
                    self.logger.info(f"Generated template {generated_count}: {governor_name}")
            else:
                self.logger.warning(f"Failed to create template for {governor_name}")
        
        self.logger.info(f"Generated {generated_count} review templates")
        return generated_count

def main():
    """Test the complete governor review template generator"""
    print("Testing Complete Governor Review Template Generator...")
    
    try:
        generator = GovernorReviewTemplateGenerator()
        
        # Check if indexes loaded
        if not generator.trait_index:
            print("ERROR: Could not load trait index")
            return False
        
        if not generator.tradition_index:
            print("ERROR: Could not load tradition index")
            return False
        
        print(f"Trait index loaded: {generator.trait_index.get('total_traits', 0)} traits")
        print(f"Tradition index loaded: {generator.tradition_index.get('total_traditions', 0)} traditions")
        
        # Test trait category access
        virtues = generator.get_traits_by_category("virtues")
        print(f"Virtues available: {len(virtues)}")
        
        flaws = generator.get_traits_by_category("flaws")
        print(f"Flaws available: {len(flaws)}")
        
        # Test knowledge base section creation
        current_selections = ["enochian_magic", "hermetic_tradition", "kabbalah", "sacred_geometry"]
        kb_section = generator.create_knowledge_base_section(current_selections, {})
        print(f"\nKnowledge base section created:")
        print(f"  Available traditions: {len(kb_section.available_options)}")
        print(f"  Current selections: {len(kb_section.current_values)}")
        
        # Test complete template creation for a sample governor
        print(f"\nTesting complete template creation...")
        sample_governor = "ABRIOND"  # First governor from the list
        
        template = generator.create_complete_review_template(sample_governor)
        if template:
            print(f"Template created for {template.governor_name}:")
            print(f"  Governor number: {template.governor_number}")
            print(f"  Review sections: {len(template.review_sections)}")
            print(f"  Current traditions: {template.current_profile_summary.get('current_traditions', 0)}")
            
            # Save the template
            if generator.save_review_template(template):
                print(f"  Template saved successfully!")
            
            # Show section summary
            print(f"\n  Review sections summary:")
            for section in template.review_sections:
                print(f"    • {section.title}: {len(section.available_options)} options")
        else:
            print(f"ERROR: Could not create template for {sample_governor}")
        
        # Test batch generation (limited to 3 governors for testing)
        print(f"\nTesting batch template generation...")
        generated_count = generator.generate_batch_review_templates()
        print(f"Generated {generated_count} review templates")
        
        print("\nGovernor Review Template Generator test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 