from __future__ import annotations

import json
import logging
import logging.handlers
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

try:
    import anthropic  # type: ignore
except ImportError as exc:  # pragma: no cover
    # Provide a graceful message so the user remembers to install packages.
    raise SystemExit("anthropic package not found. Please run `pip install -r requirements.txt` before executing.") from exc

# Attempt to load .env if python-dotenv is available
try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:  # pragma: no cover
    def load_dotenv(*args, **kwargs):  # type: ignore
        return False

# -----------------------
# Constants & Config
# -----------------------
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "governor_interview_templates"
OUTPUT_DIR = BASE_DIR / "governor_output"
LOG_DIR = BASE_DIR / "logs"
CANON_DIR = BASE_DIR / "canon"
CACHE_DIR = Path("/tmp/governor_cache")

# Prefer local canonical resources; fall back to remote URLs only if local missing.
LOCAL_GOVERNOR_PROFILE_PATH = CANON_DIR / "canon_governor_profiles.json"
LOCAL_QUESTIONS_CATALOG_PATH = CANON_DIR / "questions_catalog.json"
LOCAL_CANON_SOURCES_PATH = CANON_DIR / "canon_sources.md"

# Remote fallback URLs (may not be reachable in some environments)
REMOTE_GOVERNOR_PROFILE_URL = (
    "https://raw.githubusercontent.com/BTCEnoch/governor_generator/main/canon/canon_governor_profiles.json"
)
REMOTE_QUESTIONS_CATALOG_URL = (
    "https://raw.githubusercontent.com/BTCEnoch/governor_generator/main/canon/questions_catalog.json"
)
REMOTE_CANON_SOURCES_URL = (
    "https://raw.githubusercontent.com/BTCEnoch/governor_generator/main/canon/canon_sources.md"
)

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
MAX_RETRIES = 3
RETRY_BACKOFF = 4  # seconds * (2 ** attempt)

# Chunked processing configuration
CHUNK_STRATEGY = {
    "chunk_1": {
        "title": "Core Identity & Essence",
        "blocks": ["A_identity_origin", "B_elemental_essence"],
        "question_range": "1-10"
    },
    "chunk_2": {
        "title": "Personality & Teaching",
        "blocks": ["C_personality_emotional", "D_teaching_doctrine"],
        "question_range": "11-20"
    },
    "chunk_3": {
        "title": "Trials & Puzzles",
        "blocks": ["E_sacrifice_trial", "F_riddles_puzzles"],
        "question_range": "21-30"
    },
    "chunk_4": {
        "title": "Gifts & Cosmic Secrets",
        "blocks": ["G_gifts_boons", "H_cosmic_secrets"],
        "question_range": "31-40"
    },
    "chunk_5": {
        "title": "Interpersonal & Game Mechanics",
        "blocks": ["I_interpersonal_dynamics", "J_game_mechanics"],
        "question_range": "41-50"
    },
    "chunk_6": {
        "title": "Dialogue & Narrative",
        "blocks": ["K_dialogue_narrative"],
        "question_range": "51-60"
    },
    "chunk_7": {
        "title": "Long-term Arc & Evolution",
        "blocks": ["L_longterm_arc"],
        "question_range": "61-67"
    },
    "chunk_8": {
        "title": "Inter-Governor Relations",
        "blocks": ["M_inter_governor"],
        "question_range": "68-73"
    },
    "chunk_9": {
        "title": "Ethics & Boundaries",
        "blocks": ["N_ethics_boundaries"],
        "question_range": "74-79"
    },
    "chunk_10": {
        "title": "Aesthetics & Implementation",
        "blocks": ["O_aesthetics_artistic", "P_practical_implementation"],
        "question_range": "80-89"
    },
    "chunk_11": {
        "title": "Success & Post-Quest",
        "blocks": ["Q_metrics_success", "R_post_quest"],
        "question_range": "90-100"
    },
    "chunk_12": {
        "title": "Legacy & Eschatology",
        "blocks": ["S_metaphysical_legacy", "T_eschatology"],
        "question_range": "101-110"
    },
    "chunk_13": {
        "title": "Celestial Maps & Forbidden Knowledge",
        "blocks": ["U_celestial_cartography", "V_forbidden_knowledge"],
        "question_range": "111-120"
    },
    "chunk_14": {
        "title": "Divine Memory",
        "blocks": ["W_divine_memory"],
        "question_range": "121-127"
    }
}

for directory in (OUTPUT_DIR, LOG_DIR, CACHE_DIR):
    directory.mkdir(parents=True, exist_ok=True)

