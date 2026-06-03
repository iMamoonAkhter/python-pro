import gspread
from google.oauth2.service_account import Credentials
import os

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service_account.json")

creds = Credentials.from_service_account_file(
    credentials_path,
    scopes=SCOPES
)
client = gspread.authorize(creds)

SHEET_ID = "1fiNUhlK9K0skT4qn3x5615FCLyDOcF-ojuXNNiab3i0"

sheet = client.open_by_key(SHEET_ID).sheet1


def save_lead(name, phone):
    sheet.append_row([
        name,
        phone
    ])