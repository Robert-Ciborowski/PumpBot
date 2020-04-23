"""
Gets all TSX listings from the TSX servers as JSON.
"""

import urllib.request, json

# This might take a while...
with urllib.request.urlopen("https://www.tsx.com/json/company-directory/search/tsx/.*") as url:
    print("Downloading and decoding data...")
    data = json.loads(url.read().decode())
    print(data)
