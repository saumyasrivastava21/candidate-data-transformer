from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "inputs"
CONFIG_DIR = DATA_DIR / "configs"
OUTPUT_DIR = DATA_DIR / "outputs"

DEFAULT_OUTPUT_PATH = OUTPUT_DIR / "canonical_profile.json"
CUSTOM_OUTPUT_PATH = OUTPUT_DIR / "custom_profile.json"