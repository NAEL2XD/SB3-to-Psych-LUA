import rich.traceback as traceback
traceback.install(extra_lines=3)

import zipfile
import json
import ast
import os
import re
import time
import glob
import shutil
from wand.image import Image
from wand.color import Color
from tkinter import filedialog

import events
import motion
import looks
import sounds
import controls
import operators
import sensing
import data

def cleanup():
    for file in ["save", "spriteName", "listVars", "class", "metadata"]:
        if os.path.exists(file):
            os.remove(file)

    for rems in ["png", "svg", "wav", "mp3"]:
        for files in glob.glob(f"**.{rems}"):
            os.remove(files)

def retriveJSONSetting(schema):
    return json.load(open("settings.json"))[schema]

def getMetadata():
    return ast.literal_eval(open("metadata", "r").read())

def saveMetadata(meta):
    n = open("metadata", "w")
    n.write(str(meta))
    n.close()

def isNumOrFunc(s: str):
    if retriveJSONSetting("printingDebug"):
        print(s)

    if not s or len(s) == 0:
        return '""'
    
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s
    
    try:
        float(s)
        return s
    except ValueError:
        pass
    
    if (s.endswith("_l") or s.endswith("_v") or s.startswith("arg__")) or ("[" in s and "]" in s):
        return s
    
    if ("(" in s and ")" in s) or s in ["math.abs", "math.floor", "math.ceil", "math.sin", "math.cos", "math.tan", "math.asin", "math.acos", "math.atan", "math.log", "math.log10", "math.exp", "math.sqrt", "getProperty", "setProperty", "runHaxeCode"]:
        return s
    
    t = s.lower()
    if t == "false" or t == "true":
        return t
    
    spriteName = open("spriteName", "r").read().strip()
    if spriteName and s.startswith(f"{spriteName}."):
        return s
    
    s = s.replace('"', '\\"')
    return f'"{s}"'

def sanitizeVar(var):
    return re.sub(r'\W|^(?=\d)', '_', var)

def checkIfStageAndReturnVal(type):
    isStage = True
    typeof = []
    for fileNames in ["stageVars", "listVars"]:
        for varData in open(fileNames).read().splitlines():
            if varData.split("->")[0].lower() == sanitizeVar(type).lower():
                typeof = [sanitizeVar(type), varData.split("->")[1]]
                break

        if len(typeof) != 0:
            break

        isStage = False
    
    return [isStage, typeof]

def getInputVar(type):
    metadata = getMetadata()

    if isinstance(type[1], str):
        metadata["line"] += 1
        saveMetadata(metadata)
        return isNumOrFunc(processBlock(type[1]))
    elif isinstance(type[1], list) and len(type) == 3: # data var
        sprName = open("spriteName", "r").read()
        typeof = checkIfStageAndReturnVal(type[1][1])

        if len(typeof) == 0 or typeof[0]: # Assuming it's a stage variable
            return f'stage.{typeof[1][0]}_{typeof[1][1]}'
        
        typeof = typeof[1]
        return f'{sprName}_vars.{typeof[0]}_{typeof[1]}'
    
    ret = isNumOrFunc(type[1][1])
    return ret if len(ret) != 0 else '""'

