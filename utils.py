def convertTocelsius(fahrenheit):
    """แปลงอุณหภูมิจากฟาเรนไฮต์เป็นเซลเซียส และปัดเศษทศนิยม 2 ตำแหน่ง"""
    try:
        # รองรับ Edge Case: ตรวจสอบว่า input เป็นตัวเลขหรือไม่
        val = float(fahrenheit)
        celsius = (val - 32) * 5.0 / 9.0
        return round(celsius, 2)
    except (ValueError, TypeError):
        return None