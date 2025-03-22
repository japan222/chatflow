from flask import Flask, request, jsonify, render_template
import random
import json

app = Flask(__name__)

try:
    with open('responses.json', 'r', encoding='utf-8') as file:
        responses = json.load(file)
except FileNotFoundError:
    print("ไม่พบไฟล์ responses.json")
    responses = {}
except json.JSONDecodeError:
    print("ไฟล์ responses.json มีข้อผิดพลาดในการอ่าน")
    responses = {}

# Route สำหรับหน้าแรก
@app.route('/')
def index():
    return render_template('index.html')  # ส่งคืนไฟล์ index.html

# Endpoint สำหรับสุ่มข้อความตอบกลับ
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    keyword = data.get("keyword", "")

    if keyword in responses:
        # กำหนดจำนวนข้อความที่สุ่ม
        max_responses = 3 if keyword == "กรอกข้อมูล" else 5
        
        # สุ่มข้อความจาก JSON
        random_responses = random.sample(responses[keyword], min(max_responses, len(responses[keyword])))
        
        # แปลง \n เป็น <br> เพื่อแสดงผลใน HTML
        formatted_responses = [resp.replace("\n", "<br>") for resp in random_responses]
        return jsonify({"responses": formatted_responses})
    else:
        return jsonify({"error": "Invalid keyword"}), 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070, debug=True)