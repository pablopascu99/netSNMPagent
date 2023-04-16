#Send Traps

##Version 2c
Open console for *agente* and execute command **snmptrap**.

###Examples
``
snmptrap -v 2c -c public 127.0.0.1 '' SNMPv2-MIB::coldStart
``

``
snmptrap -v 2c -c public 127.0.0.1 '' IF-MIB::linkDown IF-MIB::ifIndex.1 i 1
``