# -*- coding: utf-8 -*-

import os
import sys
import pytest

from lxml import etree
import nltk

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from SwiftDiff.text import Line
from SwiftDiff.tokenize import SwiftSentenceTokenizer
from SwiftDiff.collate.difference_line import DifferenceLine

class TestDifferenceLine:

    @pytest.fixture()
    def base_line(self):
        base_line = Line("Lorem ipsum dolor sit", 0, SwiftSentenceTokenizer)
        base_line.tokenize()
        return base_line

    @pytest.fixture()
    def variant_line_short(self):
        base_line = Line("Lorem ipsum dolor", 0, SwiftSentenceTokenizer)
        base_line.tokenize()
        return base_line

    @pytest.fixture()
    def variant_line_long(self):
        base_line = Line("Lorem ipsum dolor sit amet", 0, SwiftSentenceTokenizer)
        base_line.tokenize()
        return base_line

    def test_init(self, base_line, variant_line_short):
        diff_line = DifferenceLine(base_line, variant_line_short, SwiftSentenceTokenizer)

    def test_tokenize(self, base_line, variant_line_short, variant_line_long):
        diff_line = DifferenceLine(base_line, variant_line_short, SwiftSentenceTokenizer)

        diff_line.tokenize()

        assert diff_line.tokens[0].value == 'Lorem'
        assert diff_line.tokens[1].value == 'ipsum'
        assert diff_line.tokens[2].value == 'dolor'
        assert diff_line.tokens[3].value == 'sit'

        assert diff_line.base_line.tokens[0].value == 'Lorem'
        assert diff_line.base_line.tokens[1].value == 'ipsum'
        assert diff_line.base_line.tokens[2].value == 'dolor'
        assert diff_line.base_line.tokens[3].value == ''

        diff_line = DifferenceLine(base_line, variant_line_long, SwiftSentenceTokenizer)

        diff_line.tokenize()

        assert diff_line.tokens[0].value == 'Lorem'
        assert diff_line.tokens[1].value == 'ipsum'
        assert diff_line.tokens[2].value == 'dolor'
        assert diff_line.tokens[3].value == 'sit'
        assert diff_line.tokens[4].value == 'amet'

        assert diff_line.base_line.tokens[0].value == 'Lorem'
        assert diff_line.base_line.tokens[1].value == 'ipsum'
        assert diff_line.base_line.tokens[2].value == 'dolor'
        assert diff_line.base_line.tokens[3].value == 'sit'
        assert diff_line.base_line.tokens[4].value == ''

    def test_align(self, base_line, variant_line_short, variant_line_long):
        diff_line = DifferenceLine(base_line, variant_line_short, SwiftSentenceTokenizer)

        diff_line.tokenize()

        assert diff_line.tokens[0].value == 'Lorem'
        assert diff_line.tokens[1].value == 'ipsum'
        assert diff_line.tokens[2].value == 'dolor'
        assert diff_line.tokens[3].value == 'sit'

        assert diff_line.base_line.tokens[0].value == 'Lorem'
        assert diff_line.base_line.tokens[1].value == 'ipsum'
        assert diff_line.base_line.tokens[2].value == 'dolor'
        assert diff_line.base_line.tokens[3].value == ''

        diff_line.align()
        pass
