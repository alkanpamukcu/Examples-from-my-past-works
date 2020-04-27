import datetime


class InventoryProduct:  # inventory product class
    def __init__(self, name_, stock_amount_, price_):
        self.name = name_
        self.price = price_
        self.stock_amount = stock_amount_


class BasketProduct(InventoryProduct):  # basket product class, subclass of inventoryProduct
    basket_amount = 0

    def modify_amount(self, new_amount):
        self.basket_amount = new_amount


class Basket:  # Basket class, holds contents of the basket in a dictionary.
    def __init__(self):
        self.contents = dict()
        self.total_value = 0

    def display_contents(self):  # Prints the contents of the basket using a list. List is used instead of dictionary
        # to prevent any enumeration confusion. Also returns the number of items in the basket. Will be useful later.
        if len(self.contents.keys()) == 0:
            print("\nYour basket is empty.")
        else:
            print("\nYour basket contains:")
        basket_list = []
        for j in self.contents.keys():
            basket_list.append(j)
            print(str(basket_list.index(j) + 1) + ". " + j + " price=$" + str(self.contents[j].price) +
                  " amount=" + str(self.contents[j].basket_amount) + " total=$" +
                  str(float(self.contents[j].price)*self.contents[j].basket_amount))
        print("Total price=$" + str(self.total_value))
        return len(basket_list)

    def show_basket_submenu(self):  # Shows and operates the basket submenu. Returns the choice the user made, which
        # will be used in the market class.
        print("\nPlease Choose an option:\n"
              "1.Update amount\n"
              "2.Remove an item\n"
              "3.Check out\n"
              "4.Go back to main menu\n\n")
        input_a = input("Your selection:")
        while input_a not in ["1", "2", "3", "4"]:
            input_a = input("Please give a valid input. Valid inputs are 1,2,3,4.")
        if input_a == "1":
            self.update_item()
            self.display_contents()
            return 1
        elif input_a == "2":
            self.remove_item()
            self.display_contents()
            return 2
        elif input_a == "3":
            return 3
        else:
            return 0

    def add_item(self, product, amount):  # When an item is added to the basket, creates a new instance of the
        # BasketProduct object and adds it to the basket. Also modifies total value of the basket.
        prod = BasketProduct(product.name, product.stock_amount, product.price)
        prod.modify_amount(amount)
        self.total_value += float(amount*prod.price)
        self.contents[prod.name] = prod

    def update_item(self):  # Updates the amount of a certain item in the basket. Uses a list as a helper variable,
        # so that there is no enumeration errors. If the updated amount is 0, removes the item from the list instead.
        # Modifies the total_value accordingly.
        basket_list = []
        for j in self.contents.keys():
            basket_list.append(j)
        input_a = int(input("Which item do you want to update?"))
        while input_a > len(basket_list) or input_a < 1:
            input_a = int(input("Please give valid input."))
        input_b = int(input("To what amount do you want to update this item?"))
        while input_b > self.contents[basket_list[input_a - 1]].stock_amount:
            input_b = int(input("Sorry, the amount exceeds the limit, please try again with smaller amount."))
        self.total_value -= self.contents[basket_list[input_a - 1]].price * \
                            (self.contents[basket_list[input_a - 1]].basket_amount-input_b)
        if input_b == 0:
            del self.contents[basket_list[input_b-1]]
        else:
            self.contents[basket_list[input_a - 1]].modify_amount(input_b)
        print("Item updated!")

    def remove_item(self):  # Removes the selected item from the basket. Also uses a list to avoid enumeration errors.
        # Modifies the total_value accordingly.
        basket_list = []
        for j in self.contents.keys():
            basket_list.append(j)
        input_a = int(input("Which item do you want to remove?"))
        while input_a > len(basket_list) or input_a < 1:
            input_a = int(input("Please give valid input."))
        self.total_value -= self.contents[basket_list[input_a - 1]].price * \
                            self.contents[basket_list[input_a - 1]].basket_amount
        del self.contents[basket_list[input_a - 1]]
        print("Item deleted!")


