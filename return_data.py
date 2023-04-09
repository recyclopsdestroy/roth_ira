import plotly.graph_objects as go
import pandas as pd
import nbformat

def calc_data(contribution, return_rate, tax_rate_0, tax_rate_r, contr_year, ret_year):
    
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


    return data

def growth(year, *args):
    # principle,rate, year, n = 1):
    [principle, rate, n] = args

    value = principle*(1 + rate/n)**(n*year)
    return value



def test():

    # (contribution, return_rate, tax_rate_0, tax_rate_r, contr_year, ret_year)

    contr = 10000
    rate = 0.07
    in_tax = 0.25
    f_tax = 0.35
    contr_year = 2023
    ret_year = 2057


    a = calc_data(contribution = contr
                    , return_rate = rate
                    , tax_rate_0 = in_tax
                    , tax_rate_r = f_tax
                    , contr_year = contr_year
                    , ret_year = ret_year)
    print()

if __name__ == "__main__":
    test()