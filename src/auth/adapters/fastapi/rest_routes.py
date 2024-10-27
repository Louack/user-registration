from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.adapters.fastapi.schemas import (
    ActivationCodeSchema,
    UserCreationSchema,
    UserSchema,
)
from src.auth.adapters.fastapi.user_authentication import authenticate_user
from src.auth.core.domain.user import User
from src.auth.core.use_cases.user_activation import UserActivation
from src.auth.core.use_cases.user_registration import UserRegistration
from src.builders.use_cases_builders import (
    get_user_activation_use_case,
    get_user_registration_use_case,
)
from src.fastapi_exceptions_handlers import APIErrorMessage

router = APIRouter()


@router.post(
    path="/auth/registration",
    response_model=UserSchema,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
)
async def register_user(
    request_data: UserCreationSchema,
    use_case: UserRegistration = Depends(get_user_registration_use_case),
) -> JSONResponse:
    user = use_case.execute(email=request_data.email, password=request_data.password)
    response_data = UserSchema(email=user.email, is_active=user.is_active)
    return JSONResponse(
        content=response_data.model_dump(), status_code=status.HTTP_201_CREATED
    )


@router.post(
    path="/auth/activation",
    response_model=UserSchema,
    responses={
        400: {"model": APIErrorMessage},
        404: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
async def activate_user(
    request_data: ActivationCodeSchema,
    user: User = Depends(authenticate_user),
    use_case: UserActivation = Depends(get_user_activation_use_case),
) -> JSONResponse:
    activated_user = use_case.execute(user=user, code=request_data.code)
    response_data = UserSchema(
        email=activated_user.email, is_active=activated_user.is_active
    )
    return JSONResponse(
        content=response_data.model_dump(), status_code=status.HTTP_200_OK
    )
