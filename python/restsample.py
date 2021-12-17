from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# Para ler as chaves:
from cryptography.hazmat.primitives import serialization

import datetime

app = Flask(__name__)

# Primeiro gere as chaves usando o OpenSSH:
# Mkdir .ssh / cd .ssh
# ssh-keygen -t rsa

# Lendo a PRIVATE_KEY para assinar token:

private_key = open('.ssh/cleuton', 'r').read()
prKey = serialization.load_ssh_private_key(private_key.encode(), password=b'teste')

# Lendo a PUBLIC_KEY para verificar token:

public_key = open('.ssh/cleuton.pub', 'r').read()
pubKey = serialization.load_ssh_public_key(public_key.encode())

app.config["JWT_PRIVATE_KEY"] = prKey
app.config["JWT_PUBLIC_KEY"] = pubKey
app.config['JWT_ALGORITHM'] = 'RS256'

# Esse será o intervalo de tempo de expiração do token:

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=1)

jwt = JWTManager(app)


# Esta rota é para o usuário se autenticar.
# Se o token expirar, ele terá que logar novamente.
# Você pode estabeler mecanismo de refresh automático do token.

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Username ou senha incorretos"}), 401
        # Você precisa proteger contra ataque de força bruta.
        # Pode contar quantas vezes um usuário tentou logar com erro.
        # e/ou pode enviar um CAPTCHA a ele.

    access_token = create_access_token(identity=username)

    # O default é retornar o token no corpo do request. 
    # O cliente tem que enviar um header "Authorization: Bearer <token>"

    return jsonify(access_token=access_token)


# O decorator @jwt_required protege a rota contra acesso anônimo.

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    
    # Pega a identidade do usuário logado: 

    current_user = get_jwt_identity()
    return jsonify(logado=current_user), 200


if __name__ == "__main__":
    app.run()