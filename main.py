import inventory

width = 80 
print("\n" + "=" * width)
print("STOCK INVENTORY MANAGEMENT SYSTEM".center(width))
print("=" * width)

def login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if username == "admin" and password == "1234":
        print("Login Successful!\n".center(width))
        return True
    else:
        print("Invalid Login!".center(width))
        return False
if not login():
    exit()

while True:
    width = 80 
    print("\n" + "=" * width)
    print("STOCK INVENTORY MANAGEMENT SYSTEM".center(width))
    print("=" * width)
    print("1. Add Product")
    print("2. View Products")
    print("3. Update Product")
    print("4. Search Product")
    print("5. Total Inventory Value")
    print("6. Low Stock Alert")
    print("7. Delete Product")
    print("8. Exit")
    

    choice = input("Enter choice: ")

    if choice == "1":
        inventory.add_product()
    elif choice == "2":
        inventory.view_products()
    elif choice == "3":
        inventory.update_product()
    elif choice == "4":
        inventory.search_product()
    elif choice == "5":
        inventory.total_inventory_value()
    elif choice == "6":
        inventory.low_stock()
    elif choice == "7":
        inventory.delete_product()
    elif choice == "8":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")