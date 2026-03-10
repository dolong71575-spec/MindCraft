from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
import os

app = FastAPI()
DB_FILE = "DuLieu_BenhNhan.json"

@app.post("/analyze")
async def receive_data(request: Request):
    data = await request.json()
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return {"status": "Success"}

def get_table_html(title, patients_list, color_class):
    if not patients_list:
        return f"<h3>{title} (0)</h3><p style='color:gray;'>Chưa có dữ liệu cho nhóm này.</p>"
    
    table_head = f"""
    <div class="section">
        <h3 class="{color_class}-text">{title} ({len(patients_list)})</h3>
        <table>
            <tr>
                <th>Ngày Đo</th>
                <th>Họ và Tên</th>
                <th>Tuổi</th>
                <th>Tổng Điểm</th>
                <th>Vận Động</th>
                <th>Nhận Thức</th>
            </tr>
    """
    
    rows = ""
    for p in patients_list:
        rows += f"""
            <tr>
                <td>{p.get('date', '')}</td>
                <td><b>{p.get('name', 'N/A')}</b></td>
                <td>{p.get('age', 'N/A')}</td>
                <td><span class="{color_class}">{p.get('total_score', '')}</span></td>
                <td>{p.get('motor_score', '')}</td>
                <td>{p.get('cognitive_score', '')}</td>
            </tr>
        """
    return table_head + rows + "</table></div>"

@app.get("/", response_class=HTMLResponse)
@app.get("/xem-du-lieu", response_class=HTMLResponse)
def view_data():
    if not os.path.exists(DB_FILE):
        return "<h1>Chưa có dữ liệu bệnh nhân nào được gửi lên Cloud.</h1>"
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        full_data = json.load(f)
        patients = full_data.get("patients_data", {})

    # Phân loại bệnh nhân vào các nhóm
    high_risk = []
    med_risk = []
    low_risk = []
    
    for key in sorted(patients.keys(), reverse=True):
        p = patients[key]
        risk = p.get('risk_level', '').upper()
        if "CAO" in risk: high_risk.append(p)
        elif "TRUNG BÌNH" in risk: med_risk.append(p)
        else: low_risk.append(p)

    html_content = f"""
    <html>
    <head>
        <title>Phân Loại Bệnh Nhân - MindCraft PD</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; background-color: #f0f2f5; }}
            h2 {{ color: #1a5276; text-align: center; text-transform: uppercase; }}
            .section {{ margin-bottom: 40px; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
            th {{ background-color: #f8f9fa; color: #333; }}
            .risk-cao {{ background-color: #ff4d4d; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
            .risk-tb {{ background-color: #ffa500; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
            .risk-thap {{ background-color: #2ecc71; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
            .risk-cao-text {{ color: #d63031; border-left: 5px solid #d63031; padding-left: 10px; }}
            .risk-tb-text {{ color: #e67e22; border-left: 5px solid #e67e22; padding-left: 10px; }}
            .risk-thap-text {{ color: #27ae60; border-left: 5px solid #27ae60; padding-left: 10px; }}
        </style>
    </head>
    <body>
        <h2>Hệ Thống Phân Loại Trạng Thái Bệnh Nhân</h2>
        
        {get_table_html("NHÓM NGUY CƠ CAO (CẦN ƯU TIÊN)", high_risk, "risk-cao")}
        {get_table_html("NHÓM NGUY CƠ TRUNG BÌNH", med_risk, "risk-tb")}
        {get_table_html("NHÓM AN TOÀN / NGUY CƠ THẤP", low_risk, "risk-thap")}
        
        <p style="text-align:center; color:gray;">Dữ liệu đồng bộ trực tiếp từ thiết bị di động</p>
    </body>
    </html>
    """
    return html_content