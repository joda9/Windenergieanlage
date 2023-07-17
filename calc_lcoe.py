import pandas as pd
import os

def calc_flh_cap_factor(installed_cap, annual_yield):
    """
    Berechnet Volllaststunden und Kapazitätsfaktor der WEA

    Parameter:
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
    Berechnet den Leistungsspezifischen Investitionskostenindex  in €/kW.

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
    berechnet den Ertragsspezifischen Investitionskostenindex in €/kWh.

    :parameter
     inv_costs: Investitionskosten in €.
     annual_yield: Jährlicher Ertrag in kWh.

    Ausgabe
        float: Der ertragsspezifische Investitionskostenindex
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
    Berechnet Dataframe unter Anderem mit relevanten ökonomischen Kennwerten.

    Die Gesamtinvestitionskosten besteht aus den Capex und den Nebenkosten für Montage
    mit 31.8% (https://www.hs-augsburg.de/~rk/downloads/projektarbeit-windkraft.pdf).
    
    Die O&M ('Betriebskosten') können variieren zwischen 1 und 3% (https://iopscience.iop.org/article/10.1088/1755-1315/410/1/012047/pdf)
    oder 3.7% (https://www.hs-augsburg.de/~rk/downloads/projektarbeit-windkraft.pdf)
    In diesem Programm wurden pauschal 2% angesetzt

    Rückbau wird zunächst pauschal auf 6548 € gesetzt. Die Summe ergibt sich aus Tabelle 16/17/18.
    (https://www.umweltbundesamt.de/sites/default/files/medien/1410/publikationen/2019_10_09_texte_117-2019_uba_weacycle_mit_summary_and_abstract_170719_final_v4_pdfua_0.pdf)

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
                                                     + df_technical_infos['battery cost'] + 6548
    df_technical_infos['Betriebskosten'] = ((df_technical_infos['Rated power:'] * capex) * 0.02)

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

