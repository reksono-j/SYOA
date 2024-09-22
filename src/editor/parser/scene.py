from enum import Enum

class Operation(Enum):
    ADD = 1
    SUB = 2
    SET = 3
    MOD = 4

class Compare(Enum):
    LESS = 1
    MORE = 2
    EQ   = 3
    LTE  = 4
    MTE  = 5

class Element:
    pass

class Dialogue(Element):
    speaker: str
    dialogue: str

class Modify(Element):
    operation: Operation
    variable: str
    amount: int

class Conditional(Element):
    compare: Compare
    var1: str
    var2: str

class Branch(Element):
    target: str

class Choice(Element):
    options: list[Element]
    
class Scene:
    lines : list[Element]
    temp_text : str 