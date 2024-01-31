import hashlib


async def hash_of_sha256(plain_text: str):
    plain_text = plain_text.encode()
    hash_of_text = hashlib.sha256(plain_text)
    return hash_of_text.hexdigest()
