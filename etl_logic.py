import pandas as pd
from google.cloud import bigquery
from koboextractor import KoboExtractor

def extract_data(api_key, end_point, form_id):
    """
    Extract data from KoboToolbox and return a raw dataframe
    with shortened column names.
    """
    kobo = KoboExtractor(api_key, end_point)
    results = kobo.get_data(asset_uid=form_id).get('results')
    df = pd.DataFrame(results)

    # Shorten column names immediately after extraction
    df.columns = df.columns.str.split('/').str[-1]

    return df


def transform_data(df):
    """
    Transform the raw dataframe:
    - Drop duplicates (based on daycare_name if available)
    - Rename columns to clean schema
    """
    # Drop duplicates safely
    if 'daycare_name' in df.columns:
        df = df.drop_duplicates(subset=['daycare_name'], keep='first')
    else:
        df = df.drop_duplicates()

    # Rename columns to standardized names
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
    """
    Load a dataframe into BigQuery, overwriting the table.
    """
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
