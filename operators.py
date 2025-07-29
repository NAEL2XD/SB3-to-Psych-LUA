import main

def noneTo0(input):
    return 0 if input == '""' else input

def operator_equals(_, blockData):
    OPERAND1 = noneTo0(main.getInputVar(blockData["inputs"]["OPERAND1"]))
    OPERAND2 = noneTo0(main.getInputVar(blockData["inputs"]["OPERAND2"]))
    return f'({OPERAND1} == {OPERAND2})'

def operator_and(_, blockData):
    OPERAND1 = noneTo0(main.getInputVar(blockData["inputs"]["OPERAND1"]))
    OPERAND2 = noneTo0(main.getInputVar(blockData["inputs"]["OPERAND2"]))
    return f'({OPERAND1} and {OPERAND2})'

def operator_gt(_, blockData):
    OPERAND1 = noneTo0(main.getInputVar(blockData["inputs"]["OPERAND1"]))
    OPERAND2 = noneTo0(main.getInputVar(blockData["inputs"]["OPERAND2"]))
    return f'({OPERAND1} > {OPERAND2})'

def operator_lt(_, blockData):
    OPERAND1 = noneTo0(main.getInputVar(blockData["inputs"]["OPERAND1"]))
    OPERAND2 = noneTo0(main.getInputVar(blockData["inputs"]["OPERAND2"]))
    return f'({OPERAND1} < {OPERAND2})'

def operator_or(_, blockData):
    OPERAND1 = noneTo0(main.getInputVar(blockData["inputs"]["OPERAND1"]))
    OPERAND2 = noneTo0(main.getInputVar(blockData["inputs"]["OPERAND2"]))
    return f'({OPERAND1} or {OPERAND2})'

def operator_not(_, blockData):
    OPTION = main.processBlock(blockData["inputs"]["OPERAND"][1])
    return f'(not {OPTION})'

def operator_add(_, blockData):
    NUM1 = noneTo0(main.getInputVar(blockData["inputs"]["NUM1"]))
    NUM2 = noneTo0(main.getInputVar(blockData["inputs"]["NUM2"]))
    return f'({NUM1} + {NUM2})'

def operator_subtract(_, blockData):
    NUM1 = noneTo0(main.getInputVar(blockData["inputs"]["NUM1"]))
    NUM2 = noneTo0(main.getInputVar(blockData["inputs"]["NUM2"]))
    return f'({NUM1} - {NUM2})'

def operator_multiply(_, blockData):
    NUM1 = noneTo0(main.getInputVar(blockData["inputs"]["NUM1"]))
    NUM2 = noneTo0(main.getInputVar(blockData["inputs"]["NUM2"]))
    return f'({NUM1} * {NUM2})'

def operator_divide(_, blockData):
    NUM1 = noneTo0(main.getInputVar(blockData["inputs"]["NUM1"]))
    NUM2 = noneTo0(main.getInputVar(blockData["inputs"]["NUM2"]))
    return f'({NUM1} / {NUM2})'

def operator_random(_, blockData):
    FROM = str(noneTo0(main.getInputVar(blockData["inputs"]["FROM"])))
    TO   = str(noneTo0(main.getInputVar(blockData["inputs"]["TO"])))
    TYPEOF = "Int"

    if (FROM.find(".") != -1 or TO.find(".") != -1) or (FROM.find("(") != -1 or TO.find("(") != -1):
        TYPEOF = "Float"

    return f'getRandom{TYPEOF}({FROM}, {TO})'

def operator_join(_, blockData):
    STRING1 = noneTo0(main.getInputVar(blockData["inputs"]["STRING1"]))
    STRING2 = noneTo0(main.getInputVar(blockData["inputs"]["STRING2"]))
    return f'({STRING1} .. {STRING2})'

def operator_letter_of(_, blockData):
    LETTER = noneTo0(main.getInputVar(blockData["inputs"]["LETTER"]))
    STRING = noneTo0(main.getInputVar(blockData["inputs"]["STRING"]))
    return f'string.sub({STRING}, {LETTER}, {LETTER})'

def operator_length(_, blockData):
    STRING = noneTo0(main.getInputVar(blockData["inputs"]["STRING"]))
    return f'#tostring({STRING})'

def operator_contains(_, blockData):
    STRING1 = noneTo0(main.getInputVar(blockData["inputs"]["STRING1"]))
    STRING2 = noneTo0(main.getInputVar(blockData["inputs"]["STRING2"]))
    return f'string.find({STRING1}, {STRING2})'

def operator_mod(_, blockData):
    NUM1 = noneTo0(main.getInputVar(blockData["inputs"]["NUM1"]))
    NUM2 = noneTo0(main.getInputVar(blockData["inputs"]["NUM2"]))
    return f'({NUM1} % {NUM2})'

def operator_round(_, blockData):
    NUM = noneTo0(main.getInputVar(blockData["inputs"]["NUM"]))
    return f'math.floor({NUM} + 0.5)'

def operator_mathop(_, blockData):
    NUM = noneTo0(main.getInputVar(blockData["inputs"]["NUM"]))
    OPE = blockData["fields"]["OPERATOR"][0]

    mathType = [
        ["acos",    "math.acos"],
        ["atan",    "math.atan"],
        ["ln",      "math.log"],
        ["log",     "math.log10"],
        ["e ^",     "math.exp"],
        ["10 ^",    "10^", True],
        ["abs",     "math.abs"],
        ["floor",   "math.floor"],
        ["ceiling", "math.ceil"],
        ["sqrt",    "math.sqrt"],
        ["sin",     "math.sin"],
        ["cos",     "math.cos"],
        ["tan",     "math.tan"],
        ["asin",    "math.asin"]
    ]

    i = 0
    for mt in mathType:
        if OPE == mt[0]:
            OPE = mt[1]
            break
        i += 1

    return f'{OPE}({NUM})' if len(mathType[i]) == 2 else f'{OPE}{NUM}'