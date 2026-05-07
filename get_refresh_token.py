"""
One-time script to get a YouTube OAuth2 refresh token.
Run: venv\Scripts\python.exe get_refresh_token.py
"""
import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode, urlparse, parse_qs

import requests
from lib.config import YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET

REDIRECT_URI = "http://localhost:8080"
SCOPES = "https://www.googleapis.com/auth/youtube.upload"

auth_code = None


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        params = parse_qs(urlparse(self.path).query)
        auth_code = params.get("code", [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<h2>Authorization complete. You can close this tab.</h2>")

    def log_message(self, *args):
        pass


def main():
    if not YOUTUBE_CLIENT_ID or not YOUTUBE_CLIENT_SECRET:
        print("ERROR: YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET must be set in .env")
        return

    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode({
        "client_id": YOUTUBE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
    })

    server = HTTPServer(("localhost", 8080), CallbackHandler)
    threading.Thread(target=server.handle_request, daemon=True).start()

    print("Opening browser for Google authorization...")
    webbrowser.open(auth_url)
    print("Waiting for callback...")

    server.handle_request()

    if not auth_code:
        print("ERROR: No authorization code received.")
        return

    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": YOUTUBE_CLIENT_ID,
        "client_secret": YOUTUBE_CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }, timeout=30)
    resp.raise_for_status()
    tokens = resp.json()

    refresh_token = tokens.get("refresh_token")
    if refresh_token:
        print("\n✓ Success! Add this to your .env file:\n")
        print(f"YOUTUBE_REFRESH_TOKEN={refresh_token}\n")
    else:
        print("ERROR: No refresh_token in response. Make sure 'prompt=consent' was used.")
        print(json.dumps(tokens, indent=2))


if __name__ == "__main__":
    main()
