#!/usr/bin/env python3

import json
from pathlib import Path

def analyze_chunk_completion():
    """Analyze the discrepancy between parse success and question completion"""
    
    # Load the actual results
    occodon_path = Path("governor_output/OCCODON.json")
    if not occodon_path.exists():
        print("OCCODON.json not found")
        return
    
    with open(occodon_path, 'r') as f:
        occodon_data = json.load(f)
    
    blocks = occodon_data["blocks"]
    
    print("=== ACTUAL RESULTS ANALYSIS ===")
    print(f"Total questions found: {sum(len(block['questions']) for block in blocks.values())}")
    print()
    
    # Analyze each block
    for block_key, block_data in blocks.items():
        questions = block_data["questions"]
        question_nums = [int(q) for q in questions.keys()]
        question_nums.sort()
        
        print(f"Block {block_key}:")
        print(f"  Questions: {question_nums}")
        print(f"  Count: {len(question_nums)}")
        print(f"  Range: {min(question_nums)}-{max(question_nums)}")
        print()
    
    # Analyze chunk strategy vs reality
    print("=== CHUNK STRATEGY ANALYSIS ===")
    
    # Expected chunks from our strategy
    expected_chunks = {
        "chunk_1": {"blocks": ["A_identity_origin", "B_elemental_essence"], "range": "1-10"},
        "chunk_2": {"blocks": ["C_personality_emotional", "D_teaching_doctrine"], "range": "11-25"},
        "chunk_3": {"blocks": ["E_sacrifice_trial", "F_riddles_puzzles"], "range": "26-35"},
        "chunk_4": {"blocks": ["G_gifts_boons", "H_cosmic_secrets"], "range": "36-51"},
        "chunk_5": {"blocks": ["I_interpersonal_dynamics", "J_game_mechanics"], "range": "52-67"},
        "chunk_6": {"blocks": ["K_dialogue_narrative", "L_longterm_arc"], "range": "68-79"},
        "chunk_7": {"blocks": ["M_inter_governor", "N_ethics_boundaries"], "range": "80-89"},
        "chunk_8": {"blocks": ["O_aesthetics_artistic", "P_practical_implementation"], "range": "90-99"},
        "chunk_9": {"blocks": ["Q_metrics_success", "R_post_quest"], "range": "100-110"},
        "chunk_10": {"blocks": ["S_metaphysical_legacy", "T_eschatology"], "range": "111-122"},
        "chunk_11": {"blocks": ["U_celestial_cartography", "V_forbidden_knowledge", "W_divine_memory"], "range": "123-127"}
    }
    
    for chunk_name, chunk_info in expected_chunks.items():
        print(f"{chunk_name}: {chunk_info['range']}")
        expected_blocks = chunk_info["blocks"]
        found_blocks = [b for b in expected_blocks if b in blocks]
        missing_blocks = [b for b in expected_blocks if b not in blocks]
        
        if found_blocks:
            print(f"  ✅ Found: {found_blocks}")
        if missing_blocks:
            print(f"  ❌ Missing: {missing_blocks}")
        
        # Count questions in found blocks
        total_questions = sum(len(blocks[b]["questions"]) for b in found_blocks)
        print(f"  Questions answered: {total_questions}")
        print()
    
    # Check for pattern
    print("=== PATTERN ANALYSIS ===")
    multi_block_chunks = [chunk for chunk, info in expected_chunks.items() if len(info["blocks"]) > 1]
    
    print("Multi-block chunks:")
    for chunk in multi_block_chunks:
        chunk_info = expected_chunks[chunk]
        expected_blocks = chunk_info["blocks"]
        found_blocks = [b for b in expected_blocks if b in blocks]
        
        print(f"  {chunk}: {len(found_blocks)}/{len(expected_blocks)} blocks completed")
        if len(found_blocks) < len(expected_blocks):
            print(f"    ⚠️  Incomplete: Only got {found_blocks} out of {expected_blocks}")

if __name__ == "__main__":
    analyze_chunk_completion() 