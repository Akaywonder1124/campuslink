from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api_v1"
    SECRET_KEY = ''
    ACCESS_TOKEN_EXPIRE_MINUTES  :int = 40
    MEMBER = "member"
    ADMIN_ROLE = "admin"
    CREATOR_ROLE = "creator"
    INTEREST_ADMIN_ROLE = "interest_admin"

    class Config:
        case_sensitive = True

settings = Settings()
