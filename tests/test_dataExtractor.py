from unittest import TestCase

import spacy
import os

from model.data_extraction import DataExtractor
from model.tree import ContextTree

os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))


class TestDataExtractor(TestCase):
    def test_set_default_params(self):
        data_extractor = DataExtractor()
        self.assertEqual(spacy.load('en'), data_extractor.spacy, "spacy model wasn't loaded correctly")
        self.assertEqual("model/contexts.json", data_extractor.context_file, "context file name isn't correct")
        self.assertEqual({' stg ': ' £ '}, data_extractor.filter_dict, "filter dictionary isn't correct")

    def test_set_bank_rate_context_tree(self):
        head_dict = {
            "label": "head",
            "validator": {
                "lemma": [
                    "be",
                ],
                "pos": [
                    "verb"
                ],
            }
        }
        subj_dict = {
            "label": "I",
            "validator": {
                "lemma": [
                    "i",
                ]
            }
        }
        obj_dict = {
            "label": "object",
            "validator": {
                "lemma": [
                    "name"
                ],
                "pos": [
                    "noun"
                ],
                "good_subtree_tokens": [
                    "david",
                    "jose",
                    "jaime"
                ]
            }
        }

        head = ContextTree.from_dict(head_dict)
        subj = ContextTree.from_dict(subj_dict)
        obj = ContextTree.from_dict(obj_dict)
        head.set_children([subj, obj])

        data_extractor_first = DataExtractor()
        data_extractor_second = DataExtractor()

        data_extractor_first.bank_rate_context_trees = []
        data_extractor_second.bank_rate_context_trees = []

        data_extractor_first.bank_rate_context_trees = [head]
        data_extractor_second.set_bank_rate_context_tree(head)

        self.assertEqual(data_extractor_first.bank_rate_context_trees, data_extractor_second.bank_rate_context_trees,
                         "insertion of one context tree isn't correct")

        data_extractor_first = DataExtractor()
        data_extractor_second = DataExtractor()

        data_extractor_first.bank_rate_context_trees = []
        data_extractor_second.bank_rate_context_trees = []

        data_extractor_first.bank_rate_context_trees = [head, head, head]
        data_extractor_second.set_bank_rate_context_tree([head, head, head])

        self.assertEqual(data_extractor_first.bank_rate_context_trees, data_extractor_second.bank_rate_context_trees,
                         "insertion of context trees isn't correct")

    def test_set_qe_context_tree(self):
        head_dict = {
            "label": "head",
            "validator": {
                "lemma": [
                    "be",
                ],
                "pos": [
                    "verb"
                ],
            }
        }
        subj_dict = {
            "label": "I",
            "validator": {
                "lemma": [
                    "i",
                ]
            }
        }
        obj_dict = {
            "label": "object",
            "validator": {
                "lemma": [
                    "name"
                ],
                "pos": [
                    "noun"
                ],
                "good_subtree_tokens": [
                    "david",
                    "jose",
                    "jaime"
                ]
            }
        }

        head = ContextTree.from_dict(head_dict)
        subj = ContextTree.from_dict(subj_dict)
        obj = ContextTree.from_dict(obj_dict)
        head.set_children([subj, obj])

        data_extractor_first = DataExtractor()
        data_extractor_second = DataExtractor()

        data_extractor_first.qe_context_trees = []
        data_extractor_second.qe_context_trees = []

        data_extractor_first.qe_context_trees = [head]
        data_extractor_second.set_qe_context_tree(head)

        self.assertEqual(data_extractor_first.qe_context_trees, data_extractor_second.qe_context_trees,
                         "insertion of one context tree isn't correct")

        data_extractor_first = DataExtractor()
        data_extractor_second = DataExtractor()

        data_extractor_first.qe_context_trees = []
        data_extractor_second.qe_context_trees = []

        data_extractor_first.qe_context_trees = [head, head, head]
        data_extractor_second.set_qe_context_tree([head, head, head])

        self.assertEqual(data_extractor_first.qe_context_trees, data_extractor_second.qe_context_trees,
                         "insertion of context trees isn't correct")

    def test_analyse(self):
        pass

    def test_search(self):
        pass

    def test_filter(self):
        sample_text = 'QUICK BROWN FOX   JUMPS  OVER THE  LAZY DOG'
        correct_text = 'Quick brown fox jumps over the lazy dog'
        data_extractor = DataExtractor()

        self.assertEqual(correct_text, data_extractor.filter(sample_text), "sample text wasn't filtered correctly")

    def test_context_search(self):
        pass

    def test_build_context_trees(self):
        data = {"case_1": [
            {
                "label": "head",
                "validator": {
                    "lemma": [
                        "be",
                    ],
                    "pos": [
                        "verb"
                    ],
                },
                "children": ["I", "object"],
                "parent": ""
            },
            {
                "label": "I",
                "validator": {
                    "lemma": [
                        "i",
                    ]
                },
                "children": [],
                "parent": "head"
            },
            {
                "label": "object",
                "validator": {
                    "lemma": [
                        "name"
                    ],
                    "pos": [
                        "noun"
                    ],
                    "good_subtree_tokens": [
                        "david",
                        "jose",
                        "jaime"
                    ],
                },
                "children": [],
                "parent": "head"
            }
        ]
        }
        head_dict = {
            "label": "head",
            "validator": {
                "lemma": [
                    "be",
                ],
                "pos": [
                    "verb"
                ],
            }
        }
        subj_dict = {
            "label": "I",
            "validator": {
                "lemma": [
                    "i",
                ]
            }
        }
        obj_dict = {
            "label": "object",
            "validator": {
                "lemma": [
                    "name"
                ],
                "pos": [
                    "noun"
                ],
                "good_subtree_tokens": [
                    "david",
                    "jose",
                    "jaime"
                ]
            }
        }

        head = ContextTree.from_dict(head_dict)
        subj = ContextTree.from_dict(subj_dict)
        obj = ContextTree.from_dict(obj_dict)

        head.set_children([subj, obj])

        data_extractor = DataExtractor()
        result = data_extractor.build_context_trees(data)

        self.assertEqual([head], data_extractor.build_context_trees(data), "context trees aren't built correctly")

    def test_from_json(self):
        pass


if __name__ == '__main__':
    tester = TestDataExtractor()
    tester.test_build_context_trees()
    TestDataExtractor.test_build_context_trees()