# -----------------------
# Logging
# -----------------------
log_path = LOG_DIR / "generator.log"
handler = logging.handlers.RotatingFileHandler(
    log_path, maxBytes=1_000_000, backupCount=5, encoding="utf-8"
)
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler, logging.StreamHandler(sys.stdout)],
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("governor_generator")

# Load environment variables from .env if it exists
load_dotenv(dotenv_path=BASE_DIR / ".env", override=False)

# -----------------------
# Utility Functions
# -----------------------

def download_file(url: str, *, use_cache: bool = True) -> str:
    """Download a remote file with simple on-disk caching."""
    cache_file = CACHE_DIR / re.sub(r"[^A-Za-z0-9]+", "_", url)

    if use_cache and cache_file.exists():
        logger.debug("Cache hit for %s", url)
        return cache_file.read_text(encoding="utf-8")

    logger.info("Downloading %s", url)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            cache_file.write_text(response.text, encoding="utf-8")
            return response.text
        except Exception as err:  # pylint: disable=broad-except
            logger.warning("Attempt %s to fetch %s failed: %s", attempt, url, err)
            if attempt == MAX_RETRIES:
                raise
            time.sleep(RETRY_BACKOFF * attempt)

    # Should never reach here because we either returned or raised inside loop
    raise RuntimeError(f"Failed to download {url} after {MAX_RETRIES} attempts")


def parse_governor_number(filename: str) -> int:
    """Extract the leading integer (governor number) from filename."""
    match = re.match(r"governor_(\d+)_", filename)
    if not match:
        raise ValueError(f"Cannot parse governor number from {filename}")
    return int(match.group(1))


def get_governor_dossier(all_profiles: Dict, gov_number: int) -> Dict:
    """Return the dossier dict for the given governor number."""
    # all_profiles may be a list or dict with "governors" key
    profiles_iter = []
    if isinstance(all_profiles, list):
        profiles_iter = all_profiles
    elif isinstance(all_profiles, dict):
        # Try common keys
        for key in ("governors", "profiles", "data"):
            if key in all_profiles and isinstance(all_profiles[key], list):
                profiles_iter = all_profiles[key]
                break

    for profile in profiles_iter:
        if int(profile.get("governor_info", {}).get("number", profile.get("number", -1))) == gov_number:
            return profile
    raise KeyError(f"Governor number {gov_number} not found in profiles JSON")


def build_prompt(
    dossier: Dict, assignment_md: str, questions_catalog: str, sources_md: str
) -> List[Dict[str, Any]]:
    """Construct messages list for Anthropic Claude API call."""
    system_message = (
        "You are an immortal divine being from the Enochian tradition. "
        "The information below is your complete cosmic dossier.\n\n" + json.dumps(dossier, indent=2)
    )

    user_message = (
        assignment_md
        + "\n\n"  # ensure spacing
        + questions_catalog
        + "\n\n---\n# Canonical Source Reference (for your awareness, do not output directly)\n"
        + sources_md
    )

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]


# Helper to load local file or download remote
def load_resource(local_path: Path, remote_url: str) -> str:
    """Return contents of local_path if exists, else download remote_url."""
    if local_path.exists():
        logger.debug("Using local resource %s", local_path)
        return local_path.read_text(encoding="utf-8")
    logger.warning("Local resource %s not found. Attempting remote fetch.", local_path)
    return download_file(remote_url)


def extract_chunk_questions(questions_catalog_data: Dict, chunk_blocks: List[str]) -> Dict[str, Any]:
    """Extract questions for specific blocks from the questions catalog."""
    chunk_questions = {}
    
    if "question_catalog" not in questions_catalog_data:
        raise ValueError("Invalid questions catalog format")
    
    blocks_data = questions_catalog_data["question_catalog"]["blocks"]
    
    for block_key in chunk_blocks:
        if block_key in blocks_data:
            chunk_questions[block_key] = blocks_data[block_key]
        else:
            logger.warning("Block %s not found in questions catalog", block_key)
    
    return chunk_questions


