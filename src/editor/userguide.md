# Speak Your Own Adventure User Guide

## Introduction
Speak Your Own Adventure is a program designed for writing and playing interactive digital narratives, wherein user choices can influence the outcome of a story. SYOA is similar to programs such as Ren'Py, Twine, and Ink, but aims to provide a more inclusive and accessible experience for low-vision or blind authors through features such as built-in speech-to-text transcription, text-to-speech story audio, and screen reader compatibility. 

## Starting a New Project
To begin creating an SYOA story, click the "Start a new project" option from the Home screen. After choosing a project name, you will be taken to the project file menu, where you can see all the scenes within the opened project. SYOA projects are a collection of connected scenes (text files) that contain custom script.
To begin scripting, click the "Create New Scene" button, and double-click the file name in the populated list.

## Editing
The primary mode of the SYOA editor is a tab-based editor inspired by coding IDEs. When a scene file is open, a numbered-line text box, and "Save Scene", "Close File", and "Open Another File Tab" buttons are displayed.
The numbered-line text box will display the contents of the currently opened scene file.
"Save Scene" and "Close File" respectively save the current text box contents to the opened file and close the opened file within the editor.
The "Open Another File Tab" will create a new tab on the upper-tab bar, which can be navigated to with a right-click. This tab will be opened to the project file menu by default, and allows for multiple scene files within a project to be opened simultaneously.

### Keybinds
SYOA provides keybind shortcuts for the easier navigation of the editor menus and access to speech-to-text transcription. By default, the shortcut menu can be accessed by pressing ```Ctrl+/```.
Keybinds can be changed by pressing the button to the right of the action name and inputting the desired key sequence (two or more keys pressed simultaneously) for the shortcut.

### Speech to Text
SYOA provides native support for speech-to-text transcription while editing. By default, the shortcut to turn-on transcription is ```Ctrl+T```.
While activated, SYOA will record all audio from the default Windows microphone device until the transcription shortcut is repressed. After recording, SYOA will process the audio as text and input the result into whatever textbox the user's cursor is focused into. 
Note: Short recordings, poor microphone quality, or long periods of silence may affect the accuracy of the transcription. 

### Searching
In especially large project files, searching for certain keywords or dialogue lines may become difficult. By using the default ```Ctrl+F``` shortcut, the search menu can be opened on an already opened/focused scene file.
The search menu takes in text input and then returns openable results for that text found within these locations throughout a project:
1. Within the text of the current scene
2. Within the text of all scenes with non-broken links (branches) to the current scene
3. Within the names of all linked scenes
Note: This will automatically save the current file and pre-compile the current project, so it's best used on newly opened projects.

## Scripting
SYOA scripts consist of dialogue (what is displayed to readers) and keyword functions (used to manipulate data, story branching, player visuals, etc.). 

### Dialogue
Dialogue encompasses all lines of a scene script that are displayed to the reader, outside of those displayed via choices. A line of dialogue can either be any line of text that does not begin with a keyword function or take the form of:
```character_name : dialogue```,
where "character_name" is the displayed speaker of the dialogue and "dialogue" is what the speaker says.

### Characters
Characters are used to track the different dialogue speakers within a script, including the text-to-speech model used for their lines.  Before use in a story, a character must first be created through the Character Manager, which can be accessed via Options -> Characters. 
Within the Character Manager, character aliases and TTS parameters can be selected.

#### Aliases
An alias is an alternate name that a character can go by in the script. When an alias is used for the "character_name" portion of a dialogue line, the player will either display the character's name (not the alias) or a predetermined name for that specific character alias. However, all alias' of a character share the same text-to-speech settings in the player. 

### Keywords
Keywords are certain words, symbols, or phrases that modify the flow of the story within a SYOA script. Keywords only function outside of dialogue lines. In this document, all keywords are denoted in uppercase (ex. ```BRANCH```), but are case-insensitive when used inside of a script.

### BRANCH/END
The ```BRANCH``` and ```END``` keywords are almost exclusively used in the last executed line of a scene.
The ```BRANCH``` keyword is used with the syntax:
```BRANCH scene_name```,
where "scene_name" is the file name of the next scene to execute in the story. This scene file must be present in the story folder, otherwise compilation will fail. 
When used in the last line of scene, the ```END``` keyword (with no surrounding syntax) marks the end of story execution.

