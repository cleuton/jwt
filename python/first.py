import jwt
from jwt import InvalidSignatureError

payload = {
    "sub": "cleuton"
}

senha_simetrica = 'senha-secreta!!'

token = jwt.encode(
    payload=payload,
    key=senha_simetrica
)

print(token)

# Copiar e verificar com jwt.io. Passar seu segredo no campo para validar a assinatura.

# Verificando a assinatura

print(jwt.decode(token, key=senha_simetrica, algorithms=['HS256', ]))

# InvalidSignatureError 

fake_token=token.replace('XA','X0')

print(fake_token)

try:
    print(jwt.decode(fake_token, key=senha_simetrica, algorithms=['HS256', ]))
except InvalidSignatureError as e:
    print(e)