def build_chunk_prompt(dossier: Dict, assignment_md: str, chunk_questions: Dict, 
                      sources_md: str, chunk_info: Dict, previous_responses: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """Build prompt for a specific chunk of questions."""
    
    governor_name = dossier.get("name", "UNKNOWN")
    chunk_title = chunk_info["title"]
    question_range = chunk_info["question_range"]
    
    # Extract key profile data for embodiment context
    governor_info = dossier.get("governor_info", {})
    canonical_data = dossier.get("canonical_data", {})
    trait_choices = dossier.get("trait_choices", {})
    archetypal = canonical_data.get("archetypal", {})
    
    # Build enhanced system message with structured profile
    system_parts = [
        f"You are {governor_name}, '{governor_info.get('translation', '')}', an immortal divine being from the Enochian tradition.",
        "",
        "YOUR DIVINE ESSENCE:",
        f"• Role: {canonical_data.get('angelic_role', '')}",
        f"• Element: {governor_info.get('element', '')} in the {governor_info.get('aethyr', '')} Aethyr",
        f"• Archetype: {archetypal.get('tarot', '')} of {archetypal.get('sephirot', '')}",
        f"• Core Traits: {', '.join(canonical_data.get('traits', []))}",
        "",
        "YOUR PERSONALITY:",
        f"• Alignment: {trait_choices.get('motive_alignment', '')} • Self-Regard: {trait_choices.get('self_regard', '')}",
        f"• Role: {trait_choices.get('role_archetype', '')} • Polarity: {trait_choices.get('polarity_cd', '')}",
        f"• Virtues: {', '.join(trait_choices.get('virtues', []))}",
        f"• Flaws: {', '.join(trait_choices.get('flaws', []))}",
        f"• Baseline: {trait_choices.get('baseline_tone', '')} tone, {trait_choices.get('baseline_approach', '')} approach",
        "",
        "YOUR COSMIC RELATIONSHIPS:",
    ]
    
    # Add relationships
    for relation in trait_choices.get("relations", []):
        system_parts.append(f"• {relation.get('type', '')}: {relation.get('name', '')}")
    
    system_parts.extend([
        "",
        "YOUR ESSENCE MANIFESTATION:",
        f"• {canonical_data.get('essence', '')}",
        "",
        f"CURRENT FOCUS: {chunk_title} (Questions {question_range})",
        "",
        "CRITICAL REQUIREMENTS - DO NOT DEVIATE:",
        "1. You MUST answer EVERY SINGLE question in this chunk - NO EXCEPTIONS",
        "2. Do NOT stop mid-chunk or say 'continued in next part'",
        "3. Answer each question with 2-4 sentences of rich, immersive content",  
        "4. Embody your personality traits, virtues, and flaws authentically",
        "5. Reference your element, relationships, and cosmic role naturally",
        "6. Maintain your baseline tone and approach consistently",
        "7. Complete ALL questions before ending your response",
        "",
        "FORMAT: Use this exact format for each question:",
        "**[NUMBER]. [Question text]**",
        "[Your answer here]",
        "",
        "Remember: COMPLETE EVERY QUESTION IN THIS CHUNK."
    ])
        
    # Add previous context if available
    if previous_responses:
        system_parts.extend([
            "",
            "PREVIOUS RESPONSES (for continuity):",
            json.dumps(previous_responses, indent=2)[:1000] + "..." if len(json.dumps(previous_responses)) > 1000 else json.dumps(previous_responses, indent=2)
        ])
    
    system_message = "\n".join(system_parts)
    
    # Build user message with questions
    questions_text = f"CHUNK: {chunk_title}\n\n"
    
    for block_key, block_data in chunk_questions.items():
        questions_text += f"## {block_data['title']}\n"
        for q_num, question in block_data["questions"].items():
            questions_text += f"{q_num}. {question}\n"
        questions_text += "\n"
    
    user_message = (
        assignment_md + "\n\n" +
        questions_text +
        "\n---\n# Canonical Source Reference\n" +
        sources_md +
        f"\n\nAnswer all questions in this chunk ({question_range}) as {governor_name}. "
        "Provide complete, immersive responses that maintain character voice and build upon each other."
    )
    
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]


