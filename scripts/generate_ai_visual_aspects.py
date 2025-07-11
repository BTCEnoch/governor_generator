"""
Script to generate AI-driven visual aspects for Enochian Governors using Anthropic API
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import os
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIVisualAspectsGenerator:
    """Generates visual aspects using AI for Enochian Governors"""
    
    def __init__(self):
        self.template_path = Path('core/governors/visual_aspects_ai/visual_aspects_template.json')
        self.output_dir = Path('core/governors/visual_aspects_ai/generated')
        self.knowledge_base_dir = Path('knowledge_base/archives/governor_archives')
        self.governor_indexes_dir = Path('data/governors/indexes')
        self.research_links_dir = Path('data/knowledge/links')
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Anthropic client
        self.client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

    def load_governor_knowledge(self, governor_id: str) -> Dict[str, Any]:
        """Load all relevant knowledge for a governor"""
        knowledge = {
            'archives': {},
            'trait_definitions': {},
            'research_links': {}
        }
        
        # Load governor archive
        archive_path = self.knowledge_base_dir / f"{governor_id.lower()}_archive.json"
        if archive_path.exists():
            with open(archive_path) as f:
                knowledge['archives'] = json.load(f)
                logger.info(f"Loaded governor archive for {governor_id}")
        
        # Load trait definitions
        for index_file in self.governor_indexes_dir.glob('*.json'):
            if index_file.stem != 'approaches':  # Skip approaches.json
                with open(index_file) as f:
                    knowledge['trait_definitions'][index_file.stem] = json.load(f)
                    logger.info(f"Loaded trait definitions from {index_file.name}")
        
        # Load research links
        research_file = self.research_links_dir / f"research_{governor_id.lower()}.json"
        if research_file.exists():
            with open(research_file) as f:
                knowledge['research_links'] = json.load(f)
                logger.info(f"Loaded research links for {governor_id}")
        
        return knowledge

    def create_knowledge_prompt(self, governor_id: str, profile: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """Create a detailed prompt incorporating all knowledge sources"""
        prompt = f"""You are tasked with generating visual aspects for the Enochian Governor {governor_id}.
Before deciding on the visual aspects, carefully analyze the following knowledge sources:

1. Governor's Core Knowledge:
{json.dumps(knowledge['archives'], indent=2)}

2. Trait and Correspondence Definitions:
{json.dumps(knowledge['trait_definitions'], indent=2)}

3. Research Connections:
{json.dumps(knowledge['research_links'], indent=2)}

4. Governor's Current Profile:
{json.dumps(profile, indent=2)}

Based on this comprehensive knowledge:
1. First analyze how the governor's traits and correspondences manifest according to our knowledge base
2. Consider how their role and essence interact with their elemental and aethyric nature
3. Study the symbolic and archetypal patterns from the research connections
4. Only then determine the visual aspects that would authentically represent this governor

You must respond with ONLY a valid JSON object following this exact template structure. Do not include any explanatory text or markdown formatting:

{json.dumps(self.load_template(), indent=2)}

Remember:
- Return ONLY the JSON object
- Ensure all values are appropriate for this specific governor based on the analyzed knowledge
- Maintain the exact structure of the template
- Use only valid JSON syntax
"""
        return prompt

    def load_governor_profile(self, governor_id: str) -> Optional[Dict[str, Any]]:
        """Load the governor's profile"""
        profile_path = Path(f'governor_dossier/{governor_id}.json')
        try:
            with open(profile_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load profile for {governor_id}: {e}")
            return None

    def load_template(self) -> Optional[Dict[str, Any]]:
        """Load the visual aspects template"""
        try:
            with open(self.template_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load template: {e}")
            return None

    def prepare_governor_context(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare context from governor profile"""
        return {
            "governor_id": profile.get("governor_id", ""),  # Some profiles use governor_id
            "element": profile.get("element", ""),
            "aethyr": profile.get("aethyr", ""),
            "angelic_role": profile.get("angelic_role", profile.get("role", "")),  # Try both keys
            "essence": profile.get("essence", ""),
            "knowledge_base": profile.get("knowledge_sources", profile.get("knowledge_base", [])),  # Try both keys
            "archetypal_correspondences": profile.get("correspondences", profile.get("archetypal_correspondences", {})),  # Try both keys
            "persona": profile.get("personality", profile.get("persona", {}))  # Try both keys
        }

    async def generate_visual_aspects(self, governor_id: str) -> Optional[Dict[str, Any]]:
        """Generate visual aspects for a single governor"""
        try:
            # Load profile and knowledge
            profile = self.load_governor_profile(governor_id)
            if not profile:
                logger.error(f"Failed to load profile for {governor_id}")
                return None
                
            knowledge = self.load_governor_knowledge(governor_id)
            template = self.load_template()
            if not template:
                logger.error("Failed to load template")
                return None
            
            # Create comprehensive prompt with knowledge
            prompt = self.create_knowledge_prompt(governor_id, profile, knowledge)
            
            # Generate visual aspects using Anthropic API
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse the response
            try:
                # Get the response content from the first text block
                for content in message.content:
                    if content.type == "text":
                        response_content = content.text
                        visual_aspects = json.loads(response_content)
                        break
                else:
                    logger.error(f"No text content found in response for {governor_id}")
                    return None
                
                # Create full response with metadata
                full_response = {
                    "governor_id": governor_id,
                    "generation_time": datetime.now().isoformat(),
                    "template_version": "1.0",
                    "context": self.prepare_governor_context(profile),
                    "visual_aspects": visual_aspects
                }
                
                # Save detailed version
                detailed_path = self.output_dir / f"{governor_id}_visual_aspects.json"
                with open(detailed_path, 'w') as f:
                    json.dump(full_response, f, indent=2)
                
                # Save compact version
                compact_path = self.output_dir / f"{governor_id}_visual_compact.json"
                with open(compact_path, 'w') as f:
                    json.dump(visual_aspects, f, indent=2)
                
                logger.info(f"Successfully generated visual aspects for {governor_id}")
                return full_response
                
            except (json.JSONDecodeError, AttributeError) as e:
                logger.error(f"Failed to parse AI response for {governor_id}: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to generate visual aspects for {governor_id}: {e}")
            return None

async def main():
    generator = AIVisualAspectsGenerator()
    await generator.generate_visual_aspects("OCCODON")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 