import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the dataset
file_name = "ecommerce_sales_analytics_5000.csv"
df = pd.read_csv(file_name)

# Clean up column names
df.columns = df.columns.str.strip()

print("--- Data Successfully Loaded ---")
print(f"Total Transactions: {len(df)}")
print("\nFirst 5 rows of data:")
print(df.head())

# 2. Key Business Metrics
print("\n--- Key Business Insights ---")
category_revenue = df.groupby('product_category')['revenue'].sum().sort_values(ascending=False)
print("\nTotal Revenue by Product Category:")
print(category_revenue)

region_revenue = df.groupby('region')['revenue'].sum().sort_values(ascending=False)
print("\nTotal Revenue by Region:")
print(region_revenue)

payment_counts = df['payment_method'].value_counts()
print("\nMost Popular Payment Methods:")
print(payment_counts)

# 3. Data Visualization
print("\n--- Generating Visualization Charts... ---")
sns.set_theme(style="whitegrid")

# Chart 1: Revenue by Product Category
## plt.figure(figsize=(8, 5))
## sns.barplot(x=category_revenue.index, y=category_revenue.values, palette="Blues_r")
## plt.title("Total Revenue by Product Category")
## plt.tight_layout()
## plt.savefig("revenue_by_category.png")
## plt.show()

#Chart 2 : Revenue by Region
## plt.figure(figsize=(8, 5))
## sns.barplot(x=region_revenue.index, y=region_revenue.values, palette="Greens_r")
## plt.title("Total Revenue by Region")
## plt.tight_layout()
## plt.savefig("revenue_by_region.png")
## plt.show()

##Chart 3: Payment Method Distribution
plt.figure(figsize=(8, 5))
sns.countplot(x='payment_method', data=df, palette="Set2")
plt.title("Payment Method Distribution")
plt.tight_layout()
plt.savefig("payment_method_distribution.png")
plt.show()