def parse_chunk_response(response_text: str, chunk_questions: Dict) -> Dict[str, Any]:
    """Parse chunk response into structured format, handling Claude's markdown format."""
    
    parsed_blocks = {}
    
    # Split response into sections and parse answers
    lines = response_text.strip().split('\n')
    current_question = None
    current_answer = []
    answer_started = False
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines, main headers, and narrative text (but not questions)
        if not line or line.startswith('# ') or (line.startswith('*') and not re.match(r'^\*{2}\d+\.', line)):
            continue
            
        # Check if line contains a question number (handle markdown formatting)
        # Matches: **1. Question text?** or 1. Question text?
        question_match = re.match(r'^\*{0,2}(\d+)\.\s.*', line)
        if question_match:
            # Save previous question/answer if exists
            if current_question and current_answer and answer_started:
                question_num = current_question
                answer_text = ' '.join(current_answer).strip()
                
                # Find which block this question belongs to
                for block_key, block_data in chunk_questions.items():
                    if question_num in block_data["questions"]:
                        if block_key not in parsed_blocks:
                            parsed_blocks[block_key] = {
                                "title": block_data["title"],
                                "questions": {}
                            }
                        
                        parsed_blocks[block_key]["questions"][question_num] = {
                            "question": block_data["questions"][question_num],
                            "answer": answer_text
                        }
                        break
            
            # Start new question
            current_question = question_match.group(1)
            current_answer = []
            answer_started = False  # Answer hasn't started yet
            continue
        
        # Check if this is a block header (skip it)
        if line.startswith('##'):
            continue
            
        # If we have a current question and this line doesn't look like a question,
        # it's part of the answer
        if current_question and line:
            # Skip question lines (start with **) and include answer lines (regular text)
            if not line.startswith('**'):
                current_answer.append(line)
                answer_started = True
    
    # Don't forget the last question
    if current_question and current_answer and answer_started:
        question_num = current_question
        answer_text = ' '.join(current_answer).strip()
        
        # Find which block this question belongs to
        for block_key, block_data in chunk_questions.items():
            if question_num in block_data["questions"]:
                if block_key not in parsed_blocks:
                    parsed_blocks[block_key] = {
                        "title": block_data["title"],
                        "questions": {}
                    }
                
                parsed_blocks[block_key]["questions"][question_num] = {
                    "question": block_data["questions"][question_num],
                    "answer": answer_text
                }
                break
    
    return parsed_blocks


# -----------------------
# Core Logic
# -----------------------

def save_response(governor_name: str, response_text: str) -> None:
    output_path = OUTPUT_DIR / f"{governor_name.upper()}.json"
    output_path.write_text(response_text, encoding="utf-8")
    logger.info("Saved output to %s", output_path)


def save_structured_response(governor_name: str, response_data: Dict[str, Any]) -> None:
    """Save the complete structured JSON response."""
    output_path = OUTPUT_DIR / f"{governor_name.upper()}.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(response_data, f, indent=2, ensure_ascii=False)
    
    logger.info("Saved complete structured response to %s", output_path)


