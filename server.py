from fastapi import FastAPI, Request
import json
import os

app = FastAPI()

# Đường dẫn file lưu dữ liệu trên Cloud
DB_FILE = "DuLieu_BenhNhan.json"

@app.post("/analyze")
async def receive_data(request: Request):
    data = await request.json()
    
    # In ra log của Server
    print("📡 ĐÃ NHẬN DỮ LIỆU TỪ APP:")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    
    # Lưu vào file JSON trên Cloud
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    return {"status": "Success", "message": "Server 24/7 đã nhận dữ liệu!"}

@app.get("/")
def read_root():
    return {"Trạng thái": "Trạm thu sóng Y Sinh đang chạy 24/7 trên Cloud rần rần nha!"}

@app.get("/xem-du-lieu")
def get_data():
    # Bác sĩ gõ link này trên trình duyệt web là xem được toàn bộ dữ liệu luôn!
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"Thông báo": "Chưa có bệnh nhân nào đo."}