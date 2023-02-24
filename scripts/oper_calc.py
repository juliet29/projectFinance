from wbsetup import *
from data import *
from const_input import * 
from oper_input import * 


# ============================================================================ #

# ! Make Headings



def make_headings(): 
    headings = ["Payment Name", ] + year_names
    col = 0
    for heading in headings:
        ws_op_calc.write(refd["gen_startrow"], col, heading, bold_format)
        col +=1

# ============================================================================ #


# ! Calculations 
def make_calc(dict, section_label, local_sheet, local_sr, foreign_sheet_ix):
    # get foreign sheet name and starting row 
    fs = refd["sheetnames"][foreign_sheet_ix]
    fr = refd["oi"][f"{section_label}_sr"]-1

    # get length of dictionary 
    dict_len = len(dict.keys()) + 1
    
    for ix in range(dict_len):
        cond = True if ix == 0 else False
        cond_bold_format = workbook.add_format({'bold': cond})
        
        label_cell = xl_rowcol_to_cell(fr+ix, 0)
        local_sheet.write_formula(local_sr+ix, 0, f"='{fs}'!{label_cell}", cond_bold_format)

        # dont do calculation for the label 
        if ix > 0:
            # get the predefined calculation 
            value_cell = xl_rowcol_to_cell(fr+ix, 1)
            v = f"'{fs}'!{value_cell}"
            calc = list(dict.values())[ix-1][1](v)
            # apply to columns 
            for iz, c in enumerate(calc):
                local_sheet.write_formula(local_sr+ix, iz+1, c, money_format)

    return local_sr+ix




# ============================================================================ #
# Main 
def run_oper_calc():
    make_headings()
    er = make_calc(comm_fees, "Fees Paid at Commisioning", ws_op_calc, refd["gen_startrow"]+1, 2)
    er = make_calc(other_fees, "General Operating Fees", ws_op_calc, er+1, 2)
    er = make_calc(other_fees, "General Operating Fees", ws_op_calc, er+1, 2)