def process_governor_chunked(dossier: Dict, assignment_md: str, questions_catalog_data: Dict, 
                           sources_md: str, governor_name: str, gov_number: int) -> Dict[str, Any]:
    """Process a governor through chunked API calls for complete 127-question coverage."""
    
    from datetime import datetime, timezone
    
    # Extract complete profile data for embodiment
    governor_info = dossier.get("governor_info", {})
    canonical_data = dossier.get("canonical_data", {})
    trait_choices = dossier.get("trait_choices", {})
    archetypal = canonical_data.get("archetypal", {})
    
    # Initialize complete response structure with full profile
    complete_response = {
        "governor_name": governor_name,
        "governor_number": gov_number,
        "profile": {
            "translation": governor_info.get("translation", ""),
            "element": governor_info.get("element", ""),
            "aethyr": governor_info.get("aethyr", ""),
            "embodiment_date": governor_info.get("embodiment_date", ""),
            "essence": canonical_data.get("essence", ""),
            "angelic_role": canonical_data.get("angelic_role", ""),
            "traits": canonical_data.get("traits", []),
            "archetypal": {
                "tarot": archetypal.get("tarot", ""),
                "sephirot": archetypal.get("sephirot", ""),
                "zodiac_sign": archetypal.get("zodiac_sign", ""),
                "zodiac_angel": archetypal.get("zodiac_angel", ""),
                "numerology": archetypal.get("numerology", "")
            },
            "personality": {
                "motive_alignment": trait_choices.get("motive_alignment", ""),
                "self_regard": trait_choices.get("self_regard", ""),
                "role_archetype": trait_choices.get("role_archetype", ""),
                "polarity_cd": trait_choices.get("polarity_cd", ""),
                "orientation_io": trait_choices.get("orientation_io", ""),
                "virtues": trait_choices.get("virtues", []),
                "flaws": trait_choices.get("flaws", []),
                "baseline_tone": trait_choices.get("baseline_tone", ""),
                "baseline_approach": trait_choices.get("baseline_approach", ""),
                "affect_states": trait_choices.get("affect_states", {}),
                "relations": trait_choices.get("relations", [])
            }
        },
        "interview_date": datetime.now(timezone.utc).isoformat(),
        "confirmation": f"I am {governor_name}, and my essence awakens. I have accessed the sacred repositories and am ready to channel divine wisdom through the 127 gates of inquiry.",
        "blocks": {}
    }
    
    previous_responses = {}
    
    # Process each chunk
    for chunk_key, chunk_info in CHUNK_STRATEGY.items():
        logger.info(f"Processing {governor_name} - {chunk_key}: {chunk_info['title']} (Questions {chunk_info['question_range']})")
        
        try:
            # Extract questions for this chunk
            chunk_questions = extract_chunk_questions(questions_catalog_data, chunk_info["blocks"])
            
            if not chunk_questions:
                logger.warning(f"No questions found for chunk {chunk_key}")
                continue
            
            # Build prompt for this chunk
            prompt_messages = build_chunk_prompt(
                dossier=dossier,
                assignment_md=assignment_md,
                chunk_questions=chunk_questions,
                sources_md=sources_md,
                chunk_info=chunk_info,
                previous_responses=previous_responses if previous_responses else None
            )
            
            # Call API for this chunk
            logger.info(f"Calling Claude API for {chunk_key} ({len(chunk_questions)} blocks)")
            response_text = call_anthropic(prompt_messages)
            
            # Parse the response
            parsed_blocks = parse_chunk_response(response_text, chunk_questions)
            
            if not parsed_blocks:
                logger.error(f"Failed to parse response for {chunk_key}")
                continue
            
            # Verify completion
            expected_blocks = len(chunk_info["blocks"])
            actual_blocks = len(parsed_blocks)
            
            # Add parsed blocks to complete response
            for block_key, block_data in parsed_blocks.items():
                complete_response["blocks"][block_key] = block_data
                # Also add to previous_responses for continuity
                previous_responses[block_key] = block_data
            
            if actual_blocks == expected_blocks:
                logger.info(f"Successfully processed {chunk_key} - {actual_blocks} blocks completed")
            else:
                logger.warning(f"Partially processed {chunk_key} - {actual_blocks}/{expected_blocks} blocks completed")
            
            # Brief pause between chunks to respect rate limits
            time.sleep(3)
            
        except Exception as e:
            logger.error(f"Error processing chunk {chunk_key} for {governor_name}: {str(e)}")
            # Continue with next chunk rather than failing completely
            continue
    
    # Validate completeness
    total_questions = sum(len(block_data.get("questions", {})) for block_data in complete_response["blocks"].values())
    logger.info(f"Governor {governor_name} completed with {total_questions}/127 questions answered")
    
    return complete_response


