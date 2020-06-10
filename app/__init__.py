import os
from flask import *
from datetime import datetime

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from utl import api
from utl import db

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

        userinfo = api.get_user_info(credentials, "me")
        hiddencourses = db.get_hidden_classes(userinfo['id'])
        courses = api.get_courses(credentials)
        for i in reversed(range(len(courses))):
            if hiddencourses.find(courses[i]['id']) != -1 and courses[i]['courseState'] != "ARCHIVED":
                courses.pop(i)

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
        if (len(posts) == 0):
            error = " No assignments found"
        else:
            error = " You may expand posts by clicking on them."

        session['credentials'] = api.credentials_to_dict(credentials)

        return render_template("class.html", course = course, posts = posts, userinfo = userinfo, id = id, error = error)

    @app.route("/todo")
    def todo():
        if 'credentials' not in session:
            return render_template("login.html")
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        courses = api.get_courses(credentials)
        userinfo = api.get_user_info(credentials, "me")
        session['credentials'] = api.credentials_to_dict(credentials)
        masterAssign = []
        #compare times, if times is later then print them to to do list
        for course in courses:
            if (course['courseState'] == "ACTIVE"):
                #thing include name, id, and assignemnt for each class
                thing = []
                something = False
                name = course['name']
                #assignments include all the assignmnets for a specific class that havnt been due yet
                assignments = []
                id = course['id']
                posts = api.get_posts(credentials, id)
                today = (datetime.now())
                #Go through posts to see if query is in either a work or announcment
                for post in posts:
                    if (type(post).__name__ == 'Work'):
                        if (post.dueDate != ''):
                            datetime_object = datetime.strptime(post.dueDate, '%Y-%m-%d')
                            if (datetime_object > today):
                                assignments.append(post)
                                something = True
                            #If same day, check if time passed already
                            elif (datetime_object == today):
                                now = datetime.now()
                                time_object = datetime.strptime(post.dueTime, "%H:%M")
                                if (time_object >= now):
                                    assignments.append(post)
                                    something = True
                thing.append("\t"+name)
                if (something):
                    thing.append(assignments)
                    masterAssign.append(thing)
                else:
                    thing.append('none')
                    masterAssign.append(thing)
        return render_template("todo.html", userinfo = userinfo, masterAssign = masterAssign)


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
        userinfo = api.get_user_info(credentials, "me")

        session['credentials'] = api.credentials_to_dict(credentials)

        calendarlink = "https://calendar.google.com/calendar/embed?height=600&amp;wkst=1&amp;bgcolor=%23ffffff&amp;ctz=America%2FNew_York&amp;"

        for calendarID in calendarIDs:
            calendarlink += ('src=' + calendarID[1] + '&amp;')

        print(calendarlink)



        return render_template("calendar.html", calendar = calendar.items(), userinfo = userinfo, clink = calendarlink)

    @app.route("/archived")
    def archived():
        if 'credentials' not in session:
            return render_template("login.html")

        credentials = google.oauth2.credentials.Credentials(**session['credentials'])

        userinfo = api.get_user_info(credentials, "me")
        hiddencourses = db.get_hidden_classes(userinfo['id'])
        courses = api.get_courses(credentials)
        hidden = []
        for course in courses:
            if hiddencourses.find(course['id']) != -1 and course['courseState'] != "ARCHIVED":
                hidden.append(course)

        userinfo = api.get_user_info(credentials, "me")

        session['credentials'] = api.credentials_to_dict(credentials)

        return render_template("archived.html", courses = courses, hiddenCourses = hidden, userinfo = userinfo)

    @app.route("/hide")
    def hide():
        if 'credentials' not in session:
            return render_template("login.html")

        credentials = google.oauth2.credentials.Credentials(**session['credentials'])

        userinfo = api.get_user_info(credentials, "me")
        userid = userinfo['id']
        classid = request.args.get('id')
        db.togglehide(userid, classid)

        return redirect(url_for('archived'))

    @app.route("/logout")
    def logout():
        session.pop('state')
        session.pop('credentials')
        return redirect(url_for('home'))

#process search query
    @app.route("/query", methods=['POST'])
    def query():
        id = request.form['id']
        if 'credentials' not in session:
            return render_template("login.html")
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        course = api.get_course(credentials, id)
        posts = api.get_posts(credentials, id)
        userinfo = api.get_user_info(credentials, "me")
        session['credentials'] = api.credentials_to_dict(credentials)
        query = request.form['keyword']
        if (query == ""):
            dog = []
            error = " No assignments found"
        else:
            query = query.lower()
            #initialize dog list
            dog = []
            #Go through posts to see if query is in either a work or announcment
            for post in posts:
                if (type(post).__name__ == 'Work'):
                    text = post.description
                    if (post.description.lower().find(query) > 0 or post.title.lower().find(query) > 0):
                        dog.append(post)
                    text = post.title
                if (type(post).__name__ == 'Announcement'):
                    text = post.text
                    if (text.lower().find(query) > 0):
                        dog.append(post)
            if (len(dog) == 0):
                error = " No assignments found"
            else: error = "You may expand posts by clicking on them."
        return render_template("class.html", course = course, error = error, posts = dog, userinfo = userinfo, id = id)

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

app = create_app()

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = "1"
    app.debug = True
    app.run()
