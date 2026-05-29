import csv

FILE = "data.csv"

def add_product():
    pid = input("Enter Product ID: ")
    name = input("Enter Product Name: ")
    qty = input("Enter Quantity: ")
    price = input("Enter Price: ")

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([pid, name, qty, price])

    print("Product Added Successfully!")

def view_products():
    width = 80
    
    print("\n" + "=" * width)
    print("PRODUCT LIST".center(width))
    print("=" * width)

    # Table Header
    print(f"{'ID':<10}{'NAME':<20}{'QTY':<15}{'PRICE':<15}")
    print("-" * width)

    with open("data.csv", "r") as f:
        next(f)  # skip header
        for line in f:
            id, name, qty, price = line.strip().split(",")
            print(f"{id:<10}{name:<20}{qty:<15}{price:<15}")

    print("=" * width)


def delete_product():
    pid = input("Enter Product ID to delete: ")
    rows = []

    with open(FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != pid:
                rows.append(row)

    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("Product Deleted!")

def low_stock():
    print("Low Stock Products (<5):")
    with open(FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if int(row[2]) < 5:
                print(row)

def update_product():
    pid = input("Enter Product ID to update: ")
    rows = []

    with open("data.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == pid:
                print("Current Data:", row)
                row[2] = input("Enter new Quantity: ")
                row[3] = input("Enter new Price: ")
            rows.append(row)

    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("Product Updated Successfully!") 

def search_product():
    search = input("Enter Product Name or ID to search: ")
    found = False

    with open("data.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            if search == row[0] or search.lower() == row[1].lower():
                print("Product Found:")
                print(f"ID: {row[0]} | Name: {row[1]} | Qty: {row[2]} | Price: {row[3]}")
                found = True

    if not found:
        print("Product not found!")

def total_inventory_value():
    total = 0

    print("\nProduct-wise Value:")

    with open("data.csv", "r") as file:
        next(file)  # skip header

        for line in file:
            data = line.strip().split(",")

            name = data[1]
            qty = int(data[2])
            price = int(data[3])

            value = qty * price
            total += value

            print(f"{name}: ₹{value}")

    print(f"\nTotal Inventory Value: ₹{total}")


def low_stock():  
    print("\n--- Low Stock Products ---")

    with open("data.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            if int(row[2]) < 5:
                print(f"{row[1]} (Qty: {row[2]})")      