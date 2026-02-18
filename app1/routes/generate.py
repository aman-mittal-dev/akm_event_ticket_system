import os, uuid
from datetime import datetime
from fastapi import APIRouter, Query, status, Response
from app1.db import tickets_collection
from app1.utils.qr_generator import encode_ticket_data, generate_qr_code
from app1.utils.csv_exporter import export_tickets_to_csv
from app1.utils.pdf_generator import IndividualPDFGenerator
from pymongo.errors import DuplicateKeyError

tickets_collection.create_index("ticket_id", unique=True)

router = APIRouter()

# Route to generate QR codes and store ticket data in MongoDB
@router.post("/generate-qr-codes", tags=["QR Code Generation"])
def generate_qr_codes(
    res: Response,
    ticket_count: int = Query(..., description="Number of tickets to generate"),
):
    if ticket_count <= 0 or ticket_count > 5000:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "data": None,
            "message": "Ticket count must be between 1 and 5000.",
            "status": status.HTTP_400_BAD_REQUEST
        }
    
    try:
        output_dir = "output/qr"
        os.makedirs(output_dir, exist_ok=True)

        generated_qr_codes = []

        for i in range(1, ticket_count + 1):
            try:
                ticket_id = f"AM-{uuid.uuid4().hex[:8].upper()}"
                encrypted = encode_ticket_data(ticket_id)

                qr_path = f"{output_dir}/{ticket_id}.png"
                generate_qr_code(encrypted, qr_path)

                ticket_data = {
                    "ticket_id": ticket_id,
                    "encrypted_data": encrypted,
                    "status": "unused", # unused | used | cancelled
                    "created_at": datetime.utcnow(), # datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "scanned_at": None,
                    "updated_at": datetime.utcnow(), #datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "pdf_generated": False,
                }

                try:
                    tickets_collection.insert_one(ticket_data)
                except DuplicateKeyError:
                    print(f"Duplicate ticket_id {ticket_id} detected. Skipping insertion.")
                    continue

                generated_qr_codes.append(ticket_id)

            except Exception as ticket_error:
                # If one ticket fails, the entire process should not crash
                print(f"Error generating qr code {i}: {str(ticket_error)}")
                continue
        
        res.status_code = status.HTTP_200_OK
        return {
            "data": generated_qr_codes,
            "message": f"{len(generated_qr_codes)} QR codes generated successfully.",
            "status": status.HTTP_200_OK,
        }

    except Exception as e:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "data": None,
            "message": str(e),
            "status": status.HTTP_400_BAD_REQUEST
        }

# Route to generate individual PDFs for tickets that have not had PDFs generated yet
@router.post("/generate-individual-pdfs", tags=["PDF Generation"])
def generate_individual_pdfs(
    res: Response,
    ticket_count: int = Query(..., description="Number of tickets to generate PDFs")
    ):
    try:
        count = 0
        pdf_gen = IndividualPDFGenerator()

        # Pick up only those tickets whose PDF has not been generated yet.
        tickets = tickets_collection.find(
            {"pdf_generated": {"$ne": True}}  # not equal to True
        ).limit(ticket_count)

        for ticket in tickets:
            ticket_id = ticket["ticket_id"]
            qr_path = f"output/qr/{ticket_id}.png"

            # If the QR code file does not exist, skip PDF generation for this ticket
            if not os.path.exists(qr_path):
                continue

            # generate PDF for the ticket
            pdf_gen.generate_ticket_pdf(ticket_id, qr_path)
            
            # After generating PDF, update the ticket document to mark PDF as generated
            tickets_collection.update_one(
                {"ticket_id": ticket_id},
                {
                    "$set": {
                        "pdf_generated": True,
                        "updated_at": datetime.utcnow() # datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                }
            )
            count += 1

        res.status_code = status.HTTP_200_OK
        return {
            "data": None,
            "message": f"{count} individual ticket PDFs generated successfully.",
            "status": status.HTTP_200_OK,
        }
    
    except Exception as e:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "data": None,
            "message": f"Failed to generate PDFs: {str(e)}",
            "status": status.HTTP_400_BAD_REQUEST,
        }

# Route to export all tickets data to CSV   
@router.get("/export-csv", tags=["CSV Export"])
def export_csv(res: Response):
    try:
        file_path = export_tickets_to_csv()
        res.status_code = status.HTTP_200_OK
        return {
            "data": file_path,
            "message": "CSV exported successfully",
            "status": status.HTTP_200_OK,
        }
    
    except Exception as e:
        res.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "data": None,
            "message": f"Failed to export CSV: {str(e)}",
            "status": status.HTTP_400_BAD_REQUEST,
        }