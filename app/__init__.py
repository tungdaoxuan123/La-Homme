from flask import Flask, request, jsonify
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import traceback

app = Flask(__name__)

# Configuration for SendGrid
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
TO_EMAIL = os.environ.get('TO_EMAIL')

# Path to your service account key file
JSON_KEYFILE = 'la-homme.json'
# Google Sheet ID
SPREADSHEET_ID = '14j6jcdU8deSEQkF1vwFLkY7G7ALn8YYv0IiliPWGt1Q'
SPREADSHEET_KTV_ID = '1u0CoP--UtA8Fywqx2361ODJmMcpJA2TMhsosEpiMkgQ'

def create_app():
    app = Flask(__name__)

    @app.route('/send-email', methods=['POST'])
    def send_email():
        try:
            service =  request.form['selected_service']
            name = request.form['name']
            phone = request.form['phone']
            price = request.form['selected_price']
            date = request.form['date']
            hour = request.form['hour']
            minute = request.form['minute']
            note = request.form['note']
            additional_service =  request.form['additional_service']
            final_price = request.form['final_price']
            ktv = "có" if request.form['KTV'] else "không"

            # Construct the complete time from the hour and minute
            time = f"{hour.zfill(2)}:{minute.zfill(2)}"

            # Add timestamp for when the form was submitted
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Data to be appended to the Google Sheet
            data = [service, name, phone, date, time, price, ktv, additional_service, timestamp, final_price, note]
            
            print(data)
            # Get Google Sheets client and append the data
            client = get_gsheet_client(JSON_KEYFILE)
            append_to_sheet(client, SPREADSHEET_ID, data)

            return jsonify(message='Form submitted successfully and data stored in Google Sheets!')

        except Exception as e:
            traceback.print_exc()
            return jsonify(message='Failed to submit form: ' + str(e)), 500
    
    @app.route('/send-ktv-info', methods=['POST'])
    def send_ktv_email():
        try:
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            message = request.form['message']
            # Data to be appended to the Google Sheet
            data = [name, phone, email, message]

            # Get Google Sheets client and append the data
            client = get_gsheet_client(JSON_KEYFILE)
            append_to_sheet(client, SPREADSHEET_KTV_ID, data)

            return jsonify(message='Form submitted successfully and data stored in Google Sheets!')

        except Exception as e:
            return jsonify(message='Failed to submit form: ' + str(e)), 500

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
