from pytrends.request import TrendReq
import pandas as pd
from datetime import date, datetime


pytrend = TrendReq()
pytrend.build_payload(
    kw_list=["Corona", "Elections", "China", "Trump"],
    timeframe='today 1-m'
)

df = pytrend.interest_over_time()
print(df.head(n=30))