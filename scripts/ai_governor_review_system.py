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

import sys
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

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ai_governor_review.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

@dataclass
class GovernorPersona:
    """Represents a governor's complete identity for AI conversation."""
    name: str
    title: str
    element: str
    aethyr: str
    essence: str
    angelic_role: str
    current_personality: Dict[str, Any]
    current_knowledge_base: List[str]
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
                 dry_run: bool = False):
        """Initialize the AI governor review system."""
        
        self.api_provider = api_provider
        self.model = model
        self.verbose = verbose
        self.dry_run = dry_run
        self.logger = logging.getLogger("AIGovernorReviewSystem")
        
        # Initialize paths
        self.project_root = Path(__file__).parent.parent
        self.governor_profiles_dir = self.project_root / "governor_output"
        self.canon_profiles_file = self.project_root / "canon" / "canon_governor_profiles.json"
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
            ]
            
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
            tradition_index_file = self.knowledge_base_dir / "archives" / "tradition_selection_index.json"
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
        """Load a governor's complete profile from individual file or canon."""
        try:
            # First try individual governor file
            individual_file = self.governor_profiles_dir / f"{governor_name}.json"
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
                    current_personality=trait_choices,  # This contains all current traits
                    current_knowledge_base=profile.get("knowledge_base_selections", []),
                    interview_responses=profile.get("interview_responses", {}),
                    archetypal_correspondences=canonical_data.get("archetypal", {})
                )
            else:
                # Individual profile structure (fallback)
                persona = GovernorPersona(
                    name=profile.get("governor_name", governor_name),
                    title=profile.get("profile", {}).get("translation", ""),
                    element=profile.get("profile", {}).get("element", ""),
                    aethyr=profile.get("profile", {}).get("aethyr", ""),
                    essence=profile.get("profile", {}).get("essence", ""),
                    angelic_role=profile.get("profile", {}).get("angelic_role", ""),
                    current_personality=profile.get("profile", {}).get("personality", {}),
                    current_knowledge_base=profile.get("knowledge_base_selections", []),
                    interview_responses=profile.get("blocks", {}),
                    archetypal_correspondences=profile.get("profile", {}).get("archetypal", {})
                )
            
            self.logger.info(f"Created persona for {governor_name} with {len(persona.current_personality)} personality traits")
            if self.verbose:
                self.logger.info(f"Personality traits: {list(persona.current_personality.keys())}")
                self.logger.info(f"Knowledge base selections: {persona.current_knowledge_base}")
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
        
        # Format current selections (handle None/empty cases)
        current_knowledge_base = persona.current_knowledge_base or []
        current_selections = []
        
        for tradition in current_knowledge_base:
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

As an eternal governor, you need to select 4 additional mystical traditions to complement your mandatory Enochian Magic foundation. These traditions will shape how you understand and interact with the mystical cosmos.

**YOUR CURRENT SELECTIONS:**
{current_text}

**AVAILABLE TRADITIONS:**
{available_text}

**YOUR TASK:**
Select exactly 4 traditions that resonate with your essence and will enhance your governance capabilities. Consider:

1. **Resonance**: Which traditions align with your element ({persona.element}) and essence?
2. **Complement**: How do these traditions work together with Enochian Magic?
3. **Governance**: Which traditions will help you guide seekers effectively?
4. **Growth**: Which traditions offer paths for your eternal development?

**RESPONSE FORMAT:**
Please respond with exactly 4 tradition names (using the exact names from the available list), followed by your reasoning.

Example:
SELECTIONS: Celtic Druidic, Hermetic Philosophy, Sacred Geometry, Taoism
REASONING: [Your detailed explanation for why these traditions serve your eternal purpose]

