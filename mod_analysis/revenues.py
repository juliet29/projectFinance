import pandas as pd
import numpy as np

class RevenuesMixin:
    # ! Helper Functions 
    def monthly_possible_pay(self, capacity, pay=None):
        if pay == None:
            pay = self.pay # TODO check this out!

        capacity_chunks = capacity/1000
        self.total_possible_pay = pay*capacity_chunks
        return self.total_possible_pay #  $/month...


    # ! PPA
    def calc_ppa(self):
        # inflation adjusted pay 
        inflat_pay = [0]* len(self.year_nums)
        inflat_pay[0] = self.pay


        for i in self.year_nums[0:-1]:
            inflat_pay[i] = inflat_pay[i-1]*self.ppa_inflat_rate

        # project ppa 
        ppa_forecast = []
        for pay in inflat_pay:
            ppa_forecast.append([self.monthly_possible_pay(i*self.capacity,pay) for i in self.target_avail])


        col_names = self.year_col_names
        months_in_year = pd.date_range('2025-01-01','2025-12-31', 
                    freq='MS').strftime("%b").tolist()


        self.ppa_df = pd.DataFrame(ppa_forecast, columns=months_in_year, index=col_names[3:]).T

        self.ppa_df.loc["Total", :] = self.ppa_df.sum(axis=0)

        return self.ppa_df


