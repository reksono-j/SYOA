from pyparsing import Combine, Word, Literal, Suppress, CharsNotIn, nested_expr, Regex, Optional, OneOrMore, one_of, alphanums, nums, printables


# Grammar 
# Dialogue - Speaker:Sentence or Sentence -> string:string or string
# modify - MODIFY Operation Variable Amount 
# Choice - CHOICE String \\\ Each line acts as a separate choice
# Conditional - IF Compare \n Elements \n IFEND ELSE \n Elements \n ELEND
# Branch - BRANCH SceneName -> BRANCH String
# Compare - string Condition string|int
# Condition - LESS | MORE | EQ | LTE | MTE
# Operation - ADD | SUB | SET | MOD
# 

# CHARACTER 1 - {"C1", "C1A" as "Mysterious person"}

# Speaker1 : Hello world
# CHOICE Hi there
#  Speaker2: Hi there
# END
# Choice Pick up rock
# You picked up a rock
# modify rock add 1 
# END
# IF rock eq 1
# Speaker1 : That's a sweet rock
# Speaker2 : Isn't it?
# ELSE
# Speaker 1 looks at the ground, leans over, and picks up a rock.
# Speaker1 : Wow this is an awesome rock.
# Speaker2: Woah, you're right.
# END
# Branch Scene2

# The parsing process would first categorize each line as an elmeent
# Then it would process the blocked statements in conditionals and choices
# Dialogue {speaker:Speaker1 text:"Hello world"}
# ChoiceOption {option:'"Hi there"'}
# Dialogue {speaker:Speaker2 text:"Hi there"}
# End{}
# ChoiceOption {option:'Pick up rock'}
# Dialogue{text:"You picked up a rock"}
# Modify {variable:rock operation:ADD value:1}
# End{}
# IF {variable1:rock operation:eq 1}
# Dialogue {speaker:Speaker1 text:"That's a sweet rock"}
# Dialogue {speaker:Speaker2 text:"Isn't it?"}
# Else {}
# Dialogue {text:"Speaker 1 looks at the ground, leans over, and picks up a rock."}
# Dialogue {speaker:Speaker1 text:"Wow this is an awesome rock."}
# Dialogue {speaker:Speaker2 text:"Woah, you're right."}
# End{}
# Branch {target:Scene2}

# Dialogue {speaker:Speaker1 text:"Hello world"}
# Choice{ choices: [ChoiceOption {option:'"Hi there"' 
#                                 elements:[Dialogue {speaker:Speaker2 text:"Hi there"}],
#                   ChoiceOption {option:'Pick up rock'
#                                 elements:[Dialogue{text:"You picked up a rock"},
#                                           Modify {variable:rock operation:ADD value:1}]}
# Condition{ if: IF{variable1:rock operation:eq 1} 
#            ifElements: [Dialogue {speaker:Speaker1 text:"That's a sweet rock"},
#                         Dialogue {speaker:Speaker2 text:"Isn't it?"}
#            elseElements: [Dialogue {text:"Speaker 1 looks at the ground, leans over, and picks up a rock."},
#                           Dialogue {speaker:Speaker1 text:"Wow this is an awesome rock."},
#                           Dialogue {speaker:Speaker2 text:"Woah, you're right."}]}
# Branch {target:Scene2}

ExampleScript = """IF var1 EQ 1
Test
Speaker 2: Wow
ELSE
Speaker 1: Right?
END"""

#Dialogue
"""Speaker1 : This is a test 
Speaker2 : No kid:ding? 
Speaker3 :Seriously? 
I'm writing a test"""

#Modify
"MOD set var1 1"

# Choice
"""CHOICE "Left"
MOD add var1 2
This is another test line
END
CHOICE "Right"
This is another test line
END
CHOICE "Forward"
This is another test line
OVER
"""
#Branch
"BRANCH Scene2"


def parse_text(text: str):
    # Working
    speaker = Regex('^([A-Za-z0-9]*?)(?=[ :])')
    dialogue = Optional(speaker('speaker') + Literal(':')) + Word(printables + ' ')('text')
    modify    = Literal("MODIFY") + one_of("ADD SUB SET MOD", caseless = True)('Operation') + Word(alphanums)('Variable') + Word(nums)('Amount')
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
    
    #example = conditional.parseString(ExampleScript)[0]
    example = dialogue.runTests(ExampleScript)
    print(example)
    return example

def read_script():
  test = ExampleScript
  
  parse_text(test)
      

if __name__ == "__main__":
  read_script()