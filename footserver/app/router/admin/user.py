from fastapi import APIRouter

from app.models.user import *
from app.service.admin.user_service import UserService

router = APIRouter(prefix="/users")

@router.post(path="/login")
async def login(body: FormLoginByAdmin):
    """
    `관리자 로그인 API`

    Args:
    - **id**: 회원 아이디
    - **password**: 회원 이름
    """

    return UserService.login(body=body)


@router.post(path="")
async def create_user(body: FormUser):
    """
    `회원등록 API`

    Args:
    - **uid**: 회원 아이디
    - **name**: 회원 이름
    - **email**: 회원 이메일
    - **password**: 회원 비밀번호
    - **password_re**: 비밀번호 확인
    - **phone**: 회원 전화번호
    """

    return UserService.create(body=body)


@router.put(path="")
async def update_user(body: FormUser):
    """
    `회원수정 API`

    Args:
    - **user_id**: 회원 아이디
    - **user_name**: 회원 이름
    - **email**: 회원 이메일
    - **password**: 회원 비밀번호
    - **gender**: 회원 성별
    - **birth**: 회원 생년월일
    - **affiliation**:
    - **finish_pretest1**:
    - **finish_survey1**:
    - **finish_test_anxiety**:
    - **finish_pretest2**:
    - **finish_survey2**:
    - **fcm_token**: 회원 푸시토큰
    """

    return UserService.update(body=body)


@router.delete(path="/{uid}")
async def delete_user(uid: str):
    """
    `회원삭제 API`

    Args:
    - **user_id**: 회원 아이디
    """

    return UserService.delete(uid=uid)


@router.get(path="")
async def read_user_list():
    """
    `회원목록 조회 API`
    """

    return UserService.fetch_user_list()

