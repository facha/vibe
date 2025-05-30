from pydantic import BaseModel
from typing import List, Optional
from vibe import code

class Item(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

class ShoppingCart(BaseModel):
    items: List[Item] = []

    @code
    def add_item(self, item: Item) -> None:
        """Adds an item to the shopping cart or updates the quantity if the item already exists."""

    @code
    def remove_item(self, item_id: int) -> None:
        """Removes an item from the shopping cart by its ID."""

    @code
    def update_item_quantity(self, item_id: int, quantity: int) -> None:
        """Updates the quantity of an item in the shopping cart."""

    @code
    def calculate_total(self) -> float:
        """Calculates the total price of all items in the shopping cart."""

    @code
    def save(self, file_name: str = "cart.json"):
        """Save shopping cart to a json file."""

    @code
    def load(self, file_name: str = "cart.json"):
        """Load shopping cart from a json file."""

item1 = Item(id=1, name="Notebook", price=4.99, quantity=3)
item2 = Item(id=2, name="Pencil", price=0.99, quantity=10)
item3 = Item(id=3, name="Eraser", price=0.49, quantity=5)

print("Initializing the cart...")
cart = ShoppingCart()
cart.add_item(item1)
cart.add_item(item2)
cart.add_item(item3)
print(f"Cart: {cart}\nTotal: {cart.calculate_total()}")

print("Updating item quantity...")
cart.update_item_quantity(item_id=1, quantity=1)
print(f"Cart: {cart}\nTotal: {cart.calculate_total()}")

print("Removing item...")
cart.remove_item(item_id=1)
print(f"Cart: {cart}\nTotal: {cart.calculate_total()}")

print("Saving cart to a file...")
cart.save()

print("Loading cart back from the file...")
cart = ShoppingCart()
cart.load()
print(f"Cart: {cart}\nTotal: {cart.calculate_total()}")
