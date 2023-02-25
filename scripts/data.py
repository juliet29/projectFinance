from collections import OrderedDict
from xlsxwriter.utility import xl_rowcol_to_cell, xl_cell_to_rowcol
from icecream import ic

# ============================================================================ #
# ! Timing

months = range(1,25)

year_nums = range(0,40)
year_names = [f"{2025 + ix} - Year {ix}" for ix in year_nums]
year_names[0] = "Commisioning - 2025 - Year 0"

# ============================================================================ #
# ! Pre-Financial Close Costs 

# TODO
# permit for fed weetland construction 3M
# state enviro fee for monitoring during const, 800k at 

#
# ============================================================================ #
# ! Financial Close Costs 


# payments at financial close  
fc_costs = {
    "Land": 12.5e6,
    "Development Expenses": 28.5e6,
    "Development Fees": 14.7e6,
    "Closing Costs" : 14.392e6,
    "Contingency Fees": 30.754e6
}

# ============================================================================ #
# ! Construction Phase Costs 

# eng, procurement, const base cost 
epc_cost = 455e6
epc_data = {
        "epc_cost": 455e6
    }

# other payments over course of construction period 
split_costs = {
"Interest and Fees" : 56.853e6,
"Insurance and Fees" : 25e6,
"Management and Oversight ": 8.15e6
}


epc_sched = OrderedDict()

for i in list(months):
    if i <= 3:
        epc_sched[i] = 0.02
    elif i <= 8: 
        epc_sched[i] = 0.04
    elif i <= 14: 
        epc_sched[i] = 0.06
    elif i <= 18: 
        epc_sched[i] = 0.05
    else: 
        epc_sched[i] = 0.03


# ============================================================================ #
# ! Calculations



v = 10 # in reality, v is a ref to another sheet...
quarterly_calc = lambda v: [f"={v}*4" for i in year_names]
# quarterly_calc[0] = "={v}*2" july -> july so no need...

monthly_calc = lambda v:[f"={v}*12" for i in year_names]
# quarterly_calc[0] = "={v}*6"

annual_calc = lambda v:[f"={v}" for i in year_names]

one_time_calc = lambda v:["=0" if i > 0 else f"={v}"  for i in year_nums]
# one_time_calc[0] = f"={v}"

annual_calc_0_025 = lambda v:[f"={v}*1.025" for i in year_names] # each is supposed to ref the last... 

# def rising_calc(v, local_sr, local_sheet="Operat. Period Calcs", local_col=1):
#     # ic(v.split("!")[0])
#     sheet_ref = v.split("!")[0] + "!"
#     # sr, sc = xl_cell_to_rowcol(v.split("!")[1])
#     # ic(sr, sc)
#     # do #0
#     calcs = []
#     calcs.append(f"={v}")
#     for col in year_nums:
#         ic(col, local_col+col)
#         # ref cell NEEDS to be the cell that just got written in 
#         ref_cell = xl_rowcol_to_cell(local_sr+1, local_col + col)
#         # ic(ref_cell)
#         curr_cell = f"='{local_sheet}'!{ref_cell}*1.025"
#         # ic(curr_cell)
#         calcs.append(curr_cell)
#         # ic(len(calcs[0:-1]))

#     calcs_fin = calcs[0:-1]
#     ic(calcs_fin)
#     return calcs_fin


# fs = "Operat. Period Cost Inputs"
# v =  f"'{fs}'!B16"
# rising_calc(v)



# ============================================================================ #
# ! Commisioning Costs 

comm_fees = { # one time 
    "ABSCO Interconnection Fee": [2.5e6, one_time_calc],
    "ABSCO Network Upgrades": [5.2e6, one_time_calc],
    "HIPU Interconnection Fee": [2e6, one_time_calc]
}
comm_fees = OrderedDict(comm_fees)


# ============================================================================ #
# ! Operations Costs 

# TODO include notes about how these are going to be calculated 
# during operations and constructon 

other_fees = {
    "Quarterly MaintCo Maintennance Fee": [690e3, quarterly_calc], # quarterly during operations 
    "Annual Fisheries Mitigation Permit": [130e3, annual_calc], # annual (during operations?)
    "Monthly HIPU Interconection Fee, Decade 1": [110e3, monthly_calc], # monthly during oper.
    "Monthly HIPU Interconection Fee, Post-Decade 1": [220e3, monthly_calc] # monthly during oper
}
other_fees = OrderedDict(other_fees)

corporate_costs = { # annually during construction and operations, escalate w/ annual rate of inflation 2.5% starting in oper. phase 
    "General" : {
        "Corporate Resources": 1.9e6
    },
    "Outside Reources" : {
        "Engineering": 220e3,
        "Legal": 315e3,
        "Accounting": 180e3,
        "Community Relations": 80e3,
        "Industry Relations": 20e3,
        "Misc.": 50e3,
    },
    "Overhead": {
        "Station Power Service": 285e3,
        "Utilities": 65e3,
        "Rent": 82e3,
        "Telecommunications": 50e3,
        "Travel/Office": 260e3,
        "Misc.": 200e3,
        "Contingency": 120e3,
    },
    "Other Annual Costs": {
        "Insurance": 2.5e6,
        "Property Taxes": 2.55e6, # TODO does this account for the other property taxes, maybe move...?
        "Cable Easment": 700e3,
        "Contribution to Stanford Global Project Center": 25e3,
    }

}

for k,v in corporate_costs.items():
    for k2, v2 in v.items():
        corporate_costs[k][k2] = [v2, rising_calc]

corporate_costs = OrderedDict(corporate_costs)










# def rising_calc(fs, v, value_cell="A1"):
#     calcs = year_names
#     values = year_names
#     (row,col) = xl_cell_to_rowcol(value_cell)
#     for ix in year_nums:
#         if ix == 0:
#             calcs[ix] = v # row, col
#             values[ix] = v
#         else:
            
#             prev_cell = values[ix-1].split("!")
#             ic(prev_cell)
#             # calcs[ix] = f"='{fs}'!{prev_cell}*1.025"

#             # (row,col) = xl_cell_to_rowcol(prev_cell)
#             # curr_cell = xl_rowcol_to_cell(row, col+1)
#             # values[ix] = curr_cell
#             # cell = xl_rowcol_to_cell(row, col-1)
#     #         ic(cell)
#     #         calcs[ix] = f"='{fs}'!{cell}*1.025" # calcs[ix-1]*1.025
#     # ic(values)
#     return calcs
# fs = "Operat. Period Cost Inputs"
# v =  f"'{fs}'!B16"
# rising_calc( fs, v, value_cell="B16")