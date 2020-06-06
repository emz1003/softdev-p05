from googleapiclient.discovery import build
import datetime

# Calendar API =================================================================
def get_calendar(credentials, courses):
    calendar = build('calendar', 'v3', credentials = credentials)
    dict = {}

    for course in courses:
        arr = []
        page_token = None
        while True:
            events = calendar.events().list(calendarId = course[1], pageToken = page_token).execute()
            for event in events['items']:
                # Dict mappings: https://developers.google.com/calendar/v3/reference/events#resource
                summary = event['summary']
                if "dateTime" in event['start']:
                    due_date = str(event['start']['dateTime'])
                    due_day = due_date[:10]
                    due_time = due_date[11:16]
                    arr.append({
                        "summary": summary,
                        "due_day": due_day,
                        "due_time": due_time
                    })

            page_token = events.get('nextPageToken')
            dict[course[0]] = arr
            # print("\n")
            if not page_token:
                break

    return dict
# ==============================================================================

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

def get_posts(credentials, courseid):
    """
    page_token = None
    while True:
        events = calendar.events().list(calendarId = course[1], pageToken = page_token).execute()
        for event in events['items']:
            # Dict mappings: https://developers.google.com/calendar/v3/reference/events#resource
            summary = event['summary']
            if "dateTime" in event['start']:
                due_date = str(event['start']['dateTime'])
                due_day = due_date[:10]
                due_time = due_date[11:16]
                arr.append({
                    "summary": summary,
                    "due_day": due_day,
                    "due_time": due_time
                })

        page_token = events.get('nextPageToken')
        dict[course[0]] = arr
        # print("\n")
        if not page_token:
            break
    """

    gclass = build('classroom', 'v1', credentials = credentials)

    results = gclass.courses().courseWork().list(courseId = courseid, pageSize = 30).execute()
    work = results.get('courseWork', [])

    return work
