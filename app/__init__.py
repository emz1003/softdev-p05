from flask import *
import os
from utl import api

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

dirname = os.path.dirname(__file__) or '.'
CLIENT_SECRET_FILE =  dirname + '/' + 'client_secret.json'
userinfo = None

SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/classroom.announcements.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
    'https://www.googleapis.com/auth/classroom.topics.readonly',
    'https://www.googleapis.com/auth/classroom.push-notifications',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events.readonly'
]

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('PASSPHRASE', 'Optional default value')

    @app.route("/")
    def home():
        if 'credentials' not in session:
            return render_template("login.html")

        credentials = google.oauth2.credentials.Credentials(**session['credentials'])

        courses = api.get_courses(credentials)
        userinfo = api.get_user_info(credentials, "me")

        session['credentials'] = api.credentials_to_dict(credentials)

        return render_template("classes.html", courses = courses, userinfo = userinfo)

    @app.route("/course/<id>")
    def course(id):
        if 'credentials' not in session:
            return render_template("login.html")

        credentials = google.oauth2.credentials.Credentials(**session['credentials'])

        course = api.get_course(credentials, id)
        posts = api.get_posts(credentials, id)
        userinfo = api.get_user_info(credentials, "me")

        session['credentials'] = api.credentials_to_dict(credentials)

        return render_template("class.html", course = course, posts = posts, userinfo = userinfo)

    @app.route("/calendar")
    def calendar():
        if 'credentials' not in session:
            return render_template("login.html")

        credentials = google.oauth2.credentials.Credentials(**session['credentials'])

        courses = api.get_courses(credentials)
        calendarIDs = []
        for course in courses:
            if course['courseState'] == "ACTIVE":
                calendarIDs.append( (course['name'], course['calendarId']) )

        calendar = api.get_calendar(credentials, calendarIDs)
        print(calendar)
        userinfo = api.get_user_info(credentials, "me")

        session['credentials'] = api.credentials_to_dict(credentials)

        return render_template("calendar.html", calendar = calendar.items(), userinfo = userinfo)

    @app.route("/logout")
    def logout():
        session.pop('state')
        session.pop('credentials')
        return redirect(url_for('home'))

    # OAuth2 authentication ====================================================
    @app.route("/auth")
    def auth():
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE, scopes = SCOPES)

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
            CLIENT_SECRET_FILE, scopes = SCOPES, state = state)
        flow.redirect_uri = url_for('callback', _external = True)

        auth_response = request.url
        flow.fetch_token(authorization_response = auth_response)
        credentials = flow.credentials
        session['credentials'] = api.credentials_to_dict(credentials)

        return redirect(url_for('home'))

    # ==========================================================================

    return app

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = "1"
    app = create_app()
    app.debug = True
    app.run()
