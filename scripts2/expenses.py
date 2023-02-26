import pandas as pd
import numpy as np
from data import * 
from inputs import *

def make_year_col_names():
        col_names = ["Financial Close - July 2023", "Construction Year 1 - July 2024", "Commisioning and Construction Year 2 - July 2025"]
        year_names = [f"July {2025 + ix} - Year {ix}" for ix in year_nums]
        col_names = col_names + year_names


        return col_names

def prep_for_calcs(df, yearly=False):
    # make a copy 
    df_df = df.copy()
    df_inputs = df.copy()

    if not yearly:
        # add columns for months and pre-fc 
        col_names = ["Pre-Financial Close", "Financial Close - July 2023"]
        # TODO add real months here!
        month_names = [f"Month {i}" for i in months]
        col_names = col_names + month_names
    else:
        col_names = ["Financial Close - July 2023", "Construction Year 1 - July 2024", "Commisioning and Construction Year 2 - July 2025"]
        year_names = [f"July {2025 + ix} - Year {ix}" for ix in year_nums]
        col_names = col_names + year_names


    # create empty list to initialize the dataframe 
    empty_list = len(df_df) * [0]

    # initialize df 
    for col in col_names:
        df_df[col] = empty_list

    # drop the value column 
    df_df.drop(columns=["Value"], inplace=True)

    return df_df, df_inputs


# ============================================================================ #
# ! construction phase

const_df, const_inputs = prep_for_calcs(const_phase_inputs)

# pre- financial close
const_df.loc["Pre-Financial Close Expenses", "Pre-Financial Close"] = const_inputs.loc["Pre-Financial Close Expenses"]["Value"].values

# at financial close 
const_df.loc["Financial Close Expenses", "Financial Close - July 2023"] = const_inputs.loc["Financial Close Expenses"]["Value"].values


# --- monthly split expenses  ---
# get values from input dataframe
vals = const_inputs.loc["Construction Period Even Split Monthly Expenses"]["Value"].values

# perform calculatuation, expense is split evenly over months of the year 
a = const_df.loc["Construction Period Even Split Monthly Expenses"].apply(lambda x: vals/12)

# assign values to dataframe 
for i in const_df.loc["Construction Period Even Split Monthly Expenses"].index:
    const_df.loc[("Construction Period Even Split Monthly Expenses", i)] = a.loc[i]

# correction because payments are only during the construction period 
const_df.loc["Construction Period Even Split Monthly Expenses", ["Pre-Financial Close", "Financial Close - July 2023"]] = 0

# --- EPC expenses  -----
for ix, col in enumerate(const_df.columns):
    # simplify code with these variables 
    ix1 = "Construction Period Custom Schedule Monthly Expenses"
    ix2 = "EPC Cost"
    # get the value of EPC from input dataframe 
    val = const_inputs.loc[(ix1, ix2), "Value"]

    # initial entries are 0, payments only occur during the construction period 
    offset = 1
    if ix <= offset:
        const_df.loc[(ix1, ix2), col]  = 0
    else:
        # reference the payment schedule 
        const_df.loc[(ix1, ix2), col]  = epc_sched[ix -1] * val

# calculate total per time period 
const_df.loc[("Total", ""), :] = const_df.sum(axis=0)


# ============================================================================ # 
# ! operations phase

op_df, op_ref = prep_for_calcs(oper_phase_inputs, yearly=True)

# one time commisioning fees 
op_df.loc["Commisioning Fees", "Commisioning and Construction Year 2 - July 2025"] = op_ref.loc["Commisioning Fees","Value"].values

# quarterly payments to MaintCo 
op_df.iloc[op_df.index.get_level_values(1)=="Quarterly MaintCo Maintennance Fee", 3:] = op_ref.loc[("Operating Fees to External Entities", "Quarterly MaintCo Maintennance Fee"),"Value"]*4

# annual fishery payments 
op_df.iloc[op_df.index.get_level_values(1)=="Annual Fisheries Mitigation Permit", 3:] = op_ref.loc[("Operating Fees to External Entities", "Annual Fisheries Mitigation Permit"),"Value"]

# -- variable monthly interconnection fee 
# decade one 
op_df.iloc[op_df.index.get_level_values(1)=="Monthly HIPU Interconection Fee, Decade 1", 3:3+10] = op_ref.loc[("Operating Fees to External Entities", "Monthly HIPU Interconection Fee, Decade 1"),"Value"]
# decade two 
op_df.iloc[op_df.index.get_level_values(1)=="Monthly HIPU Interconection Fee, Decade 1", 3+10:] = op_ref.loc[("Operating Fees to External Entities", "Monthly HIPU Interconection Fee, Post-Decade 1"),"Value"]
# rename
op_df.rename(index={'Monthly HIPU Interconection Fee, Decade 1': 'Monthly HIPU Interconection Fee'}, inplace=True)
# drop the other entry 
op_df.drop("Monthly HIPU Interconection Fee, Post-Decade 1", level=1, inplace=True)

# calculate total per time period 
op_df.loc[("Total", ""), :] = op_df.sum(axis=0)


# ============================================================================ # 
# ! corporate expenses 
corp_df, corp_ref = prep_for_calcs(corp_inputs, yearly=True)

# set year 1 equal to the appropriate value 
corp_df["Construction Year 1 - July 2024"] = corp_ref["Value"].values

# increase with inflation 
for col in corp_df.columns[2:]:
    curr_ix = corp_df.columns.get_loc(col)
    corp_df.iloc[:, curr_ix] = corp_df.iloc[:, curr_ix-1]*(1+inflation_rate)

# calculate total per time period 
corp_df.loc[("Total", ""), :] = corp_df.sum(axis=0)



# ============================================================================ #
# ! Debt Service 
ds2 = ds.copy()
col_names = make_year_col_names()
ds2.insert(0, "newcol", [0]*4)
ds2.insert(1, "newcol2", [0]*4)
ds2 = ds2.set_axis(col_names[:23], axis=1, copy=True)
ds2.drop("Year", axis=0, inplace=True)
