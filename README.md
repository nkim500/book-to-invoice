# Book-to-Invoice Streamlit Application

Upload the recordkeeping book to generatve your monthly invoice. This is the standalone version of the rent invoicing app. 

In a terminal, navigate to the local repo and enter `streamlit run main.py`

---
### Initializing

Before using the app, you will need to create a .csv file named `properties.csv` under `template` directory. This file expects the following 3 details for any properties you may want to invoice to, delimited by back slashes:
- Property code
- Street of the property
- City, state, zip code

A hypothetical line item in this file can look like this:
- ABC/Main Street/New York, NY 10001


---
### Workflow Overview:
1. Set the statement date for your invoice from the side bar
  - Defaults to first of the next month vs. today (i.e. statement date is automatically set to January 1, 2025 if today were December 25, 2024)
2. Upload the bookkeeping file via the Streamlit UI
3. Enter the worksheet name in the text input box to choose as the data source for invoicing
4. Upload the water usage report via the Streamlit UI
  - The usage reports are expected to be for a month-range ending one month before the statement date (i.e. for invoices with January 1, 2025 statement date, the water usages are expected to be for the period of November 1, 2024 ~ December 1, 2024)
5. Click `Generate Invoice` after which invoices in .xlsx format will appear in the invoices folder
  - You will also be given the option to download the composed invoices as a .zip file
