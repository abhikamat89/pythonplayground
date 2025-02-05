import requests

# Set up API credentials
BASE_URL = "https://api.arenasolutions.com/v1"
TOKEN = "YOUR_ACCESS_TOKEN"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def get_all_extracts():
    """Fetch all extracts from Arena API"""
    url = f"{BASE_URL}/extracts"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error getting extracts:", response.status_code, response.text)
        return None

def get_latest_extract():
    """Fetch the latest extract"""
    extracts = get_all_extracts()
    if extracts and "results" in extracts and extracts["results"]:
        return extracts["results"][0]  # Assuming first entry is the latest
    return None

def get_extract_runs(extract_id):
    """Fetch all runs for a specific extract"""
    url = f"{BASE_URL}/extracts/{extract_id}/runs"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting extract runs for {extract_id}:", response.status_code, response.text)
        return None

def get_latest_run(extract_id):
    """Fetch the latest run for a specific extract"""
    runs = get_extract_runs(extract_id)
    if runs and "results" in runs and runs["results"]:
        return runs["results"][0]  # Assuming first entry is the latest
    return None

def get_all_file_associations():
    """Fetch all file associations from Arena API"""
    url = f"{BASE_URL}/file-associations"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error getting file associations:", response.status_code, response.text)
        return None

# Example usage
if __name__ == "__main__":
    print("Fetching all extracts...")
    extracts = get_all_extracts()
    print(extracts)

    print("\nFetching latest extract...")
    latest_extract = get_latest_extract()
    print(latest_extract)

    if latest_extract:
        extract_id = latest_extract["id"]
        print(f"\nFetching extract runs for extract ID {extract_id}...")
        extract_runs = get_extract_runs(extract_id)
        print(extract_runs)

        print(f"\nFetching latest run for extract ID {extract_id}...")
        latest_run = get_latest_run(extract_id)
        print(latest_run)

    print("\nFetching all file associations...")
    file_associations = get_all_file_associations()
    print(file_associations)