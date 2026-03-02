import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(credentials)
    sheet = client.open("BreatheSmart_Data")

    return sheet.worksheet("users"), sheet.worksheet("logs")
