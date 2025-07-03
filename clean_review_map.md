# Governor Generation Project - Clean Structure Map
**Generated on:** 2025-07-02 18:48:47
**Focus:** Core codebase and documentation (excluding large assets)

## 📊 Core Project Overview

| Metric | Value |
|--------|-------|
| **Core Files** | 241 |
| **Core Directories** | 52 |
| **Core Size** | 4.0 MB |
| **Project Root** | `D:\Enochian Cyphers\Governor Generation\governor_generator` |

## 📁 Core File Type Distribution

| File Type | Count |
|-----------|-------|
| Configuration | 90 |
| Documentation | 42 |
| JavaScript | 1 |
| Other | 5 |
| Python | 103 |

## 🚫 Excluded from This Map

The following directories are excluded to focus on core development files:
- `Aekashics/` - Large game asset library (2.7 GB excluded)
- `__pycache__/` - Python cache files
- `governor_output/` - Generated output files
- `storyline_output_v*/` - Generated storyline files
- `.git/`, `.vscode/`, etc. - Development environment files


## 🌳 Core Directory Structure

```
- canon/
  - 91_governors_canon.json (34.5 KB) (730 lines)
  - BITCOIN_ONCHAIN_RESOURCES.md (12.9 KB) (241 lines)
  - canon_governor_profiles.json (173.0 KB) (6476 lines)
  - canon_sources.md (58.7 KB) (678 lines)
  - canon_sources_index.json (20.1 KB) (367 lines)
  - questions_catalog.json (16.2 KB) (292 lines)
  - expansions/
    - advanced-considerations.md (10.6 KB) (328 lines)
    - prebaked_expansion_pack_instructions.md (55.5 KB) (337 lines)
    - voidmaker/
      - voidmaker_concepts.md (22.6 KB) (184 lines)
      - voidmaker_expansion.md (11.9 KB) (304 lines)
      - voidmaker_questions.md (6.0 KB) (111 lines)
- cli/
  - mystical_cli.py (2.8 KB) (79 lines)
- concept_docs/
  - LIGHTHOUSE_SUMMARY.md (4.4 KB) (104 lines)
  - context_aware.md (12.1 KB) (334 lines)
  - games_with_angels.md (11.3 KB) (232 lines)
  - historical_incarnations.md (34.1 KB) (110 lines)
  - storyline_generator_architecture.md (54.5 KB) (1089 lines)
  - the_lighthouse.md (34.3 KB) (842 lines)
- game_mechanics/
  - dialog_system/
    - __init__.py (4.2 KB) (135 lines)
    - behavioral_filter.py (20.0 KB) (429 lines)
    - cache_optimizer.py (19.4 KB) (517 lines)
    - core_structures.py (15.2 KB) (376 lines)
    - governor_preferences.py (14.1 KB) (321 lines)
    - intent_classifier.py (7.5 KB) (188 lines)
    - nlu_engine.py (12.4 KB) (347 lines)
    - preference_encoder.py (21.2 KB) (472 lines)
    - preference_structures.py (8.3 KB) (191 lines)
    - response_selector.py (16.7 KB) (382 lines)
    - similarity_engine.py (6.5 KB) (166 lines)
    - state_machine.py (16.7 KB) (457 lines)
    - storage_schemas.py (13.6 KB) (351 lines)
    - trait_mapper.py (16.6 KB) (387 lines)
  - divination_systems/
    - tarot_game_engine.py (7.8 KB) (186 lines)
    - tarot_game_interface.py (4.0 KB) (100 lines)
  - ritual_systems/
- governor_indexes/
  - COMPREHENSIVE_TRAIT_CHOICES.md (30.0 KB) (1163 lines)
  - READ_ME.md (6.1 KB) (118 lines)
  - approaches.json (2.1 KB) (92 lines)
  - canonical_traits.json (3.8 KB) (113 lines)
  - flaws_pool.json (3.4 KB) (41 lines)
  - motive_alignment.json (993.0 B) (12 lines)
  - orientation_io.json (321.0 B) (6 lines)
  - polarity_cd.json (318.0 B) (6 lines)
  - relationship_types.json (338.0 B) (7 lines)
  - role_archtypes.json (1.9 KB) (23 lines)
  - self_regard_options.json (2.0 KB) (23 lines)
  - tones.json (2.0 KB) (92 lines)
  - trait_choice_questions_catalog.json (6.8 KB) (183 lines)
  - virtues_pool.json (3.5 KB) (41 lines)
- integration_layer/
  - coordinators/
    - batch_governor_assignment.py (4.3 KB) (97 lines)
- knowledge_base/
  - CODER_AGENT_INSTRUCTIONS.md (7.8 KB) (208 lines)
  - CODER_AGENT_INSTRUCTIONS_PART2.md (7.1 KB) (191 lines)
  - NEXT_IMPLEMENTATION_STEPS.md (5.9 KB) (163 lines)
  - README.md (9.6 KB) (224 lines)
  - SYSTEM_STATUS_REPORT.md (6.4 KB) (184 lines)
  - approach_comparison.json (1.0 KB) (26 lines)
  - complete_system_test.py (8.7 KB) (185 lines)
  - complete_system_test_results.json (43.0 B) (3 lines)
  - direct_wikipedia_mapping.json (100.7 KB) (869 lines)
  - extracted_knowledge_content.json (57.5 KB) (408 lines)
  - focused_mystical_retrieval_test.json (5.0 KB) (120 lines)
  - free_content_consolidator.py (5.2 KB) (128 lines)
  - free_web_scraper.py (8.5 KB) (209 lines)
  - implementation_dashboard.md (11.2 KB) (297 lines)
  - lighthouse_research_index.py (65.3 KB) (1338 lines)
  - lighthouse_research_results.json (199.1 KB) (2482 lines)
  - missing_traditions_analysis.md (29.1 KB) (707 lines)
  - organized_tradition_mapper.py (13.1 KB) (299 lines)
  - organized_tradition_mapping.json (8.2 KB) (246 lines)
  - requirements.txt (298.0 B) (16 lines)
  - restructure_log.py (3.4 KB) (75 lines)
  - retrieval_results_occodon_test.json (104.8 KB) (1191 lines)
  - run_lighthouse_research.py (6.6 KB) (171 lines)
  - url_content_processor.py (10.6 KB) (253 lines)
  - wiki_api_extractor.py (10.3 KB) (267 lines)
  - wiki_api_knowledge_content.json (166.2 KB) (1848 lines)
  - archives/
    - batch_processor.py (9.1 KB) (220 lines)
    - complete_concepts_processor.py (18.5 KB) (167 lines)
    - complete_remaining.py (1.2 KB) (46 lines)
    - comprehensive_traditions_index.json (5.7 KB) (157 lines)
    - comprehensive_traditions_processor.py (12.2 KB) (290 lines)
    - create_index.py (3.3 KB) (78 lines)
    - demo_thoughtful_selection.py (4.0 KB) (116 lines)
    - enhanced_batch_processor.py (8.7 KB) (205 lines)
    - enhanced_governor_index.json (113.1 KB) (1790 lines)
    - enhanced_knowledge_extractor.py (30.2 KB) (556 lines)
    - enhanced_trait_index.json (83.1 KB) (1567 lines)
    - enhanced_trait_indexer.log (3.5 KB) (50 lines)
    - enhanced_trait_indexer.py (13.0 KB) (308 lines)
    - governor_review_template.log (4.7 KB) (63 lines)
    - governor_review_template.py (23.7 KB) (532 lines)
    - knowledge_extraction.log (11.9 KB) (61 lines)
    - knowledge_extractor.py (21.0 KB) (428 lines)
    - legacy_research_processor.py (24.0 KB) (370 lines)
    - mystical_content_extractor.py (12.5 KB) (258 lines)
    - mystical_traditions_index.json (183.7 KB) (2702 lines)
    - mystical_traditions_processor.py (6.8 KB) (166 lines)
    - test_extractor.py (5.6 KB) (150 lines)
    - tradition_audit.py (7.0 KB) (175 lines)
    - tradition_selection_index.json (19.4 KB) (519 lines)
    - tradition_selection_indexer.log (6.7 KB) (82 lines)
    - tradition_selection_indexer.py (16.4 KB) (374 lines)
    - unified_knowledge_index.json (12.2 KB) (462 lines)
    - governor_archives/
      - celtic_druidic_governor_archive.json (4.4 KB) (106 lines)
      - chaos_magic_governor_archive.json (4.2 KB) (106 lines)
      - classical_philosophy_governor_archive.json (4.1 KB) (106 lines)
      - egyptian_magic_governor_archive.json (4.3 KB) (106 lines)
      - enochian_magic_governor_archive.json (8.5 KB) (167 lines)
      - gnostic_traditions_governor_archive.json (4.0 KB) (98 lines)
      - golden_dawn_governor_archive.json (4.3 KB) (100 lines)
      - hermetic_philosophy_governor_archive.json (8.4 KB) (165 lines)
      - i_ching_governor_archive.json (4.0 KB) (98 lines)
      - kabbalistic_mysticism_governor_archive.json (8.3 KB) (163 lines)
      - kuji_kiri_governor_archive.json (4.0 KB) (98 lines)
      - norse_traditions_governor_archive.json (3.9 KB) (98 lines)
      - sacred_geometry_governor_archive.json (3.9 KB) (98 lines)
      - sufi_mysticism_governor_archive.json (3.8 KB) (98 lines)
      - taoism_governor_archive.json (3.9 KB) (98 lines)
      - tarot_knowledge_governor_archive.json (4.0 KB) (98 lines)
      - thelema_governor_archive.json (3.8 KB) (98 lines)
    - personality_seeds/
      - celtic_druidic_seed.json (411.0 B) (13 lines)
      - chaos_magic_seed.json (487.0 B) (17 lines)
      - classical_philosophy_seed.json (497.0 B) (17 lines)
      - egyptian_magic_seed.json (395.0 B) (13 lines)
      - gnostic_traditions_seed.json (385.0 B) (13 lines)
      - golden_dawn_seed.json (521.0 B) (17 lines)
      - i_ching_seed.json (392.0 B) (13 lines)
      - kuji_kiri_seed.json (409.0 B) (13 lines)
      - norse_traditions_seed.json (500.0 B) (17 lines)
      - sacred_geometry_seed.json (381.0 B) (13 lines)
      - sufi_mysticism_seed.json (474.0 B) (17 lines)
      - taoism_seed.json (475.0 B) (17 lines)
      - tarot_knowledge_seed.json (502.0 B) (17 lines)
      - thelema_seed.json (369.0 B) (13 lines)
    - review_templates/
      - ABRIOND_review_template.json (33.9 KB) (306 lines)
      - ADVORPT_review_template.json (34.8 KB) (306 lines)
      - AMBRIOL_review_template.json (34.8 KB) (306 lines)
      - ANDISPI_review_template.json (34.8 KB) (306 lines)
      - ASPIAON_review_template.json (34.8 KB) (306 lines)
  - data/
    - curated_sources.py (6.0 KB) (142 lines)
    - extraction.log (2.1 KB) (20 lines)
  - links/
    - research_celtic_druidic.json (10.0 KB) (67 lines)
    - research_chaos_magic.json (9.5 KB) (67 lines)
    - research_classical_philosophy.json (10.1 KB) (67 lines)
    - research_egyptian_magic.json (9.7 KB) (67 lines)
    - research_enochian_magic.json (5.6 KB) (87 lines)
    - research_gnostic_traditions.json (9.5 KB) (67 lines)
    - research_golden_dawn.json (9.5 KB) (65 lines)
    - research_golden_dawn_magic.json (5.9 KB) (87 lines)
    - research_hermetic_philosophy.json (5.8 KB) (87 lines)
    - research_i_ching.json (10.1 KB) (67 lines)
    - research_kabbalistic_mysticism.json (5.9 KB) (87 lines)
    - research_kuji_kiri.json (10.3 KB) (67 lines)
    - research_norse_traditions.json (9.8 KB) (67 lines)
    - research_sacred_geometry.json (9.4 KB) (67 lines)
    - research_sufi_mysticism.json (9.3 KB) (67 lines)
    - research_taoism.json (9.5 KB) (67 lines)
    - research_tarot_knowledge.json (9.8 KB) (67 lines)
    - research_thelema.json (11.9 KB) (78 lines)
  - retrievers/
    - focused_mystical_retriever.py (15.2 KB) (298 lines)
    - knowledge_retriever.py (11.1 KB) (245 lines)
    - retrieval_results_occodon_test.json (1.2 KB) (58 lines)
  - schemas/
    - discovery_schemas.py (1.6 KB) (59 lines)
    - knowledge_schemas.py (4.5 KB) (129 lines)
  - traditions/
    - enochian_knowledge_database.py (18.5 KB) (369 lines)
    - golden_dawn_knowledge_database.py (4.6 KB) (82 lines)
    - hermetic_knowledge_database.py (19.5 KB) (381 lines)
    - kabbalah_knowledge_database.py (25.0 KB) (494 lines)
    - unified_knowledge_retriever.py (8.6 KB) (213 lines)
  - utils/
    - simple_index_updater.py (7.8 KB) (192 lines)
    - knowledge_base/
      - data/
        - index_backups/
- mystical_systems/
  - kabbalah_system/
    - data/
      - sefirot_database.py (9.4 KB) (253 lines)
  - numerology_system/
    - data/
      - numerology_database.py (7.8 KB) (197 lines)
  - tarot_system/
    - tarot_system.py (2.1 KB) (52 lines)
    - test_tarot.py (411.0 B) (13 lines)
    - data/
      - tarot_cards_database.py (11.8 KB) (275 lines)
    - engines/
      - governor_tarot_assigner.py (11.1 KB) (245 lines)
    - schemas/
      - tarot_schemas.py (1.7 KB) (59 lines)
    - ui/
      - card_render.py (3.9 KB) (109 lines)
    - utils/
      - tarot_utils.py (1.3 KB) (33 lines)
  - zodiac_system/
    - data/
      - zodiac_database.py (11.6 KB) (303 lines)
- pack/
  - aethyrs.json (36.8 KB) (1122 lines)
  - enochian_alphabet.json (279.0 B) (25 lines)
  - sigillum.json (427.0 B) (23 lines)
  - sigillum_dei_aemeth.js (3.7 KB) (115 lines)
  - watchtowers.json (3.6 KB) (65 lines)
governor_generator/ (core)
- storyline_engine/
  - batch_retry_handler.py (9.5 KB) (243 lines)
  - batch_storyline_generator.py (16.5 KB) (403 lines)
  - canonical_loader.py (2.1 KB) (65 lines)
  - canonical_trait_registry.py (5.2 KB) (147 lines)
  - core_loader.py (12.1 KB) (294 lines)
  - enhanced_element_detector.py (7.5 KB) (198 lines)
  - enhanced_story_builder.py (7.1 KB) (179 lines)
  - governor_engine.py (13.7 KB) (320 lines)
  - persona_extractor.py (5.5 KB) (157 lines)
  - rate_limit_handler.py (9.7 KB) (257 lines)
  - storyline_template.py (3.7 KB) (105 lines)
  - dev_tools/
    - batch_usage_examples.py (4.5 KB) (135 lines)
    - direct_validation.py (7.2 KB) (190 lines)
    - enhanced_generator_v2.py (16.0 KB) (381 lines)
    - final_validation.py (6.6 KB) (179 lines)
    - production_readiness_summary.py (3.6 KB) (107 lines)
    - readiness_core_batch.py (1.8 KB) (57 lines)
    - readiness_data_validation.py (2.8 KB) (87 lines)
    - readiness_error_handling.py (2.9 KB) (83 lines)
    - run_production_assessment.py (1.3 KB) (38 lines)
    - simple_generator.py (11.2 KB) (295 lines)
    - test_components.py (6.7 KB) (203 lines)
    - test_integration.py (12.0 KB) (331 lines)
    - test_persona.py (1.4 KB) (46 lines)
    - test_pipeline.py (13.4 KB) (342 lines)
    - test_storyline_engine_fixes.py (11.3 KB) (305 lines)
    - test_validation_integration.py (1.2 KB) (39 lines)
    - updated_production_assessment.py (5.6 KB) (130 lines)
  - schemas/
    - __init__.py (431.0 B) (14 lines)
    - governor_input_schema.py (7.2 KB) (187 lines)
    - storyline_output_schema.py (10.6 KB) (269 lines)
  - storyline_docs/
    - storyline_checklist.md (37.3 KB) (577 lines)
    - storyline_template.md (50.7 KB) (462 lines)
- tests/
  - performance_benchmark.py (15.6 KB) (402 lines)
  - test_governor_preferences.py (9.9 KB) (252 lines)
  - unit_tests/
- trac_build/
  - IMPLEMENTATION_GUIDES.md (32.8 KB) (1237 lines)
  - TAP_TRAC_RESOURCES.md (10.5 KB) (232 lines)
  - architecture_map_trac.md (44.9 KB) (959 lines)
  - high_level_overview_trac.md (63.4 KB) (163 lines)
  - implementation-roadmap_trac.md (31.3 KB) (810 lines)
  - template_psudocode_samples_trac.md (124.8 KB) (2698 lines)
  - trac_build_review.md (68.0 KB) (164 lines)
  - ui_build_checklist_trac.md (37.0 KB) (1006 lines)
  - utility_matrix.md (42.0 KB) (108 lines)
- unified_profiler/
  - core/
    - mystical_profiler.py (10.7 KB) (246 lines)
    - system_registry.py (0.0 B)
  - interfaces/
    - base_system.py (1.7 KB) (43 lines)
  - schemas/
    - mystical_schemas.py (4.6 KB) (137 lines)
```

