import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# load .env variables
load_dotenv()

# define scope (Google Sheets API)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# load credentials from JSON key file
creds = Credentials.from_service_account_file("service-key-file.json", scopes=SCOPES)

# authenticate with Google Sheets
client = gspread.authorize(creds)

# open spreadsheet by ID
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# error checking
if not SPREADSHEET_ID:
    raise ValueError("Missing SPREADSHEET_ID environment variable.")

# open spreadsheet
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# read data
data = sheet.get_all_values()
print("Sheet Data:", data)
