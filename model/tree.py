import copy

from nltk.tree import ParentedTree

from model.helpers import found


class ParentedTreeWrapper(ParentedTree):
    def __init__(self, token, children=None):
        super(ParentedTreeWrapper, self).__init__(token.orth_, children)
        self.text = token.orth_
        self.lemma = token.lemma_
        self.pos = token.pos_
        self.dep = token.dep_
        self.tag = token.tag_
        self.children = children
        self.token = token

    @staticmethod
    def from_spacy_tree(root_token):
        """
        Build tree from spacy root token

        Args:
            root_token: (Token) root of Span of spacy Doc object

        Returns:
            result: (ParentedTreeWrapper) built tree object
        """
        if root_token.n_lefts + root_token.n_rights > 0:
            return ParentedTreeWrapper(root_token,
                                       [ParentedTreeWrapper.from_spacy_tree(child_token) for child_token in
                                        root_token.children])
        else:
            return ParentedTreeWrapper(root_token, [])

    def subtree_tokens(self):
        """
        Returns the list of all subtree texts.
        Useful for checking if something is contained in a subtree of given node.
        Returns:
            result:(list) node texts from subtree nodes
        """
        children_texts = []
        for child in self.children:
            children_texts.extend(child.subtree_tokens())
        return [self.text] + children_texts

    def is_ancestor(self, node):
        """
        Checks if given node is ancestor of current node

        Args:
            node: (ParentedTreeWrapper)

        Returns:
            result: (bool)
        """
        parent = self
        while parent is not None and parent != node:
            parent = parent.parent()

        if parent == node:
            answer = True
        else:
            answer = False

        return answer

    def leaves(self):
        """
        Traversal on tree nodes.
        Collects all leaf node texts.

        Returns:
            leaves: (list) containing texts of leaf nodes
        """
        leaves = []
        for child in self.children:
            if len(child.children) > 0:
                leaves.extend(child.leaves())
            else:
                leaves.append(child.text)
        return leaves

    def less(self, tree):
        """
        Compares current tree node to given one, to find out if current comes before the given one in sentence.
        Uses 'treeposition' function to get relevant information about node's relative positions in tree.

        Args:
            tree: (ParentedTreeWrapper) node for comparison

        Returns:
            result: (bool) current node comes before given one or not

        """
        result = True
        for a, b in zip(self.treeposition(), tree.treeposition()):
            if a is None:
                result = True
            elif b is None:
                result = False
            elif a > b:
                result = False
            elif a < b:
                result = True

        return result

    @staticmethod
    def lca(node_1, node_2):
        """
        Find lowest common ancestor for given nodes

        Args:
            node_1: (ParentedTreeWrapper) first node
            node_2: (ParentedTreeWrapper) second node

        Returns:
             result: (ParentedTreeWrapper) lowest common ancestor
        """
        result = None

        if node_1 == node_2 or node_2.parent() == node_1:
            result = node_1
        elif node_1.parent() == node_2:
            result = node_2

        if result is None:
            parent = node_2.parent()
            while parent is not None and not node_1.is_ancestor(parent):
                parent = parent.parent()

            if parent is not None and node_1.is_ancestor(parent):
                result = parent

        return result

    def traverse(self, mode='preorder'):
        """
        Tree traversal with two modes:'preorder' and 'postorder'

        Args:
            mode: (str) traversal mode

        Returns:
            result: (list) traversed nodes of full tree

        """
        result = []
        if mode == 'preorder':
            result.append(self)

        for child in self.children:
            result.extend(child.traverse())

        if mode == 'postorder':
            result.append(self)

        return result

    def valid(self, **kwargs):
        """
        validates parameters of tree:
        pos, dep, lemma, tag, text,...,

        Args:
            **kwargs: (dict)parameters with names [pos, dep, lemma, text,....,]

        Returns:
            result: (bool) current tree node is "valid" or not

        Examples:
            self.valid(pos=['NNP','ADP'], dep=['conj'])
        """
        is_valid = True
        if self.pos.lower() not in kwargs.get('pos', [self.pos.lower()]):
            is_valid = False
        elif self.dep.lower() not in kwargs.get('dep', [self.dep.lower()]):
            is_valid = False
        elif self.lemma.lower() not in kwargs.get('lemma', [self.lemma.lower()]):
            is_valid = False
        elif self.text.lower() not in kwargs.get('text', [self.text.lower()]):
            is_valid = False

        if is_valid:
            subtree_tokens = [x.lower() for x in self.subtree_tokens()]
            good_tokens = kwargs.get("good_subtree_tokens", None)
            bad_tokens = kwargs.get("bad_subtree_tokens", None)

            if good_tokens is not None and not found(subtree_tokens, good_tokens, 'all'):
                is_valid = False
            elif bad_tokens is not None and found(subtree_tokens, bad_tokens, 'any'):
                is_valid = False

        return is_valid

    def find_with_properties(self, **kwargs):
        """
        Traverses all tree nodes and returns list of nodes which is "valid"

        Args:
            **kwargs: (dict) parameters with names [pos, dep, lemma, text,....,] to match dependency tree nodes

        Returns:
            result: (list) containing ParentedTreeWrapper "valid" nodes
        """
        result = []
        for subtree in self.traverse():
            if subtree.valid(**kwargs):
                result.append(subtree)

        return result

    def deepcopy(self):
        """
        Create deepcopy Create deepcopy of current object

        Returns:
            new_object: (ParentedTreeWrapper)
        """
        new_object = copy.deepcopy(self)
        return new_object

    def _get_node(self):
        pass

    def _set_node(self, value):
        pass


