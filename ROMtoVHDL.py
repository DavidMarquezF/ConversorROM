#!/usr/bin/env python
#-*- coding: utf-8 -*-
import ReadWriteFiles
from MainLib import *

ROMout ="pr_op"
ProgramCounter="pr_pc"

LineProgram=0

startText = "ROM : process ({0}) is\nbegin\n\tcase {1} is\n".format(ProgramCounter, ProgramCounter)
endText = "\twhen others => {0} <= (others => '-');\n\tend case;\nend process;".format(ROMout)

INPorts=[0,1,2]
OUTPorts=[8,9,10]

startRegisterNum=16
endRegisterNum=32

def readFile(folder):
    """
    Llegeix el fitxer dins del directori

    :param folder: Directori on hi ha el fitxer ROM
    :return: El txt amb tot el text
    """
    l = ReadWriteFiles.readlines(folder, ReadWriteFiles.ROM)
    return l if l != False else exit()

def getCodeFromFolder(folder):
    """
    Funció principal. Obté el VHDL del fitxer ROM que està dins del directori

    :param folder: El directori on hi ha els fitxers requerits
    :return: El txt amb tot el codi VHDL
    """
    lines = readFile(folder)
    return getCode(lines)

def getCodeFromFile(file):
    """
    Funció principal. Obté el VHDL del fitxer especificat

    :param file: Nom del fitxer d'on s'ha d'obtenir les dades
    :return: El txt amb tot el codi VHDL
    """
    try:
        f = open(file)
        l = [value.rstrip("\n") for value in f.readlines() if value != "\n"]
        f.close()
    except IOError:
        exception("El fitxer {0} no existeix".format(file))
    return getCode(l)

def getCode(lines):
    """
    Obté el codi vhdl a partir d'una llista de línies escrites en ROM

    :param lines: Llista de línies escrites en format ROM
    :return: El txt de VHDL resultant
    """
    logInfo("ROM-VHDL", "Iniciant conversió de ROM a VHDL")

    txt=startText
    counter=0

    global LineProgram
    try:
        for line in lines:
            txt +='\twhen x"{:02x}" =>\n'.format(counter)
            li = line.split()
            txt += "\t\t{0} <= {1};\n".format(ROMout, Options[li[0]]("" if li[0] == "NOP" else li[1]))
            counter+=1
            LineProgram+=1
        txt += endText
    except KeyError:
        exception("Clau no correcta", LineProgram, ReadWriteFiles.ROM)
    except Exception as e:
        exception(e.message, LineProgram, ReadWriteFiles.ROM)

    logSuccess("Conversió de ROM a VHDL s'ha fet correctament")
    return txt

def analyzeRegister(registerStr):
    """
    Analitza si el registre està en el format correcte i és el que toca. El format hauría de ser de tipus r16

    :param registerStr: La string del registre
    :return: El registre passat a bits
    """
    try:
        if not registerStr.startswith("r"):
            raise Exception("El format del registre {0} no és valid ".format(registerStr))

        if not (startRegisterNum <= int(registerStr[1:]) <= endRegisterNum):
            raise ValueError()
    except ValueError:
        exception("El registre ha d'estar entre {0} and {1}".format(startRegisterNum, endRegisterNum), LineProgram, ReadWriteFiles.ROM)
    except Exception as e:
        exception(e.message, LineProgram, ReadWriteFiles.ROM)

    return  "{0:b}".format(int(registerStr[1:])).zfill(4)[1:]

def analyzeHex(hex,n=8):
    """
    Analitza si el valor és hexadecimal

    :param hex: La string de l'hexadecimal. S'hauria d'esciure en format x12
    :param n: El nombre de bits que ha de tenir la string retornada
    :return: El valor hexadecimal passat a bits de llargada n

    >>> analyzeHex("x1")
    '00000001'
    >>> analyzeHex("x2", 4)
    '0010'
    """
    try:
        hexVal = hex.replace("x","")
        return bin(int(hexVal, 16))[2:].zfill(n)[:n]
    except ValueError:
        exception("El registre {0} no està en el format correcte".format(hex))


def analyzeNOP(line):
    """
    Analitza la NOP

    :param line: paràmetre que en aquest cas és inútil, però necessàri perquè cridem tots els analize amb un paràmetre
    :return: Retorna la comanda passada a VHDL
    """
    return 'NOP & "0000" & "--------"'

def analyzeLDI(params):
    """
    Analitza el LDI

    :param params: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """
    p = params.split(",")
    if len(p) != 2:
        exception("LDI només té 2 paràmetres", LineProgram, ReadWriteFiles.ROM)

    register = analyzeRegister(p[0])
    hex = analyzeHex(p[1])
    return 'LDI & "{0}" & "{1}" & "{2}"'.format(hex[:4], register, hex[4:8])

def analyzeADC(params):
    """
    Analitza el ADC

    :param params: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """
    p = params.split(",")
    if len(p) != 2:
        exception("ADC has only 2 params", LineProgram, ReadWriteFiles.ROM)
    registre1=analyzeRegister(p[0])
    registre2=analyzeRegister(p[1])
    return 'ADC & "1111" & "{0}" & "{1}"'.format(registre1,registre2)

