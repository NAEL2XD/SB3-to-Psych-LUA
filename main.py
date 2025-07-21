import rich.traceback as traceback
traceback.install(extra_lines=3)

import zipfile
import json
import ast
import os
import re
import shutil
import time
from tkinter import filedialog

import events
import motion
import looks
import controls
import operators
import sensing
import data

zip = zipfile.ZipFile(filedialog.askopenfilename(filetypes=[("Scratch Project 3.0", "*.sb3")]))

metadata = {
    "line": 0,
    "isAFunc": False,
    "spriteName": "None"
}

def retriveJSONSetting(schema):
    return json.load(open("settings.json"))[schema]

def getMetadata():
    return metadata

def isNumOrFunc(s: str):
    print(s)

    if not s:
        return '""'
    
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s
    
    try:
        float(s)
        return s
    except ValueError:
        pass
    
    if (s.endswith("_l") or s.endswith("_v")) or ("[" in s and "]" in s):
        return s
    
    if ("(" in s and ")" in s) or s in ["math.abs", "math.floor", "math.ceil", "math.sin", "math.cos", "math.tan", "math.asin", "math.acos", "math.atan", "math.log", "math.log10", "math.exp", "math.sqrt", "getProperty", "setProperty", "runHaxeCode"]:
        return s
    
    sprite_name = ""
    if os.path.exists("spriteName"):
        with open("spriteName", "r") as f:
            sprite_name = f.read().strip()
    
    if sprite_name and s.startswith(f"{sprite_name}."):
        return s
    
    s = s.replace('"', '\\"')
    return f'"{s}"'

def getInputVar(type):
    metadata = getMetadata()

    if isinstance(type[1], str):
        metadata["isAFunc"] = True
        return isNumOrFunc(processBlock(type[1]))
    elif isinstance(type[1], list) and len(type) == 3: # data var
        sprName = open("spriteName", "r").read()
        typeof = []

        for varData in open("listVars").read().splitlines():
            if varData.startswith(sanitizeVar(type[1][1])):
                typeof = [sanitizeVar(type[1][1]), varData.split("->")[1]]
                break

        if len(typeof) == 0:
            return f'--[[{typeof}]]'
        
        return f'{sprName}_vars.{typeof[0]}_{typeof[1]}'
    
    metadata["isAFunc"] = False
    ret = isNumOrFunc(type[1][1])
    return ret if len(ret) != 0 else '""'

def sanitizeVar(var):
    return re.sub(r'\W|^(?=\d)', '_', var)

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

        # Controls
        "control_wait": controls.control_wait,
        "control_repeat": controls.control_repeat,
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
        "data_listcontainsitem": data.data_listcontainsitem
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
        metadata["isAFunc"] = True
        stack = []

        while blockID != None:
            stack.append(processBlock(blockID))
            try:
                blockID = curClass["blocks"].get(blockID)["next"]
            except TypeError:
                # Try again
                blockID = json.load(open("class", "r", encoding="utf-8"))["blocks"].get(blockID)["next"]
            
        return '\n'.join(stack)

    opc = data["opcode"]
    if opc in opcodes:
        return opcodes[opc](target["name"], data)

    return f"--[=[Unsupported OPCODE: {opc}]=]"

def main():
    global curClass, target, opcodes
    start = time.time()

    if os.path.exists("export"):
        shutil.rmtree("export")

    os.mkdir("export")
    os.mkdir("export/scripts")
    os.mkdir("export/images")
    os.mkdir("export/weeks")
    os.mkdir("export/data")
    os.mkdir("export/data/scratch")

    with open("export/weeks/scratchWeek.json", "w") as f:
        f.write('{"songs":[["Scratch","bf",[12,181,0]]],"hideFreeplay":false,"weekBackground":"","difficulties":"Normal","weekCharacters":["","",""],"storyName":"Converted Using Nael\'s SB3 to FNF Script","weekName":"","freeplayColor":[146,113,253],"hideStoryMode":false,"weekBefore":"","startUnlocked":false}')
        f.close()

    for diff in ["", "-normal"]:
        with open(f"export/data/scratch/scratch{diff}.json", "w") as f:
            f.write('{"song":{"speed":1,"stage":"","player1":"","player2":"","notes":[],"bpm":0,"song":"Scratch"}}')
            f.close()

    zip.extract("project.json")
    opcodes = fetchOPCodes()
    project = json.load(open("project.json", "r", encoding="utf=8"))
    for target in project["targets"]:
        events.containsONCREATE = False

        if not target["isStage"]:
            if len(target["blocks"]) == 0:
                continue

            print(list(target["blocks"].keys()))

            spriteName = sanitizeVar(target["name"])
            n = open("spriteName", "w")
            n.write(sanitizeVar(spriteName))
            n.close()

            metadata = {
                "line": 0,
                "isAFunc": False,
                "spriteName": sanitizeVar(spriteName)
            }
            
            curClass = target
            n = open("class", "w", encoding="utf-8")
            n.write(json.dumps(target))
            n.close()

            n = open("listVars", "w")

            # Collecting the variables
            compiledList = [f'local {sanitizeVar(spriteName)}_vars = {{']
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
            compiledList.append("}")
            n.close()

            def searchForBlockOPCodes(target, allSearchFor):
                gottenBlockIDS = []
                for bID in list(target["blocks"].keys()):
                    for searchFor in allSearchFor:
                        if target["blocks"].get(bID)["opcode"] == searchFor:
                            gottenBlockIDS.append([bID, searchFor])
                return gottenBlockIDS

            for blockID, typeof in searchForBlockOPCodes(target, ["event_whenflagclicked", "event_whenbroadcastreceived"]):
                while blockID != None:
                    blockData = target["blocks"].get(blockID)
                    if retriveJSONSetting("addJsonDebug"):
                        compiledList.append(f'--[=[{blockData}]=]')

                    compiledList.append(processBlock(blockID))
                    if typeof == "event_whenbroadcastreceived":
                        break

                    metadata["line"] += 1
                    blockID = blockData["next"]

            if events.containsONCREATE:
                compiledList.append("end")

            compiledList.append('function wait(n) if n>0 then os.execute("ping -n "..tonumber(n+1).." localhost > NUL") end end')
            compiledList.append("""function mouseOverlaps(tag)
    addHaxeLibrary('Reflect')
    return runHaxeCode([[
        var obj = game.getLuaObject(']]..tag..[[');
        if (obj == null) obj = Reflect.getProperty(game, ']]..tag..[[');
        if (obj == null) return false;
        return obj.getScreenBounds(null, obj.cameras[0]).containsPoint(FlxG.mouse.getScreenPosition(obj.cameras[0]));
    ]])
end""")
            compiledList.append("""function itemnumoflist(list,str)
    local count=0
    for _=1,#list do
        if list[_]==str then
            count=count+1
        end
    end
    return count
end""")
            compiledList.append("""function listcontainsitem(list,str)
    for _=1,#list do
        if string.find(list[_],str) then
            return true
        end
    end
    return false
end""")
            
            with open(f"export/scripts/{spriteName}.lua", "w") as f:
                f.write('\n'.join(compiledList))
                f.close()

            if os.path.exists("save"):
                os.remove("save")
            if os.path.exists("spriteName"):
                os.remove("spriteName")
            if os.path.exists("listVars"):
                os.remove("listVars")
            if os.path.exists("class"):
                os.remove("class")

            print(f"Finished: {spriteName}")

    print(f"FULLY DONE! Saved in {round(time.time() - start, 5)} seconds!")

if __name__ == "__main__":
    main()