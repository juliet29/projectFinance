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

# # tax deductible debt service payments 
# taxable_debt_payments = debt_service_df.loc["Interest Payment"] + debt_service_df.loc["Fees"]
# taxable_debt_payments

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
# # ! Depreciation 
# depreciation on assets and capx 
substation_value = 100*corporate_costs["Other Annual Costs"]["Property Taxes"][0]
capx = epc_data["EPC Cost"]

depreciable_assets = property_value + init_capx
annual_dep = depreciable_assets/straight_line_dep_term
term_dep = [annual_dep]*20


dep_df = pd.DataFrame([term_dep], columns=year_col_names[0:20], index=["Depreciation"])