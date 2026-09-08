"""
One-time interactive setup: run this yourself once (`python google_auth_setup.py`)
to grant Jarvis access to Gmail and Calendar. It opens a browser for you to log
in and consent, then saves the resulting token to token.json for future runs.
"""

from google_services import get_google_creds

if __name__ == "__main__":
    get_google_creds()
    print("Google authorization complete. token.json saved.")
