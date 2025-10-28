#!/bin/bash
# Delete inactive customers (no orders in the past year)
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting cleanup..." >> /tmp/customer_cleanup_log.txt

python3 manage.py shell <<END
from crm.models import Customer
from datetime import datetime, timedelta

cutoff = datetime.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff)
count = inactive_customers.count()
inactive_customers.delete()
print(f"{count} inactive customers deleted.")
END

echo "$(date '+%Y-%m-%d %H:%M:%S') - Cleanup complete." >> /tmp/customer_cleanup_log.txt
