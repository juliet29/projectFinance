from collections import OrderedDict

months = range(1,25)


# payments at financial close  
fc_costs = {
    "Land": 12.5e6,
    "Development Expenses": 28.5e6,
    "Development Fees": 14.7e6,
    "Closing Costs" : 14.392e6,
    "Contingency Fees": 30.754e6
}

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