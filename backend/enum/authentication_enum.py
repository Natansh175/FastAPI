from enum import Enum


class AuthenticationEnum(str, Enum):
    ENCODING = "utf-8"
    HASH_ALGORITHM = "HS256"
    ACCESSTOKEN = "accesstoken"
    REFRESHTOKEN = "refreshtoken"
    ADMIN_ROLE = "admin"
    USER_ROLE = "user"
    ACCESS_TOKEN_MAX_AGE = 300000
    REFRESH_TOKEN_MAX_AGE = 86400000
    ACCESS_TOKEN_EXP = 5
    REFRESH_TOKEN_EXP = 24
