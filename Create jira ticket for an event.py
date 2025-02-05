import requests
import json

# Arena API Configuration
ARENA_BASE_URL = "https://api.arenasolutions.com/v1"
ARENA_TOKEN = "YOUR_ARENA_ACCESS_TOKEN"
ARENA_HEADERS = {
    "Authorization": f"Bearer {ARENA_TOKEN}",
    "Content-Type": "application/json"
}

# Jira API Configuration
JIRA_BASE_URL = "https://yourcompany.atlassian.net/rest/api/3"
JIRA_USER = "your-email@example.com"
JIRA_API_TOKEN = "YOUR_JIRA_API_TOKEN"
JIRA_HEADERS = {
    "Authorization": f"Basic {requests.auth._basic_auth_str(JIRA_USER, JIRA_API_TOKEN)}",
    "Content-Type": "application/json"
}

# Jira Project and Issue Type
JIRA_PROJECT_KEY = "PROJECT_KEY"
JIRA_ISSUE_TYPE = "Task"  # Change as needed


def get_arena_events():
    """Fetch new events from Arena"""
    url = f"{ARENA_BASE_URL}/events"
    response = requests.get(url, headers=ARENA_HEADERS)
    if response.status_code == 200:
        events = response.json().get("results", [])
        return events
    else:
        print("Error fetching events:", response.status_code, response.text)
        return None


def create_jira_ticket(event):
    """Create a Jira issue based on the Arena event"""
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
        print(f"Jira issue created: {jira_issue['key']}")
        return jira_issue["key"]
    else:
        print("Error creating Jira ticket:", response.status_code, response.text)
        return None


def reconcile_arena_event(event_id):
    """Mark an Arena event as processed"""
    url = f"{ARENA_BASE_URL}/events/{event_id}/reconcile"
    response = requests.post(url, headers=ARENA_HEADERS)
    if response.status_code == 200:
        print(f"Event {event_id} reconciled successfully.")
    else:
        print(f"Error reconciling event {event_id}:", response.status_code, response.text)


if __name__ == "__main__":
    # Step 1: Get new events from Arena
    events = get_arena_events()

    if events:
        for event in events:
            event_id = event["id"]

            # Step 2: Create a Jira ticket for the event
            jira_issue_key = create_jira_ticket(event)

            if jira_issue_key:
                # Step 3: Reconcile the event in Arena
                reconcile_arena_event(event_id)
    else:
        print("No new events found.")