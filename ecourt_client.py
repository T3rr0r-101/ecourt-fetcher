import requests, time, json, os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

BASE = "https://services.ecourts.gov.in/ecourtindia_v6"
HEADERS = {"User-Agent":"Mozilla/5.0 (compatible)"}
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)

def date_str(day="today"):
    d = datetime.now() if day=="today" else datetime.now() + timedelta(days=1)
    return d.strftime("%d-%m-%Y")

def post_search_cnr(cnr):
    """Example: emulate the POST/GET that returns case details for a CNR."""
    url = f"{BASE}/?p=casestatus/casestatus_search"   # <-- example placeholder
    payload = {"cnr": cnr}
    r = session.post(url, data=payload, timeout=15)
    r.raise_for_status()
    return r.text

def parse_case_from_html(html):
    """Parse HTML and extract court name, serial number, pdf link."""
    soup = BeautifulSoup(html, "lxml")
    case_block = soup.select_one(".case-result") or soup
    court = case_block.select_one(".court-name")
    serial = case_block.select_one(".serial-no")
    pdf_a = case_block.find("a", href=lambda h: h and ".pdf" in h)
    return {
        "court_name": court.get_text(strip=True) if court else None,
        "serial_no": serial.get_text(strip=True) if serial else None,
        "pdf_url": pdf_a["href"] if pdf_a else None,
        "raw_html_sample": (str(case_block)[:200] if case_block else None)
    }

def download_pdf(url, outname):
    if not url:
        return None
    if url.startswith("/"):
        url = "https://services.ecourts.gov.in" + url
    r = session.get(url, stream=True, timeout=30)
    if r.status_code == 200 and 'application/pdf' in r.headers.get('Content-Type','').lower():
        path = os.path.join(DATA_DIR, outname)
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024*64):
                f.write(chunk)
        return path
    return None