Speak as yourself, {persona.name}. Be authentic to your nature and role."""
        
        return prompt
    
    def _generate_trait_prompt(self, persona: GovernorPersona, category: str, options: Dict[str, Any]) -> str:
        """Generate personality trait selection prompt."""
        
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
        current_value = persona.current_personality.get(personality_key, "Unknown")
        
        # Debug output
        if self.verbose:
            self.logger.info(f"Trait mapping: {category} -> {personality_key}")
            self.logger.info(f"Current value: {current_value}")
            self.logger.info(f"Available personality keys: {list(persona.current_personality.keys())}")
        
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
        
        # Get other personality traits for context
        other_traits = []
        for key, value in persona.current_personality.items():
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
REASONING: [Your detailed explanation for your decision]

Speak as yourself, {persona.name}. Be authentic to your eternal nature."""
        
        return prompt
    
    def _get_category_options(self, category: str) -> Dict[str, Any]:
        """Get available options for a specific category."""
        if category == "knowledge_base":
            return self.knowledge_base_traditions
        else:
            return self.trait_indexes.get(category, {})
    
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
                )
                
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
                )
                
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
        if "KNOWLEDGE BASE" in prompt:
            return """SELECTIONS: Celtic Druidic, Hermetic Philosophy, Sacred Geometry, Taoism
REASONING: These traditions resonate deeply with my elemental nature and provide complementary wisdom paths. Celtic Druidic connects me to the natural world, Hermetic Philosophy offers systematic understanding of cosmic principles, Sacred Geometry provides structural insight into reality's patterns, and Taoism teaches the flow of balanced existence. Together with Enochian Magic, they create a comprehensive foundation for eternal governance."""
        
        elif "VIRTUES" in prompt:
            return """DECISION: CONFIRM Courage
REASONING: After deep reflection, Courage remains the cornerstone of my being. This virtue has guided me through countless challenges and aligns perfectly with my role as a teacher and guide. Courage allows me to face the unknown with confidence and to lead others through their own transformative journeys. It complements my other virtues and provides the strength needed for eternal service."""
        
        elif "FLAWS" in prompt:
            return """DECISION: CONFIRM Impatience
REASONING: I acknowledge that Impatience is indeed a shadow aspect of my nature that I must work with. While it can lead to hasty decisions, it also drives my urgency to help others grow and transform. This flaw keeps me humble and reminds me that even as an eternal governor, I continue to evolve. It balances my other traits and provides important lessons in patience and timing."""
        
        elif "APPROACH" in prompt:
            return """DECISION: CONFIRM Teaching
REASONING: Teaching remains my truest expression of service. This approach allows me to share wisdom while respecting each seeker's unique journey. It aligns with my role as a guide and provides structure for meaningful interactions. Teaching combines patience, wisdom, and care - qualities that resonate deeply with my essence as an eternal governor."""
        
        elif "TONE" in prompt:
            return """DECISION: CONFIRM Nurturing
REASONING: The Nurturing tone authentically reflects my deep care for those who seek guidance. This tone creates a safe space for learning and growth, allowing seekers to explore their potential without fear. It complements my teaching approach and helps foster the trust necessary for meaningful spiritual development. This tone will serve me well throughout eternity."""
        
        else:
            return """DECISION: CONFIRM Current Trait
REASONING: After careful consideration, I find that my current trait authentically represents my eternal essence. This trait has been carefully chosen to reflect my core nature and serves my role as an eternal governor. It creates harmony with my other personality aspects and provides a stable foundation for my interactions with seekers across all realms."""
    
    def parse_ai_response(self, response: str, category: str) -> Optional[ReviewChoice]:
        """Parse the AI response to extract the governor's choice."""
        
        if not response:
            return None
        
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
            )
    
    def _parse_knowledge_base_response(self, response: str) -> Optional[ReviewChoice]:
        """Parse knowledge base selection response with flexible pattern matching."""
        
        # Multiple patterns to try for selections
        selection_patterns = [
            r'SELECTIONS?:\s*([^\n]+)',
            r'CHOICES?:\s*([^\n]+)',
            r'I\s+(?:choose|select|pick):\s*([^\n]+)',
            r'My\s+selections?:\s*([^\n]+)',
            r'I\s+would\s+select:\s*([^\n]+)',
            r'(?:I\s+)?select\s+the\s+following:\s*([^\n]+)',
        ]
        
        # Try each pattern
        selections_text = None
        for pattern in selection_patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                selections_text = match.group(1).strip()
                break
        
        # If no structured selection found, try to extract tradition names directly
        if not selections_text:
            # Look for tradition names in the response
            tradition_keywords = [
                "Celtic Druidic", "Hermetic Philosophy", "Sacred Geometry", "Taoism",
                "Chaos Magic", "Golden Dawn", "Kabbalah", "Sufi Mysticism", 
                "Egyptian Magic", "Norse Traditions", "Gnostic Traditions",
                "Classical Philosophy", "Thelema", "I Ching", "Tarot Knowledge", "Kuji Kiri"
            ]
            
            found_traditions = []
            for tradition in tradition_keywords:
                if re.search(r'\b' + re.escape(tradition) + r'\b', response, re.IGNORECASE):
                    found_traditions.append(tradition)
            
            if found_traditions:
                selections_text = ", ".join(found_traditions)
        
        if not selections_text:
            # Return with explanation if no selection found
            return ReviewChoice(
                category="knowledge_base",
                selected_value="parsing_failed",
                reasoning=f"Unable to parse selection from response: {response[:200]}...",
                confidence_level="low"
            )
        
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
        
        # Extract reasoning with flexible patterns
        reasoning_patterns = [
            r'REASONING:\s*(.*)',
            r'EXPLANATION:\s*(.*)',
            r'(?:My\s+)?(?:reasoning|rationale):\s*(.*)',
            r'(?:I\s+choose\s+these\s+because|These\s+resonate\s+because)\s*(.*)',
            r'(?:Because|As)\s+(.*)',
        ]
        
        reasoning = "No reasoning provided"
        for pattern in reasoning_patterns:
            match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
            if match:
                reasoning = match.group(1).strip()[:500]  # Limit length
                break
        
        # If still no reasoning, use last part of response
        if reasoning == "No reasoning provided":
            sentences = response.split('.')
            if len(sentences) > 1:
                reasoning = sentences[-2].strip() if len(sentences) > 2 else sentences[-1].strip()
        
        # Convert to underscore format
        selection_mapping = {
            "Celtic Druidic": "celtic_druidic",
            "Hermetic Philosophy": "hermetic_philosophy", 
            "Sacred Geometry": "sacred_geometry",
            "Taoism": "taoism",
            "Chaos Magic": "chaos_magic",
            "Golden Dawn": "golden_dawn",
            "Kabbalah": "kabbalah",
            "Sufi Mysticism": "sufi_mysticism",
            "Egyptian Magic": "egyptian_magic",
            "Norse Traditions": "norse_traditions",
            "Gnostic Traditions": "gnostic_traditions",
            "Classical Philosophy": "classical_philosophy",
            "Thelema": "thelema",
            "I Ching": "i_ching",
            "Tarot Knowledge": "tarot_knowledge",
            "Kuji Kiri": "kuji_kiri"
        }
        
        converted_selections = []
        for selection in selections:
            selection_clean = selection.strip()
            mapped = selection_mapping.get(selection_clean, selection_clean.lower().replace(" ", "_"))
            converted_selections.append(mapped)
        
        return ReviewChoice(
            category="knowledge_base",
            selected_value=",".join(converted_selections),
            reasoning=reasoning,
            confidence_level="high" if len(converted_selections) > 0 else "low"
        )
    
    def _parse_trait_response(self, response: str, category: str) -> Optional[ReviewChoice]:
        """Parse personality trait selection response."""
        
        # Extract decision
        decision_match = re.search(r'DECISION:\s*([^\n]+)', response, re.IGNORECASE)
        if not decision_match:
            return None
        
        decision_text = decision_match.group(1).strip()
        
        # Extract reasoning
        reasoning_match = re.search(r'REASONING:\s*(.*)', response, re.IGNORECASE | re.DOTALL)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "No reasoning provided"
        
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
        
        return ReviewChoice(
            category=category,
            selected_value=selected_value,
            reasoning=reasoning,
            confidence_level="high"
        )
    
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
            )
            
            # 3. Review categories in order
            review_categories = [
                "knowledge_base",
                "virtues_pool",
                "flaws_pool",
                "approaches", 
                "tones",
                "motive_alignment",
                "role_archtypes",
                "orientation_io",
                "polarity_cd",
                "self_regard_options"
            ]
            
            print(f"🔄 Processing {len(review_categories)} review categories...")
            
            for i, category in enumerate(review_categories, 1):
                print(f"\n📝 [{i}/{len(review_categories)}] Reviewing: {category.replace('_', ' ').title()}")
                
                # Generate prompt
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
            
            # 4. Generate final profile updates
            print(f"\n💾 Generating profile updates...")
            session.final_profile_updates = self._generate_profile_updates(session.review_choices)
            
            # 5. Complete session
            session.completion_status = "completed"
            session.processing_time_seconds = time.time() - start_time
            
            # Print audit summary at the top
            print(f"\n📊 AUDIT SUMMARY")
            print("=" * 50)
            print(f"   ⏱️  Processing time: {session.processing_time_seconds:.1f} seconds")
            print(f"   🔄 API calls made: {session.total_api_calls}")
            print(f"   ✅ Choices recorded: {len(session.review_choices)}")
            print(f"   📝 Categories reviewed: {len(review_categories)}")
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
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving review session: {e}")
            return False

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
            dry_run=args.dry_run
        )
        
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