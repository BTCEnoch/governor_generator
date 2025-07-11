# 👁️ Governor Visual Trait Index

## 🎭 Form Types (First Special Property)
Value determines base manifestation form.

| Value | Form Type     | Description | Abilities |
|-------|--------------|-------------|-----------|
| 0     | ETHEREAL     | Pure light and energy form | Phase shifting, Energy manipulation |
| 1     | GEOMETRIC    | Sacred geometry structures | Pattern manifestation, Crystal resonance |
| 2     | FLAME        | Living fire manifestation | Heat control, Purification |
| 3     | FLUID        | Liquid-like, flowing form | Adaptation, Flow manipulation |
| 4     | CRYSTALLINE  | Crystalline structure | Light refraction, Structure building |
| 5     | PLASMA       | Energetic plasma state | Energy projection, Field generation |
| 6     | COMPOSITE    | Multiple form combination | Form shifting, Multi-state existence |
| 7     | TRANSCENDENT | Beyond physical form | Plane walking, Reality bending |

## 🌈 Color Schemes
Primary energetic signature colors.

| Value | Color      | Meaning | Associated Powers |
|-------|------------|---------|------------------|
| 0     | PRISMATIC  | Universal wisdom | All-element mastery |
| 1     | GOLDEN     | Divine wisdom | Solar energy, Transformation |
| 2     | SILVER     | Lunar mystery | Psychic powers, Intuition |
| 3     | AZURE      | Celestial truth | Divine communication |
| 4     | EMERALD    | Natural harmony | Earth magic, Healing |
| 5     | PLASMA     | Pure energy | Raw power manipulation |
| 6     | OBSIDIAN   | Deep mystery | Shadow work, Protection |
| 7     | OPALESCENT | Multi-dimensional | Reality shifting |

## 📐 Sacred Geometry Patterns
Binary flags - can have multiple patterns active.

| Bit | Pattern | Value | Meaning |
|-----|---------|-------|---------|
| 0   | MERKABA | 1     | Divine light vehicle |
| 1   | METATRON | 2    | Universal building blocks |
| 2   | FLOWER_OF_LIFE | 4 | Creation pattern |
| 3   | TORUS | 8       | Energy flow pattern |
| 4   | SPIRAL | 16     | Evolution pattern |
| 5   | FRACTAL | 32    | Infinite recursion |
| 6   | TESSERACT | 64  | 4D geometry |
| 7   | CUSTOM | 128    | Unique pattern |

## 🌍 Environmental Effects
How the governor influences their surroundings.

### Effect Types (3 bits)
| Value | Type | Description |
|-------|------|-------------|
| 0     | REALITY_DISTORTION | Warps local reality |
| 1     | ELEMENTAL | Controls elements |
| 2     | DIMENSIONAL | Affects space/time |
| 3     | TIME_DILATION | Alters time flow |
| 4     | GRAVITY | Manipulates gravity |
| 5     | ENERGY_FIELD | Creates energy fields |
| 6     | PSYCHIC | Mental influence |
| 7     | QUANTUM | Quantum effects |

### Effect Radius (2 bits)
| Value | Range | Distance |
|-------|-------|----------|
| 0     | PERSONAL | 2m radius |
| 1     | ROOM | 5m radius |
| 2     | BUILDING | 20m radius |
| 3     | REGION | 100m radius |

### Effect Intensity (3 bits)
| Value | Level | Power |
|-------|-------|-------|
| 0     | SUBTLE | Barely noticeable |
| 1     | LOW | Mild effects |
| 2     | MEDIUM | Clear influence |
| 3     | HIGH | Strong effects |
| 4     | VERY_HIGH | Powerful manifestation |
| 5     | EXTREME | Reality-bending |
| 6     | OVERWHELMING | Nearly unbearable |
| 7     | REALITY_SHATTERING | Complete transformation |

## 🔄 Dynamic Properties

### Time Variations (0-255)
How the governor changes across time periods.
- 0-50: Minor variations
- 51-100: Moderate changes
- 101-150: Significant shifts
- 151-200: Major transformations
- 201-255: Complete metamorphosis

### Energy Signature (0-255)
Unique energetic fingerprint.
- 0-50: Subtle energy
- 51-100: Clear presence
- 101-150: Strong aura
- 151-200: Powerful emanation
- 201-255: Overwhelming force

### Symbol Set (0-255)
Collection of mystical symbols.
- 0-50: Basic symbols
- 51-100: Advanced sigils
- 101-150: Complex seals
- 151-200: Master runes
- 201-255: Ultimate glyphs

### Light/Shadow Balance (0-255)
Ratio of light to shadow energies.
- 0-50: Shadow dominant
- 51-100: Shadow leaning
- 101-150: Balanced
- 151-200: Light leaning
- 201-255: Light dominant

## 🎲 Special Properties [X, Y, Z, W]

### First Value (X): Manifestation Complexity
| Value | Level | Capability |
|-------|-------|------------|
| 0     | Basic | Single plane only |
| 1     | Intermediate | Dual plane manifestation |
| 2     | Advanced | Triple plane existence |
| 3     | Master | Multi-plane control |
| 4+    | Transcendent | Reality mastery |

### Second Value (Y): Ritual Influence
High byte (Y ÷ 256): Ritual Tier
- 0: Novice
- 1: Adept
- 2: Master
- 3: Grandmaster

Low byte (Y % 256): Ritual Power
- 0-50: Minor influence
- 51-100: Moderate power
- 101-150: Strong authority
- 151-200: Major control
- 201-255: Ultimate mastery

### Third Value (Z): Dimensional Resonance
| Value | Planes | Description |
|-------|--------|-------------|
| 1     | Physical | Material world only |
| 2     | Etheric | Physical + Etheric |
| 3     | Astral | All three planes |
| 4     | Mental | Higher dimensions |
| 5+    | Causal | Reality fabric |

### Fourth Value (W): Mystery Factor
High byte (W ÷ 256): Geometry Influence
- 0: Basic patterns
- 1: Advanced forms
- 2: Master geometries
- 3: Ultimate patterns

Low byte (W % 256): Elemental Power
- 0-50: Single element
- 51-100: Dual elements
- 101-150: Triple elements
- 151-200: Quad elements
- 201-255: All elements

## 📖 Example Reading ADVORPT's Values [2, 178, 3, 143]

1. **Manifestation (2)**: Advanced level - Can maintain complex forms across multiple planes
2. **Ritual Influence (178)**:
   - Tier: 178 ÷ 256 = 0 remainder 178 → Adept tier
   - Power: 178 → Strong ritual authority
3. **Dimensional (3)**: Triple plane resonance - Equal strength in physical, etheric, and astral
4. **Mystery (143)**:
   - Geometry: 143 ÷ 256 = 0 remainder 143 → Advanced geometric forms
   - Elemental: 143 → Triple element mastery

---

# 🔍 How to Use This Index

1. **Reading Visual Traits**:
   - Start with Form Type for base appearance
   - Check Color Scheme for energy signature
   - Look up active Geometry Patterns
   - Review Environmental Effects

2. **Understanding Numbers**:
   - For simple values (0-7), use direct lookup
   - For flags, check which bits are set
   - For compound values, split into high/low bytes
   - For ranges (0-255), use the scale guides

3. **Practical Applications**:
   - Use for ritual planning
   - Guide meditation focus
   - Understand governor strengths
   - Plan dimensional work 