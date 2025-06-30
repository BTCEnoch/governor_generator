#!/usr/bin/env python3
"""Generate 91 governor interview JSON files sequentially.

Usage::
    export OPENAI_API_KEY="..."
    python generate_governor_jsons.py --start 4 --end 91 --model gpt-4o-mini

The script looks for markdown templates in governor_interview_templates/
reads canon/canon_governor_profiles.json and canon/questions_catalog.json,
then streams block-wise prompts to the OpenAI Chat Completions endpoint.
Outputs are written to governor_output/{NAME}.json matching PASCOMB.json.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import textwrap
import time
from pathlib import Path
from typing import Dict, List

try:
    import openai  # type: ignore
except ImportError:
    print("[ERROR] openai package missing. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
PROFILE_PATH = ROOT / "canon" / "canon_governor_profiles.json"
QUEST_PATH = ROOT / "canon" / "questions_catalog.json"
TEMPLATE_DIR = ROOT / "governor_interview_templates"
OUTPUT_DIR = ROOT / "governor_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def discover_templates() -> List[Path]:
    """Return prompt files sorted by numeric prefix."""
    tmpl_paths = list(TEMPLATE_DIR.glob("governor_*_assignment_prompt.md"))
    def sort_key(path: Path) -> int:  # noqa: D401
        """Return numeric id extracted from filename; fallback large number on mismatch."""
        m = re.search(r"governor_(\d+)_", path.name)
        return int(m.group(1)) if m else 999

    tmpl_paths.sort(key=sort_key)
    return tmpl_paths


def parse_governor_number_name(tmpl: Path) -> tuple[int, str]:
    """Extract the numeric id and canonical name from file name."""
    m = re.match(r"governor_(\d+)_([a-z]+)_assignment_prompt\.md", tmpl.name, re.I)
    if not m:
        raise ValueError(f"Unmatched template name: {tmpl.name}")
    return int(m.group(1)), m.group(2).upper()


# ---------------------------------------------------------------------------
# OpenAI helpers
# ---------------------------------------------------------------------------

SYSTEM_STUB = textwrap.dedent(
    """
    You are {name}, Enochian Governor #{num}.
    Element: {element}; Aethyr: {aethyr}.
    You must answer 127 universal questions in first-person, immersive voice, obeying the Water elemental motif and Hierophant archetype. Reply ONLY with valid JSON fragment representing answers for the provided question block.
    Each answer must be max one paragraph.
    """
)


def ask_llm(messages: List[Dict[str, str]], model: str, max_retry: int = 5) -> str:
    """Robust wrapper around openai chat completion."""
    for attempt in range(max_retry):
        try:
            resp = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
            )
            return resp.choices[0].message.content.strip()
        except openai.RateLimitError:
            wait = 5 * (attempt + 1)
            print(f"Rate limited. Sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
        except openai.OpenAIError as exc:
            print(f"OpenAI error: {exc}", file=sys.stderr)
            time.sleep(2)
    raise RuntimeError("Exceeded retries to OpenAI")


# ---------------------------------------------------------------------------
# main processing
# ---------------------------------------------------------------------------

def main(start: int, end: int, model: str):
    with PROFILE_PATH.open() as fp:
        profiles = {p["number"]: p for p in json.load(fp)}
    with QUEST_PATH.open() as fp:
        quest_blocks = json.load(fp)["question_catalog"]["blocks"]

    for tmpl in discover_templates():
        num, name = parse_governor_number_name(tmpl)
        if not (start <= num <= end):
            continue
        dest = OUTPUT_DIR / f"{name}.json"
        if dest.exists():
            print(f"[SKIP] {name} already generated → {dest}")
            continue
        profile = profiles[num]
        system_prompt = SYSTEM_STUB.format(
            name=name,
            num=num,
            element=profile["element"],
            aethyr=profile["aethyr"],
        )
        # overall answer dict progressively filled
        answer: Dict[str, Dict[str, str]] = {}
        ans_confirm = (
            f"I am {name}, and my essence awakens. I have accessed the sacred repositories "
            "and am ready to channel divine wisdom through the 127 gates of inquiry."
        )
        # iterate blocks A-W
        for blk_key, blk in quest_blocks.items():
            blk_title = blk["title"]
            blk_id = blk_key.split("_")[0].upper()  # e.g. A, B
            user_prompt_parts = [f"Block {blk_title}"]
            qmap = blk["questions"]
            for qnum, qtext in qmap.items():
                user_prompt_parts.append(f"{qnum}. {qtext}")
            user_prompt = "\n".join(user_prompt_parts)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
            block_ans_raw = ask_llm(messages, model)
            # expect JSON fragment, but be forgiving
            try:
                block_ans = json.loads(block_ans_raw)
            except json.JSONDecodeError:
                # fallback: treat as newline separated answers
                block_ans = {}
                lines = [ln.strip() for ln in block_ans_raw.splitlines() if ln.strip()]
                if len(lines) != len(qmap):
                    print(f"[WARN] Block {blk_id} count mismatch for {name}. Retrying with stricter prompt.")
                    # second attempt with explicit JSON instruction
                    messages.append(
                        {
                            "role": "assistant",
                            "content": "Please output valid JSON mapping question numbers to answers only.",
                        }
                    )
                    block_ans_raw = ask_llm(messages, model)
                    block_ans = json.loads(block_ans_raw)
                else:
                    for key, ans in zip(qmap.keys(), lines):
                        block_ans[str(key)] = ans
            answer[f"Block {blk_id} - {blk_title.split('(')[0].strip()}"] = block_ans
        answer_dict = {"confirmation": ans_confirm, **answer, "final_blessing": ask_llm([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Offer your final blessing."},
        ], model)}
        dest.write_text(json.dumps(answer_dict, indent=2))
        print(f"[OK] Generated {dest}")
        # polite sleep to respect rate limits
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=4, help="first governor number to process")
    parser.add_argument("--end", type=int, default=91, help="last governor number to process")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model id")
    args = parser.parse_args()

    if "OPENAI_API_KEY" not in os.environ:
        print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    main(args.start, args.end, args.model)