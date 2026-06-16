from flask import Flask
import etl_logic

app = Flask(__name__)

@app.route("/", methods=["GET"])
def run_etl():
    api_key = "ac46f71db524c5a4dba2b12999c542cf149935fb"
    end_point = "https://kf.kobotoolbox.org/api/v2"
    form_id = "a9JtHkYwBhca4MbxfFsEmG"
    PROJECT_ID = "bigquery-test-project-466814"

    # Extract
    df_raw = etl_logic.extract_data(api_key, end_point, form_id)
    # Transform
    df_clean = etl_logic.transform_data(df_raw)

    # Load to BigQuery
    raw_table = f"{PROJECT_ID}.lake.workshop_attendance_raw"
    clean_table = f"{PROJECT_ID}.warehouse.workshop_attendance"

    etl_logic.load_to_bigquery(df_raw, raw_table)
    etl_logic.load_to_bigquery(df_clean, clean_table)

    return "ETL job completed successfully!"
