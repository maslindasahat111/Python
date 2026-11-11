import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import plotly.express as px

## Importing the dataset
df = pd.read_csv("D:\\DataEngineer\\Kaggle_E_commerce_Porject\\pizza_sales.csv")

## Metadata of the dataset
print(df.head(2))
print(df.tail(2))

print("The Metadata of the dataset is:", df.shape)
print("The Row of the dataset is:", df.shape[0])
print("The Columns of the dataset is:", df.shape[1])

print(df.columns)
print(df.info())

## Data Types in Raw Data
print(df.dtypes)
print(df.describe())

## KPI's
total_revenue = df["total_price"].sum()
total_pizzas_sold = df["quantity"].sum()
total_orders = df["order_id"].nunique()
avg_order_value = total_revenue / total_orders
avg_pizzas_per_order = total_pizzas_sold / total_orders

print(f"Total Revenue is : RM{total_revenue:,.2f}")
print(f"Total Pizza Sold is : {total_pizzas_sold:,.2f}")
print(f"Total Order is : {total_orders:,.2f}")
print(f"Total Avg Order Value is: RM{avg_order_value:,.2f}")
print(f"Total Avg Pizza per Order is: {avg_pizzas_per_order:.3f}")

## Charts
## Ingredient Analysis
ingredient = (
                df['pizza_ingredients']
                .str.split(',')
                .explode()
                .str.strip()
                .value_counts()
                .reset_index()
                .rename(columns={'index':'Counts', 'pizza_ingredients': 'Indegredients'})
            )
print(ingredient.head(10))

## Daily Trend - Total Orders
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)
df['day_name'] = df['order_date'].dt.day_name()
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df['day_name'] = pd.Categorical(df['day_name'], categories=weekday_order, ordered=True)
orders_by_day = df.groupby('day_name', observed=False)['order_id'].nunique()
ax = orders_by_day.plot(kind='bar', figsize=(8,5), color='green', edgecolor='black')

plt.title("Title Orders by Day of week")
plt.xlabel("Day of Week")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)

for i, val in enumerate(orders_by_day):
    plt.text(i, val+20, str(val), ha='center', va='bottom', fontsize='9', fontweight='bold')

plt.tight_layout()
plt.show()

## Daily Trend - Total Revenue
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)
df['day_name'] = df['order_date'].dt.day_name()
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df['day_name'] = pd.Categorical(df['day_name'], categories=weekday_order, ordered=True)
orders_by_day = df.groupby('day_name', observed=False)['total_price'].sum()
ax = orders_by_day.plot(kind='bar', figsize=(8,5), color='pink', edgecolor='black')

plt.title("Title Revenue by Day of week")
plt.xlabel("Day of Week")
plt.ylabel("Total Revenues")
plt.xticks(rotation=45)

for i, val in enumerate(orders_by_day):
    plt.text(i, val+20, str(val), ha='center', va='bottom', fontsize='9', fontweight='bold')

plt.tight_layout()
plt.show()


## Hourly Trend - Total Orders
df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S')
df['order_hour'] = df['order_time'].dt.hour
orders_by_hour = df.groupby('order_hour', observed=False)['order_id'].nunique()
ax = orders_by_hour.plot(kind='bar', figsize=(8,5), color='maroon', edgecolor='black')

plt.title("Total Orders by Hour of Day")
plt.xlabel("Hour of Day(24H format)")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)

for i, val in enumerate(orders_by_hour):
    plt.text(i, val+5, str(val), ha='center', va='bottom', fontsize='9', fontweight='bold')

plt.tight_layout()
plt.show()

## Monthly Trend - Total Orders
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)
df['month_name'] = df['order_date'].dt.month_name()
month_order = ["Jan", "Feb", "Mac", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
df['month_name'] = pd.Categorical(df['month_name'], categories=month_order, ordered=True)
orders_by_month = df.groupby('month_name', observed=False)['order_id'].nunique()

plt.figure(figsize=(10,5))
plt.fill_between(orders_by_month.index, orders_by_month.values, color='orange', alpha=0.6)
plt.plot(orders_by_month.index, orders_by_month.values, color="black", linewidth=2, marker='o')


plt.title("Title Orders by Month")
plt.xlabel("Month of Years")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)

for i, val in enumerate(orders_by_month):
    plt.text(i, val+20, str(val), ha='center', va='bottom', fontsize='9', fontweight='bold')

