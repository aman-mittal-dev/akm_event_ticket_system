from fastapi import APIRouter, status, Response
from pydantic import BaseModel
from datetime import datetime
from app1.db import tickets_collection

router = APIRouter()

class QRScanRequest(BaseModel):
    encrypted_data: str

# QR code scanning endpoint
@router.post("/scan", tags=["QR Code Scanning"])
def scan_ticket(res: Response, data: QRScanRequest):
    try:
        ticket = tickets_collection.find_one({"encrypted_data": data.encrypted_data})

        if not ticket:
            res.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "data": None,
                "message": "Invalid QR code",
                "status": status.HTTP_400_BAD_REQUEST
            }

        if ticket["status"] == "used":
            res.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "data": None,
                "message": "Ticket has already been used",
                "status": status.HTTP_400_BAD_REQUEST
            }

        # Mark as used and update scanned_at and updated_at
        tickets_collection.update_one(
            {"_id": ticket["_id"]},
            {"$set": {
                "status": "used",
                "scanned_at": datetime.utcnow(), #datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.utcnow(), #datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            }
        )

        res.status_code = status.HTTP_200_OK
        return {
            "data": ticket["ticket_id"],
            "message": "Ticket successfully marked as used",
            "status": status.HTTP_200_OK
        }
    except Exception as e:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "data": None,
            "message": f"Error processing QR code: {str(e)}",
            "status": status.HTTP_400_BAD_REQUEST
        }