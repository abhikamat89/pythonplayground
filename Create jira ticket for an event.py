import requests
import json

# Arena API Configuration
ARENA_BASE_URL = "https://api.arenasolutions.com/v1"
ARENA_USERNAME = "your-username"
ARENA_PASSWORD = "your-password"

# Jira API Configuration
JIRA_BASE_URL = "https://yourcompany.atlassian.net/rest/api/3"
JIRA_USER = "your-email@example.com"
JIRA_API_TOKEN = "YOUR_JIRA_API_TOKEN"
JIRA_HEADERS = {
    "Authorization": f"Basic {requests.auth._basic_auth_str(JIRA_USER, JIRA_API_TOKEN)}",
    "Content-Type": "application/json"
}

JIRA_PROJECT_KEY = "PROJECT_KEY"
JIRA_ISSUE_TYPE = "Task"  # Change as needed


def get_arena_session():
    """Authenticate with Arena and return a session object"""
    url = f"{ARENA_BASE_URL}/login"
    payload = {"username": ARENA_USERNAME, "password": ARENA_PASSWORD}

    session = requests.Session()  # Persist authentication using session
    response = session.post(url, json=payload)

    if response.status_code == 200:
        print("✅ Arena session created successfully.")
        return session  # Return the authenticated session object
    else:
        print("❌ Error logging in:", response.status_code, response.text)
        return None


def get_arena_events(session):
    """Fetch new events from Arena API using session authentication"""
    url = f"{ARENA_BASE_URL}/events"
    response = session.get(url)

    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("❌ Error fetching events:", response.status_code, response.text)
        return None


def create_jira_ticket(event):
    """Create a Jira issue based on an Arena event"""
    url = f"{JIRA_BASE_URL}/issue"
    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": f"Arena Event: {event['type']} - {event['id']}",
            "description": f"New event in Arena:\n\n{json.dumps(event, indent=2)}",
            "issuetype": {"name": JIRA_ISSUE_TYPE}
        }
    }

    response = requests.post(url, headers=JIRA_HEADERS, json=payload)
    if response.status_code == 201:
        jira_issue = response.json()
        print(f"✅ Jira issue created: {jira_issue['key']}")
        return jira_issue["key"]
    else:
        print("❌ Error creating Jira ticket:", response.status_code, response.text)
        return None


def reconcile_arena_event(session, event_id):
    """Mark an Arena event as reconciled"""
    url = f"{ARENA_BASE_URL}/events/{event_id}/reconcile"
    response = session.post(url)

    if response.status_code == 200:
        print(f"✅ Event {event_id} reconciled successfully.")
    else:
        print(f"❌ Error reconciling event {event_id}:", response.status_code, response.text)


if __name__ == "__main__":
    # Step 1: Authenticate with Arena
    session = get_arena_session()
    if not session:
        exit("❌ Failed to authenticate with Arena. Exiting...")

    # Step 2: Fetch Arena events
    events = get_arena_events(session)
    if not events:
        print("🔍 No new events found.")
    else:
        for event in events:
            event_id = event["id"]

            # Step 3: Create a Jira ticket for each event
            jira_issue_key = create_jira_ticket(event)

            # Step 4: Reconcile the event in Arena if Jira issue was created
            if jira_issue_key:
                reconcile_arena_event(session, event_id)

    # Step 5: Logout from Arena
    session.get(f"{ARENA_BASE_URL}/logout")
    print("🚪 Logged out of Arena.")