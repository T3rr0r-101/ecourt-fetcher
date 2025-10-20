import click
from ecourt_client import post_search_cnr, parse_case_from_html, download_pdf, date_str
import json, os

@click.group()
def cli(): pass

@cli.command()
@click.option("--cnr", help="CNR number (preferred)")
@click.option("--case-type", help="Case type (if using non-CNR search)")
@click.option("--case-no", help="Case number")
@click.option("--year", help="Year")
@click.option("--today", is_flag=True)
@click.option("--tomorrow", is_flag=True)
@click.option("--pdf", is_flag=True)
def case(cnr, case_type, case_no, year, today, tomorrow, pdf):
    day = "today" if today else "tomorrow"
    if not cnr:
        print("Currently this demo requires --cnr. Add parsing for case-type flows.")
        return
    html = post_search_cnr(cnr)
    info = parse_case_from_html(html)
    info["queried_on"] = date_str(day)
    print(json.dumps(info, indent=2, ensure_ascii=False))
    out = os.path.join("data", f"{cnr}_{day}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    print("Saved:", out)
    if pdf and info.get("pdf_url"):
        path = download_pdf(info["pdf_url"], f"{cnr}_{day}.pdf")
        print("Downloaded PDF to", path)

@cli.command()
@click.option("--court-id", required=True, help="Court identifier discovered from cause list UI")
@click.option("--today", is_flag=True)
@click.option("--tomorrow", is_flag=True)
def causelist(court_id, today, tomorrow):
    day = "today" if today else "tomorrow"
    url = f"{BASE}/?p=cause_list/get_cause_list"
    payload = {"court_id":court_id, "date": date_str(day)}
    r = session.post(url, data=payload)
