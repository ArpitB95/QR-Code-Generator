import bcrypt
import uuid

# example password
password = "passwordabc"

print(uuid.uuid4().hex)
# converting password to array of bytes
bytes = password.encode("utf-8")

# generating the salt
salt = b"$2b$12$tii0QHwvxAEWKUHrLtZSku"
print(salt)
# Hashing the password
hash = bcrypt.hashpw(bytes, salt)
print(hash.decode())
# Taking user entered password
userPassword = "passwordabc"

# encoding user password
userBytes = userPassword.encode("utf-8")

# checking password
result = bcrypt.checkpw(userBytes, hash)

print(result)
