# API CALL
import pandas as pd
import numpy as np


# BookSnapshot 
# {
#   venue, 
#   product, 
#   sequence,
#   bids[], 
#   bid_quantity,
#   asks[],
#   ask_quantity,
#   exchange_ts, 
#   received_ts
# }


data = pd.read_json(api_call)
data.info()
data.loc[data.isna().any(axis="columns")]


# --------------------------------------------------
# 1. CLEAN DATA
# --------------------------------------------------

data = data.copy()

data["exchange_ts"] = pd.to_datetime(data["exchange_ts"], errors="coerce")
data["venue"] = data["venue"].str.lower().str.strip()
data["product"] = data["product"].str.lower().str.strip()

data["bids"] = pd.to_numeric(data["bids"], errors="coerce")
data["bid_quantity"] = pd.to_numeric(data["bid_quantity"], errors="coerce")
data["asks"] = pd.to_numeric(data["asks"], errors="coerce")
data["ask_quantity"] = pd.to_numeric(data["ask_quantity"], errors="coerce")