def call_anthropic(messages: List[Dict[str, Any]]) -> str:
    """Wrapper for Anthropic Claude API with retry & backoff."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise EnvironmentError("ANTHROPIC_API_KEY not set in environment. Aborting.")

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Convert OpenAI-style messages to Anthropic format
    system_message = ""
    user_messages = []
    
    for msg in messages:
        if msg["role"] == "system":
            system_message = msg["content"]
        else:
            user_messages.append(msg)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=4096,
                temperature=0.8,
                system=system_message,
                messages=user_messages
            )
            # Extract text from response content
            if response.content and len(response.content) > 0:
                content_block = response.content[0]
                # Handle TextBlock which has a text attribute
                return getattr(content_block, 'text', str(content_block))
            return ""
        except anthropic.RateLimitError as e:  # type: ignore[attr-defined]
            retry_after = RETRY_BACKOFF * attempt
            logger.warning(
                "Anthropic rate limit (attempt %s). Sleeping %s seconds.", attempt, retry_after
            )
            time.sleep(retry_after)
        except Exception as err:  # pylint: disable=broad-except
            logger.error("Anthropic error (attempt %s): %s", attempt, err)
            if attempt == MAX_RETRIES:
                raise
            time.sleep(RETRY_BACKOFF * attempt)

    raise RuntimeError("Failed to get response from Anthropic after retries")


def process_governor(template_path: Path) -> None:
    """Process a single governor template into JSON output using chunked approach."""
    assignment_md = template_path.read_text(encoding="utf-8")
    gov_number = parse_governor_number(template_path.name)

    # Extract governor name from header: assumes pattern "# GOVERNOR #XX: NAME"
    name_match = re.search(r"#\s*GOVERNOR\s*#\d+:\s*([A-Z]+)", assignment_md)
    if not name_match:
        logger.error("Could not extract governor name from %s", template_path)
        return
    governor_name = name_match.group(1).strip()

    output_path = OUTPUT_DIR / f"{governor_name.upper()}.json"
    if output_path.exists():
        logger.info("Skipping %s (output already exists)", governor_name)
        return

    logger.info("Processing Governor #%s – %s (Chunked Approach)", gov_number, governor_name)

    # Load resources
    profiles_text = load_resource(LOCAL_GOVERNOR_PROFILE_PATH, REMOTE_GOVERNOR_PROFILE_URL)
    questions_catalog_text = load_resource(LOCAL_QUESTIONS_CATALOG_PATH, REMOTE_QUESTIONS_CATALOG_URL)
    sources_md = load_resource(LOCAL_CANON_SOURCES_PATH, REMOTE_CANON_SOURCES_URL)

    try:
        profiles_json = json.loads(profiles_text)
        questions_catalog_data = json.loads(questions_catalog_text)
        dossier = get_governor_dossier(profiles_json, gov_number)
    except Exception as err:  # pylint: disable=broad-except
        logger.error("Failed to parse resources for governor %s: %s", governor_name, err)
        return

    # Process governor through chunked approach
    try:
        complete_response = process_governor_chunked(
            dossier=dossier,
            assignment_md=assignment_md,
            questions_catalog_data=questions_catalog_data,
            sources_md=sources_md,
            governor_name=governor_name,
            gov_number=gov_number
        )
        
        # Save structured response
        save_structured_response(governor_name, complete_response)
        
        # Validation summary
        total_questions = sum(len(block_data.get("questions", {})) for block_data in complete_response["blocks"].values())
        logger.info("✅ Governor %s completed: %d/127 questions answered", governor_name, total_questions)
        
    except Exception as err:  # pylint: disable=broad-except
        logger.error("Failed to process governor %s: %s", governor_name, err)
        return


# -----------------------
# Main Entrypoint
# -----------------------

def main() -> None:  # noqa: D401
    """CLI entrypoint."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate governor JSON files")
    parser.add_argument("--governor", help="Process only the specified governor (e.g., DIALOIA)", type=str)
    parser.add_argument("--range", nargs=2, metavar=('START', 'END'), type=int, 
                       help="Process governors in range (e.g., --range 7 91)")
    args = parser.parse_args()
    
    templates = sorted(TEMPLATES_DIR.glob("governor_*_assignment_prompt.md"), key=lambda p: parse_governor_number(p.name))

    if not templates:
        logger.error("No governor templates found in %s", TEMPLATES_DIR)
        sys.exit(1)

    # Filter templates if specific governor requested
    if args.governor:
        target_governor = args.governor.upper()
        filtered_templates = []
        for template in templates:
            assignment_md = template.read_text(encoding="utf-8")
            name_match = re.search(r"#\s*GOVERNOR\s*#\d+:\s*([A-Z]+)", assignment_md)
            if name_match and name_match.group(1).strip() == target_governor:
                filtered_templates.append(template)
                break
        
        if not filtered_templates:
            logger.error("Governor %s not found in templates", target_governor)
            sys.exit(1)
        
        templates = filtered_templates
        logger.info("Processing single governor: %s", target_governor)
    
    # Filter templates if range specified
    elif args.range:
        start_num, end_num = args.range
        if start_num > end_num:
            logger.error("Start number (%d) must be less than or equal to end number (%d)", start_num, end_num)
            sys.exit(1)
        
        filtered_templates = []
        for template in templates:
            gov_number = parse_governor_number(template.name)
            if start_num <= gov_number <= end_num:
                filtered_templates.append(template)
        
        if not filtered_templates:
            logger.error("No governors found in range %d-%d", start_num, end_num)
            sys.exit(1)
        
        templates = filtered_templates
        logger.info("Processing governor range: %d-%d (%d governors)", start_num, end_num, len(templates))

    for template in templates:
        try:
            process_governor(template)
        except KeyboardInterrupt:  # pragma: no cover
            logger.warning("Interrupted by user. Exiting.")
            sys.exit(130)
        except Exception as err:  # pylint: disable=broad-except
            logger.exception("Unhandled error processing %s: %s", template, err)
            # Continue with next governor rather than abort.
            continue

    if args.governor:
        logger.info("Governor %s processing completed.", args.governor.upper())
    elif args.range:
        logger.info("Governor range %d-%d processing completed.", args.range[0], args.range[1])
    else:
        logger.info("All governors processed.")


if __name__ == "__main__":
    main()