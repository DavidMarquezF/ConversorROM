#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys

import PartituraToROM
import ROMtoVHDL
import ReadWriteFiles


def getVhdl():
    """
    S'encarrega de crear un directori amb els fitxers necessàris a dins. Si ja hi és fa les conversions Partitura-ROM-VHDL
    """
    fol= ReadWriteFiles.createUseFolder()
    if(not fol[1]):
        return
    fol = fol[0]
    rom = PartituraToROM.linesToROM(fol)
    ReadWriteFiles.writeToFile(fol, ReadWriteFiles.ROM, rom)

    vhdl = ROMtoVHDL.getCodeFromFolder(fol)
    ReadWriteFiles.writeToFile(fol, ReadWriteFiles.VHDL, vhdl)









if (__name__ == "__main__"):
    getVhdl()
