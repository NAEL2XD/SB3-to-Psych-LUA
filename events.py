import main
containsONCREATE = False

def event_whenflagclicked(spriteName, _):
    global containsONCREATE

    if containsONCREATE:
        return ""
    
    containsONCREATE = True
    return f"""function onCreate()
    makeLuaSprite("stage")
    makeGraphic("stage", 1920, 1080, "FFFFFF")
    setObjectCamera("stage", "other")
    addLuaSprite("stage")

    makeLuaSprite("{spriteName}", "{spriteName}", 0, 0)
    setObjectCamera("{spriteName}", "other")
    addLuaSprite("{spriteName}")
    
    addHaxeLibrary("Timer", "haxe")
    addHaxeLibrary("Date", "haxe")
    addHaxeLibrary("FlxMath", "flixel.math")
    local oldTimer = runHaxeCode("return Timer.stamp()")
    -- code begins here"""

def event_whenbroadcastreceived(_, blockData):
    BROADCAST_OPTION = main.sanitizeVar(blockData["fields"]["BROADCAST_OPTION"][0]).replace(" ", "_")
    CODE = main.processBlock(blockData["next"], True)
    return f'function {BROADCAST_OPTION}()\n{CODE}\nend'

def event_broadcast(_, blockData):
    SANITIZE = main.getInputVar(blockData["inputs"]["BROADCAST_INPUT"]).replace(" ", "_")
    return f'caller = {SANITIZE}\ncallOnLuas(caller, {{}})'