import subprocess
import time

def pipeline1():
    # Ejecutar el archivo .exe
    time.sleep(5)
    subprocess.call(["snmptrap", "-v", "2c", "-c", "public", "127.0.0.1" ,"''", "SNMPv2-MIB::coldStart"])
    time.sleep(5)
    subprocess.call(["snmptrap", "-v", "2c", "-c", "public", "127.0.0.1" ,"''", "IF-MIB::linkDown", "IF-MIB::ifIndex.1", "i", "1",
                    "IF-MIB::ifDescr.1","s",'"eth0"',"IF-MIB::ifType.1","i","6"])

def main():
    pipeline1()
    print("SALIDA")

main()