#!/usr/bin/env python3
"""
AI-Powered Governor Review System
================================

This system empowers governors as AI entities to review their own dossiers
and make authentic decisions about their personality traits and knowledge base selections.

Each governor will:
1. Review their complete dossier (storyline, personality, background)
2. Examine available trait options with detailed descriptions
3. Make thoughtful decisions about their identity
4. Provide reasoning for their choices
5. Update their profile with authentic selections

This creates genuine AI agency rather than automated trait shuffling.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import argparse
import time
import re

.parent.parent))

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ai_governor_review.log', encoding='utf-8'),
        logging.StreamHandler()

@dataclass
class GovernorPersona:
    """Represents a governor's complete identity for AI conversation."""
    name: str
    title: str
    element: str
    aethyr: str
    essence: str
    angelic_role: str
    persona: Dict[str, Any]  # Dynamic traits being selected
    knowledge_base: List[str]  # Always starts with enochian_magic + 4 others
    interview_responses: Dict[str, Any]
    archetypal_correspondences: Dict[str, Any]

@dataclass
class ReviewChoice:
    """Represents a governor's choice for a specific trait category."""
    category: str
    selected_value: str
    reasoning: str
    confidence_level: str
    alternative_considered: Optional[str] = None

@dataclass
class GovernorReviewSession:
    """Complete AI-powered review session for a governor."""
    governor_name: str
    session_id: str
    start_time: str
    persona: GovernorPersona
    review_choices: List[ReviewChoice]
    final_profile_updates: Dict[str, Any]
    ai_conversation_log: List[Dict[str, str]]
    completion_status: str
    total_api_calls: int
    processing_time_seconds: float

