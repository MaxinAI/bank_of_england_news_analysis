import json
import warnings
import os
import spacy
from model.tree import ContextTree, ParentedTreeWrapper

warnings.filterwarnings('ignore')


class DataExtractor(object):
    """
    Class that takes bank news texts, extracts bank rate percentage and quantitative easing number using context
    analysis.
    """

    def __init__(self, spacy_model=None, context_file=None):
        self.spacy = spacy_model
        self.bank_rate_context_trees = []
        self.qe_context_trees = []
        self.context_file = context_file
        self.filter_dict = None
        self.set_default_params()
        self.from_json(self.context_file)

    def set_default_params(self):
        """Set Default parameters"""
        if self.spacy is None:
            self.spacy = spacy.load('en')
        if self.context_file is None:
            self.context_file = "model/contexts.json"
        if self.filter_dict is None:
            self.filter_dict = {' stg ': ' £ '}

    def set_bank_rate_context_tree(self, context_tree):
        """
        Set bank context tree

        Args:
            context_tree: (list or ContextTree) context tree object(s)

        """
        if isinstance(context_tree, list):
            self.bank_rate_context_trees.extend(context_tree)
        elif isinstance(context_tree, ContextTree):
            self.bank_rate_context_trees.append(context_tree)

    def set_qe_context_tree(self, context_tree):
        if isinstance(context_tree, list):
            self.qe_context_trees.extend(context_tree)
        elif isinstance(context_tree, ContextTree):
            self.qe_context_trees.append(context_tree)

    def analyse(self, text):
        """
        Takes bank news string, finds bank rate percentage and quantitative easing number.
        Uses dependency tree for analysing contexts.

        Args:
            text: (str) bank news

        Returns:
            results: (dict) contains original string, bank rate percentage number
            and quantitative easing number.

        """
        if text is None or (not isinstance(text, str) and not isinstance(text, list)):
            result = {'news': '', 'Bank_Rate': '', 'QE': ''}
            return result

        if isinstance(text, str):
            texts = [text]
        else:
            texts = text

        all_results = []
        for news in texts:
            news = self.filter(news)
            bank_rate_result = self.search(news, self.bank_rate_context_trees)
            qe_result = self.search(news, self.qe_context_trees)

            if len(bank_rate_result) > 0:
                bank_rate = bank_rate_result[0]
            else:
                bank_rate = ""

            if len(qe_result) > 0:
                qe = qe_result[0]
            else:
                qe = ""

            result = {'news': news, 'Bank_Rate': bank_rate, 'QE': qe}

            all_results.append(result)

        return all_results

    def search(self, text, context_trees):
        """
        Takes text and context tree. Splits text into sentences, builds dependency trees and matches contexts.

        Args:
            text: (str) containing bank news statement
            context_trees: (list) containing ContextTree objects

        Returns:
            results: (list) found bank rate and qe numbers if available else empty list

        """
        doc = self.spacy(text)
        results = []
        for span in doc.sents:
            tree = ParentedTreeWrapper.from_spacy_tree(span.root)
            # tree.draw()
            for context_tree in [x.deepcopy() for x in context_trees]:
                context_result = self.context_search(tree, context_tree)
                # print(context_result)

                validated_nodes = context_result.traverse_and_get('validated')
                if sum(validated_nodes) == len(validated_nodes):
                    results.extend(context_result.traverse_and_extract())
                    break

        return results

    def filter(self, text):
        """
        Takes incoming text, removes unnecessary spaces, capitalises and replaces some keys with appropriate values.
        These key, value pairs are defined in this class.

        Args:
            text: (str) bank news statement

        Returns:
            filtered_text: (str) filtered bank news statement
        """
        filtered_text = ' '.join([x.strip() for x in text.split()]).capitalize()
        for key, replacement in self.filter_dict.items():
            filtered_text = filtered_text.replace(key, replacement)
        return filtered_text

    @staticmethod
    def context_search(tree, context_tree):
        """
        Given sentence dependency tree and context tree objects matches context and returns context tree itself
        which contains all information in its nodes.
        Then it's possible simply to traverse and collect matching information.

        Args:
            tree: (ParentedTreeWrapper) dependency tree of sentence
            context_tree: (ContextTree) context tree

        Returns:
            context_tree: (ContextTree) the same context tree object with results contained inside

        """
        curr_candidates = tree.find_with_properties(**context_tree.validator)
        if len(curr_candidates) > 0:
            context_tree.validated = True
            context_tree.found_value = curr_candidates[0].text
            context_tree.candidates.extend(curr_candidates)

            for node in context_tree.traverse()[1:]:
                for prev_candidate in node.parent.candidates:
                    curr_candidates = prev_candidate.find_with_properties(**node.validator)
                    if len(curr_candidates) > 0:
                        node.validated = True
                        node.found_value = curr_candidates[0].text
                        node.candidates.extend(curr_candidates)
                        break
                if not node.validated:
                    break

        return context_tree

    @staticmethod
    def build_context_trees(data):
        """
        Builds Context tree from dictionary containing context names as keys and values list of context nodes.
        Each of this nodes contain dictionary with keys as ContextTree object parameter names and values to assign.

        Args:
            data: (dict) dictionary for building ContextTree

        Returns:
            context_trees: (list) containing list of built ContextTree objects
        """
        context_trees = []
        for case in data.keys():
            case_tree_nodes = {}
            for context_dict in data[case]:
                tree_node = ContextTree.from_dict(context_dict)
                case_tree_nodes[tree_node.label] = tree_node

            tree_root = None
            for _, tree_node in case_tree_nodes.items():
                # set parent
                if tree_node.parent == "" and tree_root is None:
                    tree_root = tree_node

                if not isinstance(tree_node.parent, ContextTree):
                    found_node = case_tree_nodes.get(tree_node.parent, None)
                    assert found_node is not None or tree_node.parent == "", f'node with label {tree_node.parent} ' \
                                                                             f'not found to assign as a parent of ' \
                                                                             f'node with label {tree_node.label}!'
                    tree_node.parent = found_node

                # set children
                children_nodes = []
                for child_label in tree_node.children:
                    found_node = case_tree_nodes.get(child_label, None)
                    assert found_node is not None, f'node with label {child_label} ' \
                                                   f'not found to assign as a child of ' \
                                                   f'node with label {tree_node.label}!'
                    children_nodes.append(found_node)

                tree_node.children = children_nodes

            context_trees.append(tree_root)

        return context_trees

    def from_json(self, filename=None):
        """
        Reads dictionary from json file and build ContextTree objects.

        Args:
            filename: (str) file containing context dictionaries

        """
        if filename is None:
            filename = self.context_file

        assert os.path.exists(filename), f'{filename} not exists!'

        with open(filename, 'r') as file:
            data = json.load(file)

        bank_rate_contexts = data.get("Bank_Rate", None)
        qe_contexts = data.get("QE", None)

        bank_rate_context_trees = []
        qe_context_trees = []

        if bank_rate_contexts is not None:
            bank_rate_context_trees = self.build_context_trees(bank_rate_contexts)
        if qe_contexts is not None:
            qe_context_trees = self.build_context_trees(qe_contexts)

        self.set_bank_rate_context_tree(bank_rate_context_trees)
        self.set_qe_context_tree(qe_context_trees)
