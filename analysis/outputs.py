import numpy_financial as npf
import pandas as pd
import numpy as np


class OutputsMixin:

    def format_df(self, df):
        return (df/1e6).round(decimals=2)


    def calc_outputs(self, loan_perc=0.7, interest_rate=0.08 ):
        # ~ investments
        total_invest  = self.loan_amount*1/loan_perc
        # assume
        equity_amount = total_invest*(1 - loan_perc)

        # ~ create dataframe
        df0 = pd.DataFrame(columns=self.year_col_names)

        # revenue 
        df0.loc["Revenue"] = self.ppa_df.loc["Total"]
        df0 = df0.fillna(0)

        # expenses 
        df0.loc["Capital and Operating Expenses"] = self.exp_df.loc["Total"]*-1

        df0.loc["Taxable Debt Service Expenses"] = self.debt_service_df.loc["Interest Payment"]*-1 + self.debt_service_df.loc["Fees"]*-1

        df0.loc["Total Expenses"] = df0.loc["Capital and Operating Expenses"] + df0.loc["Taxable Debt Service Expenses"] 

        # ebitda 
        df0.loc["EBITDA"] = df0.loc["Revenue"] + df0.loc["Total Expenses"]

        # tax depreciation 
        df0.loc["Depreciation Value"] = self.dep_df.loc["Depreciation"]*-1
        df0 = df0.fillna(0)


        # taxable income/loss, also earnings after depreciation 
        df0.loc["EBIT"] = df0.loc["EBITDA"] + df0.loc["Depreciation Value"]

        # tax credit to recieve/ tax to pay  
        df0.loc["Corporate Tax Due"] = df0.loc["EBIT"] .apply(lambda x: max(x* self.corp_tax_rate,0))*-1


        df0.loc["Net Income"] = df0.loc["EBIT"] + df0.loc["Corporate Tax Due"]

        df0.loc["Loan Repayments Due"] = self.debt_service_df.loc["Prinicpal Payment"]*-1

        df0.loc["HIPU Escrow Account"] = [i*-1 for i in self.hipu_escrow_full]

        df0.loc["Loan Income"] = [self.loan_amount] + [0]*len(df0.columns[1:])

        df0.loc["Equity Income"] = [equity_amount] + [0]*len(df0.columns[1:])

        df0.loc["Cash Flow"] = df0.loc["Net Income"] - df0.loc["Depreciation Value"] + df0.loc["HIPU Escrow Account"] + df0.loc["Loan Repayments Due"] + df0.loc["Loan Income"] #+ df0.loc["Equity Income"]

        df0.loc["Cumulative Cash Flow"] = df0.loc["Cash Flow"].cumsum()

        self.roe = df0.loc["Cash Flow"][0:23].sum()/df0.loc["Equity Income"][0]

        self.npv = npf.npv(rate=interest_rate, values=df0.loc["Cash Flow"])/1e6

        self.df_out = df0

        self.df_out_format = self.format_df(df0)

        return self.roe, self.df_out_format, self.npv, self.df_out