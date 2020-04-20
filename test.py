import numpy as np
import requests
import json
import pandas as pd
from datetime import datetime
from datetime import timedelta
pd.options.display.float_format = '{:20,.2f}'.format
pd.set_option('display.max_colwidth', None)

url = "https://www.nseindia.com/market-data/exchange-traded-funds-etf"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.137"}

r = requests.get(url, headers=headers)
r.status_code
# df1=pd.DataFrame().from_records(r['data'])
