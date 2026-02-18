# app/utils/qr_generator.py
import base64, qrcode

def encode_ticket_data(data: str) -> str:
    return base64.b64encode(data.encode()).decode()

def generate_qr_code(data: str, path: str):
    img = qrcode.make(data)
    img.save(path)
