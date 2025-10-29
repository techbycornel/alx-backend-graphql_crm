from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes and checks GraphQL hello query."""
    log_path = "/tmp/crm_heartbeat_log.txt"
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    try:
        # Configure the GraphQL client
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Optional GraphQL query to verify the hello field
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
