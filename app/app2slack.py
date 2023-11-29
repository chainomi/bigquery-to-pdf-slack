from google.cloud import bigquery
from google.cloud import storage
import time
import pandas as pd
import pdfkit
from slack_sdk import WebClient
import logging, os
from weasyprint import HTML,CSS

# Authenticate with Google Cloud using a service account key

# client = bigquery.Client(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
# storage_client = storage.Client(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

client = bigquery.Client()
storage_client = storage.Client()

# Define the BigQuery SQL query to retrieve the data
query = f"""
    SELECT 
     logName,
     resource.type,
     textPayload,
     severity,
    FROM `{os.environ["TABLE"]}` 
    LIMIT 3;
"""

bigqueryClient = bigquery.Client()
df = bigqueryClient.query(query).to_dataframe()
df.to_csv("test-name.csv", index=False)

#https://stackoverflow.com/questions/31651171/export-bigquery-data-to-csv-without-using-google-cloud-storage



# cell_hover = {  # for row hover use <tr> instead of <td>
#     'selector': 'td:hover',
#     'props': [('background-color', '#ffffb3')]
# }
# index_names = {
#     'selector': '.index_name',
#     'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
# }
# headers = {
#     'selector': 'th:not(.index_name)',
#     'props': 'background-color: #000066; color: white;'
# }



# CSV = pd.read_csv("test-name.csv").style.set_table_styles([cell_hover, index_names, headers])
properties = {"border": "2px solid gray", "color": "green", "font-size": "16px"}

CSV = pd.read_csv("test-name.csv").style.set_properties(**properties)

CSV.to_html("test-name.html")  

htmldoc = HTML("test-name.html").write_pdf( "FinalOutput.pdf", stylesheets=[CSS(string='body { font-family: Times New Roman } table { background-color:#F4FAF9;border-collapse:collapse;} td,th { padding:5px;border:1px solid;} th { background-color:#05D7CC;} @page {size: Letter;  margin: 0in 0.44in 0.2in 0.44in; }')])
# options = {
#     'page-size': 'Letter',
#     'margin-top': '0.5in',
#     'margin-right': '0.5in',
#     'margin-bottom': '0.5in',
#     'margin-left': '0.5in',
#     'orientation': 'Landscape',
#     'zoom': '0.5'
# }

# pdfkit.from_url("test-name.html", "FinalOutput.pdf", options = options)


slack_client = WebClient(os.environ["SLACK_BOT_TOKEN"])


# Sets the debug level. 
# If you're using this in production, you can change this back to INFO and add extra log entries as needed.
logging.basicConfig(level=logging.DEBUG)


upload_text_file = slack_client.files_upload(
    channels="#general",
    title="Big query result",
    file="./FinalOutput.pdf",
    initial_comment="Here is the file:",
)