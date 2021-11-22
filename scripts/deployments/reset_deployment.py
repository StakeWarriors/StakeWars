from scripts.file_functions import (
    clean_directory,
    move_used_img_back,
    update_archived_tokens,
    update_dictionary,
    update_edition,
)


def reset():
    clean_directory()
    update_dictionary([])
    update_archived_tokens([])
    update_edition(0)
    move_used_img_back()


def main():
    reset()
