from pyparsing import Word, CaselessKeyword, Literal, Regex, Optional, one_of, alphanums, nums, printables, Suppress, OneOrMore
from enum import Enum
from src.editor.sceneStructure import *
import re

# Grammar 
# Dialogue - Speaker:Sentence or Sentence -> string:string or string
# modify - MODIFY Operation Variable Amount 
# Choice - CHOICE String \\\ Each line acts as a separate choice
# Conditional - IF Compare \n Elements \n IFEND ELSE \n Elements \n ELEND
# Branch - BRANCH SceneName -> BRANCH String
# Compare - string Condition string|int
# Condition - LESS | MORE | EQ | LTE | MTE
# Operation - ADD | SUB | SET | MOD

# Below is the process by which the parser processes a script

# Speaker1 : Hello world
# CHOICE Hi there
# Speaker2: Hi there
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
# (DIALOGUE, {speaker:"Speaker1" text:"Hello world"})
# (CHOICE, {option:"Hi there"})
# (DIALOGUE, {speaker:"Speaker2" text:"Hi there"})
# (END, {})
# (CHOICE, {option:"Pick up rock"})
# (DIALOGUE, {text:"You picked up a rock"})
# (MODIFY, {variable:"rock" operation:"ADD" value:"1"})
# (END, {})
# (IF, {variable1:"rock" operation:"eq" "1"})
# (DIALOGUE, {speaker:"Speaker1" text:"That's a sweet rock"})
# (DIALOGUE, {speaker:"Speaker2" text:"Isn't it?"})
# (ELSE, {})
# (DIALOGUE, {text:"Speaker 1 looks at the ground, leans over, and picks up a rock."})
# (DIALOGUE, {speaker:"Speaker1" text:"Wow this is an awesome rock."})
# (DIALOGUE, {speaker:"Speaker2" text:"Woah, you're right."})
# (End, {})
# (Branch, {target: "Scene2"})

# Then it would build the elements and place it in a scene's line list
# Dialogue {speaker:"Speaker1" text:"Hello world"}
# Choice {options: [ChoiceOption {option:'Hi there' 
#                                 elements:[Dialogue {speaker: "Speaker2" text:"Hi there"}],
#                   ChoiceOption {option: "Pick up rock"
#                                 elements:[Dialogue{text:"You picked up a rock"},
#                                           Modify {variable:"rock" operation:"ADD" value:"1"}]}
# Conditional{compare: "EQ"
#             var1: "rock" 
#             var2: "1"
#             ifElements: [Dialogue {speaker:Speaker1 text:"That's a sweet rock"},
#                          Dialogue {speaker:Speaker2 text:"Isn't it?"}
#             elseElements: [Dialogue {text:"Speaker 1 looks at the ground, leans over, and picks up a rock."},
#                           Dialogue {speaker:Speaker1 text:"Wow this is an awesome rock."},
#                           Dialogue {speaker:Speaker2 text:"Woah, you're right."}]}
# Branch {target:Scene2}

class Parsed(Enum):
  MODIFY = 0,
  END = 1,
  IF = 2,
  ELSE = 3,
  CHOICE = 4,
  BRANCH = 5,
  DIALOGUE = 6,
  SFX = 7,
  BGM = 8,
  BG = 9

