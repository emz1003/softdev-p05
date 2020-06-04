from flask import *
import os
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']

app = Flask(__name__)
# Secret key handling ========================================
# To team: run str(os.urandom(32)) to get your own, and paste it into a secret_key.txt
# file in the app/ directory.
SECRET_KEY_FILE = 'secret_key.txt'
file = open(SECRET_KEY_FILE, 'r')
app.secret_key = file.read()
file.close()
# ============================================================

@app.route("/")
def home():
    if 'credentials' not in session:
        return render_template("login.html")

    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = build('classroom', 'v1', credentials=credentials)

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])

    session['credentials'] = credentials_to_dict(credentials)

    return render_template("classes.html", courses = courses)

@app.route("/auth")
def auth():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('callback', _external = True)
    auth_url, state = flow.authorization_url(
        access_type = 'offline',
        prompt = 'consent',
        include_granted_scopes = 'true')

    session['state'] = state

    return redirect(auth_url)

@app.route("/callback")
def callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, state = state)
    flow.redirect_uri = url_for('callback', _external = True)

    auth_response = request.url
    flow.fetch_token(authorization_response = auth_response)
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.pop('state')
    session.pop('credentials')
    return redirect(url_for('home'))

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.debug = True
    app.run()
