import numpy as np
from graphviz import Digraph

from giraffe.globals import BACKEND as B
from giraffe.node import Node, OperatorNode, ValueNode
from giraffe.tree import Tree


def draw_tree(to_draw: Node | OperatorNode | Tree | ValueNode, dot=None, add_val_eval=True):
    """
    Create a visual representation of a tree structure using Graphviz.

    This function generates a directed graph visualization of a tree structure,
    showing nodes and their hierarchical relationships. For ValueNodes, it can
    optionally display the tensor values and evaluations if they're small enough.

    Args:
        to_draw: The object to visualize (can be a Tree, Node, OperatorNode, or ValueNode)
        dot: Optional existing Digraph object to add to. If None, a new one is created.
        add_val_eval: If True, include value and evaluation information for ValueNodes

    Returns:
        A Graphviz Digraph object representing the tree structure
    """
    node: None | Node | OperatorNode | ValueNode
    if isinstance(to_draw, Tree):
        node = to_draw.root
    else:
        node = to_draw

    if dot is None:
        dot = Digraph(comment="Tree")

    if isinstance(node, ValueNode):
        if node.value is not None:
            value = B.to_numpy(node.value) if (np.prod(node.value.shape) <= 9) else f"Tensor with memory adress: {hex(id(node.value))}"
        else:
            value = None

        if node.evaluation is not None:
            evaluation = (
                B.to_numpy(node.evaluation) if (np.prod(B.shape(node.evaluation)) <= 9) else f"Tensor with memory adress: {hex(id(node.evaluation))}"
            )
        else:
            evaluation = None

        display_string = "Value Node\n"

        if node.id is not None:
            display_string += f"Model ID: {node.id}\n"

        if add_val_eval:
            display_string += f"Value: {value} | Eval: {evaluation}"

        dot.node(
            f"{hex(id(node))}",
            display_string,
        )
    else:
        dot.node(f"{hex(id(node))}", f"Op\n{str(node)}")

    for child in node.children:
        draw_tree(child, dot, add_val_eval)
        dot.edge(f"{hex(id(node))}", f"{hex(id(child))}")

    return dot
