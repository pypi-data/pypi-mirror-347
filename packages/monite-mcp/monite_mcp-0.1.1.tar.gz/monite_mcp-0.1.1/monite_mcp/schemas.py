from pydantic import BaseModel


class MoniteAuthToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
