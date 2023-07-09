import pandas as pd
import os

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

    data = {'disk_invest': [], 'disk_ertrag': []}

    for year in range(1, lifetime + 1):
        present_costs = yearly_costs / (1 + interest_rate) ** year
        present_yield = yearly_yield / (1 + interest_rate) ** year
        data['disk_invest'].append(present_costs)
        data['disk_ertrag'].append(present_yield)

    df = pd.DataFrame(data, index=range(1, lifetime + 1))
    lcoe = (inv_costs + df['disk_invest'].sum()) / df['disk_ertrag'].sum()

    return round(lcoe,2)

def append_costs_df(capex):
    """
    TODO: Beschreibung anpassen, das hier soll nur zur Orientierung dienen.
    Die Gesamtinvestitionskosten besteht aus den Capex und den Nebenkosten für Montage
    mit 31.8% (https://www.hs-augsburg.de/~rk/downloads/projektarbeit-windkraft.pdf).
    Die O&M können variieren zwischen 1 und 3% (https://iopscience.iop.org/article/10.1088/1755-1315/410/1/012047/pdf)
    oder 3.7% (https://www.hs-augsburg.de/~rk/downloads/projektarbeit-windkraft.pdf)
    Rückbau wird zunächst pauschal auf 6548 € gesetzt. Die Summe ergibt sich aus Tabelle 16/17/18.
    (https://www.umweltbundesamt.de/sites/default/files/medien/1410/publikationen/2019_10_09_texte_117-2019_uba_weacycle_mit_summary_and_abstract_170719_final_v4_pdfua_0.pdf)

    :parameter
    capex: investment costs in €/kW.

    return
        float: lcoe of all wind turbines
    """

    df_technical_infos = pd.read_excel('data/technical_information.xlsx')
    df_cp_curves = pd.read_excel('data/Wetterdaten_Wanna_Szenario_1.xlsx')

    df_technical_infos['Gesamtinvestitionskosten'] = df_technical_infos['Rated power:'] * capex + (capex * 0.318) \
                                                     + df_technical_infos['battery cost'] + 6548
    df_technical_infos['Betriebskosten'] = ((df_technical_infos['Rated power:'] * capex) * 0.02)

    # Get the cost value from the 'costs' column
    for index, row in df_technical_infos.iterrows():
        turbine_name = row['Turbine']
        inv_costs = row['Gesamtinvestitionskosten']
        yearly_costs = row['Betriebskosten']

        lcoe = calculate_lcoe(inv_costs=inv_costs,
                              yearly_costs=yearly_costs,
                              yearly_yield=df_cp_curves[turbine_name].sum(),
                              interest_rate=0.04,
                              lifetime=20)

        df_technical_infos.loc[index, 'LCOE'] = lcoe

    return df_technical_infos

tech_lcoe = append_costs_df(capex=4500)
tech_lcoe.to_excel('data/technical_information_lcoe.xlsx')