## 🔍 Core Codebase Analysis

### 📋 Largest Core Files

| File | Size | Lines | Type |
|------|------|-------|------|
| `knowledge_base\lighthouse_research_results.json` | 199.1 KB | 2,482 | Configuration |
| `knowledge_base\archives\mystical_traditions_index.json` | 183.7 KB | 2,702 | Configuration |
| `canon\canon_governor_profiles.json` | 173.0 KB | 6,476 | Configuration |
| `knowledge_base\wiki_api_knowledge_content.json` | 166.2 KB | 1,848 | Configuration |
| `review_map.md` | 140.4 KB | 3,368 | Documentation |
| `trac_build\template_psudocode_samples_trac.md` | 124.8 KB | 2,698 | Documentation |
| `knowledge_base\archives\enhanced_governor_index.json` | 113.1 KB | 1,790 | Configuration |
| `knowledge_base\retrieval_results_occodon_test.json` | 104.8 KB | 1,191 | Configuration |
| `knowledge_base\direct_wikipedia_mapping.json` | 100.7 KB | 869 | Configuration |
| `knowledge_base\archives\enhanced_trait_index.json` | 83.1 KB | 1,567 | Configuration |

### 🐍 Python Files Summary

**Total Python Lines:** 24,041

| File | Lines | Size |
|------|-------|------|
| `knowledge_base\lighthouse_research_index.py` | 1,338 | 65.3 KB |
| `knowledge_base\archives\enhanced_knowledge_extractor.py` | 556 | 30.2 KB |
| `knowledge_base\archives\governor_review_template.py` | 532 | 23.7 KB |
| `game_mechanics\dialog_system\cache_optimizer.py` | 517 | 19.4 KB |
| `knowledge_base\traditions\kabbalah_knowledge_database.py` | 494 | 25.0 KB |
| `create_clean_map.py` | 487 | 19.1 KB |
| `game_mechanics\dialog_system\preference_encoder.py` | 472 | 21.2 KB |
| `game_mechanics\dialog_system\state_machine.py` | 457 | 16.7 KB |
| `game_mechanics\dialog_system\behavioral_filter.py` | 429 | 20.0 KB |
| `knowledge_base\archives\knowledge_extractor.py` | 428 | 21.0 KB |

