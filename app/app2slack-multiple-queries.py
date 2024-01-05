from google.cloud import bigquery
from google.cloud import secretmanager
import time
import pandas as pd
from slack_sdk import WebClient
import logging, os
from weasyprint import HTML, CSS

html_file_name = "test-name.html"
csv_file_name = "combined_output.csv"
pdf_file_name = "FinalOutput.pdf"

# Define the BigQuery SQL query to retrieve the data
queries = [
    f"""
    SELECT 
     logName,
     resource.type,
     textPayload,
     severity,
     insertId,
    FROM `{os.environ["TABLE"]}` 
    LIMIT 3;
    """,
    f"""
    SELECT 
     logName,
     resource.type,
     trace,
     severity,
    FROM `{os.environ["TABLE"]}` 
    LIMIT 3;
    """,
    f"""
    SELECT 
     logName,
     resource.type,
     insertId,
     severity,
    FROM `{os.environ["TABLE"]}` 
    LIMIT 3;    
    """]

report_names = ["Query1", "Query2", "Query3"]

#slack_token = os.environ["SLACK_BOT_TOKEN"]

#retrieve slack_token

# project_number = "976036132338"
# secret_name = "slack_token"
# secret_version = "latest"

# def slack_secret(project_number, secret_name, secret_version):
#     client = secretmanager.SecretManagerServiceClient()

#     name = client.secret_version_path(
#             project=project_number,
#             secret=secret_name,
#             secret_version=secret_version
#         )
#     payload = client.access_secret_version(name=name).payload.data.decode("utf-8")

#     return payload

# slack_token = slack_secret(project_number, secret_name, secret_version)


def query_to_pdf(queries):
    bigqueryClient = bigquery.Client()

    # Initialize an empty list to store DataFrames
    result_dfs = []

    # Execute queries and store results as DataFrames
    for query in queries:
        query_job = bigqueryClient.query(query)
        result_df = query_job.result().to_dataframe()
        result_dfs.append(result_df)

    # Concatenate DataFrames along axis 1 (columns) to form a single DataFrame
    final_result = pd.concat(result_dfs)

    # Save the final DataFrame to a CSV file 
    # Change 'combined_output.csv' to your desired file name

    final_result.to_csv(csv_file_name, index=False)
   
    CSV = pd.read_csv(csv_file_name)
    CSV.to_html(html_file_name)
    htmldoc = HTML(html_file_name).write_pdf( pdf_file_name, stylesheets=[CSS(string='body { font-family: Times New Roman; font-size: 10px; } table { background-color:#F4FAF9;border-collapse:collapse;} td,th { padding:5px;border:1px solid;} th { background-color:#05D7CC;} @page {size: Letter;  margin: 0in 0.44in 0.2in 0.44in; }')])
    #print(f"{report_name} converted to pdf")

# def slack_push(report_name):
#     slack_client = WebClient(slack_token)

#     # Sets the debug level. 
#     # If you're using this in production, you can change this back to INFO and add extra log entries as needed.
#     # logging.basicConfig(level=logging.DEBUG)

#     upload_text_file = slack_client.files_upload(
#         channels="#general",
#         title=f"Bigquery {report_name} result",
#         file=pdf_file_name,
#         #initial_comment=f"{report_name} file:",
#     )
#     print(f"{report_name} pushed to slack channel")



def main():
    # for query, report_name in zip(queries, report_names):
          query_to_pdf(queries)
        #  slack_push(report_name)    


if __name__ == '__main__':
    main()