# Fix circular Error
def fetchOPCodes():
    return {
        # Events
        "event_whenflagclicked": events.event_whenflagclicked,
        "event_whenbroadcastreceived": events.event_whenbroadcastreceived,
        "event_broadcast": events.event_broadcast,

        # Motions
        "motion_movesteps": motion.motion_movesteps,
        "motion_turnleft": motion.motion_turnleft,
        "motion_turnright": motion.motion_turnright,
        "motion_goto": motion.motion_goto,
        "motion_goto_menu": motion.motion_goto,
        "motion_gotoxy": motion.motion_gotoxy,
        "motion_glideto": motion.motion_glideto,
        "motion_glideto_menu": motion.motion_glideto,
        "motion_glidesecstoxy": motion.motion_glidesecstoxy,
        "motion_pointindirection": motion.motion_pointindirection,
        "motion_pointtowards": motion.motion_pointtowards,
        "motion_pointtowards_menu": motion.motion_pointtowards,
        "motion_changexby": motion.motion_changexby,
        "motion_setx": motion.motion_setx,
        "motion_changeyby": motion.motion_changeyby,
        "motion_sety": motion.motion_sety,
        "motion_xposition": motion.motion_xposition,
        "motion_yposition": motion.motion_yposition,
        "motion_direction": motion.motion_direction,

        # Looks
        "looks_sayforsecs": looks.looks_say,
        "looks_say": looks.looks_say,
        "looks_thinkforsecs": looks.looks_say,
        "looks_think": looks.looks_say,
        "looks_setsizeto": looks.looks_setsizeto,
        "looks_changesizeby": looks.looks_changesizeby,
        "looks_changeeffectby": looks.looks_changeeffectby,
        "looks_seteffectto": looks.looks_seteffectto,
        "looks_cleargraphiceffects": looks.looks_cleargraphiceffects,
        "looks_show": looks.looks_show,
        "looks_hide": looks.looks_hide,
        "looks_gotofrontback": looks.looks_gotofrontback,
        "looks_goforwardbackwardlayers": looks.looks_goforwardbackwardlayers,
        "looks_size": looks.looks_size,

        # Sounds
        "sound_play": sounds.sound_play,
        "sound_sounds_menu": sounds.sound_play,
        "sound_playuntildone": sounds.sound_playuntildone,

        # Controls
        "control_wait": controls.control_wait,
        "control_repeat": controls.control_repeat,
        "control_forever": controls.control_forever,
        "control_if": controls.control_if,
        "control_if_else": controls.control_if_else,
        "control_wait_until": controls.control_wait_until,
        "control_repeat_until": controls.control_repeat_until,
        "control_while": controls.control_while,
        "control_stop": controls.control_stop,

        # Operators
        "operator_equals": operators.operator_equals,
        "operator_and": operators.operator_and,
        "operator_gt": operators.operator_gt,
        "operator_lt": operators.operator_lt,
        "operator_or": operators.operator_or,
        "operator_not": operators.operator_not,
        "operator_add": operators.operator_add,
        "operator_subtract": operators.operator_subtract,
        "operator_multiply": operators.operator_multiply,
        "operator_divide": operators.operator_divide,
        "operator_random": operators.operator_random,
        "operator_join": operators.operator_join,
        "operator_letter_of": operators.operator_letter_of,
        "operator_length": operators.operator_length,
        "operator_contains": operators.operator_contains,
        "operator_mod": operators.operator_mod,
        "operator_round": operators.operator_round,
        "operator_mathop": operators.operator_mathop,

        # Sensing
        "sensing_mousedown": sensing.sensing_mousedown,
        "sensing_mousex": sensing.sensing_mousex,
        "sensing_mousey": sensing.sensing_mousey,
        "sensing_timer": sensing.sensing_timer,
        "sensing_current": sensing.sensing_current,
        "sensing_dayssince2000": sensing.sensing_dayssince2000,
        "sensing_keypressed": sensing.sensing_keypressed,
        "sensing_keyoptions": sensing.sensing_keypressed,
        "sensing_resettimer": sensing.sensing_resettimer,
        "sensing_username": sensing.sensing_username,
        "sensing_touchingobject": sensing.sensing_touchingobject,
        "sensing_touchingobjectmenu": sensing.sensing_touchingobject,
        "sensing_distanceto": sensing.sensing_distanceto,
        "sensing_distancetomenu": sensing.sensing_distanceto,

        # Data
        "data_setvariableto": data.data_setvariableto,
        "data_changevariableby": data.data_changevariableby,
        "data_addtolist": data.data_addtolist,
        "data_deleteoflist": data.data_deleteoflist,
        "data_deletealloflist": data.data_deletealloflist,
        "data_insertatlist": data.data_insertatlist,
        "data_replaceitemoflist": data.data_replaceitemoflist,
        "data_itemoflist": data.data_itemoflist,
        "data_itemnumoflist": data.data_itemnumoflist,
        "data_lengthoflist": data.data_lengthoflist,
        "data_listcontainsitem": data.data_listcontainsitem,

        # Procedures
        "procedures_prototype": data.procedures_prototype,
        "procedures_definition": data.procedures_definition,
        "procedures_call": data.procedures_call,
        "argument_reporter_string_number": data.argument_reporter_string_number,
        "argument_reporter_boolean": data.argument_reporter_string_number,
    }

