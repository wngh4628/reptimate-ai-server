from fastapi import UploadFile, HTTPException
from core.errors import exceptions as ex
from typing import List, Union

class FileChecker:
    async def imgCheck(files: Union[UploadFile, List[UploadFile]]):

        if isinstance(files, List):
            for file in files:
                # 파일 확장자 검사 (JPEG 또는 PNG)
                if not file.filename.endswith(('.jpeg', '.jpg', '.png')):
                    raise ex.NotImgFile()
                content = await file.read()
                # 파일 크기 검사 (100MB 미만)
                if len(content) > 100 * 1024 * 1024:  # 100MB
                    return HTTPException(status_code=500, detail="파일 크기는 100MB 이하만 가능합니다.")

        else:
            if not files.filename.endswith(('.jpeg', '.jpg', '.png')):
                raise ex.NotImgFile()
            content = await files.read()
            # 파일 크기 검사 (100MB 미만)
            if len(content) > 100 * 1024 * 1024:  # 100MB
                return HTTPException(status_code=500, detail="파일 크기는 100MB 이하만 가능합니다.")
