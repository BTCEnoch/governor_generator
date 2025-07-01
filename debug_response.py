#!/usr/bin/env python3

import json
from pathlib import Path
from generate_governor_jsons import (
    load_resource, get_governor_dossier, extract_chunk_questions,
    build_chunk_prompt, call_anthropic, parse_chunk_response,
    LOCAL_GOVERNOR_PROFILE_PATH, REMOTE_GOVERNOR_PROFILE_URL,
    LOCAL_QUESTIONS_CATALOG_PATH, REMOTE_QUESTIONS_CATALOG_URL,
    LOCAL_CANON_SOURCES_PATH, REMOTE_CANON_SOURCES_URL,
    CHUNK_STRATEGY
)

def debug_chunk_response():
    """Debug what Claude returns for chunk 1"""
    
    # Load data
    assignment_md = Path("governor_interview_templates/governor_01_occodon_assignment_prompt.md").read_text(encoding="utf-8")
    profiles_text = load_resource(LOCAL_GOVERNOR_PROFILE_PATH, REMOTE_GOVERNOR_PROFILE_URL)
    questions_catalog_text = load_resource(LOCAL_QUESTIONS_CATALOG_PATH, REMOTE_QUESTIONS_CATALOG_URL)
    sources_md = load_resource(LOCAL_CANON_SOURCES_PATH, REMOTE_CANON_SOURCES_URL)
    
    profiles_json = json.loads(profiles_text)
    questions_catalog_data = json.loads(questions_catalog_text)
    dossier = get_governor_dossier(profiles_json, 1)
    
    # Test chunk 1
    chunk_info = CHUNK_STRATEGY["chunk_1"]
    chunk_questions = extract_chunk_questions(questions_catalog_data, chunk_info["blocks"])
    
    print("=== CHUNK 1 DEBUG ===")
    print(f"Chunk info: {chunk_info}")
    print(f"Number of blocks: {len(chunk_questions)}")
    print(f"Blocks: {list(chunk_questions.keys())}")
    
    # Build prompt
    prompt_messages = build_chunk_prompt(
        dossier=dossier,
        assignment_md=assignment_md,
        chunk_questions=chunk_questions,
        sources_md=sources_md,
        chunk_info=chunk_info
    )
    
    print(f"\n=== SYSTEM MESSAGE PREVIEW ===")
    print(prompt_messages[0]["content"][:500] + "...")
    
    print(f"\n=== CALLING CLAUDE ===")
    response_text = call_anthropic(prompt_messages)
    
    print(f"\n=== RAW RESPONSE ===")
    print(response_text[:1000])
    if len(response_text) > 1000:
        print(f"... [truncated, total length: {len(response_text)}]")
    
    # Try parsing
    print(f"\n=== PARSING ATTEMPT ===")
    parsed_blocks = parse_chunk_response(response_text, chunk_questions)
    print(f"Parsed blocks: {len(parsed_blocks)}")
    print(f"Block keys: {list(parsed_blocks.keys())}")
    
    if parsed_blocks:
        for block_key, block_data in parsed_blocks.items():
            print(f"Block {block_key}: {len(block_data.get('questions', {}))} questions")
    else:
        print("❌ No blocks parsed")
        
        # Debug: show first few lines of response
        lines = response_text.strip().split('\n')[:10]
        print(f"\nFirst 10 lines of response:")
        for i, line in enumerate(lines):
            print(f"{i+1}: {line}")

if __name__ == "__main__":
    debug_chunk_response() 