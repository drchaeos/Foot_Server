from dataclasses import asdict
from fastapi.staticfiles import StaticFiles

import uvicorn
from fastapi import FastAPI

# 미들웨어
from starlette.middleware.cors import CORSMiddleware

from app.config.config import conf
from app.database.conn_root import db

# 라우터
from app.router import index
from app.router.admin import user as admin_user
from app.router.client import analysis, user



def create_app():
    app = FastAPI()

    app.mount("/static", StaticFiles(directory="../static"), name="static")
    # 데이터 베이스 이니셜라이즈
    db.init_app(app, **asdict(conf()))

    # 미들웨어 정의
    app.add_middleware(CORSMiddleware, allow_origins=conf().ALLOW_SITE, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    # 라우터 정의
    app.include_router(index.router, tags=["Index"])

    app.include_router(user.router, tags=["User"])
    app.include_router(analysis.router, tags=["Analysis"])

    app.include_router(admin_user.router, tags=["Admin_Users"], prefix="/admin")

    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=9090, reload=True)
