import main

def looks_say(spriteName, blockData):
    meta = main.getMetadata()
    MESSAGE = main.isNumOrFunc(main.getInputVar(blockData["inputs"]["MESSAGE"]))
    
    return f'debugPrint("{spriteName}:{meta["line"]}: " .. tostring({MESSAGE}))'

def looks_setsizeto(spriteName, blockData):
    SIZE = main.getInputVar(blockData["inputs"]["SIZE"]) + "/100"
    return f'scaleObject("{spriteName}", {SIZE}, {SIZE})'

def looks_changesizeby(spriteName, blockData):
    CHANGE = main.getInputVar(blockData["inputs"]["CHANGE"])
    return f'size=getProperty("{spriteName}.scale.x")+({CHANGE}/100)\nscaleObject("{spriteName}", size, size)'

def looks_changeeffectby(spriteName, blockData):
    CHANGE = main.getInputVar(blockData["inputs"]["CHANGE"])
    FIELDS = blockData["fields"]["EFFECT"][0]

    if FIELDS == "GHOST":
        FIELDS = "alpha"
    else:
        FIELDS = f"alpha --[[{FIELDS} is not supported.]]"

    return f'setProperty("{spriteName}.{FIELDS}", getProperty("{spriteName}.{FIELDS}") - ({CHANGE} / 100))'

def looks_seteffectto(spriteName, blockData):
    VALUE = main.getInputVar(blockData["inputs"]["VALUE"])
    FIELDS = blockData["fields"]["EFFECT"][0]
    ARG = ""

    if FIELDS == "GHOST":
        FIELDS = "alpha"
        ARG = f"(-{VALUE} / 100) + 1"
    else:
        FIELDS = f"alpha --[[{FIELDS} is not supported.]]"
        ARG = f"(-{VALUE} / 100) + 1"

    return f'setProperty("{spriteName}.{FIELDS}", {ARG})'

def looks_cleargraphiceffects(spriteName, _):
    return f'setProperty("{spriteName}.alpha", 1)'

def looks_show(spriteName, _):
    return f'setProperty("{spriteName}.visible", true)'

def looks_hide(spriteName, _):
    return f'setProperty("{spriteName}.visible", false)'

def looks_gotofrontback(spriteName, blockData):
    FRONT_BACK = "2147483647" if blockData["fields"]["FRONT_BACK"][0] == "front" else "0"
    return f'setObjectOrder("{spriteName}", {FRONT_BACK})'

def looks_goforwardbackwardlayers(spriteName, blockData):
    NUM = main.getInputVar(blockData["inputs"]["NUM"])
    FB = "-" if blockData["fields"]["FORWARD_BACKWARD"][0] != "forward" else "+"
    return f'setObjectOrder("{spriteName}", getObjectOrder("{spriteName}") {FB} {NUM})'

def looks_size(spriteName, _):
    return f'getProperty("{spriteName}.scale.x") * 100'