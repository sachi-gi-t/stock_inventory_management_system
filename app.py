import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import random
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


 

def random_color_list(n):
    """Generate n random hex colors"""
    return ['#' + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in range(n)]

def load_data():
    df = pd.read_csv("data.csv")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna()
    df["value"] = df["quantity"] * df["price"]
    return df

def add_product(df, pid, name, quantity, price):
    new_row = pd.DataFrame([[pid, name, quantity, price, quantity*price]], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("data.csv", index=False)
    return df


st.title("Stock Inventory Management System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# st.set_page_config(layout="wide")

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "View Inventory", "Add Product", "Update Product", "Search Product", "Delete Product", "Total Value"]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

df = load_data()

if menu == "View Inventory":
    st.subheader(" Product List")
    st.dataframe(df)

elif menu == "Delete Product":
    st.subheader("Delete Product")
    pid = st.text_input("Enter Product ID to delete")

    if st.button("Delete"):
        df = df[df["id"] != pid]
        df.to_csv("data.csv", index=False)
        st.success("Product Deleted Successfully!")

elif menu == "Add Product":
    st.subheader("Add New Product")
    pid = st.text_input("Product ID")
    name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=0)
    price = st.number_input("Price", min_value=0)

    if st.button("Add Product"):
        df = add_product(df, pid, name, quantity, price)
        st.success(" Product Added Successfully!")
        st.dataframe(df)

elif menu == "Update Product":
    st.subheader("Update Product")

    # Select product by ID
    product_ids = df["id"].tolist()
    selected_id = st.selectbox("Select Product ID", product_ids)

    # Get selected product row
    product = df[df["id"] == selected_id].iloc[0]

    # Pre-fill values
    new_name = st.text_input("Product Name", product["Name"])
    new_quantity = st.number_input("Quantity", value=int(product["Quantity"]))
    new_price = st.number_input("Price", value=int(product["Price"]))

    if st.button("Update Product"):
        # Update values in dataframe
        df.loc[df["id"] == selected_id, "Name"] = new_name
        df.loc[df["id"] == selected_id, "Quantity"] = new_quantity
        df.loc[df["id"] == selected_id, "Price"] = new_price

        df.columns = df.columns.str.strip().str.upper()

        # Save back to CSV
        df.to_csv("data.csv", index=False)

        st.success("✅ Product Updated Successfully!")

        st.rerun()



elif menu == "Search Product":
    st.subheader(" Search Product")
    search = st.text_input("Enter Product Name or ID")
    if st.button("Search"):
        result = df[(df["name"].str.contains(search, case=False)) | (df["id"]==search)]
        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("Product not found!")



elif menu == "Total Value":
    st.subheader("Stock Inventory Value")
    total_value = df["value"].sum()
    st.metric("Total Stock Inventory Value", f"₹{total_value}")
    st.dataframe(df[["name","quantity","price","value"]])


elif menu == "Dashboard":
    sns.set_style("darkgrid")
    q_low = df["price"].quantile(0.05)
q_high = df["price"].quantile(0.95)
df_clean = df[(df["price"] >= q_low) & (df["price"] <= q_high)]
st.subheader("Interactive Analytics Dashboard")

    
selected_products = st.multiselect("Select Products to Display", df["name"].unique(), default=df["name"].unique())
df_filtered = df[df["name"].isin(selected_products)]
n = len(df_filtered)

    

fig_bar = px.bar(
        df_filtered, x="name", y="value", color="name", 
        color_discrete_sequence=random_color_list(n),
        title="Stock Inventory Value per Product",
        hover_data={"quantity": True, "price": True, "value": True}
    )
st.plotly_chart(fig_bar, use_container_width=True)

  
fig_line = px.line(
        df_filtered.sort_values("quantity"), x="name", y="quantity", markers=True,
        color_discrete_sequence=random_color_list(n),
        title="Product Quantity Trend",
        hover_data={"quantity": True, "price": True}
    )
st.plotly_chart(fig_line, use_container_width=True)

  
fig_scatter = px.scatter(
        df_filtered, x="quantity", y="price", color="name", size="value",
        color_discrete_sequence=random_color_list(n),
        title="Quantity vs Price Scatter",
        hover_data={"value": True, "id": True}
    )
st.plotly_chart(fig_scatter, use_container_width=True)

   
fig_hist = px.histogram(
        df_filtered, x="quantity", nbins=10,
        color_discrete_sequence=random_color_list(1),
        title="Quantity Distribution",
        hover_data={"name": True}
    )
st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("📊 Advanced Data Analysis (Seaborn + Matplotlib)")


fig1, ax1 = plt.subplots()
sns.boxplot(y=df["price"], ax=ax1, color="purple")
ax1.set_title("Price Distribution (Box Plot)")
st.pyplot(fig1)


fig, ax = plt.subplots(figsize=(5,4))
sns.violinplot(
y=df_clean["quantity"],
color="#00CED1",
ax=ax
)
ax.set_title("Quantity Distribution (Violin)")
st.pyplot(fig)

st.subheader("Feature Relationships")

pair_fig = sns.pairplot(
    df_clean[["quantity","price","value"]],
    diag_kind="kde"
)
st.pyplot(pair_fig)

fig, ax = plt.subplots(figsize=(5,4))
sns.lineplot(
    x="name",
    y="quantity",
    data=df_clean.sort_values("quantity"),
    marker="o",
    color="#FF1493",
    ax=ax
)
plt.xticks(rotation=45)
ax.set_title("Product Quantity Trend")
st.pyplot(fig)


fig3, ax3 = plt.subplots()
sns.heatmap(df[["quantity", "price", "value"]].corr(), annot=True, cmap="coolwarm", ax=ax3)
ax3.set_title("Correlation Heatmap")
st.pyplot(fig3)



# Clean data before ML
q_low = df["price"].quantile(0.05)
q_high = df["price"].quantile(0.95)
df_clean = df[(df["price"] >= q_low) & (df["price"] <= q_high)].copy()

st.subheader("K-Means Clustering")

# Prepare data
X = df_clean[["quantity", "price"]]

# Scale data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
df_clean["Cluster"] = kmeans.fit_predict(X_scaled)
print(df.columns)

fig5, ax5 = plt.subplots(figsize=(5,4))
sns.scatterplot(
    x=df_clean["quantity"],
    y=df_clean["price"],
    hue=df_clean["Cluster"],
    palette="Set2",
    ax=ax5
)
ax5.set_title("K-Means Clustering")
st.pyplot(fig5)



st.subheader("Contour Plot (Density View)")

x = df_clean["quantity"]
y = df_clean["price"]

# Create grid
x_grid, y_grid = np.meshgrid(
    np.linspace(x.min(), x.max(), 100),
    np.linspace(y.min(), y.max(), 100)
)

z = np.sin(x_grid/100) + np.cos(y_grid/100000)  # synthetic density

fig7, ax7 = plt.subplots(figsize=(5,4))
contour = ax7.contourf(x_grid, y_grid, z, cmap="viridis")
fig7.colorbar(contour)
ax7.set_title("Contour Density Map")
st.pyplot(fig7)



st.subheader(" Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Products", len(df_filtered))
col2.metric("Total Stock Inventory Value", f"₹{df_filtered['value'].sum()}")
col3.metric("Low Stock Items (<5)", len(df_filtered[df_filtered["quantity"]<5]))