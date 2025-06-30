from __future__ import annotations

import json
import logging
import logging.handlers
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List

import requests

try:
    import openai  # type: ignore
except ImportError as exc:  # pragma: no cover
    # Provide a graceful message so the user remembers to install packages.
    raise SystemExit("openai package not found. Please run `pip install -r requirements.txt` before executing.") from exc

# -----------------------
# Constants & Config
# -----------------------
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "governor_interview_templates"
OUTPUT_DIR = BASE_DIR / "governor_output"
LOG_DIR = BASE_DIR / "logs"
CACHE_DIR = Path("/tmp/governor_cache")

GOVERNOR_PROFILE_URL = (
    "https://raw.githubusercontent.com/BTCEnoch/enochian/main/canon/canon_governor_profiles.json"
)
QUESTIONS_CATALOG_URL = (
    "https://raw.githubusercontent.com/BTCEnoch/enochian/main/canon/questions_catalog.json"
)
CANON_SOURCES_URL = (
    "https://raw.githubusercontent.com/BTCEnoch/enochian/main/canon/canon_sources.md"
)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MAX_RETRIES = 3
RETRY_BACKOFF = 4  # seconds * (2 ** attempt)

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
    for profile in all_profiles[
        "governors"
    ]:  # assuming JSON is of shape {"governors": [ {...}, ... ]}
        if int(profile.get("number")) == gov_number:
            return profile
    raise KeyError(f"Governor number {gov_number} not found in profiles JSON")


def build_prompt(
    dossier: Dict, assignment_md: str, questions_catalog: str, sources_md: str
) -> List[Dict[str, str]]:
    """Construct messages list for OpenAI ChatCompletion call."""
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


# -----------------------
# Core Logic
# -----------------------

def save_response(governor_name: str, response_text: str) -> None:
    output_path = OUTPUT_DIR / f"{governor_name.upper()}.json"
    output_path.write_text(response_text, encoding="utf-8")
    logger.info("Saved output to %s", output_path)


def call_openai(messages: List[Dict[str, str]]) -> str:
    """Wrapper for OpenAI ChatCompletion with retry & backoff."""
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY not set in environment. Aborting.")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            chat_completion = openai.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.8,
                max_tokens=4096,
            )
            return chat_completion.choices[0].message.content  # type: ignore[attr-defined]
        except openai.RateLimitError as e:  # type: ignore[attr-defined]
            retry_after = int(e.headers.get("Retry-After", RETRY_BACKOFF * attempt))
            logger.warning(
                "OpenAI rate limit (attempt %s). Sleeping %s seconds.", attempt, retry_after
            )
            time.sleep(retry_after)
        except Exception as err:  # pylint: disable=broad-except
            logger.error("OpenAI error (attempt %s): %s", attempt, err)
            if attempt == MAX_RETRIES:
                raise
            time.sleep(RETRY_BACKOFF * attempt)

    raise RuntimeError("Failed to get response from OpenAI after retries")


def process_governor(template_path: Path) -> None:
    """Process a single governor template into JSON output."""
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

    logger.info("Processing Governor #%s – %s", gov_number, governor_name)

    profiles_text = download_file(GOVERNOR_PROFILE_URL)
    questions_catalog = download_file(QUESTIONS_CATALOG_URL)
    sources_md = download_file(CANON_SOURCES_URL)

    try:
        profiles_json = json.loads(profiles_text)
        dossier = get_governor_dossier(profiles_json, gov_number)
    except Exception as err:  # pylint: disable=broad-except
        logger.error("Failed to parse dossier for governor %s: %s", governor_name, err)
        return

    prompt_messages = build_prompt(dossier, assignment_md, questions_catalog, sources_md)

    response_text = call_openai(prompt_messages)

    save_response(governor_name, response_text)


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