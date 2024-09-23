from pyparsing import Combine, Word, CaselessKeyword, Literal, Suppress, CharsNotIn, nested_expr, Regex, Optional, OneOrMore, one_of, alphanums, nums, printables


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

ExampleScript = """Speaker1 : Hello world
CHOICE Hi there
 Speaker2: Hi there
END
Choice Pick up rock
You picked up a rock
modify rock add 1 
END
IF rock eq 1
Speaker1 : That's a sweet rock
Speaker2 : Isn't it?
ELSE
Speaker 1 looks at the ground, leans over, and picks up a rock.
Speaker1 : Wow this is an awesome rock.
Speaker2: Woah, you're right.
END
Branch Scene2"""

def parse_text(text: str):
    Speaker     = Regex('^([A-Za-z0-9]*?)(?=[ :])')
    Variable    = Regex('^([A-Za-z]{1}[A-Za-z0-9]*)')('Value')
    Number      = Word(nums)('Value')
    Value       = Variable | Number
    Dialogue    = Optional(Speaker('speaker') + Literal(':')) + Word(printables + ' ')('Text')
    Modify      = CaselessKeyword("MODIFY") + Word(alphanums)('Variable') + one_of("ADD SUB SET MOD", caseless = True)('Operation') + Number('Amount')
    Branch      = CaselessKeyword('BRANCH') + Word(alphanums)('scene')
    Comparator  = one_of("LESS MORE EQ LTE MTE", caseless = True)
    Compare     = Variable('var1') + Comparator('condition') + Variable('var2')
    Choice      = CaselessKeyword("CHOICE") + Word(printables + ' ')('Option')
    If          = CaselessKeyword('IF') + Compare
    Else        = CaselessKeyword('ELSE') # TODO split into two lists if('if') and else('else') split by ELSE
    End         = CaselessKeyword('END')
    
    Element = Modify | End | If | Else | Choice | Branch | Dialogue
    
    
    Conditional = nested_expr(opener=If, closer=End, content=Combine(OneOrMore(~If + ~End + Word(printables + ' '))))

    #example = [x[0] for x in conditional.searchString(ExampleScript).as_list()]
    #example = dialogue.runTests(ExampleScript)
    #example = End.parse_string("END")
    example = Element.runTests(ExampleScript)
    #example = [x for x in Element.scan_string(ExampleScript)]
    #for x in example:
    #  print(x)
    
    print(example)
    return example

def read_script():
  test = ExampleScript
  
  parse_text(test)
      

if __name__ == "__main__":
  read_script()