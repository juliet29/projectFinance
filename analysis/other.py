import pandas as pd
import numpy as np


"""Items that are neither direct expenses or revenues"""


class OtherCalcsMixin:

    # ! Debt Service 
    def calc_debt_service(self):
        # ~ read in data 
        ds = pd.read_csv("debt_service.csv", skiprows=[0,1], names=["Year", "Interest Payment", "Prinicpal Payment", "Fees"], dtype=np.float64)
        ds = ds.T

        # ~ make format fit others...
        debt_service = ds.copy()
        col_names =  self.year_col_names
        debt_service.insert(0, "newcol", [0]*4)
        debt_service.insert(1, "newcol2", [0]*4)
        debt_service = debt_service.set_axis(col_names[:23], axis=1, copy=True)
        debt_service.drop("Year", axis=0, inplace=True)

        # make length match other expense dataframes 
        empty = len(debt_service)*[0]
        empty_data = [empty for i in range(20)]
        empty_df = pd.DataFrame(empty_data, index=col_names[23:], columns=debt_service.index).T
        self.debt_service_df = pd.concat(objs=[debt_service, empty_df], axis=1)

        return self.debt_service_df


    # ! HIPU Escrow 
    def calc_hipu_escrow(self):
        hipu_escrow = [0]* len(self.year_nums)
        hipu_escrow[0] = self.hipu_escrow_op


        for i in self.year_nums[0:-1]:
            hipu_escrow[i] = hipu_escrow[i-1]*(1-self.annual_escrow_dec)

        hipu_escrow2 = [-(hipu_escrow[0] - i) for i in hipu_escrow[1:]]
        true_op_hipu_escrow = [hipu_escrow[0]] + hipu_escrow2
        true_op_hipu_escrow

        self.hipu_escrow_full = [self.hipu_escrow_fc, 0, 0] + true_op_hipu_escrow



    # ! Depreciation 
    def calc_depreciation(self):
       # depreciation on assets and capx 
       self.property_value = 100*self.corporate_costs["Other Annual Costs"]["Property Taxes"][0]
       self.init_capx = self.epc_data["EPC Cost"][0]
       
       depreciable_assets = self.property_value + self.init_capx
       annual_dep = depreciable_assets/self.straight_line_dep_term
       term_dep = [annual_dep]*20
       
       self.dep_df = pd.DataFrame([term_dep], columns=self.year_col_names[0:20], index=["Depreciation"])

    
    def calc_other(self):
        self.calc_debt_service()
        self.calc_hipu_escrow()
        self.calc_depreciation()