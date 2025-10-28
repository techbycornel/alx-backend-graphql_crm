import datetime, requests

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    try:
        res = requests.post("http://localhost:8000/graphql", json={"query": "{ hello }"})
        status = "OK" if res.status_code == 200 else "FAIL"
    except Exception:
        status = "FAIL"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{timestamp} CRM is alive - {status}\n")


def update_low_stock():
    import requests, datetime
    query = """
    mutation {
      updateLowStockProducts {
        success
        updated
      }
    }
    """
    res = requests.post("http://localhost:8000/graphql", json={"query": query})
    data = res.json().get("data", {}).get("updateLowStockProducts", {})
    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {data}\n")
