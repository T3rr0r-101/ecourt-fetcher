import requests
from datetime import datetime, timedelta
import json, os
import click
from rich.console import Console

console = Console()
BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0"}

def save_json(data, filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    console.print(f"[green]Saved results to {path}[/green]")

def download_pdf(url, filename):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
        path = os.path.join(DATA_DIR, filename)
        with open(path, "wb") as f:
            f.write(response.content)
        console.print(f"[green]Downloaded PDF:[/green] {path}")
        return path
    else:
        console.print("[red]PDF not available[/red]")
        return None

def fetch_case_listing(cnr=None, case_type=None, case_no=None, year=None, date=None):
    target_date = date or datetime.now()
    date_str = target_date.strftime("%d-%m-%Y")
    console.print(f"[cyan]Fetching case info for {date_str}...[/cyan]")

    session = requests.Session()
    session.headers.update(HEADERS)

    # Official JSON endpoint for case details
    api_url = BASE_URL + "casestatus/casestatus_search"
    payload = {"cnr": cnr} if cnr else {"case_type": case_type, "case_no": case_no, "year": year}

    try:
        r = session.post(api_url, data=payload)
        data = r.json()
    except Exception:
        console.print("[red]Failed to fetch case details from eCourts API[/red]")
        data = {}

    case_details = {
        "listed_on": date_str,
        "cnr": cnr or data.get("cnr"),
        "case_type": case_type or data.get("case_type"),
        "case_no": case_no or data.get("case_no"),
        "year": year or data.get("year"),
        "court_name": data.get("court_name"),
        "serial_no": data.get("serial_no"),
        "pdf_url": data.get("pdf_url")
    }

    save_json(case_details, f"listing_{date_str}.json")
    return case_details

def fetch_cause_list(date=None):
    target_date = date or datetime.now()
    date_str = target_date.strftime("%d-%m-%Y")
    console.print(f"[cyan]Fetching cause list for {date_str}...[/cyan]")

    session = requests.Session()
    session.headers.update(HEADERS)

    cause_list_url = BASE_URL + f"causelist/pdf?date={date_str}"
    download_pdf(cause_list_url, f"cause_list_{date_str}.pdf")

def parse_date(today, tomorrow, days, date):
    if today:
        return datetime.now()
    elif tomorrow:
        return datetime.now() + timedelta(days=1)
    elif days is not None:
        return datetime.now() + timedelta(days=days)
    elif date:
        for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(date, fmt)
            except ValueError:
                continue
        console.print("[red]Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY[/red]")
        raise SystemExit
    else:
        return datetime.now()

@click.group()
def cli():
    pass

@cli.command()
@click.option("--cnr", help="Case CNR number")
@click.option("--case-type", help="Case type (e.g. WP, CR, etc.)")
@click.option("--case-no", help="Case number")
@click.option("--year", help="Year of case")
@click.option("--today", is_flag=True)
@click.option("--tomorrow", is_flag=True)
@click.option("--date", type=str)
@click.option("--days", type=int)
@click.option("--pdf", is_flag=True)
def case(cnr, case_type, case_no, year, today, tomorrow, date, days, pdf):
    target_date = parse_date(today, tomorrow, days, date)
    result = fetch_case_listing(cnr, case_type, case_no, year, date=target_date)
    console.print("[bold green]Case Details:[/bold green]")
    console.print(json.dumps(result, indent=4))
    if pdf and result.get("pdf_url"):
        filename = f"{(cnr or f'{case_type}-{case_no}-{year}')}_{target_date.strftime('%d-%m-%Y')}.pdf"
        download_pdf(result["pdf_url"], filename)

@cli.command()
@click.option("--today", is_flag=True)
@click.option("--tomorrow", is_flag=True)
@click.option("--date", type=str)
@click.option("--days", type=int)
def causelist(today, tomorrow, date, days):
    target_date = parse_date(today, tomorrow, days, date)
    fetch_cause_list(date=target_date)

if __name__ == "__main__":
    cli()
