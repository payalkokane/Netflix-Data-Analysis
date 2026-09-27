# Netflix Data Analysis Dashboard

A Streamlit dashboard for exploring Netflix viewing activity, customer ratings, subscriptions, and revenue. It includes interactive filters, six charts, and CSV upload support.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

The dashboard loads `Netflix.csv` by default. To analyze another dataset, use **Upload dataset** in the sidebar and select a CSV file.

Uploaded CSV files must include these columns:

`Customer_ID`, `Region`, `Subscription_Plan`, `Category`, `Type`, `Rating`, `Watch_Count`, `Watch_Date`, `Watch_Time_Minutes`, `Device`, and `Monthly_Revenue`.

The `images/` folder contains the artwork used in the dashboard.