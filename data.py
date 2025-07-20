import main

def data_setvariableto(spriteName, blockData):
    VALUE = main.getInputVar(blockData["inputs"]["VALUE"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["VARIABLE"][0])
    spriteName = main.sanitizeVar(spriteName)
    return f'{spriteName}_vars.{VARIABLE}_v = {VALUE}'

def data_changevariableby(spriteName, blockData):
    VALUE = main.getInputVar(blockData["inputs"]["VALUE"])
    VARIABLE = main.sanitizeVar(blockData["fields"]["VARIABLE"][0])
    spriteName = main.sanitizeVar(spriteName)
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