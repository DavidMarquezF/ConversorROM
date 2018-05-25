#!/usr/bin/env python
#-*- coding: utf-8 -*-

def exception(message, LineProgram=None, place=None, exitProgram = True):
    """
    Printeja una excepció i fa exit si cal

    :param message: El missatge a printejar
    :param LineProgram: La línia on el programa ha fallat (opcional)
    :param place: El lloc/fitxer on el programa ha fallat (opcional)
    :param exitProgram: Sortir del programa després de fer l'excepció, de default està a True
    """
    print "\033[01;31mError\033[00m{0}{1} - {2}".format((" a " + place) if place != None else "",
                                                          (" a la línia " + str(LineProgram)) if LineProgram != None else"", message)
    if exitProgram:
        exit()

def warning(message, LineProgram=None, place=None):
    """
    Printeja una warning

    :param message: El missatge a printejar
    :param LineProgram: La línia on el programa té un warning (opcional)
    :param place: El lloc/fitxer on el programa té un warning (opcional)

    """
    print "\033[93m;31mError\033[00m{0}{1} - {2}".format((" a " + place) if place != None else "",
                                                        (" a la línia " + str(
                                                            LineProgram)) if LineProgram != None else"", message)


def logInfo(TAG, message):
    """
    Mostra info per la pantalla

    :param TAG: La tag relacionada al missatge
    :param message: El missatge a printejar
    """
    print "AVR Log: {0} - {1}".format(TAG, message)

def logSuccess(message):
    """
    Printeja de color verd el text que se li passa

    :param message: El missatge que es vol printejar
    """
    print "\033[92mÈxit - {0}\033[0m".format(message)
