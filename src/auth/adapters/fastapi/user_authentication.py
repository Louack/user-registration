from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.auth.core.use_cases.user_authentication import UserAuthentication
from src.builders.use_cases_builders import get_user_auth_use_case

basic_auth = HTTPBasic()


async def authenticate_user(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
    use_case: UserAuthentication = Depends(get_user_auth_use_case),
):
    user = use_case.execute(email=credentials.username, password=credentials.password)
    return user
