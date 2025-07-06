"""
Visual Aspects Interview System

This module defines the structured interview questions and response options for gathering
governor visual aspects. Each governor must be asked the same questions in the same order,
and must consider all options before making choices based on their traits and attributes.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

# Response Option Enums
class FormType(Enum):
    ETHEREAL = "Pure energy/light forms"
    GEOMETRIC = "Sacred geometry based"
    ABSTRACT = "Non-euclidean/conceptual"
    COMPOSITE = "Multiple forms combined"
    METAMORPHIC = "Shape-shifting/fluid"
    SYMBOLIC = "Manifests as pure symbols"
    ELEMENTAL = "Pure elemental form"
    HUMANOID = "Angelic humanoid form"
    CELESTIAL = "Cosmic/stellar form"
    OTHER = "Unique manifestation"

class ColorScheme(Enum):
    PRISMATIC = "Full spectrum of shifting colors"
    MONOCHROMATIC = "Single color with variations"
    ELEMENTAL = "Colors of their element"
    CELESTIAL = "Cosmic/starlight colors"
    METALLIC = "Metallic/reflective colors"
    CRYSTALLINE = "Crystal/transparent colors"
    SHADOW = "Shadow/void colors"
    LIGHT = "Pure light colors"
    AETHYRIC = "Colors of their Aethyr"
    SYMBOLIC = "Colors tied to their role"

@dataclass
class InterviewQuestion:
    """Structure for a single interview question"""
    id: str
    question: str
    context: str
    options: List[str]
    requires_explanation: bool = True

class VisualAspectsInterview:
    """Defines the structured interview for gathering governor visual aspects"""
    
    def __init__(self):
        self.questions = self._initialize_questions()
        
    def _initialize_questions(self) -> List[InterviewQuestion]:
        """Initialize the full set of interview questions"""
        return [
            InterviewQuestion(
                id="primary_form",
                question="What is your primary form of manifestation?",
                context="""
                Consider your element, aethyr, and role. Review all options before choosing:
                - ETHEREAL: Pure energy/light forms
                - GEOMETRIC: Sacred geometry based
                - ABSTRACT: Non-euclidean/conceptual
                - COMPOSITE: Multiple forms combined
                - METAMORPHIC: Shape-shifting/fluid
                - SYMBOLIC: Manifests as pure symbols
                - ELEMENTAL: Pure elemental form
                - HUMANOID: Angelic humanoid form
                - CELESTIAL: Cosmic/stellar form
                - OTHER: Unique manifestation
                
                Your choice should reflect your essence and angelic role.
                """,
                options=[form.name for form in FormType],
            ),
            InterviewQuestion(
                id="color_scheme",
                question="What colors dominate your manifestation?",
                context="""
                Consider your element, aethyr, and correspondences. Review all options:
                - PRISMATIC: Full spectrum of shifting colors
                - MONOCHROMATIC: Single color with variations
                - ELEMENTAL: Colors of your element
                - CELESTIAL: Cosmic/starlight colors
                - METALLIC: Metallic/reflective colors
                - CRYSTALLINE: Crystal/transparent colors
                - SHADOW: Shadow/void colors
                - LIGHT: Pure light colors
                - AETHYRIC: Colors of your Aethyr
                - SYMBOLIC: Colors tied to your role
                
                Your choice should align with your essence and nature.
                """,
                options=[color.name for color in ColorScheme],
            ),
            InterviewQuestion(
                id="sacred_geometry",
                question="What sacred geometric patterns are present in your form?",
                context="""
                Consider your sephirot and numerological correspondences. Options include:
                - Platonic solids (tetrahedron, cube, octahedron, etc.)
                - Tree of Life patterns
                - Metatron's Cube
                - Flower of Life
                - Spirals (Fibonacci, Golden)
                - Your personal sigil geometry
                - Elemental symbols
                - Zodiacal geometry
                - Enochian letter forms
                - Custom sacred patterns
                
                Describe how these patterns manifest and interact.
                """,
                options=[],  # Free-form response with guidance
            ),
            InterviewQuestion(
                id="dimensional_presence",
                question="How does your form manifest across different dimensions?",
                context="""
                Consider your role and essence. Describe your presence in:
                - Physical dimension
                - Etheric plane
                - Astral realm
                - Mental plane
                - Spiritual dimensions
                - Time dimension
                - Your home Aethyr
                
                Explain how your form changes or remains constant.
                """,
                options=[],  # Free-form response with guidance
            ),
            InterviewQuestion(
                id="environmental_effects",
                question="What effects does your presence have on the surrounding environment?",
                context="""
                Consider your element and powers. Effects might include:
                - Changes in light/shadow
                - Temperature changes
                - Air/wind effects
                - Water/moisture effects
                - Earth/material effects
                - Time distortions
                - Reality fluctuations
                - Energy manifestations
                - Sound/vibration changes
                - Emotional/mental influences
                
                Describe the sphere of your influence.
                """,
                options=[],  # Free-form response with guidance
            ),
            InterviewQuestion(
                id="time_variations",
                question="How does your appearance change with different temporal conditions?",
                context="""
                Consider your zodiacal and planetary correspondences. Describe changes based on:
                - Astrological alignments
                - Planetary hours
                - Day/night cycle
                - Seasonal influences
                - Lunar phases
                - Solar cycles
                - Aethyric tides
                
                Explain the nature and reason for these changes.
                """,
                options=[],  # Free-form response with guidance
            ),
            InterviewQuestion(
                id="energy_signature",
                question="What is the unique signature of your energetic presence?",
                context="""
                Consider your element and essence. Describe your:
                - Energy frequency
                - Vibrational pattern
                - Aethyric resonance
                - Elemental harmonics
                - Light/shadow balance
                - Power manifestation
                - Spiritual radiation
                
                Explain how others would sense your presence.
                """,
                options=[],  # Free-form response with guidance
            ),
            InterviewQuestion(
                id="symbolic_aspects",
                question="What symbolic elements are consistently present in your manifestation?",
                context="""
                Consider your role and correspondences. Describe your:
                - Personal sigils
                - Elemental marks
                - Angelic seals
                - Sacred symbols
                - Enochian letters
                - Geometric emblems
                - Power signs
                - Divine names
                
                Explain how these symbols relate to your essence.
                """,
                options=[],  # Free-form response with guidance
            ),
            InterviewQuestion(
                id="scale_proportion",
                question="What is your scale and proportion relative to human perception?",
                context="""
                Consider your role and power. Describe:
                - Natural size range
                - Size variations
                - Proportional relationships
                - Dimensional scaling
                - Perceptual adjustments
                - Form ratios
                - Sacred proportions
                
                Explain how and why your scale changes.
                """,
                options=[],  # Free-form response with guidance
            ),
            InterviewQuestion(
                id="interaction_methods",
                question="How do you interact with physical and spiritual entities?",
                context="""
                Consider your approach and tone. Describe:
                - Physical interaction methods
                - Energy manipulation
                - Communication channels
                - Power transmission
                - Blessing/protection methods
                - Teaching techniques
                - Healing approaches
                
                Explain how these align with your role.
                """,
                options=[],  # Free-form response with guidance
            )
        ]

    def get_interview_prompt(self, governor_data: Dict) -> str:
        """
        Generate the complete interview prompt for a governor
        
        Args:
            governor_data: The governor's complete profile data
            
        Returns:
            A formatted prompt string for the interview
        """
        prompt = f"""
        VISUAL ASPECTS INTERVIEW FOR {governor_data['governor_name']}
        
        Before answering each question, carefully consider:
        - Your element: {governor_data['persona']['element']}
        - Your aethyr: {governor_data['persona']['aethyr']}
        - Your essence: {governor_data['persona']['essence']}
        - Your angelic role: {governor_data['persona']['angelic_role']}
        - Your knowledge domains: {', '.join(governor_data['persona']['knowledge_base'])}
        - Your correspondences: {governor_data['persona']['archetypal_correspondences']}
        - Your approach and tone: {governor_data['persona']['polar_traits']['baseline_approach']}, {governor_data['persona']['polar_traits']['baseline_tone']}
        
        Instructions:
        1. Read each question carefully
        2. Review ALL provided options before making choices
        3. Consider how your choices align with your traits and attributes
        4. Provide detailed explanations for your choices
        5. Maintain consistency with your established persona
        
        Questions follow below. Take time to consider each one fully.
        """
        
        for i, question in enumerate(self.questions, 1):
            prompt += f"\n\nQuestion {i}: {question.question}\n"
            prompt += f"Context: {question.context}\n"
            if question.options:
                prompt += f"Options: {', '.join(question.options)}\n"
            prompt += "Please provide your response and explanation:"
        
        return prompt

    def validate_response(self, question_id: str, response: str, governor_data: Dict) -> bool:
        """
        Validate that a response aligns with the governor's traits
        
        Args:
            question_id: The ID of the question being answered
            response: The governor's response
            governor_data: The governor's complete profile data
            
        Returns:
            True if the response is valid, False otherwise
        """
        # Implementation would validate response against governor traits
        # For now, return True as placeholder
        # TODO: Implement full validation logic
        return True 