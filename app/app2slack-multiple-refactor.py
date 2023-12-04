from google.cloud import bigquery
import time
import pandas as pd
from slack_sdk import WebClient
import logging, os
from weasyprint import HTML,CSS


html_file_name = "test-name.html"
csv_file_name = "test-name.csv"
pdf_file_name = "FinalOutput.pdf"

# Define the BigQuery SQL query to retrieve the data
query1 = f"""
    SELECT 
     logName,
     resource.type,
     textPayload,
     severity,
     insertId,
    FROM `{os.environ["TABLE"]}` 
    LIMIT 3;
    SELECT 
     logName,
     resource.type,
     trace,
     severity,
    FROM `{os.environ["TABLE"]}` 
    LIMIT 3;
"""

query2 = f"""
    SELECT 
     logName,
     resource.type,
     trace,
     severity,
    FROM `{os.environ["TABLE"]}` 
    LIMIT 3;
"""

query3 = f"""
    SELECT 
     logName,
     resource.type,
     insertId,
     severity,
    FROM `{os.environ["TABLE"]}` 
    LIMIT 3;
"""

queries = [query1, query2, query3]
report_names = ["Query1", "Query2", "Query3"]

slack_token = os.environ["SLACK_BOT_TOKEN"]


def query_to_pdf(query, report_name):
    bigqueryClient = bigquery.Client()
    

    df = bigqueryClient.query(query).result().to_dataframe()
    df.to_csv(csv_file_name, index=False)

    
    CSV = pd.read_csv(csv_file_name)
    # CSV.to_html(html_file_name).replace('<tr>','<tr style="text-align: right;">')  
    CSV.to_html(html_file_name)
    htmldoc = HTML(html_file_name).write_pdf( pdf_file_name, stylesheets=[CSS(string='body { font-family: Times New Roman; font-size: 10px; } table { background-color:#F4FAF9;border-collapse:collapse;} td,th { padding:5px;border:1px solid;} th { background-color:#05D7CC;} @page {size: Letter;  margin: 0in 0.44in 0.2in 0.44in; }')])
    print(f"{report_name} converted to pdf")

def slack_push(report_name):
    slack_client = WebClient(slack_token)

    # Sets the debug level. 
    # If you're using this in production, you can change this back to INFO and add extra log entries as needed.
    # logging.basicConfig(level=logging.DEBUG)

    upload_text_file = slack_client.files_upload(
        channels="#general",
        title=f"Bigquery {report_name} result",
        file=pdf_file_name,
        #initial_comment=f"{report_name} file:",
    )
    print(f"{report_name} pushed to slack channel")


def main():
    for query, report_name in zip(queries, report_names):
         query_to_pdf(query, report_name)
         slack_push(report_name)    


if __name__ == '__main__':
    main()