curClass = {}
target = {}
opcodes = {}
def processBlock(blockID, repeatUntilNextIsNull=False):
    global curClass, target, opcodes

    if blockID == None:
        return ""

    # Python breaks if it's recursive and on a file, my next move
    if curClass == {}:
        f = open("save", "r", encoding="utf-8").read().split("[[||]]")
        curClass = ast.literal_eval(f[0])
        target   = ast.literal_eval(f[1])
        opcodes  = fetchOPCodes()
    else:
        f = open("save", "w", encoding="utf-8")
        f.write(f"{curClass}[[||]]{target}")
        f.close()

    data = curClass["blocks"].get(blockID)
    if data == None:
        # Get from class and try again
        data = json.load(open("class", "r", encoding="utf-8"))["blocks"].get(blockID)
        if data == None:
            return "nil --[=[data returned none, skipping]=]"

    if repeatUntilNextIsNull:
        stack = []

        while blockID != None:
            metadata = getMetadata()
            metadata["line"] += 1
            saveMetadata(metadata)

            stack.append(processBlock(blockID))
            try:
                blockID = curClass["blocks"].get(blockID)["next"]
            except TypeError:
                # Try again
                blockID = json.load(open("class", "r", encoding="utf-8"))["blocks"].get(blockID)["next"]

            if getMetadata()["shouldSkip"]:
                break
            
        return '\n'.join(stack)

    opc = data["opcode"]
    if opc in opcodes:
        return opcodes[opc](target["name"], data)

    return f"--[=[Unsupported OPCODE: {opc}]=]"