### Variables
Variables are used to track and modify data as the player progresses through a story. Before use in a story, a variable must first be created through the Variable Manager, which can be accessed via Options -> Variables. Created variables consist of a name and initial value. 
Note: Variables can only be integer values (1,2, 3, etc.).
#### MODIFY
The ```MODIFY``` keyword is used to change the value of a declared variable within the story script. A line using the ```MODIFY``` keyword looks like the following: 
```MODIFY variable_name operation value```,
where "variable_name" is the label for the target variable, "operation" is one of the following mathematical functions, and "value" is the integer being used in the operation along with the variable's value. 
#### Operations
The following are the keywords used for mathematical operations.
##### ADD
Adds "value" to variable's value.
##### SUB
Subtracts "value" from variable's value.
##### SET
Sets variable's value to "value".
##### MOD 
Sets variable's value to the remainder of the variable's original value divided by "value".

### Conditionals
Conditionals are used to compare variables with each other and set values to allow for more complex story branching and variable manipulation.
### Comparisons
While there is no ```COMPARE``` keyword, comparisons take the form:
```value1 condition value2```,
where either "value" could be a variable, and "condition" is one of the following equivalence operators. While comparisons return whether or not the statement is true or false, they cannot be used outside of IF/ELSE statements. 
#### IF/ELSE
The ```IF``` and ```ELSE``` keywords are used to branch dialogue within a scene without the use of a a ```CHOICE```. 
The ```IF``` statement takes the form of:
```IF COMPARISON```,
If there are no ```ELSE``` keywords following ```IF``` then all lines prior to an ```END``` will execute only if the comparison statement was true. 
If ```ELSE``` follows if, then branching differs based on the value of the comparison. If true, lines after ```IF``` will play and then playback will skip to after the ```END``` keyword once ```ELSE``` is reached. If the comparison is false, only the lines between ```ELSE``` and ```END``` will execute during playback.
#### Conditions
The following are the keywords used for comparison statements.
##### LESS
Returns true if "value1" is less than "value2".
##### MORE
Returns true if "value1" is more than "value2".
##### EQ
Returns true if "value1" is equal to "value2".
##### LTE
Returns true if "value1" is less than or equal to "value2".
##### MTE
Returns true if "value1" is more than or equal to "value2".

### Choices
Choices allow for player input to influence the direction of an SYOA story. The ```CHOICE``` keyword is used with the following format:
```
CHOICE option1
option1 dialogue
END
CHOICE option2
option2 dialogue
END
```
All adjacent choices (```CHOICE``` keyword lines that consecutively follow an ```END``` line of a previous ```CHOICE```) will be presented as clickable buttons to a player at a given time, with the their "option" text being outwardly displayed. When a certain ```CHOICE``` is clicked, the story playback will branch into lines between the chosen option and the ```END``` keyword. If there is no further branching within a ```CHOICE```, the story playback will skip to the first non-```CHOICE``` line once the internal ```END``` is reached.

## Custom Audio/Images
SYOA allows for custom audio and images to be played/displayed during a story. Each of the following keywords take the following syntax:
```KEYWORD file_path```
where "file_path" is the relative path to the audio or image file within the project folder. 
##### BGM
Plays/changes the current background music when this line is reached
##### SFX
Plays a sound effect when this line is reached.
##### BG
Displays a custom image background when this line is reached.

## Compilation
When editing is finished, a SYOA project must first be compiled before it can be played in the SYOA player. To compile a project, first open the editor home screen then navigate to File -> Compile Project.
The Compile Project menu requires a final story name to be chosen (can differ from the project name), the project directory to be selected, and a starting scene to be chosen. This starting scene will be beginning of the story playback within the player.
A compiled SYOA story file has the .syoa extension.

## Editor Customization
Elements of the SYOA editor can be tweaked for better readability, visual clarity, and style. These options are located via Menus -> Settings and Menu -> Preferences, both of which save display options across sessions.

## Playing
.syoa files can be played via the SYOA player. 
When played, a SYOA file will run sequentially through each line, starting at the first line of the selected starting scene until and ```END``` is reached at the final line of a scene.
Dialogue can be progressed through by left-clicking on the player screen or using the spacebar. Choices are also selected via mouse click.
The associated text-to-speech audio created for each line of dialogue can be played by pressing the ```C``` key by default. 