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

    # Export to Google Sheets
    sheet_name = "big query test"
    work_sheet_name = "workshop data"
    etl_logic.export_to_google_sheet(df_clean, sheet_name, work_sheet_name)

    return "ETL job completed successfully and exported to Google Sheets!"
