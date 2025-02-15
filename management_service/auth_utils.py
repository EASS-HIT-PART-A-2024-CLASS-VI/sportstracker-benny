# auth_utils.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt


SECRET_KEY = "b6c2d2a03a400f1729c9b9e892ecd2e292ef1fbed2cb187391e13d564212c24007304114f65ff10aade32e03f2a9ac1e7a80d744660e32293e442ea991de1b09b2eb9b7d7621ff9e3da116fcd9a277278b17dbbc95dfefe50ea4c4ebd72c9c8928fa4a179390051ed8830eee9645e779d3bd3afa192d8100ff43799001dbd596a2844cc6dd82e61e0eaba93d5fbfa25c757ad22b31443ebfcb29a715ec93016bbfb5985e939c95078dd668a79c3845e7ad2526265c805847ecebe173847c70d3ee250788fd10dc986795609f91b73f9030d7aca46f31f924e1428227fa45dd9def3fa7ebc14d878de9d0590b19d560dd3a7f1cb685d9e60dc4adebd0f85388c0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)