#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
==================
Creador de cicles
==================

Aquest mòdul s'encarrega de printejar els cicles que es necessiten per generar les freqüències necessàries per fer
sonar les notes. Amb aquest sistema es pot arribar a generar totes les freqüències necessàries.

Els cicles són iguals que els que es poden veure en el fitxer penjat a Atenea, però us estalvieu copiar-los i a més a més
tindreu totes les notes que volgueu.
"""
variableCiclesNecessaris="ciclesNeed"
liniaDefault = "\tto_unsigned({0}, {1}'length) when {2},"


def cicles(midi):
    """
    Calcula els cicles necessàris per fer sonar la nota amb la clau midi

    :param midi: Clau midi
    :return: Nombre de cicles necessàris
    """
    return int(round(1000000 / (880 * (2**(1/12.0))**(midi - 69))))

def creacicles():
    """
    Printeja els cicles necessàris de la nota midi 0 a la 127 (es pot ampliar tant com sigui necessàri)
    """
    midi = dict()
    for nota in range(0, 127):
        midi[str(nota)] = cicles(nota)

    print "{0} <= ".format(variableCiclesNecessaris)
    for key, value in midi.items():
        print liniaDefault.format(value, variableCiclesNecessaris, key)

if __name__ == "__main__":
    creacicles()

