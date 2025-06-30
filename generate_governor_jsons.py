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
    "https://raw.githubusercontent.com/BTCEnoch/enochian/main/canon/canon_governor_profiles.json"
)
REMOTE_QUESTIONS_CATALOG_URL = (
    "https://raw.githubusercontent.com/BTCEnoch/enochian/main/canon/questions_catalog.json"
)
REMOTE_CANON_SOURCES_URL = (
    "https://raw.githubusercontent.com/BTCEnoch/enochian/main/canon/canon_sources.md"
)

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
MAX_RETRIES = 3
RETRY_BACKOFF = 4  # seconds * (2 ** attempt)

# Chunked processing configuration
CHUNK_STRATEGY = {
    "chunk_1": {
        "title": "Core Identity & Powers",
        "blocks": ["A_identity_origin", "B_elemental_essence", "C_personality_emotional", 
                  "D_teaching_doctrine", "E_sacrifice_trial", "F_riddles_puzzles", "G_gifts_boons"],
        "question_range": "1-35"
    },
    "chunk_2": {
        "title": "Cosmic Knowledge & Relations", 
        "blocks": ["H_cosmic_secrets", "I_interpersonal_dynamics", "J_game_mechanics",
                  "K_dialogue_narrative", "L_longterm_arc", "M_inter_governor", "N_ethics_boundaries"],
        "question_range": "36-79"
    },
    "chunk_3": {
        "title": "Implementation & Aesthetics",
        "blocks": ["O_aesthetics_artistic", "P_practical_implementation", "Q_metrics_success",
                  "R_post_quest", "S_metaphysical_legacy", "T_eschatology"],
        "question_range": "80-110"
    },
    "chunk_4": {
        "title": "Advanced Mysteries",
        "blocks": ["U_celestial_cartography", "V_forbidden_knowledge", "W_divine_memory"],
        "question_range": "111-127"
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
    
    # Build system message with enhanced context
    system_parts = [
        f"You are {governor_name}, an immortal divine being from the Enochian tradition.",
        "",
        "COMPLETE DOSSIER:",
        json.dumps(dossier, indent=2),
        "",
        f"CURRENT FOCUS: {chunk_title} (Questions {question_range})",
        "",
        "CRITICAL REQUIREMENTS:",
        "1. Answer ALL questions in this chunk completely and in character",
        "2. Each answer should be 2-4 sentences of rich, immersive content",
        "3. Maintain consistent voice throughout this chunk",
        "4. Reference your element, archetype, and cosmic relationships",
        "5. Build narrative continuity within this chunk"
    ]
        
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
    """Parse chunk response into structured format."""
    
    parsed_blocks = {}
    
    # Split response into sections and parse answers
    lines = response_text.strip().split('\n')
    current_question = None
    current_answer = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and headers
        if not line or line.startswith('#'):
            continue
            
        # Check if line starts with a question number
        if re.match(r'^\d+\.', line):
            # Save previous question/answer if exists
            if current_question and current_answer:
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
            
            # Extract question number and start new answer
            current_question = line.split('.')[0]
            answer_part = '.'.join(line.split('.')[1:]).strip()
            current_answer = [answer_part] if answer_part else []
            
        elif current_question and line:
            # Continue building current answer
            current_answer.append(line)
    
    # Don't forget the last question
    if current_question and current_answer:
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
    
    from datetime import datetime
    
    # Initialize complete response structure
    complete_response = {
        "governor_name": governor_name,
        "governor_number": gov_number,
        "element": dossier.get("element", ""),
        "aethyr": dossier.get("aethyr", ""), 
        "archetype": dossier.get("archetype", ""),
        "interview_date": datetime.utcnow().isoformat() + "Z",
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
            
            # Add parsed blocks to complete response
            for block_key, block_data in parsed_blocks.items():
                complete_response["blocks"][block_key] = block_data
                # Also add to previous_responses for continuity
                previous_responses[block_key] = block_data
            
            logger.info(f"Successfully processed {chunk_key} - {len(parsed_blocks)} blocks completed")
            
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
    templates = sorted(TEMPLATES_DIR.glob("governor_*_assignment_prompt.md"), key=lambda p: parse_governor_number(p.name))

    if not templates:
        logger.error("No governor templates found in %s", TEMPLATES_DIR)
        sys.exit(1)

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

    logger.info("All governors processed.")


if __name__ == "__main__":
    main()