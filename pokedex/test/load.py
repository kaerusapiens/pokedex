from google.cloud import storage
from google.cloud import bigquery
import os
import yaml 

#Abosulte Path /pokedex
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent 

#Yamlロード
def read_yaml_config(file_path): 
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

config = read_yaml_config(BASE_DIR / 'config/config.ymal')

project_id = config.get('project_id')
dataset_id = config.get('dataset_id')
table_id = config.get('table_id')



# Set up BQ Clients
storage_client = storage.Client()
bigquery_client = bigquery.Client()
table_id = bigquery.Table()


# Define BigQuery table
client = bigquery.Client(project=project_id)
table_ref = client.dataset(dataset_id).table(table_id)


# Load DataFrame to BigQuery with auto-detection of schema
def load_df_to_bq(df, table_ref):
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",  # Options: WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY
    )

    try:
        # Initiate the load job
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        
        # Wait for the job to complete
        job.result()  
        
        # Print the number of rows loaded
        print(f"Loaded {job.output_rows} rows into {dataset_id}:{table_id}.")
    
    except Exception as e:
        # Handle other errors
        print(f"An unexpected error occurred: {e}")