class User:  # User class. Initializes necessary variables for users.
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.basket = Basket()


# Raw data.
inventory_source = {'asparagus':  [10, 5], 'broccoli': [15, 6], 'carrots': [18, 7], 'apples': [20, 5],
                    'banana': [10, 8], 'berries': [30, 3], 'eggs': [50, 2], 'mixed fruit juice': [0, 8],
                    'fish sticks': [25, 12], 'ice cream': [32, 6], 'apple juice': [40, 7],
                    'orange juice': [30, 8], 'grape juice': [10, 9]}
users_source = {'ahmet': '1234', 'meryem': '4444'}


class Market:  # Market class, whole application is operated here. Has all the necessary methods.
    def __init__(self):  # Initializes inventory and users dictionaries, accepts data from our raw data.
        self.inventory = dict()
        self.users = dict()
        for i in inventory_source:
            self.inventory[i] = InventoryProduct(i, inventory_source[i][0], inventory_source[i][1])
        for i in users_source:
            self.users[i] = User(i, users_source[i])

    def login(self):  # Operates login screen, sends the correct username to the show_market_menu method.
        print("****Welcome to BOUN Online Market****\n"
              "Please log in by providing your user credentials:")
        input_a = input("User Name:")
        input_b = input("Password:")
        while input_a not in self.users or self.users[input_a].password != input_b:
            print("\nYour user name and/or password is not correct. Please try again!\n")
            input_a = input("User Name:")
            input_b = input("Password:")
        self.show_market_menu(self.users[input_a])

    def show_market_menu(self, user):  # Operates the main menu and calls for necessary methods depending on user input.
        print("\nWelcome, "+user.username+"! Please choose one of the following options by "
                                          "entering the corresponding menu number.\n"
              "Please choose one of the following services:\n\n"
              "1.Search for a product\n"
              "2.See Basket\n"
              "3.Check Out\n"
              "4.Logout\n"
              "5.Exit\n")
        input_a = input("Your Choice: ")  # Accepts the input as string to avoid complications. Converts to int later.
        while input_a not in ["1", "2", "3", "4", "5"]:
            input_a = input("\nPlease give valid input. Valid inputs are 1,2,3,4,5.")
        input_a = int(input_a)
        if input_a == 1:
            self.search(user)
            self.show_market_menu(user)  # After the execution of the search method, returns back to the main menu.
        elif input_a == 2:
            basket_list_len = user.basket.display_contents()
            if basket_list_len == 0:  # If 'see basket' is selected and the basket is empty, returns to the main menu.
                self.show_market_menu(user)
            else:
                status = user.basket.show_basket_submenu()
                if status == 3:  # If the user checked out in the basket submenu, the status is 3 and main menu
                    # operates accordingly.
                    self.check_out(user)
                else:  # If the user did anything else, program returns back to the main menu.
                    self.show_market_menu(user)
        elif input_a == 3:
            self.check_out(user)
        elif input_a == 4:  # Returns to the login page. Basket information of the user is saved for later use.
            self.login()
        elif input_a == 5:  # Exits the program.
            exit()

    def search(self, user):  # Search method.
        search_list = []
        input_a = input("\nWhat are you searching for? ")
        for i in self.inventory.keys():  # If a key in inventory dictionary contains the input, adds the key to a list.
            if input_a in i and self.inventory[i].stock_amount != 0:
                search_list.append(i)
        while len(search_list) == 0:  # Keeps asking for new keywords until the inventory contains at least 1 key
            # that contains the keyword. Or until the user wants to return to the main menu by typing 0.
            input_a = input("Your search did not match any items. Please try something else (Enter 0 for main menu):")
            if input_a == "0":
                self.show_market_menu(user)
            else:
                for i in self.inventory.keys():
                    if input_a in i and self.inventory[i].stock_amount != 0:
                        search_list.append(i)
        print("\nFound " + str(len(search_list)) + " similar items:")
        i = 0
        temp_list = []
        for j in range(len(search_list)):  # Prints the found items. Also adds indexes of the items to a list as
            # strings, which will be useful when the user wants to select an item.
            print(str(j + 1) + ". " + search_list[j] + ", price: $" + str(self.inventory[search_list[j]].price))
            i += 1
            temp_list.append(str(i))
        input_b = input("\nPlease select which item you want to add to your basket.(Enter 0 for main menu:)")
        while input_b != 0 and input_b not in temp_list:  # Asks user for a valid input.
            input_b = input("\nPlease give a valid input.")
        input_b = int(input_b)  # Converts the valid input to integer, since we need it in integer form for search_list
        # operations.
        if input_b == 0:  # Returns to the main menu if user types 0.
            self.show_market_menu(user)
        elif search_list[input_b-1] in user.basket.contents.keys():  # If item is already in the basket, asks the user
            # to update its amount instead.
            print("Item already in basket, please update the amount of the item instead. Going back to main menu.\n")
            self.show_market_menu(user)
        else:  # Item is ready to be added to the basket.
            input_c = int(input("Adding " + self.inventory[search_list[input_b - 1]].name + ". Enter amount: "))
            while input_c > self.inventory[search_list[input_b - 1]].stock_amount:  # Asks for an amount that is lower
                # than the stock amount.
                input_c = int(input("Sorry, the amount exceeds the limit, please try again with smaller amount.\n"
                                    "Amount (Enter 0 for main menu): "))
            if input_c != 0:  # If amount is 0, do nothing. Otherwise, add the item to the basket by calling the
                # 'add_item' method of Basket class. Since the 'add_item' method can not access to stock amount, all
                # the necessary stock amount checks are done in this method and then passed to the 'add_item' method.
                user.basket.add_item(self.inventory[search_list[input_b - 1]], input_c)
                print(str(input_c) + " " + self.inventory[search_list[input_b - 1]].name + " are added to your basket.")
                print("Remaining " + self.inventory[search_list[input_b - 1]].name + " amount: " +
                      str(self.inventory[search_list[input_b - 1]].stock_amount-input_c))
                print("Going back to main menu...")

    def update_stock_amount(self, product, sold_amount):  # Updates the stock amount. Does not have much functionality.
        # Could be implemented in check_out method instead but the project pdf specifies the method,
        # so I implemented it.
        self.inventory[product].stock_amount -= sold_amount

    def check_out(self, user):  # Operates the check out process with the help of print_receipt and update_stock_amount
        # methods. For each item in the basket, the stock amount needs to be updated.
        for i in user.basket.contents:
            self.update_stock_amount(i, user.basket.contents[i].basket_amount)
        self.print_receipt(user.basket)
        self.show_market_menu(user)  # Returns back to the main menu.

    def print_receipt(self, basket):  # Prints the receipt. Does not have much functionality. Could be implemented in
        # check_out method instead but the project pdf specifies the method, so I implemented it.
        print("\nProcessing your receipt...\n"
              "******* BOUN Online Market ********\n"
              "************************************\n"
              "\t4444034\n"
              "\tboun.edu.tr\n"
              "------------------------------------")
        for j in basket.contents:
            print(j + " price=$" + str(basket.contents[j].price) + " amount=" + str(basket.contents[j].basket_amount) +
                  " total=$" + str(float(basket.contents[j].price) * basket.contents[j].basket_amount))
        print("------------------------------------\n"
              "Total\t" + str(basket.total_value)+"\n"
              "------------------------------------\n"
              ""+datetime.datetime.now().strftime("%x")+"\t"+datetime.datetime.now().strftime("%X")+"\n"
              "Thank You for using our Market!\n")


market = Market()  # Creates an instance of the Market class.
market.login()  # Starts the execution of the program.
