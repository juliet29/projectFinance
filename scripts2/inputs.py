from collections import OrderedDict
import pandas as pd
from data import * 
import numpy as np

# ============================================================================ #
# ! General Expenses 


def make_two_index_df(d_orig):
    d = d_orig.copy()
    # make entries into arrays
    for inner_dict in d.values():
        for k, v in inner_dict.items():
            inner_dict[k] = [v]
    # arrange the dictionary to have tuples 
    reform_d = {(outerKey, innerKey): values for outerKey, innerDict in d.items() for innerKey, values in innerDict.items()}
    # make the multi index dictionary 
    df = pd.DataFrame(reform_d, index=["Value"])
    df = df.T
    return df

# ! Construction Phase 
d = {
    "Pre-Financial Close Expenses": pre_fc_costs,
    "Financial Close Expenses": fc_costs,
    "Construction Period Even Split Monthly Expenses": monthly_split_costs,
    "Construction Period Custom Schedule Monthly Expenses": epc_data
}
const_phase_inputs = make_two_index_df(d)

# ! Operations Phase 
oper_d = {
    "Commisioning Fees": comm_fees,
    "Operating Fees to External Entities": other_fees
}
oper_phase_inputs = make_two_index_df(oper_d)

# ! Corporate Phase
corp_inputs = make_two_index_df(corporate_costs)


# ============================================================================ #
#  ! Debt 
ds = pd.read_csv("debt_service.csv", skiprows=[0,1], names=["Year", "Interest Payment", "Prinicpal Payment", "Fees"], dtype=np.float64)
ds = ds.T
