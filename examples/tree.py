from dataclasses import dataclass
from typing import Optional
from vibe import code


@dataclass
class TreeNode:
    data: int
    children: list["TreeNode"] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


@code
def insert_node(root: TreeNode, parent_data: int, new_data: int) -> bool:
    """
    Insert a new node with new_data as a child of the node with parent_data.

    Args:
        root: The root node of the tree.
        parent_data: The data of the parent node to which the new node will be attached.
        new_data: The data for the new node.

    Returns:
        bool: True if the insertion was successful, False otherwise.
    """
    pass


@code
def find_node(root: TreeNode, data: int) -> Optional[TreeNode]:
    """
    Find and return the node with the specified data.

    Args:
        root: The root node of the tree.
        data: The data to search for in the tree.

    Returns:
        Optional[TreeNode]: The node with the specified data, or None if not found.
    """
    pass


@code
def delete_node(root: TreeNode, data: int) -> bool:
    """
    Delete the node with the specified data from the tree.

    Args:
        root: The root node of the tree.
        data: The data of the node to be deleted.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    pass


@code
def traverse_preorder(root: TreeNode) -> list[int]:
    """
    Perform a pre-order traversal of the tree and return the data of the nodes.

    Args:
        root: The root node of the tree.

    Returns:
        list[int]: A list of node data in pre-order traversal order.
    """
    pass


@code
def traverse_postorder(root: TreeNode) -> list[int]:
    """
    Perform a post-order traversal of the tree and return the data of the nodes.

    Args:
        root: The root node of the tree.

    Returns:
        list[int]: A list of node data in post-order traversal order.
    """
    pass


@code
def height(root: TreeNode) -> int:
    """
    Calculate the height of the tree.

    Args:
        root: The root node of the tree.

    Returns:
        int: The height of the tree.
    """
    pass


# Usage example
root = TreeNode(1)
insert_node(root, 1, 2)
insert_node(root, 1, 3)
insert_node(root, 2, 4)
insert_node(root, 2, 5)
insert_node(root, 3, 6)

found_node = find_node(root, 4)
print(f"Found node: {found_node.data if found_node else 'Not found'}")

print("Pre-order traversal:", traverse_preorder(root))
print("Post-order traversal:", traverse_postorder(root))
print("Height of the tree:", height(root))

delete_node(root, 4)

found_node = find_node(root, 4)
print(f"Found node: {found_node.data if found_node else 'Not found'}")

print(
    "Node 4 was successfully deleted."
    if not find_node(root, 4)
    else "Node 4 was not deleted."
)
print("Updated pre-order traversal:", traverse_preorder(root))
