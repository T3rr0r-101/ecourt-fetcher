eCourts Case & Cause List Fetcher

A Python project to fetch case listings and cause lists from eCourts using the official API. The project supports CLI and GUI (Tkinter), with options to download PDFs.

Features:

* Fetch individual case details by CNR or Case Type, Number, Year.
* Check listing for today, tomorrow, specific date, or N days later.
* Download case PDFs if available.
* Download entire cause list PDFs for selected dates.
* Save results as JSON in a local data/ folder.
* CLI and GUI interfaces for easy usage.

Installation:

1. Clone the repository:
   git clone [https://github.com/username/ecourts-fetcher.git](https://github.com/username/ecourts-fetcher.git)
   cd ecourts-fetcher

2. Create a Python virtual environment:
   python -m venv venv

3. Activate the virtual environment:
   Windows (PowerShell): .\venv\Scripts\Activate.ps1
   Linux/macOS: source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

Folder Structure:

* ui_ecourt.py        # Tkinter GUI
* cli.py              # Command-line interface
* ecourt.py           # API functions
* ecourt_client.py    # Low-level client functions
* data/               # JSON results and PDFs
* requirements.txt

Usage:

1. GUI (Tkinter):
   python ui_ecourt.py

   * Opens a window with two tabs: Case and Cause List.
   * Fill fields, select options, click Fetch.
   * JSON results and PDFs are saved to data/.

2. CLI (Command Line):
   Fetch a case:
   python cli.py case --cnr MHJK010012342022 --today --pdf

   Using case type, number, year:
   python cli.py case --case-type WP --case-no 123 --year 2025 --date 22-10-2025 --pdf

   Fetch cause list:
   python cli.py causelist --court-id 101 --today
   python cli.py causelist --court-id 101 --date 22-10-2025

Options:

| Option      | Description                                    |
| ----------- | ---------------------------------------------- |
| --cnr       | Case CNR number                                |
| --case-type | Case type (WP, CR, etc.)                       |
| --case-no   | Case number                                    |
| --year      | Year of case                                   |
| --today     | Fetch listing for today                        |
| --tomorrow  | Fetch listing for tomorrow                     |
| --date      | Fetch listing for a specific date (DD-MM-YYYY) |
| --days      | Fetch listing N days from today                |
| --pdf       | Download PDF if available                      |
| --court-id  | Court identifier for cause list                |

Dependencies:

* Python 3.10+
* requests
* click
* rich
* Tkinter (built-in)

Install all dependencies via:
pip install -r requirements.txt

Data Storage:
All JSON results and PDFs are saved in the data/ folder:

* listing_22-10-2025.json
* MHJK010012342022_22-10-2025.pdf
* cause_list_22-10-2025.pdf

Notes:

* Ensure a stable internet connection to fetch data.
* GUI runs on the main thread; large cause lists may take time to download.
* PDFs may not be available for all cases.
