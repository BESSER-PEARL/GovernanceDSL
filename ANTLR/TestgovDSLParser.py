from antlr4 import *
from govdslLexer import govdslLexer
from govdslParser import govdslParser
# from govdslListener import govdslListener
from govErrorListener import govErrorListener
from besser.BUML.metamodel.object import ObjectModel
from govdsl_buml_listener import BUMLGenerationListener
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

        listen = BUMLGenerationListener()
        walker = ParseTreeWalker()
        walker.walk(listen, tree)
        object_model: ObjectModel = listen.get_buml_object_model()
        print("Object model: ")
        for i in object_model.instances:
            print("Instance: {}".format(i.name))
            print("Slots: ")
            for s in i.slots:
                print(" Attributes: {}".format(s.attribute))
                print(" Classifier: {}".format(s.value.classifier))
                print(" Value: {}\n".format(s.value.value))
            print("\n")
        for l in object_model.links:
            print("Link: {}".format(l.name))
        print("\n")
        # print(object_model.instances)  
        # print(object_model.links)           
    
        # dsl = govdslListener() # self.output
        # walker = ParseTreeWalker()
        # walker.walk(dsl, tree)              

        # let's check that there aren't any symbols in errorListener   
        try:      
            self.assertEqual(len(self.errorListener.symbol), 0)
        except AssertionError:
            print(f"Error: {self.errorListener.error_message}, symbol: {self.errorListener.symbol}")

if __name__ == '__main__':
    unittest.main()