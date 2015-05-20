# -*- coding: utf-8 -*-

import os
import sys
import pytest

from lxml import etree
import nltk

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collation import Collation
from tokenizer import Tokenizer

class TestCollation:

    @pytest.fixture()
    def diff_tree(self, request):

        file_paths = map(lambda path: os.path.join(os.path.dirname(os.path.abspath(__file__)), path), ['fixtures/test_tei_a.xml', 'fixtures/test_tei_b.xml'])
        
        # tei_stanzas = map(Tokenizer.parse_stanza, file_paths)
        tei_stanzas = map(Tokenizer.parse_text, file_paths)

        # Work-around
        tei_stanza_u, tei_stanza_v = tei_stanzas[0:2]

        diff_tree = Tokenizer.diff(tei_stanza_u, 'u', tei_stanza_v, 'v')

        return diff_tree

    @pytest.fixture()
    def diff_tree_tags(self, request):

        file_paths = map(lambda path: os.path.join(os.path.dirname(os.path.abspath(__file__)), path), ['fixtures/test_tei_a.xml', 'fixtures/test_tei_c.xml'])
        
        tei_stanzas = map(Tokenizer.parse_stanza, file_paths)

        # Work-around
        tei_stanza_u, tei_stanza_v = tei_stanzas[0:2]

        diff_tree = Tokenizer.diff(tei_stanza_u, 'u', tei_stanza_v, 'v')

        return diff_tree

    @pytest.fixture()
    def stemma(self, request):

        file_paths = map(lambda path: os.path.join(os.path.dirname(os.path.abspath(__file__)), path), ['fixtures/test_tei_a.xml', 'fixtures/test_tei_b.xml', 'fixtures/test_tei_c.xml'])

        # tei_stanzas = map(Tokenizer.parse_stanza, file_paths)
        tei_stanzas = map(Tokenizer.parse_text, file_paths)

        base_text = tei_stanzas.pop()

        witnesses = [ { 'node': tei_stanzas[0], 'id': 'v' }, { 'node': tei_stanzas[1], 'id': 'w' } ]

        diff_tree = Tokenizer.stemma({ 'node': base_text, 'id': 'u' }, witnesses)

        return diff_tree

    @pytest.fixture()
    def stemma_alignment(self, request):

        file_paths = map(lambda path: os.path.join(os.path.dirname(os.path.abspath(__file__)), path), ['fixtures/test_tei_d.xml', 'fixtures/test_tei_e.xml', 'fixtures/test_tei_f.xml'])

        # tei_stanzas = map(Tokenizer.parse_stanza, file_paths)
        tei_stanzas = map(Tokenizer.parse_text, file_paths)

        base_text = tei_stanzas.pop()

        witnesses = [ { 'node': tei_stanzas[0], 'id': 'v' }, { 'node': tei_stanzas[1], 'id': 'w' } ]

        diff_tree = Tokenizer.stemma({ 'node': base_text, 'id': 'u' }, witnesses)

        return diff_tree

    @pytest.fixture()
    def stemma_alignment_b(self, request):

        file_paths = map(lambda path: os.path.join(os.path.dirname(os.path.abspath(__file__)), path), ['fixtures/test_swift_36629.xml', 'fixtures/test_swift_36711.tei.xml'])

        # tei_stanzas = map(Tokenizer.parse_stanza, file_paths)
        tei_stanzas = map(Tokenizer.parse_text, file_paths)

        base_text = tei_stanzas.pop()

        witnesses = [ { 'node': tei_stanzas[0], 'id': 'v' } ]

        diff_tree = Tokenizer.stemma({ 'node': base_text, 'id': 'u' }, witnesses)

        return diff_tree

    def test_init(self, diff_tree):

        collation = Collation(diff_tree)

    def test_values_stemma(self, stemma):

        collation = Collation(stemma)
        collation_values = collation.values()

        lines = collation_values['lines']

        line_1 = lines[1]

        # print line_1['ngram']
        # print line_1['line']
        # assert False

    def test_stemma_alignment(self, stemma_alignment, stemma_alignment_b):

        collation = Collation(stemma_alignment)
        collation_values = collation.values()

        lines = collation_values['lines']

        # One extraneous token
        line_1 = lines[1]
        assert line_1['ngram']['u'] == ['Piping', 'down', 'the', 'valleys', 'wild,']

        # Two additional tokens
        line_3 = lines[3]
        assert line_3['ngram']['u'] == ['On', 'a', 'cloud', 'I', 'saw', 'a', 'child,']
        # assert line_3['line'][2]['text'] == 'On Lorem a cloud I saw a amet child, '

        # One token at a distance of 2 steps
        line_4 = lines[4]
        assert line_4['ngram']['u'] == ['And', 'he', 'laughing', 'said', 'to', 'me:']

        #
        #

        collation_b = Collation(stemma_alignment_b)
        collation_values_b = collation_b.values()

        lines_b = collation_values_b['lines']

    def test_values(self, diff_tree, diff_tree_tags):

        collation = Collation(diff_tree)
        collation_values = collation.values()

        row_a = collation_values['lines'][5]
        base_text_a = row_a['line'][0]

        assert base_text_a['number'] == 5

