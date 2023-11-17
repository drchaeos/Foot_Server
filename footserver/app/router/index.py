from datetime import datetime
from os import environ

from fastapi import APIRouter, Request, File, UploadFile
from starlette.responses import Response


router = APIRouter()


@router.get("/")
async def index():
    return Response(
        f"API Server [ENV : {environ.get('API_ENV', 'local')}] (KST: {datetime.now().strftime('%Y.%m.%d %H:%M:%S')})")
