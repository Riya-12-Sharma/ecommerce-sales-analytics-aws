# E-Commerce Sales Analytics on AWS

A portfolio-ready starter project that analyzes order data through a Streamlit dashboard, with an optional AWS S3 + Lambda serverless summary API.

## Dashboard features
- Revenue, order count, units sold, and average order value KPIs
- Revenue trends over time
- Top products and category performance
- Regional sales comparison
- Filters by region and category
- CSV upload and export

## Stack
Python, Pandas, Streamlit, Plotly, Amazon S3, AWS Lambda, API Gateway, IAM, CloudWatch.

## Run locally
Use Python 3.10 or newer:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Dataset columns
`order_id, order_date, product, category, quantity, unit_price, region`

The included sample data is synthetic and for learning only.

## Optional AWS deployment
1. Review the current AWS Free Tier offer and your account's eligibility.
2. Set up billing notifications or a budget alert first; alerts are not hard spending caps.
3. Create a private S3 bucket and keep Block Public Access enabled.
4. Upload `data/orders.csv` as `orders.csv`.
5. Create a Lambda execution role with narrowly scoped `s3:GetObject` permission for this object and CloudWatch logging permissions.
6. Deploy `lambda/handler.py` as a Python Lambda function; set `DATA_BUCKET` to your bucket name and optionally `DATA_KEY`.
7. Test the Lambda in the AWS console.
8. Add API Gateway only after checking current pricing and eligibility. For real use, configure authorization and throttling; don't expose private business data through an unauthenticated endpoint.
9. Remove unused resources when finished to avoid unexpected charges.

The Streamlit dashboard runs locally in this starter version. Connecting the dashboard to API Gateway is a next-step enhancement. Never put AWS credentials in frontend code.

## Resume bullet
Use only after building and testing it: “Developed an e-commerce sales analytics dashboard using Python, Pandas, and Plotly to track revenue, order value, product performance, and regional trends, with an AWS S3 and Lambda serverless analytics component.”
