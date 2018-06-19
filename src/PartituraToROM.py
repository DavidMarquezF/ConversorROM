#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ReadWriteFiles
from MainLib import exception

Notes = {
    "C":12,
    "C#":13,
    "Db":13,
    "D":14,
    "D#":15,
    "Eb":15,
    "E":16,
    "E#":17,
    "Fb":16,
    "F":17,
    "F#":18,
    "Gb":18,
    "G":19,
    "G#":20,
    "Ab":20,
    "A":21,
    "A#":22,
    "Bb":22,
    "B":23,
    "B#":24
}
LineProgram=0

def readFile(folder):
    """
    Llegeix el fitxer dins del directori

    :param folder: Directori on hi ha el fitxer ROM
    :return: El txt amb tot el text
    """
    l = ReadWriteFiles.readlines(folder, ReadWriteFiles.ORIGINAL)
    return [line.split() for line in l] if l != False else exit()

def getMidi(note):
    """
    Calcula el valor midi a partir de la nota escrita

    :param note: La string de la nota, que està en format C1,B3, Bb1, G#
    :return: El int de la clau midi
    """
    try:
        p = int(note[-1])
        midiNote = Notes[note[:-1]]
        return midiNote + 12 *p
    except Exception:
        exception("Error convertint la nota " + note, LineProgram, ReadWriteFiles.ORIGINAL)

def convertMidis(lines):
    """
    Convertiex els midis: A partir de la llista amb les línies de la partitura passa les notes a midi

    :param lines: Les línies de la partitura dividides en notes
    :return: Les línies de la partitura dividides en claus midi
    """
    global LineProgram
    try:
        for line in lines:
            for note in range(len(line) - 1):
                if line[note] != "0":
                    line[note] = hex(getMidi(line[note]) + 128)[1:]
                else:
                    line[note] = hex(0)[1:]
            LineProgram+=1
    except ValueError:
        exception("Error al convertir de nota a midi", LineProgram, ReadWriteFiles.ORIGINAL)

    LineProgram=0
    return lines

def linesToROM(folder):
    """
    Fa la conversió a partir del directori on hi ha la partitura a ROM

    :param folder: El directori on hi ha els fitxer de Partitura i ROM
    :return: Retorna el text de ROM
    """
    global LineProgram
    lines = readFile(folder)
    convertMidis(lines)
    ROM = []
    ROM.append("NOP")
    ROM.append("LDI r{0},{1}".format(22, hex(0)[1:]))
    try:
        for line in lines:
            registre = 16
            for note in range(len(line)-1):
                ROM.append("LDI r{0},{1}".format(registre,line[note]))
                registre+=1
            ROM.append("LDI r{0},{1}".format(20,hex(int(line[-1]))))
            ROM.append("OUT {0},r{1}".format(10, 20))
            ROM.append("IN r{0},{1}".format(21, 2))
            ROM.append("EOR r{0},r{1}".format(21, 22))
            ROM.append("BRNE -3")
            LineProgram+=1
        ROM.append("RJMP -1")
    except ValueError:
        exception("Error convertint la octava(nombre) a int", LineProgram, ReadWriteFiles.ORIGINAL)

    return "\n".join(ROM)

















if (__name__ == "__main__"):
    pass