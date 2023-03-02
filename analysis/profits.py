import pandas as pd
import numpy as np
from data import * 
from expenses import * 
from revenues import * 

# ============================================================================ #
# ! Expenses

debt_service_exp = debt_service_df.loc["Total"]
corp_exp = corp_df.loc[("Total", "")]
op_exp = op_df.loc[("Total", "")]
summ_df = pd.DataFrame([corp_exp, op_exp, debt_service_exp, ], index=["Corporate Expenses", "Operations Expenses", "Debt Service"])


# ~ Summarize construction costs 
year_1 = const_df.iloc[const_df.index.get_level_values(0)=="Total", 2:14].sum(axis=1).values[0]

year_2 = const_df.iloc[const_df.index.get_level_values(0)=="Total", 14:].sum(axis=1).values[0]

by_fc = const_df.iloc[const_df.index.get_level_values(0)=="Total", 0:2].sum(axis=1).values[0]

const_costs = len(summ_df.columns)*[0]
const_costs[0] = by_fc
const_costs[1] = year_1
const_costs[2] = year_2
const_exp = pd.DataFrame(const_costs, index=list(summ_df.columns), columns=["Construction Expenses"]).T

summary_df = pd.concat(objs=[const_exp, summ_df])

# ~ Hipu Escrow
summary_df.loc["HIPU Escrow*"] = hipu_escrow_full

# ~ Summary total expenses
summary_df.loc["Total Expenses"] = summary_df.sum(axis=0)

# ============================================================================ #
# ! Income

summary_df.loc["Revenues"] = rev_df.loc["Total"].T # TODO expenses should be negative! 

summary_df.loc["Net Income"] = summary_df.loc["Revenues"] - summary_df.loc["Total Expenses"]


# ============================================================================ #
# ! Taxes
summary_df.loc["Corporate Tax Payable"] = summary_df.loc["Net Income"]*corp_tax_rate

summary_df.iloc[-1, 0:4] = 0

summary_df.loc["After Tax Income"] = summary_df.loc["Net Income"] - summary_df.loc["Corporate Tax Payable"]