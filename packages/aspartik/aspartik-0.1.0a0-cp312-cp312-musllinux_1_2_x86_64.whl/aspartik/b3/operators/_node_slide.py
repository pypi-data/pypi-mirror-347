from ._util import scale_on_range
from .. import State, Proposal, Tree


class NodeSlide:
    """Operator which slides a random node between its parent and children.

    This operator is similar to BEAST2's `EpochFlexOperator`: it will only
    affect the age of the selected node without altering the tree topology (a
    node cannot slide past its parent).
    """

    def __init__(
        self,
        tree: Tree,
        distribution,
        weight: float = 1,
    ):
        """
        Args:
            tree: The tree to edit.
            distribution:
                The distribution which will sample the new node height on the
                interval between its parent and the closest child.
        """
        self.tree = tree
        self.distribution = distribution
        self.weight = weight

    def propose(self, state: State) -> Proposal:
        """
        If there are no non-root internal nodes, the operator will bail with
        `Proposal.Reject`.
        """

        tree = self.tree
        rng = state.rng

        # automatically fail on trees without non-root internal nodes
        if tree.num_internals == 1:
            return Proposal.Reject()

        # Pick a non-root internal node
        node = tree.random_internal(rng)
        parent = tree.parent_of(node)
        while parent is None:
            node = tree.random_internal(rng)
            parent = tree.parent_of(node)

        left, right = tree.children_of(node)

        oldest = tree.weight_of(parent)
        youngest = max(tree.weight_of(left), tree.weight_of(right))

        (new_weight, ratio) = scale_on_range(youngest, oldest, self.distribution, rng)

        tree.update_weight(node, new_weight)

        return Proposal.Hastings(ratio)
