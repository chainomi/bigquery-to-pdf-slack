from google.cloud import bigquery
from google.cloud import storage
import time
import pandas as pd
from slack_sdk import WebClient
import logging, os
from weasyprint import HTML,CSS


client = bigquery.Client()
storage_client = storage.Client()

# Define the BigQuery SQL query to retrieve the data
query1 = f"""
    SELECT 
     logName,
     resource.type,
     textPayload,
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
names = {
    "query1" : f"query1",
    "query2" : "query2",
    "query3" : "query3",
}


for query in queries:

    bigqueryClient = bigquery.Client()
    df = bigqueryClient.query(query).to_dataframe()
    df.to_csv("test-name.csv", index=False)

    CSV = pd.read_csv("test-name.csv")

    CSV.to_html("test-name.html")  

    htmldoc = HTML("test-name.html").write_pdf( "FinalOutput.pdf", stylesheets=[CSS(string='body { font-family: Times New Roman } table { background-color:#F4FAF9;border-collapse:collapse;} td,th { padding:5px;border:1px solid;} th { background-color:#05D7CC;} @page {size: Letter;  margin: 0in 0.44in 0.2in 0.44in; }')])

    slack_client = WebClient(os.environ["SLACK_BOT_TOKEN"])

    # Sets the debug level. 
    # If you're using this in production, you can change this back to INFO and add extra log entries as needed.
    logging.basicConfig(level=logging.DEBUG)

    upload_text_file = slack_client.files_upload(
        channels="#general",
        title=f"Bigquery the query result",
        file="./FinalOutput.pdf",
        initial_comment=f"Here is the query file:",
    )
    print(f"query pushed to slack channel")