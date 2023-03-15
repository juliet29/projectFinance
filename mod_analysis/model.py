from inputs import * 
from expenses import * 
from revenues import *
from other import * 
from outputs import * 


class FinancialModel(InputsMixin, ExpensesMixin, RevenuesMixin, OtherCalcsMixin, OutputsMixin):
    def __init__(self):
        self.define_inputs()
    def run_base_case(self):
        # expenses 
        self.calc_exp_df()
        self.calc_ppa()
        self.calc_other()
        self.calc_outputs()

    def eval_epc_currency_sens(self, value):
        """
        value => new value of the EPC contract
        """
        self.calc_exp_df(value)
        self.calc_ppa()
        self.calc_other()
        self.calc_outputs()

        return self.roe

