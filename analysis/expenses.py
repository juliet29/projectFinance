import pandas as pd
import numpy as np
from icecream import ic


"""Calculation of Expenses over Time based on Inputs 
outputs: const_exp, op_exp, corp_exp"""




class ExpensesMixin:
    # ============================================================================ #
    # ! helper functions 
    def prep_for_calcs(self, df, yearly=False):
        # make a copy 
        df_df = df.copy()
        df_inputs = df.copy()

        if not yearly:
            # add columns for months and pre-fc 
            col_names = ["Pre-Financial Close", "Financial Close - July 2023"]
            # TODO add real months here!
            month_names = [f"Month {i}" for i in self.months]
            col_names = col_names + month_names
        else:
            col_names = ["Financial Close - July 2023", "Construction Year 1 - July 2024", "Commisioning and Construction Year 2 - July 2025"]
            year_names = [f"July {2025 + ix} - Year {ix}" for ix in self.year_nums]
            col_names = col_names + year_names


        # create empty list to initialize the dataframe 
        empty_list = len(df_df) * [0]

        # initialize df 
        for col in col_names:
            df_df[col] = empty_list

        # drop the value column 
        df_df.drop(columns=["Value"], inplace=True)

        return df_df, df_inputs

    def make_two_index_df(self, d_orig):
        """ Make multi index dictionary """
        d = d_orig.copy()
        # make entries into arrays
        for inner_dict in d.values():
            for k, v in inner_dict.items():
                inner_dict[k] = [v]
        # arrange the dictionary to have tuples 
        reform_d = {(outerKey, innerKey): values for outerKey, innerDict in d.items() for innerKey, values in innerDict.items()}
        # make the multi index dictionary 
        df = pd.DataFrame(reform_d, index=["Value"])
        df = df.T
        return df



    # ============================================================================ #
    # ! Construction Phase

    def calc_non_epc_expenses(self):
        # ~ prep data ----------
        d = {
            "Pre-Financial Close Expenses": self.pre_fc_costs,
            "Financial Close Expenses": self.fc_costs,
            "Construction Period Even Split Monthly Expenses": self.monthly_split_costs,
            "Construction Period Custom Schedule Monthly Expenses": self.epc_data
        }
        const_phase_inputs = self.make_two_index_df(d)
        const_df, const_inputs = self.prep_for_calcs(const_phase_inputs)

        # ~ pre- financial close 
        const_df.loc["Pre-Financial Close Expenses", "Pre-Financial Close"] = const_inputs.loc["Pre-Financial Close Expenses"]["Value"].values

        # ~ at financial close 
        const_df.loc["Financial Close Expenses", "Financial Close - July 2023"] = const_inputs.loc["Financial Close Expenses"]["Value"].values


        # ~ monthly split expenses  
        # get values from input dataframe
        vals = const_inputs.loc["Construction Period Even Split Monthly Expenses"]["Value"].values


        # perform calculatuation, expense is split evenly over months of the year 

        a = const_df.loc["Construction Period Even Split Monthly Expenses"].apply(lambda x: vals/12)

        # assign values to dataframe 
        for i in const_df.loc["Construction Period Even Split Monthly Expenses"].index:
            const_df.loc[("Construction Period Even Split Monthly Expenses", i)] = a.loc[i]

        # correction because payments are only during the construction period, not before financial close  
        const_df.loc["Construction Period Even Split Monthly Expenses", ["Pre-Financial Close", "Financial Close - July 2023"]] = 0

        return const_df, const_inputs

    def calc_epc_expenses(self, const_df, const_inputs, new_val=None):
        # ~ EPC expenses based on EPC payments 
        for ix, col in enumerate(const_df.columns):
            # simplify code with these variables 
            ix1 = "Construction Period Custom Schedule Monthly Expenses"
            ix2 = "EPC Cost"
            # get the value of EPC from input dataframe 
            if not new_val:
                val = const_inputs.loc[(ix1, ix2), "Value"]
            else:
                val = new_val

            # initial entries are 0, payments only occur during the construction period 
            offset = 1
            if ix <= offset:
                const_df.loc[(ix1, ix2), col]  = 0
            else:
                # reference the payment schedule 
                const_df.loc[(ix1, ix2), col]  = self.epc_sched[ix -1] * val

        # calculate total per time period 
        const_df.loc[("Total", ""), :] = const_df.sum(axis=0)

        return const_df

    def make_const_exp(self, const_df):
        # ~ Collapse construction costs into final reporting periods 
        # TODO make these bi-annual 
        year_1 = const_df.iloc[const_df.index.get_level_values(0)=="Total", 2:14].sum(axis=1).values[0]

        year_2 = const_df.iloc[const_df.index.get_level_values(0)=="Total", 14:].sum(axis=1).values[0]

        by_fc = const_df.iloc[const_df.index.get_level_values(0)=="Total", 0:2].sum(axis=1).values[0]

        const_costs = len(self.year_col_names)*[0]
        const_costs[0] = by_fc
        const_costs[1] = year_1
        const_costs[2] = year_2
        const_exp_df = pd.DataFrame(const_costs, index=list(self.year_col_names), columns=["Construction Expenses"]).T

        const_exp = const_exp_df.loc["Construction Expenses"]

        return const_exp

    def calc_const_exp(self, new_val=None):
        const_df, const_inputs = self.calc_non_epc_expenses()
        const_df_base = self.calc_epc_expenses(const_df, const_inputs, new_val)
        self.const_exp = self.make_const_exp(const_df_base)

        return self.const_exp
    # ============================================================================ # 
    # ! Operations phase

    def calc_op_exp(self):
        # ~ prep data 
        oper_d = {
        "Commisioning Fees": self.comm_fees,
        "Operating Fees to External Entities": self.other_fees
        }
        oper_phase_inputs = self.make_two_index_df(oper_d)
        op_df, op_ref = self.prep_for_calcs(oper_phase_inputs, yearly=True)
        # ~ one time commisioning fees 
        op_df.loc["Commisioning Fees", "Commisioning and Construction Year 2 - July 2025"] = op_ref.loc["Commisioning Fees","Value"].values

        # ~ quarterly payments to MaintCo 
        op_df.iloc[op_df.index.get_level_values(1)=="Quarterly MaintCo Maintennance Fee", 3:] = op_ref.loc[("Operating Fees to External Entities", "Quarterly MaintCo Maintennance Fee"),"Value"]*4

        # ~ annual fishery payments 
        op_df.iloc[op_df.index.get_level_values(1)=="Annual Fisheries Mitigation Permit", 3:] = op_ref.loc[("Operating Fees to External Entities", "Annual Fisheries Mitigation Permit"),"Value"]

        # ~ -- variable monthly interconnection fee 
        # decade one 
        op_df.iloc[op_df.index.get_level_values(1)=="Monthly HIPU Interconection Fee, Decade 1", 3:3+10] = op_ref.loc[("Operating Fees to External Entities", "Monthly HIPU Interconection Fee, Decade 1"),"Value"]
        # decade two 
        op_df.iloc[op_df.index.get_level_values(1)=="Monthly HIPU Interconection Fee, Decade 1", 3+10:] = op_ref.loc[("Operating Fees to External Entities", "Monthly HIPU Interconection Fee, Post-Decade 1"),"Value"]
        # rename
        op_df.rename(index={'Monthly HIPU Interconection Fee, Decade 1': 'Monthly HIPU Interconection Fee'}, inplace=True)
        # drop the other entry 
        op_df.drop("Monthly HIPU Interconection Fee, Post-Decade 1", level=1, inplace=True)

        # calculate total per time period 
        op_df.loc[("Total", ""), :] = op_df.sum(axis=0)

        # export op_exp 
        self.op_exp = op_df.loc[("Total", "")]

        return self.op_exp
    # ============================================================================ # 
    # ! Corporate Expenses 

    def calc_corp_exp(self):
        # ~ prep data 
        corp_inputs = self.make_two_index_df(self.corporate_costs)
        corp_df, corp_ref = self.prep_for_calcs(corp_inputs, yearly=True)

        # ~ calculations 
        # set year 1 equal to the appropriate value 
        corp_df["Construction Year 1 - July 2024"] = corp_ref["Value"].values

        # increase with inflation 
        for col in corp_df.columns[2:]:
            curr_ix = corp_df.columns.get_loc(col)
            corp_df.iloc[:, curr_ix] = corp_df.iloc[:, curr_ix-1]*(1+self.inflation_rate)

        # calculate total per time period 
        corp_df.loc[("Total", ""), :] = corp_df.sum(axis=0)

        # export corp_exp 
        self.corp_exp = corp_df.loc[("Total", "")]

        return self.corp_exp


    # ============================================================================ # 
    # ! Summary of Expenses 

    def calc_exp_df(self, new_val=None):
        self.calc_const_exp(new_val)
        self.calc_op_exp()
        self.calc_corp_exp()
        self.exp_df = pd.concat([self.const_exp, self.op_exp, self.corp_exp], axis=1).T
        self.exp_df = self.exp_df.set_axis(["Construction", "Operating", "Corporate"], copy=True)
        self.exp_df.loc["Total", :] = self.exp_df.sum(axis=0)

        return self.exp_df

