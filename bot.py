import requests
import os

TOKEN_GITHUB = os.getenv("TOKEN_GITHUB")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
REPO_OWNER = "MilesONerd"
REPO_NAME = "closure-next"

def get_changelog():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    headers = {'Authorization': f'token {TOKEN_GITHUB}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        commits = response.json()
        changelog = "\n".join([f"{commit['commit']['author']['name']}: {commit['commit']['message']}" for commit in commits[:1]])  
        return changelog
    else:
        return "Error fetching changelogs."

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    return response

def main():
    changelog = get_changelog()
    response = send_to_telegram(changelog)
    if response.status_code == 200:
        print("Changelog sent successfully!")
    else:
        print(f"Error sending changelog: {response.status_code}")

if __name__ == "__main__":
    main()
