from jose import JWTError, jwt
from datetime import datetime, timedelta

# Chave utilizada para assinatura dos tokens JWT
SECRET_KEY = "biblioteca_tde_2025"

# Algoritmo de criptografia utilizado
ALGORITHM = "HS256"

# Tempo de expiração do token em minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """
    Gera um token JWT contendo os dados do usuário
    e uma data de expiração.
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(token: str):
    """
    Valida o token recebido pelo cliente.
    Retorna o payload caso o token seja válido.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None