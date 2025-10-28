#!/usr/bin/env python3
import datetime
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
logging.basicConfig(
    filename="/tmp/orderreminderslog.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql/",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Define your GraphQL query
query = gql("""
query GetPendingOrders {
  orders(status: "pending") {
    id
    customer {
      email
      name
    }
    due_date
  }
}
""")

try:
    result = client.execute(query)
    orders = result.get("orders", [])
    logging.info(f"Found {len(orders)} pending orders.")

    for order in orders:
        email = order["customer"]["email"]
        name = order["customer"]["name"]
        due_date = order["due_date"]
        # Simulate sending reminder
        logging.info(f"Sent reminder to {name} ({email}) for order due {due_date}")

except Exception as e:
    logging.error(f"Error sending order reminders: {e}")
