'''==============================================================================================================================
Author: Kgothatso Masha
Date Created: 8 August 2026
Purpose: Creating a simple console based application that helps Kasi Fresh Grocers
        manage stock and loyalty points.
================================================================================================================================='''

# Importing 
import os
from datetime import datetime
'''===============================================================================================================================
                                                        A. CREATING CLASSESS
'''

'''------------------------------------------------  1. Creating the Customer class  ---------------------------------------------'''
class Customer:
    """" This class will store a customer's details and
     be able to load and save their details """
    def __init__(self, customer_id, name, loyalty_points):
        self.customer_id = customer_id #
        self.name = name
        self.loyalty_points = loyalty_points

    # This fuction adds points to the customer's loyalty points
    def add_points(self, amount): 
        self.loyalty_points += amount

    # This function redeems a customer's loyalty points
    def redeem_points(self, amount):
        if amount > self.loyalty_points: # making sure a customer cannot redeem more points than they have available
            # raising this error which will be caught later by choice3 function:
            raise ValueError(f"Customer {self.name},has only {self.loyalty_points} points to redeem.")
        self.loyalty_points -= amount

    # This function will save a customer's details or changes into a file
    def save_to_file(self, filename):
        with open(filename, "w") as file:
            file.write(f"{self.customer_id}, {self.name}, {self.loyalty_points}\n")
        print(f"Customer {self.name} is saved to the file {filename}.")

    # This function will loads the saved customer's details file
    def load_from_file(self, filename):
        # Creating an try/exception erro handling if a customer's file cannot be found 
        try: # if it is found:
            with open(filename, "r") as file:
                line = file.readline().strip()
                cusID, name, points = line.split(", ")
                self.customer_id = int(cusID)
                self.name = name
                self.loyalty_points = int(points)
            print(f"Customer {name}'s data has been loaded successfully from the file {filename}.")
            return True
        except FileNotFoundError: # If it is not found
            print(f"The file name {filename} has not been found")
            return False
####################################################################################################################################

'''--------------------------------------------  2.1 Creating the Product class  -------------------------------------------------'''
class Product():
    """ This class is a base class that stores a product's details and has
    a function that allow to restock, sell and show product information"""
    def __init__(self, product_id, name, unit_price, quantity_in_stock):
        self.product_id = product_id
        self.name = name
        self.unit_price = unit_price
        self.quantity_in_stock = quantity_in_stock

    # This function will restock a product
    def restock(self, quantity):
        self.quantity_in_stock += quantity

    # This fuction will sell a product
    def sell(self, quantity):
        if quantity > self.quantity_in_stock: # making sure more stock than available cannot be sold
            # Raising an error that will later be caught by choice2 function
            raise ValueError(f"There are only {self.quantity_in_stock} units of {self.name} left in stock.")
        self.quantity_in_stock -= quantity

    # This fuction displays the product infromation
    def display_info(self):
        return f"""
        Product ID: {self.product_id}
        Name: {self.name}
        Unit Price: {self.unit_price}
        Quantity in Stock: {self.quantity_in_stock}"""

'''---------------------  2.2 Creating Perishable Product class  -----------------------------'''
class PerishableProduct(Product):
    """ This fuctions inherits attributes from product class and stores both product details
     and adds things like expiry date and shelf life days of a product that perishes. """
    def __init__(self, product_id, name, unit_price, quantity_in_stock, expiry_date, shelf_life_days):
        super().__init__(product_id, name, unit_price, quantity_in_stock)
        self.expiry_date = expiry_date
        self.shelf_life_days = shelf_life_days
        self.shelf_life_days

    # Thus function checks if a product is perishable (has expired)
    def is_expired(self, current_date):
        return current_date > self.expiry_date

    # This function calculates shelf life days
    def update_shelf_life_days (self):
        today = datetime.now()
        expiry = datetime.strptime(self.expiry_date, "%d-%m-%Y")
        time_left = expiry - today
        self.shelf_life_days = time_left.days
        return self.shelf_life_days

    # Dispalying product information from Products class that has beem overriten
    def display_info(self):
        product_info = super().display_info()
        return f"""{product_info}
        Expiry Date: {self.expiry_date}
        Shelf Life Days: {self.update_shelf_life_days()}
        """

