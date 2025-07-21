import main

def control_wait(_, blockData):
    try: DURATION = main.getInputVar(blockData["inputs"]["DURATION"])
    except: DURATION = "0"
    return f'wait({DURATION})'

def control_repeat(_, blockData):
    try: TIMES = main.getInputVar(blockData["inputs"]["TIMES"])
    except: TIMES = "1"
    try: SUBSTACK = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    except: SUBSTACK = ""
    return f'for _=1,{TIMES} do\n{SUBSTACK}\nend'

def control_forever(_, blockData):
    try: SUBSTACK = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    except: SUBSTACK = ""
    return f'function onUpdate(__)\n{SUBSTACK}\nend'

def control_if(_, blockData):
    try: COND = main.processBlock(blockData["inputs"]["CONDITION"][1], True)
    except: COND = "false"
    try: SUBS = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    except: SUBS = ""
    return f'if {COND} then\n{SUBS}\nend'

def control_if_else(_, blockData):
    try: COND = main.processBlock(blockData["inputs"]["CONDITION"][1], True)
    except: COND = "false"
    try: SUBS1 = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    except: SUBS1 = ""
    try: SUBS2 = main.processBlock(blockData["inputs"]["SUBSTACK2"][1], True)
    except: SUBS2 = ""
    return f'if {COND} then\n{SUBS1}\nelse\n{SUBS2}\nend'

def control_wait_until(_, blockData):
    try: COND = main.processBlock(blockData["inputs"]["CONDITION"][1], True)
    except: COND = "false"
    return f'repeat until {COND}'

def control_repeat_until(_, blockData):
    try: SUBS = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    except: SUBS = ""
    try: COND = main.processBlock(blockData["inputs"]["CONDITION"][1], True)
    except: COND = "false"
    return f'repeat\n{SUBS}\nuntil {COND}'

def control_while(_, blockData):
    try: SUBS = main.processBlock(blockData["inputs"]["SUBSTACK"][1], True)
    except: SUBS = ""
    try: COND = main.processBlock(blockData["inputs"]["CONDITION"][1], True)
    except: COND = "false"
    return f'while {COND} do\n{SUBS}\nend'

def control_stop(_, blockData):
    OPTION = blockData["fields"]["STOP_OPTION"][0]
    return f'return --[[TYPEOF {OPTION}]]'