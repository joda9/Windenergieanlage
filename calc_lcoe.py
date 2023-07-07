import pandas as pd

def calc_flh_cap_factor(installed_cap, annual_yield):
    """
    Calculates full load hours and also capacity factor
    of wind turbine

    :parameter
    installed_cap: installed nominal capacity in kW.
    annual_yield: annual yield in kWh.

    return
        float: full load hours and capacity factor of wind turbine
    """
    flh = annual_yield/installed_cap
    cap_factor = flh/8760

    return round(flh,2), round(cap_factor,2)

def calc_investment_cost_index (inv_costs, installed_cap):
    """
    Calculates the performance-specific investment cost index (Leistungsspezifischer Investitionskostenindex)
    in €/kW.

    :parameter
    inv_costs: investment costs in €.
    installed_cap: installed nominal capacity in kW.

    return
        float: the performance-specific investment cost index
    """

    inv_cost_index = inv_costs/installed_cap
    return round(inv_cost_index,2)

def calc_yield_cost_index(inv_costs, annual_yield):
    """
    Calculathe the yield-specific investment cost index (Ertragsspezifischer Investitionskostenindex)
    in €/kWh.

    :parameter
     inv_costs: investment costs in €.
     annual_yield: annual yield in kWh.

    return
        float: the yield-specific investment cost index
    """

    yield_cost_index= inv_costs/annual_yield

    return round(yield_cost_index,2)


def calculate_lcoe(inv_costs,yearly_costs,yearly_yield, interest_rate, lifetime):
    """
    Calculates the LCOE of the wind turbine. The LCOE has the unit €/kWh.
    The yearly costs consider the fixed and variable costs as well as the
    availability of the wind turbine.

    :parameter:
        inv_costs: investment costs in €.
        yearly_costs (float): Yearly costs in €/a.
        yearly_yield (float): Yearly yield of wind turbine in kWh
        interest_rate (float): Interest rate in %.
        lifetime (int): Lifetime of the product in years.

    return
        float: The LCOE of the wind turbine
    """

    data = {'Annual Costs': [], 'Annual Yield': []}

    for year in range(1, lifetime + 1):
        present_costs = yearly_costs[year - 1] / (1 + interest_rate) ** year
        present_yield = yearly_yield[year - 1] / (1 + interest_rate) ** year

        data['Annual Costs'].append(present_costs)
        data['Annual Yield'].append(present_yield)

    df = pd.DataFrame(data, index=range(1, lifetime + 1))
    lcoe = (inv_costs + df['Annual Costs'].sum()) / df['Annual Yield'].sum()
    return df, round(lcoe, 2)

# Example
inv_costs = 10000
yearly_costs = [100,140,100] # Costs in €/a
interest_rate = 0.05  # 5% interest rate
lifetime = 3  # Lifetime of the product in years
yearly_yield = [30, 30, 35]

lcoe=calculate_lcoe(inv_costs=inv_costs,
                    yearly_costs=yearly_costs,
                    yearly_yield=yearly_yield,
                    interest_rate=interest_rate,
                    lifetime=lifetime)
print(lcoe)