### 📚 Documentation Files

| File | Lines | Size |
|------|-------|------|
| `review_map.md` | 3,368 | 140.4 KB |
| `trac_build\template_psudocode_samples_trac.md` | 2,698 | 124.8 KB |
| `trac_build\trac_build_review.md` | 164 | 68.0 KB |
| `trac_build\high_level_overview_trac.md` | 163 | 63.4 KB |
| `canon\canon_sources.md` | 678 | 58.7 KB |
| `enochian_workbook.md` | 474 | 56.8 KB |
| `canon\expansions\prebaked_expansion_pack_instructions.md` | 337 | 55.5 KB |
| `concept_docs\storyline_generator_architecture.md` | 1,089 | 54.5 KB |
| `storyline_engine\storyline_docs\storyline_template.md` | 462 | 50.7 KB |
| `trac_build\architecture_map_trac.md` | 959 | 44.9 KB |
| `trac_build\utility_matrix.md` | 108 | 42.0 KB |
| `storyline_engine\storyline_docs\storyline_checklist.md` | 577 | 37.3 KB |
| `trac_build\ui_build_checklist_trac.md` | 1,006 | 37.0 KB |
| `concept_docs\the_lighthouse.md` | 842 | 34.3 KB |
| `concept_docs\historical_incarnations.md` | 110 | 34.1 KB |
| `trac_build\IMPLEMENTATION_GUIDES.md` | 1,237 | 32.8 KB |
| `enochian_workbook_overview.txt` | 363 | 31.6 KB |
| `trac_build\implementation-roadmap_trac.md` | 810 | 31.3 KB |
| `README.md` | 673 | 30.9 KB |
| `governor_indexes\COMPREHENSIVE_TRAIT_CHOICES.md` | 1,163 | 30.0 KB |
| `knowledge_base\missing_traditions_analysis.md` | 707 | 29.1 KB |
| `canon\expansions\voidmaker\voidmaker_concepts.md` | 184 | 22.6 KB |
| `canon\BITCOIN_ONCHAIN_RESOURCES.md` | 241 | 12.9 KB |
| `concept_docs\context_aware.md` | 334 | 12.1 KB |
| `canon\expansions\voidmaker\voidmaker_expansion.md` | 304 | 11.9 KB |
| `concept_docs\games_with_angels.md` | 232 | 11.3 KB |
| `knowledge_base\implementation_dashboard.md` | 297 | 11.2 KB |
| `canon\expansions\advanced-considerations.md` | 328 | 10.6 KB |
| `trac_build\TAP_TRAC_RESOURCES.md` | 232 | 10.5 KB |
| `knowledge_base\README.md` | 224 | 9.6 KB |
| `knowledge_base\CODER_AGENT_INSTRUCTIONS.md` | 208 | 7.8 KB |
| `CONTEXT_AWARE_DIALOG_HANDOFF.md` | 151 | 7.4 KB |
| `knowledge_base\CODER_AGENT_INSTRUCTIONS_PART2.md` | 191 | 7.1 KB |
| `knowledge_base\SYSTEM_STATUS_REPORT.md` | 184 | 6.4 KB |
| `governor_indexes\READ_ME.md` | 118 | 6.1 KB |
| `canon\expansions\voidmaker\voidmaker_questions.md` | 111 | 6.0 KB |
| `knowledge_base\NEXT_IMPLEMENTATION_STEPS.md` | 163 | 5.9 KB |
| `concept_docs\LIGHTHOUSE_SUMMARY.md` | 104 | 4.4 KB |
| `anthropic_setup.md` | 60 | 1.7 KB |
| `knowledge_base\requirements.txt` | 16 | 298.0 B |
| `requirements.txt` | 3 | 59.0 B |
| `requirements_enhancement.txt` | 2 | 34.0 B |

