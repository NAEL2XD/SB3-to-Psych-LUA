import main

def control_wait(_, blockData):
    DURATION = main.getInputVar(blockData["inputs"]["DURATION"])
    return f'wait({DURATION})'

def control_repeat(_, blockData):
    TIMES = main.getInputVar(blockData["inputs"]["TIMES"])
    SUBSTACK = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    return f'for _=1,{TIMES} do\n{SUBSTACK}\nend'

def control_forever(_, blockData):
    SUBSTACK = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    return f'function onUpdate(__)\n{SUBSTACK}\nend'

def control_if(_, blockData):
    COND = main.processBlock(blockData["inputs"]["CONDITION"][1], True)
    SUBS = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    return f'if {COND} then\n{SUBS}\nend'

def control_if_else(_, blockData):
    COND = main.processBlock(blockData["inputs"]["CONDITION"][1], True)
    SUBS1 = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    SUBS2 = main.processBlock(blockData["inputs"]["SUBSTACK2"][1], True)
    return f'if {COND} then\n{SUBS1}\nelse\n{SUBS2}\nend'

def control_wait_until(_, blockData):
    COND = main.processBlock(blockData["inputs"]["CONDITION"][1], True)
    return f'repeat until {COND}'

def control_repeat_until(_, blockData):
    SUBS = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    COND = main.processBlock(blockData["inputs"]["CONDITION"][1], True)
    return f'repeat\n{SUBS}\nuntil {COND}'

def control_while(_, blockData):
    SUBS = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    COND = main.processBlock(blockData["inputs"]["CONDITION"][1], True)
    return f'while {COND} do\n{SUBS}\nend'

def control_stop(_, blockData):
    OPTION = blockData["fields"]["STOP_OPTION"][0]
    return f'return --[[TYPEOF {OPTION}]]'