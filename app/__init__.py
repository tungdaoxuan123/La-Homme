from flask import Flask, request, jsonify
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Configuration for SendGrid
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
TO_EMAIL = os.environ.get('TO_EMAIL')

# Path to your service account key file
JSON_KEYFILE = 'la-homme-1722075889171-894f2a881bd0.json'
# Google Sheet ID
SPREADSHEET_ID = '14j6jcdU8deSEQkF1vwFLkY7G7ALn8YYv0IiliPWGt1Q'

def create_app():
    app = Flask(__name__)

    @app.route('/send-email', methods=['POST'])
    def send_email():
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        price = request.form['selected_price']

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = [name, email, phone, price, timestamp]

        client = get_gsheet_client(JSON_KEYFILE)
        append_to_sheet(client, SPREADSHEET_ID, data)

        return jsonify(message='Form submitted successfully and data stored in Google Sheets!')

    from .routes import main
    app.register_blueprint(main)
    
    return app

def get_gsheet_client(json_keyfile):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(json_keyfile, scopes=scopes)
    client = gspread.authorize(creds)
    return client

def append_to_sheet(client, spreadsheet_id, data):
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.get_worksheet(0)  # Assumes the first sheet
    worksheet.append_row(data, value_input_option='RAW')