def main():
    global curClass, target, opcodes
    addToPrecaches = [[], []]

    os.mkdir("export")
    os.mkdir("export/scripts")
    os.mkdir("export/sounds")
    os.mkdir("export/images")
    os.mkdir("export/weeks")
    os.mkdir("export/data")
    os.mkdir("export/data/scratch")

    with open("export/weeks/scratchWeek.json", "w") as f:
        f.write('{"songs":[["Scratch","bf",[12,181,0]]],"hideFreeplay":false,"weekBackground":"","difficulties":"Normal","weekCharacters":["","",""],"storyName":"Converted Using Nael\'s SB3 to FNF Script","weekName":"","freeplayColor":[146,113,253],"hideStoryMode":false,"weekBefore":"","startUnlocked":false}')
        f.close()

    for diff in ["", "-normal"]:
        with open(f"export/data/scratch/scratch{diff}.json", "w") as f:
            f.write('{"song":{"player1":"bf","notes":[],"player2":"gf","song":"Scratch","speed":1,"gfVersion":"gf","events":[],"stage":"stage","needsVoices":true,"bpm":100}}')
            f.close()

    zip = zipfile.ZipFile(filedialog.askopenfilename(filetypes=[("Scratch Project 3.0", "*.sb3")]))
    zip.extract("project.json")

    start = time.time()
    opcodes = fetchOPCodes()
    project = json.load(open("project.json", "r", encoding="utf=8"))
    for target in project["targets"]:
        spriteName = sanitizeVar(target["name"])
        n = open("spriteName", "w")
        n.write(sanitizeVar(spriteName))
        n.close()

        metadata = {
            "line": 0,
            "shouldSkip": False,
            "containsOnCreate": False
        }
        saveMetadata(metadata)
            
        curClass = target
        n = open("class", "w", encoding="utf-8")
        n.write(json.dumps(target))
        n.close()

        for costume in target["costumes"]:
            f = costume["md5ext"]
            o = costume["name"]

            if os.path.exists(f"export/images/{o}.png"):
                continue

            zip.extract(f)
            if os.path.getsize(f) > 250: # Limit the size so that it doesn't throw an error
                if f.endswith("png"):
                    os.rename(f, f"export/images/{f}")
                else:
                    img = Image(filename=f)
                    img.format = 'png'
                    img.transparent_color(Color("#FFFFFF"), alpha=0)
                    img.save(filename=f"export/images/{o}.png")
                addToPrecaches[0].append(o)

        for sound in target["sounds"]:
            f = sound["md5ext"]
            o = sound["name"]

            if os.path.exists(f"export/sounds/{o}.ogg"):
                continue

            zip.extract(f)
            os.system(f"ffmpeg -hide_banner -loglevel quiet -i {f} -acodec libvorbis export/sounds/{o}.ogg")
            addToPrecaches[1].append(o)

        n = open("listVars", "w")

        # Collecting the variables
        compiledList = [f'-- Generated using Nael\'s SB3 to Psych Lua! https://github.com/NAEL2XD/SB3-to-Psych-LUA\nlocal {sanitizeVar(spriteName)}_vars = {{']
        for types in ["variables", "lists"]:
            for var in list(target[types].keys()):
                var = target[types][var]

                name = sanitizeVar(var[0])
                value = ""

                if types == "lists":
                    setAs = "{"
                    if len(var[1]) != 0:
                        for listLength in var[1]:
                            listLength = str(listLength).replace("\\", "\\\\")
                            setAs += f'"{listLength}",'
                    value = f"{setAs}}}"
                else:
                    value = isNumOrFunc(str(var[1]))

                vorl = "v" if types == "variables" else "l"
                n.write(f"{name}->{vorl}\n")
                compiledList.append(f'{name}_{vorl} = {value},')
        compiledList.append("}\nlocal threads = {}")
        n.close()

        if not target["isStage"]:
            compiledList.append('local stage = require("mods.scripts.Stage")\nluaDebugMode = true\nlocal oldTimer = 0\nlocal updateCounter = 0')
        else:
            compiledList.append('luaDebugMode = true\nlocal oldTimer = 0')
            n = open("stageVars", "w")
            n.write(open("listVars", "r").read())
            n.close()

        def searchForBlockOPCodes(target, allSearchFor):
            gottenBlockIDS = []
            for bID in list(target["blocks"].keys()):
                for searchFor in allSearchFor:
                    if target["blocks"].get(bID)["opcode"] == searchFor:
                        gottenBlockIDS.append([bID, searchFor])
            return gottenBlockIDS

        onCreateExists = False
        onUpdateExists = False
        onUpdateCount = 1
        for blockID, typeof in searchForBlockOPCodes(target, ["event_whenflagclicked", "control_forever", "event_whenbroadcastreceived", "procedures_definition"]):
            if typeof == "procedures_definition":
                metadata["line"] += 1
                saveMetadata(metadata)
                compiledList.append(processBlock(blockID))

                continue

            elif typeof == "event_whenflagclicked":
                onCreateExists = True

            elif typeof == "control_forever":
                if not onUpdateExists:
                    onUpdateExists = True
                    compiledList.append("function onUpdate(__)")
                
                compiledList.append(f"if updateCounter == {onUpdateCount} then")
                compiledList.append(processBlock(target["blocks"].get(blockID)["inputs"]["SUBSTACK"][1], True))
                compiledList.append("end")
                onUpdateCount += 1

                continue

            while blockID != None:
                blockData = target["blocks"].get(blockID)
                if retriveJSONSetting("addJsonDebug"):
                    compiledList.append(f'--[=[{blockData}]=]')

                compiledList.append(processBlock(blockID))
                meta = getMetadata()
                if (typeof == "event_whenbroadcastreceived" or blockData["opcode"] == "sound_playuntildone") or meta["shouldSkip"]:
                    if meta["shouldSkip"]:
                        meta["shouldSkip"] = False
                        saveMetadata(meta)

                    break

                metadata["line"] += 1
                saveMetadata(metadata)
                blockID = blockData["next"]

        if onCreateExists:
            compiledList.append("end")
        if onUpdateExists:
            compiledList.append('end')

        compiledList.append('function mouseOverlaps(tag)\naddHaxeLibrary("Reflect")\nreturn runHaxeCode([[\nvar obj = game.getLuaObject("]]..tag..[[");\nif (obj == null) obj = Reflect.getProperty(game, "]]..tag..[[");\nif (obj == null) return false;\nreturn obj.getScreenBounds(null, obj.cameras[0]).containsPoint(FlxG.mouse.getScreenPosition(obj.cameras[0]));\n]])\nend')
        compiledList.append('function itemnumoflist(list,str)\nlocal count=0\nfor _=1,#list do\nif list[_]==str then count=count+1 end\nend\nreturn count\nend')
        compiledList.append('function listcontainsitem(list,str)\nfor _=1,#list do\nif string.find(list[_],str) then return true end\nend\nreturn false\nend')
        compiledList.append('function daysSince2000()\nreturn(os.time()-os.time{year=2000,month=1,day=1})/86400\nend')
        compiledList.append('function tnew(time,func)\nlocal name="timer_"..getRandomInt(-1000000000,1000000000)\nrunTimer(name,time)\ntable.insert(threads,{name,func})\nend')
        compiledList.append('function onTimerCompleted(tag)\nimpl(tag)\nend')
        compiledList.append('function snew(snd,func)\nlocal name="snd_"..getRandomInt(-1000000000,1000000000)\nplaySound(snd,1,name)\ntable.insert(threads,{name,func})\nend')
        compiledList.append('function onSoundFinished(tag)\nimpl(tag)\nend')
        compiledList.append('function impl(t)\nfor i=1,#threads do\nif threads[i][1]==t then\nthreads[i][2]()\ntable.remove(threads,i)\nend\nend\nend')
        
        if target["isStage"]:
            compiledList.append('\nfunction onCreate()\nmakeLuaSprite(\"stage\")\nmakeGraphic(\"stage\", 1920, 1080, \"FFFFFF\")\nsetObjectCamera(\"stage\", \"hud\")\naddLuaSprite(\"stage\")\nsetProperty(\"camGame.alpha\", 0)\nend')
            compiledList.append(f'return {sanitizeVar(spriteName)}_vars')

        with open(f"export/scripts/{spriteName}.lua", "w") as f:
            f.write('\n'.join(compiledList))
            f.close()

        if retriveJSONSetting("doCleanup"):
            cleanup()

        print(f"Finished: {spriteName}")

    if os.path.exists("stageVars"):
        os.remove("stageVars")

    n = open("export/scripts/main_func.lua", "w")
    n.write('function onUpdate(_)setTextString("scoreTxt","")for i=0,1 do for j=0,3 do setPropertyFromGroup(i==0 and"opponentStrums"or"playerStrums",j,"visible",false)end end if keyboardPressed("ESCAPE")then exitSong()end end function onStartCountdown()return Function_Stop end function onCreatePost()for v0=0,1 do makeLuaSprite("a_"..v0,"",v0==0 and 480 or 0,v0==1 and 360 or 0);makeGraphic("a_"..v0,999,999,"000000");setObjectCamera("a_"..v0,"other");addLuaSprite("a_"..v0);end runHaxeCode("FlxG.updateFramerate = 30;FlxG.drawFramerate = 30;")end function onDestroy()runHaxeCode("FlxG.updateFramerate = 60;FlxG.drawFramerate = 60;")end')
    n.close()

    if retriveJSONSetting("doPrecache"):
        n = open("export/scripts/precache.lua", "w")
        n.write("function onCreate()\n")
    
        for costume in addToPrecaches[0]:
            n.write(f'precacheImage("{costume}")')
        for sounds in addToPrecaches[1]:
            n.write(f'precacheSound("{sounds}")')
        
        n.write("end")
        n.close()

    print(f"FULLY DONE! Saved in {round(time.time() - start, 5)} seconds!")

if __name__ == "__main__":
    if os.path.isdir("export"):
        shutil.rmtree("export")

    cleanup()
    main()