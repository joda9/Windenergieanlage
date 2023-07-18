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
    Berechnet den leistungsspezifischen Investitionskostenindex  in €/kW.

    :parameter
    inv_costs: Investitionskosten in €.
    installed_cap: Installierte nominelle Kapazität in kW.

    Ausgabe:
        float: Der leistungsspezifische Investitionskostenindex
    """

    inv_cost_index = inv_costs/installed_cap
    return round(inv_cost_index,2)

def calc_yield_cost_index(inv_costs, annual_yield):
    """
    Berechnet den Ertragsspezifischer Investitionskostenindex in €/kWh

    :parameter
     inv_costs: Investitionskosten in €.
     annual_yield: Jährlicher Ertrag in kWh.

    Ausgabe
        float: Ertragsspezifischer Investitionskostenindex
    """

    yield_cost_index= inv_costs/annual_yield

    return round(yield_cost_index,2)


def calculate_lcoe(inv_costs, yearly_costs, yearly_yield, interest_rate, lifetime):
    """
    Berechnet die LCOE der WEA in €/kWh.
    Jährliche Kosten berücksichtigen fixe und variable Kosten, sowie die Verfügbarkeit der Anlage

    :parameter:
        inv_costs: Investitionskosten in €.
        yearly_costs (float): Jährliche Kosten in €/a.
        yearly_yield (float): Jährlicher Ertrag der WEA in kWh
        interest_rate (float): Zinssatz in %.
        lifetime (int): Erwartete Betriebsdauer der Anlage in Jahren.

    Ausgabe:
        float: LCOE der WEA
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
    capex: Investitionskosten in €/kW.
    lifetime: Betriebsdauer der WEA in Jahren.
    interest_rate: Zinssatz in %.

    Ausgabe:
        DataFrame: DataFrame df_technical_infos mit berechneten wirtschaftlichen Kenngrößen
    """

    df_technical_infos = pd.read_excel('data/technical_information.xlsx')
    df_cp_curves = pd.read_excel('data/Wetterdaten_Wanna_Szenario_1.xlsx')

    df_technical_infos['Gesamtinvestitionskosten'] = df_technical_infos['Rated power:'] * capex + (capex * 0.318) \
                                                     + df_technical_infos['battery cost']
    df_technical_infos['Betriebskosten'] = ((df_technical_infos['Rated power:'] * capex) * 0.02) + 6548

    # Berechnet den LCOE mithilfe der Funktion calculate_lcoe und speichert ihn in einer neuen Spalte ab
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

