from passlib.context import CryptContext
import logging
from .filter_attribute import BcryptWarningFilter
    
logging.basicConfig(level=logging.INFO)
logger = logging.Logger("bcrypt")
logger.setLevel(logging.INFO)
logger.addFilter(BcryptWarningFilter())

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


