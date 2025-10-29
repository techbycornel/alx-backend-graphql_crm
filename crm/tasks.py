from celery import shared_task
from datetime import datetime
import requests

@shared_task
def generate_crm_report():
    try:
        # Example task logic (you can replace this with real report logic)
        response = requests.get("https://example.com/api/customers")
        data = response.json()

        # Log success
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{datetime.now()} - Successfully generated report with {len(data)} records\n")

    except Exception as e:
        # Log any errors
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{datetime.now()} - Error: {str(e)}\n")
        raise e
