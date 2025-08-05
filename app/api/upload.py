from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
from pathlib import Path
from fastapi.responses import JSONResponse

router = APIRouter()

# Thư mục lưu trữ ảnh
UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Kiểm tra định dạng file
        allowed_extensions = {".jpg", ".jpeg", ".png", ".gif"}
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Định dạng file không được hỗ trợ. Chỉ chấp nhận jpg, jpeg, png, gif.")

        # Tạo tên file duy nhất
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / file_name

        # Lưu file
        with file_path.open("wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Tạo URL tuyệt đối
        file_url = f"/static/uploads/{file_name}"
        return JSONResponse(content={"url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể tải lên file: {str(e)}")