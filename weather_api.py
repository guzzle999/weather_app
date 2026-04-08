import requests

def get_coordinates(city_name):
    """ดึงพิกัด (Latitude, Longitude) จากชื่อเมือง"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&format=json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # เช็คว่า HTTP Status เป็น 200 OK หรือไม่
        data = response.json()
        
        # จัดการกรณีที่ไม่พบชื่อเมือง (Error Handling)
        if "results" not in data or len(data["results"]) == 0:
            return None, "ไม่พบข้อมูลพิกัดของเมืองที่คุณระบุ"
            
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]

        # ดึงชื่อเมืองที่ API หาเจอ และประเทศ:
        actual_name = data["results"][0].get("name", city_name)
        country = data["results"][0].get("country", "ไม่ระบุประเทศ")
        return (lat, lon, actual_name, country), None

    except requests.exceptions.Timeout:
        return None, "หมดเวลาการเชื่อมต่อเครือข่าย (Timeout)"
    except requests.exceptions.RequestException as e:
        return None, f"เกิดปัญหาในการเชื่อมต่อ API พิกัด: {str(e)}"

def get_weather(lat, lon):
    """ดึงข้อมูลสภาพอากาศปัจจุบันแบบละเอียด"""
    # ระบุ temperature_unit=fahrenheit เพื่อนำมาเข้าฟังก์ชันแปลงค่า
    # อัปเดต URL เพื่อขอข้อมูลเพิ่มเติม (อุณหภูมิ, ความชื้นสัมพัทธ์, ความเร็วลม, ปริมาณฝน, รหัสสภาพอากาศ)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&temperature_unit=fahrenheit"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # ดึงก้อนข้อมูล current ออกมา
        current = data.get("current", {})
        
        # เก็บค่าต่างๆ ลงตัวแปร (ใช้ .get() และกำหนดค่า default เป็น 0 เพื่อป้องกัน Error)
        temp_f = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m", 0)
        wind_speed = current.get("wind_speed_10m", 0)
        precipitation = current.get("precipitation", 0)
        
        # แผนผังรหัสสภาพอากาศ (Weather Code) แบบย่อ
        weather_code = current.get("weathercode", 0)
        description = "ท้องฟ้าแจ่มใส" if weather_code <= 1 else "มีเมฆมาก/ฝนตก"
        
        # ส่งค่ากลับไปเป็น Dictionary ที่มีข้อมูลครบขึ้น
        return {
            "temp_f": temp_f, 
            "description": description,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "precipitation": precipitation
        }, None

    except requests.exceptions.RequestException as e:
        return None, f"เกิดปัญหาในการเชื่อมต่อ API สภาพอากาศ: {str(e)}"