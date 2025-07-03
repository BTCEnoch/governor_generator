#!/usr/bin/env python3
"""
Knowledge Retriever System
Connects governor knowledge_base_selections to extracted Wikipedia content.
Bridges the gap between governor traits and actual mystical knowledge.
"""

import json
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path

# LOGGING SETUP
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("KnowledgeRetriever")

class KnowledgeRetriever:
    """
    Retrieves specific knowledge content based on governor knowledge_base_selections.
    Maps abstract knowledge categories to actual extracted Wikipedia content.
    """
    
    def __init__(self, knowledge_content_path: str = "wiki_api_knowledge_content.json"):
        self.knowledge_content_path = knowledge_content_path
        self.knowledge_data = self._load_knowledge_content()
        
        # Mapping from governor knowledge_base_selections to tradition names
        self.knowledge_to_tradition_mapping = {
            # Core mystical systems
            'hermetic_tradition': ['golden_dawn', 'classical_philosophy'],
            'mystical_philosophy': ['classical_philosophy', 'gnostic_traditions'],
            'wisdom_traditions': ['taoism', 'sufi_mysticism'],
            'ancient_wisdom': ['egyptian_magic', 'classical_philosophy'],
            
            # Practical mystical arts
            'transformation_mysteries': ['thelema', 'gnostic_traditions'],
            'divination_systems': ['tarot_knowledge', 'i_ching'],
            'sacred_mathematics': ['sacred_geometry', 'i_ching'],
            'ritual_practices': ['golden_dawn', 'kuji_kiri'],
            
            # Specific traditions
            'egyptian_mysteries': ['egyptian_magic'],
            'golden_dawn_practices': ['golden_dawn'],
            'thelemic_philosophy': ['thelema'],
            'tarot_wisdom': ['tarot_knowledge'],
            'sacred_geometry': ['sacred_geometry'],
            'chaos_magick': ['chaos_magic'],
            'norse_wisdom': ['norse_traditions'],
            'sufi_path': ['sufi_mysticism'],
            'celtic_mysteries': ['celtic_druidic'],
            'eastern_philosophy': ['taoism', 'i_ching'],
            'mudra_practices': ['kuji_kiri'],
            
            # Philosophical approaches
            'compassion_teachings': ['sufi_mysticism', 'taoism'],
            'wisdom_keeper_role': ['celtic_druidic', 'classical_philosophy'],
            'spiritual_transformation': ['thelema', 'sufi_mysticism'],
            'balance_harmony': ['taoism', 'sacred_geometry'],
            'inner_alchemy': ['taoism', 'classical_philosophy'],
            'divine_union': ['gnostic_traditions', 'sufi_mysticism']
        }
    
    def _load_knowledge_content(self) -> Dict[str, Any]:
        """Load the extracted Wikipedia knowledge content."""
        try:
            with open(self.knowledge_content_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"❌ Knowledge content file not found: {self.knowledge_content_path}")
            return {}
        except Exception as e:
            logger.error(f"❌ Error loading knowledge content: {e}")
            return {}
    
    def get_tradition_content(self, tradition_name: str) -> Optional[Dict[str, Any]]:
        """Get all content for a specific tradition."""
        if not self.knowledge_data:
            return None
            
        traditions = self.knowledge_data.get('traditions', {})
        return traditions.get(tradition_name)
    
    def retrieve_knowledge_for_selections(self, knowledge_selections: List[str]) -> Dict[str, Any]:
        """
        Retrieve relevant knowledge content based on governor's knowledge_base_selections.
        
        Args:
            knowledge_selections: List of knowledge categories from governor
            
        Returns:
            Dict with retrieved content organized by tradition and selection
        """
        logger.info(f"🔍 Retrieving knowledge for selections: {knowledge_selections}")
        
        retrieved_content = {
            'selections_processed': knowledge_selections,
            'traditions_accessed': [],
            'content_by_tradition': {},
            'content_by_selection': {},
            'total_articles': 0,
            'total_word_count': 0
        }
        
        # Process each knowledge selection
        for selection in knowledge_selections:
            if selection in self.knowledge_to_tradition_mapping:
                tradition_names = self.knowledge_to_tradition_mapping[selection]
                
                retrieved_content['content_by_selection'][selection] = {
                    'mapped_traditions': tradition_names,
                    'articles': []
                }
                
                # Collect content from mapped traditions
                for tradition_name in tradition_names:
                    tradition_content = self.get_tradition_content(tradition_name)
                    
                    if tradition_content and tradition_content['extracted_articles']:
                        # Add to tradition tracking
                        if tradition_name not in retrieved_content['traditions_accessed']:
                            retrieved_content['traditions_accessed'].append(tradition_name)
                            retrieved_content['content_by_tradition'][tradition_name] = tradition_content
                        
                        # Add articles to this selection
                        for article in tradition_content['extracted_articles']:
                            retrieved_content['content_by_selection'][selection]['articles'].append({
                                'title': article['title'],
                                'tradition': tradition_name,
                                'summary': article['summary'],
                                'word_count': article['word_count'],
                                'url': article['url']
                            })
                            
                            retrieved_content['total_articles'] += 1
                            retrieved_content['total_word_count'] += article['word_count']
            else:
                logger.warning(f"⚠️ No tradition mapping found for knowledge selection: {selection}")
                retrieved_content['content_by_selection'][selection] = {
                    'mapped_traditions': [],
                    'articles': [],
                    'error': 'No tradition mapping found'
                }
        
        logger.info(f"📚 Retrieved {retrieved_content['total_articles']} articles from {len(retrieved_content['traditions_accessed'])} traditions")
        logger.info(f"📖 Total word count: {retrieved_content['total_word_count']:,}")
        
        return retrieved_content
    
    def get_governor_knowledge_summary(self, knowledge_selections: List[str]) -> Dict[str, Any]:
        """
        Get a concise summary of knowledge for a governor.
        Useful for forming personality and storyline generation.
        """
        retrieved = self.retrieve_knowledge_for_selections(knowledge_selections)
        
        # Create summary
        summary = {
            'knowledge_selections': knowledge_selections,
            'traditions_count': len(retrieved['traditions_accessed']),
            'total_articles': retrieved['total_articles'],
            'total_words': retrieved['total_word_count'],
            'key_concepts': [],
            'wisdom_themes': []
        }
        
        # Extract key concepts from article titles
        for selection, data in retrieved['content_by_selection'].items():
            concepts = [article['title'] for article in data.get('articles', [])]
            summary['key_concepts'].extend(concepts[:3])  # Top 3 per selection
        
        # Extract wisdom themes from traditions accessed
        tradition_themes = {
            'golden_dawn': 'Ceremonial Magic and Initiation',
            'thelema': 'True Will and Individual Path',
            'egyptian_magic': 'Ancient Mysteries and Divine Power',
            'taoism': 'Natural Harmony and Wu Wei',
            'i_ching': 'Change Patterns and Divination',
            'kuji_kiri': 'Sacred Gestures and Focus',
            'classical_philosophy': 'Wisdom and Contemplation',
            'gnostic_traditions': 'Hidden Knowledge and Gnosis',
            'tarot_knowledge': 'Symbolic Divination and Insight',
            'sacred_geometry': 'Divine Proportions and Order',
            'chaos_magic': 'Paradigm Flexibility and Results',
            'norse_traditions': 'Honor and Ancestral Wisdom',
            'sufi_mysticism': 'Divine Love and Surrender',
            'celtic_druidic': 'Nature Wisdom and Otherworld'
        }
        
        for tradition in retrieved['traditions_accessed']:
            if tradition in tradition_themes:
                summary['wisdom_themes'].append(tradition_themes[tradition])
        
        return summary
    
    def save_retrieval_results(self, knowledge_selections: List[str], governor_name: str = "test") -> str:
        """Save retrieval results to file for inspection."""
        retrieved = self.retrieve_knowledge_for_selections(knowledge_selections)
        
        output_file = f"retrieval_results_{governor_name}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(retrieved, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Retrieval results saved to {output_file}")
        return output_file

