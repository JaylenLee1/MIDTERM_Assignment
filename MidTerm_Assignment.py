import re

# Constants
TAX_RATE = 0.0825
DISCOUNT_THRESHOLD = 100.00
DISCOUNT_RATE = 0.10
DELIVERY_FEE = 10.00

# Sample product list
PRODUCTS = {
    1: {"name": "Widget A", "price": 25.00},
    2: {"name": "Widget B", "price": 35.00},
    3: {"name": "Widget C", "price": 45.00},
    4: {"name": "Gadget A", "price": 55.00},
    5: {"name": "Gadget B", "price": 65.00},
}


def is_valid_phone(phone):
    """Validate phone number format."""
    pattern = r'^\d{10}$'  # Simple pattern for 10-digit numbers
    return re.match(pattern, phone)


def is_valid_email(email):
    """Validate email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def input_customer_info():
    """Input and validate customer information."""
    while True:
        name = input("Enter customer name: ")
        phone = input("Enter phone number (10 digits): ")
        if not is_valid_phone(phone):
            print("Invalid phone number. Please enter a valid 10-digit phone number.")
            continue

        email = input("Enter email address: ")
        if not is_valid_email(email):
            print("Invalid email format. Please enter a valid email.")
            continue

        return {
            "name": name,
            "phone": phone,
            "email": email,
        }


def display_product_list():
    """Display the available products."""
    print("\nAvailable Products:")
    for product_id, product in PRODUCTS.items():
        print(f"ID: {product_id}, Name: {product['name']}, Price: ${product['price']:.2f}")


def calculate_total_cost(order_items):
    """Calculate the total cost of the order, apply discounts if applicable."""
    total_cost = sum(PRODUCTS[product_id]["price"] * quantity for product_id, quantity in order_items.items())

    if total_cost > DISCOUNT_THRESHOLD:
        total_cost *= (1 - DISCOUNT_RATE)  # Apply discount

    total_cost += total_cost * TAX_RATE  # Apply tax
    return total_cost


def save_order_to_file(customer_info, order_items, total_cost, delivery_choice):
    """Save order information to a text file."""
    with open("orders.txt", "a") as file:
        file.write(f"Customer: {customer_info['name']}\n")
        file.write(f"Phone: {customer_info['phone']}\n")
        file.write(f"Email: {customer_info['email']}\n")
        file.write("Ordered Items:\n")
        for product_id, quantity in order_items.items():
            product_name = PRODUCTS[product_id]["name"]
            file.write(f"- {product_name}: {quantity}\n")
        file.write(f"Total Cost: ${total_cost:.2f}\n")
        file.write(f"Delivery Option: {delivery_choice}\n")
        file.write("\n")


def main():
    """Main function to control the flow of the program."""
    customer_info = input_customer_info()
    display_product_list()

    order_items = {}
    while True:
        try:
            product_id = int(input("Enter product ID to purchase (or 0 to finish): "))
            if product_id == 0:
                break
            if product_id not in PRODUCTS:
                print("Invalid product ID. Please try again.")
                continue

            quantity = int(input("Enter quantity: "))
            if quantity < 1:
                print("Quantity must be at least 1.")
                continue

            order_items[product_id] = order_items.get(product_id, 0) + quantity

        except ValueError:
            print("Invalid input. Please enter numeric values for product ID and quantity.")

    delivery_choice = input("Choose delivery (yes) or pickup (no): ").strip().lower()
    total_cost = calculate_total_cost(order_items)

    if delivery_choice == "yes":
        total_cost += DELIVERY_FEE

    print(f"\nFinal Order Amount: ${total_cost:.2f}")
    save_order_to_file(customer_info, order_items, total_cost, delivery_choice)

    print("Order saved. Thank you for your purchase!")


if __name__ == "__main__":
    main()
