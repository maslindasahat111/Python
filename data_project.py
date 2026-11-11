import pandas as pd
import matplotlib.pyplot as plt

# 1. CREATE MOCK DATA (Simulating a messy CSV file)
data = {
    'Transaction_ID':[101, 102, 103, 104, 105, 106, 107, 108],
    'Customer_ID': ['C1', 'C2', 'C1', 'C3', 'C2', 'C1', 'C4', 'C3'],
    'Product_Category': ['Electronics', 'Clothing', 'Electronics', 'Home', 'Clothing', 'Electronics', 'Home', 'Clothing'],
    'Revenue': [1200, 45, 850, None, 120, 300, 450, 65],  # Contains a missing value (None)
    'Region': ['North', 'East', 'North', 'West', 'East', 'South', 'West', 'East']
}
df = pd.DataFrame(data)

print("--- RAW DATA ---")
print(df)
print("\n" + "="*40 + "\n")

# 2. DATA CLEANING
# Real data is messy. Let's fix the missing revenue by filling it with the average revenue.
avg_revenue = df['Revenue'].mean()
df['Revenue'] = df['Revenue'].fillna(avg_revenue)

print("--- CLEANED DATA (Missing Revenue Fixed) ---")
print(df)
print("\n" + "="*40 + "\n")

# 3. DATA ANALYSIS (Answering Business Questions)
# Question A: Which region brought in the most revenue?
regional_sales = df.groupby('Region')['Revenue'].sum().reset_index()

# Question B: Who are our top-spending customers?
customer_spending = df.groupby('Customer_ID')['Revenue'].sum().sort_values(ascending=False)

print("--- INSIGHT A: Total Revenue by Region ---")
print(regional_sales)
print("\n--- INSIGHT B: Top Spending Customers ---")
print(customer_spending)
print("\n" + "="*40 + "\n")

# 4. DATA VISUALIZATION
# Let's create a bar chart for Regional Revenue to present to stakeholders
plt.figure(figsize=(8, 5))
plt.bar(regional_sales['Region'], regional_sales['Revenue'], color='skyblue', edgecolor='black')

# Adding labels and titles
plt.title('Total Revenue Contribution by Region', fontsize=14, fontweight='bold')
plt.xlabel('Region', fontsize=12)
plt.ylabel('Revenue (USD)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Display the chart
print("📊 Generating chart window... Close the chart window to finish the script.")
plt.show()
