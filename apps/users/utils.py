import random
import string

def generate_verification_code(length=4):
    code = ''.join(random.choices(string.digits, k=length))
    return code
