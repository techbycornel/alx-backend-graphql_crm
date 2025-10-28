import datetime, requests

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

def log_crm_heartbeat():
    """Log heartbeat and optionally verify GraphQL hello query."""
    log_path = "/tmp/crm_heartbeat_log.txt"
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    try:
        # Try hitting the GraphQL hello endpoint
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("""
        query {
            hello
        }
        """)

        result = client.execute(query)
        message = result.get("hello", "GraphQL endpoint not responsive")
    except Exception as e:
        message = f"GraphQL check failed: {e}"

    with open(log_path, "a") as f:
        f.write(f"{now} CRM is alive — {message}\n")
