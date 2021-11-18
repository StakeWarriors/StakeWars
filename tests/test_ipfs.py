from scripts.ipfs_functions import get_ipfs_dir


def test_get_ipfs_dir():
    x = get_ipfs_dir()
    assert len(x) > 0
