import aiohttp
import json
from typing import Dict, Optional

class WikipediaIChing:
    """Handles fetching I Ching hexagram data from Wikipedia API."""
    
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.hexagram_cache: Dict[int, Dict] = {}

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_hexagram_data(self, hexagram_number: int) -> Optional[Dict]:
        """
        Fetch data for a specific I Ching hexagram from Wikipedia.
        
        Args:
            hexagram_number: Integer from 1-64 representing the hexagram number
            
        Returns:
            Dictionary containing the hexagram data or None if not found
        """
        if not self.session:
            raise RuntimeError("WikipediaIChing must be used as an async context manager")
            
        if hexagram_number in self.hexagram_cache:
            return self.hexagram_cache[hexagram_number]

        # Convert hexagram number to Unicode code point (0x4DC0 + hexagram_number - 1)
        unicode_point = 0x4DC0 + hexagram_number - 1
        
        params = {
            "action": "parse",
            "format": "json",
            "page": f"I Ching hexagram {hexagram_number}",
            "prop": "text|sections|displaytitle",
            "formatversion": "2"
        }

        try:
            async with self.session.get(self.BASE_URL, params=params) as response:
                data = await response.json()
                
                if "error" in data:
                    return None

                # Extract relevant sections from the Wikipedia article
                parsed_data = {
                    "number": hexagram_number,
                    "unicode_char": chr(unicode_point),
                    "title": data["parse"]["title"].replace("I Ching hexagram ", ""),
                    "sections": {},
                }

                # Parse the HTML content to extract sections
                for section in data["parse"]["sections"]:
                    section_title = section["line"].lower()
                    if section_title in ["interpretation", "the judgment", "the image", "the lines"]:
                        parsed_data["sections"][section_title] = section["index"]

                # Cache the result
                self.hexagram_cache[hexagram_number] = parsed_data
                return parsed_data

        except Exception as e:
            print(f"Error fetching hexagram {hexagram_number}: {str(e)}")
            return None

    async def get_all_hexagrams(self) -> Dict[int, Dict]:
        """
        Fetch data for all 64 I Ching hexagrams.
        
        Returns:
            Dictionary mapping hexagram numbers to their data
        """
        if not self.session:
            raise RuntimeError("WikipediaIChing must be used as an async context manager")
            
        results = {}
        for i in range(1, 65):
            result = await self.get_hexagram_data(i)
            if result:
                results[i] = result
        return results 