============
ConversorROM
============

Projecte per facilitar la programació de la pràctica del miniAVR. 

S'encarrega de generar VHDL a partir de ROM, VHDL a partir de partitures i a generar els cicles necessàris per fer les notes midi.

Customització
--------------

Afegir comandes noves és extremadament fàcil, i ho podreu fer al fitxer ROMToVHDL. Està explicat en l'apartat de Customització.

https://davidmarquezf.github.io/ConversorROM/Customitzacio.html

Creador de cicles
------------------

En aquest projecte també hi incloim un creador de cicles necessàris per la primera part de la pràctica, que consiteix en crear els sintetizadors.

Bàsicament us facilitarà la vida perquè no ho haureu de copiar a mà i tindreu totes les notes fetes

Com funciona?
=================

Per fer la conversió de partitures s'ha de fer cridant la comanda::

    python VHDLdePartitura.py

Es podria convertir en un executable molt fàcilment però no ho hem trobat necessàri.

Es demanarà que s'esculli un directori a on guardar la info. Poseu el nom que trobeu convenient.
Donarà informació i us crearà el directori. Si tot ha anat bé us hauria de sortir un text verd que ho confirma.

Haurieu de tenir el directori creat. Ara cal modificar el fitxer Partitura.txt. A dins escriviu la partitura d'aquesta manera::

    Nota1 Nota2 Nota3 temps

Està més ben explicat a la documentació en l'apartat de PartituraToROM.

Un cop heu fet la partitura, cal que torneu a executar el fitxer python VHDLdePartitura un altre cop i quan us demani el directori
posar-li el que hi teniu la partitura.

Si tot va bé, ja haurieu de tenir el fitxer ROM i el fitxer VHDL amb el codi corresponent.
Si no funciona, els errors mostrats per pantalla us haurien de guiar a arreglar el codi que hagueu fet.


Cal tenir en compte
====================

Holi


==============================
Documentació de les classes
==============================

Tota la documentació i informació necessària la podreu trobar en aquest link (github pages):

https://davidmarquezf.github.io/ConversorROM/

Per si algu li interessa saber com crear la pàgina web de sphinx i penjar-la a GitHub com la que utilitzem, en aquest link
s'explica molt bé: https://daler.github.io/sphinxdoc-test/includeme.html

Autors
============

Irene Mollet i David Márquez