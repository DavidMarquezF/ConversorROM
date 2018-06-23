==============
Customització
==============

Per customitzar/afegir comandes noves (com SUBI, etc.), cal que aneu al mòdul ROMtoVHDL i a la variable global Opcions
afegir un nou item al diccionari (key: nom comanda, value: la funció que analitza aquella instrucció). Cal tenir present que
el value ha de ser una referència a la funció i no una crida (tal com es pot veure en totes les altres).

Per analitar el hex/registre si la comanda en questió en conté, ja hi ha funcions que s'encarreguen de passar del hex a binari i del registre
a binari (analizeRegister i analizeHex).

La vostra funció que analitza ha de tenir dun paràmetre. Aquest equival a els paràmetres que t'han passat en forma de string. És a dir que si
per exemple et criden::

LDI r16,x01

Es cridaria la funció passant-li el paràmetre "r16,x01".

Un cop això ja està creat ja no heu de fer res, ja que el programa se n'encarrega de la resta.


Hi ha variables amb strings que podeu variar depenent de com heu fet el VHDL. Per exemple la variable Program_Counter
hi té assignat "pr_pc", però si l'hi heu posat un altre nom canvieu la string i ja es printejarà d'aquesta manera.