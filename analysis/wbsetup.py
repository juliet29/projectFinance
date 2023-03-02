import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell, xl_cell_to_rowcol
from icecream import ic

# ============================================================= #
#  Setup workbook 

workbook = xlsxwriter.Workbook('IslandEnergy.xlsx')
ws_const_in = workbook.add_worksheet(name="Construction Period Cost Inputs")
ws_const_calc = workbook.add_worksheet(name="Construction Period Calcs")
ws_op_in = workbook.add_worksheet(name="Operat. Period Cost Inputs")
ws_op_calc = workbook.add_worksheet(name="Operat. Period Calcs")
profits_calc = workbook.add_worksheet(name="Profits")

# dictionary of references for wos 
refd= {}
refd["sheetnames"] = list(workbook.sheetnames.keys())
refd["gen_startrow"] = 4 




# ============================================================= #
# Formats 

# Add a bold format to use to highlight cells.
bold_format = workbook.add_format({'bold': True})
bold_format.set_text_wrap()

# Add a number format for cells with money.
money_format = workbook.add_format({'num_format': '$#,##0'})

# create format to use in merged range 
merge_format = workbook.add_format({
    'bold': 2,
    'border': 1,
    'align': 'left',
    # 'valign': 'vcenter',
    # 'fg_color': 'yellow'
    })

title_format = workbook.add_format({'bold': True})
title_format.set_text_wrap()
title_format.set_align("left")

secondary_heading_format = workbook.add_format({
    "italic": True, 
})

percent_format = workbook.add_format({'num_format': '0.00%'})

left_align_format = workbook.add_format()
left_align_format.set_align("left")


# ============================================================= #
#  Format worksheets

# Page Headers 
for name, sheet in workbook.sheetnames.items():
    sheet.write('A1', 'Project Name', bold_format)
    sheet.write('A2', 'Sheet Name', bold_format)
    sheet.merge_range('B1:C1', "Island Energy", bold_format)
    sheet.merge_range('B2:C2', name, bold_format)
    # sheet.set_column("A:C", 30)
    sheet.set_column("A:AR", 30)
    

def depth(d):
     if isinstance(d, dict):
        return 1 + (max(map(depth, d.values())) if d else 0)
     return 0
