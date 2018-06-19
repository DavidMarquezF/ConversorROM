#!/usr/bin/env python
#-*- coding: utf-8 -*-
from MainLib import *
import os

ORIGINAL = "Partitura.txt"
ROM = "ROM.txt"
VHDL = "VHDL.txt"


def checkFilesExist(fol):
    """
    Chequeja si el directori fol conté els fitxers necessaris

    :param fol: El directori que s'ha de comprobar si té els fitxers o no
    :return: True si conté els fitxers necessàris i False si no
    """
    return (os.path.isfile(fol + "/" + ROM) and os.path.isfile(fol + "/" + VHDL) and os.path.isfile(fol + "/" + ORIGINAL))

def prepareFiles(folderName, createDir =True):
    """
    Crea els fitxers necessàris en un directori, que, si no existeix, també es crea

    :param folderName: El nom del directori
    :param createDir: Si s'ha de crear o no un directori
    """
    if(createDir):
        os.makedirs(folderName)
    open(folderName +"/" + ROM, "w").close()
    open(folderName + "/" + VHDL, "w").close()
    open(folderName + "/" + ORIGINAL, "w").close()


def createUseFolder():
    """
    S'utilitza per guardar dades (crear el directori i fitxers, utilitzar-ne de ja existents, etc.)

    :return: El nom del directori on s'han guardat
    """
    while True:
        fol = raw_input("Esculli un directori on hi té/vol la informació: ")
        if(not os.path.exists(fol)):
            logInfo("Creació fitxers", "Aquestes dades no exiteixen")
            logInfo("Creació fitxers", "Creant el directori i fitxers necessaris")
            prepareFiles(fol)
            logSuccess("Creació de fitxers completada!")
            logInfo("Ajuda", "Ara has d'editar el fitxer {0} on hi has d'escriure la teva partitura".format(ORIGINAL))
            return [fol, False]
        else:
            if(not checkFilesExist(fol)):
                logInfo("Creació fitxers", "Aquest directori no conte els fitxers necessaris. Creant els fitxers...")
                prepareFiles(fol, False)
                logSuccess("Creació de fitxers completada!")
                return [fol,False]
            return [fol,True]

def checkIfTypeExists(type):
    """
    Chequeja si el nom del fitxer és un dels existents en el mòdul

    :param type: El nom del fitxer
    :return: True si existeix i False si no
    """
    return type == ROM or type == VHDL or type == ORIGINAL

def writeToFile(folderName, type, txt):
    """
    Escriu al fitxer type dins de folderName el text (lines)

    :param folderName: El nom del directori que conté els fitxers adeqüats
    :param type: El nom del fitxer que es vol accedir
    :param lines: El text que se li vol  posar
    :return: False si no s'ha pogut realitzar correctament i True si s'ha pogut fer tot correctament
    """
    if not checkIfTypeExists(type):
        warning("El fitxer {0} no existeix".format(type))
        return False

    try:
        f = open(folderName+"/"+type,"w")
    except IOError as e:
        exception("Error al obrir el fitxer {0} : {1}".format(type,e.message))
        return False
    except Exception as e:
        exception("Error al obrir el fitxer {0} : {1}".format(type, e.message))
        return False

    f.write(txt)
    f.close()
    return True

def readlines(folderName, type):
    """
    Llegeix el fitxer type dins de folderName

    :param folderName: El nom del directori que conté els fitxers adeqüats
    :param type: El nom del fitxer que es vol accedir
    :return: False si no s'ha pogut fer amb èxit i la llista de línies si si que s'ha pogut
    """
    if not checkIfTypeExists(type):
        exception("El fitxer {0} no existeix".format(type))
        return False
    try:
        f = open(folderName + "/" + type)
    except IOError as e:
        exception("Error al obrir el fitxer {0} : {1}".format(type, e.message))
        return False
    except Exception as e:
        exception("Error al obrir el fitxer {0} : {1}".format(type, e.message))
        return False

    l = f.readlines()
    l = [value for value in l if value != "\n"]
    for line in range(len(l)):
        l[line] = l[line].rstrip("\n")
    f.close()
    return l
def askYorNQuestion(question):
    """
    Pregunta una pregunta de sí o no.

    :param question: La pregunta que es vol fer a l'usuari
    :return: True o False depenent del que ha triat l'usuari
    """
    while (True):
        answerUser = raw_input(question + "(Y/N) ")
        if (answerUser == "N" or answerUser == "n"):
            return False
        if (answerUser == "Y" or answerUser == "y"):
            return True