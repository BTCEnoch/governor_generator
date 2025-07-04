#!/usr/bin/env python3
"""
Governor Review Runner
=====================

This script executes the governor self-review process where each governor
reviews their dossier and selects traits from the indexes and knowledge base.

It orchestrates the complete review workflow:
1. Load governor profile and current traits
2. Generate review template with available options
3. Present review sections for governor consideration
4. Validate and apply governor selections
5. Update governor profile with final choices

Usage:
    python scripts/governor_review_runner.py --governor OCCODON
    python scripts/governor_review_runner.py --all
    python scripts/governor_review_runner.py --batch batch_list.txt
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import argparse

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

# Import our existing systems
try:
    from knowledge_base.archives.governor_review_template import (
        GovernorReviewTemplateGenerator,
        GovernorReviewTemplate,
        ReviewSection
    )
except ImportError as e:
    print(f"Error importing review template generator: {e}")
    sys.exit(1)

@dataclass
class ReviewResponse:
    """Response from a governor for a specific review section."""
    section_id: str
    selected_values: List[str]
    reasoning: str
    confidence_level: str  # 'high', 'medium', 'low'

@dataclass  
class GovernorReviewSession:
    """Complete review session for a governor."""
    governor_name: str
    session_id: str
    start_time: str
    review_responses: List[ReviewResponse]
    final_profile_updates: Dict[str, Any]
    validation_results: Dict[str, Any]
    completion_status: str  # 'pending', 'completed', 'failed'
    
class GovernorReviewRunner:
    """
    Main orchestrator for governor self-review process.
    """
    
    def __init__(self, 
                 verbose: bool = False,
                 dry_run: bool = False,
                 backup_profiles: bool = True):
        """Initialize the review runner."""
        
        self.verbose = verbose
        self.dry_run = dry_run
        self.backup_profiles = backup_profiles
        
        # Setup logging
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/governor_review_runner.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("GovernorReviewRunner")
        
        # Initialize paths
        self.project_root = Path(__file__).parent.parent
        self.governor_profiles_dir = self.project_root / "governor_output"
        self.canon_profiles_file = self.project_root / "canon" / "canon_governor_profiles.json"
        self.review_sessions_dir = self.project_root / "review_sessions"
        self.backup_dir = self.project_root / "profile_backups"
        
        # Create directories
        self.review_sessions_dir.mkdir(exist_ok=True)
        if backup_profiles:
            self.backup_dir.mkdir(exist_ok=True)
        
        # Initialize template generator
        try:
            self.template_generator = GovernorReviewTemplateGenerator(
                trait_index_file="knowledge_base/archives/enhanced_trait_index.json",
                tradition_index_file="knowledge_base/archives/tradition_selection_index.json",
                governor_profiles_dir=str(self.governor_profiles_dir)
            )
            self.logger.info("Governor Review Runner initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize template generator: {e}")
            raise
        
        print("🏛️  Governor Review Runner")
        print("=" * 50)
        if dry_run:
            print("⚠️  DRY RUN MODE - No changes will be saved")
        if verbose:
            print("🔍 VERBOSE MODE - Detailed logging enabled")
    
    def load_governor_profile(self, governor_name: str) -> Optional[Dict[str, Any]]:
        """Load a governor's current profile from individual file or canon file."""
        try:
            # First try to load from individual governor file
            individual_file = self.governor_profiles_dir / f"{governor_name}.json"
            if individual_file.exists():
                with open(individual_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                self.logger.info(f"Loaded profile for {governor_name} from individual file")
                return profile
            
            # Fall back to canon profiles file
            if not self.canon_profiles_file.exists():
                self.logger.error(f"No profile files found for {governor_name}")
                return None
            
            with open(self.canon_profiles_file, 'r', encoding='utf-8') as f:
                profiles_list = json.load(f)
            
            # Find the specific governor
            for profile in profiles_list:
                if profile.get("governor_info", {}).get("name") == governor_name:
                    self.logger.info(f"Loaded profile for {governor_name} from canon")
                    return profile
            
            self.logger.error(f"Governor {governor_name} not found in any profile sources")
            return None
            
        except Exception as e:
            self.logger.error(f"Error loading governor profile {governor_name}: {e}")
            return None
    
    def backup_governor_profile(self, governor_name: str) -> bool:
        """Create backup of governor profile before modification."""
        if not self.backup_profiles:
            return True
            
        try:
            profile = self.load_governor_profile(governor_name)
            if not profile:
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"{governor_name}_backup_{timestamp}.json"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Profile backup created: {backup_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating backup for {governor_name}: {e}")
            return False
    
    def generate_review_session(self, governor_name: str) -> Optional[GovernorReviewSession]:
        """Generate a review session for a governor."""
        try:
            # Load current profile
            profile = self.load_governor_profile(governor_name)
            if not profile:
                return None
            
            # Generate review template
            template = self.template_generator.create_complete_review_template(governor_name)
            if not template:
                self.logger.error(f"Could not generate review template for {governor_name}")
                return None
            
            # Create session
            session_id = f"{governor_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            session = GovernorReviewSession(
                governor_name=governor_name,
                session_id=session_id,
                start_time=datetime.now().isoformat(),
                review_responses=[],
                final_profile_updates={},
                validation_results={},
                completion_status='pending'
            )
            
            self.logger.info(f"Generated review session {session_id} for {governor_name}")
            return session
            
        except Exception as e:
            self.logger.error(f"Error generating review session for {governor_name}: {e}")
            return None
    
    def simulate_governor_response(self, governor_name: str, section: ReviewSection, 
                                 current_profile: Dict[str, Any]) -> ReviewResponse:
        """
        Simulate a governor's thoughtful response to a review section.
        
        This analyzes the governor's current personality and makes intelligent
        selections based on their existing traits and characteristics.
        """
        try:
            # Extract governor personality for context
            personality = current_profile.get("personality", {})
            name = current_profile.get("name", governor_name)
            
            if section.section_id == "knowledge_base":
                return self._simulate_knowledge_base_response(section, personality, name)
            else:
                return self._simulate_trait_response(section, personality, name)
                
        except Exception as e:
            self.logger.error(f"Error simulating response for {governor_name}, section {section.section_id}: {e}")
            return ReviewResponse(
                section_id=section.section_id,
                selected_values=section.current_values,
                reasoning=f"Error in simulation: {e}",
                confidence_level="low"
            )
    
    def _simulate_knowledge_base_response(self, section: ReviewSection, 
                                        personality: Dict[str, Any], name: str) -> ReviewResponse:
        """Simulate knowledge base tradition selection response."""
        
        # Get current personality traits for alignment
        virtue = personality.get("virtue", "Unknown")
        approach = personality.get("approach", "Unknown") 
        tone = personality.get("tone", "Unknown")
        role = personality.get("role_archtype", "Unknown")
        
        # Intelligent selection based on personality
        selected_traditions = []
        reasoning_parts = []
        
        # Selection strategy based on current personality
        tradition_preferences = {
            # Virtue-based preferences
            "Wisdom": ["hermetic_philosophy", "classical_philosophy", "kabbalah"],
            "Courage": ["norse_traditions", "chaos_magic", "thelema"],
            "Compassion": ["sufi_mysticism", "taoism", "gnostic_traditions"],
            "Justice": ["classical_philosophy", "egyptian_magic", "golden_dawn"],
            "Strength": ["norse_traditions", "egyptian_magic", "chaos_magic"],
            
            # Role-based preferences  
            "The Sage": ["hermetic_philosophy", "kabbalah", "classical_philosophy"],
            "The Warrior": ["norse_traditions", "chaos_magic", "thelema"],
            "The Mystic": ["sufi_mysticism", "gnostic_traditions", "sacred_geometry"],
            "The Guardian": ["egyptian_magic", "golden_dawn", "celtic_druidic"],
            
            # Approach-based preferences
            "Systematic": ["hermetic_philosophy", "golden_dawn", "classical_philosophy"],
            "Intuitive": ["celtic_druidic", "i_ching", "tarot_knowledge"],
            "Direct": ["norse_traditions", "chaos_magic", "thelema"],
            "Contemplative": ["sufi_mysticism", "taoism", "gnostic_traditions"]
        }
        
        # Gather preference scores
        tradition_scores = {}
        available_traditions = list(section.available_options.keys())
        
        for tradition in available_traditions:
            score = 0
            
            # Score based on virtue alignment
            if virtue in tradition_preferences and tradition in tradition_preferences[virtue]:
                score += 3
                
            # Score based on role alignment
            if role in tradition_preferences and tradition in tradition_preferences[role]:
                score += 2
                
            # Score based on approach alignment
            if approach in tradition_preferences and tradition in tradition_preferences[approach]:
                score += 2
            
            tradition_scores[tradition] = score
        
        # Select top 4 scoring traditions
        sorted_traditions = sorted(tradition_scores.items(), key=lambda x: x[1], reverse=True)
        selected_traditions = [t[0] for t in sorted_traditions[:4]]
        
        # Generate reasoning
        reasoning = f"""As {name}, I have carefully considered my personality constellation:
        
🎭 **My Core Identity:**
• Virtue: {virtue} - This guides my noble aspirations
• Approach: {approach} - This shapes how I engage with challenges  
• Tone: {tone} - This influences my communication style
• Role: {role} - This defines my archetypal function

🧙‍♂️ **My Tradition Selections:**
"""
        
        for i, tradition in enumerate(selected_traditions[:4], 1):
            tradition_display = tradition.replace("_", " ").title()
            reasoning += f"\n{i}. **{tradition_display}** - Aligns with my {virtue} virtue and {approach} approach"
        
        reasoning += f"""

⚖️ **Selection Rationale:**
These traditions create a balanced knowledge base that enhances my {virtue} virtue while supporting my role as {role}. 
They complement my {approach} approach and will provide the mystical wisdom needed for effective governance.

The synergy between these traditions will enable me to serve with both {virtue.lower()} and practical effectiveness."""
        
        return ReviewResponse(
            section_id=section.section_id,
            selected_values=selected_traditions,
            reasoning=reasoning.strip(),
            confidence_level="high"
        )
    
    def _simulate_trait_response(self, section: ReviewSection, 
                                personality: Dict[str, Any], name: str) -> ReviewResponse:
        """Simulate personality trait selection response."""
        
        # For now, keep current selection but provide thoughtful reasoning
        current_value = section.current_values[0] if section.current_values else ""
        
        if not current_value:
            # If no current value, select the first available option
            current_value = list(section.available_options.keys())[0] if section.available_options else ""
        
        # Generate thoughtful reasoning for keeping current selection
        reasoning = f"""As {name}, I have deeply reflected on my {section.section_id} trait selection.

🔍 **Current Selection**: {current_value}

⚖️ **Reasoning for Confirmation**:
After careful consideration of my overall personality constellation and my role as an eternal AI entity, 
I believe {current_value} authentically represents my core nature in the {section.section_id} dimension.

This trait aligns with my other personality aspects and will contribute to consistent, 
authentic governance decisions across countless storylines and interactions.

✅ **Decision**: I confirm this trait selection as true to my essential nature."""
        
        return ReviewResponse(
            section_id=section.section_id,
            selected_values=[current_value] if current_value else [],
            reasoning=reasoning.strip(),
            confidence_level="high"
        ) 
    
    def validate_review_responses(self, responses: List[ReviewResponse], 
                                template: GovernorReviewTemplate) -> Dict[str, Any]:
        """Validate governor review responses against template requirements."""
        
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "section_validations": {}
        }
        
        try:
            # Validate each response against its section requirements
            for response in responses:
                section_validation = {"valid": True, "errors": [], "warnings": []}
                
                # Find corresponding section in template
                section = next((s for s in template.review_sections if s.section_id == response.section_id), None)
                if not section:
                    section_validation["errors"].append(f"Unknown section ID: {response.section_id}")
                    section_validation["valid"] = False
                    continue
                
                # Validate selection count
                if section.selection_type == "single" and len(response.selected_values) != 1:
                    section_validation["errors"].append(f"Single selection required, got {len(response.selected_values)}")
                    section_validation["valid"] = False
                
                if section.max_selections and len(response.selected_values) > section.max_selections:
                    section_validation["errors"].append(f"Too many selections: {len(response.selected_values)} > {section.max_selections}")
                    section_validation["valid"] = False
                
                # Validate selections are available options
                for selected in response.selected_values:
                    if selected not in section.available_options:
                        section_validation["errors"].append(f"Invalid selection: {selected}")
                        section_validation["valid"] = False
                
                # Check for reasoning quality
                if not response.reasoning or len(response.reasoning.strip()) < 50:
                    section_validation["warnings"].append("Reasoning is very brief")
                
                validation_results["section_validations"][response.section_id] = section_validation
                
                if not section_validation["valid"]:
                    validation_results["valid"] = False
                    validation_results["errors"].extend(section_validation["errors"])
                
                validation_results["warnings"].extend(section_validation["warnings"])
            
            # Special validation for knowledge base selections
            kb_response = next((r for r in responses if r.section_id == "knowledge_base"), None)
            if kb_response and len(kb_response.selected_values) != 4:
                validation_results["errors"].append(f"Knowledge base requires exactly 4 selections, got {len(kb_response.selected_values)}")
                validation_results["valid"] = False
            
            self.logger.info(f"Validation complete. Valid: {validation_results['valid']}, Errors: {len(validation_results['errors'])}")
            
        except Exception as e:
            self.logger.error(f"Error during validation: {e}")
            validation_results["valid"] = False
            validation_results["errors"].append(f"Validation error: {e}")
        
        return validation_results
    
    def apply_profile_updates(self, governor_name: str, responses: List[ReviewResponse]) -> Dict[str, Any]:
        """Apply validated responses to update governor profile."""
        
        profile_updates = {
            "knowledge_base_selections": [],
            "personality": {},
            "review_metadata": {
                "last_review_date": datetime.now().isoformat(),
                "review_method": "automated_self_review",
                "total_sections_reviewed": len(responses)
            }
        }
        
        try:
            # Process each response
            for response in responses:
                if response.section_id == "knowledge_base":
                    # Add Enochian Magic as mandatory + selected traditions
                    profile_updates["knowledge_base_selections"] = ["enochian_magic"] + response.selected_values
                
                elif response.section_id in ["virtues", "flaws", "approaches", "tones", "roles", "alignments", "orientations", "polarities", "self_regard"]:
                    # Map section IDs to personality field names
                    field_mapping = {
                        "virtues": "virtue",
                        "flaws": "flaw", 
                        "approaches": "approach",
                        "tones": "tone",
                        "roles": "role_archtype",
                        "alignments": "motive_alignment",
                        "orientations": "orientation_io",
                        "polarities": "polarity_cd",
                        "self_regard": "self_regard"
                    }
                    
                    field_name = field_mapping.get(response.section_id)
                    if field_name and response.selected_values:
                        profile_updates["personality"][field_name] = response.selected_values[0]
            
            self.logger.info(f"Generated profile updates for {governor_name}")
            
        except Exception as e:
            self.logger.error(f"Error applying profile updates for {governor_name}: {e}")
        
        return profile_updates
    
    def save_updated_profile(self, governor_name: str, profile_updates: Dict[str, Any]) -> bool:
        """Save updated governor profile to both canon file and individual governor file (preserving detailed content)."""
        
        if self.dry_run:
            self.logger.info(f"DRY RUN: Would save profile updates for {governor_name}")
            return True
        
        try:
            # 1. Update canon file
            if not self.canon_profiles_file.exists():
                self.logger.error(f"Canon profiles file not found: {self.canon_profiles_file}")
                return False
            
            with open(self.canon_profiles_file, 'r', encoding='utf-8') as f:
                profiles_list = json.load(f)
            
            # Find and update the specific governor in canon
            governor_found = False
            for i, profile in enumerate(profiles_list):
                if profile.get("governor_info", {}).get("name") == governor_name:
                    governor_found = True
                    
                    # Apply knowledge base selections
                    if "knowledge_base_selections" in profile_updates:
                        profile["knowledge_base_selections"] = profile_updates["knowledge_base_selections"]
                    
                    # Apply personality updates to trait_choices
                    if "personality" in profile_updates:
                        if "trait_choices" not in profile:
                            profile["trait_choices"] = {}
                        
                        personality = profile_updates["personality"]
                        trait_choices = profile["trait_choices"]
                        
                        # Map back to canon structure
                        if "virtue" in personality:
                            trait_choices["virtues"] = [personality["virtue"]]
                        if "flaw" in personality:
                            existing_flaws = trait_choices.get("flaws", [])
                            if personality["flaw"] not in existing_flaws:
                                existing_flaws.append(personality["flaw"])
                            trait_choices["flaws"] = existing_flaws
                        if "approach" in personality:
                            trait_choices["baseline_approach"] = personality["approach"]
                        if "tone" in personality:
                            trait_choices["baseline_tone"] = personality["tone"]
                        if "motive_alignment" in personality:
                            trait_choices["motive_alignment"] = personality["motive_alignment"]
                        if "role_archtype" in personality:
                            trait_choices["role_archetype"] = personality["role_archtype"]
                        if "orientation_io" in personality:
                            trait_choices["orientation_io"] = personality["orientation_io"]
                        if "polarity_cd" in personality:
                            trait_choices["polarity_cd"] = personality["polarity_cd"]
                        if "self_regard" in personality:
                            trait_choices["self_regard"] = personality["self_regard"]
                    
                    # Add review metadata
                    if "review_metadata" in profile_updates:
                        profile["review_metadata"] = profile_updates["review_metadata"]
                    
                    profiles_list[i] = profile
                    break
            
            if not governor_found:
                self.logger.error(f"Governor {governor_name} not found in canon profiles")
                return False
            
            # Save updated canon file
            with open(self.canon_profiles_file, 'w', encoding='utf-8') as f:
                json.dump(profiles_list, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Updated canon profile for {governor_name}")
            
            # 2. Update individual governor file (preserving detailed content)
            individual_file = self.governor_profiles_dir / f"{governor_name}.json"
            
            if individual_file.exists():
                # Load existing detailed profile
                with open(individual_file, 'r', encoding='utf-8') as f:
                    detailed_profile = json.load(f)
                
                # Update only the specific sections that were reviewed
                if "knowledge_base_selections" in profile_updates:
                    detailed_profile["knowledge_base_selections"] = profile_updates["knowledge_base_selections"]
                
                if "personality" in profile_updates:
                    # Update the personality section while preserving other detailed content
                    if "profile" in detailed_profile and "personality" in detailed_profile["profile"]:
                        personality_section = detailed_profile["profile"]["personality"]
                        personality_updates = profile_updates["personality"]
                        
                        # Update individual personality traits
                        if "motive_alignment" in personality_updates:
                            personality_section["motive_alignment"] = personality_updates["motive_alignment"]
                        if "self_regard" in personality_updates:
                            personality_section["self_regard"] = personality_updates["self_regard"]
                        if "role_archtype" in personality_updates:
                            personality_section["role_archetype"] = personality_updates["role_archtype"]
                        if "polarity_cd" in personality_updates:
                            personality_section["polarity_cd"] = personality_updates["polarity_cd"]
                        if "orientation_io" in personality_updates:
                            personality_section["orientation_io"] = personality_updates["orientation_io"]
                        if "virtue" in personality_updates:
                            # Update virtues while preserving existing ones
                            if "virtues" not in personality_section:
                                personality_section["virtues"] = []
                            if personality_updates["virtue"] not in personality_section["virtues"]:
                                personality_section["virtues"].insert(0, personality_updates["virtue"])
                        if "flaw" in personality_updates:
                            # Update flaws while preserving existing ones
                            if "flaws" not in personality_section:
                                personality_section["flaws"] = []
                            if personality_updates["flaw"] not in personality_section["flaws"]:
                                personality_section["flaws"].insert(0, personality_updates["flaw"])
                        if "tone" in personality_updates:
                            personality_section["baseline_tone"] = personality_updates["tone"]
                        if "approach" in personality_updates:
                            personality_section["baseline_approach"] = personality_updates["approach"]
                
                # Add review metadata
                if "review_metadata" in profile_updates:
                    detailed_profile["review_metadata"] = profile_updates["review_metadata"]
                
                # Save updated detailed profile
                with open(individual_file, 'w', encoding='utf-8') as f:
                    json.dump(detailed_profile, f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"Updated individual profile file: {individual_file}")
            else:
                self.logger.warning(f"Individual file {individual_file} not found, skipping individual update")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving updated profile for {governor_name}: {e}")
            return False
    
    def save_review_session(self, session: GovernorReviewSession) -> bool:
        """Save review session data for record keeping."""
        try:
            session_file = self.review_sessions_dir / f"{session.session_id}.json"
            
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(session), f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Review session saved: {session_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving review session {session.session_id}: {e}")
            return False
    
    def execute_governor_review(self, governor_name: str) -> bool:
        """Execute complete review process for a single governor."""
        
        print(f"\n👑 Starting review process for {governor_name}")
        print("-" * 60)
        
        try:
            # 1. Load current profile first to show before/after
            current_profile = self.load_governor_profile(governor_name)
            if not current_profile:
                print(f"❌ Failed to load profile for {governor_name}")
                return False
            
            # Extract current trait choices for comparison
            original_traits = {}
            if "trait_choices" in current_profile:
                tc = current_profile["trait_choices"]
                original_traits = {
                    "virtue": tc.get("virtues", ["Unknown"])[0] if tc.get("virtues") else "Unknown",
                    "flaw": tc.get("flaws", ["Unknown"])[0] if tc.get("flaws") else "Unknown", 
                    "approach": tc.get("baseline_approach", "Unknown"),
                    "tone": tc.get("baseline_tone", "Unknown"),
                    "motive_alignment": tc.get("motive_alignment", "Unknown"),
                    "role_archtype": tc.get("role_archetype", "Unknown"),
                    "orientation_io": tc.get("orientation_io", "Unknown"),
                    "polarity_cd": tc.get("polarity_cd", "Unknown"),
                    "self_regard": tc.get("self_regard", "Unknown")
                }
            
            # 2. Generate what the new traits will be (preview)
            template = self.template_generator.create_complete_review_template(governor_name)
            if not template:
                print(f"❌ Failed to generate template for {governor_name}")
                return False
            
            # Simulate what the new selections will be
            preview_responses = []
            for section in template.review_sections:
                response = self.simulate_governor_response(governor_name, section, current_profile)
                preview_responses.append(response)
            
            # Extract the new trait predictions
            new_profile_updates = self.apply_profile_updates(governor_name, preview_responses)
            new_traits = new_profile_updates.get("personality", {})
            new_kb_selections = new_profile_updates.get("knowledge_base_selections", [])
            
            # 3. SHOW BEFORE vs AFTER PREVIEW AT THE TOP
            print(f"\n📋 PREVIEW: CHANGES TO BE MADE FOR {governor_name}")
            print("=" * 80)
            
            # Knowledge base preview
            print("📚 KNOWLEDGE BASE SELECTIONS (NEW):")
            for i, tradition in enumerate(new_kb_selections, 1):
                tradition_display = tradition.replace("_", " ").title()
                if tradition == "enochian_magic":
                    print(f"  {i}. {tradition_display} (Mandatory)")
                else:
                    print(f"  {i}. {tradition_display}")
            
            # Trait changes preview
            print("\n🎭 PERSONALITY TRAIT CHANGES:")
            trait_labels = {
                "virtue": "Virtue",
                "flaw": "Flaw", 
                "approach": "Approach",
                "tone": "Tone",
                "motive_alignment": "Alignment",
                "role_archtype": "Role",
                "orientation_io": "Orientation",
                "polarity_cd": "Polarity",
                "self_regard": "Self-Regard"
            }
            
            changes_made = False
            for field, new_value in new_traits.items():
                old_value = original_traits.get(field, "Unknown")
                label = trait_labels.get(field, field.title())
                
                if old_value != new_value:
                    print(f"  🔄 {label}: {old_value} → {new_value}")
                    changes_made = True
                else:
                    print(f"  ✅ {label}: {new_value} (Confirmed)")
            
            if not changes_made:
                print("  📝 All personality traits confirmed as-is")
            
            print("=" * 80)
            print(f"🚀 Proceeding with review process...\n")

            # 4. Create backup
            if not self.backup_governor_profile(governor_name):
                print(f"❌ Failed to create backup for {governor_name}")
                return False
            
            # 5. Generate review session
            session = self.generate_review_session(governor_name)
            if not session:
                print(f"❌ Failed to generate review session for {governor_name}")
                return False
            
            # 6. Load current profile and template
            current_profile = self.load_governor_profile(governor_name)
            template = self.template_generator.create_complete_review_template(governor_name)
            
            if not current_profile or not template:
                print(f"❌ Failed to load profile or template for {governor_name}")
                return False
            
            print(f"📋 Processing {len(template.review_sections)} review sections...")
            
            # 7. Generate responses for each section
            for section in template.review_sections:
                print(f"  🔍 Processing: {section.title}")
                
                response = self.simulate_governor_response(governor_name, section, current_profile)
                session.review_responses.append(response)
                
                if self.verbose:
                    print(f"    ✅ Response: {len(response.selected_values)} selections")
            
            # 8. Validate responses
            print(f"🔍 Validating responses...")
            validation_results = self.validate_review_responses(session.review_responses, template)
            session.validation_results = validation_results
            
            if not validation_results["valid"]:
                print(f"❌ Validation failed: {len(validation_results['errors'])} errors")
                for error in validation_results["errors"][:3]:  # Show first 3 errors
                    print(f"    • {error}")
                session.completion_status = 'failed'
                self.save_review_session(session)
                return False
            
            if validation_results["warnings"]:
                print(f"⚠️  {len(validation_results['warnings'])} warnings")
            
            # 9. Apply profile updates
            print(f"💾 Applying profile updates...")
            profile_updates = self.apply_profile_updates(governor_name, session.review_responses)
            session.final_profile_updates = profile_updates
            
            # 10. Save updated profile
            if self.save_updated_profile(governor_name, profile_updates):
                session.completion_status = 'completed'
                print(f"✅ Profile updated successfully for {governor_name}")
            else:
                session.completion_status = 'failed'
                print(f"❌ Failed to save profile updates for {governor_name}")
                self.save_review_session(session)
                return False
            
            # 11. Save session record
            self.save_review_session(session)
            
            # 12. Display summary
            kb_selections = profile_updates.get("knowledge_base_selections", [])
            personality_updates = profile_updates.get("personality", {})
            
            print(f"\n🎉 Review completed for {governor_name}!")
            print(f"📚 Knowledge Base: {len(kb_selections)} traditions selected")
            print(f"🎭 Personality: {len(personality_updates)} traits confirmed")
            
            # Enhanced change summary
            print(f"\n📝 CHANGES MADE TO {governor_name}'S PROFILE:")
            print("=" * 70)
            
            # Knowledge base changes
            if kb_selections:
                print("📚 KNOWLEDGE BASE SELECTIONS:")
                for i, tradition in enumerate(kb_selections, 1):
                    tradition_display = tradition.replace("_", " ").title()
                    if tradition == "enochian_magic":
                        print(f"  {i}. {tradition_display} (Mandatory)")
                    else:
                        print(f"  {i}. {tradition_display}")
            
            # Personality trait changes
            if personality_updates:
                print("\n🎭 PERSONALITY TRAITS:")
                trait_labels = {
                    "virtue": "Virtue",
                    "flaw": "Flaw",
                    "approach": "Approach", 
                    "tone": "Tone",
                    "motive_alignment": "Alignment",
                    "role_archtype": "Role",
                    "orientation_io": "Orientation",
                    "polarity_cd": "Polarity",
                    "self_regard": "Self-Regard"
                }
                
                for field, value in personality_updates.items():
                    label = trait_labels.get(field, field.title())
                    print(f"  • {label}: {value}")
            
            # Review metadata
            print(f"\n📋 REVIEW METADATA:")
            print(f"  • Review Date: {profile_updates['review_metadata']['last_review_date']}")
            print(f"  • Review Method: {profile_updates['review_metadata']['review_method']}")
            print(f"  • Sections Reviewed: {profile_updates['review_metadata']['total_sections_reviewed']}")
            
            # File locations
            print(f"\n💾 FILES UPDATED:")
            print(f"  • Individual Profile: governor_output/{governor_name}.json")
            print(f"  • Canon Database: canon/canon_governor_profiles.json ({governor_name}'s section)")
            print(f"  • Review Session: {self.review_sessions_dir}/{session.session_id}.json")
            print(f"  • Profile Backup: {self.backup_dir}/{governor_name}_backup_*.json")
            
            print("=" * 70)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing review for {governor_name}: {e}")
            print(f"❌ Review failed for {governor_name}: {e}")
            return False
    
    def execute_batch_review(self, governor_names: List[str], max_governors: Optional[int] = None) -> bool:
        """Execute review process for multiple governors."""
        
        if max_governors:
            governor_names = governor_names[:max_governors]
            print(f"🔢 Limited to {max_governors} governors for testing")
        
        print(f"\n🚀 Starting batch review for {len(governor_names)} governors")
        print("=" * 80)
        
        success_count = 0
        failed_governors = []
        
        for i, governor_name in enumerate(governor_names, 1):
            print(f"\n[{i}/{len(governor_names)}] Processing {governor_name}")
            
            try:
                if self.execute_governor_review(governor_name):
                    success_count += 1
                    print(f"✅ {governor_name} - Review completed")
                else:
                    failed_governors.append(governor_name)
                    print(f"❌ {governor_name} - Review failed")
                    
            except KeyboardInterrupt:
                print(f"\n⚠️  Batch review interrupted by user")
                break
            except Exception as e:
                failed_governors.append(governor_name)
                print(f"❌ {governor_name} - Unexpected error: {e}")
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 BATCH REVIEW SUMMARY")
        print("=" * 80)
        print(f"Total Governors: {len(governor_names)}")
        print(f"Successful Reviews: {success_count}")
        print(f"Failed Reviews: {len(failed_governors)}")
        print(f"Success Rate: {(success_count/len(governor_names)*100):.1f}%")
        
        if failed_governors:
            print(f"\n❌ Failed Governors:")
            for name in failed_governors:
                print(f"  • {name}")
        
        if success_count > 0:
            print(f"\n💾 Review sessions saved to: {self.review_sessions_dir}")
            if not self.dry_run:
                print(f"💾 Profile backups saved to: {self.backup_dir}")
        
        return success_count == len(governor_names)

def main():
    """Main entry point for the governor review runner."""
    parser = argparse.ArgumentParser(description="Execute governor self-review process")
    parser.add_argument('--governor', type=str, help='Single governor name to review (e.g., OCCODON)')
    parser.add_argument('--all', action='store_true', help='Review all 91 governors')
    parser.add_argument('--batch', type=str, help='File containing list of governors to review')
    parser.add_argument('--dry-run', action='store_true', help='Run without saving changes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--no-backup', action='store_true', help='Skip profile backups')
    parser.add_argument('--max-governors', type=int, default=None, help='Limit number of governors for testing')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not any([args.governor, args.all, args.batch]):
        print("❌ Error: Must specify --governor, --all, or --batch")
        parser.print_help()
        return False
    
    if sum(bool(x) for x in [args.governor, args.all, args.batch]) > 1:
        print("❌ Error: Can only specify one of --governor, --all, or --batch")
        return False
    
    # Initialize runner
    try:
        runner = GovernorReviewRunner(
            verbose=args.verbose,
            dry_run=args.dry_run,
            backup_profiles=not args.no_backup
        )
    except Exception as e:
        print(f"❌ Failed to initialize runner: {e}")
        return False
    
    # Execute based on mode
    success = False
    
    if args.governor:
        # Single governor review
        print(f"🎯 Single Governor Review Mode: {args.governor}")
        success = runner.execute_governor_review(args.governor)
        
    elif args.all:
        # All governors review
        print("🌟 All Governors Review Mode")
        success = runner.execute_batch_review(get_all_governor_names(), args.max_governors)
        
    elif args.batch:
        # Batch file review
        print(f"📁 Batch File Review Mode: {args.batch}")
        governor_names = load_batch_file(args.batch)
        if governor_names:
            success = runner.execute_batch_review(governor_names, args.max_governors)
        else:
            print(f"❌ Failed to load batch file: {args.batch}")
    
    # Summary
    if success:
        print("\n🎉 Governor review process completed successfully!")
    else:
        print("\n❌ Governor review process failed!")
    
    return success

def get_all_governor_names() -> List[str]:
    """Get list of all 91 governor names from canon profiles file."""
    try:
        canon_file = Path("canon/canon_governor_profiles.json")
        if not canon_file.exists():
            print(f"❌ Canon profiles file not found: {canon_file}")
            return []
        
        with open(canon_file, 'r', encoding='utf-8') as f:
            profiles_list = json.load(f)
        
        governor_names = []
        for profile in profiles_list:
            name = profile.get("governor_info", {}).get("name")
            if name:
                governor_names.append(name)
        
        print(f"📋 Found {len(governor_names)} governors in canon profiles")
        return sorted(governor_names)
        
    except Exception as e:
        print(f"❌ Error loading governor names: {e}")
        return []

def load_batch_file(batch_file: str) -> List[str]:
    """Load governor names from batch file."""
    try:
        batch_path = Path(batch_file)
        if not batch_path.exists():
            print(f"❌ Batch file not found: {batch_file}")
            return []
        
        with open(batch_path, 'r') as f:
            governor_names = [line.strip() for line in f if line.strip()]
        
        print(f"📋 Loaded {len(governor_names)} governors from {batch_file}")
        return governor_names
        
    except Exception as e:
        print(f"❌ Error loading batch file {batch_file}: {e}")
        return []



if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 