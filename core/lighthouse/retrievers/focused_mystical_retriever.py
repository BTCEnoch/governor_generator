#!/usr/bin/env python3
"""
Focused Mystical Knowledge Retriever
Provides concise, practical mystical knowledge for governors instead of massive Wikipedia dumps.
Curates specific mystical teachings based on governor canonical traits.
"""

import json
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path

# LOGGING SETUP
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FocusedMysticalRetriever")

class FocusedMysticalRetriever:
    """
    Curated mystical knowledge retriever that provides focused, practical knowledge
    for governors based on their canonical traits and spiritual needs.
    """
    
    def __init__(self):
        self.mystical_knowledge_base = self._build_curated_knowledge_base()
        
    def _build_curated_knowledge_base(self) -> Dict[str, Dict]:
        """Build curated mystical knowledge base with focused, practical content"""
        return {
            "spiritual_ascension": {
                "domain": "Spiritual Ascension",
                "core_teachings": [
                    "The path of spiritual ascension requires surrendering the ego-self to divine will",
                    "True spiritual ascension occurs through integration of shadow and light aspects",
                    "The ascension process involves raising one's vibrational frequency through purification",
                    "Mastery of the four elements (earth, water, fire, air) enables spiritual elevation",
                    "The Tree of Life serves as a map for the soul's journey toward divine union"
                ],
                "practices": [
                    "Daily meditation and contemplation of divine mysteries",
                    "Invocation of higher spiritual beings and guides", 
                    "Study of sacred texts and mystical philosophy",
                    "Energy work and chakra purification techniques",
                    "Service to others as a path of spiritual development"
                ],
                "wisdom_keys": [
                    "As above, so below - the microcosm reflects the macrocosm",
                    "Know thyself - self-knowledge is the foundation of all wisdom",
                    "The divine spark within seeks reunion with its source",
                    "Spiritual ascension is both journey and destination",
                    "Love is the ultimate transformative force in the universe"
                ],
                "word_count": 234
            },
            
            "hermetic_tradition": {
                "domain": "Hermetic Wisdom",
                "core_teachings": [
                    "The Emerald Tablet contains the fundamental principles of alchemical transformation",
                    "Mental transmutation - changing one's mental state changes reality",
                    "The Seven Hermetic Principles govern all planes of existence",
                    "Correspondence between inner and outer worlds enables magical working",
                    "The hermetic path seeks to reunite consciousness with divine source"
                ],
                "practices": [
                    "Study of hermetic texts and alchemical symbolism",
                    "Practical alchemy - both laboratory and spiritual work",
                    "Invocation and evocation of spiritual forces",
                    "Scrying and divination for higher guidance",
                    "Ritual magic for spiritual transformation"
                ],
                "wisdom_keys": [
                    "That which is below is like that which is above",
                    "Nothing rests; everything moves; everything vibrates",
                    "Every cause has its effect; every effect has its cause",
                    "As a man thinketh in his heart, so is he",
                    "The wise one rules the stars, the fool is ruled by them"
                ],
                "word_count": 198
            },
            
            "transformation_mysteries": {
                "domain": "Sacred Transformation",
                "core_teachings": [
                    "True transformation occurs through death and rebirth of consciousness",
                    "The alchemical process mirrors the soul's journey of purification",
                    "Transformation requires facing and integrating the shadow self",
                    "Sacred initiation catalyzes profound spiritual metamorphosis",
                    "The phoenix principle - rising from destruction into new life"
                ],
                "practices": [
                    "Ritual death and rebirth ceremonies",
                    "Deep shadow work and psychological integration",
                    "Alchemical meditation on solve et coagula",
                    "Vision quests and spiritual retreats",
                    "Working with plant spirit medicines and sacred substances"
                ],
                "wisdom_keys": [
                    "What does not kill you makes you stronger",
                    "The darkest hour comes before the dawn",
                    "Transformation is the law of life",
                    "From the ashes of the old, the new is born",
                    "Change is the only constant in the universe"
                ],
                "word_count": 187
            },
            
            "intuitive_wisdom": {
                "domain": "Divine Intuition",
                "core_teachings": [
                    "Intuition is the direct knowing that bypasses rational thought",
                    "The Third Eye chakra governs psychic perception and inner sight",
                    "Developing intuition requires quieting the analytical mind",
                    "Dreams and visions are messages from the unconscious wisdom",
                    "Synchronicities guide those who learn to read the signs"
                ],
                "practices": [
                    "Regular meditation to access inner knowing",
                    "Dream journaling and interpretation",
                    "Divination with tarot, runes, or other oracles",
                    "Psychic development exercises and energy sensing",
                    "Nature communion for earth-based wisdom"
                ],
                "wisdom_keys": [
                    "Trust your first instinct - it's usually correct",
                    "The body knows what the mind refuses to acknowledge",
                    "Silence the chatter to hear the whisper of truth",
                    "Intuition speaks through feeling, not thinking",
                    "The universe is always sending us guidance"
                ],
                "word_count": 172
            },
            
            "compassion_teachings": {
                "domain": "Divine Love and Compassion",
                "core_teachings": [
                    "Compassion is the natural expression of awakened consciousness",
                    "True compassion includes both self-love and love for others",
                    "The heart chakra is the bridge between earthly and spiritual realms",
                    "Loving-kindness meditation cultivates universal compassion",
                    "Service to others is service to the divine within all beings"
                ],
                "practices": [
                    "Daily loving-kindness meditation practice",
                    "Acts of service and charity without expectation",
                    "Heart-centered breathing and energy work",
                    "Forgiveness practices for self and others",
                    "Compassionate communication and deep listening"
                ],
                "wisdom_keys": [
                    "Love is the bridge between two hearts",
                    "Compassion without wisdom is mere sentiment",
                    "The greatest teaching is a life lived in love",
                    "See the divine in every being you encounter",
                    "Love heals all wounds, given time and patience"
                ],
                "word_count": 165
            },
            
            "ancient_wisdom": {
                "domain": "Timeless Sacred Knowledge",
                "core_teachings": [
                    "Ancient wisdom traditions preserve humanity's deepest spiritual insights",
                    "The perennial philosophy appears in all authentic mystical traditions",
                    "Sacred geometry reveals the mathematical foundations of creation",
                    "Mythology encodes profound spiritual truths in symbolic form",
                    "The Great Work is the transformation of lead consciousness into gold"
                ],
                "practices": [
                    "Study of ancient texts and sacred scriptures",
                    "Meditation on sacred symbols and mandalas",
                    "Chanting of sacred names and mantras",
                    "Temple rituals and ceremonial practices",
                    "Pilgrimage to sacred sites and power places"
                ],
                "wisdom_keys": [
                    "What has been will be again; what has been done will be done again",
                    "The ancients knew secrets we are only beginning to rediscover",
                    "Truth is one, but the wise call it by many names",
                    "The old ways contain power for those who understand",
                    "Wisdom is justified by her children"
                ],
                "word_count": 181
            },
            
            "mystical_philosophy": {
                "domain": "Philosophical Mysticism",
                "core_teachings": [
                    "Philosophy seeks wisdom; mysticism seeks direct experience of truth",
                    "The One is both transcendent beyond all and immanent within all",
                    "Consciousness is the fundamental reality from which all emerges",
                    "The soul's journey is a return to its divine source",
                    "Contemplation of eternal truths transforms the philosopher"
                ],
                "practices": [
                    "Contemplative meditation on philosophical questions",
                    "Study of Platonic and Neoplatonic texts",
                    "Dialectical reasoning and logical inquiry",
                    "Contemplation of mathematical and geometric principles",
                    "Integration of philosophical understanding with spiritual practice"
                ],
                "wisdom_keys": [
                    "The unexamined life is not worth living",
                    "Wonder is the beginning of wisdom",
                    "All things are full of gods",
                    "The cave allegory - awakening from the shadows of illusion",
                    "Philosophy is preparation for death - release from material bondage"
                ],
                "word_count": 167
            }
        }
    
    def retrieve_governor_knowledge(self, knowledge_selections: List[str], canonical_traits: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Retrieve focused mystical knowledge for a governor based on their selections.
        Returns concise, practical mystical content instead of massive Wikipedia dumps.
        """
        logger.info(f"🧠 Retrieving focused mystical knowledge for selections: {knowledge_selections}")
        
        # Map knowledge selections to our curated content
        knowledge_mapping = {
            "hermetic_tradition": "hermetic_tradition",
            "mystical_philosophy": "mystical_philosophy", 
            "wisdom_traditions": "ancient_wisdom",
            "transformation_mysteries": "transformation_mysteries",
            "ancient_wisdom": "ancient_wisdom",
            "compassion_teachings": "compassion_teachings",
            "spiritual_ascension": "spiritual_ascension",
            "intuitive_wisdom": "intuitive_wisdom"
        }
        
        retrieved_knowledge = {}
        total_word_count = 0
        
        for selection in knowledge_selections:
            mapped_key = knowledge_mapping.get(selection)
            if mapped_key and mapped_key in self.mystical_knowledge_base:
                knowledge_content = self.mystical_knowledge_base[mapped_key]
                retrieved_knowledge[selection] = knowledge_content
                total_word_count += knowledge_content.get("word_count", 0)
                logger.info(f"✅ Retrieved {selection} → {knowledge_content['domain']} ({knowledge_content.get('word_count', 0)} words)")
            else:
                logger.warning(f"⚠️ No curated content found for selection: {selection}")
        
        # Create focused summary
        summary = {
            "governor_knowledge_profile": {
                "selections_processed": knowledge_selections,
                "knowledge_domains": [content["domain"] for content in retrieved_knowledge.values()],
                "total_word_count": total_word_count,
                "knowledge_type": "curated_mystical_content"
            },
            "mystical_knowledge": retrieved_knowledge
        }
        
        logger.info(f"🎯 Knowledge retrieval complete: {len(retrieved_knowledge)} domains, {total_word_count} total words")
        return summary
    
    def get_practical_guidance(self, domain: str, situation: str = "general") -> Optional[Dict]:
        """Get practical mystical guidance for specific situations"""
        if domain in self.mystical_knowledge_base:
            knowledge = self.mystical_knowledge_base[domain]
            return {
                "domain": knowledge["domain"],
                "relevant_teachings": knowledge["core_teachings"][:3],  # Top 3 most relevant
                "recommended_practices": knowledge["practices"][:2],    # Top 2 practices
                "wisdom_guidance": knowledge["wisdom_keys"][:2]         # Top 2 wisdom keys
            }
        return None

def test_focused_retriever():
    """Test the focused mystical retriever"""
    logger.info("🧪 Testing Focused Mystical Retriever")
    
    retriever = FocusedMysticalRetriever()
    
    # Test with Occodon's knowledge selections
    occodon_selections = [
        "hermetic_tradition",
        "mystical_philosophy", 
        "transformation_mysteries",
        "compassion_teachings"
    ]
    
    knowledge = retriever.retrieve_governor_knowledge(occodon_selections)
    
    logger.info(f"📊 Results Summary:")
    logger.info(f"   Domains: {len(knowledge['mystical_knowledge'])}")
    logger.info(f"   Total Words: {knowledge['governor_knowledge_profile']['total_word_count']}")
    logger.info(f"   Knowledge Domains: {knowledge['governor_knowledge_profile']['knowledge_domains']}")
    
    # Save results
    with open("focused_mystical_retrieval_test.json", "w") as f:
        json.dump(knowledge, f, indent=2)
    
    logger.info("✅ Test complete - results saved to focused_mystical_retrieval_test.json")

if __name__ == "__main__":
    test_focused_retriever() 