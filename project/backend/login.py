import jwt
from datetime import datetime, timedelta

# 定义密钥
key = 'lSbCWJdg-73rjKfV5ZijV0dyxZXnH-Ev3eVgkkZbab9xelhTlExdnBKDD1d6F9C_ZkvyV3tOg1tcD27iKZ4WD2Xy6vvUvNj6fxtbcgKOQnW2G5l2aJ69EegXE6RG9yc6EjKX69361t8pZ76MWFQ3BNt-X-6ZqQRJgrzDGD5pTMXHaZceuIIA3blVtBIylKmowt2ug6ieKTMk6CEzdDetBDSeGnXc8vgNQa3TzSvYW4wRVmCIYVby_qKUQqqAnWw1RtrtnLNrp0cJHiCf05g7eRttc4xHA0u4GnhlJEuEVQSr_7DC3tEMcrdH30l_PqO6FHs8DoEn6LrFCsG1oSza2w'

def create_token(username):
    payload = {
        'exp': datetime.now() + timedelta(days=7),  # token的过期时间
        'username': username
    }

    return jwt.encode(payload, key, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return False
    return payload['username']
