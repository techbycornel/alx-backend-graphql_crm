from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    """
    Weekly CRM Report: total customers, total orders, total revenue.
    Logs results to /tmp/crm_report_log.txt
    """
    # Configure GraphQL transport
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql/",  # adjust if your server runs elsewhere
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query
    query = gql("""
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
    """)

    try:
        result = client.execute(query)
        customers = result.get("totalCustomers", 0)
        orders = result.get("totalOrders", 0)
        revenue = result.get("totalRevenue", 0)

        log_message = (
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
            f"Report: {customers} customers, {orders} orders, {revenue} revenue\n"
        )

        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(log_message)

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{datetime.now()} - ERROR: {str(e)}\n")
