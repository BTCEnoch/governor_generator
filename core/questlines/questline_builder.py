"""
Questline Builder
Core system for governors to create their own questlines
"""

import random
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from .schemas.questline_schemas import (
    Questline, Encounter, QuestlineType, DifficultyLevel, 
    EncounterType, QuestlineReward, EncounterChoice, QuestlineTemplate
)

logger = logging.getLogger(__name__)

class QuestlineBuilder:
    """
    Allows governors to create custom questlines based on their personality 
    and wisdom domains
    """
    
    def __init__(self, governor_data: Dict[str, Any]):
        """
        Initialize with governor data for personalized questline creation
        
        Args:
            governor_data: Complete governor profile with traits, wisdom, elements
        """
        self.governor_data = governor_data
        self.governor_name = governor_data.get('name', 'Unknown')
        self.element = governor_data.get('element', 'Spirit')
        self.wisdom_domains = governor_data.get('wisdom_domains', [])
        self.personality_traits = governor_data.get('personality_traits', {})
        
        # Load questline templates
        self.templates = self._load_questline_templates()
        
        logger.info(f"QuestlineBuilder initialized for {self.governor_name}")
    
    def create_questline(self, 
                        questline_type: QuestlineType,
                        difficulty: DifficultyLevel,
                        title: Optional[str] = None,
                        custom_theme: Optional[str] = None) -> Questline:
        """
        Create a new questline based on governor's personality and specified parameters
        
        Args:
            questline_type: Type of questline to create
            difficulty: Difficulty level for the questline
            title: Optional custom title, will generate if not provided
            custom_theme: Optional theme to focus on
            
        Returns:
            Complete Questline object ready for use
        """
        logger.info(f"Creating {questline_type.value} questline for {self.governor_name}")
        
        # Generate title if not provided
        if not title:
            title = self._generate_title(questline_type, custom_theme)
        
        # Create base questline structure
        questline = Questline(
            id="",  # Will be auto-generated
            creator_governor=self.governor_name,
            title=title,
            description=self._generate_description(questline_type, custom_theme),
            type=questline_type,
            difficulty=difficulty,
            estimated_duration=self._calculate_duration(difficulty),
            elemental_alignment=self.element,
            wisdom_themes=self._select_wisdom_themes(questline_type, custom_theme),
            tags=self._generate_tags(questline_type, difficulty)
        )
        
        # Generate encounters based on questline type and difficulty
        encounters = self._generate_encounters(questline_type, difficulty)
        questline.encounters = encounters
        
        # Create encounter flow (how encounters connect)
        questline.encounter_flow = self._create_encounter_flow(encounters)
        
        # Generate completion rewards
        questline.completion_rewards = self._generate_completion_rewards(difficulty, questline_type)
        
        logger.info(f"Created questline '{title}' with {len(encounters)} encounters")
        return questline
    
    def _generate_title(self, questline_type: QuestlineType, custom_theme: Optional[str] = None) -> str:
        """Generate a questline title based on governor personality and type"""
        
        # Base title patterns by type
        title_patterns = {
            QuestlineType.WISDOM_TRIAL: [
                "The {adjective} Trial of {concept}",
                "{governor}'s Test of {virtue}",
                "The {element} Path to {wisdom}"
            ],
            QuestlineType.ELEMENTAL_JOURNEY: [
                "Journey Through the {element} Realm",
                "The {element} Awakening",
                "{governor}'s {element} Mastery"
            ],
            QuestlineType.MYSTERY_INVESTIGATION: [
                "The Mystery of {artifact}",
                "Unraveling the {ancient} Secret",
                "The {hidden} Truth"
            ],
            QuestlineType.SPIRITUAL_ASCENSION: [
                "Ascension to {higher_plane}",
                "The {spiritual} Transformation",
                "Path to {enlightenment}"
            ],
            QuestlineType.ARTIFACT_QUEST: [
                "Quest for the {artifact}",
                "The {legendary} Artifact",
                "Seeking the {powerful} Relic"
            ],
            QuestlineType.GOVERNOR_ENCOUNTER: [
                "Meeting with {governor}",
                "The {governor} Audience",
                "Wisdom from {governor}"
            ],
            QuestlineType.RITUAL_COMPLETION: [
                "The {sacred} Ritual",
                "Completing the {ancient} Rite",
                "The {mystical} Ceremony"
            ],
            QuestlineType.KNOWLEDGE_SEEKING: [
                "Seeking {knowledge}",
                "The {hidden} Learning",
                "Wisdom of {tradition}"
            ]
        }
        
        # Select appropriate pattern
        patterns = title_patterns.get(questline_type, ["The {governor} Quest"])
        pattern = random.choice(patterns)
        
        # Fill in template variables
        replacements = {
            'governor': self.governor_name,
            'element': self.element,
            'adjective': self._get_personality_adjective(),
            'concept': custom_theme or self._get_wisdom_concept(),
            'virtue': self._get_virtue(),
            'wisdom': self._get_wisdom_concept(),
            'artifact': self._get_artifact_name(),
            'ancient': 'Ancient',
            'hidden': 'Hidden',
            'higher_plane': 'Higher Understanding',
            'spiritual': 'Spiritual',
            'enlightenment': 'Enlightenment',
            'legendary': 'Legendary',
            'powerful': 'Powerful',
            'sacred': 'Sacred',
            'mystical': 'Mystical',
            'knowledge': self._get_knowledge_domain(),
            'tradition': random.choice(self.wisdom_domains) if self.wisdom_domains else 'Wisdom'
        }
        
        # Replace placeholders
        for key, value in replacements.items():
            pattern = pattern.replace(f'{{{key}}}', value)
        
        return pattern
    
    def _generate_description(self, questline_type: QuestlineType, custom_theme: Optional[str] = None) -> str:
        """Generate questline description based on governor personality"""
        base_descriptions = {
            QuestlineType.WISDOM_TRIAL: f"A trial designed by {self.governor_name} to test wisdom and understanding.",
            QuestlineType.ELEMENTAL_JOURNEY: f"Journey through the {self.element} realm with {self.governor_name} as your guide.",
            QuestlineType.MYSTERY_INVESTIGATION: f"Investigate an ancient mystery with {self.governor_name}'s guidance.",
            QuestlineType.SPIRITUAL_ASCENSION: f"Ascend to higher spiritual understanding through {self.governor_name}'s teachings.",
            QuestlineType.ARTIFACT_QUEST: f"Seek a powerful artifact under {self.governor_name}'s direction.",
            QuestlineType.GOVERNOR_ENCOUNTER: f"A personal encounter with {self.governor_name} to gain wisdom.",
            QuestlineType.RITUAL_COMPLETION: f"Complete a sacred ritual guided by {self.governor_name}.",
            QuestlineType.KNOWLEDGE_SEEKING: f"Seek hidden knowledge with {self.governor_name}'s teachings."
        }
        
        description = base_descriptions.get(questline_type, f"A quest created by {self.governor_name}.")
        
        if custom_theme:
            description += f" This questline focuses on {custom_theme}."
        
        return description
    
    def _calculate_duration(self, difficulty: DifficultyLevel) -> int:
        """Calculate estimated duration based on difficulty"""
        duration_map = {
            DifficultyLevel.NOVICE: 15,
            DifficultyLevel.APPRENTICE: 30,
            DifficultyLevel.ADEPT: 45,
            DifficultyLevel.MASTER: 60,
            DifficultyLevel.GRANDMASTER: 90
        }
        return duration_map.get(difficulty, 30)
    
    def _select_wisdom_themes(self, questline_type: QuestlineType, custom_theme: Optional[str] = None) -> List[str]:
        """Select wisdom themes based on governor domains and questline type"""
        themes = []
        
        if custom_theme:
            themes.append(custom_theme)
        
        # Add governor's wisdom domains
        if self.wisdom_domains:
            themes.extend(self.wisdom_domains[:2])  # Take first 2
        
        # Add type-specific themes
        type_themes = {
            QuestlineType.WISDOM_TRIAL: ["wisdom", "testing", "knowledge"],
            QuestlineType.ELEMENTAL_JOURNEY: [self.element.lower(), "balance", "mastery"],
            QuestlineType.MYSTERY_INVESTIGATION: ["mystery", "discovery", "truth"],
            QuestlineType.SPIRITUAL_ASCENSION: ["ascension", "transformation", "enlightenment"],
            QuestlineType.ARTIFACT_QUEST: ["artifacts", "power", "seeking"],
            QuestlineType.GOVERNOR_ENCOUNTER: ["meeting", "dialogue", "guidance"],
            QuestlineType.RITUAL_COMPLETION: ["ritual", "ceremony", "sacred"],
            QuestlineType.KNOWLEDGE_SEEKING: ["knowledge", "learning", "wisdom"]
        }
        
        themes.extend(type_themes.get(questline_type, []))
        
        return list(set(themes))  # Remove duplicates
    
    def _generate_tags(self, questline_type: QuestlineType, difficulty: DifficultyLevel) -> List[str]:
        """Generate tags for questline categorization"""
        tags = [
            questline_type.value,
            difficulty.value,
            self.element.lower(),
            self.governor_name.lower()
        ]
        
        return tags
    
    def _get_personality_adjective(self) -> str:
        """Get an adjective based on governor personality"""
        adjectives = ["challenging", "enlightening", "mysterious", "profound", "sacred"]
        return random.choice(adjectives)
    
    def _get_wisdom_concept(self) -> str:
        """Get a wisdom concept from governor's domains"""
        if self.wisdom_domains:
            return random.choice(self.wisdom_domains)
        return "Wisdom"
    
    def _get_virtue(self) -> str:
        """Get a virtue for the questline"""
        virtues = ["Courage", "Wisdom", "Justice", "Temperance", "Faith", "Hope", "Charity"]
        return random.choice(virtues)
    
    def _get_artifact_name(self) -> str:
        """Generate an artifact name"""
        artifacts = ["Sacred Chalice", "Ancient Tome", "Crystal of Power", "Eternal Flame", "Mystic Orb"]
        return random.choice(artifacts)
    
    def _get_knowledge_domain(self) -> str:
        """Get a knowledge domain"""
        domains = ["Sacred Geometry", "Alchemy", "Astrology", "Mysticism", "Ancient Wisdom"]
        return random.choice(domains)
    
    def _load_questline_templates(self) -> Dict[QuestlineType, QuestlineTemplate]:
        """Load questline templates - placeholder for now"""
        return {}
    
    def _generate_encounters(self, questline_type: QuestlineType, difficulty: DifficultyLevel) -> List[Encounter]:
        """Generate encounters for the questline - placeholder for now"""
        return []
    
    def _create_encounter_flow(self, encounters: List[Encounter]) -> Dict[str, str]:
        """Create encounter flow mapping - placeholder for now"""
        return {}
    
    def _generate_completion_rewards(self, difficulty: DifficultyLevel, questline_type: QuestlineType) -> List[QuestlineReward]:
        """Generate completion rewards - placeholder for now"""
        return [] 