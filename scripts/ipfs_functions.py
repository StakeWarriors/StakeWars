from brownie import network
import ipfshttpclient

from scripts.helpful_scripts import is_local


def upload_to_ipfs_client(edition, public_token_uri, file_to_upload):
    path_uri = f"/{network.show_active()}/ed.{edition}/{public_token_uri}"
    full_uri = None

    if is_local():
        return (
            path_uri,
            f"file://{network.show_active}/{path_uri}/?filename={public_token_uri}",
        )
    print(file_to_upload)
    print(path_uri)
    with ipfshttpclient.connect() as client:
        client.files.write(path_uri, open(file_to_upload, "rb"), create=True)
        filehash = client.files.stat(path_uri)["Hash"]
        full_uri = f"https://ipfs.io/ipfs/{filehash}/?filename={public_token_uri}"
    return (path_uri, full_uri)
