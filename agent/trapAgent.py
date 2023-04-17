import subprocess

# Ejecutar el archivo .exe
subprocess.call(["snmptrap", "-v", "2c", "-c", "public", "127.0.0.1" ,"''", "SNMPv2-MIB::coldStart"])
# output = subprocess.run([ruta_exe, "-v:1", "-c:public", "-r:172.16.239.20", "-to:1.3.6.1.6.3.1.1.4.1.0", "-del:''", "-eo:1.3.6.1.4.1.8072.3.2.10", "-vid:1.3.6.1.6.3.1.1.5.1", "-vtp:str", "-val:'1'", "-p:162"], stdout=subprocess.PIPE)
# Decodificar la salida y mostrarla por pantalla
# print(output.stdout)
#  Imprimir la salida
print("SALIDA")