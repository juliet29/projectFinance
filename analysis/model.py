import numpy_financial as npf
import pandas as pd
import numpy as np
from data import * 
from expenses import * 
from revenues import * 
from other import *


def format_df(df):
    return (df/1e6).round(decimals=2)


def run_model(ppa_df, exp_df, debt_service_df, dep_df, loan_amount=loan_amount, loan_perc = 0.7, corp_tax_rate=corp_tax_rate, hipu_escrow_full=hipu_escrow_full,  year_col_names=year_col_names):

    # ~ investments
    total_invest  = loan_amount*1/loan_perc
    # assume
    equity_amount = total_invest*(1 - loan_perc)

    # ~ create dataframe
    df0 = pd.DataFrame( columns=year_col_names)

    # revenue 
    df0.loc["Revenue"] = ppa_df.loc["Total"]
    df0 = df0.fillna(0)

    # expenses 
    df0.loc["Capital and Operating Expenses"] = exp_df.loc["Total"]*-1

    df0.loc["Taxable Debt Service Expenses"] = debt_service_df.loc["Interest Payment"]*-1 + debt_service_df.loc["Fees"]*-1

    df0.loc["Total Expenses"] = df0.loc["Capital and Operating Expenses"] + df0.loc["Taxable Debt Service Expenses"] 

    # ebitda 
    df0.loc["EBITDA"] = df0.loc["Revenue"] + df0.loc["Total Expenses"]

    # tax depreciation 
    df0.loc["Depreciation Value"] = dep_df.loc["Depreciation"]*-1
    df0 = df0.fillna(0)


    # taxable income/loss, also earnings after depreciation 
    df0.loc["EBIT"] = df0.loc["EBITDA"] + df0.loc["Depreciation Value"]

    # tax credit to recieve/ tax to pay  
    df0.loc["Corporate Tax Due"] = df0.loc["EBIT"] .apply(lambda x: max(x* corp_tax_rate,0))*-1


    df0.loc["Net Income"] = df0.loc["EBIT"] + df0.loc["Corporate Tax Due"]

    df0.loc["Loan Repayments Due"] = debt_service_df.loc["Prinicpal Payment"]*-1

    df0.loc["HIPU Escrow Account"] = [i*-1 for i in hipu_escrow_full]

    df0.loc["Loan Income"] = [loan_amount] + [0]*len(df0.columns[1:])

    df0.loc["Equity Income"] = [equity_amount] + [0]*len(df0.columns[1:])

    df0.loc["Cash Flow"] = df0.loc["Net Income"] - df0.loc["Depreciation Value"] + df0.loc["HIPU Escrow Account"] + df0.loc["Loan Repayments Due"] + df0.loc["Loan Income"] #+ df0.loc["Equity Income"]

    df0.loc["Cumulative Cash Flow"] = df0.loc["Cash Flow"].cumsum()

    print(df0.loc["Cash Flow"][0:23])

    roe = df0.loc["Cash Flow"][0:23].sum()/df0.loc["Equity Income"][0]

    npv = npf.npv(rate=0.08, values=df0.loc["Cash Flow"])/1e6

    format_df0 = format_df(df0)

    return format_df0, df0, roe, npv