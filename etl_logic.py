import pandas as pd
from google.cloud import bigquery
from koboextractor import KoboExtractor

def extract_data(api_key, end_point, form_id):
    kobo = KoboExtractor(api_key, end_point)
    results = kobo.get_data(asset_uid=form_id).get('results')
    return pd.DataFrame(results)

def transform_data(df):
    # Drop duplicates
    df = df.drop_duplicates(subset=['daycare_name'], keep='first')
    # Shorten column names
    df.columns = df.columns.str.split('/').str[-1]
    # Rename columns
    columns_dict = {
        'kidogo_code': 'Code',
        'county': 'County',
        'subcounty': 'SubCounty',
        'ward': 'Ward',
        'daycare_name': 'CenterName',
        'center_type': 'CenterType',
        'workshop_date': 'WorkshopDate',
        'MMP_joining_QIP': 'MMPJoiningQIP'
    }
    return df.rename(columns=columns_dict)

def load_to_bigquery(df, table_id):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
