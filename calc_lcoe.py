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
        present_costs = yearly_costs / (1 + interest_rate) ** year
        present_yield = yearly_yield / (1 + interest_rate) ** year

        data['Annual Costs'].append(present_costs)
        data['Annual Yield'].append(present_yield)

    df = pd.DataFrame(data, index=range(1, lifetime + 1))
    lcoe = (inv_costs + df['Annual Costs'].sum()) / df['Annual Yield'].sum()

    return df, round(lcoe, 2)


def append_costs_df(capex,wt_name):
    """
    TODO: Beschreibung anpassen, das hier soll nur zur Orientierung dienen.
    Die Gesamtinvestitionskosten besteht aus den Capex und den Nebenkosten für Montage
    mit 31.8% (https://www.hs-augsburg.de/~rk/downloads/projektarbeit-windkraft.pdf).
    Die O&M können variieren zwischen 1 und 3% (https://iopscience.iop.org/article/10.1088/1755-1315/410/1/012047/pdf)
    oder 3.7% (https://www.hs-augsburg.de/~rk/downloads/projektarbeit-windkraft.pdf)

    :parameter
     capex: investment costs in €/kW.
     wt_name: name of wind turbine (str).

    return
        float: lcoe of wind turbine
    """
    #Capex müssen variabel bleiben, damit wir hier sensibilitätsanalyse machen können
    df_technical_infos = pd.read_excel('data/technical_information_new.xlsx')
    df_cp_curves = pd.read_excel('data/Wetterdaten_Wanna_Szenario_1.xlsx')

    df_technical_infos['Gesamtinvestitionskosten'] = df_technical_infos['Rated power:'] * capex + (capex * 0.318)
    df_technical_infos['Betriebskosten'] = ((df_technical_infos['Rated power:'] * capex) * 0.02)

    #Damit die Daten für eine bestimmte Wind turbine genommen werden
    turbine_row = df_technical_infos[df_technical_infos['Turbine'] == wt_name]
    turbine_var_cost = df_technical_infos[df_technical_infos['Turbine'] == wt_name]

    # Check if the turbine name exists in the DataFrame
    if turbine_row.empty:
        return 'Windturbine kann nicht gefunden werden.'

    if turbine_var_cost.empty:
        return 'Windturbinen Betriebskosten kann nicht gefunden werden.'

    # Get the cost value from the 'costs' column
    inv_costs = turbine_row['Gesamtinvestitionskosten'].values[0]
    yearly_costs = turbine_var_cost['Betriebskosten'].values[0]

    lcoe = calculate_lcoe(inv_costs=inv_costs,
                          yearly_costs=yearly_costs,
                          yearly_yield=df_cp_curves[wt_name].sum(),
                          interest_rate=0.08,
                          lifetime=20)

    return lcoe

nordex_n29= append_costs_df(capex=4500,
                       wt_name='Nordex N29')
print(nordex_n29)