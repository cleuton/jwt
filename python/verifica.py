import datetime
from datetime import timezone
import sys

# first import the module
from cryptography.hazmat.primitives import serialization

import jwt
from jwt import ExpiredSignatureError

token = sys.argv[1]

public_key = open('.ssh/cleuton.pub', 'r').read()
pubKey = serialization.load_ssh_public_key(public_key.encode())

try:
    print(jwt.decode(jwt=token, key=public_key, algorithms=['RS256', ]))
except ExpiredSignatureError as e:
    print(e)
