from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker
from besser.utilities.buml_code_builder import domain_model_to_code 
from besser.BUML.metamodel.object import ObjectModel
from besser.BUML.metamodel.domain import DomainModel
from .govdslLexer import govdslLexer
from .govdslParser import govdslParser
from .govdsl_buml_listener import BUMLGenerationListener


def object_model_to_code(object_model: ObjectModel, domain_model: DomainModel, file_path: str):
    """
    Generates Python code for a B-UML object model and writes it to a specified file.

    Parameters:
    model (ObjectModel): The B-UML object model containing instances and links, conformed to a DomainModel.
    file_path (str): The path where the generated code will be saved.

    Outputs:
    - A Python file containing the base code representation of the B-UML object domain model.
    """

def govdsl_to_buml(govdsl_path:str, buml_file_path:str = None):
    """Transforms a governance DSL instance into a B-UML model.

    Args:
        govdsl_path (str): The path to the file containing the governance DSL instance.
        buml_file_path (str, optional): the path of the file produced with the base 
                code to build the B-UML model (None as default).

    Returns:
        BUML_object_model (ObjectModel): the B-UML object model object.
    """
    lexer = govdslLexer(FileStream(govdsl_path))
    parser = govdslParser(CommonTokenStream(lexer))

    text_file = ""
    with open("example.txt", "r") as file:
        text_file = file.read()
        print(text_file)
    parser = self.setup(text_file)
    parse_tree = parser.project()
    listen = BUMLGenerationListener()
    walker = ParseTreeWalker()
    walker.walk(listen, parse_tree)
    object_model: ObjectModel = listen.get_buml_object_model()
    print(object_model)
    # if buml_file_path is not None:
    #     object_model_to_code(object_model=object_model, file_path=buml_file_path)
    return object_model