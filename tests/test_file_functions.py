from pathlib import Path
import os
import pytest

from scripts.file_functions import (
    get_character_name,
    move_to_used,
    number_of_gifs,
    read_dictionary,
    read_group_uris,
    update_dictionary,
    read_edition,
    update_edition,
    update_group_uris,
)
from scripts.helpful_scripts import is_local, is_mainnet


def test_get_character_name():
    (raw_character_name, full_file_path) = get_character_name(0)

    assert raw_character_name == "Ininor_Bobern"
    assert full_file_path == "./img/gif/Ininor_Bobern.gif"


def test_read_dictionary():
    assert isinstance(read_dictionary(), list)


def test_update_dictionary():
    original_dict = read_dictionary()
    update_dictionary(["expected"])
    new_dict = read_dictionary()
    assert new_dict[0] == "expected"

    update_dictionary(original_dict)


def test_get_edition():
    EXPECTED_EDITION = read_edition()

    edition = read_edition()
    assert edition == EXPECTED_EDITION

    update_edition(edition + 1)
    edition = read_edition()
    assert edition == EXPECTED_EDITION + 1

    edition = update_edition(EXPECTED_EDITION)
    edition = read_edition()
    assert edition == EXPECTED_EDITION


def test_num_gifs():
    EXPECTED = 714
    assert number_of_gifs() == EXPECTED


def test_move_to_used():
    if not is_mainnet():
        pytest.skip()
    raw_character_name = "Abbus_Nykama"
    move_to_used(raw_character_name)

    assert Path(f"./img/used_gifs/{raw_character_name}.gif").is_file()

    # Undo
    old_path = f"./img/used_gifs/{raw_character_name}.gif"
    new_path = f"./img/gif/{raw_character_name}.gif"
    os.rename(old_path, new_path)


def test_update_group_uris():
    expected_cid = "EXPECTED"
    update_group_uris(-1, expected_cid)
    given_cid = read_group_uris().get("-1")
    assert expected_cid == given_cid

    # Reset
    update_group_uris(-1, None)