def parseText(text: str):
  Speaker     = Regex('([A-Za-z0-9]*?)(?=[ :])')
  Variable    = Regex('([A-Za-z]{1}[A-Za-z0-9]*)')
  Number      = Word(nums)
  Value       = Variable | Number
  Dialogue    = Optional(Speaker('speaker') + Literal(':')) + Word(printables + ' ')('text')
  Modify      = CaselessKeyword("MODIFY") + Word(alphanums)('variable') + one_of("ADD SUB SET MOD", caseless = True)('operation') + Number('amount')
  Branch      = CaselessKeyword('BRANCH') + Word(alphanums)('scene')
  Comparator  = one_of("LESS MORE EQ LTE MTE", caseless = True)
  Compare     = Value('var1') + Comparator('comparator') + Value('var2')
  Choice      = CaselessKeyword("CHOICE") + Word(printables + ' ', exclude_chars='\n')('option')
  If          = CaselessKeyword('IF') + Compare('comparison')
  Else        = CaselessKeyword('ELSE')
  End         = CaselessKeyword('END')
  Sfx         = CaselessKeyword('SFX') + Optional(one_of("HIGH MED LOW", caseless=True)("volume")) + Regex('[a-zA-Z0-9_-./\ ]+')('name')
  Bgm         = CaselessKeyword('BGM') + Optional(one_of("HIGH MED LOW", caseless=True)("volume")) + Regex('[a-zA-Z0-9_-./\ ]+')('name')
  Background  = CaselessKeyword('Background') + Word(alphanums)('name')
  
  def LabelElement(ElementType: Parsed):
    def parseAction(str, loc, tok):
        return ElementType, tok.asDict()
    return parseAction
  
  Element = (Modify.setParseAction(LabelElement(Parsed.MODIFY))  | 
              End.setParseAction(LabelElement(Parsed.END))       |
              If.setParseAction(LabelElement(Parsed.IF))         |
              Else.setParseAction(LabelElement(Parsed.ELSE))     |
              Choice.setParseAction(LabelElement(Parsed.CHOICE)) |
              Branch.setParseAction(LabelElement(Parsed.BRANCH)) |
              Sfx.setParseAction(LabelElement(Parsed.SFX))|
              Bgm.setParseAction(LabelElement(Parsed.BGM)) |
              Background.setParseAction(LabelElement(Parsed.BG)) |
              Dialogue.setParseAction(LabelElement(Parsed.DIALOGUE)))
  
  parsedList = [x[0][0] for x in Element.scan_string(text)]
  return parsedList

def buildScene(parsedList):
  scene = Scene()
  contextStack = [scene.lines]
  for identifier, content in parsedList:
      activeContext = contextStack[-1]
      match identifier:
        case Parsed.DIALOGUE:
          dialogue = Dialogue()
          if 'speaker' in content:
            dialogue.speaker = content['speaker']
            
          text = content['text']
          
          # Regular expression to match 'audio=' or 'audio' followed by spaces and then '='
          match = re.search(r'\baudio\s*=\s*(.+)', text)
          if match:
              dialogue.audio = match.group(1).strip() 
              text = text[:match.start()].strip()
          
          dialogue.text = text
          activeContext.append(dialogue)  
        case Parsed.MODIFY:
          operation = Operation[content['operation']] # converts string to enum
          mod = Modify(operation, content['variable'], content['amount'])
          activeContext.append(mod)
        case Parsed.END:
          contextStack.pop()
        case Parsed.IF:
          conditional = Conditional(Comparator[content['comparator']], content['var1'], content['var2'])        
          activeContext.append(conditional)
          contextStack.append(conditional.ifElements)
        case Parsed.ELSE:
          contextStack.pop()
          activeContext = contextStack[-1]
          ifElement = activeContext[-1]
          if type(ifElement) is not Conditional:
            raise Exception("Else elements should be in the same logical block as If elements")
          contextStack.append(ifElement.elseElements)
        case Parsed.CHOICE:
          choice = Choice()
          if type(activeContext[-1]) is Choice:
            choice = activeContext[-1]
          else:
            activeContext.append(choice)
          option = ChoiceOption(content['option'])
          choice.options.append(option)
          contextStack.append(option.consequences)
        case Parsed.BRANCH:
          activeContext.append(Branch(content['scene']))
          scene.links.append(content['scene'])
        case Parsed.SFX:
          if 'volume' in content:
            activeContext.append(Asset("sfx", content['name'], content['volume']))
          else:
            activeContext.append(Asset("sfx", content['name']))
        case Parsed.BGM:
          if 'volume' in content:
            activeContext.append(Asset("bgm", content['name'], content['volume']))
          else:
            activeContext.append(Asset("bgm", content['name']))
        case Parsed.BG:
          activeContext.append(Asset("bg", content['name']))
  return scene
  
def readScript(script: str):
  parsedList = parseText(script)
  return buildScene(parsedList)

if __name__ == "__main__":
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
  scene = readScript(ExampleScript)
  print(scene)
  lines = scene.lines
  for line in lines:
    print(line)