class ContextTree:
    def __init__(self):
        self.label = None
        self.parent = None
        self.children = []
        self.validated = False
        self.validator = None
        self.good_subtree_tokens = []
        self.bad_subtree_tokens = []
        self.extract = False
        self.found_value = None
        self.candidates = []

    def set_children(self, children):
        """
        Set children nodes to current node and assign current node as parent to each children node.

        Args:
            children: (list) ContextTree objects

        """
        if isinstance(children, ContextTree):
            children = [children]

        if isinstance(children, list) and len(children) > 0:
            for child in children:
                if isinstance(child, ContextTree):
                    child.parent = self
                    self.children.append(child)

    def traverse(self, mode='preorder'):
        """
        Tree traversal with two modes:'preorder' and 'postorder'

        Args:
            mode: (str) traversal mode

        Returns:
            result: (list) traversed nodes of full tree

        """
        result = []
        if mode == 'preorder':
            result.append(self)

        for child in self.children:
            result.extend(child.traverse())

        if mode == 'postorder':
            result.append(self)

        return result

    def traverse_and_get(self, param_name):
        """
        Tree traversal to collect concrete parameters of tree nodes

        Args:
            param_name: (str) name of the parameter to collect from current tree nodes

        Returns:
            result: (list) traversed nodes parameters if exist

        """
        result = []
        for subtree in self.traverse():
            if hasattr(subtree, param_name):
                result.append(getattr(subtree, param_name))
        return result

    def traverse_and_extract(self):
        """
        Tree traversal to collect the found_values of tree nodes which contain needed results for context search.
        Such tree nodes have parameter "extract" set to True which means that we need to extract them.

        Returns:
            result: (list) required found_values contained in context tree nodes

        """
        result = []
        for subtree in self.traverse():
            if subtree.extract:
                result.append(subtree.found_value)
        return result

    def is_ancestor(self, node):
        """
        Checks if given node is ancestor of current node

        Args:
            node: (ContextTree)

        Returns:
            result: (bool)
        """
        parent = self
        while parent is not None and parent != node:
            parent = parent.parent()

        if parent == node:
            answer = True
        else:
            answer = False

        return answer

    @staticmethod
    def lca(node_1, node_2):
        """
        Find lowest common ancestor for given nodes

        Args:
            node_1: (ContextTree) first node
            node_2: (ContextTree) second node

        Returns:
             result: (ContextTree) lowest common ancestor
        """
        result = None

        if node_1 == node_2 or node_2.parent() == node_1:
            result = node_1
        elif node_1.parent() == node_2:
            result = node_2

        if result is None:
            parent = node_2.parent()
            while parent is not None and not node_1.is_ancestor(parent):
                parent = parent.parent()

            if parent is not None and node_1.is_ancestor(parent):
                result = parent

        return result

    def __str__(self):
        """
        String representation for easy printing
        Returns:
            result: (str) string of dictionary ContextTree parameters
        """
        result = {'label': self.label,
                  'parent': 'ROOT' if self.parent is None else self.parent.label,
                  'children': [child.label for child in self.children],
                  'validated': self.validated,
                  'validator': self.validator,
                  'good_subtree_tokens': self.good_subtree_tokens,
                  'bad_subtree_tokens': self.bad_subtree_tokens,
                  'self.extract': self.extract,
                  'found_value': self.found_value,
                  'candidates': self.candidates,
                  }
        return str(result)

    @staticmethod
    def from_dict(data):
        """
        Build and return context tree object from given dictionary.

        Args:
            data: (dict) containing parameter names and their values to assign to built ContextTree object

        Returns:
            context_tree: (ContextTree) tree built from given dictionary
        """
        assert isinstance(data, dict), f'function needs argument of type dict (dictionary)!'

        context_tree = ContextTree()
        context_tree.label = data.get("label")
        context_tree.validator = data.get("validator")
        context_tree.children = data.get("children", [])
        context_tree.parent = data.get("parent", None)
        context_tree.extract = data.get('extract', False)
        context_tree.bad_subtree_tokens = data.get("bad_subtree_tokens", [])
        context_tree.good_subtree_tokens = data.get("good_subtree_tokens", [])

        return context_tree

    def deepcopy(self):
        """
        Create deepcopy of current object
        Returns:
            new_object: (ContextTree)
        """
        new_object = copy.deepcopy(self)
        return new_object
