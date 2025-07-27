import main

def sound_play(_, blockData):
    if blockData["fields"] != {}:
        return blockData["fields"]["SOUND_MENU"][0]
    
    CODE = main.isNumOrFunc(main.processBlock(blockData["inputs"]["SOUND_MENU"][1]))
    return f"playSound({CODE})"

def sound_playuntildone(_, blockData):
    if blockData["fields"] != {}:
        return blockData["fields"]["SOUND_MENU"][0]
    
    meta = main.getMetadata()
    meta["shouldSkip"] = True
    main.saveMetedata(meta)
    
    CODE = main.isNumOrFunc(main.processBlock(blockData["inputs"]["SOUND_MENU"][1]))
    FUNC = main.processBlock(blockData["next"], True)
    return f"snew({CODE}, function()\n{FUNC}\nend)"