import pandas as pd
import numpy as np
from data import * 
from expenses import * 
from revenues import * 

# ============================================================================ #
# ! Expenses




summ_df = pd.DataFrame([corp_exp, op_exp, debt_service_exp, ], index=["Corporate Expenses", "Operations Expenses", "Debt Service"])




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