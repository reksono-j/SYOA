def stripShortcutsName(transcription:str):
    """
    Gets rid of punctuation and spaces, turns string to lowercase.
    Used to standardize the key in dictionary of callback functions in keybinds.py so that
    voiceCommands.py can work better.
    """
    stripped = transcription.lower().replace(",", "").replace(".", "").replace("?","")
    stripped = stripped.replace("!","").replace("-","").replace(" ","")
    return stripped