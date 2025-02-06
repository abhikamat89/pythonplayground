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


def search_integrations(session, search_params=None):
    """Search for integrations based on provided parameters."""
    url = f"{ARENA_BASE_URL}/integrations/search"
    response = session.get(url, params=search_params)

    if response.status_code == 200:
        integrations = response.json().get("results", [])
        print(f"Found {len(integrations)} integration(s).")
        return integrations
    else:
        print("❌ Error searching integrations:", response.status_code, response.text)
        return None

def get_integration_details(session, integration_id):
    """Retrieve details of a specific integration."""
    url = f"{ARENA_BASE_URL}/integrations/{integration_id}"
    response = session.get(url)

    if response.status_code == 200:
        integration_details = response.json()
        print(f"Integration Details: {json.dumps(integration_details, indent=2)}")
        return integration_details
    else:
        print("❌ Error retrieving integration details:", response.status_code, response.text)
        return None

def get_event(session, event_id):
    """Fetch details of a specific event."""
    url = f"{ARENA_BASE_URL}/events/{event_id}"
    response = session.get(url)

    if response.status_code == 200:
        event_details = response.json()
        print(f"Event Details: {json.dumps(event_details, indent=2)}")
        return event_details
    else:
        print("❌ Error retrieving event details:", response.status_code, response.text)
        return None

def get_event_item_guids(session, event_id):
    """Obtain GUIDs of items associated with a specific event."""
    url = f"{ARENA_BASE_URL}/events/{event_id}/items/guids"
    response = session.get(url)

    if response.status_code == 200:
        item_guids = response.json().get("guids", [])
        print(f"Found {len(item_guids)} item GUID(s) for event {event_id}.")
        return item_guids
    else:
        print("❌ Error retrieving event item GUIDs:", response.status_code, response.text)
        return None

def get_event_item_details(session, event_id, item_guid):
    """Retrieve details of a specific item associated with an event."""
    url = f"{ARENA_BASE_URL}/events/{event_id}/items/{item_guid}"
    response = session.get(url)

    if response.status_code == 200:
        item_details = response.json()
        print(f"Item Details: {json.dumps(item_details, indent=2)}")
        return item_details
    else:
        print("❌ Error retrieving event item details:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    # Step 1: Authenticate with Arena
    session = get_arena_session()
    if not session:
        exit("❌ Failed to authenticate with Arena. Exiting...")

    # Step 2: Search for Integrations
    search_params = {"name": "Your Integration Name"}  # Adjust search parameters as needed
    integrations = search_integrations(session, search_params)

    if integrations:
        # Assuming we're interested in the first integration found
        integration_id = integrations[0]["id"]

        # Step 3: Get Integration Details
        get_integration_details(session, integration_id)

        # Step 4: Fetch Events for the Integration
        # Note: Adjust event fetching logic as per your requirements
        events = get_arena_events(session)  # Implement this function as needed

        if events:
            # Assuming we're interested in the first event
            event_id = events[0]["id"]

            # Step 5: Get Event Details
            get_event(session, event_id)

            # Step 6: Get Event Item GUIDs
            item_guids = get_event_item_guids(session, event_id)

            if item_guids:
                # Assuming we're interested in the first item GUID
                item_guid = item_guids[0]

                # Step 7: Get Event Item Details
                get_event_item_details(session, event_id, item_guid)

    # Step 8: Logout from Arena
    session.get(f"{ARENA_BASE_URL}/logout")
    print("🚪 Logged out of Arena.")