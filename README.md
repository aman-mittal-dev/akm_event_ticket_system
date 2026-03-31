# 🎟 Event Ticketing System

A complete backend-based Event Ticketing System built using **FastAPI** and **MongoDB** that supports bulk ticket generation, QR code verification, PDF generation, and CSV export functionality.

## 🚀 Features

- ✅ Bulk Ticket Generation
- ✅ Unique Ticket ID (AM-XXXX format)
- ✅ Base64 Encoded Secure Ticket Data
- ✅ QR Code Generation
- ✅ PDF Ticket Generation with Embedded QR
- ✅ Ticket Verification API
- ✅ Status Tracking (unused / used)
- ✅ CSV Export of Tickets
- ✅ Timestamp Logging (created_at, updated_at)
- ✅ Swagger API Documentation

## 🛠 Tech Stack

- Python
- FastAPI
- MongoDB
- Pydantic
- QRCode Library
- FPDF
- Jinja2
- Uvicorn

## 📂 Project Structure

app1/

assets/

output/

├── pdfs/

├── qr/

templates/

.env

.gitignore

main.py

requirements.txt

README.md

## ⚙️ Installation and Setup

### 1️⃣ Clone Repository

bash

git clone https://github.com/your-username/ticketing-system.git

cd ticketing-system

### 2️⃣ Create Virtual Environment

bash

python -m venv venv

source venv/bin/activate   # Mac/Linux

venv\Scripts\activate      # Windows

### 3️⃣ Install Dependencies

bash
pip install -r requirements.txt

### 4️⃣ Setup Environment Variables

Create `.env` file:

MONGO_URL=your_mongodb_connection_string

DATABASE_NAME=ticket_db

## ▶️ Run Application

bash

uvicorn main:app --reload

Open in browser:

http://127.0.0.1:8000/docs

Swagger UI will open.

## 📌 API Endpoints

#### QR Code Generation
POST /ticket/generate-qr-codes

#### PDF Generation
POST /generate-individual-pdfs

#### Export CSV
GET /ticket/export-csv

#### QR Code Scanning
POST /ticket/scan

#### Welcome & Health
Greating
GET /greating

Health Check
GET /health

Read Root
GET /

## 🔐 Ticket Lifecycle

1. Unique Ticket ID Generated
2. Data Encoded using Base64
3. QR Code Created
4. Ticket Stored in MongoDB
5. PDF Generated
6. Ticket Verified via Scan API

## 📊 Database Fields

* ticket_id
* encoded_data
* status (unused/used)
* pdf_generated
* created_at
* updated_at

## 📈 Future Improvements

* Admin Dashboard
* Authentication & Authorization
* Docker Deployment
* Cloud Deployment (AWS/Render)
* Email Ticket Delivery

## 👨‍💻 Author

Aman Kumar Mittal
Backend Developer
FastAPI | MongoDB | Python

## ✅ Important: .gitignore Update
Add the following to `.gitignore` depending on your project structure:

####  Ignore output if needed
output/

#### Ignore assets if needed
assets/

#### Ignore virtual environment
venv/

#### Ignore env file
.env#
