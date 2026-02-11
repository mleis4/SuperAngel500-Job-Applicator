import requests
import pandas as pd
import time

all_companies = []

for page in range(1, 35):
    print(f"Fetching page {page}/34...")

    url = (
        f"https://500.superangel.io/root-fetcher"
        f"?for=Q1-2025"
        f"&sortBy=employees"
        f"&sortIn=desc"
        f"&pageSize=20"
        f"&page={page}"
        f"&list=ALL"
        f"&_data=routes%2Froot-fetcher"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print(f"  Failed on page {page} - status {response.status_code}")
        break

    data = response.json()

    companies = data.get("startupsResponse", {}).get("companies", [])

    if not companies:
        print(f"  No companies found on page {page}, stopping.")
        break

    all_companies.extend(companies)
    print(f"  Got {len(companies)} companies (total so far: {len(all_companies)})")

    time.sleep(0.3)

# Save to CSV
if all_companies:
    df = pd.DataFrame(all_companies)
    df.to_csv("superangel500.csv", index=False)
    print(f"\nDone! Saved {len(all_companies)} companies to superangel500.csv")
else:
    print("\nNo data collected.")