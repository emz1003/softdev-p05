from googleapiclient.discovery import build

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def get_user_info(credentials, userid):
    gclass = build('classroom', 'v1', credentials = credentials)
    results = gclass.userProfiles().get(userId = userid).execute()

    dict = {}
    dict['name'] = results['name']['fullName']
    dict['id'] = results['id']
    dict['email'] = results['emailAddress']
    dict['avatar'] = results['photoUrl']

    return dict

def get_courses(credentials):
    gclass = build('classroom', 'v1', credentials = credentials)

    results = gclass.courses().list(pageSize = 30).execute()
    courses = results.get('courses', [])

    return courses

def get_course(credentials, courseid):
    gclass = build('classroom', 'v1', credentials = credentials)

    results = gclass.courses().get(id = courseid).execute()

    return results

def get_roster(credentials, courseid):
    gclass = build('classroom', 'v1', credentials = credentials)

    results = gclass.courses().students().list(courseId = courseid).execute()
    students = results.get('students')

    return students
