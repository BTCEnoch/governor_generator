import sys
import os
# , '../..'))  # Removed during reorganization

from engines.mystical_systems.tarot_system.tarot_system import TarotSystem

print("Testing tarot system...")
tarot = TarotSystem()
test_governor = {"name": "ABRIOND"}
profile = tarot.generate_profile(test_governor)
is_valid = tarot.validate_profile(profile)
print(f"Profile valid: {is_valid}")
print("Test complete!")

