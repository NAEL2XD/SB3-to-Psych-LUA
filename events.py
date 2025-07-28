import main
import ast

def event_whenflagclicked(spriteName, _):
    if main.getMetadata()["containsOnCreate"]:
        return ""
    
    f = ast.literal_eval(open("save", "r", encoding="utf-8").read().split("[[||]]")[0])

    try:
        x = f["x"]
        y = f["y"]
        visible = f["visible"]
        costume = f["costumes"][0]["name"]
    except:
        x = 0
        y = 0
        visible = True
        costume = spriteName

    meta = main.getMetadata()
    meta["containsOnCreate"] = True
    main.saveMetadata(meta)
    
    return f"""function onCreatePost()
    makeLuaSprite("{spriteName}", "{costume}", {x}+240, {y}+180)
    setObjectCamera("{spriteName}", "other")
    setProperty("{spriteName}.visible", {str(visible).lower()})
    addLuaSprite("{spriteName}")
    
    addHaxeLibrary("Timer", "haxe")
    addHaxeLibrary("Date", "haxe")
    addHaxeLibrary("FlxMath", "flixel.math")
    oldTimer = runHaxeCode("return Timer.stamp()")
    setPropertyFromClass("flixel.FlxG", "mouse.visible", true)
    -- code begins here"""

def event_whenbroadcastreceived(_, blockData):
    BROADCAST_OPTION = main.sanitizeVar(blockData["fields"]["BROADCAST_OPTION"][0]).replace(" ", "_")
    CODE = main.processBlock(blockData["next"], True)
    return f'function {BROADCAST_OPTION}()\n{CODE}\nend'

def event_broadcast(_, blockData):
    SANITIZE = main.getInputVar(blockData["inputs"]["BROADCAST_INPUT"]).replace(" ", "_")
    return f'callOnLuas(caller, {SANITIZE})'