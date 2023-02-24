from wbsetup import *
from data import *
from const_input import * 
from const_calc import *




def main():
    ic(refd)
    er_epc = calc_on_inputs(refd["gen_startrow"]+1, refd["cpi"]["epc_sr"], epc_data, "EPC Payments", 2, calc_epc)

    er_monthly = calc_on_inputs(er_epc, refd["cpi"]["split_sr"], split_costs, "Monthly Payments", 2, calc_split)

    er_fc = calc_on_inputs(er_monthly , refd["cpi"]["fc_sr"], fc_costs, "Payments at Financial Close", 2, calc_fc)


    calc_totals(er_fc, ref_row_start=refd["gen_startrow"]+1, ref_row_end=er_fc-1)



    workbook.close()



if __name__ == "__main__":
    main()