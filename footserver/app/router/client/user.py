from fastapi import APIRouter

from app.models.user import *
from app.service.client.user_service import UserService

router = APIRouter(prefix="/users")


@router.post(path="/login")
async def login(body: FormLoginByClient):
    """
    `로그인 API`

    Args:
    - **id**: 회원 아이디
    - **password**: 회원 비밀번호
    """

    return UserService.login(body=body)
