import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import json
import os
import requests
from ecourt import fetch_case_listing, fetch_cause_list, parse_date  # import your API functions

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_case_ui():
    cnr = cnr_entry.get().strip()
    case_type = case_type_entry.get().strip()
    case_no = case_no_entry.get().strip()
    year = year_entry.get().strip()
    date_input = date_entry.get().strip()
    
    if date_input:
        date_obj = parse_date(False, False, None, date_input)
    else:
        date_obj = datetime.now()
    
    result = fetch_case_listing(cnr, case_type, case_no, year, date=date_obj)
    if result:
        messagebox.showinfo("Case Details", json.dumps(result, indent=4))
        if pdf_var.get() and result.get("pdf_url"):
            filename = f"{(cnr or f'{case_type}-{case_no}-{year}')}_{date_obj.strftime('%d-%m-%Y')}.pdf"
            fetch_case_listing.download_pdf(result["pdf_url"], filename)
    else:
        messagebox.showerror("Error", "Failed to fetch case details.")

def fetch_cause_ui():
    date_input = cause_date_entry.get().strip()
    if today_var.get():
        date_obj = datetime.now()
    elif tomorrow_var.get():
        date_obj = datetime.now() + timedelta(days=1)
    elif date_input:
        date_obj = parse_date(False, False, None, date_input)
    else:
        date_obj = datetime.now()
    fetch_cause_list(date=date_obj)
    messagebox.showinfo("Success", f"Cause list fetched for {date_obj.strftime('%d-%m-%Y')}")

root = tk.Tk()
root.title("eCourts Fetcher")
root.geometry("500x500")

tab_control = ttk.Notebook(root)

case_tab = ttk.Frame(tab_control)
cause_tab = ttk.Frame(tab_control)

tab_control.add(case_tab, text='Case')
tab_control.add(cause_tab, text='Cause List')
tab_control.pack(expand=1, fill='both')

# --- Case Tab ---
tk.Label(case_tab, text="CNR:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
cnr_entry = tk.Entry(case_tab, width=30)
cnr_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(case_tab, text="Case Type:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
case_type_entry = tk.Entry(case_tab, width=30)
case_type_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(case_tab, text="Case No:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
case_no_entry = tk.Entry(case_tab, width=30)
case_no_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(case_tab, text="Year:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
year_entry = tk.Entry(case_tab, width=30)
year_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(case_tab, text="Date (DD-MM-YYYY):").grid(row=4, column=0, sticky='w', padx=10, pady=5)
date_entry = tk.Entry(case_tab, width=30)
date_entry.grid(row=4, column=1, padx=10, pady=5)

pdf_var = tk.BooleanVar()
tk.Checkbutton(case_tab, text="Download PDF", variable=pdf_var).grid(row=5, column=1, sticky='w', padx=10, pady=5)

tk.Button(case_tab, text="Fetch Case", command=fetch_case_ui).grid(row=6, column=1, pady=15)

# --- Cause List Tab ---
today_var = tk.BooleanVar()
tomorrow_var = tk.BooleanVar()
tk.Checkbutton(cause_tab, text="Today", variable=today_var).grid(row=0, column=0, sticky='w', padx=10, pady=5)
tk.Checkbutton(cause_tab, text="Tomorrow", variable=tomorrow_var).grid(row=0, column=1, sticky='w', padx=10, pady=5)

tk.Label(cause_tab, text="Date (DD-MM-YYYY):").grid(row=1, column=0, sticky='w', padx=10, pady=5)
cause_date_entry = tk.Entry(cause_tab, width=30)
cause_date_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Button(cause_tab, text="Fetch Cause List", command=fetch_cause_ui).grid(row=2, column=1, pady=15)

root.mainloop()
