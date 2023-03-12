from collections import OrderedDict

# TODO define as attributes of the class??

class InputsMixin:

    # ! Timing
    def define_timing(self):
        self.months = range(1,25)
        self.year_nums = range(1,41)

        col_names = ["Financial Close - July 2023", "Construction Year 1 - July 2024", "Commisioning and Construction Year 2 - July 2025"]
        year_names = [f"July {2025 + ix} - Year {ix}" for ix in self.year_nums]
        self.year_col_names = col_names + year_names

        return self.year_col_names
        

    # ! Construction Phase Expenses 
    def define_const_costs(self):
        self.pre_fc_costs = {
            "Wetland Construction Permit": 3e6,
            "State Environmental Monitoring Fee": 800e3
        }

        # payments at financial close  
        self.fc_costs = {
            "Land Acquisition": 12.5e6,
            "Development Expenses": 28.5e6,
            "Development Fees": 14.7e6,
            "Closing Costs" : 14.392e6,
            "Contingency Fees": 30.754e6
        }

        # other payments over course of construction period 
        self.monthly_split_costs = {
        "Interest and Fees" : 56.853e6,
        "Insurance and Fees" : 25e6,
        "Management and Oversight ": 8.15e6
        }

        # eng, procurement, const base cost 
        self.epc_data = {
                "EPC Cost": 455e6
        }


        epc_sched = OrderedDict()
        for i in list(self.months):
            if i <= 3:
                epc_sched[i] = 0.02
            elif i <= 8: 
                epc_sched[i] = 0.04
            elif i <= 14: 
                epc_sched[i] = 0.06
            elif i <= 18: 
                epc_sched[i] = 0.05
            else: 
                epc_sched[i] = 0.03
        self.epc_sched = epc_sched



    # ! Operations Phase Expenses
    def define_oper_costs(self):
        # commisioning costs 
        comm_fees = { # one time 
                "ABSCO Interconnection Fee": 2.5e6,
                "ABSCO Network Upgrades": 5.2e6,
                "HIPU Interconnection Fee": 2e6
            }
        self.comm_fees = OrderedDict(comm_fees)


        other_fees = {
            "Quarterly MaintCo Maintennance Fee": 690e3, # quarterly during operations 
            "Annual Fisheries Mitigation Permit": 130e3, # annual (during operations?)
            "Monthly HIPU Interconection Fee, Decade 1": 110e3,  # monthly during oper.
            "Monthly HIPU Interconection Fee, Post-Decade 1": 220e3,  # monthly during oper
        }
        self.other_fees = OrderedDict(other_fees)

        self.inflation_rate = 0.025
        corporate_costs = { # annually during construction and operations, escalate w/ annual rate of inflation 2.5% starting in oper. phase 
            "General" : {
                "Corporate Resources": 1.9e6
            },
            "Outside Reources" : {
                "Engineering": 220e3,
                "Legal": 315e3,
                "Accounting": 180e3,
                "Community Relations": 80e3,
                "Industry Relations": 20e3,
                "Misc.": 50e3,
            },
            "Overhead": {
                "Station Power Service": 285e3,
                "Utilities": 65e3,
                "Rent": 82e3,
                "Telecommunications": 50e3,
                "Travel/Office": 260e3,
                "Misc.": 200e3,
                "Contingency": 120e3,
            },
            "Other Annual Costs": {
                "Insurance": 2.5e6,
                "Property Taxes": 2.55e6, # TODO does this account for the other property taxes, maybe move...?
                "Cable Easment": 700e3,
                "Contribution to Stanford Global Project Center": 25e3,
            }
        }

        self.corporate_costs = OrderedDict(corporate_costs)



    # ! Miscelanneous Inputs
    def define_misc_inputs(self):
        # ~ Escrow 
        # escrow at financial close
        self.hipu_escrow_fc = 7e6
        # escrow during operations 
        self.hipu_escrow_op = 22.5e6
        # annuel escrow decrease 
        self.annual_escrow_dec = 0.05

        #  ~ Taxes
        self.corp_tax_rate = 0.3

        # ~ Depreciation 
        self.straight_line_dep_term = 20
        self.property_tax_rate = 0.01 
        property_value = 1/(self.property_tax_rate) * self.corporate_costs["Other Annual Costs"]["Property Taxes"]
        self.init_capx = self.epc_data["EPC Cost"]


        # ~ PPA
        self.target_avail = ([0.95] * 5) + ([1] * 4) + ([0.95] * 3) #TODO add to inputs 
        self.capacity = 660e6 # watts <- needs to multiplied by ratio, for now just the availability 
        self.pay = 10.52 # $/(1000 watts-month) -> base payment 
        self.ppa_inflat_rate = 1.05 # 0.5%

        # ~ Loan
        self.loan_amount = 550062792 # $


        # ! Interest Rate #made up!!!!
        self.interest_rate = 0.08 

    def define_inputs(self):
        self.define_timing()
        self.define_const_costs()
        self.define_oper_costs()
        self.define_misc_inputs()