#        row_a = collation_values['lines'][1]
#        base_text_a = row_a['line'][0]
#
#        assert base_text_a['number'] == 1
#        assert base_text_a['text'] == 'Piping down the valleys wild, '
#        assert base_text_a['distance'] == 0
#
#        row_b = collation_values['lines'][2]
#        base_text_b = row_b['line'][-1]
#
#        assert base_text_b['text'] == 'PIPING SONGS OF PLEASANT GLEE, '
#        assert base_text_b['distance'] == 24
#
#        # Testing for collations involving TEI tags
#        collation = Collation(diff_tree_tags)
#        collation_values = collation.values()
#
#        row_a = collation_values['lines'][1]
#        base_text_a = row_a['line'][0]
#
#        assert base_text_a['number'] == 1
#        assert base_text_a['text'] == 'Piping down the valleys wild, '
#        assert base_text_a['distance'] == 0
#
#        row_b = collation_values['lines'][2]
#        base_text_b = row_b['line'][-1]
#
#        assert base_text_b['text'] == u'Piping «gap» songs of pleasant glee, '
#        assert base_text_b['distance'] == 6
#
#        # Analyze the line ngram tokens
#        row_b_ngrams = row_b['ngram']
#
#        assert row_b_ngrams['base'] == ['Piping', '', '', '', '', '']
#        assert row_b_ngrams['v'] == ['', u'«gap»', 'songs', 'of', 'pleasant', 'glee']
#        assert row_b_ngrams['u'] == ['', 'songs', 'of', 'pleasant', 'glee', ',']

    def test_str(self, diff_tree):

        collation = Collation(diff_tree)
#        assert unicode(collation) == u"""{"1": [{"text": "Piping down the valleys wild, ", "number": 1, "witness": "u", "distance": 0}, {"text": "piping down the valleys wild, ", "number": 1, "witness": "v", "distance": 1}], "2": [{"text": "Piping songs of pleasant glee, ", "number": 2, "witness": "u", "distance": 0}, {"text": "PIPING SONGS OF PLEASANT GLEE, ", "number": 2, "witness": "v", "distance": 24}], "3": [{"text": "On a cloud I saw a child, ", "number": 3, "witness": "u", "distance": 0}, {"text": "On cloud I saw child ", "number": 3, "witness": "v", "distance": 5}], "4": [{"text": "And he laughing said to me: ", "number": 4, "witness": "u", "distance": 0}, {"text": "he laughing said me: ", "number": 4, "witness": "v", "distance": 7}]}"""
#        assert str(collation) == """{"1": [{"text": "Piping down the valleys wild, ", "number": 1, "witness": "u", "distance": 0}, {"text": "piping down the valleys wild, ", "number": 1, "witness": "v", "distance": 1}], "2": [{"text": "Piping songs of pleasant glee, ", "number": 2, "witness": "u", "distance": 0}, {"text": "PIPING SONGS OF PLEASANT GLEE, ", "number": 2, "witness": "v", "distance": 24}], "3": [{"text": "On a cloud I saw a child, ", "number": 3, "witness": "u", "distance": 0}, {"text": "On cloud I saw child ", "number": 3, "witness": "v", "distance": 5}], "4": [{"text": "And he laughing said to me: ", "number": 4, "witness": "u", "distance": 0}, {"text": "he laughing said me: ", "number": 4, "witness": "v", "distance": 7}]}"""

    def test_table(self, diff_tree):

        collation = Collation(diff_tree)
        collation_table = collation.table()

        

        pass
