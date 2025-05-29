from dataclasses import dataclass
from typing import Any, Optional
from vibe import code


@dataclass
class Node:
    data: Any
    next: Optional["Node"] = None


@code
def create_node(data: Any) -> Node:
    """Create a new node with the given data."""


@code
def append(head: Node, data: Any = 5) -> Node:
    """Append a new node with the given data to the linked list."""


@code
def prepend(head: Node, data: Any) -> Node:
    """Prepend a new node with the given data to the linked list."""


@code
def search(head: Node, data: Any) -> Node:
    """Search for a node with the given data in the linked list."""


@code
def delete(head: Node, data: Any) -> Node:
    """Delete a node from head."""


@code
def print_list(head: Node) -> None:
    """Print the linked list data on a single line using -> as a separator."""


print("--- initialize the list ---")
head = create_node(10)
print(head)
print()

print("--- add new element ---")
head = prepend(head, 5)
print(head)
print()

print("--- add new element to an end of the list ---")
head = append(head, 20)
print(head)
print()

print("--- pretty print all elements ---")
print_list(head)
print()

print("--- find an element with data == 10 ---")
print(search(head, 10))
print()

print("--- remove an element with data == 10 ---")
head = delete(head, 10)
print(head)
print()

print("--- find an element with data == 10 ---")
print(search(head, 10))
print()

print("--- pretty print all elements once again ---")
print_list(head)
print()