'''----------------------  2.3 Creating Non-Perishable Product class  -------------------------'''
class NonPerishableProduct(Product):
    """ This fuctions inherits attributes from product class and 
    stores both product details and warranty of a products that does not perish. """
    def __init__(self, product_id, name, unit_price, quantity_in_stock, warranty_months):
        super().__init__(product_id, name, unit_price, quantity_in_stock)
        self.warranty_months = warranty_months

    # Dispalying product information from Products class that has beem overriten
    def display_info(self):
        product_info = super().display_info()
        return f"""{product_info}
        Waranty Months: {self.warranty_months}
        """
#############################################################################################################################

'''----------------------------------------------  3. Creating Inventory Class  -------------------------------------------'''
class Inventory:
    """This class stores a list of Products and provides methods to add, 
    remove, find products by ID, see total value of stock, save and load inventory details"""
    def __init__(self):
        self.products = [] # list of products

    # This function searches for a product using ID
    def find_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    # This functions adds a product to the list of products
    def add_product(self, product):
        self.products.append(product)

    # This function removes a product from product list
    def remove_product(self, product_id):
        product = self.find_product(product_id)
        if product is None:
            print(f"Product with ID {product} has not been found.")
            return
        self.products.remove(product)

    # This function calculates the total value of a product
    def total_stock_value(self):
        return sum(product.unit_price * product.quantity_in_stock for product in self.products)

    # This function saves an inventory's details
    def save_to_file(self, filename):
        with open(filename, "w") as file:
            for product in self.products:
                file.write(f"{product.product_id}, {product.name}, {product.unit_price}, {product.quantity_in_stock}\n")
        print(f"Inventory has been successfully saved to file {filename} ")

    # This function will loads the saved inventory details file
    def load_from_file(self, filename):
        try: # if found
            with open(filename, "r") as file: # opens the file
                for line in file:
                    line = line.strip() # strips every line
                    if not line:
                        continue
                    product_id, name, price, quantity = line.split(", ") # splits the products with a comma
                    self.add_product(Product(int(product_id), name, float(price), int(quantity)))
            print(f"Inventory for the product {name} has been successfully loaded from file {filename}.")
            return True
        except FileNotFoundError: # if not found
            print(f"The filename {filename} has not found.")
            return False
###################################################################################################################################

'''-------------------------------------------------  4. Creating Employee Class  ------------------------------------------------'''
class Employee():
    """ This class stores an employee's details and has a function that
    calculates their pay. """
    def __init__(self, employee_id, name, branch):
        self.employee_id = employee_id
        self.name = name
        self.branch = branch

    # This returns a customer's base start as 0
    def calculate_pay(self):
        return 0.0

    # This function displays an employee's details
    def display_info(self):
        return f"""
        Employee ID: {self.employee_id}
        Name: {self.name}
        Branch: {self.branch}"""

'''--------------------------  4.2 Creating Cashier Employee Class  ---------------------------'''
class Cashier(Employee):
    """ This class inherits from Employee class and ads attributes like a cashier's
    hourly rate and hours they have worked and also has a functtion that calculates their pay using that,"""
    def __init__(self, employee_id, name, branch, hourly_rate, hours_worked):
        super().__init__(employee_id, name, branch)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    # This function returns a cashier's salary
    def calculate_pay(self):
        return self.hourly_rate * self.hours_worked

''''------------------------  4.3 Creating Manager Employee Class  -----------------------------'''
class Manager(Employee):
    """ This class inherits from Employee class and adds attributes like a manager's montly salary
    and bonus."""
    def __init__(self, employee_id, name, branch, monthly_salary, bonus):
        super().__init__(employee_id, name, branch)
        self.monthly_salary = monthly_salary
        self.bonus = bonus

    # This function returns a manager's salary
    def calculate_pay(self):
        return self.monthly_salary + self.bonus
'''================================================================================================================================'''

''''================================================================================================================================
                                                B. ADDING VALUES TO THE CLASSESS
'''

'''-----------------------------  1. Adding to Inventory class  --------------------------'''
inventory = Inventory()

# checking if the added things are in the inventory yet
inserted_inv = inventory.load_from_file("stock_list.txt") 

if not inserted_inv: 
    inventory.add_product(Product(1, "Maize Meal", 25.00, 16))
    inventory.add_product(PerishableProduct(2, "Yogurt", 23.99, 12, "16-09-2026", 0))
    inventory.add_product(NonPerishableProduct(3, "Tin fish", 18.65, 23, 24))

