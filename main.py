from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv
import os

app = FastAPI()

# --- CORS 설정 추가 ---
# 로컬에서 index.html을 직접 열면 origin이 'null'이 됩니다.
# 따라서 'null' origin을 허용해야 합니다.
# 실제 프로덕션 환경에서는 특정 도메인만 허용하도록 변경해야 합니다.
# origins = [
#     "http://localhost:8000",  # FastAPI 서버 자체의 Origin (필요에 따라)
#     "http://127.0.0.1:8000",  # FastAPI 서버 자체의 Origin (필요에 따라)
#     "null"                    # 로컬 파일에서 요청할 때의 Origin
# ]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 Origin 목록
    allow_credentials=True,  # 쿠키, HTTP 인증 등 자격 증명을 허용할지 여부
    allow_methods=["*"],    # 모든 HTTP 메소드 (GET, POST 등) 허용
    allow_headers=["*"],    # 모든 HTTP 헤더 허용
)
# --- CORS 설정 끝 ---

# CSV 파일 경로
CSV_FILE = "data.csv"

# CSV 파일이 없으면 헤더를 포함하여 생성합니다.
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["이름", "전화번호"])


class UserInfo(BaseModel):
    name: str
    phone: str

# 이 시나리오에서는 index.html을 FastAPI가 서빙하지 않습니다.
# 따라서 루트 경로 ("/")에 대한 GET 요청 핸들러는 필요하지 않습니다.
# 사용자가 직접 index.html 파일을 브라우저로 열 것입니다.


@app.post("/submit_promo")
async def submit_promo(user_info: UserInfo):
    """
    `/submit_promo` 경로로 POST 요청이 오면 이름과 전화번호를 받아 CSV 파일에 저장합니다.
    """
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([user_info.name, user_info.phone])
        return {"message": "참여 신청이 완료되었습니다!"}
    except Exception as e:
        # 실제 환경에서는 더 자세한 로깅이 필요합니다.
        print(f"Error saving data: {e}")
        raise HTTPException(
            status_code=500, detail=f"데이터 저장 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
