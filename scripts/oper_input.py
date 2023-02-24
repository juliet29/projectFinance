from wbsetup import *
from data import *

# ============================================================================ #

# keep track of rows 
refd["oi"] = {}
row = refd["gen_startrow"]

def make_input_section(row, name, dict):
    ws_op_in.merge_range(row, 0, row, 1, name, merge_format)
    row+=1
    refd["oi"][f"{name}_sr"] = row

    for k,v in dict.items():
        # if type(v) != dict
        ws_op_in.write(row, 0, k)
        ws_op_in.write(row, 1, v, money_format)
        row += 1
    return row
# TODO: include col for how often this is paid 

comm_er = make_input_section(row, 'Fees Paid at Commisioning', comm_fees)
# op_fees_er = make_input_section(comm_er, 'General Operating Fees', other_fees)
# corp_costs_er = make_input_section(op_fees_er, 'Corporate Costs', corporate_costs)
