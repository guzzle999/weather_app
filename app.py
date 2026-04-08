from flask import Flask, render_template, request
from weather_api import get_coordinates, get_weather
from utils import convertTocelsius

app = Flask(__name__)

# สร้างหน้าเว็บหลัก (รองรับทั้งการเข้าชมปกติ GET และการส่งข้อมูล POST)
@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_message = None

    # ถ้าผู้ใช้กดปุ่ม "ค้นหา" (ส่งข้อมูลแบบ POST)
    if request.method == 'POST':
        city_input = request.form.get('city') # รับชื่อเมืองจากช่องกรอกข้อมูลในเว็บ

        # --- การตรวจสอบ ---
        if not city_input or not city_input.strip():
            error_message = "กรุณาระบุชื่อเมือง"
        elif city_input.strip().isdigit():
            error_message = "ชื่อเมืองไม่สามารถเป็นตัวเลขล้วนได้"
        else:
            city = city_input.strip()
            coords, error = get_coordinates(city)
            
            if error:
                error_message = error
            else:
                lat, lon, actual_name, country = coords
                weather_info, error = get_weather(lat, lon)
                
                if error:
                    error_message = error
                else:
                    temp_celsius = convertTocelsius(weather_info["temp_f"])
                    
                    # จัดเตรียมข้อมูลใส่ตัวแปร weather_data เพื่อส่งไปที่หน้าเว็บ
                    weather_data = {
                        "city": actual_name,
                        "country": country,
                        "condition": weather_info["description"],
                        "temperature": temp_celsius,
                        "humidity": weather_info["humidity"],
                        "wind_speed": weather_info["wind_speed"],
                        "precipitation": weather_info["precipitation"]
                    }

    # ส่งตัวแปรไปให้ไฟล์ index.html ทำการแสดงผล
    return render_template('index.html', weather_data=weather_data, error_message=error_message)

if __name__ == '__main__':
    # รันเซิร์ฟเวอร์ เปิดโหมด debug เพื่อให้เห็นข้อผิดพลาดได้ง่ายขึ้น
    app.run(debug=True)