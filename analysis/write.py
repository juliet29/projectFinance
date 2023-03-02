import pandas as pd
import numpy as np
from data import * 
from expenses import * 
from revenues import * 
from profits import *

# ============================================================================ #
# ! Setup 
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('IslandEnergy.xlsx', engine='xlsxwriter')
workbook  = writer.book

# ============================================================================ #
# ! Formats 
title_format = workbook.add_format({'bold': True, "font_name": "Calibri", "bg_color": "#769ddb" })
title_format.set_text_wrap()
title_format.set_align("left")

# Add a bold format to use to highlight cells.
bold_format = workbook.add_format({'bold': True, "font_name": "Calibri"})
bold_format.set_text_wrap()

# Add a number format for cells with money.
money_format = workbook.add_format({'num_format': '$#,##0'})

# Add a header format.
header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'align': 'left',
    "font_name": "Calibri",
    # 'border': 1
    })

# ============================================================================ #
# ! Write 

# ~ Helpers 
general_sr = 4 # general start row 

def format_df_headers(ws, df, sr, multiindex=False):
    for col_num, value in enumerate(df.columns.values):
        var_add = 1 if multiindex else 2
        ws.write(sr, col_num + var_add, value, header_format)

    for row_num, value in enumerate(df.index.values):
        if multiindex:
            ws.write(sr+row_num+1, 0, value[0], header_format)
            ws.write(sr+row_num+1, 1, value[1], header_format)
        else:
            ws.write(sr+row_num+1, 0, value, header_format)


def write_one_df(df, sheet_name, sr=general_sr):
    df.to_excel(writer, sheet_name=sheet_name, startrow=sr)
    format_df_headers(ws=writer.sheets[sheet_name], df=df, sr=sr)

def write_one_of_many_df(df, sheet_name, title, sr):
    df.to_excel(writer, sheet_name=sheet_name, startrow=sr)
    ws = writer.sheets[sheet_name]

    # title 
    ws.merge_range(sr-1, 0, sr-1, 50, title, title_format)

    max_row, max_col = df.shape
    end_row = sr + max_row

    format_df_headers(ws, df, sr, multiindex=True)

    return end_row 


# ~ Single DF Per Page
write_one_df(rev_df, "Revenues")
write_one_df(summ_df, "Profits")


# ~ Multi DF Per Page
er = write_one_of_many_df(const_df, "Expenses", "Construction Phase Expenses", sr=7)

er = write_one_of_many_df(op_df, "Expenses", "Outward Operating Expenses", sr=er+5)

er = write_one_of_many_df(corp_df, "Expenses", "Coporate Operating Expenses", sr=er+5)
