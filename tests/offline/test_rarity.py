import json
from scripts.file_functions import update_prompts


def test_used_prompts():

    update_prompts("Fake Prompt", test_mode=True)
    filepath = f"./metadata/TEST_used_prompts.json"

    with open(filepath, "r") as file:
        js = json.load(file)
        assert js[0] == "Fake Prompt"

    with open(filepath, "w") as file:
        json.dump([], file)
