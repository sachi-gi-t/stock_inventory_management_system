import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("data.csv")


# Sort by quantity

df = df.sort_values(by="quantity", ascending=False)
plt.figure(figsize=(10,5))

sns.lineplot(x="name", y="quantity", data=df, marker="o")

plt.xticks(rotation=45)
plt.title("Product Trend")

plt.show()





































# Add value column
# df["value"] = df["quantity"] * df["price"]

# plt.figure(figsize=(10, 5))

# sns.barplot(x="name", y="value", data=df)

# plt.xticks(rotation=45)
# plt.title("Stock Inventory Value per Product")
# plt.xlabel("Product Name")
# plt.ylabel("Value")

# plt.tight_layout()
# plt.show()