from wbsetup import *
from data import *

# ============================================================================ #

# keep track of rows 
refd["oi"] = {}
# refd["oi"]["subheadings"] = {}
row = refd["gen_startrow"]

def make_input_section(row, name, dict):
    ws_op_in.merge_range(row, 0, row, 1, name, merge_format)
    row+=1
    refd["oi"][f"{name}_sr"] = row

    if depth(dict) == 1:
        for k,v in dict.items():
            ws_op_in.write(row, 0, k)
            ws_op_in.write(row, 1, v[0], money_format)
            row += 1
    else:
        for k,v in dict.items():
            # ws_op_in.write(row, 0, k, secondary_heading_format)
            ws_op_in.merge_range(row, 0, row, 1, k, secondary_heading_format)
            refd["oi"][f"{k}_sr"] = row
            row+=1
            for k2, v2 in v.items():
                ws_op_in.write(row, 0, k2)
                ws_op_in.write(row, 1, v2[0], money_format)
                row += 1
    return row

# TODO: include col for how often this is paid 

comm_er = make_input_section(row, 'Fees Paid at Commisioning', comm_fees)
op_fees_er = make_input_section(comm_er, 'General Operating Fees', other_fees)
corp_costs_er = make_input_section(op_fees_er, 'Corporate Costs', corporate_costs)
