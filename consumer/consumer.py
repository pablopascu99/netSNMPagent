from confluent_kafka import Consumer
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from pysnmp.smi import builder, view, compiler, rfc1902
from pysmi import debug as pysmi_debug
import json
import psycopg2

# c = Consumer({'bootstrap.servers':'kafka1:19091','group.id':'counting-group','auto.offset.reset':'earliest'})
# print('Kafka Consumer has been initiated...')

#print('Available topics to consume: ', c.list_topics().topics)
# c.subscribe(['user-tracker'])

#establishing the connection
# conn = psycopg2.connect(database="postgres", user='postgres', password='postgres', host='postgres', port= '5432')

#Creating a cursor object using the cursor() method
# cursor = conn.cursor()

# sql= '''CREATE TABLE IF NOT EXISTS users (
#     user_id INTEGER PRIMARY KEY,
#     user_name VARCHAR (255),
#     user_address VARCHAR (255),
#     platform VARCHAR (255)
# )'''

# cursor.execute(sql)
# conn.commit()
def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    print('cbFun is called')
    while wholeMsg:
        print('loop...')
        # print(wholeMsg)
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        print('Version: %s' % (msgVer))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message(),)
        print('Notification message from %s:%s: ' % (transportDomain, transportAddress))
        print('ReqMsg: %s' % (reqMsg))
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        print('ReqPDU: %s' % (reqPDU))
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                enterprise = pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                print('Enterprise: %s' % (enterprise))
                agentAdress = pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                print('Agent Address: %s' % (agentAdress))
                genericTrap = pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                print('Generic Trap: %s' % (genericTrap))
                specificTrap = pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                print('Specific Trap: %s' % (specificTrap))
                uptime = pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                print('Uptime: %s' % (uptime))
                varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)
                varBindsList = []
                for oid, val in varBinds:
#                    oid = oid.prettyPrint()
                    print('OID: %s' % (oid))
#                    value = val.prettyPrint()
                    print('Value: %s' % (val))
                    varBindsTuple = (oid,val)
                    varBindsList.append(varBindsTuple)
                # Assemble MIB browser
                mibBuilder = builder.MibBuilder()

                # SI NO FUNCIONA DESCOMENTAR. AQUI SE VE LA RUTA QUE COGE LOS MIBs
                # pysmi_debug.setLogger(pysmi_debug.Debug('compiler'))

                compiler.addMibCompiler(mibBuilder)
                mibViewController = view.MibViewController(mibBuilder)

                # Pre-load MIB modules we expect to work with
                mibBuilder.loadModules('IF-MIB')
                print("TRADUCCION.............")
                # ent = rfc1902.ObjectType(rfc1902.ObjectIdentity(enterprise)).resolveWithMib(mibViewController)
                # print(ent)
                resolvedVarBinds = []
                for x in varBinds:
                    resolvedVarBind = rfc1902.ObjectType(rfc1902.ObjectIdentity(x[0]), x[1]).resolveWithMib(mibViewController)
                    resolvedVarBinds.append(resolvedVarBind)
                    print(resolvedVarBind)
            else:
                mibBuilder = builder.MibBuilder()

                # SI NO FUNCIONA DESCOMENTAR. AQUI SE VE LA RUTA QUE COGE LOS MIBs
                # pysmi_debug.setLogger(pysmi_debug.Debug('compiler'))

                compiler.addMibCompiler(mibBuilder)
                mibViewController = view.MibViewController(mibBuilder)

                # Pre-load MIB modules we expect to work with
                mibBuilder.loadModules('IF-MIB')
                print("TRADUCCION2.............")
                # ent = rfc1902.ObjectType(rfc1902.ObjectIdentity(enterprise)).resolveWithMib(mibViewController)
                # print(ent)
                resolvedVarBinds = []
                varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)
                for oid, val in varBinds:
                    resolvedVarBind = rfc1902.ObjectType(rfc1902.ObjectIdentity(oid), val).resolveWithMib(mibViewController)
                    resolvedVarBinds.append(resolvedVarBind)
                    print(resolvedVarBind)
    return wholeMsg

# while True:
transportDispatcher = AsynsockDispatcher()

transportDispatcher.registerRecvCbFun(cbFun)
print("Corre")
# UDP/IPv4
transportDispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode(('0.0.0.0', 162))
)

# # UDP/IPv6
# transportDispatcher.registerTransport(
#     udp6.domainName, udp6.Udp6SocketTransport().openServerMode(('::1', 163))
# )

transportDispatcher.jobStarted(1)

try:
    # Dispatcher will never finish as job#1 never reaches zero
    print('run dispatcher')
    transportDispatcher.runDispatcher()
except:
    transportDispatcher.closeDispatcher()
    raise    
# msg=c.poll(1.0) #timeout
# if msg is None:
#     continue
# if msg.error():
#     print('Error: {}'.format(msg.error()))
    # continue
#Setting auto commit false
# conn.autocommit = True

#Creating a cursor object using the cursor() method
# cursor = conn.cursor()
# data=json.loads(msg.value().decode('utf-8'))
# cursor.execute(""" INSERT INTO users (user_id, user_name, user_address, platform) VALUES (%s,%s,%s,%s)""",
#     (data['user_id'],
#      data['user_name'],
#      data['user_address'],
#      data['platform']))