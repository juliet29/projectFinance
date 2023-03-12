import pandas as pd
import numpy as np
from data import * 
from expenses import * 

# ============================================================================ #
# ! Helper Functions 
def monthly_possible_pay(capacity, pay=pay):
    capacity_chunks = capacity/1000
    total_possible_pay = pay*capacity_chunks
    return total_possible_pay #  $/month...

# ============================================================================ #
# ! PPA

# inflation adjusted pay 
inflat_pay = [0]* len(year_nums)
inflat_pay[0] = pay


for i in year_nums[0:-1]:
    inflat_pay[i] = inflat_pay[i-1]*ppa_inflat_rate

# project ppa 
ppa_forecast = []
for pay in inflat_pay:
    ppa_forecast.append([monthly_possible_pay(i*capacity,pay) for i in target_avail])


col_names = year_col_names
months_in_year = pd.date_range('2025-01-01','2025-12-31', 
              freq='MS').strftime("%b").tolist()


ppa_df = pd.DataFrame(ppa_forecast, columns=months_in_year, index=col_names[3:]).T

ppa_df.loc["Total", :] = ppa_df.sum(axis=0)


