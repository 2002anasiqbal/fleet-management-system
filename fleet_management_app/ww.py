import numpy as np

# Parameters
mean_demand = 160
std_dev_demand = 40
replenishment_level = 140
cost_per_unit = 150
selling_price = 300
holding_cost = 20
shortage_cost_value = 40  # Renamed to avoid conflict with function parameter
num_simulations = 1000  # Number of months to simulate

# Function to calculate the profit for a single month
def calculate_profit(demand):
    # Revenue from selling the goggles
    revenue = min(demand, replenishment_level) * selling_price
    
    # Cost of Goods Sold (COGS)
    cogs = replenishment_level * cost_per_unit
    
    # Inventory (Holding) Cost - only applies when demand is less than 140
    inventory_cost = max(0, replenishment_level - demand) * holding_cost
    
    # Shortage Cost - only applies when demand exceeds 140
    shortage_cost = max(0, demand - replenishment_level) * shortage_cost_value
    
    # Total Profit
    profit = revenue - cogs - inventory_cost - shortage_cost
    return profit

# Simulate monthly profits
profits = []
for _ in range(num_simulations):
    # Simulate demand using normal distribution
    demand = np.random.normal(mean_demand, std_dev_demand)
    # Ensure demand is a non-negative integer
    demand = max(0, round(demand))
    # Calculate profit for the simulated month
    profit = calculate_profit(demand)
    profits.append(profit)

# Calculate the average profit
average_profit = np.mean(profits)
average_profit = round(average_profit)  # Round to the nearest dollar

# Output the result
print(f"The average monthly profit from stocking 140 goggles is: ${average_profit}")