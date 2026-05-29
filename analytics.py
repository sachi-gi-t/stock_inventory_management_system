import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

# Load and clean data
df = pd.read_csv("data.csv")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df = df.dropna()
df["value"] = df["quantity"] * df["price"]
df["stock_status"] = df["quantity"].apply(lambda x: "Low" if x < 5 else "OK")

# Base theme colors
base_colors = ["#F5CBA7", "#6A0DAD", "#000000", "#FF8C00"]

sns.set_style("whitegrid")

# Create figure 2x2
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

#Barplot: Inventory Value per Product
random.shuffle(base_colors)
bar_colors = [base_colors[i % len(base_colors)] for i in range(len(df))]
sns.barplot(x="name", y="value", data=df, ax=axs[0,0], palette=None)
for bar, color in zip(axs[0,0].patches, bar_colors):
    bar.set_facecolor(color)
axs[0,0].set_title("Inventory Value per Product", fontsize=14, fontweight='bold')
axs[0,0].tick_params(axis='x', rotation=45)

# Lineplot: Quantity Trend
random.shuffle(base_colors)
line_color = random.choice(base_colors)
sns.lineplot(x="name", y="quantity", data=df, ax=axs[0,1], marker="o", color=line_color)
axs[0,1].set_title("Product Quantity Trend", fontsize=14, fontweight='bold')
axs[0,1].tick_params(axis='x', rotation=45)

# Scatter Plot: Quantity vs Price
scatter_colors = [random.choice(base_colors) for _ in range(len(df))]
sns.scatterplot(x="quantity", y="price", data=df, ax=axs[1,0], hue="stock_status",
                palette={"Low": scatter_colors[0], "OK": scatter_colors[1]}, s=120)
axs[1,0].set_title("Quantity vs Price", fontsize=14, fontweight='bold')
axs[1,0].legend(title="Stock Status")

# Heatmap: Correlation

cmap_options = ["magma", "viridis", "plasma", "cividis"]
heatmap_cmap = random.choice(cmap_options)
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap=heatmap_cmap, ax=axs[1,1])
axs[1,1].set_title("Correlation Heatmap", fontsize=14, fontweight='bold')

# Layout adjustment
plt.tight_layout()
plt.show()