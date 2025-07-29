import main

def motion_movesteps(spriteName, blockData):
    STEPS = main.getInputVar(blockData["inputs"]["STEPS"])
    return f'setProperty("{spriteName}.x",getProperty("{spriteName}.x")+{STEPS})'

def motion_turnleft(spriteName, blockData):
    DEGREES = main.getInputVar(blockData["inputs"]["DEGREES"])
    return f'setProperty("{spriteName}.angle",getProperty("{spriteName}.angle")-{DEGREES})'

def motion_turnright(spriteName, blockData):
    DEGREES = main.getInputVar(blockData["inputs"]["DEGREES"])
    return f'setProperty("{spriteName}.angle",getProperty("{spriteName}.angle")+{DEGREES})'

def motion_goto(spriteName, blockData):
    if blockData["fields"] != {}:
        to = blockData["fields"]["TO"][0]
        if to == "_random_":
            return ["getRandomInt(0, 480)", "getRandomInt(0, 360)"]
        elif to == "_mouse_":
            return ['getMouseX("hud")', 'getMouseY("hud")']
        else: # Assuming it's a sprite
            return [f'getProperty("{to}.x")', f'getProperty("{to}.y")']
        
    TO = main.processBlock(blockData["inputs"]["TO"])
    
    if TO[1] == "_random_":
        return f'setProperty("{spriteName}.x",getRandomInt(0, 480)+240)\nsetProperty("{spriteName}.y",getRandomInt(0, 360)+180)'
    elif TO[1] == "_mouse_":
        return f'setProperty("{spriteName}.x",getMouseX("hud"))\nsetProperty("{spriteName}.y",getMouseY("hud"))'
    else: # Assuming it's a sprite
        return f'setProperty("{spriteName}.x",getProperty("{TO[1]}.x"))\nsetProperty("{spriteName}.y",getProperty("{TO[1]}.y"))'
    
def motion_gotoxy(spriteName, blockData):
    X = main.getInputVar(blockData["inputs"]["X"])
    Y = main.getInputVar(blockData["inputs"]["Y"])
    return f'setProperty("{spriteName}.x",{X}+240-(getProperty("{spriteName}.width")/2))\nsetProperty("{spriteName}.y",{Y}+180-(getProperty("{spriteName}.height")/2))'

def motion_glideto(spriteName, blockData):
    if blockData["fields"] != {}:
        to = blockData["fields"]["TO"][0]
        if to == "_random_":
            return ["getRandomInt(0, 480)", "getRandomInt(0, 360)"]
        elif to == "_mouse_":
            return ['getMouseX("hud")', 'getMouseY("hud")']
        else: # Assuming it's a sprite
            return [f'getProperty("{to}.x")', f'getProperty("{to}.y")']
        
    SECS = main.getInputVar(blockData["inputs"]["SECS"])
    TO = main.processBlock(blockData["inputs"]["TO"])
    return f'doTweenX("{spriteName}_glideX","{spriteName}",{TO[0]}+240,{SECS})\ndoTweenY("{spriteName}_glideY","{spriteName}",{TO[1]}+180,{SECS})'

def motion_glidesecstoxy(spriteName, blockData):
    SECS = main.getInputVar(blockData["inputs"]["SECS"])
    X = main.getInputVar(blockData["inputs"]["X"])
    Y = main.getInputVar(blockData["inputs"]["Y"])
    return f'doTweenX("{spriteName}_glideX","{spriteName}",{X}+240,{SECS})\ndoTweenX("{spriteName}_glideY","{spriteName}",{Y}+180,{SECS})'

def motion_pointindirection(spriteName, blockData):
    DIRECTION = main.getInputVar(blockData["inputs"]["DIRECTION"])
    return f'setProperty("{spriteName}.angle", {DIRECTION})'

def motion_pointtowards(spriteName, blockData):
    if blockData["fields"] != {}:
        to = blockData["fields"]["TOWARDS"][0]
        if to == "_mouse_":
            return f'math.atan2(getMouseY("hud")-getProperty("{spriteName}.y"),getMouseX("hud")-getProperty("{spriteName}.x"))'
        elif to == "_random_":
            return f'getRandomInt(-180,180)'
        else:
            return f'getProperty("{to}.angle")'

    TOWARDS = main.processBlock(blockData["inputs"]["TOWARDS"])
    return f'setProperty("{spriteName}.angle",{TOWARDS})'

def motion_changexby(spriteName, blockData):
    DX = main.getInputVar(blockData["inputs"]["DX"])
    return f'setProperty("{spriteName}.x",getProperty("{spriteName}.x")+{DX})'

def motion_setx(spriteName, blockData):
    X = main.getInputVar(blockData["inputs"]["X"])
    return f'setProperty("{spriteName}.x",{X}+240-(getProperty("{spriteName}.width")/2))'

def motion_changeyby(spriteName, blockData):
    DY = main.getInputVar(blockData["inputs"]["DY"])
    return f'setProperty("{spriteName}.y",getProperty("{spriteName}.y")+{DY})'

def motion_sety(spriteName, blockData):
    Y = main.getInputVar(blockData["inputs"]["Y"])
    return f'setProperty("{spriteName}.y",{Y}+180-(getProperty("{spriteName}.height")/2))'

def motion_xposition(spriteName, _):
    return f'getProperty("{spriteName}.x")-240'

def motion_yposition(spriteName, _):
    return f'getProperty("{spriteName}.y")-180'

def motion_direction(spriteName, _):
    return f'getProperty("{spriteName}.angle")'