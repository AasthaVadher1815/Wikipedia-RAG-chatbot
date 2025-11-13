###########################################################################################################
##################################  1. IMPORTING MODULES AND SETUP  ######################################
###########################################################################################################

from dotenv import load_dotenv
import os
import requests
import pandas as pd
import time
import uuid
import re
import json
from bs4 import BeautifulSoup
import html

load_dotenv()
pd.options.mode.chained_assignment = None

###########################################################################################################
##################################  2. VALIDATE ENVIRONMENT  ##############################################
###########################################################################################################

def check_environment():
    storage_file = os.getenv('SNAPSHOT_STORAGE_FILE')
    dataset_folder = os.getenv('DATASET_STORAGE_FOLDER')

    if not storage_file or not dataset_folder:
        print("❌ Please set SNAPSHOT_STORAGE_FILE and DATASET_STORAGE_FOLDER in .env")
        return False

    os.makedirs(dataset_folder, exist_ok=True)
    return True

if not check_environment():
    exit(1)

###########################################################################################################
##################################  3. LOAD KEYWORDS  ####################################################
###########################################################################################################

try:
    keywords = pd.read_excel("keywords.xlsx")
    if "Keyword" not in keywords.columns:
        raise ValueError("Missing column 'Keyword' in keywords.xlsx")
    print(f"✅ Loaded {len(keywords)} keywords.")
except Exception as e:
    print(f"❌ Error reading keywords.xlsx: {e}")
    exit(1)

###########################################################################################################
##################################  4. WIKIPEDIA SCRAPER  #################################################
###########################################################################################################

API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "WikipediaStructuredScraper/2.0 (contact@example.com)"}

def clean_wiki_html(html_text):
    """Convert raw HTML from Wikipedia into clean paragraph text."""
    soup = BeautifulSoup(html_text, "html.parser")

    # Remove non-content elements
    for tag in soup(["table", "script", "style", "math", "sup", "img", "figure"]):
        tag.decompose()

    text_blocks = []
    for p in soup.find_all("p"):
        text = p.get_text(" ", strip=True)
        text = html.unescape(text)
        text = re.sub(r"\[[0-9]+\]", "", text)
        text = re.sub(r"\s+", " ", text)
        if text:
            text_blocks.append(text)

    return "\n".join(text_blocks).strip()


def fetch_article(keyword):
    """Return a structured Wikipedia scrape matching the sample output format."""
    # Search for the best-matching page
    search_params = {"action": "query", "list": "search", "srsearch": keyword, "format": "json"}
    r = requests.get(API_URL, headers=HEADERS, params=search_params, timeout=10)
    data = r.json()
    results = data.get("query", {}).get("search", [])
    if not results:
        return f'"url": "", "title": "{keyword}", "table_of_contents": [], "raw_text": "No Wikipedia page found."\n\n'

    title = results[0]["title"]

    # Fetch parsed page content
    page_params = {"action": "parse", "page": title, "format": "json", "prop": "text|sections", "formatversion": 2}
    r = requests.get(API_URL, headers=HEADERS, params=page_params, timeout=10)
    parsed = r.json().get("parse", {})

    url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
    toc = [sec["line"] for sec in parsed.get("sections", [])]
    html_text = parsed.get("text", "")

    clean_text = clean_wiki_html(html_text)

    # Format the output to match your example
    toc_str = json.dumps(toc, ensure_ascii=False)
    clean_text = clean_text.replace('"', '\\"')  # escape quotes for JSON consistency

    formatted = (
        f"\"url\":\"{url}\","
        f"\"title\":\"{title}\","
        f"\"table_of_contents\":{toc_str},"
        f"\"raw_text\":\"{clean_text}\"\n\n"
    )
    return formatted


###########################################################################################################
##################################  5. SCRAPE AND SAVE  ###################################################
###########################################################################################################

dataset_folder = os.getenv("DATASET_STORAGE_FOLDER")
data_path = os.path.join(dataset_folder, "data.txt")
snapshot_file = os.getenv("SNAPSHOT_STORAGE_FILE")

if not os.path.isfile(snapshot_file):
    snapshot_id = str(uuid.uuid4())
    with open(snapshot_file, "w") as f:
        f.write(snapshot_id)
    print(f"🆕 Created snapshot ID: {snapshot_id}")
else:
    snapshot_id = open(snapshot_file).read().strip()
    print(f"🗂️ Using existing snapshot ID: {snapshot_id}")

print("\n📊 Starting Wikipedia structured scraping...\n")

with open(data_path, "w", encoding="utf-8") as out:
    for _, row in keywords.iterrows():
        kw = str(row["Keyword"]).strip()
        if not kw:
            continue
        print(f"🔍 Fetching {kw} ...")
        try:
            entry = fetch_article(kw)
            out.write(entry)
        except Exception as e:
            msg = str(e).replace('"', "'")
            out.write(f'"url": "", "title": "{kw}", "table_of_contents": [], "raw_text": "Error: {msg}"\n\n')
        time.sleep(0.5)

print(f"\n✅ Done! Structured text saved to: {data_path}")
