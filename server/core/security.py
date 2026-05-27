from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(*,plain_password:str):
    return password_hash.hash(password=plain_password)

def verify_password(*,plain_password:str, hash:str):
    return password_hash.verify(password=plain_password, hash=hash)
