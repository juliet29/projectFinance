import pandas as pd
import numpy as np
from data import * 
from inputs import *


# make a copy 
const_df = const_phase_inputs.copy()
const_inputs = const_phase_inputs.copy()

# add columns for months and pre-fc 
col_names = ["Pre-Financial Close", "Financial Close - July 2023"]
# TODO add real months here!
month_names = [f"Month {i}" for i in months]
col_names = col_names + month_names


# empty list to initialize 
empty_list = len(const_df) * [0]


# initialize df 
for col in col_names:
    const_df[col] = empty_list

# drop the value column 
const_df.drop(columns=["Value"], inplace=True)

# ============================================================================ #
# ! calculations 

# pre- financial close
const_df.loc["Pre-Financial Close Expenses", "Pre-Financial Close"] = const_inputs.loc["Pre-Financial Close Expenses"]["Value"].values

# at financial close 
const_df.loc["Financial Close Expenses", "Financial Close - July 2023"] = const_inputs.loc["Financial Close Expenses"]["Value"].values


# monthly split expenses 
vals = const_inputs.loc["Construction Period Even Split Monthly Expenses"]["Value"].values

a = const_df.loc["Construction Period Even Split Monthly Expenses"].apply(lambda x: vals/12)

for i in const_df.loc["Construction Period Even Split Monthly Expenses"].index:
    const_df.loc[("Construction Period Even Split Monthly Expenses", i)] = a.loc[i]

const_df.loc["Construction Period Even Split Monthly Expenses", ["Pre-Financial Close", "Financial Close - July 2023"]] = 0

# construction expenses 
for ix, col in enumerate(const_df.columns):
    ix1 = "Construction Period Custom Schedule Monthly Expenses"
    ix2 = "EPC Cost"
    val = const_inputs.loc[(ix1, ix2), "Value"]

    offset = 1
    if ix <= offset:
        const_df.loc[(ix1, ix2), col]  = 0
    else:
        const_df.loc[(ix1, ix2), col]  = epc_sched[ix -1] * val


const_df.loc[("Total", ""), :] = const_df.sum(axis=0)