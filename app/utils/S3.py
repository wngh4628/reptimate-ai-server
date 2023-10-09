from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import FastAPI, UploadFile
from dotenv import dotenv_values
import datetime
import pytz
import uuid
import asyncio

class S3Uploader:
    def __init__(self, bucket_name, region, access_key, secret_key):
        print('bucket_name', bucket_name)
        self.bucket_name = bucket_name
        self.region = region
        self.access_key = access_key
        self.secret_key = secret_key
        self.s3 = boto3.client('s3', region_name=self.region,
                               aws_access_key_id=self.access_key,
                               aws_secret_access_key=self.secret_key)
    # 한개씩
    def upload_image(self, file: UploadFile, folder_name):
        try:
            # 업로드할 파일의 이름을 생성 (이름 중복 방지)
            file_name = f"{self.moment_file()}-{uuid.uuid4()}-{file.filename}"
            # 폴더 + 파일 이름
            object_key = f"{folder_name}/{file_name}"
            # S3에 파일 업로드
            self.s3.upload_fileobj(file.file, self.bucket_name, object_key)

            # 업로드한 이미지의 URL 생성
            image_url = f"https://{self.bucket_name}.s3-{self.region}.amazonaws.com/{object_key}"

            return {"message": f"Image uploaded successfully. URL: {image_url}"}

        except NoCredentialsError:
            return {"message": "AWS credentials not available."}
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}

    def moment_file(self):
        seoul_timezone = pytz.timezone('Asia/Seoul')
        current_time = datetime.datetime.now(seoul_timezone)
        formatted_time = current_time.strftime('%Y%m%d%H%M%S')
        return formatted_time



# S3Uploader 클래스 인스턴스 생성
s3_uploader = S3Uploader(
    bucket_name=dotenv_values('../.env').get("AWS_BUCKET_NAME"),
    region=dotenv_values('../.env').get("AWS_BUCKET_REGION"),
    access_key=dotenv_values('../.env').get("AWS_ACECSS_KEY_ID"),
    secret_key=dotenv_values('../.env').get("AWS_SECRET_ACCESS_KEY"),
)
