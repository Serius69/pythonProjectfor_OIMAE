import graphviz


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.solved_value = None
        self.is_in_path = False


def create_tree():
    return Node('l',
                Node('x',
                     Node((2, 0, 1)),
                     Node((1, 5, 6))),
                Node('R',
                     Node('y',
                          Node((2, 1, 2)),
                          Node((5, 4, 4))),
                     Node('p',
                          Node((0, 1, 7)),
                          Node((2, 2, 0)))))


def solve_tree_bottom_up(root):
    def post_order_traversal(node):
        if node is None:
            return 0, False

        left_value, left_in_path = post_order_traversal(node.left)
        right_value, right_in_path = post_order_traversal(node.right)

        if isinstance(node.value, tuple):
            node.solved_value = node.value[0] + node.value[1] - node.value[2]
            node.is_in_path = True
            return node.solved_value, True

        if node.value == 'x':
            node.solved_value = left_value * right_value
        elif node.value == 'y':
            node.solved_value = left_value ** right_value
        elif node.value in ['l', 'R', 'p']:
            node.solved_value = max(left_value, right_value)
            if left_value > right_value:
                node.left.is_in_path = True
            else:
                node.right.is_in_path = True

        node.is_in_path = left_in_path or right_in_path
        return node.solved_value, node.is_in_path

    final_value, _ = post_order_traversal(root)
    return final_value


def visualize_tree(root):
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB', size='8,8')

    def add_nodes_edges(node, parent=None):
        if node:
            node_id = str(id(node))
            label = f"{node.value}\n{node.solved_value}"

            if node.is_in_path:
                dot.node(node_id, label, style='filled', color='lightblue')
            else:
                dot.node(node_id, label)

            if parent:
                dot.edge(str(id(parent)), node_id)

            add_nodes_edges(node.left, node)
            add_nodes_edges(node.right, node)

    add_nodes_edges(root)
    dot.render('binary_tree', format='png', cleanup=True)
    print("Tree visualization saved as 'binary_tree.png'")


# Create and solve the tree
root = create_tree()
result = solve_tree_bottom_up(root)

print(f"The solution to the tree is: {result}")

# Visualize the tree
visualize_tree(root)


def get_path_description(node):
    if node is None:
        return []

    if isinstance(node.value, tuple):
        return [f"{node.value} = {node.solved_value}"]

    left_path = get_path_description(node.left)
    right_path = get_path_description(node.right)

    if node.left and node.left.is_in_path:
        return [f"{node.value}: {node.solved_value}"] + left_path
    elif node.right and node.right.is_in_path:
        return [f"{node.value}: {node.solved_value}"] + right_path
    else:
        return []


print("\nSolution path description:")
path_description = get_path_description(root)
for step in path_description:
    print(step)