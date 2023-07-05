import pandas as pd


def calc_full_load_hours(installed_cap, y_yield):
    flh = y_yield/installed_cap
    return flh

def calculate_annuity(yearly_costs, interest_rate, lifetime):
    """
    Calculates the annuity of an investment based on the parameters.

    :parameter:
        yearly_costs (float): Yearly costs in €/a.
        interest_rate (float): Interest rate in %.
        lifetime (int): Lifetime of the product in years.

    return
        float: The annuity of the investment.
    """
    annuity = 0

    for i in range(1, lifetime + 1):
        present_value = yearly_costs / (1 + interest_rate) ** i
        annuity += present_value

    return round(annuity, 2)

# Example usage
yearly_costs = 10  # Costs in €/a
interest_rate = 0.05  # 5% interest rate
lifetime = 2  # Lifetime of the product in years

#annuity = calculate_annuity(yearly_costs, interest_rate, lifetime)
#print("The annuity of the investment is:", annuity)


