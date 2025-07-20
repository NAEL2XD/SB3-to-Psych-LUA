import main
containsONCREATE = False

def event_whenflagclicked(spriteName, _):
    global containsONCREATE

    if containsONCREATE:
        return ""
    
    main.metadata["indent"] += 1
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