# type: ignore
from abc import ABC, abstractmethod
import json
import os

INVENTORY = "inventory.json"

class Product(ABC):
    def __init__(self, product_id: int, name: str, price: float, quantity: int):
        self.__product_id = product_id
        self.name = name
        self.__price = price
        self.quantity = quantity

    @abstractmethod
    def restock(self, amount: int):
        pass

    @abstractmethod
    def sell(self, amount: int):
        pass

    def get_product_id(self):
        return self.__product_id

    def get_total_value(self):
        return self.__price * self.quantity

    def __str__(self):
        return f"Product ID: {self.__product_id}, Name: {self.name}, Price: {self.__price}, Quantity: {self.quantity}"


class Electronics(Product):
    def __init__(self, product_id, name, price, quantity, warranty_period, brand):
        self.warranty_period = warranty_period
        self.brand = brand
        super().__init__(product_id, name, price, quantity)

    def __str__(self):
        return super().__str__() + f", Warranty Period: {self.warranty_period}, Brand: {self.brand}"

    def restock(self, amount: int):
        self.quantity += amount

    def sell(self, amount: int):
        if self.quantity >= amount:
            self.quantity -= amount
        else:
            print("Not enough quantity available.")


class Grocery(Product):
    def __init__(self, product_id, name, price, quantity, expiration_date):
        self.expiration_date = expiration_date
        super().__init__(product_id, name, price, quantity)

    def __str__(self):
        return super().__str__() + f", Expiration Date: {self.expiration_date}"

    def is_expired(self):
        if self.expiration_date < "2025-10-01":
            return True
        return False

    def restock(self, amount: int):
        self.quantity += amount

    def sell(self, amount: int):
        if self.quantity >= amount:
            self.quantity -= amount
        else:
            print("Not enough quantity available.")


