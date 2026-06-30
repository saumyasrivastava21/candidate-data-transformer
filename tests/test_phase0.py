from app.settings import INPUT_DIR, CONFIG_DIR, OUTPUT_DIR


def test_directories_exist():
    assert INPUT_DIR.exists()
    assert CONFIG_DIR.exists()
    assert OUTPUT_DIR.exists()


def test_sample_inputs_exist():
    assert (INPUT_DIR / "recruiter.csv").exists()
    assert (INPUT_DIR / "ats.json").exists()
    assert (INPUT_DIR / "notes.txt").exists()


def test_custom_config_exists():
    assert (CONFIG_DIR / "custom_config.json").exists()