def test_knowledge_retriever():
    """Test the knowledge retriever with sample governor selections."""
    logger.info("🧪 Testing Knowledge Retriever System")
    
    retriever = KnowledgeRetriever()
    
    # Test with sample knowledge selections (like from Occodon governor)
    test_selections = [
        'hermetic_tradition',
        'mystical_philosophy', 
        'wisdom_traditions',
        'transformation_mysteries',
        'ancient_wisdom',
        'compassion_teachings'
    ]
    
    logger.info(f"🎯 Testing with selections: {test_selections}")
    
    # Test retrieval
    results = retriever.retrieve_knowledge_for_selections(test_selections)
    
    # Test summary
    summary = retriever.get_governor_knowledge_summary(test_selections)
    
    # Save results
    output_file = retriever.save_retrieval_results(test_selections, "occodon_test")
    
    # Print summary
    logger.info("📊 RETRIEVAL TEST SUMMARY:")
    logger.info(f"   Selections processed: {len(test_selections)}")
    logger.info(f"   Traditions accessed: {summary['traditions_count']}")
    logger.info(f"   Articles retrieved: {summary['total_articles']}")
    logger.info(f"   Total words: {summary['total_words']:,}")
    logger.info(f"   Key concepts: {summary['key_concepts'][:5]}")
    logger.info(f"   Wisdom themes: {summary['wisdom_themes'][:3]}")
    
    return results, summary

if __name__ == "__main__":
    test_knowledge_retriever() 