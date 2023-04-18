import subprocess
import time

# Ejecutar el archivo .exe
time.sleep(5)
subprocess.call(["snmptrap", "-v", "2c", "-c", "public", "127.0.0.1" ,"''", "SNMPv2-MIB::coldStart"])
# subprocess.call(["snmptrap", "-v", "2c", "-c", "public", "127.0.0.1" ,"''", "SNMPv2-MIB::coldStart"])
time.sleep(5)
# subprocess.call(["snmptrap", "-v", "2c", "-c", "public", "127.0.0.1" ,"''", "IF-MIB::linkDown", "IF-MIB::ifIndex.1", "i", "1"])
subprocess.call(["snmptrap", "-v", "2c", "-c", "public", "127.0.0.1" ,"''", "IF-MIB::linkDown", "IF-MIB::ifIndex.1", "i", "1",
                 "IF-MIB::ifDescr.1","s",'"eth0"',"IF-MIB::ifType.1","i","6"])

# output = subprocess.run([ruta_exe, "-v:1", "-c:public", "-r:172.16.239.20", "-to:1.3.6.1.6.3.1.1.4.1.0", "-del:''", "-eo:1.3.6.1.4.1.8072.3.2.10", "-vid:1.3.6.1.6.3.1.1.5.1", "-vtp:str", "-val:'1'", "-p:162"], stdout=subprocess.PIPE)
# Decodificar la salida y mostrarla por pantalla
# print(output.stdout)
#  Imprimir la salida
print("SALIDA")