# app/utils/csv_exporter.py
import csv, os
from app1.db import tickets_collection

def export_tickets_to_csv(filename="output/tickets.csv"):
    # Create an output folder if you don't have one.
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Open the file and start writing
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["ticket_id", "encrypted_data", "status", "created_at", "updated_at", "scanned_at"])

        # Fetch all tickets from mongodb and writing them to the CSV file
        for ticket in tickets_collection.find():
            writer.writerow([
                ticket.get("ticket_id", ""),
                ticket.get("encrypted_data", ""),
                ticket.get("status", "unused"),
                ticket.get("created_at", ""),
                ticket.get("updated_at", ""),
                ticket.get("scanned_at", ""),
            ])
    
    return filename
