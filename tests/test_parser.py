import unittest
from antlr4 import *
from ..grammar.govdslLexer import govdslLexer
from ..grammar.govdslParser import govdslParser
from ..grammar.govErrorListener import govErrorListener

class TestParser(unittest.TestCase):
    def setUp(self):
        self.test_cases_path = "tests/test_cases"
    
    def test_valid_syntax(self):
        with open(f"{self.test_cases_path}/valid_examples/simple_project.txt", "r") as file:
            text = file.read()
            lexer = govdslLexer(InputStream(text))
            stream = CommonTokenStream(lexer)
            parser = govdslParser(stream)
            tree = parser.project()
            self.assertIsNotNone(tree)