import plotly.graph_objects as go
import pandas as pd
import nbformat

def calc_data(contribution, return_rate, current_income, retirement_income, contr_year, ret_year):
    
    def growth(year, *args):
        # principle,rate, year, n = 1):
        [principle, rate, n] = args

        value = principle*(1 + rate/n)**(n*year)
        return value

    def effective_tax(taxable_income):
        federal = pd.DataFrame({
            'income': [10275, 41775, 89075, 170050, 215950, 539900, 539901],
            'rate': [0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]
        })

        state = pd.DataFrame({
            'income': [10099, 23942, 37788, 52455, 66295, 338639, 406364, 677275, 677276],
            'rate': [0.01, 0.02, 0.04, 0.06, 0.08, 0.093, 0.103, 0.113, 0.123]
        })

        fed_calc = federal.iloc[0:federal.loc[federal['income'] < taxable_income].shape[0]+1]
        fed_calc.iloc[-1, fed_calc.columns.get_loc('income')] = taxable_income - fed_calc.iloc[-2, fed_calc.columns.get_loc('income')]
        for i, value in enumerate(fed_calc['income']):
            if i != 0 and i < fed_calc.shape[0]-1:
                fed_calc.loc[fed_calc['income'] == value, 'income'] = value - fed_calc['income'][i-1]


        state_calc = state.iloc[0:state.loc[state['income'] < taxable_income].shape[0]+1]
        state_calc.iloc[-1, state_calc.columns.get_loc('income')] = taxable_income - state_calc.iloc[-2, state_calc.columns.get_loc('income')]
        for i, value in enumerate(state_calc['income']):
            if i != 0 and i < state_calc.shape[0]-1:
                state_calc.loc[state_calc['income'] == value, 'income'] = value - state_calc['income'][i-1]

        fed_taxes = fed_calc['income'].dot(fed_calc['rate'])
        state_taxes = state_calc['income'].dot(state_calc['rate'])

        all_taxes = fed_taxes + state_taxes

        return all_taxes/taxable_income

    tax_rate_0 = effective_tax(current_income)
    tax_rate_r = effective_tax(retirement_income)

    year = pd.Series(range(contr_year, ret_year + 1))

    roth_cont = contribution*(1 -tax_rate_0)
    ira_cont = contribution

    years_since = year - contr_year
    
    roth_args = (roth_cont, return_rate, 1)
    ira_args = (ira_cont, return_rate, 1)

    roth_value = years_since.apply(growth,args = roth_args)
    ira_value = years_since.apply(growth, args = ira_args)

    data = pd.concat([year, roth_value, ira_value], axis = 1)
    data.columns = ['year', 'roth_value', 'ira_value']

    post_retirement_years = pd.Series(range(ret_year + 1, ret_year + 6))

    roth_retirement_value = roth_value[roth_value.shape[0] - 1]
    pretax_ira_retirement_value = ira_value[ira_value.shape[0] - 1]
    ira_retirement_value = pretax_ira_retirement_value*(1 - tax_rate_r)

    ret_roth_value = pd.Series([roth_retirement_value]*post_retirement_years.shape[0])
    ret_ira_value = pd.Series([ira_retirement_value]*post_retirement_years.shape[0])

    post_ret_data = pd.concat([post_retirement_years, ret_roth_value, ret_ira_value], axis = 1)
    post_ret_data.columns = ['year', 'roth_value', 'ira_value']

    data = pd.concat([data, post_ret_data], axis = 0).reset_index(drop=True)

    data = data.melt(id_vars= 'year', value_vars = ('roth_value', 'ira_value'), var_name = 'retirement', value_name= 'return')

    return data





def test():

    # (contribution, return_rate, tax_rate_0, tax_rate_r, contr_year, ret_year)


    a = effective_tax(65000)

    print(a)
    # contr = 10000
    # rate = 0.07
    # in_tax = 0.25
    # f_tax = 0.35
    # contr_year = 2023
    # ret_year = 2057


    # a = calc_data(contribution = contr
    #                 , return_rate = rate
    #                 , tax_rate_0 = in_tax
    #                 , tax_rate_r = f_tax
    #                 , contr_year = contr_year
    #                 , ret_year = ret_year)
    # print()

if __name__ == "__main__":
    test()