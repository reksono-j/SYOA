from pyparsing import Combine, Word, Literal, Suppress, CharsNotIn, nested_expr, Regex, Optional, OneOrMore, one_of, alphanums, nums, printables


# Grammar 
# Dialogue - Speaker:Sentence or Sentence -> string:string or string
# Change - CHANGE Operation Variable Amount 
# Choice - CHOICE String \\\ Each line acts as a separate choice
# Conditional - IF Compare \n Elements \n IFEND ELSE \n Elements \n ELEND
# Branch - BRANCH SceneName -> BRANCH String
# Compare - string Condition string|int
# Condition - LESS | MORE | EQ | LTE | MTE
# Operation - ADD | SUB | SET | MOD
# 

ExampleScript = """IF var1 EQ 1
Test
Speaker 2: Wow
ELSE
Speaker 1: Right?
END"""

#Dialogue
"""Speaker1 : This is a test 
Speaker2: :No kid:ding? 
Speaker3 :Seriously? 
I'm writing a test"""

#Modify
"MOD set var1 1"

# Choice
"""CHOICE First option
MOD add var1 2
CHOICE END
CHOICE Second Option
This is another test line
END
CHOICE Second Option
This is another test line
OVER
"""
#Branch
"BRANCH Scene2"


def parse_text(text: str):
    # Working
    speaker = Regex('^([A-Za-z0-9]*?)(?=[ :])')
    dialogue = Optional(speaker('speaker') + Literal(':')) + Word(printables + ' ')('text')
    change    = Literal("CHANGE") + one_of("ADD SUB SET MOD", caseless = True)('Operation') + Word(alphanums)('Variable') + Word(nums)('Amount')
    branch   = Literal('BRANCH') + Word(alphanums)('scene')
    
    # WIP - CONDITIONAL
    condIf    = 'IF' + dialogue
    condElse  = 'ELSE' # TODO split into two lists if('if') and else('else') split by ELSE
    condEnd   = 'END'
    conditional = nested_expr(opener=condIf, closer=condEnd, content=Combine(OneOrMore(~Literal('IF') + ~Literal(condEnd) + Word(printables + ' '))))
    
    # WIP - CHOICE
    # choice    = Literal("CHOICE") + Word(printables + ' ')('text')
    # possibly choices start with a choice and some text then capture the elements that follow until another choice or some closing keyword is found 
    
    # WIP - COMPARE
    # condition = one_of("LESS MORE EQ LTE MTE", caseless = True)
    # compare   = Word(alphanums)('var1') + condition('condition') + Word(alphanums)('var2')
    
    example = conditional.parseString(ExampleScript)[0]
    print(example)
    return example

def read_script():
  test = ExampleScript
  
  parse_text(test)
      

if __name__ == "__main__":
  read_script()