# Construction inputs 
from wbsetup import *
from data import *

# ============================================================================ #
# ! Financial close costs 

ws_const_in.merge_range('A4:B4', 'Costs Paid at Financial Close', merge_format)

# keep track of rows 
refd["cpi"] = {}
refd["cpi"]["heading_row"] = xl_cell_to_rowcol('A4') 

# financial close inputs 
row = refd["cpi"]["heading_row"][0]+1
refd["cpi"]["fc_sr"] = row
col = 0
for k,v in fc_costs.items():
    ws_const_in.write(row, col, k)
    ws_const_in.write(row, col+1, v, money_format)
    row += 1



# ============================================================================ #
# ! Costs Paid over Construction Period 


# skip a row to make header 
row+=1
ws_const_in.merge_range(row, 0, row, 1, 'Costs Paid Over Construction Period', merge_format)

# EPC costs TODO make this its own dictionary 
row+=1
refd["cpi"]["epc_sr"] = row 
ws_const_in.write(row, col, "EPC Cost")
ws_const_in.write(row, col+1, epc_cost)

# split costs 
row+=1
refd["cpi"]["split_sr"] = row
for k,v in split_costs.items():
    ws_const_in.write(row, col, k)
    ws_const_in.write(row, col+1, v, money_format)
    row += 1


# ============================================================================ #
# ! EPC Payment Shchedule 

# skip a row to make header 
row+=1
ws_const_in.merge_range(row, 0, row, 1, 'EPC Payment Schedule', merge_format)

row+=1
ws_const_in.write(row, 0, "EPC Contract Month", bold_format)
ws_const_in.write(row, 1, "Max. Payment, as percentage of total EPC price", bold_format)

row+=1
refd["cpi"]["epc_perc_sr"] = row
for k,v in epc_sched.items():
    ws_const_in.write(row, 0, k)
    ws_const_in.write(row, 1, v, )#percent_format
    row += 1