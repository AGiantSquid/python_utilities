import base64
import hashlib


def get_aws_hash(zip_file):
    '''Compute bash64 sha256 hash of zip archive, with aws algorithm.

    This can be used to determine if a local zip is the same as a remote zip in aws.'''
    with open(zip_file, "rb") as f:
        sha256_hash = hashlib.sha256()

        # Read and update hash string value in blocks of 4K
        while byte_block := f.read(4096):
            sha256_hash.update(byte_block)

    hash_value = base64.b64encode(sha256_hash.digest()).decode('utf-8')

    return hash_value
