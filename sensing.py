import main

def sensing_mousedown(_1, _2):
    return 'mousePressed("left")'

def sensing_mousex(_1, _2):
    return 'getMouseX("other")'

def sensing_mousey(_1, _2):
    return 'getMouseY("other")'

def sensing_timer(_1, _2):
    return 'runHaxeCode("return Timer.stamp();") - oldTimer'

def sensing_current(_, blockData):
    INCRE = "0"
    CURYEAR = blockData["fields"]["CURRENTMENU"][0]

    if CURYEAR == "YEAR":
        CURYEAR = "getFullYear"
    elif CURYEAR == "MONTH":
        CURYEAR = "getMonth"
        INCRE = "1"
    elif CURYEAR == "DATE":
        CURYEAR = "getDate"
    elif CURYEAR == "DAYOFWEEK":
        CURYEAR = "getDay"
        INCRE = "1"
    elif CURYEAR == "HOUR":
        CURYEAR = "getHours"
    elif CURYEAR == "MINUTE":
        CURYEAR = "getMinutes"
    elif CURYEAR == "SECOND":
        CURYEAR = "getSeconds"

    return f'runHaxeCode("return Date.now().{CURYEAR}();") + {INCRE}'

def sensing_dayssince2000(_, _2):
    return 'daysSince2000()'

def sensing_keypressed(_, blockData):
    if blockData["inputs"] == {}:
        KEY = blockData["fields"]["KEY_OPTION"][0].upper()
        
        specialKeysList = [
            [",", "COMMA"],
            [".", "DOT"],
            ["-", "DASH"],
            ["1", "ONE"],
            ["2", "TWO"],
            ["3", "THREE"],
            ["4", "FOUR"],
            ["5", "FIVE"],
            ["6", "SIX"],
            ["7", "SEVEN"],
            ["8", "EIGHT"],
            ["9", "NINE"],
            ["0", "ZERO"],
        ]

        for KCHECK in specialKeysList:
            if KEY == KCHECK[0]:
                KEY = KCHECK[1]
                break

        if KEY.endswith("ARROW"):
            KEY = KEY.split(" ")[0]

        return f'keyboardPressed("{KEY}")'

    return main.processBlock(blockData["inputs"]["KEY_OPTION"][1])

def sensing_resettimer(_, _2):
    return 'oldTimer = runHaxeCode("return Timer.stamp()")'

def sensing_username(_, _2):
    return 'os.getenv("username")'

def sensing_touchingobject(spriteName, blockData):
    if blockData["inputs"] == {}:
        TYPEOF = blockData["fields"]["TOUCHINGOBJECTMENU"][0]

        if TYPEOF == "_mouse_":
            return f'mouseOverlaps("{spriteName}")'
        elif TYPEOF == "_edge_":
            return f"true --[[{TYPEOF} is not supported!]]"
        else:
            return f'objectsOverlap("{spriteName}", "{TYPEOF}")'
        
    return main.processBlock(blockData["inputs"]["TOUCHINGOBJECTMENU"][1])

def sensing_distanceto(spriteName, blockData):
    if blockData["inputs"] == {}:
        TYPEOF = blockData["fields"]["DISTANCETOMENU"][0]

        if TYPEOF == "_mouse_":
            return f'runHaxeCode("return FlxMath.distanceToMouse(game.getLuaObject(\\"{spriteName}\\", false))")'
        else:
            return f'runHaxeCode("return FlxMath.distanceBetween(game.getLuaObject(\\"{spriteName}\\", false), game.getLuaObject(\\"{TYPEOF}\\", false))")'
        
    return main.processBlock(blockData["inputs"]["DISTANCETOMENU"][1])