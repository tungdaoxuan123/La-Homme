from flask import Flask, request, jsonify
import os
import requests
import sendgrid
from app import create_app
from sendgrid.helpers.mail import Mail, Email, To, Content

app = Flask(__name__)
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
