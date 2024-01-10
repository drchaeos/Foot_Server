import json
from dataclasses import asdict

import bcrypt
from app.utils.DH_PyLogger import Log
from app.utils.DH_PyMoment import D
from app.utils.DH_PyValidator import *

from app.database.conn_root import db
from app.database.schema.schema import Users
from app.models.user import *


class UserService:

    # 로그인 기능
    @classmethod
    def login(cls, body: FormLoginByClient):

        user = Users.filter(uid=body.id).first()

        if not user:
            return dict(is_login=False, message="이메일과 비밀번호를 확인해주세요.", user=UserModel())

        is_verified = bcrypt.checkpw(body.password.encode("utf-8"), user.password.encode("utf-8"))
        if not is_verified:
            return dict(is_login=False, message="이메일과 비밀번호를 확인해주세요.", user=UserModel())

        user = Users.filter(uid=user.uid).first()

        return dict(is_login=True, message="로그인에 성공하셨습니다.", user=user)
