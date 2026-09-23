from typing import final
from machine_learning_1 import monte_carlo
import random
import math


def run_simulations(starting_price, mean_return, volatility, days, simulations):
    final_prices = []
    mean = 0 
    variance = 0 

    def simulation(starting_price, mean_return, volatility, days):
        current_price = starting_price
        prices = []
        for i in range(1, days):

            random_return = random.gauss(mean_return, volatility)  # Generates random normal distribution 
            current_price = current_price * (1 + random_return)
            prices.append(current_price)
        final_prices.append(prices[-1])

    for i in range(simulations):
        simulation(starting_price, mean_return, volatility, days)
    
    def profit_probability(starting_price, final_prices):
        seen = {}
        profit = 0

        for i in range(len(final_prices)):
            if final_prices[i] > starting_price:
                profit += 1 
        return profit / len(final_prices)
    
    def arithmetic_mean(final_prices):
        total = 0
        for i in range(len(final_prices)):
            total += final_prices[i]
        mean = total / len(final_prices)
        return mean

    def variance(mean, final_prices):
        #Variance = E[X^2] - E[X]^2
        squared_mean = 0
        for i in range(len(final_prices)):
            squared_mean += final_prices[i] ** 2
        squared_mean = squared_mean / len(final_prices)

        variance = squared_mean - (mean ** 2)
        return variance
    
    def standard_deviation(variance):
        return math.sqrt(variance)

    def percentile(final_prices, percentage):
        ordered_return = sorted(final_prices)

        return ordered_return[int(len(final_prices) * percentage) - 1]

            
