# Primeiro gere as chaves usando o OpenSSH:
# Mkdir .ssh / cd .ssh
# ssh-keygen -t rsa
# pip install -r requirements.txt

import datetime
from datetime import timezone

# first import the module
from cryptography.hazmat.primitives import serialization

import jwt
from jwt import InvalidSignatureError

payload_data = {
    "sub": "cleuton"
}

# Carrega a chave privada que geramos
# Ela tem um passphrase que passei no argumento "password"
private_key = open('.ssh/cleuton', 'r').read()
key = serialization.load_ssh_private_key(private_key.encode(), password=b'teste')

new_token = jwt.encode(
    payload=payload_data,
    key=key,
    algorithm='RS256'
)

print(new_token)

# Verificando a assinatura: 

public_key = open('.ssh/cleuton.pub', 'r').read()
pubKey = serialization.load_ssh_public_key(public_key.encode())

print(jwt.decode(jwt=new_token, key=public_key, algorithms=['RS256', ]))

# Falsificando o token: 

fake_token = new_token.replace('XA','X0')

try:
    print(jwt.decode(jwt=fake_token, key=public_key, algorithms=['RS256', ]))
except InvalidSignatureError as e:
    print(e)

# Criando um token com expiration date: 

futura = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=30)

payload_data = {
    "sub": "cleuton",
    "exp": futura
}

token_exp = jwt.encode(
    payload=payload_data,
    key=key,
    algorithm='RS256'
)

print(jwt.decode(jwt=token_exp, key=public_key, algorithms=['RS256', ]))
print("python verifica.py " + token_exp)
