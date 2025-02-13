import sys
from antlr4 import *
from govdslParser import govdslParser
from govdslListener import govdslListener
from antlr4.error.ErrorListener import *
import io

class govErrorListener(ErrorListener):

    def __init__(self, output):
        self.output = output        
        self._symbol = ''
        self._error_message = ''
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):        
        error_message = f"line {line}:{column} {msg}"
        self.output.write(error_message)
        self._symbol = offendingSymbol.text
        self._error_message = error_message

    @property        
    def symbol(self):
        return self._symbol
    
    @property
    def error_message(self):
        return self._error_message