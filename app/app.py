from google.cloud import bigquery
from google.cloud import storage
import time
import os

# Authenticate with Google Cloud using a service account key

# client = bigquery.Client(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
# storage_client = storage.Client(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

client = bigquery.Client()
storage_client = storage.Client()

# Define the BigQuery SQL query to retrieve the data
query = f"""
    SELECT *
    FROM `{os.environ["TABLE"]}`
    LIMIT 5
"""

# Define the destination URI where the query results will be stored in GCS
bucket_name = os.environ["BUCKET"]
timestamp = time.strftime("%Y%m%d-%H%M%S")
blob_name = f'result-{timestamp}.csv'
destination_uri = f'gs://{bucket_name}/{blob_name}'


# Run the query and export the results to GCS
query_job = client.query(query)
destination_blob = storage_client.bucket(bucket_name).blob(blob_name)
destination_blob.content_type = 'text/csv'
query_job.result().to_dataframe().to_csv(destination_blob.open('w'), index=False)


# Verify that the query results are exported to GCS
bucket = storage_client.get_bucket(bucket_name)
blob = bucket.get_blob(blob_name)
print(f'The query results are exported to {blob.public_url}')