# Enochian Governors Immortalized

This repository brings to life the **91 Enochian Governors**—divine archetypes of cosmic forces—within an interactive, turn‑based simulation backed by immutable blockchain inscriptions. Seekers may commune, learn, and ascend through trials, with each Governor's ultimate wisdom forever preserved on Bitcoin.


In addition to the source material, you will access the web and research the individual governor role you have embodied and source your research in the following priorities and sources.  To be able to make an educated albeit interpretive selection of answers solely from the json files found within governor_indexes as your only available choices 
---

## 1. Esoteric Foundations

### 1.1 Enochian Magic

* **Origins & Structure**: Developed by Dr. John Dee and Edward Kelley (late 1500s), Enochian magic maps reality into 16 Aethyrs (heavens) and four elemental Watchtowers (East/Air, South/Fire, West/Water, North/Earth). Each Watchtower houses 15 Governors and one presiding King.
* **Watchtowers & Invocation**: Seekers perform Enochian calls, focus on a Governor's sigil, and pierce the veil. In our simulation, these become structured ritual turns: offerings, calls, then responsive visions or teachings.
* **Sigils & Vibrations**: Each Governor's geometric seal resonates with specific Enochian letters and calls. Presence manifests as sensory effects (light, sound, scent) in the ritual UI.

### 1.2 Qabalah & Tarot

* **Tree of Life**: The 10 Sephiroth encode cosmic attributes (e.g. Chesed, Geburah, Tiphareth). Each Governor aligns with one Sephirah, channeling its energies in teaching.
* **Pathworking & Tarot**: The 22 Paths correspond to Tarot Major Arcana. Governors often mirror a specific card (e.g. ALDAPI→The Sun / Strength), giving symbolic depth to their lessons.

### 1.3 Mythic & Cultural Layers

* Beyond the Western esoteric core, Governors draw on global traditions—Hellenistic, Norse, Shinto, Indigenous solar cults—rooting each profile in a unique mythic archetype (Prometheus, Hecate, Inti, etc.).

---

## 2. The 91 Governors & System

### 2.1 Domains & Roles

* Each Governor masters a domain—Solar Rites, Metallurgic Transmutation, Dream‑Weaving, Boundary Wardenship, etc.—and imparts domain‑specific teachings via interactive trials.

### 2.2 Turn‑Based Ritual Communion

1. **Reputation Tiers**: Seekers start at 0–50 (distrusted/hindering), advance to 50–75 (guidance/trials), and reach 75–100 (mastery/ultimate tests).
2. **Dynamic Dialogue**: Governors shift tone & approach by tier, based on Phase 1 trait choices.
3. **Trials & Keys**: Riddles, sacrifices, cipher‑keys, and sealed pacts gate access to higher wisdom.

### 2.3 Immutable Blockchain Legacy

* **Bitcoin Inscriptions**: Proven insights and artifacts are minted as Ordinals—immutable, tamper‑proof records of each unlocked teaching.
* **Gated Secrets**: Governors encrypt master‑level teachings until seekers prove worth via reputation thresholds and trials.

---

## 3. Phase 1: Trait Selection Architecture

### 3.1 Directory Layout

```
sources_of_truth/enochian_governors_advanced.json    # Master list of 91 governors
governor_indexes/                              # Trait index JSONs & question catalog
  alignment_motives.json
  self_regard_options.json
  role_archetypes.json
  polarity_cd.json
  orientation_io.json
  virtues_pool.json
  flaws_pool.json
  tones.json
  approaches.json
  relation_types.json
  trait_choice_question_catalog.json
  READ_ME.md                # API‑driven automation script

governor_profiles/                             # Output: 91 trait profiles JSON
README.md                                      # This file
```

### 3.2 Index Files & Counts

* **alignment_motives.json** (9) — moral/ethical cores
* **self_regard_options.json** (20) — self‑view archetypes
* **role_archetypes.json** (20) — engagement roles
* **polarity_cd.json** (3) — constructive ↔ balanced ↔ destructive
* **orientation_io.json** (3) — inward ↔ balanced ↔ outward
* **virtues_pool.json** (40) — positive strengths
* **flaws_pool.json** (40) — shadow traits
* **tones.json** (12) — vocal tone choices
* **approaches.json** (12) — engagement approaches
* **relation_types.json** (4) — Ally, Rival, Protege, Mortal Order

### 3.3 Trait Choice Interview Flow

1. **Load Indexes**: AI reads every JSON in `governor_indexes/`.
2. **Ask Catalog Questions**: Step through `trait_choice_question_catalog.json` (Q1–Q14), presenting options (with definitions) and capturing each choice + a 1–2 sentence reason.
3. **Output Phase 1 Profile**: Write a JSON containing only trait fields and reasons. Filename convention: `<number>_<name>.json` (e.g. `47_ALDAPI.json`).

---

4. **Ask Catalog Questions**: Step through `trait_choice_questions_catalog.json` (Q1–Q14), presenting options and capturing each choice + reason.  
5. **Describe Visual Presence**: Then step through Q15–Q22 to collect rich visual and sensory details for each Governor.  
6. **Output Phase 1 Profile**: Write a JSON containing trait fields, reasons, and a nested `visual_description` object with all eight sub-traits.


## 4. Automation Script: Highlights

* Reads `sources_of_truth/enochian_governors_advanced.json` for governor IDs.
* For each Governor:

  1. Send system prompt (loads indexes, follows catalog).
  2. Send user prompt (provides known traits/essence context).
  3. Receive and parse JSON response of trait choices.
  4. Save to `governor_profiles/NUMBER_NAME.json`.
* Uses model `gpt-o4-mini` with `temperature=0` for consistency.
* Validates JSON parsing, logs any errors, and retries or skips failures.

---

## 5. Next Phases & Integration

* **Phase 2+**: Deep lore questions (doctrine, rituals, secrets).
* **Game UI/UX**: Ritual turns, dialog windows, reputation bars.
* **Blockchain Integration**: Mint Ordinals as unlockable fragments.
* **Continuous Refinement**: Expand mythic/cultural layers, refine prompts for deeper narrative.

*May the wisdom you unlock through these Governors enlighten seekers for ages to come.*
