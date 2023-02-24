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
def make_calc(dict, section_label, local_sheet, local_sr, foreign_sheet_ix, ital=False, sub=False):
    # get foreign sheet name and starting row 
    fs = refd["sheetnames"][foreign_sheet_ix]
    if sub:
        fr = refd["oi"][f"{section_label}_sr"]
    else:
       fr = refd["oi"][f"{section_label}_sr"]-1 
    
    ic(section_label)

    # get length of dictionary 
    dict_len = len(dict.keys()) + 1
    
    for ix in range(dict_len):
        # conditionally format the heading
        cond = True if ix == 0 else False
        format = "italic" if ital == True else "bold"
        cond_format = workbook.add_format({format: cond})
        
        label_cell = xl_rowcol_to_cell(fr+ix, 0)
        local_sheet.write_formula(local_sr+ix, 0, f"='{fs}'!{label_cell}", cond_format)


        if ix > 0:
            # get the predefined calculation 
            value_cell = xl_rowcol_to_cell(fr+ix, 1)
            v = f"'{fs}'!{value_cell}"
            ic(v)
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
    
    er = make_calc(corporate_costs["General"], "General", ws_op_calc, er+2, 2, True, True)

    other_corp_costs = list(corporate_costs.keys())[1:]

    for cost in other_corp_costs:
        er = make_calc(corporate_costs[cost], cost, ws_op_calc, er+1, 2, True, True)


# corporate_costs[""]