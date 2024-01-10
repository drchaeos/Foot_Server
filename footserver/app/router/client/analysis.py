import os
import time

from fastapi import APIRouter, Request, File, UploadFile

from app.config.config import base_dir
from app.models.user import *
from app.service.client.user_service import UserService

from app.ai.web_foot_lateral_inference import save_samples as foot_lateral
from app.ai.web_foot_ap_inference import save_samples as foot_ap

router = APIRouter(prefix="/analysis")

import zipfile
import os


def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

    zip_file.close()


# Example usage

@router.post(path="/lateral")
async def analysis_lateral(request: Request, file: UploadFile = File(...)):
    """
    `Lateral 분석 API`
    """

    contents = await file.read()
    filename = file.filename
    file_path = os.path.join(base_dir, "static/foot_lateral/test_imgs", filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        foot_lateral()

        base_url = str(request.base_url)

        zip_folder(f'{base_dir}static/foot_lateral/out', f'{base_dir}static/foot_lateral/out.zip')

        outputs = os.listdir(f"{base_dir}static/foot_lateral/out")

        import csv

        result_csv = []
        with open(f"{base_dir}static/foot_lateral/out/footlat_result.csv") as csvfile:
            spamreader = csv.reader(csvfile)
            for index, row in enumerate(spamreader):
                #result_csv = row
                result_csv.append(row)

        return {
            "result": list(map(lambda x: f"{base_url}static/foot_lateral/out/{x}", outputs)),
            "zip_src": f"{base_url}static/foot_lateral/out.zip",
            "result_csv": result_csv
        }
    except Exception as e:
        return {
            "result": [],
            "zip_src": "",
            "result_csv": ""
        }


@router.post(path="/ap")
async def analysis_ap(request: Request, file: UploadFile = File(...)):
    """
    `AP 분석 API`
    """

    contents = await file.read()
    filename = file.filename
    file_path = os.path.join("../static/foot_ap/test_imgs", filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        foot_ap()

        base_url = str(request.base_url)

        zip_folder(f'{base_dir}static/foot_ap/out', f'{base_dir}static/foot_ap/out.zip')

        outputs = os.listdir(f"{base_dir}static/foot_ap/out")

        import csv

        result_csv = []
        with open(f"{base_dir}static/foot_ap/out/footap_result.csv") as csvfile:
            spamreader = csv.reader(csvfile)
            for index, row in enumerate(spamreader):
                #result_csv = row
                result_csv.append(row)

        return {
            "result": list(map(lambda x: f"{base_url}static/foot_ap/out/{x}", outputs)),
            "zip_src": f"{base_url}static/foot_ap/out.zip",
            "result_csv": result_csv
        }
    except Exception as e:
        return {
            "result": [],
            "zip_src": "",
            "result_csv": ""
        }


@router.get(path="/clear")
async def clear():
    outputs_lateral = os.listdir(f"{base_dir}static/foot_lateral/out")
    images_lateral = os.listdir(f"{base_dir}static/foot_lateral/test_imgs")

    for name in outputs_lateral:
        os.remove(f"{base_dir}static/foot_lateral/out/{name}")

    for name in images_lateral:
        os.remove(f"{base_dir}static/foot_lateral/test_imgs/{name}")

    outputs_ap = os.listdir(f"{base_dir}static/foot_ap/out")
    images_ap = os.listdir(f"{base_dir}static/foot_ap/test_imgs")

    for name in outputs_ap:
        os.remove(f"{base_dir}static/foot_ap/out/{name}")

    for name in images_ap:
        os.remove(f"{base_dir}static/foot_ap/test_imgs/{name}")
