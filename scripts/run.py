from wbsetup import *
from data import *
from const_input import * 
from const_calc import *




def main():
    end_row = calc_on_inputs(refd["gen_startrow"]+1, refd["cpi"]["split_sr"], split_costs, "Monthly Payments", 2, calc_split)

    er = calc_on_inputs(end_row, refd["cpi"]["fc_sr"], fc_costs, "Payments at Financial Close", 2, calc_fc)

    # calc_on_inputs(local_start_row, foreign_start_row, input_data, merge_name, eqn_start_col, calc_fx)
    epc_data = {
        "1": 1
    }
    er_epc = calc_on_inputs(er, refd["cpi"]["epc_sr"], epc_data, "EPC payments", 2, calc_epc)

    workbook.close()



if __name__ == "__main__":
    main()