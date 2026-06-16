import os
import json
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

def export_to_google_sheet(df, sheet_name, work_sheet_name):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Read secret JSON from environment variable
    secret_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS")
    if not secret_json:
        raise RuntimeError("Missing GOOGLE_SHEETS_CREDENTIALS environment variable")

    creds_info = json.loads(secret_json)
    creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
    gc = gspread.authorize(creds)

    try:
        sheet = gc.open(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = gc.create(sheet_name)

    try:
        worksheet = sheet.worksheet(work_sheet_name)
        worksheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=work_sheet_name, rows=df.shape[0], cols=df.shape[1])

    set_with_dataframe(worksheet, df)
    print(f"✅ Data exported to Google Sheet: {sheet_name} → {work_sheet_name}")
