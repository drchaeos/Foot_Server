from dataclasses import asdict

import bcrypt

from app.config.consts import ADMIN_ID, ADMIN_PW
from app.database.conn_root import db
from app.database.schema.schema import Users
from app.models.user import *
from app.utils.DH_PyMoment import D


class UserService:

    # 회원등록 기능
    @classmethod
    def create(cls, body: FormUser):
        session = next(db.session())

        is_exist = Users.filter(uid=body.uid).count() > 0
        if is_exist:
            return dict(is_create=False, message="이미 등록된 회원입니다.")

        data = asdict(body)
        data["regist_dt"] = D.get_now()

        data["password"] = bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt())
        data["password_re"] = bcrypt.hashpw(body.password_re.encode("utf-8"), bcrypt.gensalt())

        Users.create(session=session, auto_commit=True, **data)

        return dict(is_create=True, message="회원이 등록되었습니다.")

    # 회원수정 기능
    @classmethod
    def update(cls, body: FormUser):
        is_exist = Users.filter(uid=body.uid).count() > 0
        if not is_exist:
            return dict(is_create=False, message="등록되지 않은 회원입니다.")

        data = asdict(body)

        user = Users.filter(uid=body.uid).first()

        is_verified = bcrypt.checkpw(body.password.encode("utf-8"), user.password.encode("utf-8"))
        if not is_verified:
            data["password"] = bcrypt.hashpw(body.password.encode("utf-8"), bcrypt.gensalt())
        else:
            del data["password"]

        Users.filter(uid=body.uid).update(auto_commit=True, **data)

        return dict(is_create=True, message="회원이 수정되었습니다.")

    # 회원삭제 기능
    @classmethod
    def delete(cls, uid: str):
        Users.filter(uid=uid).delete(auto_commit=True)

        return dict(is_delete=True, message="회원이 삭제되었습니다.")

    # 관리자 로그인 기능
    @classmethod
    def login(cls, body: FormLoginByAdmin):
        if body.id == ADMIN_ID and body.password == ADMIN_PW:
            return dict(is_login=True, message="관리자 로그인에 성공했습니다.")
        else:
            return dict(is_login=False, message="관리자 계정을 확인해주세요.")

    # 회원목록 조회 기능
    @classmethod
    def fetch_user_list(cls):
        return dict(
            items=Users.filter().all(limit=0)
        )
