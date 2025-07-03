#!/usr/bin/env python3
"""
Curated High-Quality Sources for Wisdom Traditions
Hand-picked, working URLs with comprehensive content
"""

# Curated sources organized by tradition
CURATED_SOURCES = {
    "enochian_magic": {
        "sacred_texts": [
            {
                "url": "https://sacred-texts.com/eso/dee/",
                "title": "The Calls of Enoch - Enochian Keys",
                "description": "Full text of the 48 Enochian Keys with original language and English translation",
                "content_type": "primary_texts",
                "estimated_quality": "very_high"
            },
            {
                "url": "https://sacred-texts.com/eso/enoch/index.htm",
                "title": "Enochian Dictionary",
                "description": "Glossary of Enochian terms giving meanings of angelic words",
                "content_type": "reference",
                "estimated_quality": "high"
            }
        ],
        "hermetic_library": [
            {
                "url": "https://hermetic.com/dee/",
                "title": "Enochian Magick Reference", 
                "description": "Comprehensive overview of John Dee and Edward Kelley's angelic communication system",
                "content_type": "comprehensive_guide",
                "estimated_quality": "very_high"
            }
        ],
        "archive_org": [
            {
                "url": "https://archive.org/details/truefaithfulrel00deejgoog",
                "title": "A True and Faithful Relation",
                "description": "Scanned original diary records of John Dee's Enochian workings",
                "content_type": "primary_source",
                "estimated_quality": "very_high"
            }
        ]
    },
    
    "hermetic_tradition": {
        "sacred_texts": [
            {
                "url": "https://sacred-texts.com/chr/herm/",
                "title": "Corpus Hermeticum",
                "description": "Core Hermetic dialogues attributed to Hermes Trismegistus",
                "content_type": "primary_texts",
                "estimated_quality": "very_high"
            },
            {
                "url": "https://sacred-texts.com/alc/emerald.htm",
                "title": "The Emerald Tablet of Hermes",
                "description": "Seminal Hermetic/alchemical text with commentary",
                "content_type": "primary_text",
                "estimated_quality": "very_high"
            },
            {
                "url": "https://sacred-texts.com/eso/kyb/",
                "title": "The Kybalion",
                "description": "Seven Hermetic Principles in accessible form",
                "content_type": "systematic_guide",
                "estimated_quality": "high"
            }
        ],
        "archive_org": [
            {
                "url": "https://archive.org/details/threebbooksofoccultphilosophy",
                "title": "Three Books of Occult Philosophy",
                "description": "Complete Renaissance Hermetic magic compendium by Agrippa",
                "content_type": "comprehensive_system",
                "estimated_quality": "very_high"
            }
        ]
    },
    
    "kabbalah": {
        "sacred_texts": [
            {
                "url": "https://sacred-texts.com/jud/yetzirah.htm",
                "title": "Sefer Yetzirah (Book of Creation)",
                "description": "Foundational Kabbalistic text introducing Ten Sefirot and 22 Hebrew letters",
                "content_type": "primary_text",
                "estimated_quality": "very_high"
            },
            {
                "url": "https://sacred-texts.com/jud/cab/",
                "title": "The Kabbalah Unveiled (Mathers)",
                "description": "Translation of key Zohar sections with extensive commentary",
                "content_type": "primary_texts_with_commentary",
                "estimated_quality": "very_high"
            }
        ],
        "sefaria": [
            {
                "url": "https://www.sefaria.org/Zohar",
                "title": "Zohar",
                "description": "Monumental mystical commentary on the Torah, central to Kabbalah",
                "content_type": "primary_texts",
                "estimated_quality": "very_high"
            }
        ]
    }
}

# Wikipedia quick reference mappings
WIKIPEDIA_MAPPINGS = {
    "enochian_magic": {
        "Enochian magic": "https://en.wikipedia.org/wiki/Enochian_magic",
        "Enochian keys": "https://en.wikipedia.org/wiki/Enochian_keys", 
        "Great Table": "https://en.wikipedia.org/wiki/Enochian_table",
        "Aethyrs": "https://en.wikipedia.org/wiki/Aethyrs",
        "Watchtowers": "https://en.wikipedia.org/wiki/Watchtower_(magic)"
    },
    "hermetic_tradition": {
        "Correspondence principle": "https://en.wikipedia.org/wiki/Principle_of_correspondence",
        "Hermeticism": "https://en.wikipedia.org/wiki/Hermeticism",
        "Emerald Tablet": "https://en.wikipedia.org/wiki/Emerald_Tablet",
        "Alchemy": "https://en.wikipedia.org/wiki/Alchemy",
        "Seven Hermetic principles": "https://en.wikipedia.org/wiki/The_Kybalion"
    },
    "kabbalah": {
        "Kabbalah": "https://en.wikipedia.org/wiki/Kabbalah",
        "Tree of Life": "https://en.wikipedia.org/wiki/Tree_of_Life_(Kabbalah)",
        "Sefirot": "https://en.wikipedia.org/wiki/Sefirot",
        "Ein Sof": "https://en.wikipedia.org/wiki/Ein_Sof",
        "Gematria": "https://en.wikipedia.org/wiki/Gematria",
        "Tetragrammaton": "https://en.wikipedia.org/wiki/Tetragrammaton"
    }
}

def get_curated_sources_for_tradition(tradition: str) -> dict:
    """Get curated sources for a specific tradition"""
    return CURATED_SOURCES.get(tradition, {})

def get_wikipedia_links_for_tradition(tradition: str) -> dict:
    """Get Wikipedia quick reference links for a tradition"""
    return WIKIPEDIA_MAPPINGS.get(tradition, {}) 