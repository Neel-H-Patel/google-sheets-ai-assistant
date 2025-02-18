from fastapi import FastAPI, Query, HTTPException
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# define API
app = FastAPI()

# google sheets API setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "service-key-file.json"

def get_sheets_service():
    """Initialize Google Sheets API Service"""
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)

@app.get("/analyze-sheet")
async def analyze_sheet(
        spreadsheet_id: str = Query(..., description="Google Spreadsheet ID"),
        data_range: str = Query("Sheet1!A1:Z", description="Range to fetch (default: all columns in Sheet1)")
):
    """
    Fetch data from a Google Sheet and return it as JSON
    :param spreadsheet_id: The ID of the Google Sheet
    :param data_range: The range to fetch (default: Sheet1!A1:Z)
    :return: JSON response containing data from Google Sheet or an error message
    """
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=data_range).execute()
        values = result.get('values', [])

        if not values:
            return {"message": "No data found in the specified range."}

        return {"data": values}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")