import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Fetch catalog page
response = requests.get(CATALOG_URL, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

# Find all links
links = soup.find_all("a")

assessment_urls = []

# Extract assessment URLs
for link in links:

    href = link.get("href")
    text = link.get_text(strip=True)

    # Keep only Individual Test Solutions
    if (
        href
        and "/products/product-catalog/view/" in href
        and text
        and "solution" not in text.lower()
    ):

        full_url = BASE_URL + href if href.startswith("/") else href

        assessment_urls.append({
            "name": text,
            "url": full_url
        })

# Remove duplicates
unique_assessments = []
seen = set()

for item in assessment_urls:

    if item["url"] not in seen:

        seen.add(item["url"])
        unique_assessments.append(item)

print(f"Found {len(unique_assessments)} assessments")

all_assessments = []

# Visit each assessment page
for idx, item in enumerate(unique_assessments):

    print(f"Scraping {idx + 1}/{len(unique_assessments)}")

    try:

        page = requests.get(item["url"], headers=headers)

        page_soup = BeautifulSoup(page.text, "html.parser")

        # Extract useful paragraph text
        paragraphs = page_soup.find_all("p")

        description_parts = []

        for p in paragraphs:

            text = p.get_text(strip=True)

            # Ignore tiny or useless text
            if (
                len(text) > 50
                and "outdated browser" not in text.lower()
                and "cookie" not in text.lower()
            ):

                description_parts.append(text)

        description = " ".join(description_parts[:10])

        # Save assessment
        assessment = {
            "name": item["name"],
            "url": item["url"],
            "description": description
        }

        all_assessments.append(assessment)

        time.sleep(1)

    except Exception as e:
        print("Error scraping:", item["url"])
        print(e)

# Save JSON file
with open("catalog/assessments.json", "w", encoding="utf-8") as f:

    json.dump(
        all_assessments,
        f,
        indent=2,
        ensure_ascii=False
    )

print("\nSaved catalog/assessments.json successfully!")
print(f"Total assessments saved: {len(all_assessments)}")