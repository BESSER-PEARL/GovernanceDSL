from antlr4 import *
from govdslLexer import govdslLexer
from govdslParser import govdslParser
# from govdslListener import govdslListener
from govErrorListener import govErrorListener
from governance import Project
from ProjectCreationListener import ProjectCreationListener
import unittest
import io

class TestgovDSLParser(unittest.TestCase):

    def setup(self, text):        
        lexer = govdslLexer(InputStream(text))        
        stream = CommonTokenStream(lexer)
        parser = govdslParser(stream)
        
        self.output = io.StringIO()
        self.error = io.StringIO()

        parser.removeErrorListeners()        
        errorListener = govErrorListener(self.error)
        parser.addErrorListener(errorListener)  

        self.errorListener = errorListener              
        
        return parser
        
    def test_dsl(self):
        text_file = ""
        with open("example.txt", "r") as file:
            text_file = file.read()
            print(text_file)
        parser = self.setup(text_file)
        tree = parser.project()  

        listen = ProjectCreationListener()
        walker = ParseTreeWalker()
        walker.walk(listen, tree)
        object_model: Project = listen.get_project()
        print("Object model: {}".format(object_model.name))
        print("Deadlines of project: {}".format(object_model.deadlines))

        # let's check that there aren't any symbols in errorListener   
        try:      
            self.assertEqual(len(self.errorListener.symbol), 0)
        except AssertionError:
            print(f"Error: {self.errorListener.error_message}, symbol: {self.errorListener.symbol}")

if __name__ == '__main__':
    unittest.main()