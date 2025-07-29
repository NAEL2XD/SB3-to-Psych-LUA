import main

def sound_play(_, blockData):
    if blockData["fields"] != {}:
        return blockData["fields"]["SOUND_MENU"][0]
    
    CODE = main.isNumOrFunc(main.processBlock(blockData["inputs"]["SOUND_MENU"][1]))
    return f"playSound({CODE})"

def sound_playuntildone(_, blockData):
    if blockData["fields"] != {}:
        return blockData["fields"]["SOUND_MENU"][0]
    
    CODE = main.isNumOrFunc(main.processBlock(blockData["inputs"]["SOUND_MENU"][1]))
    FUNC = main.processBlock(blockData["next"], True)

    meta = main.getMetadata()
    meta["shouldSkip"] = True
    main.saveMetadata(meta)

    return f"snew({CODE},function()\n{FUNC}\nend)"

# the following stuff below is likely broken so yeah
def sound_stopallsounds(_, _2):
    return 'runHaxeCode("for (sound in FlxG.sound.list.members) if (sound != null && !sound.persist) sound.destroy();")'

def sound_changeeffectby(_, blockData):
    VALUE = main.getInputVar(blockData["inputs"]["VALUE"])
    EFFECT = blockData["fields"]["EFFECT"][0].lower()
    return f'runHaxeCode("for (sound in FlxG.sound.list.members) if (sound != null) sound.{EFFECT} += "..({VALUE}/100)..";")'

def sound_seteffectto(_, blockData):
    VALUE = main.getInputVar(blockData["inputs"]["VALUE"])
    EFFECT = blockData["fields"]["EFFECT"][0].lower()
    return f'runHaxeCode("for (sound in FlxG.sound.list.members) if (sound != null) sound.{EFFECT} = "..({VALUE}/100)..";")'

def sound_cleareffects(_, _2):
    return 'runHaxeCode("for (sound in FlxG.sound.list.members) if (sound != null) {sound.pitch = sound.pan = 0; sound.volume = 1;}")'

def sound_changevolumeby(_, blockData):
    VOLUME = main.getInputVar(blockData["inputs"]["VOLUME"])
    return f'runHaxeCode("for (sound in FlxG.sound.list.members) if (sound != null) sound.volume += "..({VOLUME}/100)..";")'

def sound_setvolumeto(_, blockData):
    VOLUME = main.getInputVar(blockData["inputs"]["VOLUME"])
    return f'runHaxeCode("for (sound in FlxG.sound.list.members) if (sound != null) sound.volume = "..({VOLUME}/100)..";")'

def sound_volume(_, _2):
    return 'runHaxeCode("for (sound in FlxG.sound.list.members) {if (sound != null) return sound.volume;} return 1") * 100'