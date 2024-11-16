from enum import Enum

class Operation(Enum):
    ADD = 1
    SUB = 2
    SET = 3
    MOD = 4

class Comparator(Enum):
    LESS = 1
    MORE = 2
    EQ   = 3
    LTE  = 4
    MTE  = 5

class Element:
    pass

class Dialogue(Element):
    speaker: str
    text: str
    
    def __init__(self, _speaker, _text):
        self.speaker  = _speaker
        self.text = _text
    def __repr__(self):
        return 'Dialogue(%s, %s)' % (self.speaker, self.text)
    

class Modify(Element):
    operation: Operation
    variable: str
    amount: int
    
    def __init__(self, _operation, _variable, _amount):
        self.operation = _operation
        self.variable  = _variable
        self.amount    = _amount
    def __repr__(self):
        return 'Modify(%s, %s, %s)' % (self.operation.name, self.variable, self.amount)


class Conditional(Element):
    compare: Comparator
    var1: str
    var2: str
    ifElements: list[Element]
    elseElements: list[Element]
    
    def __init__(self, _compare, _var1, _var2):
        self.compare = _compare
        self.var1    = _var1
        self.var2    = _var2
        self.ifElements = []
        self.elseElements = []
    def __repr__(self):
        return 'Conditional(%s, %s, %s, %s, %s)' % (self.compare.name, self.var1, self.var2, self.ifElements, self.elseElements)

class Branch(Element):
    scene: str
    
    def __init__(self, _scene):
        self.scene = _scene
    def __repr__(self):
        return 'Branch(%s)' % self.scene

class ChoiceOption:
    text: str
    consequences: list[Element]
    def __init__(self, _text):
        self.text = _text
        self.consequences = []
    def __repr__(self):
        return 'ChoiceOptions(%s, %s)' % (self.text, self.consequences)
    def add_consequence(self, _element):
        self.consequences.append(_element)

class Choice(Element):
    options: list[ChoiceOption]
    def __init__(self):
        self.options = []
    def __repr__(self):
        return 'Choice(%s)' % self.options


class Asset(Element):
    type: str
    fileName: str
    options: list[str] # This currently allows for a single option but could be turned into a list later if more are needed
    def __init__(self, _type, _fileName, _options=""):
        self.type = _type
        self.fileName = _fileName
        self.options = _options
    def __repr__(self):
        return 'Asset(%s, %s)' % (self.type, self.fileName)
    
class Scene:
    title : str
    lines : list[Element]
    links : list[str]
    def __init__(self):
        self.lines = []
        self.links = []
    def add_line(self, element:Element):
        self.lines.append(element)
        