# Printing products i just added
print("\n----------------  Current Stock  ----------------")
for product in inventory.products:
    print(product.display_info())


'''----------------------------  2. Adding to Customer class  ------------=----------------'''
customer = Customer(1, 'Kgothatso', 32)
customer.load_from_file("customer_list.txt")



'''-------------------------  3. Adding to the Employee class  ----------------------------'''
employees = [
    Cashier(1, "Ishmael", "Mowbray", 32.0, 46),
    Manager(2, "Conlee", "Mowbray", 10000.0, 1600.0),
]

# Printing the employees i just added
print("\n----------------  Employees  ----------------")
for employee in employees:
    print(employee.display_info())
    print(f"\tPay: {employee.calculate_pay()}")


# This catches the error when redeeming more points that available
try:
    customer.redeem_points(500)
except ValueError as error:
    print(f"Error: {error}")



'''=====================================================================================================================
                                        C. Creating Functions for the Menu


''''-----------------------------  1. Creating function for option 1  -----------------------------'''
def choice1():
    """ This function displays all the products available in the inventory"""
    print("\n----------------  Current Stock  ----------------")
    for product in inventory.products:
        print(product.display_info())
    print(f"Total value of stock: R{inventory.total_stock_value():.2f}")
######################################################################################################

'''--------------------------------  2. Creating function for option 2  ---------------------------------'''
def choice2():
    """ This function allows the user to sells a product"""
    # Making sure that the user enters a valid product ID
    try:
        product_id = int(input("Enter the ID of the product you want to sell: "))
    except ValueError:
        print("Input Invalid! Please enter a valid product ID number")
        return

    # This searches for the product ID entered in the inventory
    product = inventory.find_product(product_id)
    if product is None: # if not found
        print(f"Product with ID {product} has not been found.")
        return

    # This makes sure the user enters a number of units to sell
    try:
        quantity = int(input("Enter the quantity you want to sell: "))
    except ValueError:
        print("Input Invalid, please enter a number.")
        return

    # This uses the sell function from porduct class to sell the units
    try:
        product.sell(quantity)
        print(f"{quantity} units of {product.name} has been successfully sold.")
    except ValueError as error: # this catches the error raised when selling more units that available
            print(f"Invalid: {error}")
#############################################################################################################

'''----------------------------  3. Creating function for option 3  -----------------------------'''
def choice3():
    """ This function gives the user of the system to manage points with an opition
    to either A. add points or B. redeem points. """
    # Making sure the user chooses between these options
    option = input("""
                Enter a choice between:
                A. Add points  
                B. Redeem points
                Choice: """).strip().upper()

    # Making sure the user enters the amount of points as a number:
    try:
        amount = int(input("Enter the amount of points: "))
    except ValueError:
        print("Input Invalid! Please enter a number")
        return

    # Making sure option A adds points to a customer
    if option == 'A':
        customer.add_points(amount)
        print(f"New Points: {customer.loyalty_points}")

    # Making sure option B redeems a customer's points
    elif option == 'B':
        try:
            customer.redeem_points(amount)
            print(f"New Points: {customer.loyalty_points}")
        except ValueError as error: # thus catches the error raised when redeeming more points that available
            print(f"Error: {error}")

    else:
        print("Enter choice A or B")
'''=========================================================================================================================='''

        
''''============================================================================================================================
                                                    D. CREATING THE MAIN MENU
'''

while True: # This is what allows the user to interact with the system
    print("""
    =====================================
         Kasi Fresh Grocers System
    -------------------------------------
            1. View stock
            2. Sell product
            3. Manage loyalty points
            4. Save & exit 
    =====================================""")

    try: # this intakes a user's choice
        choice = int(input("Enter your choice: "))

        if choice < 1 or choice > 4: # this makes sure the user enters a choice between 1 and 4
            print("Input Invalid! Please enter number between 1 and 4")
            continue

    except ValueError:
        print("Input Invalid! Please enter a vaild number")
        continue

    if choice == 1: # this uses choice1 function
        choice1()

    elif choice == 2: # this uses choice2 function
        choice2()

    elif choice == 3: # this uses chaice3 function
        choice3()

    # This uses the save to file functons to save both inventory and customer details
    elif choice == 4: 
        inventory.save_to_file("stock_list.txt")
        customer.save_to_file("customer_list.txt")
        print("Files have been saved.")
        break
''''=============================================================================================================================='''