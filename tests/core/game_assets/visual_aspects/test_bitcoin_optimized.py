"""
Tests for Bitcoin L1 optimized visual traits system.
"""

import pytest
from core.game_assets.visual_aspects.bitcoin_optimized import (
    FormType, ColorScheme, GeometryPattern, EnvironmentalEffectType,
    EffectRadius, EffectIntensity, EnvironmentalEffect,
    generate_visual_traits, expand_visual_traits, verify_traits,
    TRAITS_SIZE, HEADER_VERSION
)

def test_traits_generation():
    """Test basic traits generation"""
    # Test with known governor
    traits = generate_visual_traits("ABRIOND", 3, "Fire")
    
    assert len(traits) == TRAITS_SIZE
    assert traits[0:4] == HEADER_VERSION
    
    # Verify form type is valid
    assert 0 <= traits[4] <= 7
    
    # Verify color scheme is valid
    assert 0 <= traits[5] <= 7
    
    # Verify geometry patterns are valid
    assert traits[6] & 0xFF == traits[6]  # 8 bits only
    
    # Verify environmental effects
    effect = EnvironmentalEffect.from_byte(traits[7])
    assert isinstance(effect.effect_type, EnvironmentalEffectType)
    assert isinstance(effect.radius, EffectRadius)
    assert isinstance(effect.intensity, EffectIntensity)

def test_traits_deterministic():
    """Test that generation is deterministic"""
    traits1 = generate_visual_traits("ABRIOND", 3, "Fire")
    traits2 = generate_visual_traits("ABRIOND", 3, "Fire")
    
    assert traits1 == traits2
    
    # Different inputs should give different results
    traits3 = generate_visual_traits("ABRIOND", 4, "Fire")
    traits4 = generate_visual_traits("ABRIOND", 3, "Water")
    traits5 = generate_visual_traits("VIROOLI", 3, "Fire")
    
    assert traits1 != traits3  # Different aethyr
    assert traits1 != traits4  # Different element
    assert traits1 != traits5  # Different name

def test_environmental_effect_packing():
    """Test environmental effect packing/unpacking"""
    effect = EnvironmentalEffect(
        effect_type=EnvironmentalEffectType.ELEMENTAL,
        radius=EffectRadius.ROOM,
        intensity=EffectIntensity.HIGH
    )
    
    # Pack to byte
    byte = effect.to_byte()
    
    # Unpack from byte
    unpacked = EnvironmentalEffect.from_byte(byte)
    
    assert unpacked.effect_type == effect.effect_type
    assert unpacked.radius == effect.radius
    assert unpacked.intensity == effect.intensity

def test_geometry_patterns():
    """Test geometry pattern generation"""
    # Test highest aethyr (1-3)
    traits = generate_visual_traits("ABRIOND", 3, "Fire")
    patterns = traits[6]
    assert patterns & GeometryPattern.MERKABA.value  # Should have Merkaba
    assert patterns & GeometryPattern.METATRON.value  # Should have Metatron
    
    # Test mid aethyr (4-7)
    traits = generate_visual_traits("ABRIOND", 5, "Fire")
    patterns = traits[6]
    assert patterns & GeometryPattern.FLOWER_OF_LIFE.value  # Should have Flower of Life
    assert patterns & GeometryPattern.TORUS.value  # Should have Torus
    
    # Test lower aethyr (8-12)
    traits = generate_visual_traits("ABRIOND", 10, "Fire")
    patterns = traits[6]
    assert patterns & GeometryPattern.SPIRAL.value  # Should have Spiral
    assert patterns & GeometryPattern.FRACTAL.value  # Should have Fractal

def test_element_color_mapping():
    """Test element to color scheme mapping"""
    # Test Fire element
    traits = generate_visual_traits("ABRIOND", 3, "Fire")
    assert traits[5] == ColorScheme.GOLDEN
    
    # Test Water element
    traits = generate_visual_traits("ABRIOND", 3, "Water")
    assert traits[5] == ColorScheme.AZURE
    
    # Test Air element
    traits = generate_visual_traits("ABRIOND", 3, "Air")
    assert traits[5] == ColorScheme.SILVER
    
    # Test Earth element
    traits = generate_visual_traits("ABRIOND", 3, "Earth")
    assert traits[5] == ColorScheme.EMERALD
    
    # Test Spirit element
    traits = generate_visual_traits("ABRIOND", 3, "Spirit")
    assert traits[5] == ColorScheme.PLASMA

def test_traits_expansion():
    """Test expanding binary traits to full description"""
    traits = generate_visual_traits("ABRIOND", 3, "Fire")
    expanded = expand_visual_traits(traits)
    
    assert 'form' in expanded
    assert 'color' in expanded
    assert 'geometry' in expanded
    assert 'environment' in expanded
    assert 'time_variations' in expanded
    assert 'energy_signature' in expanded
    assert 'symbol_set' in expanded
    assert 'light_shadow' in expanded
    assert 'special_properties' in expanded
    
    # Verify form expansion
    assert expanded['form']['name'] in [f.name for f in FormType]
    assert 'description' in expanded['form']
    assert 'interactions' in expanded['form']
    
    # Verify geometry expansion
    assert isinstance(expanded['geometry']['patterns'], list)
    assert isinstance(expanded['geometry']['complexity'], int)
    assert 0 <= expanded['geometry']['complexity'] <= 8
    
    # Verify environment expansion
    assert 'effect_type' in expanded['environment']
    assert 'radius' in expanded['environment']
    assert 'intensity' in expanded['environment']

def test_traits_verification():
    """Test traits verification"""
    traits = generate_visual_traits("ABRIOND", 3, "Fire")
    
    # Should verify against same inputs
    assert verify_traits(traits, "ABRIOND", 3, "Fire")
    
    # Should fail verification with different inputs
    assert not verify_traits(traits, "ABRIOND", 4, "Fire")
    assert not verify_traits(traits, "ABRIOND", 3, "Water")
    assert not verify_traits(traits, "VIROOLI", 3, "Fire")

def test_invalid_traits():
    """Test handling of invalid traits data"""
    # Test invalid size
    with pytest.raises(ValueError):
        expand_visual_traits(b'too short')
        
    # Test invalid version
    invalid_version = bytearray(TRAITS_SIZE)
    invalid_version[0:4] = b'BAD1'
    with pytest.raises(ValueError):
        expand_visual_traits(bytes(invalid_version))

def test_special_properties():
    """Test special properties generation"""
    traits = generate_visual_traits("ABRIOND", 3, "Fire")
    expanded = expand_visual_traits(traits)
    
    # Should have 4 bytes of special properties
    assert len(expanded['special_properties']) == 4
    
    # Values should be deterministic
    traits2 = generate_visual_traits("ABRIOND", 3, "Fire")
    expanded2 = expand_visual_traits(traits2)
    assert expanded['special_properties'] == expanded2['special_properties'] 