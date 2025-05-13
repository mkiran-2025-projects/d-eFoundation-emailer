import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
BASE_URL = "https://api.hunter.io/v2/domain-search"

# Read domains
domains_df = pd.read_csv("domains.csv")

results = []

for _, row in domains_df.iterrows():
    domain = row["domain"]
    params = {
        "domain": domain,
        "api_key": HUNTER_API_KEY,
        "limit": 1
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        emails = data.get("data", {}).get("emails", [])
        if emails:
            email = emails[0]["value"]
            first_name = emails[0].get("first_name", "there")
            results.append({
                "name": first_name,
                "email": email
            })
            print(f"✅ Found {email} on {domain}")
        else:
            print(f"⚠️ No email found on {domain}")
    else:
        print(f"❌ Error for {domain}: {response.status_code}")

# Save to recipients.csv
df = pd.DataFrame(results)
df.to_csv("emails.csv", index=False)
print("📦 Saved to recipients.csv")