def analizeALU_B(parametres, type):
    """
    Analitza l'ALU_B

    :param parametres: Paràmetres que ens passa l'usuari
    :param type: El tipus de ALU_B (recordar que  hi havia MOV, AND, EOR...)
    :return: Retorna la comanda passada a VHDL
    """

    p = parametres.split(",")
    if len(p) != 2:
        exception("{0} només té 2 paràmetres".format(type), LineProgram, ReadWriteFiles.ROM)
    registre1 = analyzeRegister(p[0])
    registre2 = analyzeRegister(p[1])
    return 'ALU_B & {0} & "00" & "{1}" & "{2}"'.format(type, registre1, registre2)

def analizeRJMP(params):
    """
    Analitza RJMP

    :param params: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """
    try:
        if len(params.split(",")) != 1:
            raise Exception("RJMP només té 1 paràmetre")

        jump = bin(int(params) % (1 << 12))[2:].zfill(12)
        return 'RJMP & "----" & "{0}" & "{1}"'.format(jump[4:8],jump[8:])
    except Exception as e:
        exception(e.message, LineProgram, ReadWriteFiles.ROM)

def analizeBREQ(params):
    """
    Analitza el BREQ

    :param params: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """
    try:
        if len(params.split(",")) != 1:
            raise Exception("BREQ només té 1 paràmetre")
        jump=bin(int(params)%(1<<7))[2:].zfill(7)
        return 'BRANCH & "00{0}" & "{1}" & "{2}001"'.format(jump[:2], jump[2:6], jump[6])

    except Exception as e:
        exception(e.message, LineProgram, ReadWriteFiles.ROM)


def analizeBRNE(params):
    """
    Analitza el BRNE

    :param params: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """
    try:
        if len(params.split(",")) != 1:
            raise Exception("BRNE només té 1 paràmetre")
        jump=bin(int(params)%(1<<7))[2:].zfill(7)
        return 'BRANCH & "01{0}" & "{1}" & "{2}001"'.format(jump[:2], jump[2:6], jump[6])

    except Exception as e:
        exception(e.message, LineProgram, ReadWriteFiles.ROM)

def analizeMOV(parametres):
    """
    Analitza el MOV

    :param parameters: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """
    return analizeALU_B(parametres, "ALU_B_MOV")

def analizeAND(parametres):
    """
    Analitza AND

    :param parameters: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """
    return analizeALU_B(parametres, "ALU_B_AND")

def analizeOR(parametres):
    """
    Analitza OR

    :param parameters: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """
    return analizeALU_B(parametres, "ALU_B_OR")

def analizeEOR(parametres):
    """
    Analitza EOR

    :param parameters: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """
    return analizeALU_B(parametres, "ALU_B_EOR")

def analizeINOUT(params,out):
    """
    Analitza INOUT

    :param parameters: Paràmetres que ens passa l'usuari
    :param out: Boleà que indica si és  in o out
    :return: Retorna la comanda passada a VHDL
    """
    try:
        p = params.split(",")
        if (len(p) != 2):
            raise Exception("INOUT només té 2 paràmetres")
        if (out):
            p = p[::-1]
        registre = analyzeRegister(p[0])
        valor = int(p[1])

        if (not out and valor not in INPorts):
            raise Exception("In només pot ser {0}".format(", ".join(INPorts)))
        elif out and valor not in OUTPorts:
            raise Exception("Out només pot ser {0}".format(", ".join(OUTPorts)))

    except ValueError:
        exception("INOUT valor ha de ser un nombre decimal", LineProgram, ReadWriteFiles.ROM)
    except Exception as e:
        exception(e.message, LineProgram, ReadWriteFiles.ROM)

    return 'IN_OUT & "{0}000" & "{1}" & "{2}"'.format(1 if out else 0, registre, bin(int(valor))[2:].zfill(4))

def analizeIN(params):
    """
    Analitza IN

    :param params: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """

    return analizeINOUT(params, False)

def analizeOUT(params):
    """
    Analitza OUT

    :param parameters: Paràmetres que ens passa l'usuari
    :return: Retorna la comanda passada a VHDL
    """
    return analizeINOUT(params, True)

def analizeORI(params):
    p = params.split(",")
    if len(p) != 2:
        exception("ORI només té 2 paràmetres", LineProgram, ReadWriteFiles.ROM)

    register = analyzeRegister(p[0])
    hex = analyzeHex(p[1])
    return 'ORI & "{0}" & "{1}" & "{2}"'.format(hex[:4], register, hex[4:8])

def analizeANDI(params):
    p = params.split(",")
    if len(p) != 2:
        exception("ANDI només té 2 paràmetres", LineProgram, ReadWriteFiles.ROM)

    register = analyzeRegister(p[0])
    hex = analyzeHex(p[1])
    return 'ANDI & "{0}" & "{1}" & "{2}"'.format(hex[:4], register, hex[4:8])


Options ={                  #Llista de les opciona a analitzar.
    "NOP" : analyzeNOP,
    "LDI" : analyzeLDI,
    "ADC" : analyzeADC,
    "MOV" : analizeMOV,
    "RJMP" :analizeRJMP,
    "BREQ": analizeBREQ,
    "BRNE": analizeBRNE,
    "IN" : analizeIN,
    "OUT": analizeOUT,
    "EOR": analizeEOR,
    "AND": analizeAND,
    "OR" : analizeOR,
    "ORI" : analizeORI,
    "ANDI":analizeANDI
}


if (__name__ == "__main__"):
    print getCodeFromFile(raw_input("Escriu el nom del fitxer on hi tens el codi: "))