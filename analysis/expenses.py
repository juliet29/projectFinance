import pandas as pd
import numpy as np
from data import * 


# ============================================================================ #
# ! helper functions 

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

def make_two_index_df(d_orig):
    """ Make multi index dictionary """
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



# ============================================================================ #
# ! construction phase

# ~ prep data ----------
d = {
    "Pre-Financial Close Expenses": pre_fc_costs,
    "Financial Close Expenses": fc_costs,
    "Construction Period Even Split Monthly Expenses": monthly_split_costs,
    "Construction Period Custom Schedule Monthly Expenses": epc_data
}
const_phase_inputs = make_two_index_df(d)
const_df, const_inputs = prep_for_calcs(const_phase_inputs)



# ~ pre- financial close 
const_df.loc["Pre-Financial Close Expenses", "Pre-Financial Close"] = const_inputs.loc["Pre-Financial Close Expenses"]["Value"].values

# ~ at financial close 
const_df.loc["Financial Close Expenses", "Financial Close - July 2023"] = const_inputs.loc["Financial Close Expenses"]["Value"].values


# ~ monthly split expenses  
# get values from input dataframe
vals = const_inputs.loc["Construction Period Even Split Monthly Expenses"]["Value"].values

# perform calculatuation, expense is split evenly over months of the year 
a = const_df.loc["Construction Period Even Split Monthly Expenses"].apply(lambda x: vals/12)

# assign values to dataframe 
for i in const_df.loc["Construction Period Even Split Monthly Expenses"].index:
    const_df.loc[("Construction Period Even Split Monthly Expenses", i)] = a.loc[i]

# correction because payments are only during the construction period 
const_df.loc["Construction Period Even Split Monthly Expenses", ["Pre-Financial Close", "Financial Close - July 2023"]] = 0

# ~ EPC expenses 
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

# ~ prep data 
oper_d = {
    "Commisioning Fees": comm_fees,
    "Operating Fees to External Entities": other_fees
}
oper_phase_inputs = make_two_index_df(oper_d)
op_df, op_ref = prep_for_calcs(oper_phase_inputs, yearly=True)

# ~ one time commisioning fees 
op_df.loc["Commisioning Fees", "Commisioning and Construction Year 2 - July 2025"] = op_ref.loc["Commisioning Fees","Value"].values

# ~ quarterly payments to MaintCo 
op_df.iloc[op_df.index.get_level_values(1)=="Quarterly MaintCo Maintennance Fee", 3:] = op_ref.loc[("Operating Fees to External Entities", "Quarterly MaintCo Maintennance Fee"),"Value"]*4

# ~ annual fishery payments 
op_df.iloc[op_df.index.get_level_values(1)=="Annual Fisheries Mitigation Permit", 3:] = op_ref.loc[("Operating Fees to External Entities", "Annual Fisheries Mitigation Permit"),"Value"]

# ~ -- variable monthly interconnection fee 
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
# ~ prep data 
corp_inputs = make_two_index_df(corporate_costs)
corp_df, corp_ref = prep_for_calcs(corp_inputs, yearly=True)

# ~ calculations 
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
# ~ read in data 
ds = pd.read_csv("debt_service.csv", skiprows=[0,1], names=["Year", "Interest Payment", "Prinicpal Payment", "Fees"], dtype=np.float64)
ds = ds.T

# ~ make format fit 
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


debt_service_df.loc["Total", :] = debt_service_df.sum(axis=0)


# ~ HIPU Escrow 
hipu_escrow = [0]* len(year_nums)
hipu_escrow[0] = hipu_escrow_op


for i in year_nums[0:-1]:
    hipu_escrow[i] = hipu_escrow[i-1]*(1-annual_escrow_dec)

hipu_escrow2 = [-(hipu_escrow[0] - i) for i in hipu_escrow[1:]]
true_op_hipu_escrow = [hipu_escrow[0]] + hipu_escrow2
true_op_hipu_escrow

hipu_escrow_full = [hipu_escrow_fc, 0, 0] + true_op_hipu_escrow

