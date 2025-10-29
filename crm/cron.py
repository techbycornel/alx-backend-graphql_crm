from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime

def update_low_stock():
    """
    Calls the GraphQL mutation to update low stock products
    and logs the process to /tmp/low_stock_updates_log.txt
    """
    log_file = "/tmp/low_stock_updates_log.txt"

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=False,
            retries=3,
        )

        client = Client(transport=transport, fetch_schema_from_transport=True)

        # GraphQL mutation
        query = gql("""
            mutation {
                updateLowStockProducts {
                    success
                    message
                }
            }
        """)

        response = client.execute(query)

        with open(log_file, "a") as log:
            log.write(f"{datetime.datetime.now()} - updateLowStockProducts executed successfully: {response}\n")

    except Exception as e:
        with open(log_file, "a") as log:
            log.write(f"{datetime.datetime.now()} - Error running updateLowStockProducts: {str(e)}\n")