## 🧩 Core Component Breakdown

| Component | Dirs | Files | Size | Python Files | Python Lines | Docs | Config |
|-----------|------|-------|------|--------------|--------------|------|--------|
| `canon` | 3 | 11 | 422.1 KB | 0 | 0 | 7 | 4 |
| `cli` | 1 | 1 | 2.8 KB | 1 | 79 | 0 | 0 |
| `concept_docs` | 1 | 6 | 150.7 KB | 0 | 0 | 6 | 0 |
| `game_mechanics` | 4 | 16 | 204.3 KB | 16 | 5,005 | 0 | 0 |
| `governor_indexes` | 1 | 14 | 63.5 KB | 0 | 0 | 2 | 12 |
| `integration_layer` | 2 | 1 | 4.3 KB | 1 | 97 | 0 | 0 |
| `knowledge_base` | 14 | 120 | 2.0 MB | 37 | 9,968 | 8 | 70 |
| `mystical_systems` | 13 | 10 | 61.0 KB | 10 | 1,539 | 0 | 0 |
| `pack` | 1 | 5 | 44.9 KB | 0 | 0 | 0 | 4 |
| `storyline_engine` | 4 | 33 | 308.4 KB | 31 | 5,786 | 2 | 0 |
| `tests` | 2 | 2 | 25.5 KB | 2 | 654 | 0 | 0 |
| `trac_build` | 1 | 9 | 454.6 KB | 0 | 0 | 9 | 0 |
| `unified_profiler` | 4 | 4 | 17.0 KB | 4 | 426 | 0 | 0 |

---
*Generated by Clean Project Mapper - 2025-07-02 18:48:47*
*This map focuses on core development files and excludes large asset directories.*
