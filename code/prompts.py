
from pathlib import Path


# Find the main project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Map each prompt version to its text file
PROMPT_FILES = {
    "V1 - Basic": PROJECT_DIR / "prompts" / "v1" / "basic_prompt.txt",
    "V2 - Improved": PROJECT_DIR / "prompts" / "v2" / "improved_prompt.txt",
    "V3 - Advanced": PROJECT_DIR / "prompts" / "v3" / "advanced_prompt.txt",
}


def generate_prompt(claim, evidence, sources, version):
    """Load a prompt template and insert the user's information."""

    if version not in PROMPT_FILES:
        raise ValueError("Invalid prompt version selected.")

    prompt_path = PROMPT_FILES[version]

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    template = prompt_path.read_text(encoding="utf-8")

    prompt = (
        template
        .replace("{claim}", claim)
        .replace("{evidence}", evidence)
        .replace("{sources}", sources or "Not provided")
    )

    return prompt
