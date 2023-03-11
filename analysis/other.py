import pandas as pd
import numpy as np
from data import * 
from expenses import * 
from revenues import * 

"""Items that are neither direct expenses or revenues"""

# ============================================================================ #
# ! Debt Service 
# ~ read in data 
ds = pd.read_csv("debt_service.csv", skiprows=[0,1], names=["Year", "Interest Payment", "Prinicpal Payment", "Fees"], dtype=np.float64)
ds = ds.T

# ~ make format fit others...
debt_service = ds.copy()
col_names = make_year_col_names()
debt_service.insert(0, "newcol", [0]*4)
debt_service.insert(1, "newcol2", [0]*4)
debt_service = debt_service.set_axis(col_names[:23], axis=1, copy=True)
debt_service.drop("Year", axis=0, inplace=True)

# make length match other expense dataframes 
empty = len(debt_service)*[0]
empty_data = [empty for i in range(20)]
empty_df = pd.DataFrame(empty_data, index=col_names[23:], columns=debt_service.index).T
debt_service_df = pd.concat(objs=[debt_service, empty_df], axis=1)


# ============================================================================ #
# ~ HIPU Escrow 
hipu_escrow = [0]* len(year_nums)
hipu_escrow[0] = hipu_escrow_op


for i in year_nums[0:-1]:
    hipu_escrow[i] = hipu_escrow[i-1]*(1-annual_escrow_dec)

hipu_escrow2 = [-(hipu_escrow[0] - i) for i in hipu_escrow[1:]]
true_op_hipu_escrow = [hipu_escrow[0]] + hipu_escrow2
true_op_hipu_escrow

hipu_escrow_full = [hipu_escrow_fc, 0, 0] + true_op_hipu_escrow





# # ============================================================================ #
# # ! Expenses
# summ_df = pd.DataFrame([corp_exp, op_exp, debt_service_exp, ], index=["Corporate Expenses", "Operations Expenses", "Debt Service"])

# summary_df = pd.concat(objs=[const_exp, summ_df])

# # ~ Hipu Escrow
# summary_df.loc["HIPU Escrow*"] = hipu_escrow_full

# # ~ Summary total expenses
# summary_df.loc["Total Expenses"] = summary_df.sum(axis=0)

# # ============================================================================ #
# # ! Income

# summary_df.loc["Revenues"] = rev_df.loc["Total"].T # TODO expenses should be negative! 

# summary_df.loc["Net Income"] = summary_df.loc["Revenues"] - summary_df.loc["Total Expenses"]


# # ============================================================================ #
# # ! Taxes
# summary_df.loc["Corporate Tax Payable"] = summary_df.loc["Net Income"]*corp_tax_rate

# summary_df.iloc[-1, 0:4] = 0

# summary_df.loc["After Tax Income"] = summary_df.loc["Net Income"] - summary_df.loc["Corporate Tax Payable"]