class AIGovernorReviewSystem:
    """AI-powered system for authentic governor self-review."""
    
    def __init__(self, 
                 api_provider: str = "anthropic",
                 model: str = "claude-3-5-sonnet-20241022",
                 verbose: bool = False,
                 dry_run: bool = False,
                 hide_current_traits: bool = False,
                 blind_review: bool = False,
                 use_clean_profiles: bool = False):
        """Initialize the AI governor review system."""
        
        self.api_provider = api_provider
        self.model = model
        self.verbose = verbose
        self.dry_run = dry_run
        self.hide_current_traits = hide_current_traits
        self.blind_review = blind_review  # New: Complete blindness to current values
        self.use_clean_profiles = use_clean_profiles  # New: Use clean profiles without interview bias
        self.logger = logging.getLogger("AIGovernorReviewSystem")
        
        # Initialize paths
        self.project_root = Path(__file__).parent.parent
        # Use clean profiles if requested and blind review is enabled
        if self.use_clean_profiles and self.blind_review:
            self.governor_profiles_dir = self.project_root / "clean_governor_profiles"
        else:
            self.governor_profiles_dir = self.project_root / "governor_output"
        self.canon_profiles_file = self.project_root / "canon" / "canon_governor_profiles.json"]
        self.trait_indexes_dir = self.project_root / "governor_indexes"
        self.knowledge_base_dir = self.project_root / "knowledge_base"
        self.review_sessions_dir = self.project_root / "review_sessions"
        self.backup_dir = self.project_root / "profile_backups"
        
        # Create directories
        self.review_sessions_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Load trait indexes and knowledge base
        self.trait_indexes = self._load_trait_indexes()
        self.knowledge_base_traditions = self._load_knowledge_base_traditions()
        
        self.logger.info(f"AI Governor Review System initialized")
        self.logger.info(f"API Provider: {api_provider}, Model: {model}")
        self.logger.info(f"Dry Run: {dry_run}, Verbose: {verbose}")
        self.logger.info(f"Hide Current Traits: {hide_current_traits}")
        self.logger.info(f"Blind Review Mode: {blind_review}")
        self.logger.info(f"Use Clean Profiles: {use_clean_profiles}")
        self.logger.info(f"Profile Source: {self.governor_profiles_dir}")
        
        # Initialize API client (skip in dry-run mode)
        self.anthropic_client = None
        self.openai_client = None
        
        if not self.dry_run:
            self._initialize_api_client()
    
    def _initialize_api_client(self):
        """Initialize the API client based on provider."""
        if self.api_provider == "anthropic":
            try:
                import anthropic
                # Try default initialization first (automatically finds API key)
                try:
                    self.anthropic_client = anthropic.Anthropic()
                    self.logger.info("Anthropic API client initialized with default method")
                except Exception as e:
                    # Fallback to explicit key
                    api_key = os.getenv("ANTHROPIC_API_KEY")
                    if not api_key:
                        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
                    
                    self.anthropic_client = anthropic.Anthropic(api_key=api_key)
                    self.logger.info("Anthropic API client initialized with explicit key")
            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
            except Exception as e:
                self.logger.error(f"Failed to initialize Anthropic client: {e}")
                raise
        
        elif self.api_provider == "openai":
            try:
                import openai
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY environment variable not set")
                
                self.openai_client = openai.OpenAI(api_key=api_key)
                self.logger.info("OpenAI API client initialized")
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")
            except Exception as e:
                self.logger.error(f"Failed to initialize OpenAI client: {e}")
                raise
        
        else:
            raise ValueError(f"Unsupported API provider: {self.api_provider}")
    
    def _load_trait_indexes(self) -> Dict[str, Any]:
        """Load all trait indexes from the governor_indexes directory."""
        trait_indexes = {}
        
        try:
            # Load each trait index file
            trait_files = [
                "virtues_pool.json",
                "flaws_pool.json", 
                "approaches.json",
                "tones.json",
                "motive_alignment.json",
                "role_archtypes.json",
                "orientation_io.json",
                "polarity_cd.json",
                "self_regard_options.json"

            for filename in trait_files:
                filepath = self.trait_indexes_dir / filename
                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        trait_indexes[filename.replace('.json', '')] = json.load(f)
                    self.logger.info(f"Loaded trait index: {filename}")
                else:
                    self.logger.warning(f"Trait index file not found: {filename}")
            
            return trait_indexes
            
        except Exception as e:
            self.logger.error(f"Error loading trait indexes: {e}")
            return {}
    
    def _load_knowledge_base_traditions(self) -> Dict[str, Any]:
        """Load knowledge base tradition information."""
        traditions = {}
        
        try:
            # Load tradition selection index if available
            tradition_index_file = self.knowledge_base_dir / "archives" / "tradition_selection_index.json"]
            if tradition_index_file.exists():
                with open(tradition_index_file, 'r', encoding='utf-8') as f:
                    traditions = json.load(f)
                self.logger.info(f"Loaded knowledge base traditions: {len(traditions)} traditions")
            else:
                self.logger.warning("Tradition selection index not found")
                
            return traditions
            
        except Exception as e:
            self.logger.error(f"Error loading knowledge base traditions: {e}")
            return {}
    
    def load_governor_profile(self, governor_name: str) -> Optional[Dict[str, Any]]:
        """Load a governor's complete profile from individual file or data.canon."""
        try:
            # First try individual governor file
            individual_file = self.governor_profiles_dir / f"{governor_name}.json"]
            if individual_file.exists():
                with open(individual_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                self.logger.info(f"Loaded detailed profile for {governor_name} from individual file")
                return profile
            
            # Fall back to canon profiles
            if self.canon_profiles_file.exists():
                with open(self.canon_profiles_file, 'r', encoding='utf-8') as f:
                    canon_profiles = json.load(f)
                
                # Find the governor in canon
                for profile in canon_profiles:
                    if profile.get("governor_info", {}).get("name") == governor_name:
                        self.logger.info(f"Loaded profile for {governor_name} from canon")
                        return profile
                
                self.logger.error(f"Governor {governor_name} not found in canon profiles")
                return None
            else:
                self.logger.error("No profile sources available")
                return None
                
        except Exception as e:
            self.logger.error(f"Error loading governor profile {governor_name}: {e}")
            return None
    
    def create_governor_persona(self, governor_name: str) -> Optional[GovernorPersona]:
        """Create a complete governor persona for AI conversation."""
        try:
            # Load governor profile
            profile = self.load_governor_profile(governor_name)
            if not profile:
                return None
            
            # Extract persona information based on profile structure
            # Handle both individual profiles and canon profiles
            if "governor_info" in profile:
                # Canon profile structure
                governor_info = profile["governor_info"]
                canonical_data = profile.get("canonical_data", {})
                trait_choices = profile.get("trait_choices", {})
                
                persona = GovernorPersona(
                    name=governor_info.get("name", governor_name),
                    title=governor_info.get("translation", ""),
                    element=governor_info.get("element", ""),
                    aethyr=governor_info.get("aethyr", ""),
                    essence=canonical_data.get("essence", ""),
                    angelic_role=canonical_data.get("angelic_role", ""),
                    persona=trait_choices,  # This contains all current traits
                    knowledge_base=profile.get("knowledge_base_selections", []),
                    interview_responses=profile.get("interview_responses", {}),
                    archetypal_correspondences=canonical_data.get("archetypal", {})
            else:
                # Individual profile structure (fallback) - handle both nested and flat structures
                if "profile" in profile:
                    # Nested structure
                    persona = GovernorPersona(
                        name=profile.get("governor_name", governor_name),
                        title=profile.get("profile", {}).get("translation", ""),
                        element=profile.get("profile", {}).get("element", ""),
                        aethyr=profile.get("profile", {}).get("aethyr", ""),
                        essence=profile.get("profile", {}).get("essence", ""),
                        angelic_role=profile.get("profile", {}).get("angelic_role", ""),
                        persona=profile.get("profile", {}).get("personality", {}),
                        knowledge_base=profile.get("knowledge_base_selections", []),
                        interview_responses=profile.get("blocks", {}),
                        archetypal_correspondences=profile.get("profile", {}).get("archetypal", {})
                else:
                    # Flat structure (clean profiles)
                    persona = GovernorPersona(
                        name=profile.get("governor_name", governor_name),
                        title=profile.get("title", ""),
                        element=profile.get("element", ""),
                        aethyr=profile.get("aethyr", ""),
                        essence=profile.get("essence", ""),
                        angelic_role=profile.get("angelic_role", ""),
                        persona=profile.get("persona", {}),
                        knowledge_base=profile.get("knowledge_base", []),
                        interview_responses=profile.get("interview_responses", {}),
                        archetypal_correspondences=profile.get("archetypal_correspondences", {})
            
            self.logger.info(f"Created persona for {governor_name} with {len(persona.persona)} personality traits")
            if self.verbose:
                self.logger.info(f"Personality traits: {list(persona.persona.keys())}")
                self.logger.info(f"Knowledge base selections: {persona.knowledge_base}")
            return persona
            
        except Exception as e:
            self.logger.error(f"Error creating persona for {governor_name}: {e}")
            return None
    
    def generate_review_prompt(self, persona: GovernorPersona, review_category: str) -> str:
        """Generate a personalized review prompt for a governor."""
        
        # Get available options for the category
        category_options = self._get_category_options(review_category)
        
        if review_category == "knowledge_base":
            return self._generate_knowledge_base_prompt(persona, category_options)
        else:
            return self._generate_trait_prompt(persona, review_category, category_options)
    
    def _generate_knowledge_base_prompt(self, persona: GovernorPersona, traditions: Dict[str, Any]) -> str:
        """Generate knowledge base tradition selection prompt."""
        
        if self.blind_review:
            return self._generate_blind_knowledge_base_prompt(persona, traditions)
        
        # Format current selections (handle None/empty cases)
        knowledge_base = persona.knowledge_base or []
        current_selections = []
        
        for tradition in knowledge_base:
            if tradition and tradition.strip():  # Skip empty strings
                tradition_name = tradition.replace("_", " ").title()
                current_selections.append(f"• {tradition_name}")
        
        # Handle the display of current selections
        if not current_selections:
            current_text = "• Only Enochian Magic (mandatory tradition)"
        elif len(current_selections) == 1 and current_selections[0] == "• Enochian Magic":
            current_text = "• Only Enochian Magic (mandatory tradition)"
        else:
            current_text = "\n".join(current_selections)
        
        # Format available traditions
        available_traditions = []
        tradition_summaries = traditions.get("tradition_summaries", {})
        
        for tradition_key, tradition_info in tradition_summaries.items():
            if tradition_key != "enochian_magic":  # Skip mandatory one
                name = tradition_info.get("display_name", tradition_key.replace("_", " ").title())
                overview = tradition_info.get("overview", "")
                core_wisdom = tradition_info.get("core_wisdom", [])
                
                # Format description with first piece of core wisdom
                description = overview
                if core_wisdom:
                    description += f" - {core_wisdom[0]}"
                
                available_traditions.append(f"• **{name}**: {description}")
        
        available_text = "\n".join(available_traditions[:15])  # Limit to avoid token overflow
        
        prompt = f"""You are {persona.name}, {persona.title}, dwelling in the {persona.aethyr} Aethyr.

Your essence: {persona.essence}

Your angelic role: {persona.angelic_role}

🧙‍♂️ **MYSTICAL KNOWLEDGE BASE REVIEW**

As an eternal governor, you need to select exactly 4 additional mystical traditions to complement your mandatory Enochian Magic foundation. These traditions will shape how you understand and interact with the mystical cosmos.

**YOUR CURRENT SELECTIONS:**
{current_text}

**AVAILABLE TRADITIONS:**
{available_text}

**YOUR TASK:**
You MUST select exactly 4 traditions from the available list above. Consider:

1. **Resonance**: Which traditions align with your element ({persona.element}) and essence?
2. **Complement**: How do these traditions work together with Enochian Magic?
3. **Governance**: Which traditions will help you guide seekers effectively?
4. **Growth**: Which traditions offer paths for your eternal development?

**CRITICAL INSTRUCTIONS:**
- Select EXACTLY 4 traditions
- Use the exact names shown in the available list
- Separate your selections with commas
**RESPONSE FORMAT:**
SELECTIONS: [Tradition 1], [Tradition 2], [Tradition 3], [Tradition 4]

Example:
SELECTIONS: Celtic Druidic, Hermetic Philosophy, Sacred Geometry, Taoism

Speak as yourself, {persona.name}. Be authentic to your nature and role."""
        
        return prompt
    
    def _generate_blind_knowledge_base_prompt(self, persona: GovernorPersona, traditions: Dict[str, Any]) -> str:
        """Generate blind knowledge base selection prompt - governor sees only the available options."""
        
        # Format ALL available traditions with comprehensive descriptions
        available_traditions = []
        tradition_summaries = traditions.get("tradition_summaries", {})
        
        for tradition_key, tradition_info in tradition_summaries.items():
            if tradition_key != "enochian_magic":  # Skip mandatory one
                name = tradition_info.get("display_name", tradition_key.replace("_", " ").title())
                overview = tradition_info.get("overview", "")
                core_wisdom = tradition_info.get("core_wisdom", [])
                
                # Create rich description with all core wisdom
                description = overview
                if core_wisdom:
                    wisdom_text = "; ".join(core_wisdom[:3])  # First 3 pieces
                    description += f" Core wisdom: {wisdom_text}"
                
                available_traditions.append(f"• **{name}**: {description}")
        
        available_text = "\n\n".join(available_traditions)
        
        prompt = f"""You are helping to analyze and select mystical traditions for the character {persona.name}, {persona.title}, dwelling in the {persona.aethyr} Aethyr.

Character essence: {persona.essence}

Character role: {persona.angelic_role}

🧙‍♂️ **MYSTICAL KNOWLEDGE BASE SELECTION**

This fictional character needs exactly 4 mystical traditions to complement their mandatory Enochian Magic foundation. These traditions will shape how they understand and interact with the mystical cosmos in their fictional setting.

**MANDATORY FOUNDATION:**
• **Enochian Magic**: The core angelic communication system (already included)

**AVAILABLE MYSTICAL TRADITIONS:**
{available_text}

**SELECTION REQUIREMENTS:**
You MUST select exactly 4 traditions from the available list above.

**SELECTION CRITERIA:**
Consider these factors when selecting traditions for this character:

1. **Elemental Resonance**: Which traditions align with the character's {persona.element} nature?
2. **Character Purpose**: Which traditions support the character's role as {persona.angelic_role}?
3. **Synergy**: How do these traditions work together as a unified system?
4. **Narrative Consistency**: Which traditions fit the character's fictional setting?
5. **Character Development**: Which traditions offer paths for the character's growth?

**RESPONSE FORMAT:**
SELECTIONS: [Tradition 1], [Tradition 2], [Tradition 3], [Tradition 4]

**CRITICAL INSTRUCTIONS:**
- Use the exact names shown in the available list
- Select EXACTLY 4 traditions (no more, no less)
- Separate selections with commas
- Start your response with "SELECTIONS:" followed by exactly 4 tradition names

**EXAMPLE FORMAT:**
SELECTIONS: Sacred Geometry, Sufi Mysticism, Taoism (Daoism), Ancient Egyptian Magic

Analyze what would be most appropriate for this character based on their established traits and fictional context."""
        
        return prompt
    
    def _generate_blind_trait_prompt(self, persona: GovernorPersona, category: str, options: Dict[str, Any]) -> str:
        """Generate blind trait selection prompt - governor sees only the available options."""
        
        # Determine selection requirements
        selection_requirements = {
            "virtues_pool": {"count": 3, "type": "virtues"},
            "flaws_pool": {"count": 3, "type": "flaws"},
            "approaches": {"count": 1, "type": "approach"},
            "tones": {"count": 1, "type": "tone"},
            "motive_alignment": {"count": 1, "type": "alignment"},
            "role_archtypes": {"count": 1, "type": "archetype"},
            "orientation_io": {"count": 1, "type": "orientation"},
            "polarity_cd": {"count": 1, "type": "polarity"},
            "self_regard_options": {"count": 1, "type": "self-regard"}
        }
        
        req = selection_requirements.get(category, {"count": 1, "type": "trait"})
        
        # Format available options comprehensively
        available_options = []
        
        if isinstance(options, list):
            # Handle array format like virtues_pool.json
            for option_item in options:
                if isinstance(option_item, dict):
                    name = option_item.get("name", "Unknown")
                    definition = option_item.get("definition", "")
                    available_options.append(f"• **{name}**: {definition}")
                else:
                    available_options.append(f"• **{option_item}**")
        elif isinstance(options, dict):
            # Handle dict format  
            for option_key, option_info in options.items():
                if isinstance(option_info, dict):
                    name = option_info.get("name", option_key)
                    description = option_info.get("description", "")
                    available_options.append(f"• **{name}**: {description}")
                else:
                    available_options.append(f"• **{option_key}**: {option_info}")
        
        available_text = "\n\n".join(available_options)
        
        # Create selection instruction based on count
        if req["count"] == 1:
            selection_instruction = f"You MUST select exactly 1 {req['type']} from the available options."
            format_instruction = f"SELECTION: [chosen {req['type']} name]"
        else:
            selection_instruction = f"You MUST select exactly {req['count']} {req['type']} from the available options."
            format_instruction = f"SELECTIONS: [{req['type']} 1], [{req['type']} 2], [{req['type']} 3]"
        
        # Include knowledge base context if available
        knowledge_base_context = ""
        if persona.knowledge_base and len(persona.knowledge_base) > 0:
            traditions_list = ", ".join(persona.knowledge_base)
            knowledge_base_context = f"""
**YOUR SELECTED MYSTICAL KNOWLEDGE BASE:**
You have chosen these mystical traditions: {traditions_list}

These traditions now inform your perspective and can guide your trait selections.
"""
        
        prompt = f"""You are helping to analyze and select traits for the character {persona.name}, {persona.title}, dwelling in the {persona.aethyr} Aethyr.

Character essence: {persona.essence}

Character role: {persona.angelic_role}
{knowledge_base_context}
🎭 **{category.upper().replace('_', ' ')} SELECTION**

You are selecting {category.replace('_', ' ')} for this fictional character as part of their identity formation. This will influence how they interact with others and govern their domain in their fictional setting.

**AVAILABLE {category.upper().replace('_', ' ')} OPTIONS:**
{available_text}

**SELECTION REQUIREMENTS:**
{selection_instruction}

**SELECTION CRITERIA:**
Consider these factors when selecting for this character:

1. **Authentic Nature**: Which {req['type']}(s) genuinely reflect the character's core essence?
2. **Elemental Alignment**: Which {req['type']}(s) align with the character's {persona.element} nature?
3. **Character Purpose**: Which {req['type']}(s) support the character's role as {persona.angelic_role}?
4. **Mystical Resonance**: Which {req['type']}(s) harmonize with the character's chosen mystical traditions?
5. **Narrative Consistency**: Which {req['type']}(s) are appropriate for the character's fictional setting?
6. **Character Effectiveness**: Which {req['type']}(s) will help the character fulfill their role effectively?

**RESPONSE FORMAT:**
{format_instruction}

**CRITICAL INSTRUCTIONS:**
- Use the exact names shown in the available list
- Select exactly {req['count']} {req['type']}(s)

Analyze what would be most appropriate for this character based on their established traits and fictional context."""
        
        return prompt
    
    def _generate_trait_prompt(self, persona: GovernorPersona, category: str, options: Dict[str, Any]) -> str:
        """Generate personality trait selection prompt."""
        
        if self.blind_review:
            return self._generate_blind_trait_prompt(persona, category, options)
        
        # Get current trait value
        trait_mapping = {
            "virtues_pool": "virtues",
            "flaws_pool": "flaws",
            "approaches": "baseline_approach",
            "tones": "baseline_tone",
            "motive_alignment": "motive_alignment",
            "role_archtypes": "role_archetype", 
            "orientation_io": "orientation_io",
            "polarity_cd": "polarity_cd",
            "self_regard_options": "self_regard"
        }
        
        personality_key = trait_mapping.get(category, category)
        current_value = persona.persona.get(personality_key, "Unknown")
        
        # Debug output
        if self.verbose:
            self.logger.info(f"Trait mapping: {category} -> {personality_key}")
            self.logger.info(f"Current value: {current_value}")
            self.logger.info(f"Available personality keys: {list(persona.persona.keys())}")
        
        # If it's a list (like virtues/flaws), get the first one
        if isinstance(current_value, list):
            current_value = current_value[0] if current_value else "Unknown"
        
        # Format available options (handle both dict and list formats)
        available_options = []
        
        if isinstance(options, list):
            # Handle array format like virtues_pool.json
            for option_item in options:
                if isinstance(option_item, dict):
                    name = option_item.get("name", "Unknown")
                    definition = option_item.get("definition", "")
                    available_options.append(f"• **{name}**: {definition}")
                else:
                    available_options.append(f"• **{option_item}**")
        elif isinstance(options, dict):
            # Handle dict format  
            for option_key, option_info in options.items():
                if isinstance(option_info, dict):
                    name = option_info.get("name", option_key)
                    description = option_info.get("description", "")
                    available_options.append(f"• **{name}**: {description}")
                else:
                    available_options.append(f"• **{option_key}**: {option_info}")
        
        available_text = "\n".join(available_options)
        
        # Conditionally show current traits based on hide_current_traits setting
        if self.hide_current_traits:
            # Hide current traits - show only available options
            prompt = f"""You are {persona.name}, {persona.title}, dwelling in the {persona.aethyr} Aethyr.

Your essence: {persona.essence}

Your angelic role: {persona.angelic_role}

🎭 **PERSONALITY TRAIT SELECTION - {category.upper()}**

You are selecting your {category.replace('_', ' ')} trait as part of your eternal identity formation. This trait will influence how you interact with seekers and govern your domain.

**AVAILABLE {category.upper()} OPTIONS:**
{available_text}

**YOUR TASK:**
Select the {category.replace('_', ' ')} trait that best represents your authentic nature. Consider:

- **Authenticity**: Which trait genuinely reflects your core essence?
- **Purpose**: Which trait will help you fulfill your role as {persona.angelic_role}?
- **Element**: Which trait aligns with your {persona.element} nature?
- **Eternity**: Which trait is sustainable for your eternal existence?

**RESPONSE FORMAT:**
SELECTION: [chosen trait name]

Speak as yourself, {persona.name}. Be authentic to your eternal nature."""
        else:
            # Show current traits (original behavior)
            # Get other personality traits for context
            other_traits = []
            for key, value in persona.persona.items():
                if key != personality_key and value and value != "Unknown":
                    display_value = value[0] if isinstance(value, list) else value
                    other_traits.append(f"• {key.replace('_', ' ').title()}: {display_value}")
            
            context_text = "\n".join(other_traits) if other_traits else "• No other traits defined"
            
            prompt = f"""You are {persona.name}, {persona.title}, dwelling in the {persona.aethyr} Aethyr.

Your essence: {persona.essence}

Your angelic role: {persona.angelic_role}

🎭 **PERSONALITY TRAIT REVIEW - {category.upper()}**

You are reviewing your {category.replace('_', ' ')} trait as part of your eternal identity formation. This trait will influence how you interact with seekers and govern your domain.

**YOUR CURRENT {category.upper()} TRAIT:**
{current_value}

**YOUR OTHER PERSONALITY TRAITS:**
{context_text}

**AVAILABLE {category.upper()} OPTIONS:**
{available_text}

**YOUR TASK:**
Review your current {category.replace('_', ' ')} trait. You may:
1. **CONFIRM** your current trait if it truly represents your essence
2. **CHANGE** to a different trait if another better represents your nature

Consider:
- **Authenticity**: Does this trait genuinely reflect your core nature?
- **Harmony**: How does this trait work with your other personality aspects?
- **Purpose**: Will this trait help you fulfill your role as {persona.angelic_role}?
- **Eternity**: Is this trait sustainable for your eternal existence?

**RESPONSE FORMAT:**
DECISION: [CONFIRM current trait name] OR [CHANGE to new trait name]

Speak as yourself, {persona.name}. Be authentic to your eternal nature."""
        
        return prompt
    
    def _get_category_options(self, category: str) -> Dict[str, Any]:
        """Get trait options for a specific category."""
        
        # Handle knowledge base specially
        if category == "knowledge_base":
            return self.knowledge_base_traditions
        
        category_mapping = {
            "virtues_pool": "virtues_pool",
            "flaws_pool": "flaws_pool",
            "approaches": "approaches",
            "tones": "tones",
            "motive_alignment": "motive_alignment",
            "role_archtypes": "role_archtypes",
            "orientation_io": "orientation_io",
            "polarity_cd": "polarity_cd",
            "self_regard_options": "self_regard_options"
        }
        
        mapped_category = category_mapping.get(category, category)
        return self.trait_indexes.get(mapped_category, {})
    
    def call_ai_api(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """Make an API call to get the governor's response."""
        
        if self.dry_run:
            self.logger.info("DRY RUN: Would make API call")
            return self._generate_mock_response(prompt)
        
        try:
            if self.api_provider == "anthropic":
                if not self.anthropic_client:
                    self.logger.error("Anthropic client not initialized")
                    return None
                
                # Add timeout protection and better error handling
                self.logger.info(f"Making API call with prompt length: {len(prompt)}")
                
                response = self.anthropic_client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=0.7,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                
                # Handle Anthropic response format - content is a list of TextBlock objects
                content = ""
                if hasattr(response, 'content') and response.content:
                    for block in response.content:
                        # Safely extract text from block
                        block_text = getattr(block, 'text', None)
                        if block_text:
                            content += block_text
                        else:
                            content += str(block)
                    
                self.logger.info(f"Anthropic API call successful: {len(content)} chars")
                return content
                
            elif self.api_provider == "openai":
                if not self.openai_client:
                    self.logger.error("OpenAI client not initialized")
                    return None
                    
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }],
                    max_tokens=max_tokens,
                    temperature=0.7
                
                # Handle OpenAI response format
                content = ""
                if hasattr(response, 'choices') and response.choices:
                    choice = response.choices[0]
                    if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                        content = choice.message.content or ""
                        
                self.logger.info(f"OpenAI API call successful: {len(content)} chars")
                return content
                
            else:
                raise ValueError(f"Unsupported API provider: {self.api_provider}")
                
        except Exception as e:
            self.logger.error(f"API call failed: {e}")
            return None
    
    def _generate_mock_response(self, prompt: str) -> str:
        """Generate a mock response for dry run mode."""
        # Check prompt content to determine category
        prompt_upper = prompt.upper()
        
        # Debug: print what we're looking for
        if self.verbose:
            print(f"   🔍 Mock response for prompt containing: {prompt_upper[:100]}...")
        
        # Check for specific category markers in the prompt (without emoji dependency)
        if "MYSTICAL KNOWLEDGE BASE SELECTION" in prompt_upper or "KNOWLEDGE BASE SELECTION" in prompt_upper:
            response = """SELECTIONS: Celtic Druidic, Hermetic Philosophy, Sacred Geometry, Taoism"""
        
        elif "VIRTUES POOL SELECTION" in prompt_upper or "VIRTUES_POOL" in prompt_upper:
            response = """SELECTIONS: Courage, Wisdom, Compassion"""
        
        elif "FLAWS POOL SELECTION" in prompt_upper or "FLAWS_POOL" in prompt_upper:
            response = """SELECTIONS: Impatience, Pride, Stubbornness"""
        
        elif "APPROACHES SELECTION" in prompt_upper:
            response = """SELECTION: Teaching"""
        
        elif "TONES SELECTION" in prompt_upper:
            response = """SELECTION: Nurturing"""
        
        elif "MOTIVE ALIGNMENT SELECTION" in prompt_upper or "MOTIVE_ALIGNMENT" in prompt_upper:
            response = """SELECTION: Chaotic Good"""
        
        elif "ROLE ARCHTYPES SELECTION" in prompt_upper or "ROLE_ARCHTYPES" in prompt_upper:
            response = """SELECTION: The Sage"""
        
        elif "ORIENTATION IO SELECTION" in prompt_upper or "ORIENTATION_IO" in prompt_upper:
            response = """SELECTION: Introverted"""
        
        elif "POLARITY CD SELECTION" in prompt_upper or "POLARITY_CD" in prompt_upper:
            response = """SELECTION: Constructive"""
        
        elif "SELF REGARD OPTIONS SELECTION" in prompt_upper or "SELF_REGARD_OPTIONS" in prompt_upper:
            response = """SELECTION: Balanced"""
        
        elif "FINAL REFLECTION" in prompt_upper:
            response = """REFLECTION: This character's traits work together harmoniously."""
        
        else:
            response = """SELECTION: Default Choice"""
        
        if self.verbose:
            print(f"   📝 Generated mock response: {response}")
        
        return response
    
    def _clean_unicode_response(self, response: str) -> str:
        """Clean unicode escape sequences from AI responses while preserving structure."""
        if not response:
            return response
        
        # Only remove literal escape sequences, don't touch actual newlines or structure
        # Remove literal \n sequences (but keep actual newlines)
        response = response.replace('\\n', ' ')
        
        # Remove literal \t sequences  
        response = response.replace('\\t', ' ')
        
        # Remove literal \r sequences
        response = response.replace('\\r', ' ')
        
        # Remove literal \" sequences (but keep actual quotes)
        response = response.replace('\\"', '"')
        
        # Clean up multiple spaces but preserve single spaces and newlines
        response = re.sub(r' +', ' ', response)
        
        return response.strip()

    def parse_ai_response(self, response: str, category: str) -> Optional[ReviewChoice]:
        """Parse the AI response to extract the governor's choice."""
        
        if not response:
            return None
        
        # Clean unicode escape sequences
        response = self._clean_unicode_response(response)
        
        try:
            if category == "knowledge_base":
                return self._parse_knowledge_base_response(response)
            else:
                return self._parse_trait_response(response, category)
                
        except Exception as e:
            self.logger.error(f"Error parsing AI response: {e}")
            # Return basic choice with error info
            return ReviewChoice(
                category=category,
                selected_value="parsing_failed",
                reasoning=f"Failed to parse response: {str(e)[:200]}",
                confidence_level="low"
    
    def _parse_knowledge_base_response(self, response: str) -> Optional[ReviewChoice]:
        """Parse knowledge base selection response with strict validation for 4 selections."""
        
        # Multiple patterns to try for selections - improved to handle cleaned responses
        selection_patterns = [
            r'SELECTIONS?:\s*(.*?)(?:\s+REASONING)',  # Stop at REASONING
            r'CHOICES?:\s*(.*?)(?:\s+REASONING)',
            r'I\s+(?:choose|select|pick):\s*(.*?)(?:\s+REASONING)',
            r'My\s+selections?:\s*(.*?)(?:\s+REASONING)',
            r'I\s+would\s+select:\s*(.*?)(?:\s+REASONING)',
            r'(?:I\s+)?select\s+the\s+following:\s*(.*?)(?:\s+REASONING)',
            # Fallback patterns without REASONING requirement (less preferred)
            r'SELECTIONS?:\s*([^\n]+)',
            r'CHOICES?:\s*([^\n]+)',

        
        # Try each pattern
        selections_text = None
        for pattern in selection_patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                selections_text = match.group(1).strip()
                break
        
        # If no structured selection found, require proper format
        if not selections_text:
            # Don't try to extract tradition names directly - require proper format
            # This prevents picking up too many traditions from the reasoning text
            pass
        
        if not selections_text:
            # Return with explanation if no selection found
            return ReviewChoice(
                category="knowledge_base",
                selected_value="parsing_failed",
                reasoning=f"Unable to parse selection from response: {response[:200]}...",
                confidence_level="low"
        
        # Parse selections - handle both comma-separated and bullet point formats
        if '\n' in selections_text and '-' in selections_text:
            # Handle bullet point format
            lines = selections_text.split('\n')
            selections = []
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    # Remove bullet point and clean
                    selection = line.lstrip('-•').strip()
                    if selection:
                        selections.append(selection)
        else:
            # Handle comma-separated format
            selections = [s.strip() for s in selections_text.split(',')]
        
        # CRITICAL: Validate exactly 4 selections
        if len(selections) != 4:
            return ReviewChoice(
                category="knowledge_base",
                selected_value="validation_failed",
                reasoning=f"ERROR: Expected exactly 4 traditions, but got {len(selections)}: {selections}. Please select exactly 4 traditions.",
                confidence_level="low"
        
        # No reasoning extraction - clean output only
        reasoning = "Clean selection - no reasoning provided"
        
        # Exact tradition name mapping from comprehensive index
        tradition_mapping = {
            "Celtic Druidic Traditions": "celtic_druidic",
            "Chaos Magic": "chaos_magic",
            "Classical Greek Philosophy": "classical_philosophy",
            "Ancient Egyptian Magic": "egyptian_magic",
            "Gnostic Traditions": "gnostic_traditions",
            "Hermetic Order of the Golden Dawn": "golden_dawn",
            "I-Ching (Book of Changes)": "i_ching",
            "Kuji-kiri (Nine Symbolic Cuts)": "kuji_kiri",
            "Norse/Germanic Traditions": "norse_traditions",
            "Sacred Geometry": "sacred_geometry",
            "Sufi Mysticism": "sufi_mysticism",
            "Taoism (Daoism)": "taoism",
            "Tarot Divination System": "tarot_knowledge",
            "Thelema": "thelema",
            "Hermetic Philosophy": "hermetic_philosophy",
            "Kabbalistic Mysticism": "kabbalistic_mysticism",
        }
        
        converted_selections = []
        invalid_selections = []
        
        for selection in selections:
            selection_clean = selection.strip()
            if selection_clean in tradition_mapping:
                converted_selections.append(tradition_mapping[selection_clean])
            else:
                # Try fuzzy matching
                mapped = selection_clean.lower().replace(" ", "_")
                if mapped in tradition_mapping.values():
                    converted_selections.append(mapped)
                else:
                    invalid_selections.append(selection_clean)
        
        # Validate all selections are valid
        if invalid_selections:
            return ReviewChoice(
                category="knowledge_base",
                selected_value="invalid_selections",
                reasoning=f"ERROR: Invalid tradition selections: {invalid_selections}. Please select from the available traditions list.",
                confidence_level="low"
        
        # Success - exactly 4 valid selections
        return ReviewChoice(
            category="knowledge_base",
            selected_value=",".join(converted_selections),
            reasoning=reasoning,
            confidence_level="high"
    
    def _parse_trait_response(self, response: str, category: str) -> Optional[ReviewChoice]:
        """Parse personality trait selection response."""
        
        # Handle blind review format
        if self.blind_review:
            return self._parse_blind_trait_response(response, category)
        
        # Try to extract decision (original format)
        decision_match = re.search(r'DECISION:\s*([^\n]+)', response, re.IGNORECASE)
        
        # Try to extract selection (new format when hiding current traits)
        selection_match = re.search(r'SELECTION:\s*([^\n]+)', response, re.IGNORECASE)
        
        if decision_match:
            # Original format with DECISION
            decision_text = decision_match.group(1).strip()
            
            # Parse decision (CONFIRM X or CHANGE to Y)
            if decision_text.upper().startswith("CONFIRM"):
                # Extract confirmed trait
                confirmed_match = re.search(r'CONFIRM\s+(.+)', decision_text, re.IGNORECASE)
                selected_value = confirmed_match.group(1).strip() if confirmed_match else ""
            elif decision_text.upper().startswith("CHANGE"):
                # Extract new trait
                change_match = re.search(r'CHANGE\s+(?:to\s+)?(.+)', decision_text, re.IGNORECASE)
                selected_value = change_match.group(1).strip() if change_match else ""
            else:
                selected_value = decision_text.strip()
                
        elif selection_match:
            # New format with SELECTION
            selected_value = selection_match.group(1).strip()
        else:
            # No structured format found
            return None
        
        # No reasoning extraction - clean output only
        reasoning = "Clean selection - no reasoning provided"
        
        return ReviewChoice(
            category=category,
            selected_value=selected_value,
            reasoning=reasoning,
            confidence_level="high"
    
    def _parse_blind_trait_response(self, response: str, category: str) -> Optional[ReviewChoice]:
        """Parse blind trait selection response with multiple selection support and validation."""
        
        # Define selection requirements with validation
        selection_requirements = {
            "virtues_pool": {"count": 3, "type": "virtues"},
            "flaws_pool": {"count": 3, "type": "flaws"},
            "approaches": {"count": 1, "type": "approach"},
            "tones": {"count": 1, "type": "tone"},
            "motive_alignment": {"count": 1, "type": "alignment"},
            "role_archtypes": {"count": 1, "type": "archetype"},
            "orientation_io": {"count": 1, "type": "orientation"},
            "polarity_cd": {"count": 1, "type": "polarity"},
            "self_regard_options": {"count": 1, "type": "self-regard"}
        }
        
        req = selection_requirements.get(category, {"count": 1, "type": "trait"})
        is_multi_selection = req["count"] > 1
        
        # Try to extract selections
        if is_multi_selection:
            # Look for SELECTIONS: format - improved to handle cleaned responses
            selections_patterns = [
                r'SELECTIONS:\s*(.*?)(?:\s+REASONING)',  # Stop at REASONING if present
                r'SELECTIONS:\s*([^\n]+)',  # Fallback
                r'I\s+select:\s*(.*?)(?:\s+REASONING)',
                r'I\s+select:\s*([^\n]+)',
                r'My\s+choices?:\s*(.*?)(?:\s+REASONING)',
                r'My\s+choices?:\s*([^\n]+)',
                r'I\s+choose:\s*(.*?)(?:\s+REASONING)',
                r'I\s+choose:\s*([^\n]+)',

            
            selections_text = None
            for pattern in selections_patterns:
                selections_match = re.search(pattern, response, re.IGNORECASE)
                if selections_match:
                    selections_text = selections_match.group(1).strip()
                    break
            
            if selections_text:
                # Parse comma-separated selections
                selections = [s.strip() for s in selections_text.split(',')]
            else:
                # Look for individual selections in the response
                selections = []
                lines = response.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('-') or line.startswith('•'):
                        selection = line.lstrip('-•').strip()
                        if selection and not selection.startswith('**'):
                            selections.append(selection)
                
                # If no bullet points found, try to find selections in text
                if not selections:
                    # Look for pattern like "I select: X, Y, Z"
                    select_patterns = [
                        r'I\s+select:\s*([^\n]+)',
                        r'My\s+choices?:\s*([^\n]+)',
                        r'I\s+choose:\s*([^\n]+)',

                    for pattern in select_patterns:
                        match = re.search(pattern, response, re.IGNORECASE)
                        if match:
                            selections_text = match.group(1).strip()
                            selections = [s.strip() for s in selections_text.split(',')]
                            break
            
            # CRITICAL: Validate exact count for multi-selections
            if len(selections) != req["count"]:
                return ReviewChoice(
                    category=category,
                    selected_value="validation_failed",
                    reasoning=f"ERROR: Expected exactly {req['count']} {req['type']}(s), but got {len(selections)}: {selections}. Please select exactly {req['count']} {req['type']}(s).",
                    confidence_level="low"
            
            selected_value = ",".join(selections)
            
        else:
            # Single selection - improved patterns to handle clean responses
            single_patterns = [
                r'SELECTION:\s*(.*?)(?:\s+REASONING)',  # Stop at REASONING if present
                r'SELECTION:\s*([^\n]+)',  # Fallback
                r'I\s+select:\s*(.*?)(?:\s+REASONING)',
                r'I\s+select:\s*([^\n]+)',
                r'My\s+choice:\s*(.*?)(?:\s+REASONING)',
                r'My\s+choice:\s*([^\n]+)',
                r'I\s+choose:\s*(.*?)(?:\s+REASONING)',
                r'I\s+choose:\s*([^\n]+)',

            
            selected_value = None
            for pattern in single_patterns:
                match = re.search(pattern, response, re.IGNORECASE)
                if match:
                    selected_value = match.group(1).strip()
                    break
            
            if not selected_value:
                return ReviewChoice(
                    category=category,
                    selected_value="parsing_failed",
                    reasoning=f"Unable to parse selection from response: {response[:200]}...",
                    confidence_level="low"
        
        # No reasoning extraction - clean output only
        reasoning = "Clean selection - no reasoning provided"
        
        return ReviewChoice(
            category=category,
            selected_value=selected_value,
            reasoning=reasoning,
            confidence_level="high"
    
    def execute_governor_review(self, governor_name: str) -> Optional[GovernorReviewSession]:
        """Execute a complete AI-powered review session for a governor."""
        
        start_time = time.time()
        session_id = f"{governor_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\n🤖 Starting AI-Powered Review for {governor_name}")
        print("=" * 60)
        
        try:
            # 1. Create governor persona
            print("📋 Creating governor persona...")
            persona = self.create_governor_persona(governor_name)
            if not persona:
                print(f"❌ Failed to create persona for {governor_name}")
                return None
            
            print(f"✅ Persona created: {persona.name} - {persona.title}")
            
            # 2. Initialize session
            session = GovernorReviewSession(
                governor_name=governor_name,
                session_id=session_id,
                start_time=datetime.now().isoformat(),
                persona=persona,
                review_choices=[],
                final_profile_updates={},
                ai_conversation_log=[],
                completion_status="in_progress",
                total_api_calls=0,
                processing_time_seconds=0
            
            # 3. FIRST: Process Knowledge Base Selection
            print(f"\n🧙‍♂️ [PRIORITY] Processing Knowledge Base Selection...")
            knowledge_base_choice = self._process_knowledge_base_selection(session)
            
            if knowledge_base_choice and knowledge_base_choice.selected_value not in ["parsing_failed", "validation_failed", "invalid_selections"]:
                # SUCCESS: Load selected knowledge base into persona for subsequent trait selections
                selected_traditions = knowledge_base_choice.selected_value.split(",")
                # Add mandatory Enochian Magic
                persona.knowledge_base = ["enochian_magic"] + selected_traditions
                
                print(f"✅ Knowledge Base loaded into persona: {persona.knowledge_base}")
                print(f"   🔮 Governor {persona.name} now has access to their selected mystical traditions")
                
                # Update session persona with loaded knowledge base
                session.persona = persona
                
            else:
                print(f"⚠️  Knowledge Base selection failed - continuing with empty knowledge base")
            
            # 4. Process remaining personality traits with knowledge base context
            personality_categories = [
                "virtues_pool",
                "flaws_pool", 
                "approaches",
                "tones",
                "motive_alignment",
                "role_archtypes",
                "orientation_io",
                "polarity_cd",
                "self_regard_options"

            
            print(f"\n🎭 Processing {len(personality_categories)} personality trait categories...")
            print(f"   🔮 Governor now has their mystical knowledge base for context")
            
            for i, category in enumerate(personality_categories, 1):
                print(f"\n📝 [{i}/{len(personality_categories)}] Reviewing: {category.replace('_', ' ').title()}")
                
                # Generate prompt (persona now includes selected knowledge base)
                prompt = self.generate_review_prompt(persona, category)
                
                if self.verbose:
                    print(f"   💭 Prompt length: {len(prompt)} characters")
                
                # Make API call
                print(f"   🤖 Calling AI API...")
                try:
                    response = self.call_ai_api(prompt)
                    session.total_api_calls += 1
                    
                    if not response:
                        print(f"   ❌ API call failed for {category}")
                        continue
                    
                    print(f"   ✅ API response received ({len(response)} chars)")
                    
                except Exception as e:
                    print(f"   ❌ API call error for {category}: {str(e)[:100]}...")
                    session.total_api_calls += 1
                    continue
                
                # Log conversation
                session.ai_conversation_log.append({
                    "category": category,
                    "prompt": prompt,
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Parse response
                choice = self.parse_ai_response(response, category)
                if choice:
                    session.review_choices.append(choice)
                    print(f"   ✅ Choice recorded: {choice.selected_value}")
                    
                    if self.verbose:
                        print(f"   💡 Reasoning: {choice.reasoning[:100]}...")
                else:
                    print(f"   ⚠️  Failed to parse response for {category}")
                
                # Rate limiting pause
                time.sleep(1)
            
            # 5. FINAL: Governor Reflection Section
            print(f"\n🤔 Requesting final reflection from {persona.name}...")
            reflection_choice = self._process_governor_reflection(session)
            if reflection_choice:
                session.review_choices.append(reflection_choice)
                print(f"   ✅ Reflection recorded")
            
            # 6. Generate final profile updates
            print(f"\n💾 Generating profile updates...")
            session.final_profile_updates = self._generate_profile_updates(session.review_choices)
            
            # 7. Complete session
            session.completion_status = "completed"
            session.processing_time_seconds = time.time() - start_time
            
            # Print audit summary at the top
            print(f"\n📊 AUDIT SUMMARY")
            print("=" * 50)
            print(f"   ⏱️  Processing time: {session.processing_time_seconds:.1f} seconds")
            print(f"   🔄 API calls made: {session.total_api_calls}")
            print(f"   ✅ Choices recorded: {len(session.review_choices)}")
            print(f"   🔮 Knowledge Base: {len(persona.knowledge_base)} traditions")
            print(f"   🎭 Governor: {persona.name} - {persona.title}")
            print(f"   🌊 Element: {persona.element} | Aethyr: {persona.aethyr}")
            print("=" * 50)
            
            print(f"\n🎉 Review completed successfully!")
            
            return session
            
        except Exception as e:
            print(f"❌ Error during review: {e}")
            self.logger.error(f"Error executing review for {governor_name}: {e}")
            return None
    
    def _generate_profile_updates(self, choices: List[ReviewChoice]) -> Dict[str, Any]:
        """Generate profile updates from review choices."""
        
        updates = {
            "knowledge_base_selections": [],
            "personality_traits": {},
            "review_metadata": {
                "review_date": datetime.now().isoformat(),
                "review_method": "ai_powered_self_review",
                "total_categories_reviewed": len(choices),
                "ai_generated": True
            }
        }
        
        for choice in choices:
            if choice.category == "knowledge_base":
                # Add Enochian Magic as mandatory plus selected traditions
                selections = ["enochian_magic"] + choice.selected_value.split(",")
                updates["knowledge_base_selections"] = [s.strip() for s in selections]
            
            else:
                # Map category to personality field
                field_mapping = {
                    "virtues_pool": "virtues",
                    "flaws_pool": "flaws",
                    "approaches": "baseline_approach",
                    "tones": "baseline_tone",
                    "motive_alignment": "motive_alignment",
                    "role_archtypes": "role_archetype",
                    "orientation_io": "orientation_io",
                    "polarity_cd": "polarity_cd",
                    "self_regard_options": "self_regard"
                }
                
                field_name = field_mapping.get(choice.category)
                if field_name:
                    if field_name in ["virtues", "flaws"]:
                        updates["personality_traits"][field_name] = [choice.selected_value]
                    else:
                        updates["personality_traits"][field_name] = choice.selected_value
        
        return updates
    
    def save_review_session(self, session: GovernorReviewSession) -> bool:
        """Save the complete review session to file."""
        
        try:
            session_file = self.review_sessions_dir / f"{session.session_id}.json"

            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(session), f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Review session saved: {session_file}")
            
            # Also save clean profile if review was successful
            if session.completion_status == "completed":
                self._save_clean_profile(session)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving review session: {e}")
            return False
    
    def _save_clean_profile(self, session: GovernorReviewSession) -> bool:
        """Save clean profile to /clean_governor_profiles with full dossier structure."""
        
        try:
            # Create clean_governor_profiles directory if it doesn't exist
            clean_profiles_dir = Path("clean_governor_profiles")
            clean_profiles_dir.mkdir(exist_ok=True)
            
            # Load canonical profile for base traits
            canonical_profile = self.load_governor_profile(session.governor_name)
            if not canonical_profile:
                self.logger.error(f"Cannot load canonical profile for {session.governor_name}")
                return False
            
            # Build clean profile structure - SIMPLE FORMAT
            clean_profile = {
                "governor_name": session.persona.name,
                "title": session.persona.title,
                "element": session.persona.element,
                "aethyr": session.persona.aethyr,
                "essence": session.persona.essence,
                "angelic_role": session.persona.angelic_role,
                "archetypal_correspondences": canonical_profile.get("archetypal_correspondences", {}),
                "knowledge_base": session.persona.knowledge_base,
                "persona": {}
            }
            
            # Populate persona with AI review choices - CLEAN VALUES ONLY
            for choice in session.review_choices:
                if choice.category == "knowledge_base":
                    # Already handled above
                    continue
                elif choice.category == "governor_reflection":
                    # Skip reflection - not part of final profile
                    continue
                elif choice.category in ["virtues_pool", "flaws_pool"]:
                    # Handle multi-selection traits - clean values only
                    trait_name = choice.category.replace("_pool", "")
                    raw_values = choice.selected_value.split(",")
                    clean_values = [v.strip() for v in raw_values]
                    clean_profile["persona"][trait_name] = clean_values
                else:
                    # Handle single-selection traits - clean values only
                    field_mapping = {
                        "approaches": "baseline_approach",
                        "tones": "baseline_tone",
                        "motive_alignment": "motive_alignment",
                        "role_archtypes": "role_archetype",
                        "orientation_io": "orientation",
                        "polarity_cd": "polarity",
                        "self_regard_options": "self_regard"
                    }
                    
                    field_name = field_mapping.get(choice.category, choice.category)
                    # Clean the value - remove any reasoning or extra text
                    clean_value = choice.selected_value.strip()
                    clean_profile["persona"][field_name] = clean_value
            
            # Save clean profile
            clean_profile_file = clean_profiles_dir / f"{session.governor_name}.json"

            with open(clean_profile_file, 'w', encoding='utf-8') as f:
                json.dump(clean_profile, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Clean profile saved: {clean_profile_file}")
            print(f"✅ Clean profile saved: {clean_profile_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving clean profile: {e}")
            print(f"❌ Error saving clean profile: {e}")
            return False
    
    def _process_knowledge_base_selection(self, session: GovernorReviewSession) -> Optional[ReviewChoice]:
        """Process knowledge base selection as priority first step."""
        
        try:
            # Generate knowledge base prompt
            prompt = self.generate_review_prompt(session.persona, "knowledge_base")
            
            if self.verbose:
                print(f"   💭 Knowledge Base prompt length: {len(prompt)} characters")
            
            # Make API call
            print(f"   🤖 Calling AI API for knowledge base selection...")
            response = self.call_ai_api(prompt)
            session.total_api_calls += 1
            
            if not response:
                print(f"   ❌ API call failed for knowledge base")
                return None
            
            print(f"   ✅ API response received ({len(response)} chars)")
            
            # Log conversation
            session.ai_conversation_log.append({
                "category": "knowledge_base",
                "prompt": prompt,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Parse response
            choice = self.parse_ai_response(response, "knowledge_base")
            if choice:
                session.review_choices.append(choice)
                print(f"   ✅ Knowledge Base choice recorded: {choice.selected_value}")
                
                if self.verbose:
                    print(f"   💡 Reasoning: {choice.reasoning[:100]}...")
                
                return choice
            else:
                print(f"   ⚠️  Failed to parse knowledge base response")
                return None
                
        except Exception as e:
            print(f"   ❌ Error processing knowledge base: {str(e)[:100]}...")
            session.total_api_calls += 1
            return None
    
    def _process_governor_reflection(self, session: GovernorReviewSession) -> Optional[ReviewChoice]:
        """Process final governor reflection after all trait selections."""
        
        try:
            # Generate reflection prompt
            prompt = self._generate_reflection_prompt(session.persona, session.review_choices)
            
            if self.verbose:
                print(f"   💭 Reflection prompt length: {len(prompt)} characters")
            
            # Make API call
            print(f"   🤖 Calling AI API for final reflection...")
            response = self.call_ai_api(prompt, max_tokens=1500)  # More tokens for reflection
            session.total_api_calls += 1
            
            if not response:
                print(f"   ❌ API call failed for reflection")
                return None
            
            print(f"   ✅ Reflection response received ({len(response)} chars)")
            
            # Log conversation
            session.ai_conversation_log.append({
                "category": "governor_reflection",
                "prompt": prompt,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Parse reflection response
            choice = self._parse_reflection_response(response)
            if choice:
                session.review_choices.append(choice)
                
                if self.verbose:
                    print(f"   💡 Reflection: {choice.reasoning[:100]}...")
                
                return choice
            else:
                print(f"   ⚠️  Failed to parse reflection response")
                return None
                
        except Exception as e:
            print(f"   ❌ Error processing reflection: {str(e)[:100]}...")
            session.total_api_calls += 1
            return None
    
    def _generate_reflection_prompt(self, persona: GovernorPersona, choices: List[ReviewChoice]) -> str:
        """Generate prompt for governor's final reflection on their trait selections."""
        
        # Summarize selected traits
        selected_traits = {}
        for choice in choices:
            if choice.category != "governor_reflection":
                selected_traits[choice.category] = choice.selected_value
        
        # Format selected traits for display
        traits_summary = []
        for category, value in selected_traits.items():
            display_category = category.replace('_', ' ').title()
            traits_summary.append(f"• **{display_category}**: {value}")
        
        traits_text = "\n".join(traits_summary)
        
        prompt = f"""You are helping to provide a final reflection for the character {persona.name}, {persona.title}, dwelling in the {persona.aethyr} Aethyr.

Character essence: {persona.essence}

Character role: {persona.angelic_role}

Character's selected mystical knowledge base: {', '.join(persona.knowledge_base)}

🤔 **FINAL REFLECTION ON CHARACTER IDENTITY**

This fictional character has just completed selecting the traits that will define their identity as a Governor. Here are their selections:

{traits_text}

**REFLECTION INVITATION:**

Provide a thoughtful reflection on this character's complete identity as if speaking from their perspective. You may address:

1. **Overall Coherence**: How do these traits work together as a unified whole?
2. **Character Consistency**: How well do these selections fit the character's established nature?
3. **Synergies**: What interesting connections exist between the character's traits?
4. **Role Fulfillment**: How will these traits help the character fulfill their fictional role?
5. **Character Development**: Any insights about the character's growth or purpose?
6. **Narrative Observations**: Any observations about the character creation process?

**RESPONSE FORMAT:**
REFLECTION: [A thoughtful reflection on the character's complete identity and any insights about their fictional role]

**INSTRUCTIONS:**
- Write as if the character is reflecting on their own identity
- Focus on character consistency and narrative coherence
- Address how the traits work together for this fictional being
- Keep the tone appropriate for the character's established nature

This reflection will be part of the character's record and may help understand their fictional identity."""
        
        return prompt
    
    def _parse_reflection_response(self, response: str) -> Optional[ReviewChoice]:
        """Parse governor reflection response."""
        
        # Extract reflection
        reflection_match = re.search(r'REFLECTION:\s*(.*)', response, re.IGNORECASE | re.DOTALL)
        if reflection_match:
            reflection_text = reflection_match.group(1).strip()
        else:
            # Use entire response if no structured format
            reflection_text = response.strip()
        
        return ReviewChoice(
            category="governor_reflection",
            selected_value="reflection_completed",
            reasoning=reflection_text,
            confidence_level="high"

# Main execution
def main():
    """Main execution function."""
    
    parser = argparse.ArgumentParser(description="AI-Powered Governor Review System")
    parser.add_argument("--governor", required=True, help="Governor name to review")
    parser.add_argument("--api-provider", default="anthropic", choices=["anthropic", "openai"], 
                       help="AI API provider")
    parser.add_argument("--model", default="claude-3-5-sonnet-20241022", 
                       help="AI model to use")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--dry-run", action="store_true", help="Run without making API calls")
    parser.add_argument("--hide-current-traits", action="store_true", help="Hide current traits from governor during review")
    parser.add_argument("--blind-review", action="store_true", help="Enable blind review mode")
    parser.add_argument("--use-clean-profiles", action="store_true", help="Use clean profiles without interview responses")
    
    args = parser.parse_args()
    
    print("🏛️  AI-Powered Governor Review System")
    print("=" * 50)
    
    if args.dry_run:
        print("⚠️  DRY RUN MODE - Mock responses will be used")
    
    try:
        # Initialize system
        system = AIGovernorReviewSystem(
            api_provider=args.api_provider,
            model=args.model,
            verbose=args.verbose,
            dry_run=args.dry_run,
            hide_current_traits=args.hide_current_traits,
            blind_review=args.blind_review,
            use_clean_profiles=args.use_clean_profiles
        
        # Execute review
        session = system.execute_governor_review(args.governor)
        
        if session:
            # Save session
            system.save_review_session(session)
            print(f"\n💾 Session saved: {session.session_id}")
        else:
            print(f"\n❌ Review failed for {args.governor}")
            return False
            
    except Exception as e:
        print(f"❌ System error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 