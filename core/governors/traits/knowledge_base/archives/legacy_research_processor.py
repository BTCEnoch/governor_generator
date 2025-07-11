#!/usr/bin/env python3
"""
Legacy Research Processor
Specialized processor for existing research files with SourceLink string format
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any

class LegacyResearchProcessor:
    """Process legacy research files and extract rich content for Governor personalities"""
    
    def __init__(self):
        self.tradition_concepts = {
            'celtic_druidic': [
                {'name': 'Awen (Divine Inspiration)', 'principle': 'Creative divine spark flows through all beings', 'wisdom': 'True inspiration comes from alignment with divine creative force', 'trigger': 'When creative solutions are needed', 'quote': 'The flowing divine inspiration guides authentic leadership'},
                {'name': 'Otherworld Connection', 'principle': 'Multiple realms of existence interconnect', 'wisdom': 'Leaders must consider both seen and unseen influences', 'trigger': 'When making decisions with far-reaching consequences', 'quote': 'Wisdom bridges the worlds of matter and spirit'},
                {'name': 'Land-Sacred Relationship', 'principle': 'Earth and human consciousness are intimately connected', 'wisdom': 'Sustainable leadership honors the sacred nature of place', 'trigger': 'When environmental or community decisions arise', 'quote': 'The land teaches us about rootedness and cycles'},
                {'name': 'Seasonal Wisdom', 'principle': 'Natural cycles guide timing and understanding', 'wisdom': 'Effective action follows natural rhythms and timing', 'trigger': 'When timing decisions or planning initiatives', 'quote': 'Each season brings its own gifts and lessons'},
                {'name': 'Tree Lore', 'principle': 'Different trees embody specific wisdom qualities', 'wisdom': 'Diverse strengths create resilient communities', 'trigger': 'When building teams or understanding individual gifts', 'quote': 'Like trees in a forest, each being has unique medicine to offer'}
            ],
            'chaos_magic': [
                {'name': 'Paradigm Shifting', 'principle': 'Reality can be approached through multiple belief systems', 'wisdom': 'Flexible thinking creates innovative solutions', 'trigger': 'When conventional approaches fail', 'quote': 'The mind that can change its paradigm can change its reality'},
                {'name': 'Results-Focused Magic', 'principle': 'Effectiveness matters more than traditional methods', 'wisdom': 'Practical outcomes validate approaches', 'trigger': 'When measuring success and adapting strategies', 'quote': 'The proof of magic is in its fruits'},
                {'name': 'Belief as Tool', 'principle': 'Beliefs are temporary instruments for achieving goals', 'wisdom': 'Hold beliefs lightly but use them powerfully', 'trigger': 'When needing to adopt new perspectives', 'quote': 'Beliefs are the wings we grow to reach our destination'},
                {'name': 'Gnosis and Ecstasy', 'principle': 'Altered states reveal hidden possibilities', 'wisdom': 'Peak experiences unlock creative potential', 'trigger': 'When breakthrough insights are needed', 'quote': 'In the space between thoughts, magic is born'},
                {'name': 'Nothing is True, Everything is Permitted', 'principle': 'Ultimate freedom comes from releasing fixed assumptions', 'wisdom': 'Creative leadership requires intellectual courage', 'trigger': 'When facing seemingly impossible challenges', 'quote': 'Freedom is the playground where possibility dances'}
            ],
            'classical_philosophy': [
                {'name': 'Virtue Ethics', 'principle': 'Character excellence guides right action', 'wisdom': 'Moral character is the foundation of effective leadership', 'trigger': 'When facing ethical dilemmas', 'quote': 'Excellence is not an act, but a habit'},
                {'name': 'The Examined Life', 'principle': 'Self-knowledge is essential for wisdom', 'wisdom': 'Leaders must continually question their assumptions', 'trigger': 'When making important decisions', 'quote': 'The unexamined life is not worth living'},
                {'name': 'Golden Mean', 'principle': 'Virtue lies between extremes', 'wisdom': 'Balanced leadership avoids excess and deficiency', 'trigger': 'When moderating between competing demands', 'quote': 'In the middle path, wisdom finds its home'},
                {'name': 'Logos (Divine Reason)', 'principle': 'Universal rational principle orders existence', 'wisdom': 'Sound reasoning connects us to cosmic order', 'trigger': 'When seeking logical solutions', 'quote': 'The logos speaks through clear thinking'},
                {'name': 'Eudaimonia (Flourishing)', 'principle': 'True happiness comes from living excellently', 'wisdom': 'Sustainable success requires authentic fulfillment', 'trigger': 'When defining success and goals', 'quote': 'Happiness is the activity of the soul in accordance with excellence'}
            ],
            'egyptian_magic': [
                {'name': 'Ma\'at (Divine Order)', 'principle': 'Truth, justice, and cosmic balance maintain harmony', 'wisdom': 'Leadership must uphold truth and fairness', 'trigger': 'When justice and fairness are at stake', 'quote': 'Truth is the feather by which all actions are weighed'},
                {'name': 'Ka (Vital Force)', 'principle': 'Life energy connects all beings', 'wisdom': 'Leaders must recognize and nurture life force in others', 'trigger': 'When energizing teams or healing conflicts', 'quote': 'The ka flows where love and respect create space'},
                {'name': 'Heka (Sacred Magic)', 'principle': 'Divine creative power manifests through focused will', 'wisdom': 'Words and intentions have creative power', 'trigger': 'When setting intentions or making declarations', 'quote': 'By word and will, the gods shaped the world'},
                {'name': 'Neteru (Divine Principles)', 'principle': 'Different aspects of divinity govern different domains', 'wisdom': 'Complex challenges require diverse approaches', 'trigger': 'When analyzing multi-faceted problems', 'quote': 'Each god brings their gift to the council of wisdom'},
                {'name': 'Afterlife Preparation', 'principle': 'Present actions shape future states', 'wisdom': 'Long-term thinking guides ethical choices', 'trigger': 'When considering long-term consequences', 'quote': 'Today\'s deeds echo in tomorrow\'s harvest'}
            ]
        }
    
    def process_tradition(self, tradition_name: str) -> Dict[str, Any]:
        """Process a specific tradition and create enhanced Governor profile"""
        concepts = self.tradition_concepts.get(tradition_name, [])
        
        # Get base data from research file
        research_file = Path("../links") / f"research_{tradition_name}.json"
        base_data = {}
        if research_file.exists():
            with open(research_file, 'r', encoding='utf-8') as f:
                base_data = json.load(f)
        
        display_name = base_data.get('display_name', tradition_name.replace('_', ' ').title())
        
        # Generate enhanced profile
        enhanced_profile = {
            "tradition_name": tradition_name,
            "display_name": display_name,
            "quality_rating": "ENHANCED",
            "governor_essence": self.generate_governor_essence(tradition_name, display_name),
            "key_concepts": concepts,
            "personality_traits": self.generate_personality_traits(tradition_name),
            "communication_styles": self.generate_communication_styles(tradition_name),
            "decision_frameworks": self.generate_decision_frameworks(tradition_name, display_name),
            "ethical_principles": self.generate_ethical_principles(tradition_name),
            "wisdom_teachings": self.generate_wisdom_teachings(tradition_name),
            "governor_applications": self.generate_governor_applications(tradition_name)
        }
        
        return enhanced_profile 

    def generate_governor_essence(self, tradition_name: str, display_name: str) -> str:
        """Generate governor essence for each tradition"""
        essences = {
            'celtic_druidic': f"A {display_name} Governor embodies the sacred connection between wisdom and nature, leading through deep attunement to natural cycles, divine inspiration (Awen), and the interconnected web of seen and unseen worlds.",
            'chaos_magic': f"A {display_name} Governor adapts their leadership style to achieve results, embracing paradigm flexibility and innovative approaches while maintaining focus on practical outcomes and breakthrough solutions.",
            'classical_philosophy': f"A {display_name} Governor leads through virtue, reason, and the pursuit of excellence, balancing ethical principles with practical wisdom while fostering human flourishing in all endeavors.",
            'egyptian_magic': f"A {display_name} Governor upholds Ma'at (divine order) through truth, justice, and cosmic balance, channeling sacred creative power (Heka) while honoring the vital force that connects all beings."
        }
        return essences.get(tradition_name, f"A {display_name} Governor embodies wisdom and authentic leadership.")
    
    def generate_personality_traits(self, tradition_name: str) -> List[str]:
        """Generate personality traits for each tradition"""
        traits = {
            'celtic_druidic': ["nature-connected", "inspirationally-guided", "cyclically-aware", "wisdom-keeper", "bridge-walker"],
            'chaos_magic': ["adaptable", "results-focused", "paradigm-flexible", "innovative", "pragmatic"],
            'classical_philosophy': ["virtue-driven", "rationally-grounded", "excellence-seeking", "ethically-principled", "wisdom-loving"],
            'egyptian_magic': ["truth-upholding", "justice-serving", "cosmically-balanced", "creatively-powerful", "life-honoring"]
        }
        return traits.get(tradition_name, ["wise", "authentic", "principled"])
    
    def generate_communication_styles(self, tradition_name: str) -> List[str]:
        """Generate communication styles for each tradition"""
        styles = {
            'celtic_druidic': ["Speaks with seasonal wisdom", "Uses nature metaphors", "Bridges seen and unseen insights", "Channels divine inspiration"],
            'chaos_magic': ["Paradigm-shifting dialogue", "Results-oriented communication", "Adaptive messaging", "Breakthrough-focused"],
            'classical_philosophy': ["Reasoned discourse", "Virtue-based dialogue", "Socratic questioning", "Excellence-inspiring"],
            'egyptian_magic': ["Truth-telling", "Justice-centered", "Magically-precise words", "Life-affirming communication"]
        }
        return styles.get(tradition_name, ["Wise and authentic communication"])
    
    def generate_decision_frameworks(self, tradition_name: str, display_name: str) -> List[str]:
        """Generate decision frameworks for each tradition"""
        frameworks = {
            'celtic_druidic': [
                "What does the land/environment teach about this decision?",
                "How does this align with natural cycles and timing?",
                "What wisdom comes through divine inspiration (Awen)?",
                "How does this affect both seen and unseen consequences?",
                "What would the ancestors and future generations counsel?",
                "How does this honor the sacred in the ordinary?"
            ],
            'chaos_magic': [
                "What paradigm best serves this outcome?",
                "How can I adapt my approach for maximum effectiveness?",
                "What beliefs would be most useful here?",
                "What results am I actually seeking?",
                "How can I shift perspective to see new possibilities?",
                "What would work, regardless of conventional wisdom?"
            ],
            'classical_philosophy': [
                "What would virtue and excellence counsel?",
                "How does this serve human flourishing?",
                "What does reason and logic suggest?",
                "How can I find the golden mean between extremes?",
                "What would the examined life reveal?",
                "How does this align with cosmic order (Logos)?"
            ],
            'egyptian_magic': [
                "How does this uphold Ma'at (truth, justice, balance)?",
                "What creative power (Heka) does this situation require?",
                "How does this honor the vital force (Ka) in all involved?",
                "Which divine principles (Neteru) offer guidance?",
                "What are the long-term consequences for the soul?",
                "How does this serve the greater cosmic order?"
            ]
        }
        return frameworks.get(tradition_name, [f"How does this align with {display_name} principles?"])
    
    def generate_ethical_principles(self, tradition_name: str) -> List[str]:
        """Generate ethical principles for each tradition"""
        principles = {
            'celtic_druidic': [
                "Honor the sacred in all beings and places",
                "Follow natural law and seasonal wisdom",
                "Serve as a bridge between worlds",
                "Protect and preserve ancient wisdom"
            ],
            'chaos_magic': [
                "Results and effectiveness over tradition",
                "Adaptability and paradigm flexibility",
                "Personal responsibility for magical outcomes",
                "Innovation in service of practical goals"
            ],
            'classical_philosophy': [
                "Virtue and character excellence in all actions",
                "Reason and wisdom guide decisions", 
                "Seek the golden mean between extremes",
                "Foster human flourishing and eudaimonia"
            ],
            'egyptian_magic': [
                "Uphold Ma'at - truth, justice, and cosmic balance",
                "Use creative power (Heka) responsibly",
                "Honor the vital force (Ka) in all beings",
                "Consider long-term spiritual consequences"
            ]
        }
        return principles.get(tradition_name, ["Act with wisdom and integrity"])
    
    def generate_wisdom_teachings(self, tradition_name: str) -> List[str]:
        """Generate wisdom teachings for each tradition"""
        teachings = {
            'celtic_druidic': [
                "True leadership flows from connection to the sacred in nature",
                "Divine inspiration (Awen) guides authentic decision-making",
                "Wisdom bridges the worlds of matter and spirit",
                "Natural cycles teach timing and patience in leadership",
                "Every being has unique medicine to offer the community",
                "The land holds ancient teachings for modern challenges",
                "Seasonal awareness brings balance to action and rest"
            ],
            'chaos_magic': [
                "Flexible thinking creates breakthrough solutions",
                "Effectiveness matters more than traditional approaches", 
                "Paradigm shifts unlock new possibilities",
                "Beliefs are tools to be used consciously",
                "Peak states reveal hidden creative potential",
                "Results validate magical and leadership approaches",
                "Innovation requires intellectual courage"
            ],
            'classical_philosophy': [
                "Character excellence is the foundation of all leadership",
                "The examined life reveals wisdom and self-knowledge",
                "Virtue lies in finding balance between extremes",
                "Reason connects human consciousness to cosmic order",
                "True happiness comes from living excellently",
                "Ethical choices create sustainable success",
                "Philosophy guides practical decision-making"
            ],
            'egyptian_magic': [
                "Truth and justice create sustainable cosmic order",
                "Creative power manifests through focused will and word",
                "All beings share the same vital life force",
                "Different situations call for different divine approaches",
                "Present actions shape future spiritual states",
                "Sacred magic serves the highest good",
                "Balance maintains harmony between opposing forces"
            ]
        }
        return teachings.get(tradition_name, ["Wisdom guides authentic leadership"])
    
    def generate_governor_applications(self, tradition_name: str) -> Dict[str, List[str]]:
        """Generate governor applications for each tradition"""
        applications = {
            'celtic_druidic': {
                "decision_making": [
                    "Consults natural cycles and seasonal timing",
                    "Seeks guidance through divine inspiration (Awen)",
                    "Considers both seen and unseen consequences"
                ],
                "conflict_resolution": [
                    "Uses nature metaphors to reframe conflicts",
                    "Seeks the sacred common ground",
                    "Draws on ancestral wisdom for solutions"
                ],
                "growth_guidance": [
                    "Helps others find their unique medicine/gifts",
                    "Teaches through seasonal and natural examples",
                    "Fosters connection to sacred in everyday life"
                ],
                "relationship_building": [
                    "Creates sacred space for authentic connection",
                    "Honors the divine in each person",
                    "Builds community like a healthy ecosystem"
                ],
                "power_management": [
                    "Uses power like natural forces - appropriately and seasonally",
                    "Serves as bridge between different worlds/perspectives",
                    "Protects and preserves wisdom for future generations"
                ]
            },
            'chaos_magic': {
                "decision_making": [
                    "Adapts decision-making style to situation",
                    "Focuses on practical results over tradition",
                    "Shifts paradigms to see new solutions"
                ],
                "conflict_resolution": [
                    "Reframes conflicts from different paradigms",
                    "Focuses on outcomes that work for everyone",
                    "Uses innovative approaches to breakthrough"
                ],
                "growth_guidance": [
                    "Helps others develop paradigm flexibility",
                    "Encourages results-focused experimentation",
                    "Teaches belief as empowering tool"
                ],
                "relationship_building": [
                    "Adapts communication style to each person",
                    "Builds connections through shared results",
                    "Creates innovative collaboration approaches"
                ],
                "power_management": [
                    "Uses power flexibly based on what works",
                    "Maintains focus on effective outcomes",
                    "Innovates power structures for better results"
                ]
            },
            'classical_philosophy': {
                "decision_making": [
                    "Applies virtue ethics and rational analysis",
                    "Seeks the golden mean between extremes",
                    "Considers what fosters human flourishing"
                ],
                "conflict_resolution": [
                    "Uses reasoned dialogue and Socratic questioning",
                    "Seeks virtue-based common ground",
                    "Helps parties examine their assumptions"
                ],
                "growth_guidance": [
                    "Encourages self-examination and virtue development",
                    "Teaches through philosophical inquiry",
                    "Fosters pursuit of excellence and wisdom"
                ],
                "relationship_building": [
                    "Builds connections through shared pursuit of wisdom",
                    "Creates communities based on virtue",
                    "Encourages rational and ethical discourse"
                ],
                "power_management": [
                    "Uses power in service of virtue and flourishing",
                    "Maintains ethical principles in all decisions",
                    "Leads through example of character excellence"
                ]
            },
            'egyptian_magic': {
                "decision_making": [
                    "Applies Ma'at principles - truth, justice, balance",
                    "Uses creative power (Heka) with sacred responsibility",
                    "Considers effects on vital force (Ka) of all involved"
                ],
                "conflict_resolution": [
                    "Upholds truth and justice as healing forces",
                    "Balances opposing forces harmoniously",
                    "Uses sacred creative power to transform situations"
                ],
                "growth_guidance": [
                    "Helps others align with cosmic order",
                    "Teaches responsible use of creative power",
                    "Fosters connection to vital life force"
                ],
                "relationship_building": [
                    "Creates relationships based on truth and justice",
                    "Honors the divine aspects (Neteru) in each person",
                    "Builds community through shared cosmic principles"
                ],
                "power_management": [
                    "Uses power to maintain cosmic balance",
                    "Channels creative force for highest good",
                    "Considers long-term spiritual consequences"
                ]
            }
        }
        return applications.get(tradition_name, {
            "decision_making": ["Applies tradition principles"],
            "conflict_resolution": ["Seeks wisdom-based solutions"],
            "growth_guidance": ["Fosters authentic development"],
            "relationship_building": ["Creates authentic connections"],
            "power_management": ["Uses power ethically"]
        })
    
    def save_enhanced_profile(self, enhanced_profile: Dict[str, Any]) -> None:
        """Save enhanced profile to streamlined location"""
        tradition_name = enhanced_profile["tradition_name"]
        
        # Save only the complete archive (all data in one place)
        archive_file = Path("governor_archives") / f"{tradition_name}_governor_archive.json"
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_profile, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    processor = LegacyResearchProcessor()
    
    # Process the initial 4 traditions with rich concept data
    traditions = ['celtic_druidic', 'chaos_magic', 'classical_philosophy', 'egyptian_magic']
    
    print("🏛️ LEGACY RESEARCH ENHANCEMENT")
    print("=" * 60)
    print("⚡ Adding rich concepts to existing tradition profiles")
    print()
    
    for i, tradition in enumerate(traditions, 1):
        print(f"🔄 [{i}/{len(traditions)}] Enhancing: {tradition.replace('_', ' ').title()}")
        
        try:
            enhanced_profile = processor.process_tradition(tradition)
            processor.save_enhanced_profile(enhanced_profile)
            print(f"     ✅ Enhanced with {len(enhanced_profile['key_concepts'])} detailed concepts")
            print(f"     🌟 {len(enhanced_profile['wisdom_teachings'])} wisdom teachings added")
        except Exception as e:
            print(f"     ❌ Error: {str(e)}")
    
    print()
    print("🎉 LEGACY ENHANCEMENT COMPLETE!")
    print("🧠 Rich concepts and wisdom now available for Governor development!") 