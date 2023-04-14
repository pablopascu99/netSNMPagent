from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from pysnmp.smi import builder, view, compiler, rfc1902


def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    print('cbFun is called')
    while wholeMsg:
        print('loop...')
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message(),)
        print('Notification message from %s:%s: ' % (transportDomain, transportAddress))
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
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
                    oid = oid.prettyPrint()
                    print('OID: %s' % (oid))
                    value = val.prettyPrint()
                    print('Value: %s' % (value))
                    varBindsTuple = (oid,value)
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
                varBinds = pMod.apiPDU.getVarBindList(reqPDU)
                varBindsList = []
                for oid, val in varBinds:
                    oid = oid.prettyPrint()
                    print('OID: %s' % (oid))
                    value = val.prettyPrint()
                    print('Value: %s' % (value))
                    varBindsTuple = (oid,value)
                    varBindsList.append(varBindsTuple)
                print("algo")
    return wholeMsg

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

##############################################################################################################################################################
#                                                                                                                                                            #
#  Ejemplo para prueba con snmptrapGen:                                                                                                                      #
#  snmptrapGen -v:1 -c:public -r:127.0.0.1 -to:1.3.6.1.6.3.1.1.4.1.0 -del:'' -eo:1.3.6.1.4.1.8072.3.2.10 -vid:1.3.6.1.6.3.1.1.5.1 -vtp:str -val:"1" -p:163   #
#                                                                                                                                                            #
##############################################################################################################################################################