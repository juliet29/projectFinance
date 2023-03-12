from expenses import * 

class FinancialModel(ExpensesMixin):
    def __init__(self):
        self.const_exp = None
        self.op_exp = None
        self.corp_exp = None
        self.exp_df = None
