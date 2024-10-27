from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

from src.auth.exceptions import BadCredentials, InvalidCode, UserAlreadyExists


class APIErrorMessage(BaseModel):
    type: str
    message: str


async def bad_credentials_handler(
    request: Request, exc: BadCredentials
) -> JSONResponse:
    error_msg = APIErrorMessage(
        type="bad_credentials", message="Unable to log with the provided credentials."
    )
    return JSONResponse(status_code=401, content=error_msg.model_dump())


async def user_already_exists_handler(
    request: Request, exc: UserAlreadyExists
) -> JSONResponse:
    error_msg = APIErrorMessage(
        type="wrong_email", message="This email cannot be used."
    )
    return JSONResponse(status_code=400, content=error_msg.model_dump())


async def invalid_code_handler(request: Request, exc: InvalidCode) -> JSONResponse:
    error_msg = APIErrorMessage(
        type="invalid_code", message="Invalid or expired activation code."
    )
    return JSONResponse(status_code=400, content=error_msg.model_dump())


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    error_msg = APIErrorMessage(
        type="internal_server_error", message="An error occurred on the server."
    )
    return JSONResponse(status_code=500, content=error_msg.model_dump())


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(BadCredentials, bad_credentials_handler)
    app.add_exception_handler(UserAlreadyExists, user_already_exists_handler)
    app.add_exception_handler(InvalidCode, invalid_code_handler)
    # generic_error_handler always to be placed at the very end
    app.add_exception_handler(Exception, generic_error_handler)