plt.tight_layout()
plt.show()

## % of Sales by Categories
categories_sales = df.groupby('pizza_category')['total_price'].sum()
category_pct = categories_sales / categories_sales.sum() * 100

plt.figure(figsize=(7, 7))
colors = plt.get_cmap('tab20').colors

plt.pie(category_pct, labels=category_pct.index, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor':'black', 'width':0.4})
plt.title('Percentage of Sales by Pizza Category')
plt.show()

## Sales by Pizza Size & Category
sales_pivot = df.pivot_table(
    index='pizza_category',
    columns='pizza_size',
    values='total_price',
    aggfunc='sum',
    fill_value=0
)

sales_pct= sales_pivot /sales_pivot.sum().sum() * 100

plt.figure(figsize=(10, 6))
sns.heatmap(sales_pct, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=0.5)
plt.title("% of Sales by Pizza Category and Size")
plt.ylabel("Pizza Cateogry")
plt.xlabel("Pizza Size")
plt.show()

## Total Pizzas Sold by Pizza Category
pizzas_by_category = df.groupby('pizza_category')['quantity'].sum()
colors = list(plt.get_cmap('tab20').colors)
colors = colors[:len(pizzas_by_category)]

ax = pizzas_by_category.plot(kind='bar', figsize=(8,5), color=colors, edgecolor='black')

plt.title("Total PIzzas Sold by Pizza Category")
plt.xlabel("Pizza Category")
plt.ylabel("Total PIzzas Sold")
plt.xticks(rotation=45)

for i, val in enumerate(pizzas_by_category):
    plt.text(i, val+5, str(val), ha='center', va='bottom', fontsize='9', fontweight='bold')

plt.tight_layout()
plt.show()

## Top 5 BestSelling Pizza - Total Qty
pizzas_by_name = df.groupby('pizza_name')['quantity'].sum()
top5 = pizzas_by_name.sort_values(ascending=False).head(5)

ax = top5.plot(kind='bar', figsize=(8,5), color='grey', edgecolor='black')

plt.title("Top 5 Pizzas Sold")
plt.xlabel("Pizza Name")
plt.ylabel("Total PIzzas Sold")
plt.xticks(rotation=45)

for i, val in enumerate(top5):
    plt.text(i, val+2, str(val), ha='center', va='bottom', fontsize='9', fontweight='bold')

plt.tight_layout()
plt.show()

## Top 5 BestSelling Pizza - Total Order
pizzas_by_name = df.groupby('pizza_name')['order_id'].nunique()
top5 = pizzas_by_name.sort_values(ascending=False).head(5)

ax = top5.plot(kind='bar', figsize=(8,5), color='grey', edgecolor='black')

plt.title("Top 5 Pizzas Ordered")
plt.xlabel("Pizza Name")
plt.ylabel("Total PIzzas Sold")
plt.xticks(rotation=45)

for i, val in enumerate(top5):
    plt.text(i, val+2, str(val), ha='center', va='bottom', fontsize='9', fontweight='bold')

plt.tight_layout()
plt.show()

## Top 5 BestSelling Pizza - Total Sales
pizzas_by_name = df.groupby('pizza_name')['total_price'].sum()
top5 = pizzas_by_name.sort_values(ascending=False).head(5)

ax = top5.plot(kind='bar', figsize=(8,5), color='orange', edgecolor='black')

plt.title("Top 5 Pizzas by Revenue")
plt.xlabel("Pizza Name")
plt.ylabel("Total PIzzas Sold")
plt.xticks(rotation=45)

for i, val in enumerate(top5):
    plt.text(i, val+2, str(val), ha='center', va='bottom', fontsize='9', fontweight='bold')

plt.tight_layout()
plt.show()

## Bottom 5 BestSelling Pizza - Total Sales
pizzas_by_name = df.groupby('pizza_name')['total_price'].sum()
bottom5 = pizzas_by_name.sort_values(ascending=True).head(5)

ax = bottom5.plot(kind='bar', figsize=(8,5), color='Red', edgecolor='black')

plt.title("Top 5 Pizzas by Revenue")
plt.xlabel("Pizza Name")
plt.ylabel("Total PIzzas Sold")
plt.xticks(rotation=45)

for i, val in enumerate(top5):
    plt.text(i, val+2, str(val), ha='center', va='bottom', fontsize='9', fontweight='bold')

plt.tight_layout()
plt.show()