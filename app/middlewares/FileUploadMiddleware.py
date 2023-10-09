from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware


class FileUploadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # '/ValueAnalyzer_result_save' 엔드포인트에만 적용하도록 설정
        if 'file' in request.url.path and request.method == 'POST':
            form = await request.form()
            files = form.getlist('files')  # 'files'는 업로드 파일 필드의 이름
            for file in files:
                # 파일 확장자 검사 (JPEG 또는 PNG)
                if not file.filename.endswith(('.jpeg', '.jpg', '.png')):
                    raise HTTPException(status_code=400, detail=".jpeg, .jpg, .png 파일만 업로드 가능합니다.")
                # content = await file.read()
                # # 파일 크기 검사 (100MB 미만)
                # if len(content) > 100 * 1024 * 1024:  # 100MB
                #     raise HTTPException(status_code=400, detail="파일 크기는 100MB 이하만 가능합니다.")

        response = await call_next(request)
        return response