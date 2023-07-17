import pandas as pd
import os

def calc_flh_cap_factor(installed_cap, annual_yield):
    """
    Berechnet Volllaststunden und Kapazitätsfaktor der WEA


    :parameter
    installed_cap: Installierte nominelle Kapazität in kW.
    annual_yield: Jährlicher Ertrag in kWh.

    Ausgabe
        float: Volllaststunden und Kapazitätsfaktor der WEA
    """
    flh = annual_yield/installed_cap
    cap_factor = flh/8760

    return round(flh,2), round(cap_factor,2)

def calc_investment_cost_index (inv_costs, installed_cap):
    """
    Berechnet den Leistungsspezifischen Investitionskostenindex in €/kW


    :parameter
    inv_costs: Investitionskosten in €.
    installed_cap: Installierte nominelle Kapazität in kW.

    Ausgabe
        float: Leistungsspezifischen Investitionskostenindex
    """

    inv_cost_index = inv_costs/installed_cap
    return round(inv_cost_index,2)

def calc_yield_cost_index(inv_costs, annual_yield):
    """
    Berechnet den Ertragsspezifischer Investitionskostenindex in €/kWh

    :parameter
     inv_costs: investment costs in €.
     annual_yield: annual yield in kWh.

    Ausgabe
        float: Ertragsspezifischer Investitionskostenindex
    """

    yield_cost_index= inv_costs/annual_yield

    return round(yield_cost_index,2)


def calculate_lcoe(inv_costs, yearly_costs, yearly_yield, interest_rate, lifetime):
    """
    Berechnet den LCOE der WEA in €/kWh unter Berücksichtigung fixer und variabler Kosten
    der jährlichen Kosten.

    :parameter:
        inv_costs: Investitionskosten in €.
        yearly_costs (float): Jährliche Kosten in €/a.
        yearly_yield (float): Jährlicher Ertrag der WEA in kWh
        interest_rate (float): Zinssatz in %.
        lifetime (int): Lebensdauer der WEA in years.

    return
        float: Der LCOE der WEA
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

def append_costs_df(capex, lifetime, interest_rate):
    """
    Nach Eingabe von Capex, Betriebsdauer und Zinssatz einer geplanten Anlage liest die Funktion eine Tabelle mit
    technischen Informationen, sowie mit Wetter- und Anlagendaten ein.
    Anschließend werden die technischen Informationen mit Berechnungen zu Betriebs- und Gesamtkosten, sowie
    dem LCOE der einzelnen Anlagen erweitert.

    :parameter
    capex: investment costs in €/kW.
    lifetime: Lifetime of the product in years.
    interest_rate: Interest rate in %.

    return
        DataFrame: DataFrame with updated technical information
    """

    df_technical_infos = pd.read_excel('data/technical_information.xlsx')
    df_cp_curves = pd.read_excel('data/Wetterdaten_Wanna_Szenario_1.xlsx')

    df_technical_infos['Gesamtinvestitionskosten'] = df_technical_infos['Rated power:'] * capex + (capex * 0.318) \
                                                     + df_technical_infos['battery cost']
    df_technical_infos['Betriebskosten'] = ((df_technical_infos['Rated power:'] * capex) * 0.02) + 6548

    # Get the cost value from the 'costs' column
    for index, row in df_technical_infos.iterrows():
        turbine_name = row['Turbine']
        inv_costs = row['Gesamtinvestitionskosten']
        yearly_costs = row['Betriebskosten']

        lcoe = calculate_lcoe(inv_costs=inv_costs,
                              yearly_costs=yearly_costs,
                              yearly_yield=df_cp_curves[turbine_name].sum(),
                              interest_rate=interest_rate,
                              lifetime=lifetime)

        df_technical_infos.loc[index, 'LCOE'] = lcoe

    return df_technical_infos

