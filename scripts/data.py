from collections import OrderedDict

months = range(1,25)

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
# ! Commisioning Costs 

comm_fees = { # one time 
    "ABSCO Interconnection Fee": 2.5e6,
    "ABSCO Network Upgrades": 5.2e6,
    "HIPU Interconnection Fee": 2e6
}


# ============================================================================ #
# ! Operations Costs 

# TODO include notes about how these are going to be calculated 

# during operations and constructon 

other_fees = {
    "Quarely MaintCo Maintennance Fee": 690e3, # quarterly during operations 
    "Annual Fisheries Mitigation Permit": 130e3, # annual (during operations?)
    "Monthly HIPU Interconection Fee, Decade 1": 110e3, # monthly during oper.
    "Monthly HIPU Interconection Fee, Post-Decade 1": 220e3
}

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



