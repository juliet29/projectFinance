# Construction Calculations 

from wbsetup import *
from data import *
from const_input import * 


# ============================================================================ #
# ! Make Headings 
headings = ["Payment Schedule Category", "Payment Name", "Financial Close"] + list(months) # TOOD -> make this nice, month 1 + date 

col=0
for heading in headings:
    ws_const_calc.write(refd["gen_startrow"], col, heading, bold_format)
    col +=1

# ============================================================================ #
# ! Function to Calculate on Inputs 

def calc_on_inputs(local_start_row, foreign_start_row, input_data, merge_name, eqn_start_col, calc_fx):
    # costs paid at financial close 
    len_data = len(list(input_data.keys()))

    # merge names in the first colum 
    if len_data > 1: 
        sheet.merge_range(local_start_row, 0, local_start_row+len_data-1, 0, merge_name, bold_format)
    else:
        sheet.write(local_start_row, 0, merge_name, bold_format)
        

    # local columns
    name_col = 1
    row = local_start_row
    # for iterating over the foreign sheet
    i=0 

    for cost in range(len_data):
        # get cell name from other sheet 
        name_cell = xl_rowcol_to_cell(foreign_start_row+i, 0)
        # write heading 
        ws_const_calc.write_formula(row, name_col, f"='{refd['sheetnames'][0]}'!{name_cell}", left_align_format) #TODO change sheetname to be more broad later 

        # do monthly calculation 
        calc_fx(foreign_start_row, eqn_start_col, row, i)

        # iterate over foreign and local sheet 
        row+=1
        i+=1

    return row



# ============================================================================ #
# ! Helper Functions per Section 

def calc_fc(foreign_start_row, eqn_start_col, row, i):
    # get cell name from other sheet 
    data_cell = xl_rowcol_to_cell(foreign_start_row+i, 1)
    ws_const_calc.write_formula(row, eqn_start_col, f"='{refd['sheetnames'][0]}'!{data_cell}", money_format)
    # enter 0s for everything ele 
    for month in months:
        ws_const_calc.write_formula(row, eqn_start_col+month, "=0", money_format)

def calc_split(foreign_start_row, eqn_start_col, row, i): 
        # nothing paid at financial close 
        ws_const_calc.write_formula(row, eqn_start_col, "=0", money_format)
        # do monthly calculation 
        for month in months:
            # get cell name from other sheet 
            data_cell = xl_rowcol_to_cell(foreign_start_row+i, 1)
            # do calculation 
            ws_const_calc.write_formula(row, eqn_start_col+month, f"='{refd['sheetnames'][0]}'!{data_cell}/24", money_format)

def calc_epc(foreign_start_row, eqn_start_col, row, i):
        epc_sched_row = refd["cpi"]["epc_perc_sr"]
        # nothing paid at financial close 
        ws_const_calc.write_formula(row, eqn_start_col, "=0", money_format)
        # do monthly calculation 
        ci_sheet = refd['sheetnames'][0]
        for ix, month in enumerate(months):
            # get cell name from other sheet 
            epc_percent_cell = xl_rowcol_to_cell(epc_sched_row+ix, 1)
            epc_payment_cell = xl_rowcol_to_cell(foreign_start_row, 1)
            print(epc_percent_cell, epc_payment_cell, ix)
            # do calculation 
            ws_const_calc.write_formula(row, eqn_start_col+month, 
            f"='{ci_sheet}'!{epc_payment_cell} * '{ci_sheet}'!{epc_percent_cell}", money_format)