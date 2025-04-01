import requests
import json
import os
from datetime import datetime

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this as an environment variable
GITHUB_REPO = "your-username/your-repo"

# Generate dynamic release tag and name based on date/time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
RELEASE_TAG = f"v{current_time}"
RELEASE_NAME = f"Version {current_time}"
RELEASE_BODY = "Automated release with timestamp."
FILE_PATH = "path/to/your/compiled-file.zip"  # Update with your actual file path

# GitHub API URL
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases"

# Headers
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Release data
release_data = {
    "tag_name": RELEASE_TAG,
    "name": RELEASE_NAME,
    "body": RELEASE_BODY,
    "draft": False,
    "prerelease": False
}

# Create the release
response = requests.post(GITHUB_API_URL, headers=headers, data=json.dumps(release_data))

if response.status_code == 201:
    print("Release published successfully!")
    release_id = response.json()["id"]
    upload_url = response.json()["upload_url"].split("{?name,label}")[0]

    # Upload the compiled file
    with open(FILE_PATH, "rb") as file:
        file_name = os.path.basename(FILE_PATH)
        upload_headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "application/octet-stream"
        }
        upload_response = requests.post(
            f"{upload_url}?name={file_name}", headers=upload_headers, data=file
        )

        if upload_response.status_code == 201:
            print("File uploaded successfully!")
        else:
            print("Failed to upload file.")
            print(upload_response.json())
else:
    print("Failed to publish release.")
    print(response.json())
