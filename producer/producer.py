from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from pysnmp.smi import builder, view, compiler, rfc1902
# from pysmi import debug as pysmi_debug

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
                specificTrap = pMod.apiTrapPDU.getSpeciicTrap(reqPDU).prettyPrint()
                print('Specific Trap: %s' % (specificTrap))
                uptime = pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                print('Uptime: %s' % (uptime))
                varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)
                varBindsList = []
                for oid, val in varBinds:
                    # oid = oid.prettyPrint()
                    print('OID: %s' % (oid))
                    # value = val.prettyPrint()
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

# from confluent_kafka import Producer
# from faker import Faker
# import json
# import time
# import logging
# import random 
# fake=Faker()

# logging.basicConfig(format='%(asctime)s %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filename='producer.log',
#                     filemode='w')

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# p = Producer({'bootstrap.servers':'kafka1:19091'})

# print('Kafka Producer has been initiated...')

# def receipt(err,msg):
#     if err is not None:
#         print('Error: {}'.format(err))
#     else:
#         message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
#         logger.info(message)
#         print(message)

# def main():
#     for i in range(1000000):
#         data={
#             'user_id': fake.random_int(min=20000, max=100000),
#             'user_name':fake.name(),
#             'user_address':fake.street_address() + ' | ' + fake.city() + ' | ' + fake.country_code(),
#             'platform': random.choice(['Mobile', 'Laptop', 'Tablet']),
#             }
#         m=json.dumps(data)
#         p.poll(1)
#         # Producimos en el topic user-tracker
#         p.produce('user-tracker', m.encode('utf-8'),callback=receipt)
#         p.flush()
#         time.sleep(1)

# main()