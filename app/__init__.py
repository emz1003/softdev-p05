from flask import Flask, render_template, redirect, url_for, request
import os
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

CLIENT_SECRET_FILE = 'client_secret.json'

AUTH_BASE_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://www.googleapis.com/oauth2/v4/token'
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/auth")
def auth():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('import_from_api', _external = True)
    auth_url = flow.authorization_url()
    return redirect(auth_url[0])

@app.route("/import")
def import_from_api():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('import_from_api', _external = True)

    auth_response = request.url
    flow.fetch_token(authorization_response = auth_response)
    creds = flow.credentials

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', ['name'])

    return render_template("api_test.html", courses = courses)

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.debug = True
    app.run()
