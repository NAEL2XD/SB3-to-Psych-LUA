import main

def data_setvariableto(spriteName, blockData):
    VALUE = main.getInputVar(blockData["inputs"]["VALUE"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["VARIABLE"][0])
    spriteName = main.sanitizeVar(spriteName)
    RESULT = main.checkIfStageAndReturnVal(VARIABLE)

    if RESULT[0]:
        return f'stage.{RESULT[1][0]}_{RESULT[1][1]} = {VALUE}'
    
    return f'{spriteName}_vars.{VARIABLE}_v = {VALUE}'

def data_changevariableby(spriteName, blockData):
    VALUE = main.getInputVar(blockData["inputs"]["VALUE"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["VARIABLE"][0])
    spriteName = main.sanitizeVar(spriteName)
    RESULT = main.checkIfStageAndReturnVal(VARIABLE)

    if RESULT[0]:
        return f'stage.{RESULT[1][0]}_{RESULT[1][1]} = stage.{RESULT[1][0]}_{RESULT[1][1]} + {VALUE}'
    
    return f'{spriteName}_vars.{VARIABLE}_v = {spriteName}_vars.{VARIABLE}_v + {VALUE}'

def data_addtolist(spriteName, blockData):
    ITEM = main.getInputVar(blockData["inputs"]["ITEM"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["LIST"][0])
    spriteName = main.sanitizeVar(spriteName)
    return f'table.insert({spriteName}_vars.{VARIABLE}_l, {ITEM})'

def data_deleteoflist(spriteName, blockData):
    INDEX = main.getInputVar(blockData["inputs"]["INDEX"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["LIST"][0])
    spriteName = main.sanitizeVar(spriteName)
    return f'table.remove({spriteName}_vars.{VARIABLE}_l, {INDEX})'

def data_deletealloflist(spriteName, blockData):
    LIST = main.sanitizeVar(blockData["fields"]["LIST"][0])
    spriteName = main.sanitizeVar(spriteName)
    return f'{spriteName}_vars.{LIST}_l = {{}}'

def data_insertatlist(spriteName, blockData):
    ITEM = main.getInputVar(blockData["inputs"]["ITEM"])
    INDEX = main.getInputVar(blockData["inputs"]["INDEX"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["LIST"][0])
    spriteName = main.sanitizeVar(spriteName)
    return f'table.insert({spriteName}_vars.{VARIABLE}_l, {INDEX}, {ITEM})'

def data_replaceitemoflist(spriteName, blockData):
    ITEM = main.getInputVar(blockData["inputs"]["ITEM"])
    INDEX = main.getInputVar(blockData["inputs"]["INDEX"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["LIST"][0])
    spriteName = main.sanitizeVar(spriteName)
    return f'{spriteName}_vars.{VARIABLE}_l[{INDEX}] = {ITEM}'

def data_itemoflist(spriteName, blockData):
    INDEX = main.getInputVar(blockData["inputs"]["INDEX"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["LIST"][0])
    spriteName = main.sanitizeVar(spriteName)
    return f'{spriteName}_vars.{VARIABLE}_l[{INDEX}]'

def data_itemnumoflist(spriteName, blockData):
    ITEM = main.getInputVar(blockData["inputs"]["ITEM"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["LIST"][0])
    spriteName = main.sanitizeVar(spriteName)
    return f'itemnumoflist({spriteName}_vars.{VARIABLE}_l, {ITEM})'

def data_lengthoflist(spriteName, blockData):
    VARIABLE = main.sanitizeVar(blockData["fields"]["LIST"][0])
    spriteName = main.sanitizeVar(spriteName)
    return f'#{spriteName}_vars.{VARIABLE}_l'

def data_listcontainsitem(spriteName, blockData):
    ITEM = main.getInputVar(blockData["inputs"]["ITEM"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["LIST"][0])
    spriteName = main.sanitizeVar(spriteName)
    return f'listcontainsitem({spriteName}_vars.{VARIABLE}_l, {ITEM})'

def procedures_definition(_, blockData):
    CUSTOM = main.processBlock(blockData["inputs"]["custom_block"][1])
    CODE = main.processBlock(blockData["next"], True)
    return f'{CUSTOM}\n{CODE}\nend'

def procedures_prototype(_, blockData):
    ARGS = []
    proccode = main.sanitizeVar(blockData["mutation"]["proccode"])
    for inputList in list(blockData["inputs"].keys()):
        ARGS.append(main.sanitizeVar(main.processBlock(blockData["inputs"][inputList][1])))
    outVar = ""
    for i in range(len(ARGS)):
        if i == len(ARGS)-1:
            outVar += ARGS[i]
        else:
            outVar += f'{ARGS[i]},'
    return f'function {proccode}({outVar})'

def argument_reporter_string_number(_, blockData):
    VALUE = main.sanitizeVar(blockData["fields"]["VALUE"][0])
    return f"arg__{VALUE}"

def argument_reporter_boolean(_, blockData):
    VALUE = main.sanitizeVar(blockData["fields"]["VALUE"][0])
    return f"arg__{VALUE}"

def procedures_call(_, blockData):
    ARGS = []
    proccode = main.sanitizeVar(blockData["mutation"]["proccode"])
    for inputList in list(blockData["inputs"].keys()):
        arg = blockData["inputs"][inputList]

        if isinstance(arg[1], list): # num/string
            ARGS.append(main.getInputVar(arg))
        else:
            ARGS.append(main.processBlock(arg[1]))

    outVar = ""
    for i in range(len(ARGS)):
        if i == len(ARGS)-1:
            outVar += ARGS[i]
        else:
            outVar += f'{ARGS[i]},'
    return f'{proccode}({outVar})'