class Clothing(Product):
    def __init__(self, product_id, name, price, quantity, size, material):
        self.size = size
        self.material = material
        super().__init__(product_id, name, price, quantity)

    def __str__(self):
        return super().__str__() + f", Size: {self.size}, Material: {self.material}"

    def restock(self, amount: int):
        self.quantity += amount

    def sell(self, amount: int):
        if self.quantity >= amount:
            self.quantity -= amount
        else:
            print("Not enough quantity available.")


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        for p in self.products:
         if p.get_product_id() == product.get_product_id():
            print("Error: A product with this ID already exists ❌")
            return
        self.products.append(product)
        print("Product added successfully ✅")

    def remove_product(self, product_id: int):
        if not self.products:
            print("No products in inventory ❌")
            return
        for product in self.products:
            if product.get_product_id() == product_id:
                self.products.remove(product)
                print("Product removed successfully ✅")
                return

    def search_product_by_name(self, name: str):
        for product in self.products:
            if product.name == name:
                return product
        return None

    def search_product_by_type(self, product_type: str):
        result = []
        for product in self.products:
            if isinstance(product, eval(product_type)):
                result.append(product)
        return result

    def list_all_products(self):
        if not self.products:
            print("No products in inventory ❌")
            return
        for product in self.products:
            print(product)

    def sell_product(self, product_id: int, quantity: int):
        if not self.products:
            print("No products in inventory ❌")
            return
        for product in self.products:
            if product.get_product_id() == product_id:
                product.sell(quantity)
                print("Product sold successfully ✅")
                return

    def restock_product(self, product_id: int, quantity: int):
        if not self.products:
            print("No products in inventory ❌")
            return
        for product in self.products:
            if product.get_product_id() == product_id:
                product.restock(quantity)
                print("Product restocked successfully ✅")
                return

    def total_inventory_value(self):
        if not self.products:
            print("No products in inventory ❌")
            return 0
        total = 0
        for product in self.products:
            total += product.get_total_value()
        return total

    def remove_expired_products(self):
        if not self.products:
            print("No products in inventory ❌")
            return
        for product in self.products:
            if isinstance(product, Grocery):
                if product.is_expired():
                    self.products.remove(product)
                    print("Expired product removed successfully ✅")
                    return
                else:
                    print("No expired products found ❌")
                    return

    def save_to_file(self):
        data = []
        for product in self.products:
            prod_type = type(product).__name__
            common_data = {
                "type": prod_type,
                "product_id": product.get_product_id(),
                "name": product.name,
                "price": product._Product__price,
                "quantity": product.quantity
            }
            if isinstance(product, Electronics):
                common_data.update({
                    "warranty_period": product.warranty_period,
                    "brand": product.brand
                })
            elif isinstance(product, Grocery):
                common_data.update({
                    "expiration_date": product.expiration_date
                })
            elif isinstance(product, Clothing):
                common_data.update({
                    "size": product.size,
                    "material": product.material
                })
            data.append(common_data)
        with open(INVENTORY, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        if not os.path.exists(INVENTORY):
            return
        with open(INVENTORY, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return
        for item in data:
            ptype = item["type"]
            if ptype == "Electronics":
                product = Electronics(item["product_id"], item["name"], item["price"], item["quantity"],
                                      item["warranty_period"], item["brand"])
            elif ptype == "Grocery":
                product = Grocery(item["product_id"], item["name"], item["price"], item["quantity"],
                                  item["expiration_date"])
            elif ptype == "Clothing":
                product = Clothing(item["product_id"], item["name"], item["price"], item["quantity"],
                                   item["size"], item["material"])
            else:
                continue
            self.products.append(product)


def main():
    print("Welcome to the Inventory Management System!")
    inventory = Inventory()
    inventory.load_from_file()

    while True:
        print("\nMenu:")
        print("1. ➕ Add Product")
        print("2. ➖ Remove Product")
        print("3. 🔎 Search Product by Name")
        print("4. 🔎 Search Product by Type")
        print("5. 📋 List All Products")
        print("6. 🛒 Sell Product")
        print("7. 📦 Restock Product")
        print("8. 📈 Total Inventory Value")
        print("9. 📅 Remove Expired Products")
        print("10. 🚪 Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            product_id = int(input("Enter product ID: "))
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            product_type = input("Enter product type (Electronics, Grocery, Clothing): ").lower()

            if product_type == "electronics":
                warranty_period = input("Enter warranty period: ")
                brand = input("Enter brand: ")
                product = Electronics(product_id, name, price, quantity, warranty_period, brand)
            elif product_type == "grocery":
                expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
                product = Grocery(product_id, name, price, quantity, expiration_date)
            elif product_type == "clothing":
                size = input("Enter size: ")
                material = input("Enter material: ")
                product = Clothing(product_id, name, price, quantity, size, material)
            else:
                print("Invalid product type.")
                continue
            inventory.add_product(product)
            inventory.save_to_file()

        elif choice == "2":
            product_id = int(input("Enter product ID to remove: "))
            inventory.remove_product(product_id)
            inventory.save_to_file()

        elif choice == "3":
            name = input("Enter product name to search: ")
            product = inventory.search_product_by_name(name)
            if product:
                print(product)
            else:
                print("Product not found ❌")

        elif choice == "4":
            product_type = input("Enter product type to search (Electronics, Grocery, Clothing): ")
            product_type = product_type.title()
            products = inventory.search_product_by_type(product_type)
            if products:
                for product in products:
                    print(product)
            else:
                print("No products found of this type ❌")

        elif choice == "5":
            inventory.list_all_products()

        elif choice == "6":
            product_id = int(input("Enter product ID to sell: "))
            quantity = int(input("Enter quantity to sell: "))
            inventory.sell_product(product_id, quantity)
            inventory.save_to_file()

        elif choice == "7":
            product_id = int(input("Enter product ID to restock: "))
            quantity = int(input("Enter quantity to restock: "))
            inventory.restock_product(product_id, quantity)
            inventory.save_to_file()

        elif choice == "8":
            total_value = inventory.total_inventory_value()
            print(f"Total inventory value: {total_value}")

        elif choice == "9":
            inventory.remove_expired_products()
            inventory.save_to_file()

        elif choice == "10":
            inventory.save_to_file()
            print("Exiting the system. Goodbye! 👋")
            break

        else:
            print("Invalid choice. Please try again ‼️")


if __name__ == "__main__":
    main()
