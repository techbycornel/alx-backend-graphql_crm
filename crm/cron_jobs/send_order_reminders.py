#!/usr/bin/env python3
import requests, datetime

query = """
{
  orders(orderDate_Gte: "%s") {
    id
    customer {
      email
    }
  }
}
""" % ((datetime.date.today() - datetime.timedelta(days=7)).isoformat())

response = requests.post("http://localhost:8000/graphql", json={"query": query})
orders = response.json().get("data", {}).get("orders", [])

with open("/tmp/order_reminders_log.txt", "a") as f:
    for order in orders:
        f.write(f"{datetime.datetime.now()} - Order {order['id']} -> {order['customer']['email']}\n")

print("Order reminders processed!")
