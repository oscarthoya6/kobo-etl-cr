import pandas as pd
from google.cloud import bigquery
from koboextractor import KoboExtractor

def extract_data(api_key, end_point, form_id):
    kobo = KoboExtractor(api_key, end_point)
    results = kobo.get_data(asset_uid=form_id).get('results')
    df = pd.DataFrame(results)

    # Shorten column names
    df.columns = df.columns.str.split('/').str[-1]

    # Drop problematic nested/struct columns
    drop_cols = ['_attachments', '_geolocation', '_tags', '_notes', '_validation_status']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    return df


def transform_data(df):
    if 'daycare_name' in df.columns:
        df = df.drop_duplicates(subset=['daycare_name'], keep='first')
    else:
        df = df.drop_duplicates()

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
    print("✅ Data loaded into BigQuery:", table_id)
