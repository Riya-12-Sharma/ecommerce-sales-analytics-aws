"""AWS Lambda summary endpoint for orders stored in a private S3 bucket."""
import csv
import io
import json
import os
import boto3

s3 = boto3.client("s3")

def lambda_handler(event, context):
    bucket = os.environ["DATA_BUCKET"]
    key = os.environ.get("DATA_KEY", "orders.csv")
    response = s3.get_object(Bucket=bucket, Key=key)
    text = response["Body"].read().decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))

    revenue = 0.0
    order_ids = set()
    units = 0
    for row in rows:
        quantity = float(row.get("quantity") or 0)
        price = float(row.get("unit_price") or 0)
        revenue += quantity * price
        units += quantity
        order_ids.add(row.get("order_id"))

    count = len(order_ids)
    result = {
        "rows": len(rows),
        "orders": count,
        "units_sold": units,
        "total_revenue": round(revenue, 2),
        "average_order_value": round(revenue / count, 2) if count else 0
    }
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
