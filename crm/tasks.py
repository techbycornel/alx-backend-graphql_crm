from celery import shared_task
import requests
import datetime

@shared_task
def generatecrmreport():
    try:
        # Example of what the report generation could do
        response = requests.get("https://example.com/api/customers")
        report_data = response.json()

        with open("/tmp/crmreportlog.txt", "a") as log_file:
            log_file.write(f"{datetime.datetime.now()} - Report generated successfully\n")
            log_file.write(f"Fetched {len(report_data)} customer records\n")

        return "CRM report generated and logged successfully."

    except Exception as e:
        with open("/tmp/crmreportlog.txt", "a") as log_file:
            log_file.write(f"{datetime.datetime.now()} - Error: {str(e)}\n")
        raise e
