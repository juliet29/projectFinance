import pandas as pd
import numpy as np
from model import * 
from tabulate import tabulate

# base case
a = FinancialModel()
a.run_base_case()
print(a.roe) # 3.76

total_const_expense = a.construction_expense_df.loc["Total", :].sum(axis=1)/1e6

print(tabulate(a.format_df(a.construction_expense_df).iloc[:, 0:5], headers='keys', tablefmt='psql'))

print(a.construction_expense_df.loc[("Total", ""), :].sum()/1e6)


print(tabulate(a.format_df(a.corporate_expense_df, 3).iloc[:, 0:3], headers='keys', tablefmt='psql'))

print(tabulate(a.format_df(a.df_out, 3).iloc[:, 0:3], headers='keys', tablefmt='psql'))


# =Inputs!$B$29/Inputs!$E$29